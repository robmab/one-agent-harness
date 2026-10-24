"""Checks that the project's code fits its real stack and compiles.

Usage:
    py -3 check.py [files...]   # no files: the ones changed according to git
    py -3 check.py --hook       # Claude PostToolUse hook mode (reads the JSON from stdin)
    py -3 check.py --selftest   # validates RULES and tests the engine on sample files
    py -3 check.py --all [...]  # audit: the whole file, not just what changed

The rules only look at the lines changed against HEAD, so old code makes no noise; a line that has only
moved gives no warnings, only errors. Syntax is always checked on the whole file.
Exit: 0 if there are no errors (there may be warnings), 1 if there are errors (2 in hook mode).
Standard library only.
"""
import json
import os
import re
import shutil
import subprocess
import sys

# ---------------------------------------------------------------------------
# FILL-IN: project settings
# ---------------------------------------------------------------------------

# file or folder that identifies the repo root (e.g. 'manage.py', 'package.json'); None = any git repo
MARKER = None

# the project's python to compile .py files, relative to the repo root or absolute; the first that exists
# (empty = compiled with the Python running this script, with a warning)
PROJECT_PYTHON = [
    # os.path.join('..', 'env', 'Scripts', 'python.exe'),
    # os.path.join('.venv', 'Scripts', 'python.exe'),
    # os.path.join('.venv', 'bin', 'python'),   # Linux and macOS
]

EXTENSIONS = ('.py', '.js', '.html', '.css')
IGNORE = ('.min.', '/node_modules/', '/dist/', '/build/', '/.venv/', '/vendor/')

# a .js with these marks goes through a template engine before being served: node can't parse it
TEMPLATE_MARKS = ('{{', '{%')

# per-line rules: (level, extensions, regex, message). ERROR blocks; WARNING only informs
RULES = [
    # always on: a password written into a URL (in Claude, guard.py already stops it; this catches the other tools)
    ('ERROR', ('.py', '.js', '.ts', '.html', '.ps1', '.sh'), r'\b[a-z][a-z0-9+.-]*://[^\s:/@\"\'`]+:(?!\*+@|<[^>]*>@|\{[^}]*\}@|\$\w+@)[^\s@\"\'`/]+@',
     'password in plain text (user:password@ in a URL): read the connection from the config file instead'),
    # examples, uncomment and adapt them to the project's real versions:
    # ('ERROR', ('.js', '.html'), r'\bv-slot\b', 'v-slot is Vue 2.6; in this project it is <template slot="x" scope="props">'),
    # ('ERROR', ('.js', '.html'), r'\bdata-bs-[\w-]+', 'data-bs-* is Bootstrap 5; here it is data-toggle, data-target...'),
    # ('ERROR', ('.py',), r'\bmapped_column\b', 'that is SQLAlchemy 2.0; here it is 1.4'),
    # ('WARNING', ('.py', '.js'), r'\b(?:print\(|console\.log\(|debugger\b)', 'debugging leftover'),
]

# ---------------------------------------------------------------------------


