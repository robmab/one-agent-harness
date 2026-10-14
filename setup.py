"""Sets up the harness on this PC: names, language, links and each tool's settings. Windows only for now.

The harness is the folder this script lives in: put it wherever you like (on the same drive as the user
profiles, because of the hardlinks) and run it from there.

Usage:
    py -3 setup.py --project "My Project" [--tools claude,copilot,opencode] [--lang en|es]
                   [--users rober,ana] [--vscode-permissions] [--force] [--dry-run]
    py -3 setup.py --check                    # checks every link and setting; repairs what is safe to repair
    py -3 setup.py --uninstall [--tools ...] [--users ...]   # removes links and settings; keeps the harness

The first run names the pieces and applies the language. Later runs only add tools or users: the project
and the language are chosen once (the files you fill in can't be translated for you). Standard library only.
"""
import argparse
import datetime
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
TOOLS = ('claude', 'copilot', 'opencode')
LANGS = ('en', 'es')
# folders and files with placeholders; the docs (README…) keep theirs, they explain them
TEMPLATE_PARTS = ('claude', 'copilot', 'opencode', 'personal', 'AGENTS.template.md')
TEXT_EXT = ('.md', '.py', '.ts', '.json', '.jsonc', '.ps1')
# in JSON and TypeScript a \ starts an escape: paths go with /
FORWARD_EXT = ('.json', '.jsonc', '.ts')
NAME_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
VSCODE_KEYS = ('github.copilot.chat.additionalReadAccessPaths', 'chat.tools.terminal.autoApprove')

dry_run = False
checking = False
problems = []


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
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    copy = f'{path}.bak-{stamp}'
    shutil.copy2(path, copy)
    return copy


# ---------------------------------------------------------------------------
# links (Windows: junctions for folders, hardlinks for files; neither needs admin)
# ---------------------------------------------------------------------------

def norm(path):
    if path.startswith('\\\\?\\'):
        path = path[4:]
    return os.path.normcase(os.path.abspath(path))


def is_junction(path):
    try:
        return os.lstat(path).st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT
    except (OSError, AttributeError):
        return False


def junction_target(path):
    return norm(os.readlink(path))


def make_junction(link, target):
    os.makedirs(os.path.dirname(link), exist_ok=True)
    res = subprocess.run(['cmd', '/c', 'mklink', '/J', link, target], capture_output=True, text=True)
    if res.returncode:
        raise OSError(f'mklink /J failed: {(res.stdout + res.stderr).strip()}')


def remove_junction(link):
    os.rmdir(link)   # removes only the junction, never what it points to


def make_hardlink(link, target):
    os.makedirs(os.path.dirname(link), exist_ok=True)
    os.link(target, link)


def same_file(a, b):
    try:
        return os.path.samefile(a, b)
    except OSError:
        return False


def same_content(a, b):
    with open(a, 'rb') as f, open(b, 'rb') as g:
        return f.read() == g.read()


def relink(link, target):
    os.remove(link)
    make_hardlink(link, target)


def ensure_file_link(link, target, label, force):
    if not os.path.lexists(link):
        act(f'{label}: hardlink {link}', make_hardlink, link, target)
    elif same_file(link, target):
        say('ok', f'{label}: {link}')
    elif os.path.isdir(link):
        problem(f'{label}: {link} is a folder, not a file')
    elif same_content(link, target):
        # an editor saved it by replacing the file: same text, but no longer linked
        act(f'{label}: hardlink restored {link} (it had been broken, same text)', relink, link, target)
    elif force:
        def replace():
            say('backup', backup(link))
            relink(link, target)
        act(f'{label}: {link} replaced by the hardlink (--force)', replace)
    else:
        newer = 'that copy' if os.path.getmtime(link) > os.path.getmtime(target) else 'the harness original'
        problem(f'{label}: {link} has other content (newer: {newer}). If it is the link broken by an editor, '
                f'copy the text you want to keep into {short(target)} and run --check again; if it is another '
                f'project\'s, merge them (README §5) or use --force to back it up and replace it')


def ensure_dir_link(link, target, label, force, per_item=True):
    if is_junction(link):
        if junction_target(link) == norm(target):
            say('ok', f'{label}: {link}')
        else:
            problem(f'{label}: {link} already points to {junction_target(link)} (another project?). '
                    'See README §5 to share it')
    elif os.path.isdir(link):
        if not os.listdir(link):
            act(f'{label}: junction {link}', lambda: (os.rmdir(link), make_junction(link, target)))
        elif not per_item:
            problem(f'{label}: {link} is a real folder, not a junction (copied harness?). Check it is a copy of '
                    f'{short(target)}, delete it with rmdir /s and run again')
        else:
            # a real folder with other things inside: one link per item, without touching the rest
            for item in sorted(os.listdir(target)):
                ensure_item_link(os.path.join(link, item), os.path.join(target, item), label, force)
    elif os.path.lexists(link):
        problem(f'{label}: {link} is a file, not a folder')
    else:
        act(f'{label}: junction {link}', make_junction, link, target)


