"""Sets up the harness on this PC: names, language, links and each tool's settings. Windows, Linux and macOS.

The harness is the folder this script lives in: put it wherever you like and run it from there. On Windows,
on the same drive as the user profiles (the router and OpenCode's config are hardlinks); on Linux and macOS
everything is a symlink, so anywhere.

Usage (python3 instead of py -3 on Linux and macOS):
    py -3 setup.py --project "My Project" [--tools claude,copilot,opencode,dsh] [--lang en|es]
                   [--users rober,ana] [--vscode-permissions] [--force] [--dry-run]
    py -3 setup.py --check                    # checks every link and setting; repairs what is safe to repair
    py -3 setup.py --uninstall [--tools ...] [--users ...]   # removes links and settings; keeps the harness

The first run names the pieces and applies the language. Later runs only add tools or users: the project
and the language are chosen once (the files you fill in can't be translated for you). Standard library only.
"""
import argparse
import datetime
import getpass
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(ROOT, '.setup.json')
TOOLS = ('claude', 'copilot', 'opencode', 'dsh')
LANGS = ('en', 'es')
SYSTEMS = ('windows', 'linux', 'macos')
# how each system runs Python: the template is written with the Windows launcher
LAUNCHERS = {'windows': 'py -3', 'linux': 'python3', 'macos': 'python3'}
# folders and files with placeholders; the docs (README…) keep theirs, they explain them
TEMPLATE_PARTS = ('claude', 'copilot', 'opencode', 'dsh', 'personal', 'AGENTS.template.md')
TEXT_EXT = ('.md', '.py', '.ts', '.json', '.jsonc', '.ps1')
# in JSON and TypeScript a \ starts an escape: paths go with /
FORWARD_EXT = ('.json', '.jsonc', '.ts')
NAME_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
# ready-made content for a kind of project (profiles/<name>/): what it leaves to adjust is marked TUNE
PROFILES_DIR = os.path.join(ROOT, 'profiles')
PROFILES = sorted(os.listdir(PROFILES_DIR)) if os.path.isdir(PROFILES_DIR) else []
VSCODE_KEYS = ('github.copilot.chat.additionalReadAccessPaths', 'chat.tools.terminal.autoApprove')

SYSTEM = 'windows' if os.name == 'nt' else 'macos' if sys.platform == 'darwin' else 'linux'
dry_run = False
checking = False
problems = []


def windows():
    return SYSTEM == 'windows'


def dir_link_word():
    return 'junction' if windows() else 'symlink'


def file_link_word():
    return 'hardlink' if windows() else 'symlink'


# ---------------------------------------------------------------------------
# output
# ---------------------------------------------------------------------------

def say(kind, msg):
    print(f'  {kind:<7}{msg}')


def problem(msg):
    problems.append(msg)
    say('PROBLEM', msg)


def act(msg, fn, *args):
    """Runs a change, or only announces it with --dry-run."""
    if dry_run:
        say('would', msg)
        return
    fn(*args)
    say('fixed' if checking else 'done', msg)


def short(path):
    return path.replace(ROOT, '<harness>')


# ---------------------------------------------------------------------------
# files
# ---------------------------------------------------------------------------

def read_text(path):
    with io.open(path, encoding='utf-8-sig', newline='') as f:
        return f.read()


def write_text(path, text):
    # without BOM: a BOM in front of the frontmatter's --- silently breaks a skill
    with io.open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(text)


def backup(path):
    """One copy per file, from before setup.py first touched it: the one that matters to go back."""
    copy = path + '.before-harness'
    if not os.path.exists(copy):
        shutil.copy2(path, copy)
        say('backup', copy)


def backup_dated(path):
    """For a file in the way that --force replaces: someone else's content, kept as is."""
    copy = f'{path}.bak-{datetime.datetime.now():%Y%m%d-%H%M%S}'
    shutil.copy2(path, copy)
    say('backup', copy)


# ---------------------------------------------------------------------------
# links: on Windows, junctions for folders and hardlinks for files (neither needs admin);
# on Linux and macOS, symlinks for both
# ---------------------------------------------------------------------------

def norm(path):
    if path.startswith('\\\\?\\'):
        path = path[4:]
    return os.path.normcase(os.path.realpath(path))


def is_link(path):
    """A symlink or a junction (dangling ones too)."""
    if os.path.islink(path):
        return True
    try:
        return os.lstat(path).st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT
    except (OSError, AttributeError):
        return False


