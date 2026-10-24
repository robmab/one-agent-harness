"""Comprueba que el código del proyecto encaja con su stack real y que compila.

Uso:
    py -3 check.py [ficheros...]   # sin ficheros: los cambiados según git
    py -3 check.py --hook          # modo hook PostToolUse de Claude (lee el JSON por stdin)
    py -3 check.py --selftest      # valida RULES y prueba el motor con ficheros de ejemplo
    py -3 check.py --all [...]     # auditoría: el fichero entero, no solo lo cambiado

Las reglas solo miran las líneas cambiadas respecto a HEAD, para que el código antiguo no haga ruido; una línea
que solo ha cambiado de sitio no da avisos, solo errores. La sintaxis se comprueba siempre con el fichero entero.
Salida: 0 si no hay errores (puede haber avisos), 1 si hay errores (2 en modo hook).
Solo usa la librería estándar.
"""
import json
import os
import re
import shutil
import subprocess
import sys

# ---------------------------------------------------------------------------
# FILL-IN: configuración del proyecto
# ---------------------------------------------------------------------------

# fichero o carpeta que identifica la raíz del repo (p. ej. 'manage.py', 'package.json'); None = cualquier repo git
MARKER = None

# python del proyecto para compilar los .py, relativo a la raíz del repo o absoluto; el primero que exista
# (vacío = se compila con el Python que lanza el script, y se avisa)
PROJECT_PYTHON = [
    # os.path.join('..', 'env', 'Scripts', 'python.exe'),
    # os.path.join('.venv', 'Scripts', 'python.exe'),
    # os.path.join('.venv', 'bin', 'python'),   # Linux y macOS
]

EXTENSIONS = ('.py', '.js', '.html', '.css')
IGNORE = ('.min.', '/node_modules/', '/dist/', '/build/', '/.venv/', '/vendor/')

# un .js con estas marcas pasa por un motor de plantillas antes de servirse: node no lo puede parsear
TEMPLATE_MARKS = ('{{', '{%')

