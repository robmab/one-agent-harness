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
"""
import json
import os
import re
import sys

URL_CON_CLAVE = re.compile(r'\b[a-z][a-z0-9+.-]*://[^\s:/@"\'`]+:(?!\*+@|<[^>]*>@|\{[^}]*\}@|\$\w+@)[^\s@"\'`/]+@')
AVISO = ('guard: bloqueado, lleva una URL con usuario y contraseña. Lee la conexión de la configuración del '
         'proyecto sin imprimirla (como mucho el nombre de la BD). Si de verdad hace falta, pide que lo haga el usuario.')
# lo que dice el usuario al cerrar: "cierro", "terminamos" (también "temrinamos"), "acabamos", "commit", "PR", "revísalo"
CIERRE = re.compile(r'cierr|cerra|termin|temrin|acab|commit|\bpr\b|pull request|revis|reviewer', re.I)
SIN_ADJUNTOS = re.compile(r'<(?:system[-_])?reminder>|<current_datetime>')
AVISO_CIERRE = ('guard: bloqueado, {que} sin que el usuario haya cerrado la sesión. El revisor y la pregunta del '
                'repaso van solo al cierre, cuando él lo diga (o lo pida antes de un commit o PR). Sigue con lo tuyo.')


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
    sale = [t.get(k) for k in ('command', 'content', 'new_string', 'new_str', 'file_text') if isinstance(t.get(k), str)]
    sale += [e.get('new_string', '') for e in t.get('edits') or [] if isinstance(e, dict)]
    return sale


def blocked(entrada):
    return any(URL_CON_CLAVE.search(t) for t in texts(entrada))


def tool(entrada):
    return entrada.get('tool_name') or entrada.get('toolName') or ''


def is_reviewer(entrada):
    t = args(entrada)
    return tool(entrada) in ('Agent', 'Task', 'task') and 'reviewer' in (t.get('subagent_type') or t.get('agent_type') or '')


def is_retro_question(entrada):
    return (tool(entrada) in ('AskUserQuestion', 'ask_user')
            and bool(re.search(r'repaso|\bretro\b', json.dumps(args(entrada), ensure_ascii=False), re.I)))


def users_last(entrada):
    """Sus 3 últimos mensajes y lo que contestó con la herramienta de preguntas; None si no hay log."""
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
    pronto = too_early(entrada)
    aviso = AVISO if blocked(entrada) else AVISO_CIERRE.format(que=pronto) if pronto else None
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
    ]
    fallos = [f'caso {i}: esperaba {"bloqueo" if espera else "paso"}' for i, (e, espera) in enumerate(casos, 1)
              if blocked(e) != espera]
    # el cierre: (herramienta, lo último del usuario, ¿bloquea?)
    revisor = {'tool_name': 'Agent', 'tool_input': {'subagent_type': 'reviewer', 'prompt': 'Alcance: …'}}
    repaso = {'tool_name': 'AskUserQuestion', 'tool_input': {'questions': [{'question': '¿Quieres el repaso del harness?'}]}}
    cierre = [
        (revisor, 'y el icono lo quitamos', True),
        (revisor, 'temrinamos sesion', False),
        (repaso, 'ponle más ancho al cliente', True),
        (repaso, 'vale, cerramos', False),
        (revisor, None, False),   # sin log, deja pasar
        ({'tool_name': 'Agent', 'tool_input': {'subagent_type': 'general-purpose'}}, 'hola', False),
    ]
    fallos += [f'cierre {i}: esperaba {"bloqueo" if espera else "paso"}' for i, (e, ultimo, espera) in enumerate(cierre, 1)
               if bool(too_early(e, ultimo)) != espera]
    os.environ['HARNESS_UNATTENDED'] = '1'   # una sesión de la fábrica: el revisor pasa sin un "cerramos"
    fallos += [] if too_early(revisor, 'y el icono lo quitamos') is None else ['desatendida: esperaba paso']
    del os.environ['HARNESS_UNATTENDED']
    print('\n'.join(fallos) if fallos else f'autoprueba OK: {len(casos) + len(cierre) + 1} casos')
    return 1 if fallos else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    sys.exit(selftest() if '--test' in sys.argv else hook_mode())