def dangling(path):
    return is_link(path) and not os.path.exists(path)


def link_target(path):
    target = os.readlink(path)
    if target.startswith('\\\\?\\'):
        target = target[4:]
    return target if os.path.isabs(target) else os.path.join(os.path.dirname(path), target)


def points_to(link, target):
    try:
        return norm(link_target(link)) == norm(target)
    except OSError:
        return False


def make_dir_link(link, target):
    os.makedirs(os.path.dirname(link), exist_ok=True)
    if windows():
        res = subprocess.run(['cmd', '/c', 'mklink', '/J', link, target], capture_output=True, text=True)
        if res.returncode:
            raise OSError(f'mklink /J failed: {(res.stdout + res.stderr).strip()}')
    else:
        os.symlink(target, link, target_is_directory=True)


def remove_dir_link_only(link):
    # removes only the link, never what it points to
    if os.name == 'nt':
        os.rmdir(link)   # a junction or a folder symlink
    else:
        os.unlink(link)


def make_file_link(link, target):
    os.makedirs(os.path.dirname(link), exist_ok=True)
    if windows():
        os.link(target, link)
    else:
        os.symlink(target, link)


def same_file(a, b):
    try:
        return os.path.samefile(a, b)   # a hardlink, or a symlink to it
    except OSError:
        return False


def same_content(a, b):
    with open(a, 'rb') as f, open(b, 'rb') as g:
        return f.read() == g.read()


def relink(link, target):
    os.remove(link)
    make_file_link(link, target)


def ensure_file_link(link, target, label, force):
    word = file_link_word()
    if not os.path.lexists(link):
        act(f'{label}: {word} {link}', make_file_link, link, target)
    elif same_file(link, target):
        say('ok', f'{label}: {link}')
    elif dangling(link):
        act(f'{label}: {word} {link} (it pointed to something that no longer exists)', relink, link, target)
    elif os.path.isdir(link):
        problem(f'{label}: {link} is a folder, not a file')
    elif same_content(link, target):
        # an editor saved it by replacing the file: same text, but no longer linked
        act(f'{label}: {word} restored {link} (it had been broken, same text)', relink, link, target)
    elif force:
        def replace():
            backup_dated(link)
            relink(link, target)
        act(f'{label}: {link} replaced by the {word} (--force)', replace)
    else:
        newer = 'that copy' if os.path.getmtime(link) > os.path.getmtime(target) else 'the harness original'
        problem(f'{label}: {link} has other content (newer: {newer}). If it is the link broken by an editor, '
                f'copy the text you want to keep into {short(target)} and run --check again; if it is another '
                f'project\'s, merge them (docs/SETUP.md §6) or use --force to back it up and replace it')


def ensure_dir_link(link, target, label, force, per_item=True):
    word = dir_link_word()
    if is_link(link):
        if dangling(link):
            act(f'{label}: {word} {link} (it pointed to something that no longer exists)',
                lambda: (remove_dir_link_only(link), make_dir_link(link, target)))
        elif points_to(link, target):
            say('ok', f'{label}: {link}')
        else:
            problem(f'{label}: {link} already points to {link_target(link)} (another project?). '
                    'See docs/SETUP.md §6 to share it')
    elif os.path.isdir(link):
        if not os.listdir(link):
            act(f'{label}: {word} {link}', lambda: (os.rmdir(link), make_dir_link(link, target)))
        elif not per_item:
            problem(f'{label}: {link} is a real folder, not a {word} (copied harness?). Check it is a copy of '
                    f'{short(target)}, delete that copy and run again')
        else:
            # a real folder with other things inside: one link per item, without touching the rest
            for item in sorted(os.listdir(target)):
                ensure_item_link(os.path.join(link, item), os.path.join(target, item), label, force)
    elif os.path.lexists(link):
        problem(f'{label}: {link} is a file, not a folder')
    else:
        act(f'{label}: {word} {link}', make_dir_link, link, target)


def ensure_item_link(link, target, label, force):
    if not os.path.isdir(target):
        ensure_file_link(link, target, label, force)
    elif is_link(link) and points_to(link, target):
        say('ok', f'{label}: {link}')
    elif dangling(link):
        act(f'{label}: {dir_link_word()} {link} (it pointed to something that no longer exists)',
            lambda: (remove_dir_link_only(link), make_dir_link(link, target)))
    elif os.path.lexists(link):
        problem(f'{label}: {link} already exists and is not this harness\'s (same name in another project?)')
    else:
        act(f'{label}: {dir_link_word()} {link}', make_dir_link, link, target)


