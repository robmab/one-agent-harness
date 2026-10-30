"""Guarda de credenciales y del cierre para Claude Code (hook PreToolUse): bloquea antes de que pase.

Uso:
    py -3 guard.py --hook     # lo lanza el hook: lee el JSON de la herramienta por stdin
    py -3 guard.py --test     # autoprueba

Bloquea una URL con usuario:contraseña@ en las órdenes de terminal y en lo que se escribe en ficheros (los
huecos <x>, ***, {x} y $X valen). En sesiones reales lo hicieron las tres herramientas al probar contra una
base de datos, con la regla escrita en un .md: mejor una comprobación que una frase. El resto de herramientas
no tiene hook; ahí lo cubren el router y el sensor.

Y lanzar el revisor, o preguntar por el repaso, antes de que el usuario haya cerrado: mira sus 3 últimos
mensajes (y lo que contestó con la herramienta de preguntas) en el log de la sesión; si no lo encuentra, deja
pasar. Con solo el último mensaje bloqueaba la pregunta del repaso cuando el usuario, ya cerrado, preguntaba
otra cosa antes. En sesiones reales el agente lo lanzaba al acabar cada tarea, con la regla en el router. También lee lo
que manda Copilot CLI (toolName, toolArgs, sessionId), si lo enganchas ahí.
Con HARNESS_UNATTENDED=1 (lo pone factory/intake.py) no mira el cierre: no hay usuario que diga "cerramos",
y el encargo ya dice cuándo cerrar. Las credenciales se siguen bloqueando.
También un comando que imprime la contraseña o la compara con un texto (print(url.password), print(pwd == "…")):
en una sesión real, un script que leía la conexión la dejó así en el log.
Y escribir, con las herramientas de ficheros, en una ruta de FORBIDDEN_PATHS (vacía de serie): lo que no tiene
vuelta atrás, como la doc de un equipo fuera de git. En una sesión real el agente editó una por error.
"""
import json
import os
import re
import sqlite3
import sys

URL_CON_CLAVE = re.compile(r'\b[a-z][a-z0-9+.-]*://[^\s:/@"\'`]+:(?!\*+@|<[^>]*>@|\{[^}]*\}@|\$\w+@)[^\s@"\'`/]+@')
AVISO = ('guard: bloqueado, lleva una URL con usuario y contraseña, o imprime la contraseña. Lee la conexión de la configuración del '
         'proyecto sin imprimirla (como mucho el nombre de la BD). Si de verdad hace falta, pide que lo haga el usuario.')
PASSWORD_PRINTED = re.compile(r'print\([^\n]*(?:\.password\b|\b(?:pwd|passw\w*|clave|contrase\w*)\b)|\b(?:pwd|passw\w*|clave|contrase\w*)\b\s*[!=]=', re.I)
# lo que dice el usuario al cerrar: "cierro", "terminamos" (también "temrinamos"), "acabamos", "commit", "PR", "revísalo"
CIERRE = re.compile(r'cierr|cerra|\btermin(?!al)|temrin|acab|commit|\bpr\b|pull request|revis|reviewer', re.I)
SIN_ADJUNTOS = re.compile(r'<(?:system[-_])?reminder>|<current_datetime>')
AVISO_CIERRE = ('guard: bloqueado, {que} sin que el usuario haya cerrado la sesión. El revisor y la pregunta del '
                'repaso van solo al cierre, cuando él lo diga (o lo pida antes de un commit o PR). Sigue con lo tuyo.')
# TUNE: rutas en las que no se escribe nunca (con / y en minúsculas), p. ej. '/docs/equipo/'; vacía = apagado
FORBIDDEN_PATHS = ()
AVISO_RUTA = ('guard: bloqueado, escribir en {que}: esa carpeta no se toca (FORBIDDEN_PATHS). Si hace falta un '
              'cambio, díselo al usuario.')


def args(entrada):
    """Los argumentos de la herramienta, de Claude (tool_input) o de Copilot CLI (toolArgs, a veces como texto JSON)."""
    t = entrada.get('tool_input') or entrada.get('toolArgs') or {}
    if isinstance(t, str):
        try:
            t = json.loads(t)
        except ValueError:
            t = {'command': t}
    return t if isinstance(t, dict) else {}


def texts(entrada):
    """Lo que la herramienta va a ejecutar o escribir."""
    t = args(entrada)
    sale = [t.get(k) for k in ('command', 'content', 'new_string', 'new_str', 'newString', 'file_text') if isinstance(t.get(k), str)]
    sale += [e.get('new_string', '') for e in t.get('edits') or [] if isinstance(e, dict)]
    return sale


def blocked(entrada):
    orden = args(entrada).get('command')
    return (any(URL_CON_CLAVE.search(t) for t in texts(entrada))
            or isinstance(orden, str) and bool(PASSWORD_PRINTED.search(orden)))


