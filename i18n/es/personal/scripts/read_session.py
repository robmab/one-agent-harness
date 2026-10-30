"""Pasa una sesión de Claude Code, Copilot (chat o CLI), OpenCode o DeepSeek Harness a una línea de tiempo legible, para repasarla.

Uso:
    py -3 read_session.py <claude|copilot|copilot-cli|opencode|dsh> [--session ID] [--since CUANDO] [--until CUANDO]
                          [--list] [--summary] [--full] [--out FICHERO] [--repo RUTA]
    py -3 read_session.py --session ID [...]     # sin la herramienta: busca el id en todas

--session  el id de la sesión (vale el principio). Sin él, la sesión principal más reciente del repo,
           de todos los usuarios del PC; la de un subagente (la del repaso, la del revisor) nunca se
           elige por defecto. --list las enseña con su última actividad (con --since, todas las que han
           tenido actividad desde entonces), con los subagentes marcados.
--since / --until  'HH:MM' (del último día de la sesión), 'AAAA-MM-DD' o 'AAAA-MM-DD HH:MM', en hora
           local: solo se lee ese tramo (un chat largo de Copilot puede durar semanas).
--summary  solo los mensajes del usuario y cómo se usó cada pieza del harness.
--full     sin recortar nada (el informe del revisor, un mensaje de cierre largo).
--out      lo escribe en ese fichero en UTF-8 en vez de en pantalla (PowerShell 5.1 redirige en UTF-16).

Solo lee: no toca ningún log. De la base de datos de OpenCode solo lee las tablas de sesiones (la misma
base guarda tokens de cuentas: ni se miran). Los logs de DeepSeek Harness van en zstd: para leerlos
hace falta Python 3.14.
"""
import argparse
import json
import os
import re
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import unquote

HARNESS = Path(__file__).resolve().parents[2]

# lo que tiene este harness además de personal\skills (vacío en la plantilla)
EXTRA_SKILLS = []        # skills que viven en otro sitio, p. ej. las del equipo en el repo
ALIAS = {}               # otro nombre o trozo de ruta -> la skill que es
EXTRA_FILES = []         # ficheros del harness que se leen por nombre, fuera de personal\*.md
LEGACY = {}              # nombre actual -> nombre antiguo (o una tupla de ellos), para que los logs viejos sigan contando

MSG = {
    'user': 'USUARIO', 'agent': 'AGENTE', 'day': 'DÍA',
    'title': '======== EL HARNESS EN ESTA SESIÓN (pruebas para el repaso)',
    'window': '  tramo leído: {since} → {until}',
    'skill': '  skill {s}: cargada {n} vez/veces', 'skill_doc': ' (+{d} lectura(s) del doc al que apunta)',
    'unused': '  skills sin cargar: {lst}', 'none': 'ninguna',
    'file': '  fichero {f}: leído {n} vez/veces',
    'sensor': '  sensor: lanzado {run} vez/veces por el agente; {hook} resultado(s) del hook o del plugin; {err} con ERROR',
    'agent_n': '  agente {a}: lanzado {n} vez/veces', 'agent_0': '  agente {a}: no se lanzó',
    'sub_calls': '  llamadas de subagentes: {n} (no cuentan en las piezas de arriba)',
    'waits': '  esperas activas (sleep): {n}, {s} s',
    'model': '  modelo: {m} · llamadas: {c} · errores de herramienta: {e}',
    'tools': '  herramientas más usadas: ',
    'tokens': '  tokens: entrada {i}, salida {o}, caché leída {c}',
    'creds': '  contraseña en una URL: {n} llamada(s) (aquí enmascarada; nunca la copies al informe)',
    'system': '  prompt de sistema: {n} registrado(s), {k} con el texto del harness (closing.md)',
    'system_0': ': el ajuste no le llega al modelo (DeepSeek: lo tapa el persona del preset)',
    'rows_missing': '  al último prompt de sistema le faltan {n} fila(s) de {f}: {rows} (la herramienta lo carga al arrancar: reiníciala)',
    'other_tool': '(no es una sesión de {tool}: es de {other})',
    'no_sessions': 'No hay sesiones de {tool} para {repo}.',
    'not_found': 'No encuentro la sesión {s}. Prueba con --list.',
    'bad_when': "No entiendo {w!r}: usa HH:MM, AAAA-MM-DD o 'AAAA-MM-DD HH:MM'.",
    'session': 'Sesión {s} ({tool})', 'sub': '(subagente)', 'to_sub': '(a un subagente) ',
    'approval': 'ESPERANDO LA APROBACIÓN DEL USUARIO ({tool}): {why}',
    'zstd': 'Los logs de DeepSeek Harness van en zstd: para leerlos hace falta Python 3.14.',
    'h_session': 'id de la sesión (vale el principio); sin él, la principal más reciente',
    'h_since': "desde: HH:MM, AAAA-MM-DD o 'AAAA-MM-DD HH:MM' (hora local)",
    'h_until': 'hasta, mismos formatos',
    'h_list': 'lista las sesiones (las 10 más recientes, o todas desde --since) con su última actividad, y sale',
    'h_summary': 'solo los mensajes del usuario y el uso del harness',
    'h_repo': 'el repo de las sesiones (por defecto, la carpeta actual)',
    'h_tool': 'di la herramienta, o pasa --session para buscarla en todas',
    'h_full': 'sin recortar nada',
    'h_out': 'lo escribe en este fichero (UTF-8) en vez de en pantalla',
}