def remove_file_link(link, target, label):
    if os.path.lexists(link) and same_file(link, target):
        act(f'{label}: removed {link}', os.remove, link)
    elif os.path.lexists(link):
        say('skip', f'{label}: {link} is not linked to this harness, left as is')


def remove_dir_link(link, target, label):
    if is_link(link):
        if points_to(link, target):
            act(f'{label}: removed {dir_link_word()} {link}', remove_dir_link_only, link)
        else:
            say('skip', f'{label}: {link} points elsewhere, left as is')
    elif os.path.isdir(link):
        for item in sorted(os.listdir(target)):
            sub, tgt = os.path.join(link, item), os.path.join(target, item)
            if os.path.isdir(tgt) and is_link(sub) and points_to(sub, tgt):
                act(f'{label}: removed {dir_link_word()} {sub}', remove_dir_link_only, sub)
            elif os.path.isfile(tgt):
                remove_file_link(sub, tgt, label)


# ---------------------------------------------------------------------------
# what each tool needs, per user (link, target, kind)
# ---------------------------------------------------------------------------

def router(state):
    return os.path.join(ROOT, 'copilot', state['slug'] + '.instructions.md')


def tool_links(tool, home, state):
    if tool == 'copilot':
        base = os.path.join(home, '.copilot')
        return [
            (os.path.join(base, 'skills'), os.path.join(ROOT, 'personal', 'skills'), 'dir'),
            (os.path.join(base, 'agents'), os.path.join(ROOT, 'copilot', 'agents'), 'dir'),
            # read by VS Code chat and Copilot CLI; not also in the profile's prompts (it would load twice)
            (os.path.join(base, 'copilot-instructions.md'), router(state), 'file'),
        ]
    if tool == 'opencode':
        base = os.path.join(home, '.config', 'opencode')
        return [
            (os.path.join(base, 'opencode.jsonc'), os.path.join(ROOT, 'opencode', 'opencode.jsonc'), 'file'),
            (os.path.join(base, 'AGENTS.md'), router(state), 'file'),   # the same router as Copilot
            (os.path.join(base, 'skills'), os.path.join(ROOT, 'personal', 'skills'), 'dir'),
            (os.path.join(base, 'agents'), os.path.join(ROOT, 'opencode', 'agents'), 'dir'),
            (os.path.join(base, 'plugins'), os.path.join(ROOT, 'opencode', 'plugins'), 'dir'),
        ]
    if tool == 'dsh':
        # DeepSeek Harness: no agent files (the router says to use a subagent with the reviewer's instructions)
        # and no hook (the router says to run the sensor). The router's authority goes in the preset, by hand
        base = os.path.join(home, '.dsh')
        return [
            (os.path.join(base, 'AGENTS.md'), router(state), 'file'),   # the same router as Copilot
            (os.path.join(base, 'skills'), os.path.join(ROOT, 'personal', 'skills'), 'dir'),
        ]
    return []


def plugin_link(state):
    return os.path.join(ROOT, 'claude', 'plugins', state['slug']), os.path.join(ROOT, 'personal')


# ---------------------------------------------------------------------------
# Claude: ~/.claude/settings.json
# ---------------------------------------------------------------------------

def claude_entries(state):
    marketplace = 'harness-' + state['slug']
    return (marketplace,
            {'source': {'source': 'directory', 'path': os.path.join(ROOT, 'claude')}},
            f'{state["slug"]}@{marketplace}',
            # a shell runs the hook (Git Bash on Windows): forward slashes
            'cat "' + ROOT.replace('\\', '/') + '/claude/CLAUDE.md"')


def load_settings(path, label):
    if not os.path.isfile(path):
        return {}
    try:
        return json.loads(read_text(path))
    except ValueError as e:
        problem(f'{label}: {path} is not valid JSON ({e}); fix it and run again')
        return None