def repo_root(path):
    folder = os.path.dirname(os.path.abspath(path)) if os.path.isfile(path) else os.path.abspath(path)
    try:
        return subprocess.run(['git', '-C', folder, 'rev-parse', '--show-toplevel'],
                              capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def is_project(root):
    return bool(root) and (MARKER is None or os.path.exists(os.path.join(root, MARKER)))


def project_python(root):
    for candidate in PROJECT_PYTHON:
        path = candidate if os.path.isabs(candidate) else os.path.join(root, candidate)
        if os.path.isfile(path):
            return os.path.abspath(path)
    return None


def changed_files(root):
    out = set()
    for args in (['diff', '--name-only'], ['diff', '--cached', '--name-only'], ['ls-files', '--others', '--exclude-standard']):
        res = subprocess.run(['git', '-C', root] + args, capture_output=True, text=True)
        out.update(l.strip() for l in res.stdout.splitlines() if l.strip())
    return [os.path.join(root, f) for f in sorted(out)]


def changed_lines(path, root):
    # (line numbers added or modified against HEAD, removed texts); None = look at the whole file
    rel = os.path.relpath(path, root)
    res = subprocess.run(['git', '-C', root, 'diff', '-U0', 'HEAD', '--', rel], capture_output=True, text=True,
                         encoding='utf-8', errors='replace')
    if res.returncode:
        return None, set()
    if not res.stdout.strip():
        new = subprocess.run(['git', '-C', root, 'ls-files', '--error-unmatch', '--', rel], capture_output=True)
        return (None if new.returncode else set()), set()  # untracked: whole file; tracked and unchanged: nothing
    changed = set()
    for m in re.finditer(r'^@@ -\S+ \+(\d+)(?:,(\d+))? @@', res.stdout, re.M):
        start, count = int(m.group(1)), int(m.group(2) or 1)
        changed.update(range(start, start + count))
    removed = {l[1:].strip() for l in res.stdout.splitlines() if l.startswith('-') and not l.startswith('---')}
    return changed, removed


def relevant(path):
    p = path.replace('\\', '/')
    return p.endswith(EXTENSIONS) and not any(i in p for i in IGNORE) and os.path.isfile(path)


def check(path, root, whole=False):
    findings = []  # (level, line, message)
    ext = os.path.splitext(path)[1]
    with open(path, encoding='utf-8', errors='replace') as f:
        text = f.read()
    changed, removed = (None, set()) if whole else changed_lines(path, root)
    for n, line in enumerate(text.splitlines(), 1):
        if changed is not None and n not in changed:
            continue
        for level, exts, pattern, message in RULES:
            if ext not in exts or not re.search(pattern, line):
                continue
            # a line that has only moved (it was already in HEAD): its warnings are old, not from this change
            if level == 'WARNING' and line.strip() in removed:
                continue
            findings.append((level, n, message))
    findings += syntax(path, ext, text, root)
    return sorted(set(findings), key=lambda h: (h[1], h[0]))


def syntax(path, ext, text, root):
    if ext == '.py':
        python = project_python(root)
        warning = [] if python else [('WARNING', 0, 'no project python configured: compiled with the system one')]
        res = subprocess.run([python or sys.executable, '-m', 'py_compile', path], capture_output=True, text=True)
        if res.returncode:
            return warning + [('ERROR', 0, 'py_compile: ' + (res.stderr.strip().splitlines() or ['fails'])[-1])]
        return warning
    if ext == '.js':
        if any(m in text for m in TEMPLATE_MARKS):
            return []
        if not shutil.which('node'):
            return [('WARNING', 0, 'no node: JS syntax not checked')]
        res = subprocess.run(['node', '--check', path], capture_output=True, text=True)
        if res.returncode:
            detail = next((l for l in res.stderr.splitlines() if 'Error' in l), 'fails')
            return [('ERROR', 0, 'node --check: ' + detail.strip())]
    return []


def report(results, root):
    lines = []
    for path, findings in results:
        rel = os.path.relpath(path, root) if root else path
        for level, n, message in findings:
            lines.append(f'{level} {rel}:{n}  {message}' if n else f'{level} {rel}  {message}')
    errors = sum(1 for _, h in results for x in h if x[0] == 'ERROR')
    warnings = sum(1 for _, h in results for x in h if x[0] == 'WARNING')
    return lines, errors, warnings


def hook_mode():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    path = (data.get('tool_input') or {}).get('file_path') or ''
    if not path or not relevant(path):
        return 0
    root = repo_root(path)
    if not is_project(root):
        return 0
    lines, errors, warnings = report([(path, check(path, root))], root)
    if errors:
        print('check found problems in what you just edited:\n' + '\n'.join(lines), file=sys.stderr)
        return 2
    # always one line back, so the agent knows it ran (silence looks the same as a hook that never fired)
    if warnings:
        note = 'check (warnings, see whether they apply):\n' + '\n'.join(lines)
    else:
        note = f'check: OK ({os.path.relpath(path, root)})'
    print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PostToolUse', 'additionalContext': note}}))
    return 0


def selftest():
    import tempfile
    failures = []

    # the project's RULES, well formed
    for i, rule in enumerate(RULES):
        if len(rule) != 4:
            failures.append(f'RULES[{i}]: must have 4 fields (level, extensions, regex, message)')
            continue
        level, exts, pattern, message = rule
        if level not in ('ERROR', 'WARNING'):
            failures.append(f'RULES[{i}]: the level must be ERROR or WARNING, not {level!r}')
        if not isinstance(exts, tuple) or not exts or not all(isinstance(e, str) and e.startswith('.') for e in exts):
            failures.append(f'RULES[{i}]: extensions go in a tuple, e.g. (\'.js\',) or (\'.py\', \'.js\')')
        try:
            re.compile(pattern)
        except re.error as e:
            failures.append(f'RULES[{i}]: the regex does not compile: {e}')
        if not message:
            failures.append(f'RULES[{i}]: the message is missing (say what to use instead)')

    # the engine, with sample rules on temporary files
    demo = [('ERROR', ('.js',), r'\bv-slot\b', 'demo-error'), ('WARNING', ('.js',), r'console\.log\(', 'demo-warning')]
    cases = {
        'bad.js': ('var x = "v-slot";\nconsole.log(x);\n', {'demo-error', 'demo-warning'}, True),
        'good.js': ('var x = 1;\n', set(), False),
        'broken.py': ('def f(:\n    pass\n', set(), True),
        'good.py': ('x = 1\n', set(), False),
    }
    saved = RULES[:]
    RULES[:] = demo
    try:
        with tempfile.TemporaryDirectory() as d:
            for name, (text, expected, with_error) in cases.items():
                path = os.path.join(d, name)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(text)
                findings = check(path, d)
                messages = {m for _, _, m in findings}
                if not expected <= messages:
                    failures.append(f'engine: {name} is missing {sorted(expected - messages)}')
                if with_error != any(n == 'ERROR' for n, _, _ in findings):
                    failures.append(f'engine: {name} expected {"some" if with_error else "no"} ERROR, got {findings}')
            if relevant(os.path.join(d, 'x.min.js')):
                failures.append('engine: .min.* files should be ignored')
    finally:
        RULES[:] = saved
    if is_project(None):
        failures.append('engine: without a git repo it should not count as the project')

    print('\n'.join(failures) if failures else f'selftest OK: {len(RULES)} well-formed rules and the engine works.')
    return 1 if failures else 0


def main():
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    if '--hook' in sys.argv:
        return hook_mode()
    if '--selftest' in sys.argv:
        return selftest()

    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    root = repo_root(args[0] if args else os.getcwd())
    if not is_project(root):
        print("I'm not in the project repo (or there's no git).")
        return 1
    candidates = [os.path.abspath(a) for a in args] if args else changed_files(root)
    candidates = [f for f in candidates if f.endswith(EXTENSIONS) and os.path.isfile(f)]
    files = [f for f in candidates if relevant(f)]
    # say what was skipped: "nothing to check" isn't the same as "it's fine"
    skipped = [os.path.relpath(f, root) for f in candidates if not relevant(f)]
    if not files:
        print('Nothing to check (no code file changed).')
        if skipped:
            print('Not checked (minified, generated…): ' + ', '.join(skipped) + '. This is not an OK.')
        return 0

    lines, errors, warnings = report([(f, check(f, root, '--all' in sys.argv)) for f in files], root)
    print('\n'.join(lines) if lines else 'No problems.')
    print('\nChecked: ' + ', '.join(os.path.relpath(f, root) for f in files))
    if skipped:
        print('Not checked (minified, generated…): ' + ', '.join(skipped) + '. This is not an OK.')
    print(f'{len(files)} files · {errors} errors · {warnings} warnings')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