CUT_USER = 1500
CUT_TEXT = 800
CUT_LAST = 8000   # el último mensaje del agente antes de cada turno del usuario: en una sesión de preguntas, es la respuesta
CUT_RESULT = 300
FULL = False      # --full: sin recortar nada
SHELL_TOOLS = {'bash', 'powershell', 'pwsh', 'terminal', 'shell', 'run_in_terminal'}
AGENT_TOOLS = {'agent', 'task', 'subagent'}
ERROR_RX = re.compile(r'Traceback \(most recent call last\)|\b[Ee]xit(?:ed with)?(?: code)?\s*[:=]?\s*[1-9]\d*\b|^fatal: ', re.M)
# usuario:contraseña@ en una URL (no cuentan marcadores como <pw>, {pw} o $PW): se enseña enmascarada y se cuenta
CRED_RX = re.compile(r'(\b[a-z][a-z0-9+.-]*://[^\s:/@"\'`]+:)(?!\*+@|<[^>]*>@|\{[^}]*\}@|\$\w+@)[^\s@"\'`/]+@')
SENSOR_RUN_RX =r'(?:\bpy(?:thon3?)?(?:\.exe)?(?:\s+-3)?|python\.exe)\s[^|;\n]*\b(?:{names})\b'
SENSOR = 'check.py'


def names_of(name):
    old = LEGACY.get(name, ())
    return [name] + ([old] if isinstance(old, str) else list(old))


# la línea que deja el sensor por un hook o un plugin: "check: OK", "check: <fichero> sin mirar…",
# "check (avisos…", "check encontró…"
HOOK_RX = re.compile(r'\b(?:{})(?::|\s\((?:warnings|avisos)|\s(?:found|encontró))'.format(
    '|'.join(re.escape(n.removesuffix('.py')) for n in names_of(SENSOR))))
# el prompt de sistema de un subagente (la copia del revisor, o el preámbulo de subagente de la herramienta): no el principal
SUB_PROMPT_RX = re.compile(r'As a sub-agent|(?:Generated by|Generado por) opencode/sync\.py')


def homes():
    # los logs son de cada usuario: mira todos los perfiles que se puedan leer
    root = Path.home().parent
    try:
        return [p for p in root.iterdir() if p.is_dir() and not p.name.startswith(('Default', 'Public', 'All '))]
    except OSError:
        return [Path.home()]


def when(ts):
    """A log timestamp (ms or ISO, often in UTC) as local, naive time."""
    if not ts:
        return None
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts / 1000)
    try:
        t = datetime.fromisoformat(str(ts).replace('Z', '+00:00'))
    except ValueError:
        return None
    return t.astimezone().replace(tzinfo=None) if t.tzinfo else t


def cut(text, n):
    text = CRED_RX.sub(r'\1***@', ' '.join(str(text).split()))
    return text if FULL or len(text) <= n else text[:n] + ' […]'


def as_text(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)


def as_dict(v):
    if isinstance(v, dict):
        return v
    try:
        d = json.loads(v)
        return d if isinstance(d, dict) else {}
    except (TypeError, ValueError):
        return {}


class Timeline:
    def __init__(self):
        self.events = []    # dicts: t, kind (user|text|call|result|usage|system), name, data, text, error
        self.model = ''

    def add(self, kind, ts, **kw):
        self.events.append(dict(kind=kind, t=when(ts) if not isinstance(ts, datetime) else ts, **kw))

    def user(self, ts, text):
        if str(text).strip():
            self.add('user', ts, text=text)

    def text(self, ts, text):
        if str(text).strip():
            self.add('text', ts, text=text)

    def call(self, ts, name, args, sub=False):
        self.add('call', ts, name=name or 'tool', data=args, text=as_text(args), sub=sub)

    def result(self, ts, text, error=False):
        t = str(text or '')
        self.add('result', ts, text=t, error=bool(error) or bool(ERROR_RX.search(t)))

    def usage(self, ts, i=0, o=0, c=0):
        self.add('usage', ts, i=i or 0, o=o or 0, c=c or 0)

    def window(self, since, until):
        # lo que no trae hora toma la del anterior, para que un resultado vaya con su llamada
        last = None
        for e in self.events:
            e['t'] = e['t'] or last
            last = e['t']
        self.events = [e for e in self.events if (not since or not e['t'] or e['t'] >= since)
                       and (not until or not e['t'] or e['t'] <= until)]