def save_settings(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.isfile(path):
        backup(path)
    write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def has_hook(data, command):
    return any(h.get('command') == command
               for group in data.get('hooks', {}).get('SessionStart', [])
               for h in group.get('hooks', []))


def ensure_claude(home, state):
    label = 'claude'
    path = os.path.join(home, '.claude', 'settings.json')
    data = load_settings(path, label)
    if data is None:
        return
    marketplace, source, plugin, command = claude_entries(state)
    missing = []
    if data.get('extraKnownMarketplaces', {}).get(marketplace) != source:
        missing.append('marketplace')
    enabled = data.get('enabledPlugins', {}).get(plugin)
    if enabled is False:
        say('skip', f'{label}: the plugin {plugin} is disabled in {path}; left as you set it')
    elif enabled is not True:
        missing.append('plugin')
    if not has_hook(data, command):
        missing.append('SessionStart hook')
    if not missing:
        say('ok', f'{label}: {path}')
        return

    def apply():
        data.setdefault('extraKnownMarketplaces', {})[marketplace] = source
        if enabled is not False:
            data.setdefault('enabledPlugins', {})[plugin] = True
        if not has_hook(data, command):
            data.setdefault('hooks', {}).setdefault('SessionStart', []).append(
                {'hooks': [{'type': 'command', 'command': command}]})
        save_settings(path, data)
    act(f'{label}: {", ".join(missing)} in {path}', apply)


def remove_claude(home, state):
    label = 'claude'
    path = os.path.join(home, '.claude', 'settings.json')
    data = load_settings(path, label)
    if not data:
        return
    marketplace, _, plugin, command = claude_entries(state)
    found = (marketplace in data.get('extraKnownMarketplaces', {}) or plugin in data.get('enabledPlugins', {})
             or has_hook(data, command))
    if not found:
        return

    def apply():
        data.get('extraKnownMarketplaces', {}).pop(marketplace, None)
        data.get('enabledPlugins', {}).pop(plugin, None)
        hooks = data.get('hooks', {})
        if 'SessionStart' in hooks:
            for group in hooks['SessionStart']:
                group['hooks'] = [h for h in group.get('hooks', []) if h.get('command') != command]
            hooks['SessionStart'] = [g for g in hooks['SessionStart'] if g.get('hooks')]
        save_settings(path, data)
    act(f'{label}: marketplace, plugin and hook removed from {path}', apply)


# ---------------------------------------------------------------------------
# VS Code (optional): read the harness and run the sensor without permission prompts
# ---------------------------------------------------------------------------

def vscode_path(home, system=None):
    system = system or SYSTEM
    if system == 'windows':
        user = os.path.join(home, 'AppData', 'Roaming', 'Code', 'User')
    elif system == 'macos':
        user = os.path.join(home, 'Library', 'Application Support', 'Code', 'User')
    else:
        user = os.path.join(home, '.config', 'Code', 'User')
    return os.path.join(user, 'settings.json')


def js_regex_escape(text):
    # only the regex metacharacters: VS Code may compile it with the u flag, where \- or \  are errors
    return re.sub(r'([\\.^$|?*+()\[\]{}/])', r'\\\1', text)


def vscode_block(state, nl='\n'):
    check = os.path.join(ROOT, 'personal', 'scripts', 'check.py')
    rule = '/^' + js_regex_escape(LAUNCHERS[SYSTEM] + ' ' + check) + r'(\s|$)/'
    tag = f'// {state["slug"]} harness (setup.py):'
    return nl.join([f'  {tag} read the harness without asking; edits stay limited to the workspace',
                    f'  "{VSCODE_KEYS[0]}": [{json.dumps(ROOT)}],',
                    f'  {tag} its sensor (only that script) without asking',
                    f'  "{VSCODE_KEYS[1]}": {{ {json.dumps(rule)}: true }}'])


def last_token(text):
    """Last significant character of a JSONC text (outside strings and comments)."""
    last, i, n = '', 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            i += 1
            while i < n and text[i] != '"':
                i += 2 if text[i] == '\\' else 1
            last = '"'
        elif text.startswith('//', i):
            i = text.find('\n', i)
            i = n if i < 0 else i
            continue
        elif text.startswith('/*', i):
            i = text.find('*/', i + 2)
            i = n if i < 0 else i + 1
        elif not c.isspace():
            last = c
        i += 1
    return last


def ensure_vscode(home, state):
    label = 'vscode'
    path = vscode_path(home)
    if not os.path.isfile(path):
        say('skip', f'{label}: {path} doesn\'t exist (open VS Code once with that user and run again)')
        return
    text = read_text(path)
    nl = '\r\n' if '\r\n' in text else '\n'   # the file's own line endings
    block = vscode_block(state, nl)
    if block in text:
        say('ok', f'{label}: {path}')
        return
    taken = [k for k in VSCODE_KEYS if f'"{k}"' in text]
    if taken:
        problem(f'{label}: {path} already has {", ".join(taken)}; add this harness by hand '
                f'(docs/SETUP.md §A.4):\n{block}')
        return
    closing = len(text.rstrip()) - 1
    if closing < 0 or text[closing] != '}':
        problem(f'{label}: {path} doesn\'t end with }}: add the settings by hand (docs/SETUP.md §A.4)')
        return
    # inserted right after the last setting, so removing it gives back the file byte for byte
    body = text[:closing].rstrip()
    # the comma on its own line: the last line may end in a // comment
    sep = '' if last_token(body) in ('{', ',', '') else nl + '  ,'
    inserted = sep + nl + block

    def apply():
        backup(path)
        write_text(path, body + inserted + text[len(body):])
        state.setdefault('vscode', {})[home] = inserted
    act(f'{label}: harness read access and sensor without prompts in {path} (reload the window)', apply)


def remove_vscode(home, state):
    inserted = state.get('vscode', {}).get(home)
    path = vscode_path(home)
    if not inserted or not os.path.isfile(path):
        return
    text = read_text(path)
    if inserted not in text:
        say('skip', f'vscode: the harness block in {path} was changed by hand; remove it yourself')
        return

    def apply():
        backup(path)
        write_text(path, text.replace(inserted, '', 1))
        state['vscode'].pop(home)
    act(f'vscode: harness block removed from {path}', apply)


# ---------------------------------------------------------------------------
# first run: language and names
# ---------------------------------------------------------------------------

def apply_language(lang):
    base = os.path.join(ROOT, 'i18n')
    if lang != 'en':
        src = os.path.join(base, lang)
        for folder, _, files in os.walk(src):
            for f in files:
                if folder == src and f == 'names.json':
                    continue
                rel = os.path.relpath(os.path.join(folder, f), src)
                shutil.copyfile(os.path.join(src, rel), os.path.join(ROOT, rel))
        with io.open(os.path.join(src, 'names.json'), encoding='utf-8') as f:
            renames = json.load(f)['rename']
        # deepest first: a file inside a folder is renamed before its folder
        for old in sorted(renames, key=lambda p: -p.count('/')):
            os.rename(os.path.join(ROOT, *old.split('/')), os.path.join(ROOT, *renames[old].split('/')))
    # the project's harness only keeps its language
    shutil.rmtree(base)


def apply_profile(name):
    """Copies profiles/<name>/personal over personal/ and its RULES into check.py; then drops profiles/."""
    if name:
        src = os.path.join(PROFILES_DIR, name)
        for folder, _, files in os.walk(os.path.join(src, 'personal')):
            for f in files:
                rel = os.path.relpath(os.path.join(folder, f), src)
                os.makedirs(os.path.dirname(os.path.join(ROOT, rel)), exist_ok=True)
                shutil.copyfile(os.path.join(folder, f), os.path.join(ROOT, rel))
        rules_path = os.path.join(src, 'rules.py')
        if os.path.isfile(rules_path):
            check_path = os.path.join(ROOT, 'personal', 'scripts', 'check.py')
            block = re.compile(r'(?ms)^RULES = \[\n.*?^\]\n')
            check_text = read_text(check_path)
            current = block.search(check_text)
            new = block.search(read_text(rules_path))
            if not current or not new:
                raise SystemExit(f'profile {name!r}: no "RULES = [ ... ]" block to swap in check.py')
            write_text(check_path, check_text[:current.start()] + new.group(0) + check_text[current.end():])
    # the project's harness only keeps its profile
    if os.path.isdir(PROFILES_DIR):
        shutil.rmtree(PROFILES_DIR)


def template_files():
    for part in TEMPLATE_PARTS:
        path = os.path.join(ROOT, part)
        if os.path.isfile(path):
            yield path
        for folder, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not is_link(os.path.join(folder, d))]
            for f in files:
                if f.endswith(TEXT_EXT):
                    yield os.path.join(folder, f)