def ensure_item_link(link, target, label, force):
    if os.path.isdir(target):
        if is_junction(link) and junction_target(link) == norm(target):
            say('ok', f'{label}: {link}')
        elif os.path.lexists(link):
            problem(f'{label}: {link} already exists and is not this harness\'s (same name in another project?)')
        else:
            act(f'{label}: junction {link}', make_junction, link, target)
    else:
        ensure_file_link(link, target, label, force)


def remove_file_link(link, target, label):
    if os.path.lexists(link) and same_file(link, target):
        act(f'{label}: removed {link}', os.remove, link)
    elif os.path.lexists(link):
        say('skip', f'{label}: {link} is not linked to this harness, left as is')


def remove_dir_link(link, target, label):
    if is_junction(link):
        if junction_target(link) == norm(target):
            act(f'{label}: removed junction {link}', remove_junction, link)
        else:
            say('skip', f'{label}: {link} points elsewhere, left as is')
    elif os.path.isdir(link):
        for item in sorted(os.listdir(target)):
            sub, tgt = os.path.join(link, item), os.path.join(target, item)
            if is_junction(sub) and junction_target(sub) == norm(tgt):
                act(f'{label}: removed junction {sub}', remove_junction, sub)
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
            # read by VS Code chat and Copilot CLI; not also in the profile's prompts\ (it would load twice)
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
    return []


def plugin_junction(state):
    return os.path.join(ROOT, 'claude', 'plugins', state['slug']), os.path.join(ROOT, 'personal')


# ---------------------------------------------------------------------------
# Claude: ~/.claude/settings.json
# ---------------------------------------------------------------------------

def claude_entries(state):
    marketplace = 'harness-' + state['slug']
    return (marketplace,
            {'source': {'source': 'directory', 'path': os.path.join(ROOT, 'claude')}},
            f'{state["slug"]}@{marketplace}',
            # Git Bash runs the hook: forward slashes
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
        say('backup', backup(path))
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

def vscode_path(home):
    return os.path.join(home, 'AppData', 'Roaming', 'Code', 'User', 'settings.json')


def js_regex_escape(text):
    # only the regex metacharacters: VS Code may compile it with the u flag, where \- or \  are errors
    return re.sub(r'([\\.^$|?*+()\[\]{}/])', r'\\\1', text)


def vscode_block(state, nl='\n'):
    check = os.path.join(ROOT, 'personal', 'scripts', 'check.py')
    rule = '/^' + js_regex_escape('py -3 ' + check) + r'(\s|$)/'
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
                f'(README §A.4):\n{block}')
        return
    closing = len(text.rstrip()) - 1
    if closing < 0 or text[closing] != '}':
        problem(f'{label}: {path} doesn\'t end with }}: add the settings by hand (README §A.4)')
        return
    # inserted right after the last setting, so removing it gives back the file byte for byte
    body = text[:closing].rstrip()
    # the comma on its own line: the last line may end in a // comment
    sep = '' if last_token(body) in ('{', ',', '') else nl + '  ,'
    inserted = sep + nl + block

    def apply():
        say('backup', backup(path))
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
        say('backup', backup(path))
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


def template_files():
    for part in TEMPLATE_PARTS:
        path = os.path.join(ROOT, part)
        if os.path.isfile(path):
            yield path
        for folder, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not is_junction(os.path.join(folder, d))]
            for f in files:
                if f.endswith(TEXT_EXT):
                    yield os.path.join(folder, f)


def apply_names(state):
    slug, project = state['slug'], state['project']
    forward = ROOT.replace('\\', '/')
    for path in template_files():
        text = read_text(path)
        new = text.replace('sensor-<PROJECT>', 'sensor-' + slug)   # an id: no spaces
        new = new.replace('<HARNESS>', forward if path.endswith(FORWARD_EXT) else ROOT).replace('<PROJECT>', project)
        if path == os.path.join(ROOT, 'claude', 'CLAUDE.md'):
            new = new.replace('`project:', f'`{slug}:')   # the skill prefix in Claude is the plugin name
        if new != text:
            write_text(path, new)

    mp_path = os.path.join(ROOT, 'claude', '.claude-plugin', 'marketplace.json')
    mp = json.loads(read_text(mp_path))
    mp['name'] = 'harness-' + slug
    if mp.get('owner', {}).get('name') == 'YOUR_NAME':
        mp['owner']['name'] = os.environ.get('USERNAME', 'me')
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
    for path in template_files():
        n = read_text(path).count('FILL-IN')
        if n:
            out.append((os.path.relpath(path, ROOT), n))
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
    if not dry_run:
        write_text(STATE, json.dumps(state, indent=2, ensure_ascii=False) + '\n')


def slugify(project):
    return re.sub(r'[^a-z0-9]+', '-', project.lower()).strip('-')