# ---------------------------------------------------------------- Claude Code

def sessions_claude(repo):
    slug = re.sub(r'[^A-Za-z0-9]', '-', repo) if repo else '*'   # repo None: todos los proyectos
    files = []
    for h in homes():
        files += list((h / '.claude' / 'projects').glob(f'{slug}/*.jsonl'))
    return sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)


def read_claude(f, tl):
    for line in open(f, encoding='utf-8'):
        o = json.loads(line)
        t, ts = o.get('type'), o.get('timestamp')
        if t == 'user' and not o.get('isMeta'):
            c = o['message']['content']
            if isinstance(c, str):
                tl.user(ts, c)
                continue
            for b in c:
                if b.get('type') == 'text':
                    tl.user(ts, b['text'])
                elif b.get('type') == 'tool_result':
                    r = b.get('content')
                    if isinstance(r, list):
                        r = ' '.join(x.get('text', '') for x in r if isinstance(x, dict))
                    tl.result(ts, r, b.get('is_error'))
        elif t == 'assistant':
            m = o['message']
            tl.model = m.get('model') or tl.model
            u = m.get('usage') or {}
            tl.usage(ts, u.get('input_tokens'), u.get('output_tokens'), u.get('cache_read_input_tokens'))
            for b in m.get('content', []):
                if b.get('type') == 'text':
                    tl.text(ts, b['text'])
                elif b.get('type') == 'tool_use':
                    tl.call(ts, b['name'], b['input'])
        elif t == 'attachment' and str(o['attachment'].get('type', '')).startswith('hook_') \
                and o['attachment'].get('type') != 'hook_success':
            # lo que ve el modelo de un hook (la línea del sensor, o su ERROR bloqueante); hook_success lo repite en crudo
            a = o['attachment']
            blocking = (a.get('blockingError') or {}).get('blockingError') if isinstance(a.get('blockingError'), dict) \
                else a.get('blockingError')
            tl.result(ts, as_text(a.get('content') or blocking or a.get('stderr') or a), 'error' in a.get('type', ''))


def first_claude(f):
    for line in open(f, encoding='utf-8'):
        o = json.loads(line)
        if o.get('type') == 'user' and not o.get('isMeta'):
            c = o['message']['content']
            return c if isinstance(c, str) else ' '.join(b.get('text', '') for b in c if b.get('type') == 'text')
    return ''


# ---------------------------------------------------------------- Copilot (VS Code)

def vscode_storage(h):
    if sys.platform == 'win32':
        return h / 'AppData' / 'Roaming' / 'Code' / 'User' / 'workspaceStorage'
    if sys.platform == 'darwin':
        return h / 'Library' / 'Application Support' / 'Code' / 'User' / 'workspaceStorage'
    return h / '.config' / 'Code' / 'User' / 'workspaceStorage'


def sessions_copilot(repo):
    uri = unquote(Path(repo).resolve().as_uri()).lower() if repo else None
    files = []
    for h in homes():
        for w in vscode_storage(h).glob('*/workspace.json'):
            try:
                folder = unquote(json.loads(w.read_text(encoding='utf-8')).get('folder', '')).lower()
            except (OSError, ValueError):
                continue
            if uri is None or folder == uri:
                files += list((w.parent / 'chatSessions').glob('*.jsonl'))
    return sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)


def rebuild_copilot(f):
    # el .jsonl de Copilot es un registro de parches sobre un estado inicial
    state = None
    for line in open(f, encoding='utf-8'):
        if not line.strip():
            continue
        d = json.loads(line)
        k, v, path = d.get('kind'), d.get('v'), d.get('k')
        if k == 0:
            state = v
            continue
        obj = state
        for p in path[:-1]:
            obj = obj[p]
        if k == 1:
            obj[path[-1]] = v
        elif k == 2:
            items = obj[path[-1]]
            if items is None:
                items = obj[path[-1]] = []
            if d.get('i') is not None:
                del items[d['i']:]
            items.extend(v or [])
    return state or {}


def value(v):
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        return v.get('value') or v.get('text') or ''
    return ''