def for_posix(text, path):
    """The template is written for Windows: python3 for py -3, and / in the paths under the harness."""
    text = text.replace('spawn("py", ["-3", ', 'spawn("python3", [').replace('py -3 ', 'python3 ')
    text = re.sub(r'<HARNESS>((?:\\[^\\\s`"\'|)\]]+)+)', lambda m: '<HARNESS>' + m.group(1).replace('\\', '/'), text)
    if path.endswith('.md'):
        # and the ones the text mentions (personal\checklists\, claude\CLAUDE.md…), not escapes like \|
        text = re.sub(r'\b(?:personal|claude|copilot|opencode|checklists)(?:\\[\w.\-]+)+\\?',
                      lambda m: m.group(0).replace('\\', '/'), text)
    return text


def apply_names(state):
    slug, project = state['slug'], state['project']
    forward = ROOT.replace('\\', '/')
    for path in template_files():
        text = read_text(path)
        new = text if windows() else for_posix(text, path)
        new = new.replace('sensor-<PROJECT>', 'sensor-' + slug)   # an id: no spaces
        new = new.replace('<HARNESS>', forward if path.endswith(FORWARD_EXT) else ROOT).replace('<PROJECT>', project)
        if path == os.path.join(ROOT, 'claude', 'CLAUDE.md'):
            new = new.replace('`project:', f'`{slug}:')   # the skill prefix in Claude is the plugin name
        if new != text:
            write_text(path, new)

    mp_path = os.path.join(ROOT, 'claude', '.claude-plugin', 'marketplace.json')
    mp = json.loads(read_text(mp_path))
    mp['name'] = 'harness-' + slug
    if mp.get('owner', {}).get('name') == 'YOUR_NAME':
        mp['owner']['name'] = getpass.getuser()
    for p in mp['plugins']:
        p['name'], p['source'] = slug, './plugins/' + slug
    write_text(mp_path, json.dumps(mp, indent=2, ensure_ascii=False) + '\n')

    if slug != 'project':
        os.rename(os.path.join(ROOT, 'copilot', 'project.instructions.md'), router(state))