def tool(entrada):
    return entrada.get('tool_name') or entrada.get('toolName') or ''


def is_reviewer(entrada):
    t = args(entrada)
    tipo = t.get('subagent_type') or t.get('agent_type') or t.get('agent') or ''   # agent: el subagent de OpenCode
    return tool(entrada) in ('Agent', 'Task', 'task', 'subagent') and 'reviewer' in tipo


def is_retro_question(entrada):
    return (tool(entrada) in ('AskUserQuestion', 'ask_user', 'question')
            and bool(re.search(r'repaso|\bretro\b', json.dumps(args(entrada), ensure_ascii=False), re.I)))


def opencode_messages(sid):
    """Los mensajes del usuario en una sesión de OpenCode (su base de datos), con lo que contestó a sus preguntas."""
    db = os.path.expanduser('~/.local/share/opencode/opencode.db')
    if not os.path.exists(db):
        return []
    con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    try:
        filas = con.execute('select type, data from session_message where session_id = ? order by seq', (sid,)).fetchall()
    except sqlite3.Error:
        return []
    finally:
        con.close()
    mensajes = []
    for tipo, data in filas:
        d = json.loads(data)
        if tipo == 'user':
            mensajes.append(d.get('text') or '')
        elif tipo == 'assistant' and mensajes:
            for c in d.get('content') or []:
                if isinstance(c, dict) and c.get('type') == 'tool' and c.get('name') == 'question':
                    st = c.get('state') or {}   # el resultado, en output o (las versiones nuevas) en partes de content
                    mensajes[-1] += '\n' + (st.get('output') or ' '.join(
                        p.get('text', '') for p in st.get('content') or [] if isinstance(p, dict)))
    return mensajes


def users_last(entrada):
    """Sus 3 últimos mensajes y lo que contestó con la herramienta de preguntas; None si no hay log."""
    if entrada.get('opencode_session'):   # lo manda el plugin guard.ts
        mensajes = opencode_messages(entrada['opencode_session'])
        return '\n'.join(SIN_ADJUNTOS.split(m)[0] for m in mensajes[-3:]) if mensajes else None
    sid = entrada.get('sessionId')
    ruta = entrada.get('transcript_path') or (sid and os.path.expanduser(f'~/.copilot/session-state/{sid}/events.jsonl'))
    if not ruta or not os.path.exists(ruta):
        return None
    mensajes, preguntas = [], set()
    with open(ruta, encoding='utf-8', errors='replace') as f:
        for linea in f:
            try:
                e = json.loads(linea)
            except ValueError:
                continue
            d = e.get('data') or {}
            if e.get('type') == 'user' and not e.get('isSidechain'):   # Claude: texto suyo, o respuestas a preguntas
                c = (e.get('message') or {}).get('content')
                if isinstance(c, str):
                    mensajes.append(c)
                elif isinstance(c, list) and any(p.get('type') == 'text' for p in c if isinstance(p, dict)):
                    mensajes.append(' '.join(p.get('text', '') for p in c if isinstance(p, dict) and p.get('type') == 'text'))
                elif isinstance(e.get('toolUseResult'), dict) and 'answers' in e['toolUseResult'] and mensajes:
                    mensajes[-1] += '\n' + json.dumps(e['toolUseResult']['answers'], ensure_ascii=False)
            elif e.get('type') == 'user.message' and not d.get('source'):   # Copilot CLI; con source, un encargo a un subagente
                mensajes.append(d.get('content') or '')
            elif e.get('type') == 'tool.execution_start' and d.get('toolName') == 'ask_user':
                preguntas.add(d.get('toolCallId'))
            elif e.get('type') == 'tool.execution_complete' and d.get('toolCallId') in preguntas and mensajes:
                mensajes[-1] += '\n' + str((d.get('result') or {}).get('content', ''))
    # sin los adjuntos que la herramienta pega detrás (<reminder>…): ahí cualquier palabra haría de "cierre"
    return '\n'.join(SIN_ADJUNTOS.split(m)[0] for m in mensajes[-3:]) if mensajes else None


def forbidden_path(entrada, rutas=None):
    """El fichero, si se va a escribir en una ruta prohibida."""
    t = args(entrada)
    ruta = t.get('file_path') or t.get('path') or t.get('filePath') or ''
    if not isinstance(ruta, str) or 'command' in t or not texts(entrada):
        return None
    ruta = '/' + ruta.replace('\\', '/').lower()
    return ruta.rsplit('/', 1)[-1] if any(r in ruta for r in (FORBIDDEN_PATHS if rutas is None else rutas)) else None


