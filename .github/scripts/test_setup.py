"""End-to-end test of setup.py on a temporary copy of the template, with fake user profiles. Windows only.

Run from anywhere: python .github/scripts/test_setup.py [en|es ...]   (default: every language in i18n/ plus en)
It never touches your real profile: every link goes into the temporary folder (setup.py --home).
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
failures = []


def expect(cond, msg):
    if not cond:
        failures.append(msg)
        print('  FAIL ' + msg)


def run(harness, *args):
    res = subprocess.run([sys.executable, os.path.join(harness, 'setup.py')] + list(args),
                         capture_output=True, text=True, encoding='utf-8')
    return res.returncode, res.stdout + res.stderr


def read(path):
    with io.open(path, encoding='utf-8') as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(text)


def same(a, b):
    try:
        return os.path.samefile(a, b)
    except OSError:
        return False


def junction_to(link, target):
    try:
        t = os.readlink(link)
    except OSError:
        return False
    t = t[4:] if t.startswith('\\\\?\\') else t
    return os.path.normcase(os.path.abspath(t)) == os.path.normcase(os.path.abspath(target))


def copy_template(dest):
    # what a release zip has: no .git, no .github (export-ignore)
    shutil.copytree(REPO, dest, ignore=shutil.ignore_patterns('.git', '.github', '__pycache__', '.setup.json'))
    plugins = os.path.join(dest, 'claude', 'plugins')
    if os.path.isdir(plugins):
        shutil.rmtree(plugins)


def test(lang, base):
    print(f'\n=== {lang}')
    h = os.path.join(base, f'Harness {lang}')   # with a space on purpose
    copy_template(h)
    home, home2 = os.path.join(base, f'home-{lang}'), os.path.join(base, f'home2-{lang}')
    # home: lived-in profile (Claude settings, VS Code settings ending in a // comment, other skills)
    write(os.path.join(home, '.claude', 'settings.json'), json.dumps({'theme': 'dark', 'hooks': {}}, indent=2))
    write(os.path.join(home, 'AppData', 'Roaming', 'Code', 'User', 'settings.json'),
          '{\n  "editor.fontSize": 14 // mine\n}\n')
    write(os.path.join(home, '.copilot', 'skills', 'other-skill', 'SKILL.md'), 'x')
    # home2: empty profile, except a VS Code settings file with CRLF and no final newline
    vs2 = os.path.join(home2, 'AppData', 'Roaming', 'Code', 'User', 'settings.json')
    vs2_text = '{\r\n  "editor.tabSize": 2\r\n}'
    write(vs2, vs2_text)

    code, out = run(h, '--project', 'Demo App', '--lang', lang, '--home', home, '--home', home2,
                    '--vscode-permissions')
    print(out)
    expect(code == 0, f'{lang}: setup exited {code}')
    names = json.loads(read(os.path.join(REPO, 'i18n', lang, 'names.json')))['rename'] if lang != 'en' else {}

    def to(p):
        # where a template path ends up: its own rename and its folder's
        p = names.get(p, p)
        for old, new in names.items():
            if p.startswith(old + '/'):
                p = new + p[len(old):]
        return p

    # names and placeholders
    expect(not os.path.isdir(os.path.join(h, 'i18n')), f'{lang}: i18n\\ should be gone')
    router = os.path.join(h, 'copilot', 'demo-app.instructions.md')
    expect(os.path.isfile(router), f'{lang}: router not renamed')
    for folder, _, files in os.walk(h):
        for f in files:
            p = os.path.join(folder, f)
            rel = os.path.relpath(p, h).replace('\\', '/')
            if rel.split('/')[0] in ('claude', 'copilot', 'opencode', 'personal') and f.endswith(
                    ('.md', '.py', '.ts', '.json', '.jsonc', '.ps1')):
                t = read(p)
                expect('<PROJECT>' not in t and '<HARNESS>' not in t, f'{lang}: placeholder left in {rel}')
                if f.endswith(('.json', '.jsonc', '.ts')):
                    expect(h not in t, f'{lang}: backslash path in {rel} (escapes in JSON/TS)')
    expect('`demo-app:' in read(os.path.join(h, 'claude', 'CLAUDE.md')), f'{lang}: CLAUDE.md prefix')
    expect('`project:' not in read(os.path.join(h, 'claude', 'CLAUDE.md')), f'{lang}: CLAUDE.md old prefix')
    mp = json.loads(read(os.path.join(h, 'claude', '.claude-plugin', 'marketplace.json')))
    expect(mp['name'] == 'harness-demo-app' and mp['plugins'][0]['source'] == './plugins/demo-app',
           f'{lang}: marketplace')
    expect('sensor-demo-app' in read(os.path.join(h, 'opencode', 'plugins', 'sensor.ts')), f'{lang}: plugin id')
    cfg = read(os.path.join(h, 'opencode', 'opencode.jsonc'))
    json.loads(re.sub(r'(?m)^\s*//.*$', '', cfg))
    skills = sorted(os.listdir(os.path.join(h, 'personal', 'skills')))
    for s in skills:
        expect(f'"resource": "{s}"' in cfg, f'{lang}: skill {s} missing from the OpenCode allowlist')
        m = re.search(r'(?m)^name:\s*(\S+)', read(os.path.join(h, 'personal', 'skills', s, 'SKILL.md')))
        expect(m and m.group(1) == s, f'{lang}: skill {s} name does not match its folder')
    for old in names:
        expect(os.path.exists(os.path.join(h, *to(old).split('/'))), f'{lang}: {to(old)} missing')
        expect(not os.path.exists(os.path.join(h, *old.split('/'))), f'{lang}: {old} still there')
    agent = os.path.splitext(os.path.splitext(to('personal/agents/reviewer.agent.md').split('/')[-1])[0])[0]
    expect(os.path.isfile(os.path.join(h, 'opencode', 'agents', agent + '.md')), f'{lang}: OpenCode agent copy')
    expect(os.path.isfile(os.path.join(h, 'copilot', 'agents', agent + '.agent.md')), f'{lang}: Copilot agent copy')
    expect(f'--agent {agent}' in read(os.path.join(h, 'opencode', 'scripts', 'review-pending.ps1')),
           f'{lang}: review-pending.ps1 uses another agent name')

    # links
    expect(junction_to(os.path.join(h, 'claude', 'plugins', 'demo-app'), os.path.join(h, 'personal')),
           f'{lang}: plugin junction')
    for hm in (home, home2):
        for p in (('.copilot', 'copilot-instructions.md'), ('.config', 'opencode', 'AGENTS.md')):
            expect(same(os.path.join(hm, *p), router), f'{lang}: router hardlink {os.path.join(*p)} in {hm}')
        expect(junction_to(os.path.join(hm, '.config', 'opencode', 'skills'), os.path.join(h, 'personal', 'skills')),
               f'{lang}: opencode skills junction in {hm}')
        s = json.loads(read(os.path.join(hm, '.claude', 'settings.json')))
        expect(s['enabledPlugins'].get('demo-app@harness-demo-app') is True, f'{lang}: plugin enabled in {hm}')
        expect(s['extraKnownMarketplaces']['harness-demo-app']['source']['path'] == os.path.join(h, 'claude'),
               f'{lang}: marketplace path in {hm}')
    expect(junction_to(os.path.join(home2, '.copilot', 'skills'), os.path.join(h, 'personal', 'skills')),
           f'{lang}: copilot skills junction (empty profile)')
    for s in skills:   # home already had its own skill: one junction per skill, the other one untouched
        expect(junction_to(os.path.join(home, '.copilot', 'skills', s), os.path.join(h, 'personal', 'skills', s)),
               f'{lang}: per-skill junction {s}')
    expect(os.path.isfile(os.path.join(home, '.copilot', 'skills', 'other-skill', 'SKILL.md')),
           f'{lang}: the user\'s own skill was touched')
    expect(json.loads(read(os.path.join(home, '.claude', 'settings.json')))['theme'] == 'dark',
           f'{lang}: Claude settings lost a key')
    vs = read(os.path.join(home, 'AppData', 'Roaming', 'Code', 'User', 'settings.json'))
    clean = re.sub(r'(?m)\s*//.*$', '', vs)   # the test's paths have no //, so this is enough here
    data = json.loads(clean)
    expect(data['github.copilot.chat.additionalReadAccessPaths'] == [h], f'{lang}: VS Code read path')
    rule = next(iter(data['chat.tools.terminal.autoApprove'])).strip('/')
    check_py = os.path.join(h, 'personal', 'scripts', 'check.py')
    expect(re.search(rule, f'py -3 {check_py} a.js') and not re.search(rule, f'py -3 {check_py}x'),
           f'{lang}: VS Code sensor rule')
    expect(data['editor.fontSize'] == 14, f'{lang}: VS Code settings lost a key')

    # idempotent
    code, out = run(h, '--home', home, '--home', home2)
    expect(code == 0 and not re.search(r'(?m)^  (done|backup) ', out), f'{lang}: second run changed things:\n{out}')

    # --check repairs a hardlink broken by an editor (same text) and a missing junction
    link = os.path.join(home, '.copilot', 'copilot-instructions.md')
    text = read(link)
    os.remove(link)
    write(link, text)
    os.rmdir(os.path.join(home2, '.config', 'opencode', 'skills'))
    code, out = run(h, '--check')
    print(out)
    expect(code == 0 and out.count('fixed') == 2, f'{lang}: --check should fix 2 things')
    expect(same(link, router), f'{lang}: --check did not restore the hardlink')
    # ...but not one with other content
    os.remove(link)
    write(link, text + '\nmy change\n')
    code, out = run(h, '--check')
    expect(code == 1 and 'PROBLEM' in out, f'{lang}: --check should report the changed copy')
    expect(read(link).endswith('my change\n'), f'{lang}: --check overwrote a changed copy')
    os.remove(link)

    # language and project are chosen once
    other = 'es' if lang == 'en' else 'en'
    code, out = run(h, '--lang', other, '--home', home)
    expect(code == 1, f'{lang}: changing the language should fail')

    # uninstall leaves the profiles as they were, and the harness intact
    code, out = run(h, '--uninstall')
    print(out)
    expect(code == 0, f'{lang}: uninstall exited {code}')
    for hm in (home, home2):
        for p in (('.copilot', 'agents'), ('.config', 'opencode', 'skills'), ('.config', 'opencode', 'AGENTS.md')):
            expect(not os.path.lexists(os.path.join(hm, *p)), f'{lang}: {os.path.join(*p)} left in {hm}')
        s = json.loads(read(os.path.join(hm, '.claude', 'settings.json')))
        expect('harness-demo-app' not in s.get('extraKnownMarketplaces', {}), f'{lang}: marketplace left in {hm}')
    for s in skills:
        expect(not os.path.lexists(os.path.join(home, '.copilot', 'skills', s)), f'{lang}: skill link {s} left')
    expect(os.path.isfile(os.path.join(home, '.copilot', 'skills', 'other-skill', 'SKILL.md')),
           f'{lang}: uninstall touched the user\'s own skill')
    expect(json.loads(re.sub(r'(?m)\s*//.*$', '', read(os.path.join(home, 'AppData', 'Roaming', 'Code', 'User',
                                                                     'settings.json')))) == {'editor.fontSize': 14},
           f'{lang}: VS Code settings not restored')
    with open(vs2, 'rb') as f:
        expect(f.read() == vs2_text.encode(), f'{lang}: VS Code settings (CRLF) not restored byte for byte')
    expect(not os.path.lexists(os.path.join(h, 'claude', 'plugins', 'demo-app')), f'{lang}: plugin junction left')
    expect(os.path.isdir(os.path.join(h, 'personal', 'skills')) and skills == sorted(
        os.listdir(os.path.join(h, 'personal', 'skills'))), f'{lang}: uninstall damaged the harness')

    # the template repo itself is refused
    code, out = run(REPO, '--project', 'X', '--dry-run', '--home', home)
    expect(code != 0 and '.github' in out, f'{lang}: setup should refuse to run on the template repo')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if os.name != 'nt':
        print('setup.py is Windows only: nothing to test here.')
        return 0
    i18n = os.path.join(REPO, 'i18n')
    langs = sys.argv[1:] or ['en'] + (sorted(os.listdir(i18n)) if os.path.isdir(i18n) else [])
    base = tempfile.mkdtemp(prefix='harness-test-')
    try:
        for lang in langs:
            test(lang, base)
    finally:
        # junctions first, so rmtree never walks into what they point to
        for folder, dirs, _ in os.walk(base, topdown=True):
            for d in list(dirs):
                p = os.path.join(folder, d)
                if _is_junction(p):
                    os.rmdir(p)
                    dirs.remove(d)
        shutil.rmtree(base, ignore_errors=True)
    print(f'\n{len(failures)} failures' if failures else '\nsetup.py: all good.')
    return 1 if failures else 0


def _is_junction(p):
    try:
        import stat
        return os.lstat(p).st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT
    except (OSError, AttributeError):
        return False


if __name__ == '__main__':
    sys.exit(main())