def run_sync():
    res = subprocess.run([sys.executable, os.path.join(ROOT, 'opencode', 'sync.py')], capture_output=True, text=True)
    if res.returncode:
        problem('sync.py: ' + (res.stdout + res.stderr).strip())
    else:
        say('done', 'agent copies for Copilot and OpenCode: ' + res.stdout.strip())


def sync_is_current():
    res = subprocess.run([sys.executable, os.path.join(ROOT, 'opencode', 'sync.py'), '--check'],
                         capture_output=True, text=True)
    return res.returncode == 0


def pending():
    out = []
    generated = (os.path.join(ROOT, 'copilot', 'agents'), os.path.join(ROOT, 'opencode', 'agents'))
    for path in template_files():
        if path.startswith(generated):   # sync.py copies: they're filled in through personal/agents
            continue
        text = read_text(path)
        marks = ', '.join(f'{n} {mark}' for mark, n in (('FILL-IN', text.count('FILL-IN')), ('TUNE', text.count('TUNE')))
                          if n)
        if marks:
            out.append((os.path.relpath(path, ROOT), marks))
    return out


# ---------------------------------------------------------------------------
# state (.setup.json, next to this script)
# ---------------------------------------------------------------------------

def load_state():
    if not os.path.isfile(STATE):
        return None
    with io.open(STATE, encoding='utf-8') as f:
        return json.load(f)


def save_state(state):
    if dry_run:
        return
    try:
        write_text(STATE, json.dumps(state, indent=2, ensure_ascii=False) + '\n')
    except OSError as e:
        problem(f'can\'t save {STATE} ({e}): --check and --uninstall won\'t know about this run. '
                'Give this user write access to the harness folder')


def slugify(project):
    return re.sub(r'[^a-z0-9]+', '-', project.lower()).strip('-')


def homes_for(args):
    if args.home:
        return [os.path.abspath(h) for h in args.home]
    profile = os.path.expanduser('~')
    if not args.users:
        return [profile]
    users = [u.strip() for u in args.users.split(',') if u.strip()]
    if not windows():
        me = getpass.getuser()
        others = [u for u in users if u != me]
        if others:
            # files created for another user from here would belong to whoever runs this (root, with sudo)
            raise SystemExit(f'On {SYSTEM}, run setup.py as each user instead, e.g.: sudo -u {others[0]} python3 '
                             f'{os.path.join(ROOT, "setup.py")} (that user needs write access to the harness '
                             'folder, for .setup.json)')
        return [profile]
    out = []
    for user in users:
        home = os.path.join(os.path.dirname(profile), user)
        if not os.path.isdir(home):
            raise SystemExit(f'User {user!r} has no profile at {home}')
        out.append(home)
    return out