def read_copilot(f, tl):
    for req in rebuild_copilot(f).get('requests', []):
        ts = req.get('timestamp')
        tl.model = req.get('modelId') or tl.model
        tl.usage(ts, req.get('promptTokens'), req.get('completionTokens'))
        msg = req.get('message', {})
        tl.user(ts, value(msg.get('text') or msg))
        for part in req.get('response', []) or []:
            k = part.get('kind')
            if k in (None, 'markdownContent'):
                tl.text(ts, value(part.get('value', part.get('content', ''))))
            elif k == 'toolInvocationSerialized':
                data = part.get('toolSpecificData') or {}
                if data.get('kind') == 'terminal':
                    cl = data.get('commandLine', {})
                    tl.call(ts, 'terminal', cl.get('original') if isinstance(cl, dict) else cl)
                    out = data.get('terminalCommandOutput') or {}
                    code = (data.get('terminalCommandState') or {}).get('exitCode')
                    tl.result(ts, out.get('text', '') if isinstance(out, dict) else out, code not in (None, 0))
                elif data.get('kind') == 'subagent' or 'agentName' in data:
                    tl.call(ts, f'subagent:{data.get("agentName")}', data.get('prompt'))
                    tl.result(ts, data.get('result'))
                else:
                    tl.call(ts, part.get('toolId') or 'tool', value(part.get('invocationMessage')))
            elif k == 'textEditGroup':
                tl.call(ts, 'edit', part.get('uri', {}).get('path', ''))


def first_copilot(f):
    reqs = rebuild_copilot(f).get('requests', [])
    return value(reqs[0].get('message', {}).get('text')) if reqs else ''


# ---------------------------------------------------------------- Copilot CLI (also VS Code's agent sessions)

def sessions_copilot_cli(repo):
    target = os.path.normcase(str(Path(repo).resolve())) if repo else None
    files = []
    for h in homes():
        for w in (h / '.copilot' / 'session-state').glob('*/workspace.yaml'):
            try:
                meta = dict(l.split(': ', 1) for l in w.read_text(encoding='utf-8').splitlines() if ': ' in l)
            except OSError:
                continue
            folders = {os.path.normcase(str(Path(meta.get(k, '').strip()).resolve())) for k in ('cwd', 'git_root') if meta.get(k)}
            if (target is None or target in folders) and (w.parent / 'events.jsonl').exists():
                files.append(w.parent / 'events.jsonl')
    return sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)


def read_copilot_cli(f, tl):
    for line in open(f, encoding='utf-8'):
        if not line.strip():
            continue
        e = json.loads(line)
        t, d, ts = e.get('type'), e.get('data') or {}, e.get('timestamp')
        if t == 'session.start':
            tl.model = d.get('selectedModel') or tl.model
        elif t == 'system.message':
            tl.add('system', ts, text=d.get('content', ''))
        elif t == 'user.message':
            # los encargos que el agente manda a sus subagentes llegan como mensajes del usuario, marcados con su origen
            if str(d.get('source', '')).startswith('agent-'):
                tl.text(ts, MSG['to_sub'] + d.get('content', ''))
            else:
                tl.user(ts, d.get('content', ''))
        elif t == 'assistant.message':
            tl.text(ts, d.get('content', ''))
        elif t == 'session.usage_record':
            u = d.get('usage') or {}
            tl.model = u.get('model') or tl.model
            tl.usage(ts, u.get('inputTokens'), u.get('outputTokens'), u.get('cacheReadTokens'))
        elif t == 'tool.execution_start':
            tl.call(ts, d.get('toolName', 'tool'), d.get('arguments', ''), bool(d.get('parentToolCallId')))
        elif t == 'tool.execution_complete':
            r = d.get('result') or d.get('error') or {}
            # una llamada MCP fallida no trae content, solo error.message
            tl.result(ts, (r.get('content') or r.get('message', '')) if isinstance(r, dict) else r, not d.get('success', True))
        elif t == 'hook.end' and d.get('output'):
            # lo que le dice al modelo un hook tuyo (la línea del sensor, o el bloqueo del guard)
            tl.result(ts, as_text(d['output']), not d.get('success', True))


def first_copilot_cli(f):
    for line in open(f, encoding='utf-8'):
        if '"user.message"' in line:
            return json.loads(line).get('data', {}).get('content', '')
    return ''


# ---------------------------------------------------------------- OpenCode

def sessions_opencode(repo):
    folder = str(Path(repo).resolve()).replace('\\', '/') if repo else None
    rows = []
    for h in homes():
        db = h / '.local' / 'share' / 'opencode' / 'opencode.db'
        if not db.exists():
            continue
        con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
        rows += [(t, db, sid) for sid, t in con.execute(
            'select id, time_updated from session_v2 where (? is null or lower(directory) = lower(?)) and parent_id is null',
            (folder, folder))]
    return [(db, sid) for _, db, sid in sorted(rows, reverse=True)]


