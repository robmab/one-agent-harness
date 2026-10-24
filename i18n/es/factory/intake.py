"""Entrada de la fábrica (OPCIONAL): convierte los tickets nuevos en sesiones desatendidas, cada una en su rama.

Sin ella no cambia nada: abres cada sesión a mano (manual, lo de por defecto). Con ella, cada pocos minutos
(Programador de tareas o cron, mira docs/FACTORY.es.md) coge los tickets nuevos con LABEL, le da a cada uno un
worktree con su rama ia/<id> y lanza ahí tu herramienta sin ventana, con el harness entero. Dónde se para:
- before-code: el diagnóstico y las preguntas que haría prepare, sin tocar código (lo de por defecto);
- after-review: programa, pasa el revisor y arregla, y deja la rama para que la apruebes tú.
Cada sesión deja su informe en factory/reports/<id>.md. El commit, como siempre, es tuyo.

Uso (desde el repo):
    py -3 <HARNESS>/factory/intake.py [--stop before-code|after-review] [--tool copilot|claude|opencode]
                                      [--max 3] [--dry-run]
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPORTS = os.path.join(HERE, 'reports')
STATE = os.path.join(HERE, 'state.json')
# FILL-IN: la etiqueta que deja entrar un ticket. Eliges tú cuáles: claros y pequeños
LABEL = 'ia'
# La herramienta sin ventana. No puede pedir permiso, así que lo lleva de antemano, menos lo que solo hace el usuario.
# El guard (hooks) sigue bloqueando credenciales. Claude: añade --allowedTools con las órdenes que pidan tus pruebas.
TOOLS = {
    'copilot': ['copilot', '-p', '{prompt}', '--allow-all-tools', '--deny-tool', 'shell(git push)',
                '--deny-tool', 'shell(git commit)', '--deny-tool', 'shell(git branch)', '--deny-tool', 'shell(git checkout)'],
    'claude': ['claude', '-p', '{prompt}', '--permission-mode', 'acceptEdits'],
    'opencode': ['opencode', 'run', '{prompt}'],
}
STOPS = {
    'before-code': ('Para ANTES de escribir código. Busca la causa o los ficheros implicados (diagnose) y las preguntas '
                    'que haría prepare: el informe es la entrega.'),
    'after-review': ('Prográmalo y luego cierra como dice closing.md: revisor, arreglos, la tabla de hallazgos y el '
                     'mensaje de commit. Sáltate la pregunta del repaso: acaba el informe con "Repaso: pendiente, '
                     'pregúntalo cuando el usuario apruebe esta rama".'),
}
TASK = """# Ticket {id}: {title}

{body}

---
Sesión desatendida de la fábrica (factory/intake.py): nadie está leyendo. No uses herramientas de preguntas: si
preguntarías, escribe la pregunta en el informe y sigue con tu mejor suposición, marcada como tal (o para, si bloquea).
{stop}
Al acabar, escribe el informe en {report}: qué has hecho, qué has comprobado y qué no, las preguntas abiertas,
la herramienta y el id de la sesión. Nunca hagas commit ni push ni toques otras ramas: aprueba el usuario.
"""


def fetch_tickets():
    """FILL-IN: los tickets abiertos con LABEL, como [{'id', 'title', 'body'}]. El ejemplo: issues de GitHub, con gh."""
    out = subprocess.run(['gh', 'issue', 'list', '--label', LABEL, '--state', 'open', '--json', 'number,title,body'],
                         capture_output=True, text=True, encoding='utf-8', check=True).stdout
    return [{'id': str(i['number']), 'title': i['title'], 'body': i.get('body') or ''} for i in json.loads(out)]


def load_state():
    if not os.path.isfile(STATE):
        return {}
    with open(STATE, encoding='utf-8') as f:
        return json.load(f)


def save_state(state):
    with open(STATE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def worktree(repo, tid):
    """Una copia del repo en su propia rama, al lado: la sesión nunca toca tu checkout."""
    path = os.path.join(os.path.dirname(repo), f'{os.path.basename(repo)}-ia-{tid}')
    subprocess.run(['git', '-C', repo, 'worktree', 'add', '-b', f'ia/{tid}', path],
                   capture_output=True, text=True, check=True)
    return path


def run(tool, task_path, cwd, log_path):
    """El prompt solo apunta al fichero del encargo: un texto largo con saltos de línea lo destrozan los .cmd."""
    prompt = f'Tu encargo está en {task_path}: léelo y síguelo.'
    cmd = [a.replace('{prompt}', prompt) for a in TOOLS[tool]]
    cmd[0] = shutil.which(cmd[0]) or cmd[0]
    env = dict(os.environ, HARNESS_UNATTENDED='1')   # el guard deja lanzar el revisor sin un "cerramos"
    with open(log_path, 'w', encoding='utf-8') as log:
        return subprocess.run(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT).returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--repo', default=os.getcwd())
    ap.add_argument('--stop', choices=sorted(STOPS), default='before-code')
    ap.add_argument('--tool', choices=sorted(TOOLS), default='copilot')
    ap.add_argument('--max', type=int, default=3, help='tickets por pasada, uno detrás de otro (por defecto 3)')
    ap.add_argument('--dry-run', action='store_true', help='dice lo que cogería y no toca nada')
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    repo, state = os.path.abspath(a.repo), load_state()
    new = [t for t in fetch_tickets() if t['id'] not in state][:a.max]
    if not new:
        print('No hay tickets nuevos.')
        return 0
    os.makedirs(REPORTS, exist_ok=True)
    for t in new:
        if a.dry_run:
            print(f'cogería el #{t["id"]}: {t["title"]}')
            continue
        report = os.path.join(REPORTS, f'{t["id"]}.md')
        task_path = os.path.join(REPORTS, f'{t["id"]}.task.md')
        with open(task_path, 'w', encoding='utf-8') as f:
            f.write(TASK.format(id=t['id'], title=t['title'], body=t['body'], stop=STOPS[a.stop], report=report))
        try:
            cwd = worktree(repo, t['id'])
        except subprocess.CalledProcessError as e:   # la rama ya existe, o no es un repo: se salta
            print(f'#{t["id"]}: sin worktree ({e.stderr.strip()})')
            continue
        code = run(a.tool, task_path, cwd, os.path.join(REPORTS, f'{t["id"]}.log'))
        if not os.path.isfile(report):
            with open(report, 'w', encoding='utf-8') as f:
                f.write(f'# Ticket {t["id"]}\n\nLa sesión no dejó informe (salida {code}): mira {t["id"]}.log\n')
        state[t['id']] = {'date': datetime.date.today().isoformat(), 'stop': a.stop, 'tool': a.tool,
                          'branch': f'ia/{t["id"]}', 'worktree': cwd, 'exit': code}
        save_state(state)
        print(f'#{t["id"]} -> {report}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