# reglas por línea: (nivel, extensiones, regex, mensaje). ERROR bloquea; WARNING solo informa
RULES = [
    # siempre activa: una contraseña escrita en una URL (en Claude ya la para guard.py; esta pilla al resto)
    ('ERROR', ('.py', '.js', '.ts', '.html', '.ps1', '.sh'), r'\b[a-z][a-z0-9+.-]*://[^\s:/@\"\'`]+:(?!\*+@|<[^>]*>@|\{[^}]*\}@|\$\w+@)[^\s@\"\'`/]+@',
     'contraseña en claro (usuario:contraseña@ en una URL): lee la conexión del fichero de configuración'),
    # ejemplos, descomenta y adapta a las versiones reales del proyecto:
    # ('ERROR', ('.js', '.html'), r'\bv-slot\b', 'v-slot es de Vue 2.6; en este proyecto es <template slot="x" scope="props">'),
    # ('ERROR', ('.js', '.html'), r'\bdata-bs-[\w-]+', 'data-bs-* es de Bootstrap 5; aquí es data-toggle, data-target...'),
    # ('ERROR', ('.py',), r'\bmapped_column\b', 'eso es de SQLAlchemy 2.0; aquí 1.4'),
    # ('WARNING', ('.py', '.js'), r'\b(?:print\(|console\.log\(|debugger\b)', 'resto de depuración'),
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
    # (números de línea añadidos o modificados respecto a HEAD, textos quitados); None = mirar el fichero entero
    rel = os.path.relpath(path, root)
    res = subprocess.run(['git', '-C', root, 'diff', '-U0', 'HEAD', '--', rel], capture_output=True, text=True,
                         encoding='utf-8', errors='replace')
    if res.returncode:
        return None, set()
    if not res.stdout.strip():
        new = subprocess.run(['git', '-C', root, 'ls-files', '--error-unmatch', '--', rel], capture_output=True)
        return (None if new.returncode else set()), set()  # sin trackear: entero; trackeado sin cambios: nada
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
    findings = []  # (nivel, línea, mensaje)
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
            # línea que solo ha cambiado de sitio (ya estaba en HEAD): sus avisos son de antes, no del cambio
            if level == 'WARNING' and line.strip() in removed:
                continue
            findings.append((level, n, message))
    findings += syntax(path, ext, text, root)
    return sorted(set(findings), key=lambda h: (h[1], h[0]))


def syntax(path, ext, text, root):
    if ext == '.py':
        python = project_python(root)
        warning = [] if python else [('WARNING', 0, 'sin python del proyecto configurado: compilado con el del sistema')]
        res = subprocess.run([python or sys.executable, '-m', 'py_compile', path], capture_output=True, text=True)
        if res.returncode:
            return warning + [('ERROR', 0, 'py_compile: ' + (res.stderr.strip().splitlines() or ['falla'])[-1])]
        return warning
    if ext == '.js':
        if any(m in text for m in TEMPLATE_MARKS):
            return []
        if not shutil.which('node'):
            return [('WARNING', 0, 'no hay node: sintaxis JS sin comprobar')]
        res = subprocess.run(['node', '--check', path], capture_output=True, text=True)
        if res.returncode:
            detail = next((l for l in res.stderr.splitlines() if 'Error' in l), 'falla')
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
        print('check encontró problemas en lo que acabas de editar:\n' + '\n'.join(lines), file=sys.stderr)
        return 2
    # deja siempre una línea, para que el agente sepa que ha pasado (el silencio es igual que un hook que no saltó)
    if warnings:
        note = 'check (avisos, revisa si aplican):\n' + '\n'.join(lines)
    else:
        note = f'check: OK ({os.path.relpath(path, root)})'
    print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PostToolUse', 'additionalContext': note}}))
    return 0


def selftest():
    import tempfile
    failures = []

    # las RULES del proyecto, bien formadas
    for i, rule in enumerate(RULES):
        if len(rule) != 4:
            failures.append(f'RULES[{i}]: tiene que tener 4 campos (nivel, extensiones, regex, mensaje)')
            continue
        level, exts, pattern, message = rule
        if level not in ('ERROR', 'WARNING'):
            failures.append(f'RULES[{i}]: el nivel tiene que ser ERROR o WARNING, no {level!r}')
        if not isinstance(exts, tuple) or not exts or not all(isinstance(e, str) and e.startswith('.') for e in exts):
            failures.append(f'RULES[{i}]: las extensiones van en una tupla, p. ej. (\'.js\',) o (\'.py\', \'.js\')')
        try:
            re.compile(pattern)
        except re.error as e:
            failures.append(f'RULES[{i}]: la regex no compila: {e}')
        if not message:
            failures.append(f'RULES[{i}]: falta el mensaje (di qué poner en su lugar)')

    # el motor, con reglas de ejemplo sobre ficheros temporales
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
                    failures.append(f'motor: en {name} faltan {sorted(expected - messages)}')
                if with_error != any(n == 'ERROR' for n, _, _ in findings):
                    failures.append(f'motor: en {name} se esperaba {"algún" if with_error else "ningún"} ERROR, salió {findings}')
            if relevant(os.path.join(d, 'x.min.js')):
                failures.append('motor: los .min.* tendrían que ignorarse')
    finally:
        RULES[:] = saved
    if is_project(None):
        failures.append('motor: sin repo git no tendría que considerarse proyecto')

    print('\n'.join(failures) if failures else f'selftest OK: {len(RULES)} reglas bien formadas y el motor funciona.')
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
        print('No estoy en el repo del proyecto (o no hay git).')
        return 1
    candidates = [os.path.abspath(a) for a in args] if args else changed_files(root)
    candidates = [f for f in candidates if f.endswith(EXTENSIONS) and os.path.isfile(f)]
    files = [f for f in candidates if relevant(f)]
    # di lo que se ha saltado: "nada que comprobar" no es lo mismo que "está bien"
    skipped = [os.path.relpath(f, root) for f in candidates if not relevant(f)]
    if not files:
        print('Nada que comprobar (ningún fichero de código cambiado).')
        if skipped:
            print('Sin mirar (minificados, generados…): ' + ', '.join(skipped) + '. No es un visto bueno.')
        return 0

    lines, errors, warnings = report([(f, check(f, root, '--all' in sys.argv)) for f in files], root)
    print('\n'.join(lines) if lines else 'Sin problemas.')
    print('\nMirados: ' + ', '.join(os.path.relpath(f, root) for f in files))
    if skipped:
        print('Sin mirar (minificados, generados…): ' + ', '.join(skipped) + '. No es un visto bueno.')
    print(f'{len(files)} ficheros · {errors} errores · {warnings} avisos')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