def read_opencode(s, tl):
    db, sid = s
    con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    for kind, ts, data in con.execute(
            'select type, time_created, data from session_message where session_id = ? order by seq', (sid,)):
        d = json.loads(data)
        if kind == 'user':
            tl.user(ts, d.get('text', ''))
        elif kind == 'assistant':
            tl.model = (d.get('model') or {}).get('id') or tl.model
            tok = d.get('tokens') or {}
            tl.usage(ts, tok.get('input'), tok.get('output'), (tok.get('cache') or {}).get('read'))
            for c in d.get('content', []):
                if c.get('type') == 'text':
                    tl.text(ts, c.get('text', ''))
                elif c.get('type') == 'tool':
                    st = c.get('state') or {}
                    tl.call(ts, c.get('name', 'tool'), st.get('input', {}))
                    if st.get('status') == 'error':
                        tl.result(ts, json.dumps(st.get('error'), ensure_ascii=False), True)
                    else:
                        # las versiones antiguas guardan el resultado en output; las nuevas, en partes de content
                        tl.result(ts, st.get('output') or ' '.join(
                            p.get('text', '') for p in st.get('content') or [] if isinstance(p, dict)))
            if d.get('error'):
                tl.result(ts, json.dumps(d['error'], ensure_ascii=False)[:300], True)


def first_opencode(s):
    db, sid = s
    con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    row = con.execute("select data from session_message where session_id = ? and type = 'user' order by seq limit 1",
                      (sid,)).fetchone()
    return json.loads(row[0]).get('text', '') if row else ''


# ---------------------------------------------------------------- DeepSeek Harness

def sessions_dsh(repo):
    folder = '--' + re.sub(r'[^A-Za-z0-9]+', '-', str(Path(repo).resolve())) + '--' if repo else '*'
    files = []
    for h in homes():
        files += list((h / '.dsh' / 'sessions' / folder).glob('*/session.v4.jsonl.zstd'))
    return sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)


def events_dsh(f):
    try:
        from compression import zstd
    except ImportError:
        sys.exit(MSG['zstd'])
    text = zstd.decompress(f.read_bytes()).decode('utf-8')
    return [json.loads(x) for x in text.splitlines() if x.strip()]


def read_dsh(f, tl):
    for e in events_dsh(f):
        t, d, ts = e.get('type'), e.get('data') or {}, e.get('time')
        if t == 'user/message' and (d.get('source') or {}).get('kind') == 'user':
            tl.user(ts, ' '.join(c.get('text', '') for c in d.get('content', [])))
        elif t in ('model/selection', 'request/context'):
            tl.model = d.get('model', tl.model)
        elif t == 'approval/asked':
            tl.result(ts, MSG['approval'].format(tool=d.get('toolName', ''), why=d.get('reason', '')), True)
        elif t == 'system/message':
            m = d.get('message') or {}
            tl.add('system', ts, text=' '.join(c.get('text', '') for c in m.get('content', [])))
        elif t == 'assistant/message':
            u = d.get('usage') or {}
            tl.usage(ts, u.get('inputTokens'), u.get('outputTokens'), u.get('cacheReadTokens'))
            for c in (d.get('message') or {}).get('content', []):
                if c.get('type') == 'text':
                    tl.text(ts, c.get('text', ''))
        elif t == 'tool/call':
            tl.call(ts, d.get('name', 'tool'), d.get('arguments', ''))
        elif t == 'tool/result':
            m = d.get('message') or {}
            tl.result(ts, ' '.join(c.get('text', '') for c in m.get('content', [])), m.get('isError'))


def first_dsh(f):
    for e in events_dsh(f):
        d = e.get('data') or {}
        if e.get('type') == 'user/message' and (d.get('source') or {}).get('kind') == 'user':
            return ' '.join(c.get('text', '') for c in d.get('content', []))
    return ''


def is_subagent(s):
    # un subagente de DeepSeek guarda su sesión en una carpeta sin el prefijo session-
    return not isinstance(s, tuple) and s.name.startswith('session.') and not s.parent.name.startswith('session-')


# ---------------------------------------------------------------- the harness in the session

def pieces():
    # las piezas salen de la carpeta del harness: así una skill nueva entra sola
    p = HARNESS / 'personal'
    return {
        'skills': sorted(d.name for d in (p / 'skills').iterdir() if (d / 'SKILL.md').exists()) + EXTRA_SKILLS,
        'files': sorted(f.name for f in p.glob('*.md')) + sorted(f.name for f in p.glob('checklists/*.md'))
        + EXTRA_FILES,
        'sensor': SENSOR,
        'agents': sorted(f.name.split('.')[0] for f in (p / 'agents').glob('*.md')),
    }