def tools_for(args, default):
    if not args.tools:
        return list(default)
    tools = [t.strip().lower() for t in args.tools.split(',') if t.strip()]
    wrong = [t for t in tools if t not in TOOLS]
    if wrong:
        raise SystemExit(f'Unknown tools: {", ".join(wrong)} (valid: {", ".join(TOOLS)})')
    return tools


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def link_tools(state, homes, tools, force, vscode):
    if 'claude' in tools:
        print('\nClaude plugin')
        link, target = plugin_link(state)
        ensure_dir_link(link, target, 'plugin', force, per_item=False)
    for home in homes:
        print(f'\n{home}')
        for tool in tools:
            if tool == 'claude':
                ensure_claude(home, state)
            for link, target, kind in tool_links(tool, home, state):
                (ensure_file_link if kind == 'file' else ensure_dir_link)(link, target, tool, force)
            if tool == 'dsh':
                # its preset shadows any global persona and a patch replaces a config whole: not automated
                say('todo', 'dsh: the router\'s authority in the system prompt, by hand (docs/SETUP.md §A.6)')
        if vscode or home in state.get('vscode', {}):
            ensure_vscode(home, state)
        if not dry_run:
            known = state.setdefault('links', {}).setdefault(home, [])
            known.extend(t for t in tools if t not in known)


def install(args):
    state = load_state()
    if state is None:
        if not args.project:
            raise SystemExit('First run: say the project name with --project "Name".')
        if os.path.isdir(os.path.join(ROOT, '.github')):
            raise SystemExit('This looks like the template repo itself (it has .github). Copy it first '
                             '(docs/SETUP.md §1) and run setup.py from the copy.')
        if '<PROJECT>' not in read_text(os.path.join(ROOT, 'claude', 'CLAUDE.md')):
            raise SystemExit('This copy was already named by hand. setup.py names a fresh copy (docs/SETUP.md §1); '
                             'to wire up a harness set up by hand, follow the appendix instead.')
        slug = slugify(args.project)
        if not NAME_RE.match(slug):
            raise SystemExit(f'Can\'t make a name from {args.project!r}: use letters and digits.')
        state = {'project': args.project, 'slug': slug, 'lang': args.lang or 'en', 'system': SYSTEM,
                 'profile': args.profile, 'version': read_text(os.path.join(ROOT, 'VERSION')).strip()}
        if state['lang'] != 'en' and not os.path.isdir(os.path.join(ROOT, 'i18n', state['lang'])):
            raise SystemExit(f'No {state["lang"]!r} version in i18n.')
        first = True
    else:
        if args.project and slugify(args.project) != state['slug']:
            raise SystemExit(f'This harness is already {state["project"]!r}: the project is chosen once.')
        if args.lang and args.lang != state['lang']:
            raise SystemExit(f'This harness is already in {state["lang"]!r}: the language is chosen once, before '
                             'filling it in. For another one, start from a fresh copy.')
        if args.profile and args.profile != state.get('profile'):
            raise SystemExit('The profile is chosen once, on the first run. For another one, start from a fresh copy.')
        first = False

    homes = homes_for(args)
    tools = tools_for(args, TOOLS)
    if windows() and any(t in tools for t in ('copilot', 'opencode', 'dsh')):
        drive = os.path.splitdrive(ROOT)[0].lower()
        other = [h for h in homes if os.path.splitdrive(h)[0].lower() != drive]
        if other:
            raise SystemExit(f'The harness ({drive.upper()}) and these profiles are on different drives: '
                             f'{", ".join(other)}. Hardlinks only work within one drive; move the harness.')
    if os.path.isdir(os.path.join(ROOT, '.git')):
        say('WARN', 'the harness still has .git: if it is the template\'s, remove it (docs/SETUP.md §1)')

    print(f'Harness {state["project"]!r} ({state["slug"]}, {state["lang"]}, {SYSTEM}) at {ROOT}')
    if first:
        print('\nNames and language')
        act(f'language: {state["lang"]}', apply_language, state['lang'])
        act(f'profile: {state["profile"] or "none (the clean template)"}', apply_profile, state['profile'])
        act(f'names: <PROJECT> = {state["project"]}, <HARNESS> = this folder, prefix {state["slug"]}:'
            + ('' if windows() else ', python3 and / paths'), apply_names, state)
        if not dry_run:
            run_sync()
    save_state(state)
    link_tools(state, homes, tools, args.force, args.vscode_permissions)
    save_state(state)

    if not dry_run:
        print('\nSensor')
        res = subprocess.run([sys.executable, os.path.join(ROOT, 'personal', 'scripts', 'check.py'), '--selftest'],
                             capture_output=True, text=True, encoding='utf-8')
        if res.returncode:
            problem('check.py --selftest: ' + (res.stdout + res.stderr).strip())
        else:
            say('ok', res.stdout.strip())
    todo = pending() if not dry_run else []
    if todo:
        print('\nStill to fill in (FILL-IN) or to tune to your stack (TUNE):')
        for rel, marks in todo:
            print(f'  {rel} ({marks})')
    print('\nNext: fill in the FILL-IN parts and tune the TUNE ones (docs/SETUP.md §3), reload VS Code and check each '
          'tool (docs/SETUP.md §4).')
    return finish()


