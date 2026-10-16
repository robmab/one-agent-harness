"""End-to-end test of setup.py on a temporary copy of the template, with fake user profiles.

Run from anywhere: python .github/scripts/test_setup.py [en|es ...]   (default: every language in i18n/ plus en)
It never touches your real profile: every link goes into the temporary folder (setup.py --home).
On Linux and macOS it tests that system. On Windows it tests Windows (junctions and hardlinks) and, if this
user can create symlinks (Developer Mode), also how Linux and macOS are set up (setup.py --platform).
"""
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, REPO)
import setup as harness_setup   # noqa: E402  (vscode_path and the launchers, without running anything)

failures = []


def expect(cond, msg):
    if not cond:
        failures.append(msg)
        print('  FAIL ' + msg)


def run(harness, system, *args):
    res = subprocess.run([sys.executable, os.path.join(harness, 'setup.py'), '--platform', system] + list(args),
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


def links_to(link, target):
    try:
        t = os.readlink(link)
    except OSError:
        return False
    t = t[4:] if t.startswith('\\\\?\\') else t
    return os.path.normcase(os.path.realpath(t)) == os.path.normcase(os.path.realpath(target))


def is_dir_link(p):
    if os.path.islink(p):
        return True
    try:
        return os.lstat(p).st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT
    except (OSError, AttributeError):
        return False


def remove_dir_link(p):
    if os.name == 'nt':
        os.rmdir(p)   # junction or folder symlink
    else:
        os.unlink(p)


def symlinks_available():
    d = tempfile.mkdtemp(prefix='harness-symlink-')
    try:
        os.symlink(d, os.path.join(d, 'l'), target_is_directory=True)
        return True
    except OSError:
        return False
    finally:
        shutil.rmtree(d, ignore_errors=True)


def copy_template(dest):
    # what a release zip has: no .git, no .github (export-ignore)
    shutil.copytree(REPO, dest, ignore=shutil.ignore_patterns('.git', '.github', '__pycache__', '.setup.json'))
    plugins = os.path.join(dest, 'claude', 'plugins')
    if os.path.isdir(plugins):
        shutil.rmtree(plugins)


def test(lang, system, base):
    print(f'\n=== {lang} · {system}')
    tag = f'{lang}/{system}'
    launcher = harness_setup.LAUNCHERS[system]
    h = os.path.join(base, f'Harness {lang} {system}')   # with spaces on purpose
    copy_template(h)
    home, home2 = os.path.join(base, f'home-{lang}-{system}'), os.path.join(base, f'home2-{lang}-{system}')
    vs = harness_setup.vscode_path(home, system)
    vs2 = harness_setup.vscode_path(home2, system)
    # home: lived-in profile (Claude settings, VS Code settings ending in a // comment, other skills)
    write(os.path.join(home, '.claude', 'settings.json'), json.dumps({'theme': 'dark', 'hooks': {}}, indent=2))
    write(vs, '{\n  "editor.fontSize": 14 // mine\n}\n')
    write(os.path.join(home, '.copilot', 'skills', 'other-skill', 'SKILL.md'), 'x')
    # home2: empty profile, except a VS Code settings file with CRLF and no final newline
    vs2_text = '{\r\n  "editor.tabSize": 2\r\n}'
    write(vs2, vs2_text)

    code, out = run(h, system, '--project', 'Demo App', '--lang', lang, '--home', home, '--home', home2,
                    '--vscode-permissions')
    print(out)
    expect(code == 0, f'{tag}: setup exited {code}')
    names = json.loads(read(os.path.join(REPO, 'i18n', lang, 'names.json')))['rename'] if lang != 'en' else {}

    def to(p):
        # where a template path ends up: its own rename and its folder's
        p = names.get(p, p)
        for old, new in names.items():
            if p.startswith(old + '/'):
                p = new + p[len(old):]
        return p

    # names, placeholders, launcher and paths
    expect(not os.path.isdir(os.path.join(h, 'i18n')), f'{tag}: i18n should be gone')
    expect(not os.path.isdir(os.path.join(h, 'profiles')), f'{tag}: profiles should be gone (no profile chosen)')
    router = os.path.join(h, 'copilot', 'demo-app.instructions.md')
    expect(os.path.isfile(router), f'{tag}: router not renamed')
    for folder, dirs, files in os.walk(h):
        dirs[:] = [d for d in dirs if not is_dir_link(os.path.join(folder, d))]
        for f in files:
            p = os.path.join(folder, f)
            rel = os.path.relpath(p, h).replace('\\', '/')
            if rel.split('/')[0] in ('claude', 'copilot', 'opencode', 'personal') and f.endswith(
                    ('.md', '.py', '.ts', '.json', '.jsonc', '.ps1')):
                t = read(p)
                expect('<PROJECT>' not in t and '<HARNESS>' not in t, f'{tag}: placeholder left in {rel}')
                if '\\' in h and f.endswith(('.json', '.jsonc', '.ts')):
                    expect(h not in t, f'{tag}: backslash path in {rel} (escapes in JSON/TS)')
                if system != 'windows':
                    expect('py -3' not in t, f'{tag}: py -3 left in {rel}')
                    expect(h + '\\personal' not in t, f'{tag}: Windows path under the harness in {rel}')
                    if f.endswith('.md'):
                        found = re.findall(r'\b(?:personal|claude|copilot|opencode|checklists)\\\w', t)
                        expect(not found, f'{tag}: Windows-style paths in {rel}: {found}')
    sensor_cmd = f'{launcher} {h}' + ('\\personal\\scripts\\check.py' if system == 'windows'
                                      else '/personal/scripts/check.py')
    expect(sensor_cmd in read(router), f'{tag}: the router should run "{sensor_cmd}"')
    hook = json.loads(read(os.path.join(h, 'personal', 'hooks', 'hooks.json')))
    expect(hook['hooks']['PostToolUse'][0]['hooks'][0]['command']
           == f'{launcher} "${{CLAUDE_PLUGIN_ROOT}}/scripts/check.py" --hook', f'{tag}: hook launcher')
    sensor_ts = read(os.path.join(h, 'opencode', 'plugins', 'sensor.ts'))
    expect(('spawn("py", ["-3", SENSOR' if system == 'windows' else 'spawn("python3", [SENSOR') in sensor_ts,
           f'{tag}: OpenCode plugin launcher')
    expect('sensor-demo-app' in sensor_ts, f'{tag}: plugin id')
    expect('`demo-app:' in read(os.path.join(h, 'claude', 'CLAUDE.md')), f'{tag}: CLAUDE.md prefix')
    expect('`project:' not in read(os.path.join(h, 'claude', 'CLAUDE.md')), f'{tag}: CLAUDE.md old prefix')
    mp = json.loads(read(os.path.join(h, 'claude', '.claude-plugin', 'marketplace.json')))
    expect(mp['name'] == 'harness-demo-app' and mp['plugins'][0]['source'] == './plugins/demo-app',
           f'{tag}: marketplace')
    cfg = read(os.path.join(h, 'opencode', 'opencode.jsonc'))
    json.loads(re.sub(r'(?m)^\s*//.*$', '', cfg))
    skills = sorted(os.listdir(os.path.join(h, 'personal', 'skills')))
    for s in skills:
        expect(f'"resource": "{s}"' in cfg, f'{tag}: skill {s} missing from the OpenCode allowlist')
        m = re.search(r'(?m)^name:\s*(\S+)', read(os.path.join(h, 'personal', 'skills', s, 'SKILL.md')))
        expect(m and m.group(1) == s, f'{tag}: skill {s} name does not match its folder')
    for old in names:
        if old.startswith('profiles/'):
            continue   # dropped after setup: only the chosen profile's content stays, in personal/
        expect(os.path.exists(os.path.join(h, *to(old).split('/'))), f'{tag}: {to(old)} missing')
        expect(not os.path.exists(os.path.join(h, *old.split('/'))), f'{tag}: {old} still there')
    agent = os.path.splitext(os.path.splitext(to('personal/agents/reviewer.agent.md').split('/')[-1])[0])[0]
    expect(os.path.isfile(os.path.join(h, 'opencode', 'agents', agent + '.md')), f'{tag}: OpenCode agent copy')
    expect(os.path.isfile(os.path.join(h, 'copilot', 'agents', agent + '.agent.md')), f'{tag}: Copilot agent copy')
    expect(f'--agent {agent}' in read(os.path.join(h, 'opencode', 'scripts', 'review-pending.ps1')),
           f'{tag}: review-pending.ps1 uses another agent name')

    # links: junctions and hardlinks on Windows, symlinks elsewhere
    expect(links_to(os.path.join(h, 'claude', 'plugins', 'demo-app'), os.path.join(h, 'personal')),
           f'{tag}: plugin link')
    for hm in (home, home2):
        for p in (('.copilot', 'copilot-instructions.md'), ('.config', 'opencode', 'AGENTS.md')):
            link = os.path.join(hm, *p)
            expect(same(link, router), f'{tag}: router link {os.path.join(*p)} in {hm}')
            expect(os.path.islink(link) == (system != 'windows'),
                   f'{tag}: {os.path.join(*p)} should be a {"hardlink" if system == "windows" else "symlink"}')
        expect(links_to(os.path.join(hm, '.config', 'opencode', 'skills'), os.path.join(h, 'personal', 'skills')),
               f'{tag}: opencode skills link in {hm}')
        s = json.loads(read(os.path.join(hm, '.claude', 'settings.json')))
        expect(s['enabledPlugins'].get('demo-app@harness-demo-app') is True, f'{tag}: plugin enabled in {hm}')
        expect(s['extraKnownMarketplaces']['harness-demo-app']['source']['path'] == os.path.join(h, 'claude'),
               f'{tag}: marketplace path in {hm}')
    expect(links_to(os.path.join(home2, '.copilot', 'skills'), os.path.join(h, 'personal', 'skills')),
           f'{tag}: copilot skills link (empty profile)')
    for s in skills:   # home already had its own skill: one link per skill, the other one untouched
        expect(links_to(os.path.join(home, '.copilot', 'skills', s), os.path.join(h, 'personal', 'skills', s)),
               f'{tag}: per-skill link {s}')
    expect(os.path.isfile(os.path.join(home, '.copilot', 'skills', 'other-skill', 'SKILL.md')),
           f'{tag}: the user\'s own skill was touched')
    expect(json.loads(read(os.path.join(home, '.claude', 'settings.json')))['theme'] == 'dark',
           f'{tag}: Claude settings lost a key')
    clean = re.sub(r'(?m)\s*//.*$', '', read(vs))   # the test's paths have no //, so this is enough here
    data = json.loads(clean)
    expect(data['github.copilot.chat.additionalReadAccessPaths'] == [h], f'{tag}: VS Code read path')
    rule = next(iter(data['chat.tools.terminal.autoApprove'])).strip('/')
    check_py = os.path.join(h, 'personal', 'scripts', 'check.py')
    expect(re.search(rule, f'{launcher} {check_py} a.js') and not re.search(rule, f'{launcher} {check_py}x'),
           f'{tag}: VS Code sensor rule')
    expect(data['editor.fontSize'] == 14, f'{tag}: VS Code settings lost a key')

    # idempotent
    code, out = run(h, system, '--home', home, '--home', home2)
    expect(code == 0 and not re.search(r'(?m)^  (done|backup) ', out), f'{tag}: second run changed things:\n{out}')

    # --check repairs a file link broken by an editor (same text) and a missing folder link
    link = os.path.join(home, '.copilot', 'copilot-instructions.md')
    text = read(link)
    os.remove(link)
    write(link, text)
    remove_dir_link(os.path.join(home2, '.config', 'opencode', 'skills'))
    code, out = run(h, system, '--check')
    print(out)
    expect(code == 0 and out.count('fixed') == 2, f'{tag}: --check should fix 2 things')
    expect(same(link, router), f'{tag}: --check did not restore the router link')
    # ...but not one with other content
    os.remove(link)
    write(link, text + '\nmy change\n')
    code, out = run(h, system, '--check')
    expect(code == 1 and 'PROBLEM' in out, f'{tag}: --check should report the changed copy')
    expect(read(link).endswith('my change\n'), f'{tag}: --check overwrote a changed copy')
    os.remove(link)

    # language and project are chosen once
    other = 'es' if lang == 'en' else 'en'
    code, out = run(h, system, '--lang', other, '--home', home)
    expect(code == 1, f'{tag}: changing the language should fail')

    # uninstall leaves the profiles as they were, and the harness intact
    code, out = run(h, system, '--uninstall')
    print(out)
    expect(code == 0, f'{tag}: uninstall exited {code}')
    for hm in (home, home2):
        for p in (('.copilot', 'agents'), ('.config', 'opencode', 'skills'), ('.config', 'opencode', 'AGENTS.md')):
            expect(not os.path.lexists(os.path.join(hm, *p)), f'{tag}: {os.path.join(*p)} left in {hm}')
        s = json.loads(read(os.path.join(hm, '.claude', 'settings.json')))
        expect('harness-demo-app' not in s.get('extraKnownMarketplaces', {}), f'{tag}: marketplace left in {hm}')
    for s in skills:
        expect(not os.path.lexists(os.path.join(home, '.copilot', 'skills', s)), f'{tag}: skill link {s} left')
    expect(os.path.isfile(os.path.join(home, '.copilot', 'skills', 'other-skill', 'SKILL.md')),
           f'{tag}: uninstall touched the user\'s own skill')
    expect(json.loads(re.sub(r'(?m)\s*//.*$', '', read(vs))) == {'editor.fontSize': 14},
           f'{tag}: VS Code settings not restored')
    with open(vs2, 'rb') as f:
        expect(f.read() == vs2_text.encode(), f'{tag}: VS Code settings (CRLF) not restored byte for byte')
    # one backup per file, the one from before the first change, however many times it ran
    for folder, original in ((os.path.join(home, '.claude'), None), (os.path.dirname(vs2), vs2_text)):
        backups = [f for f in os.listdir(folder) if f.startswith('settings.json.')]
        expect(backups == ['settings.json.before-harness'], f'{tag}: backups in {folder}: {backups}')
        if original and backups:
            with open(os.path.join(folder, backups[0]), 'rb') as f:
                expect(f.read() == original.encode(), f'{tag}: the backup is not the original file')
    expect(not os.path.lexists(os.path.join(h, 'claude', 'plugins', 'demo-app')), f'{tag}: plugin link left')
    expect(os.path.isdir(os.path.join(h, 'personal', 'skills')) and skills == sorted(
        os.listdir(os.path.join(h, 'personal', 'skills'))), f'{tag}: uninstall damaged the harness')

    # the template repo itself is refused
    code, out = run(REPO, system, '--project', 'X', '--dry-run', '--home', home)
    expect(code != 0 and '.github' in out, f'{tag}: setup should refuse to run on the template repo')


def test_profile(lang, system, base, profile='web'):
    print(f'\n=== {lang} · {system} · --profile {profile}')
    tag = f'{lang}/{system}/{profile}'
    h = os.path.join(base, f'Harness {lang} {system} {profile}')
    copy_template(h)
    home = os.path.join(base, f'home-{lang}-{system}-{profile}')
    code, out = run(h, system, '--project', 'Web App', '--lang', lang, '--profile', profile, '--home', home)
    print(out)
    expect(code == 0, f'{tag}: setup exited {code}')
    expect(not os.path.isdir(os.path.join(h, 'profiles')), f'{tag}: profiles should be gone')
    skills = os.path.join(h, 'personal', 'skills')
    filled = 0
    for s in sorted(os.listdir(skills)):
        text = read(os.path.join(skills, s, 'SKILL.md'))
        if 'TEMPLATE · FILL-IN' in text or 'PLANTILLA · FILL-IN' in text:
            continue   # voice stays a template: it's the user's voice
        filled += 1
        expect('<PROJECT>' not in text, f'{tag}: placeholder left in the {s} skill')
    expect(filled == 6, f'{tag}: the profile should fill in the 6 core skills, filled {filled}')
    check = read(os.path.join(h, 'personal', 'scripts', 'check.py'))
    expect('innerHTML' in check, f'{tag}: the profile\'s RULES should be in check.py')
    expect('selftest OK' in out, f'{tag}: the sensor selftest should pass with the profile\'s RULES')
    checklists = os.path.join(h, 'personal', 'checklists')
    expect(any('CSRF' in read(os.path.join(checklists, f)) for f in os.listdir(checklists)),
           f'{tag}: the profile\'s security checklist should be in place')
    expect('TUNE' in out, f'{tag}: setup should list what is left to tune')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    i18n = os.path.join(REPO, 'i18n')
    langs = sys.argv[1:] or ['en'] + (sorted(os.listdir(i18n)) if os.path.isdir(i18n) else [])
    native = harness_setup.SYSTEM
    systems = [native]
    if native == 'windows':
        if symlinks_available():
            systems += ['linux', 'macos']
        else:
            print('No symlinks for this user (Developer Mode off): Linux and macOS are only tested in CI.')
    base = tempfile.mkdtemp(prefix='harness-test-')
    try:
        for system in systems:
            for lang in langs:
                test(lang, system, base)
        for lang in langs:
            test_profile(lang, native, base)
    finally:
        # on Windows, links first, so rmtree never walks into what they point to
        if os.name == 'nt':
            for folder, dirs, _ in os.walk(base, topdown=True):
                for d in list(dirs):
                    p = os.path.join(folder, d)
                    if is_dir_link(p):
                        os.rmdir(p)
                        dirs.remove(d)
        shutil.rmtree(base, ignore_errors=True)
    print(f'\n{len(failures)} failures' if failures else f'\nsetup.py: all good ({", ".join(systems)}).')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