def searches(e):
    """Whether a call searches (grep, find, glob…) instead of reading: hitting a SKILL.md isn't loading it."""
    name = e['name'].lower()
    return any(x in name for x in ('find', 'search', 'grep', 'glob')) or (
        (name in SHELL_TOOLS or 'shell' in name)
        and bool(re.search(r'\b(?:grep|rg|Select-String|findstr|sls)\b', e['text'], re.I)))


def known_skill(s, known):
    s = ALIAS.get(s, s)
    return next((k for k in known if s in names_of(k)), None)


def skill_loaded(e, known):
    """The skill a call loads, or None: the skill tool, or reading its SKILL.md (a search or a mention doesn't count)."""
    if e['name'].lower() == 'skill':
        s = as_dict(e['data'])
        return known_skill(str(s.get('skill') or s.get('name') or s.get('id') or '').split(':')[-1], known)
    if searches(e):
        return None
    m = re.search(r'Reading skill \[([\w:-]+)\]', e['text'])
    if not m and reads(e):
        m = re.search(r'skills[\\/]+([\w-]+)[\\/]+SKILL\.md', e['text'])
    return known_skill(m.group(1).split(':')[-1], known) if m else None


def doc_read(e, known):
    """The pointer skill whose doc a call reads (an ALIAS path), or None."""
    if searches(e) or not reads(e) or skill_loaded(e, known):
        return None
    path = e['text'].replace('\\\\', '/').replace('\\', '/')
    return known_skill(next((v for k, v in ALIAS.items() if '/' in k and k in path), ''), known)


def reads(e):
    """Whether a call reads a file (a read tool, or cat/Get-Content… in a shell), not just mentions it in a plan."""
    name = e['name'].lower()
    if 'read' in name or name in ('view', 'open', 'grep', 'glob'):
        return True
    return (name in SHELL_TOOLS or 'shell' in name) and bool(
        re.search(r'\b(?:cat|type|Get-Content|gc|head|tail|more|less|Select-String|grep|rg|findstr)\b', e['text'], re.I))


def launches(e, agent):
    """Whether a call launches that agent: by its name or type, by pointing at its .agent.md, or by a brief that
    says it is that agent ("the `reviewer` agent", when the tool has no agent files); never the bare word."""
    name = e['name'].lower()
    if name.startswith('subagent:'):
        return name.split(':', 1)[1] in names_of(agent)
    if name not in AGENT_TOOLS:
        return False
    d = as_dict(e['data'])
    kind = str(d.get('subagent_type') or d.get('agent_type') or d.get('agent') or d.get('agentName') or '').split(':')[-1].lower()
    text = e['text'].replace('\\\\', '/').replace('\\', '/').lower()
    return any(kind == x or f'{x}.agent.md' in text or f'agents/{x}.md' in text
               or re.search(rf'\b(?:agent|agente)\s+`{re.escape(x)}`|`{re.escape(x)}`\s+agent\b', text) for x in names_of(agent))