def check(args):
    global checking
    checking = True
    state = load_state()
    if state is None:
        raise SystemExit('No .setup.json: this harness wasn\'t set up with setup.py.')
    print(f'Checking harness {state["project"]!r} at {ROOT}')
    print('\nAgent copies')
    if sync_is_current():
        say('ok', 'the Copilot and OpenCode copies match personal/agents')
    elif not dry_run:
        run_sync()
    by_tools = {}
    for home, tools in state.get('links', {}).items():
        by_tools.setdefault(tuple(tools), []).append(home)
    for tools, homes in by_tools.items():
        link_tools(state, homes, list(tools), False, False)
    save_state(state)
    return finish()


def uninstall(args):
    state = load_state()
    if state is None:
        raise SystemExit('No .setup.json: nothing to uninstall.')
    links = state.get('links', {})
    homes = homes_for(args) if (args.users or args.home) else list(links)
    tools = tools_for(args, TOOLS)
    print(f'Uninstalling {", ".join(tools)} for {", ".join(homes)} (the harness itself stays)')
    for home in homes:
        print(f'\n{home}')
        for tool in tools:
            if tool not in links.get(home, []):
                continue
            if tool == 'claude':
                remove_claude(home, state)
            for link, target, kind in tool_links(tool, home, state):
                (remove_file_link if kind == 'file' else remove_dir_link)(link, target, tool)
            if not dry_run:
                links[home].remove(tool)
        if 'copilot' in tools:
            remove_vscode(home, state)
        if not dry_run and not links.get(home):
            links.pop(home, None)
    if 'claude' in tools and not any('claude' in t for t in links.values()):
        link, target = plugin_link(state)
        print('\nClaude plugin')
        remove_dir_link(link, target, 'plugin')
    save_state(state)
    return finish()


def finish():
    if problems:
        print(f'\n{len(problems)} problem(s): see PROBLEM above. Nothing else was touched for those.')
        return 1
    print('\nAll good.' if not dry_run else '\nDry run: nothing was changed.')
    return 0


def main():
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='Sets up the harness on this PC (Windows, Linux or macOS).')
    parser.add_argument('--project', help='project name (first run): <PROJECT>, and its lowercase form the prefix')
    parser.add_argument('--tools', help=f'comma-separated, default all: {",".join(TOOLS)}')
    parser.add_argument('--lang', choices=LANGS, help='language of the pieces the model reads (first run; default en)')
    parser.add_argument('--profile', choices=PROFILES or None,
                        help='ready-made content for a kind of project (first run; default: the clean template)')
    parser.add_argument('--users', help='Windows: comma-separated users to wire up (default: you); '
                                        'on Linux and macOS, run it as each user')
    parser.add_argument('--vscode-permissions', action='store_true',
                        help='VS Code: read the harness and run the sensor without asking (Copilot)')
    parser.add_argument('--force', action='store_true', help='replace a file in the way, after backing it up')
    parser.add_argument('--dry-run', action='store_true', help='only say what would be done')
    parser.add_argument('--check', action='store_true', help='check links and settings; repair the safe ones')
    parser.add_argument('--uninstall', action='store_true', help='remove links and settings; keep the harness')
    # for tests: a fake profile folder, and another system's way of linking (symlinks need Developer Mode on Windows)
    parser.add_argument('--home', action='append', help=argparse.SUPPRESS)
    parser.add_argument('--platform', choices=SYSTEMS, help=argparse.SUPPRESS)
    args = parser.parse_args()

    global dry_run, SYSTEM
    dry_run = args.dry_run
    if args.platform:
        if args.platform == 'windows' and os.name != 'nt':
            raise SystemExit('--platform windows only works on Windows (junctions and mklink).')
        SYSTEM = args.platform
    if args.check:
        return check(args)
    if args.uninstall:
        return uninstall(args)
    return install(args)


if __name__ == '__main__':
    sys.exit(main())