def homes_for(args):
    if args.home:
        return [os.path.abspath(h) for h in args.home]
    profile = os.path.expanduser('~')
    if not args.users:
        return [profile]
    out = []
    for user in args.users.split(','):
        home = os.path.join(os.path.dirname(profile), user.strip())
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
        link, target = plugin_junction(state)
        ensure_dir_link(link, target, 'plugin', force, per_item=False)
    for home in homes:
        print(f'\n{home}')
        for tool in tools:
            if tool == 'claude':
                ensure_claude(home, state)
            for link, target, kind in tool_links(tool, home, state):
                (ensure_file_link if kind == 'file' else ensure_dir_link)(link, target, tool, force)
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
                             '(README §3.1) and run setup.py from the copy.')
        if '<PROJECT>' not in read_text(os.path.join(ROOT, 'claude', 'CLAUDE.md')):
            raise SystemExit('This copy was already named by hand. setup.py names a fresh copy (README §3.1); '
                             'to wire up a harness set up by hand, follow the appendix instead.')
        slug = slugify(args.project)
        if not NAME_RE.match(slug):
            raise SystemExit(f'Can\'t make a name from {args.project!r}: use letters and digits.')
        state = {'project': args.project, 'slug': slug, 'lang': args.lang or 'en',
                 'version': read_text(os.path.join(ROOT, 'VERSION')).strip()}
        if state['lang'] != 'en' and not os.path.isdir(os.path.join(ROOT, 'i18n', state['lang'])):
            raise SystemExit(f'No {state["lang"]!r} version in i18n\\.')
        first = True
    else:
        if args.project and slugify(args.project) != state['slug']:
            raise SystemExit(f'This harness is already {state["project"]!r}: the project is chosen once.')
        if args.lang and args.lang != state['lang']:
            raise SystemExit(f'This harness is already in {state["lang"]!r}: the language is chosen once, before '
                             'filling it in. For another one, start from a fresh copy.')
        first = False

    homes = homes_for(args)
    tools = tools_for(args, TOOLS)
    if any(t in tools for t in ('copilot', 'opencode')):
        drive = os.path.splitdrive(ROOT)[0].lower()
        other = [h for h in homes if os.path.splitdrive(h)[0].lower() != drive]
        if other:
            raise SystemExit(f'The harness ({drive.upper()}) and these profiles are on different drives: '
                             f'{", ".join(other)}. Hardlinks only work within one drive; move the harness.')
    if os.path.isdir(os.path.join(ROOT, '.git')):
        say('WARN', 'the harness still has .git: if it is the template\'s, remove it (README §3.1)')

    print(f'Harness {state["project"]!r} ({state["slug"]}, {state["lang"]}) at {ROOT}')
    if first:
        print('\nNames and language')
        act(f'language: {state["lang"]}', apply_language, state['lang'])
        act(f'names: <PROJECT> = {state["project"]}, <HARNESS> = this folder, prefix {state["slug"]}:',
            apply_names, state)
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
        print('\nStill to fill in (FILL-IN):')
        for rel, n in todo:
            print(f'  {rel} ({n})')
    print('\nNext: fill in the FILL-IN parts (README §3.3), reload VS Code and check each tool (README §3.4).')
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
        say('ok', 'copilot\\agents and opencode\\agents match personal\\agents')
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
        link, target = plugin_junction(state)
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
    parser = argparse.ArgumentParser(description='Sets up the harness on this PC (Windows).')
    parser.add_argument('--project', help='project name (first run): <PROJECT>, and its lowercase form the prefix')
    parser.add_argument('--tools', help=f'comma-separated, default all: {",".join(TOOLS)}')
    parser.add_argument('--lang', choices=LANGS, help='language of the pieces the model reads (first run; default en)')
    parser.add_argument('--users', help='comma-separated Windows users to wire up (default: you)')
    parser.add_argument('--home', action='append', help=argparse.SUPPRESS)   # a fake profile folder, for tests
    parser.add_argument('--vscode-permissions', action='store_true',
                        help='VS Code: read the harness and run the sensor without asking (Copilot)')
    parser.add_argument('--force', action='store_true', help='replace a file in the way, after backing it up')
    parser.add_argument('--dry-run', action='store_true', help='only say what would be done')
    parser.add_argument('--check', action='store_true', help='check links and settings; repair the safe ones')
    parser.add_argument('--uninstall', action='store_true', help='remove links and settings; keep the harness')
    args = parser.parse_args()

    if os.name != 'nt':
        print('setup.py only supports Windows for now. On Linux or macOS, follow the manual steps in the README '
              '(with symlinks instead of junctions and hardlinks, and python3 instead of py -3).')
        return 1
    global dry_run
    dry_run = args.dry_run
    if args.check:
        return check(args)
    if args.uninstall:
        return uninstall(args)
    return install(args)


if __name__ == '__main__':
    sys.exit(main())