def harness_use(tl, since=None, until=None):
    pz = pieces()
    # que un subagente lea own.md o pase el sensor no es que lo haga el agente
    every_call = [e for e in tl.events if e['kind'] == 'call']
    calls = [e for e in every_call if not e['sub']]
    results = [e for e in tl.events if e['kind'] == 'result']
    out = ['', MSG['title']]
    if since or until:
        out.append(MSG['window'].format(since=since or '…', until=until or '…'))
    loads = Counter(filter(None, (skill_loaded(e, pz['skills']) for e in calls)))
    docs = Counter(filter(None, (doc_read(e, pz['skills']) for e in calls)))
    for s in pz['skills']:
        if loads[s] or docs[s]:
            out.append(MSG['skill'].format(s=s, n=loads[s]) + (MSG['skill_doc'].format(d=docs[s]) if docs[s] else ''))
    out.append(MSG['unused'].format(lst=', '.join(s for s in pz['skills'] if not loads[s] and not docs[s]) or MSG['none']))
    for f in pz['files']:
        n = sum(1 for e in calls if reads(e) and any(x in e['text'] for x in names_of(f)))
        if n:
            out.append(MSG['file'].format(f=f, n=n))
    sensor = re.compile(SENSOR_RUN_RX.format(names='|'.join(re.escape(x) for x in names_of(pz['sensor']))))
    runs = [e for e in calls if (e['name'].lower() in SHELL_TOOLS or 'shell' in e['name'].lower())
            and sensor.search(e['text'])]
    hooks = [e for e in results if HOOK_RX.search(e['text'])]
    # solo la línea "encontró" del propio sensor: un aviso o un texto pegado que diga ERROR no cuentan
    errs = sum(1 for e in results if (m := HOOK_RX.search(e['text'])) and m.group(0).endswith(('found', 'encontró')))
    out.append(MSG['sensor'].format(run=len(runs), hook=len(hooks), err=errs))
    for a in pz['agents']:
        n = sum(1 for e in calls if launches(e, a))
        out.append(MSG['agent_n' if n else 'agent_0'].format(a=a, n=n))
    if len(every_call) > len(calls):
        out.append(MSG['sub_calls'].format(n=len(every_call) - len(calls)))
    sleeps = [e for e in calls if re.search(r'\b(?:Start-Sleep|sleep)\s+(?:-Seconds\s+)?\d', e['text'])]
    if sleeps:
        secs = sum(int(m) for e in sleeps for m in re.findall(r'(?:Start-Sleep|sleep)\s+(?:-Seconds\s+)?(\d+)', e['text']))
        out.append(MSG['waits'].format(n=len(sleeps), s=secs))
    tools = Counter(e['name'] for e in every_call)
    out.append(MSG['model'].format(m=tl.model or '?', c=len(every_call), e=sum(1 for e in results if e['error'])))
    out.append(MSG['tools'] + ', '.join(f'{k} ×{v}' for k, v in tools.most_common(12)))
    use = [e for e in tl.events if e['kind'] == 'usage']
    if any(e['i'] or e['o'] for e in use):
        out.append(MSG['tokens'].format(i=f"{sum(e['i'] for e in use):,}".replace(',', '.'), o=f"{sum(e['o'] for e in use):,}".replace(',', '.'),
                                        c=f"{sum(e['c'] for e in use):,}".replace(',', '.')))
    creds = sum(1 for e in calls if CRED_RX.search(e['text']))
    if creds:
        out.append(MSG['creds'].format(n=creds))
    prompts = [e['text'] for e in tl.events if e['kind'] == 'system' and not SUB_PROMPT_RX.search(e['text'])]
    if prompts:
        k = sum(1 for p in prompts if 'closing.md' in p)
        out.append(MSG['system'].format(n=len(prompts), k=k) + ('' if k else MSG['system_0']))
        out += rows_missing(prompts[-1])
    return out


def rows_missing(prompt):
    """Las filas del router que no lleva el prompt: una herramienta que carga las instrucciones al arrancar se queda con las viejas."""
    for router in sorted((HARNESS / 'copilot').glob('*.instructions.md')):
        rows = [r.split('|')[1].strip() for r in router.read_text(encoding='utf-8').splitlines()
                if r.startswith('| ') and not r.startswith('|---')][1:]   # [1:]: la cabecera
        flat = ' '.join(prompt.split())
        missing = [r for r in rows if ' '.join(r.split()) not in flat]
        if missing and 'closing.md' in prompt:
            return [MSG['rows_missing'].format(n=len(missing), f=router.name, rows='; '.join(cut(r, 60) for r in missing))]
    return []


def render(tl, summary):
    out, day = [], None
    last, seen, after_agent = set(), False, False
    for i in range(len(tl.events) - 1, -1, -1):
        if tl.events[i]['kind'] == 'user':
            seen = False
        elif tl.events[i]['kind'] == 'text' and not seen:
            last.add(i)
            seen = True
    for i, e in enumerate(tl.events):
        t = e['t']
        if t and t.date() != day:
            day = t.date()
            out.append(f'\n======== {MSG["day"]} {day.isoformat()}')
        hm = t.strftime('%H:%M') if t else '--:--'
        k = e['kind']
        if k == 'user':
            out.append(f'\n##### {hm} {MSG["user"]}: {cut(e["text"], CUT_USER)}')
        elif summary or k == 'usage':
            continue
        elif k == 'text':
            out.append(f'  {hm} {MSG["agent"]}: {cut(e["text"], CUT_LAST if i in last else CUT_TEXT)}')
        elif k == 'call':
            length = 2000 if re.search(r'agent|task|subagent|skill', e['name'], re.I) else CUT_RESULT
            out.append(f'  {hm} → {e["name"]} {cut(e["text"], length)}')
            after_agent = e['name'].lower() in AGENT_TOOLS or e['name'].startswith('subagent:')
        elif k == 'result' and e['text'].strip():
            # lo que devuelve un subagente es su informe: recortado, había que sacarlo de la base de datos
            length = CUT_LAST if after_agent else 1500 if HOOK_RX.search(e['text']) or e['error'] else CUT_RESULT
            out.append(f'      {"✗" if e["error"] else "←"} {cut(e["text"], length)}')
    return out


