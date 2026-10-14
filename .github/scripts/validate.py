"""Structure checks for the one-agent-harness template. Standard library only.

Run from anywhere: python .github/scripts/validate.py
Exit code 1 if there is any error; warnings don't fail the build.
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TEXT_EXT = ('.md', '.py', '.json', '.jsonc', '.ts', '.svg', '.yml', '.yaml')
NAME_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
SKILL_WORDS_WARN = 700
# a real Windows user folder; placeholders (<user>, $u, %USERPROFILE%) and Public are fine
USER_PATH_RE = re.compile(r'[A-Za-z]:[\\/]+Users[\\/]+(?!Public\b|<|\$|%)[A-Za-z0-9._-]+')

errors, warnings = [], []
in_ci = os.environ.get('GITHUB_ACTIONS') == 'true'


def rel(path):
    return os.path.relpath(path, ROOT).replace('\\', '/')


def error(path, msg, line=None):
    errors.append((rel(path), line, msg))


def warn(path, msg, line=None):
    warnings.append((rel(path), line, msg))


def text_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != '.git']
        for f in files:
            if f.endswith(TEXT_EXT) or f in ('VERSION', 'LICENSE'):
                yield os.path.join(base, f)


def read(path):
    with open(path, 'rb') as f:
        raw = f.read()
    return raw, raw.decode('utf-8', errors='replace').replace('\r\n', '\n')


def frontmatter(path, text):
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    if not m:
        error(path, 'missing YAML frontmatter (the file must start with ---)')
        return None, text
    data = {}
    for line in m.group(1).splitlines():
        km = re.match(r'([A-Za-z_-]+):\s*(.*)$', line)
        if km:
            data[km.group(1)] = km.group(2).strip().strip('"').strip("'")
    return data, text[m.end():]


def check_encoding():
    for path in text_files():
        raw, text = read(path)
        if raw.startswith(b'\xef\xbb\xbf'):
            error(path, 'UTF-8 BOM at the start: it silently breaks SKILL.md frontmatter; save without BOM')
        for n, line in enumerate(text.splitlines(), 1):
            if USER_PATH_RE.search(line):
                error(path, 'absolute path to a real user folder; use a placeholder', n)


def check_skills():
    base = os.path.join(ROOT, 'personal', 'skills')
    for d in sorted(os.listdir(base)):
        path = os.path.join(base, d, 'SKILL.md')
        if not os.path.isfile(path):
            error(os.path.join(base, d), 'skill folder without SKILL.md')
            continue
        _, text = read(path)
        data, body = frontmatter(path, text)
        if data is None:
            continue
        name = data.get('name', '')
        if name != d:
            error(path, f'name "{name}" must match the folder name "{d}"')
        if not NAME_RE.match(name) or len(name) > 64:
            error(path, f'name "{name}": lowercase letters, digits and hyphens only (no _), 64 chars max')
        desc = data.get('description', '')
        if not desc:
            error(path, 'missing description: it is the only thing the model sees before loading the skill')
        elif len(desc) > 1024:
            error(path, f'description is {len(desc)} chars (1024 max)')
        words = len(body.split())
        if words > SKILL_WORDS_WARN:
            warn(path, f'{words} words in the body (aim for 600 or fewer)')


def check_agents():
    base = os.path.join(ROOT, 'personal', 'agents')
    for f in sorted(os.listdir(base)):
        if not f.endswith('.md'):
            continue
        path = os.path.join(base, f)
        _, text = read(path)
        data, _ = frontmatter(path, text)
        if data is None:
            continue
        for key in ('name', 'description', 'tools'):
            if not data.get(key):
                error(path, f'missing "{key}" in the frontmatter')
        if data.get('name') and not NAME_RE.match(data['name']):
            error(path, f'name "{data["name"]}": lowercase letters, digits and hyphens only')
        if data.get('tools', '').startswith('['):
            error(path, 'VS Code tool names in the original: Claude gets no tools; use "tools: Read, Grep, Glob, Bash"')


def load_json(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        error(path, f'invalid JSON: {e}')
        return None


def check_json():
    mp_path = os.path.join(ROOT, 'claude', '.claude-plugin', 'marketplace.json')
    mp = load_json(mp_path)
    if mp:
        if not NAME_RE.match(mp.get('name', '')):
            error(mp_path, 'marketplace name: lowercase letters, digits and hyphens only')
        for p in mp.get('plugins', []):
            if not NAME_RE.match(p.get('name', '')):
                error(mp_path, f'plugin name "{p.get("name")}": lowercase letters, digits and hyphens only')
            for key in ('strict', 'version'):
                if key in p:
                    error(mp_path, f'plugin "{p.get("name")}" has "{key}": on a plugin without plugin.json it breaks the whole marketplace')
    hooks_path = os.path.join(ROOT, 'personal', 'hooks', 'hooks.json')
    hooks = load_json(hooks_path)
    if hooks:
        for groups in hooks.get('hooks', {}).values():
            for group in groups:
                for h in group.get('hooks', []):
                    for script in re.findall(r'\$\{CLAUDE_PLUGIN_ROOT\}/([^"\s]+)', h.get('command', '')):
                        if not os.path.isfile(os.path.join(ROOT, 'personal', script)):
                            error(hooks_path, f'the hook runs "{script}", which does not exist in personal/')


def check_opencode():
    base = os.path.join(ROOT, 'opencode')
    # Config: JSONC with full-line comments only (the template's style), so it parses without dependencies
    cfg_path = os.path.join(base, 'opencode.jsonc')
    _, text = read(cfg_path)
    try:
        cfg = json.loads(re.sub(r'(?m)^\s*//.*$', '', text))
    except ValueError as e:
        error(cfg_path, f'invalid JSONC (only full-line // comments are allowed): {e}')
        cfg = None
    if cfg:
        rules = [r for r in cfg.get('permissions', []) if r.get('action') == 'skill']
        if not any(r.get('resource') == '*' and r.get('effect') == 'deny' for r in rules):
            error(cfg_path, 'no "skill" * deny rule: OpenCode would also list skills from other tools found above the repo')
        allowed = {r.get('resource') for r in rules if r.get('effect') == 'allow'}
        for skill in sorted(os.listdir(os.path.join(ROOT, 'personal', 'skills'))):
            if skill not in allowed:
                error(cfg_path, f'skill "{skill}" is missing from the skill allowlist: OpenCode would not see it')
    # Agents: generated copies up to date; OpenCode's without `tools:` (it ignores the whole agent) and
    # Copilot's with `tools:` (without the list, VS Code doesn't give the agent the tools it needs)
    sys.path.insert(0, base)
    try:
        import sync
        for source, target, expected in sync.pairs():
            _, current = read(target) if os.path.isfile(target) else (b'', None)
            has_tools = re.search(r'(?m)^tools:', expected.split('\n---', 1)[0])
            if current != expected:
                error(target, f'out of date with personal/agents/{source}: run py -3 opencode/sync.py')
            elif os.path.dirname(os.path.abspath(target)) == os.path.join(base, 'agents') and has_tools:
                error(target, 'has "tools:" in the frontmatter: OpenCode ignores the whole agent')
            elif os.path.dirname(os.path.abspath(target)) != os.path.join(base, 'agents') and not has_tools:
                error(target, 'Copilot copy without "tools:": check TARGETS in opencode/sync.py')
    finally:
        sys.path.pop(0)
    # Plugin: the sensor script exists
    plugin = os.path.join(base, 'plugins', 'sensor.ts')
    _, text = read(plugin)
    for script in re.findall(r'<HARNESS>/(personal/[^"]+)"', text):
        if not os.path.isfile(os.path.join(ROOT, script)):
            error(plugin, f'the plugin runs "{script}", which does not exist')


def check_svg():
    for base, _, files in os.walk(os.path.join(ROOT, 'img')):
        for f in files:
            if f.endswith('.svg'):
                try:
                    ET.parse(os.path.join(base, f))
                except ET.ParseError as e:
                    error(os.path.join(base, f), f'SVG is not well-formed XML: {e}')


def check_version():
    path = os.path.join(ROOT, 'VERSION')
    if not os.path.isfile(path):
        error(path, 'VERSION file is missing')
        return
    _, text = read(path)
    if not re.fullmatch(r'\d+\.\d+\.\d+\n?', text):
        error(path, f'VERSION must be MAJOR.MINOR.PATCH, found {text.strip()!r}')


def slug(heading):
    h = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', heading.strip().lower())
    h = re.sub(r'[^\w\- ]', '', h)
    return h.replace(' ', '-')


def anchors(path, cache={}):
    if path not in cache:
        _, text = read(path)
        text = re.sub(r'```.*?```', '', text, flags=re.S)
        seen, found = {}, set()
        for m in re.finditer(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
            s = slug(m.group(1))
            n = seen.get(s, 0)
            found.add(s if n == 0 else f'{s}-{n}')
            seen[s] = n + 1
        cache[path] = found
    return cache[path]


def check_links():
    for path in text_files():
        if not path.endswith('.md'):
            continue
        _, text = read(path)
        lines = text.splitlines()
        in_code = False
        for n, line in enumerate(lines, 1):
            if line.lstrip().startswith('```'):
                in_code = not in_code
                continue
            if in_code:
                continue
            line = re.sub(r'`[^`]*`', '', line)
            targets = re.findall(r'\]\(([^)\s]+)\)', line) + re.findall(r'src="([^"]+)"', line)
            for target in targets:
                if re.match(r'[a-z]+:', target) or '<' in target:
                    continue
                file_part, _, anchor = target.partition('#')
                dest = os.path.normpath(os.path.join(os.path.dirname(path), file_part)) if file_part else path
                if not os.path.exists(dest):
                    error(path, f'broken link: {target}', n)
                elif anchor and dest.endswith('.md') and anchor not in anchors(dest):
                    error(path, f'broken anchor: {target}', n)


def main():
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    for check in (check_encoding, check_skills, check_agents, check_json, check_opencode, check_svg, check_version, check_links):
        check()
    for kind, items in (('warning', warnings), ('error', errors)):
        for path, line, msg in items:
            if in_ci:
                loc = f'file={path}' + (f',line={line}' if line else '')
                print(f'::{kind} {loc}::{msg}')
            else:
                print(f'{kind.upper()} {path}' + (f':{line}' if line else '') + f'  {msg}')
    print(f'\n{len(errors)} errors · {len(warnings)} warnings')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
