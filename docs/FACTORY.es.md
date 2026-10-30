# Fábrica: entrada de tickets desatendida (opcional)

🌐 [English](FACTORY.md) · **Español**

Por defecto, cada sesión la llevas tú: la abres, hablas con el agente y apruebas al final (**manual**). Con `factory\intake.py`, los tickets nuevos abren su propia sesión, sin ventana y en su rama, y te esperan en una bandeja. Ese es el paso de harness a *software factory*: el harness es el mismo; lo que cambia es quién arranca el trabajo.

## 1. Cuándo compensa

- **Tickets claros y pequeños:** un texto, una traducción, un ajuste de estilo, un bug con pasos para reproducirlo. Una etiqueta decide cuáles entran: la pones tú, así que nada entra por sorpresa.
- **Un proyecto que se pueda comprobar sin que nadie mire:** tests, o al menos el sensor y el revisor. Si la comprobación es sobre todo visual, para antes del código (§2) y deja la parte de programar para tu sesión.
- **No compensa** con tickets ambiguos (`prepare` necesita preguntarte) ni con cambios en la base de datos, en código compartido o en permisos: esos, a mano.

## 2. Dónde se para

| `--stop` | Qué hace la sesión | Qué te llega |
|---|---|---|
| `before-code` (por defecto) | lee el ticket, busca la causa o los ficheros implicados (`diagnose`) y escribe las preguntas que haría `prepare` | un informe para empezar tu sesión a mitad de camino; ningún diff que revisar |
| `after-review` | lo programa y cierra como dice `closing.md`: revisor, arreglos, tabla de hallazgos y mensaje de commit | la rama `ia/<id>` lista para que la revises, la pruebes y hagas commit |

Si la herramienta deja renombrar, una sesión `before-code` deja ⚪ en su título (analizada y a la espera de empezar), y una que se atasca deja 🔴 (los estados, en `closing.md` §6). En los dos casos nunca hace commit ni push, y no pregunta: las preguntas van al informe. La del repaso también espera: el informe acaba con "Repaso: pendiente", y el agente te la hace cuando apruebas esa rama.

## 3. Montarlo

1. **De dónde salen los tickets:** rellena `fetch_tickets()` en `factory\intake.py`. El ejemplo lee issues de GitHub con `gh`; para otro gestor (Jira, Mantis…), su API o su exportación, devolviendo `id`, `title` y `body`. Y `LABEL`, la etiqueta que deja entrar un ticket.
2. **La herramienta:** `--tool copilot` (por defecto), `claude` u `opencode`. Sin ventana no puede pedir permiso: `TOOLS` se lo da de antemano, menos `git push`, `commit`, `branch` y `checkout`. Repasa esa lista para tu proyecto. El guard (hooks) sigue bloqueando credenciales, y deja lanzar el revisor sin un "cerramos" gracias a `HARNESS_UNATTENDED=1`, que solo pone el script.
3. **Pruébalo a mano** desde el repo: `py -3 <HARNESS>\factory\intake.py --dry-run` (dice lo que cogería), y luego sin `--dry-run` con un solo ticket (`--max 1`).
4. **Prográmalo,** cada 15 minutos por ejemplo:
   - Windows: `schtasks /Create /SC MINUTE /MO 15 /TN harness-intake /TR "py -3 <HARNESS>\factory\intake.py --repo <repo>"`
   - Linux / macOS (cron): `*/15 * * * * cd <repo> && python3 <HARNESS>/factory/intake.py`

## 4. La bandeja, en el día a día

- **Lo que espera:** `factory\reports\<id>.md` (el informe), `<id>.log` (lo que sacó la herramienta) y `factory\state.json` (la rama, la carpeta y la salida de cada ticket). Un ticket que ya está ahí no se vuelve a coger.
- **Retomar uno:** abre el worktree (`<repo>-ia-<id>`, al lado del repo) en tu editor, lee el informe y sigue en una sesión normal, o revisa el diff y haz commit si está terminado.
- **Limpiar:** `git worktree remove <carpeta>` y `git branch -d ia/<id>` cuando lo hayas integrado o descartado.

## 5. Riesgos

- **Permisos:** una sesión desatendida hace lo que sus permisos le dejan. Mantén `TOOLS` ajustado y el guard enganchado en la herramienta que uses.
- **Lo compartido:** todos los worktrees usan la misma base de datos de desarrollo y los mismos puertos que tú. La regla del router sigue valiendo (no escribir en la BD sin permiso), pero no hay nadie que lo dé: la sesión tiene que parar.
- **Coste:** cada ticket es una sesión completa. `--max` limita cuántos por pasada (3 por defecto).