def parse_when(w, last_day, end=False):
    if not w:
        return None
    for fmt in ('%Y-%m-%d %H:%M', '%Y-%m-%d', '%H:%M'):
        try:
            t = datetime.strptime(w, fmt)
        except ValueError:
            continue
        if fmt == '%H:%M':
            t = datetime.combine(last_day, t.time())
        if fmt == '%Y-%m-%d' and end:
            t += timedelta(days=1) - timedelta(seconds=1)
        return t
    sys.exit(MSG['bad_when'].format(w=w))


READERS = {
    'claude': (sessions_claude, read_claude, first_claude),
    'copilot': (sessions_copilot, read_copilot, first_copilot),
    'copilot-cli': (sessions_copilot_cli, read_copilot_cli, first_copilot_cli),
    'opencode': (sessions_opencode, read_opencode, first_opencode),
    'dsh': (sessions_dsh, read_dsh, first_dsh),
}


def name(s):
    return s[1] if isinstance(s, tuple) else (s.parent.name if s.name.startswith(('session.', 'events.')) else s.stem)


def match(s, sid):
    return name(s).replace('session-', '').startswith(sid.replace('session-', ''))


def last_activity(s):
    if isinstance(s, tuple):
        db, sid = s
        con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
        return when(con.execute('select time_updated from session_v2 where id = ?', (sid,)).fetchone()[0])
    return datetime.fromtimestamp(s.stat().st_mtime)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('tool', nargs='?', choices=READERS)
    ap.add_argument('--session', help=MSG['h_session'])
    ap.add_argument('--since', help=MSG['h_since'])
    ap.add_argument('--until', help=MSG['h_until'])
    ap.add_argument('--list', action='store_true', help=MSG['h_list'])
    ap.add_argument('--summary', action='store_true', help=MSG['h_summary'])
    ap.add_argument('--full', action='store_true', help=MSG['h_full'])
    ap.add_argument('--out', help=MSG['h_out'])
    ap.add_argument('--repo', default=os.getcwd(), help=MSG['h_repo'])
    a = ap.parse_args()
    global FULL
    FULL = a.full
    sys.stdout.reconfigure(encoding='utf-8')
    if a.out:
        sys.stdout = open(a.out, 'w', encoding='utf-8')
    if not a.tool:
        if not a.session or a.list:
            ap.error(MSG['h_tool'])
        a.tool = next((k for repo in (a.repo, None) for k, (f, _, _) in READERS.items()
                       if any(match(s, a.session) for s in f(repo))), None)
        if not a.tool:
            sys.exit(MSG['not_found'].format(s=a.session))

    find, read, first = READERS[a.tool]
    found = find(a.repo)
    if a.session and not any(match(s, a.session) for s in found):
        # basta con el id: un chat abierto sin carpeta (su cwd es el de la herramienta) no sale en la lista del repo
        found = find(None)
    if a.session and not any(match(s, a.session) for s in found):
        # el encargo dijo otra herramienta (copilot para una sesión de copilot-cli): busca en las demás
        other = next((k for k, (f, _, _) in READERS.items() if k != a.tool
                      for repo in (a.repo, None) if any(match(s, a.session) for s in f(repo))), None)
        if other:
            print(MSG['other_tool'].format(tool=a.tool, other=other))
            a.tool = other
            find, read, first = READERS[other]
            found = find(a.repo)
            found = found if any(match(s, a.session) for s in found) else find(None)
    if not found:
        sys.exit(MSG['no_sessions'].format(tool=a.tool, repo=a.repo))
    if a.list:
        # las sesiones con actividad desde --since (su última actividad); sin él, las 10 más recientes
        since = parse_when(a.since, datetime.now().date())
        rows = sorted(((last_activity(s), s) for s in found), key=lambda r: r[0], reverse=True)
        for t, s in [r for r in rows if r[0] >= since] if since else rows[:10]:
            sub = f' {MSG["sub"]}' if is_subagent(s) else ''
            print(f'{t:%Y-%m-%d %H:%M}  {name(s)}{sub}  {cut(first(s), 100)}')
        return
    if a.session:
        found = [s for s in found if match(s, a.session)]
        if not found:
            sys.exit(MSG['not_found'].format(s=a.session))
    else:
        found = [s for s in found if not is_subagent(s)] or found

    tl = Timeline()
    read(found[0], tl)
    times = [e['t'] for e in tl.events if e['t']]
    last_day = max(times).date() if times else datetime.now().date()
    since, until = parse_when(a.since, last_day), parse_when(a.until, last_day, end=True)
    tl.window(since, until)
    print(MSG['session'].format(s=name(found[0]), tool=a.tool))
    print('\n'.join(render(tl, a.summary)))
    print('\n'.join(harness_use(tl, a.since, a.until)))


if __name__ == '__main__':
    main()