def too_early(entrada, ultimo=None):
    que = 'lanzar el revisor' if is_reviewer(entrada) else 'preguntar por el repaso' if is_retro_question(entrada) else None
    if not que or os.environ.get('HARNESS_UNATTENDED') == '1':   # una sesión de la fábrica: el encargo dice cuándo cerrar
        return None
    ultimo = users_last(entrada) if ultimo is None else ultimo
    return None if ultimo is None or CIERRE.search(ultimo) else que


def hook_mode():
    try:
        entrada = json.load(sys.stdin)
    except ValueError:
        return 0
    pronto, ruta = too_early(entrada), forbidden_path(entrada)
    aviso = (AVISO if blocked(entrada) else AVISO_CIERRE.format(que=pronto) if pronto else
             AVISO_RUTA.format(que=ruta) if ruta else None)
    if aviso:
        print(aviso, file=sys.stderr)
        # 2 bloquea en las dos: Claude le pasa al modelo el stderr; Copilot CLI, el permissionDecisionReason
        print(json.dumps({'permissionDecision': 'deny', 'permissionDecisionReason': aviso}, ensure_ascii=False))
        return 2
    return 0


def selftest():
    clave = 'se' + 'creto'   # montada al vuelo: este fichero no lleva ninguna credencial escrita
    url = 'postgresql://app:' + clave + '@localhost:5432/bd'
    casos = [
        ({'tool_input': {'command': f'psql "{url}"'}}, True),
        ({'tool_input': {'content': f"DSN = '{url}'\n"}}, True),
        ({'tool_input': {'edits': [{'new_string': f'x = "{url}"'}]}}, True),
        ({'tool_input': {'content': 'url = "postgresql://<usuario>:<clave>@host/bd"'}}, False),
        ({'tool_input': {'content': 'url = "postgresql://app:***@host/bd"'}}, False),
        ({'tool_input': {'command': 'git log --oneline -5'}}, False),
        ({'tool_input': {'command': "usuario, pwd = m.groups()\nprint('ok:', pwd == 'x')"}}, True),
        ({'tool_input': {'command': 'print(make_url(url).password)'}}, True),
        ({'tool_input': {'command': 'print(make_url(url).database)'}}, False),
    ]
    fallos = [f'caso {i}: esperaba {"bloqueo" if espera else "paso"}' for i, (e, espera) in enumerate(casos, 1)
              if blocked(e) != espera]
    # el cierre: (herramienta, lo último del usuario, ¿bloquea?)
    revisor = {'tool_name': 'Agent', 'tool_input': {'subagent_type': 'reviewer', 'prompt': 'Alcance: …'}}
    repaso = {'tool_name': 'AskUserQuestion', 'tool_input': {'questions': [{'question': '¿Quieres el repaso del harness?'}]}}
    cierre = [
        (revisor, 'y el icono lo quitamos', True),
        (revisor, 'temrinamos sesion', False),
        (revisor, 'lanza esto en la terminal', True),   # "terminal" no es cerrar
        (repaso, 'ponle más ancho al cliente', True),
        (repaso, 'vale, cerramos', False),
        (revisor, None, False),   # sin log, deja pasar
        ({'tool_name': 'subagent', 'tool_input': {'agent': 'reviewer'}}, 'y el icono lo quitamos', True),   # OpenCode
        ({'tool_name': 'Agent', 'tool_input': {'subagent_type': 'general-purpose'}}, 'hola', False),
    ]
    fallos += [f'cierre {i}: esperaba {"bloqueo" if espera else "paso"}' for i, (e, ultimo, espera) in enumerate(cierre, 1)
               if bool(too_early(e, ultimo)) != espera]
    os.environ['HARNESS_UNATTENDED'] = '1'   # una sesión de la fábrica: el revisor pasa sin un "cerramos"
    fallos += [] if too_early(revisor, 'y el icono lo quitamos') is None else ['desatendida: esperaba paso']
    del os.environ['HARNESS_UNATTENDED']
    # rutas prohibidas, con una puesta solo para la prueba: (herramienta, ¿bloquea?)
    rutas = [
        ({'tool_name': 'Edit', 'tool_input': {'file_path': r'C:\x\docs\equipo\a.md', 'new_string': 'y'}}, True),
        ({'tool_name': 'Read', 'tool_input': {'file_path': r'C:\x\docs\equipo\a.md'}}, False),
        ({'tool_name': 'Edit', 'tool_input': {'file_path': r'C:\x\docs\otra\a.md', 'new_string': 'y'}}, False),
    ]
    fallos += [f'ruta {i}: esperaba {"bloqueo" if espera else "paso"}' for i, (e, espera) in enumerate(rutas, 1)
               if bool(forbidden_path(e, ('/docs/equipo/',))) != espera]
    print('\n'.join(fallos) if fallos else f'autoprueba OK: {len(casos) + len(cierre) + len(rutas) + 1} casos')
    return 1 if fallos else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    sys.exit(selftest() if '--test' in sys.argv else hook_mode())
