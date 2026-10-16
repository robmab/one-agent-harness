# Día a día

🌐 [English](DAY-TO-DAY.md) · **Español**

Añadir piezas, qué va en cada fichero de instrucciones, cómo escribir una skill que funcione y los gotchas aprendidos a palos.

## 1. Añadir piezas

- **Skill nueva:** `personal\skills\<nombre>\SKILL.md`. La ven todos los usuarios y las herramientas sin más; **en OpenCode, añádela también a la lista blanca** de `opencode\opencode.jsonc`.
- **Agente nuevo: en principio, no.** El harness tiene **un solo agente**, el `reviewer`. Un "revisor de X" se hace como skill con su checklist y se añade a la tabla de checklists del `reviewer` (ver [SKILLS-GUIDE [gotchas](#4-gotchas-aprendidos-a-palos)](SKILLS-GUIDE.es.md#6-antes-de-añadir-algo-nuevo)). Solo compensa otro agente si hacen falta ojos frescos, permisos distintos o aislar un trabajo pesado que no cubra nada más. Si llega el caso: `personal\agents\<nombre>.agent.md` con frontmatter **de Claude** (`name`, `description`, `tools: Read, Grep…`); Copilot lo detecta igual (probado). Para OpenCode, después `py -3 <HARNESS>\opencode\sync.py`.
- **Revisión desde la CLI de OpenCode:** desde el repo, `& <HARNESS>\opencode\scripts\review-pending.ps1` lanza el `reviewer` sobre lo pendiente sin commitear (o `-Branch main` para la rama) y deja el informe con fecha en `opencode\reports\`. Sin código cambiado, sale sin despertar al modelo. Sirve a mano, con un alias, programado o en un hook `pre-push` local. En modo script lo que está en `ask` se rechaza: el informe lo dice.
- **Antes de añadir nada, pasa el filtro** de la [SKILLS-GUIDE [gotchas](#4-gotchas-aprendidos-a-palos)](SKILLS-GUIDE.es.md#6-antes-de-añadir-algo-nuevo):
  - conocimiento que el modelo no puede saber,
  - o un fallo visto que se repite.

  Si se puede comprobar con una regex, mejor una regla nueva en `RULES` que una skill. **Antes de darla por buena, pásala por todo el repo (`--all`) y por las líneas añadidas en el historial**: una regla con falsos positivos bloquea al agente o acaba ignorada.
- **Checklist nueva para el revisor** (algo que solo sirve para revisar) → `personal\checklists\<nombre>.md` y una fila en la tabla de fuentes del `reviewer`, con sus ejes.

## 2. Qué va en cada fichero de instrucciones

Cada fichero tiene un papel; si se repite algo entre ellos, se gasta contexto en cada sesión y acaban contradiciéndose.

| Fichero | Quién lo lee | Qué va | Qué NO va |
|---|---|---|---|
| `AGENTS.md` (raíz del repo) | Claude y Copilot, siempre | el índice del repo: qué es, comandos que no se pueden adivinar, qué skill o agente usar para qué. Corto: cada línea, por un fallo real | lo personal, el detalle de las skills, el orden de trabajo |
| `claude\CLAUDE.md` (harness) | Claude, siempre (hook `SessionStart`) | el **router**: el orden de trabajo (entender → hacer → comprobar → revisar), el papel del sensor y del agente. Corto y condicionado a "si estás en el repo de X" | el *cuándo* de cada skill (ya está en su `description`); nada de lo que dice `AGENTS.md` |
| `copilot\<project>.instructions.md` (harness) | Copilot y OpenCode, siempre: el chat de VS Code, Copilot CLI (hardlink en `~/.copilot`) y OpenCode (hardlink `~/.config/opencode/AGENTS.md`) | el mismo router, sin prefijos, con el sensor lanzado a mano y en formato de órdenes **ANTES / DESPUÉS** (con modelos pequeños, la diferencia entre cumplirlo o no) | lo mismo que en `CLAUDE.md` |
| `SKILL.md` de cada skill | el modelo, cuando la `description` encaja | el *qué* y el *cómo*; la `description`, el *cuándo* | reglas que valgan siempre (esas, a `AGENTS.md` o a los convenios) |

Reglas:
- **Ningún `CLAUDE.md` en el repo ni en una carpeta superior** (tampoco `~/.claude/CLAUDE.md` si el repo cuelga de tu home): Claude dejaría de cargar `AGENTS.md`. Por eso el router va por hook.
- **Si algo cambia de pieza** (nueva skill, otro agente), se actualizan el router de Claude y el de Copilot; `AGENTS.md`, solo si es del repo.
- **Si el modelo se salta una fase** en los logs, primero se mejora la `description` de la skill; si es el router, se reescribe esa orden en imperativo y atada al momento. El router solo crece con fallos vistos.

## 3. Escribir una skill que funcione

- **`name`** igual que la carpeta, en minúsculas, números y guiones, **sin `_`**: si no, falla en silencio.
- **Primero el concepto:** una línea `**CONCEPT:**` (o `**CONCEPTO:**`) que diga para qué sirve la skill y qué evita. El modelo sigue mejor una regla cuando sabe por qué.
- **La `description` es lo único que ve el modelo** hasta que decide cargarla. Tiene que decir **cuándo** usarla, no resumir lo que hace, y llevar **palabras concretas** de las peticiones reales ("componente", "slot", "query"…). Si es genérica, no se dispara.
- **Corta:** 600 palabras como mucho, con tablas antes que párrafos. Si necesita más, un índice y ficheros al lado que se lean bajo demanda.
- **Si es del proyecto**, la primera línea: "Si no estás en el repo de <PROJECT>, ignora esta skill". Las skills de Claude valen en todos los proyectos.
- **Que no escriba en el repo** (planes, intents, ficheros de trabajo) y que pida permiso para la BD.
- **Si es adaptada,** el crédito al pie, con el commit de origen ("Adaptada de X de [repo] @ `sha` (fecha) (MIT)"), y su aviso de copyright en `THIRD-PARTY-NOTICES.md`.
- **Revisar el upstream** (cada pocos meses): por cada skill adaptada, diff de su repo desde el commit del pie (`git diff <sha>..HEAD -- skills/<nombre>/`). Entra solo lo que pase el filtro de la SKILLS-GUIDE [gotchas](#4-gotchas-aprendidos-a-palos); si se aplica algo, se actualiza el commit del pie.
- **Probarla en las dos herramientas,** en sesión nueva y sin invocarla a mano: ¿entra sola cuando toca? Y comprobar el resultado, no solo que la cargue. Con modelos locales pequeños, contar con invocarla a mano (`/nombre`).

## 4. Gotchas (aprendidos a palos)

- **Ningún `CLAUDE.md` en una carpeta superior al repo,** incluido `~/.claude/CLAUDE.md` si el repo cuelga de tu home: Claude deja de cargar `AGENTS.md`. Por eso las instrucciones globales van por hook.
- **Nada en `~/.claude/skills`, `~/.claude/agents` ni `.claude/` del workspace** que ya llegue por otro sitio: VS Code lo lee y duplica. No hay ajuste para evitarlo.
- **`~/.claude/skills` no se enlaza entera:** Claude guarda ahí cosas suyas por usuario.
- **Marketplace:** `"strict": false` o `"version"` en la entrada de un plugin sin `plugin.json` rompió la carga de **todo** el marketplace, sin error visible.
- **Hook en forks:** al bifurcar o retomar una conversación, si el texto del hook ya está en el historial no se vuelve a inyectar. En sesiones nuevas entra siempre.
- **Borrar junctions sin cargarse el destino:** `(Get-Item ruta -Force).Delete()` o `rmdir ruta` (sin `/s`). Nunca `Remove-Item -Recurse` sobre una junction. Desde Git Bash, `rmdir` no la borra ("Not a directory": ve la junction como un symlink): usa `cmd //c rmdir "C:\ruta"`.
- **Hardlinks (router y config de OpenCode):** el original y los enlaces de cada usuario son el mismo fichero. Pero si un programa lo guarda *reemplazándolo* (borra y crea uno nuevo), el enlace se rompe sin avisar. Comprobación: `fsutil hardlink list <fichero>` lista todas las rutas; si falta alguna, `setup.py --check` la recupera (si el texto sigue siendo el mismo). **Les pasa también a los editores de los agentes.**
- **OpenCode ignora un agente entero, sin error, si su frontmatter lleva `tools: Read, Grep…`** (el formato de Claude y Copilot): por eso `opencode\agents\` es una copia generada.
- **OpenCode sube buscando skills hasta el home:** si el repo cuelga de tu usuario, se trae las de `~/.claude/skills` (por ejemplo, las que sincroniza la app de Claude) y engordan el prompt de cada turno. Lo para la lista blanca.
- **`opencode run` no puede aprobar permisos:** lo que esté en `ask` se rechaza. En Desktop o en la TUI te lo pregunta.
- **Copiar el harness:** las junctions pueden llegar como carpetas normales o rotas. `setup.py --check` te las señala.
- **Hooks dentro del plugin:** `hooks\hooks.json` en la raíz del plugin se carga solo, y `${CLAUDE_PLUGIN_ROOT}` se resuelve bien a través de la junction.
- **`py -3` y no `python`** (Windows; en Linux y macOS, `python3`): el lanzador está en `C:\Windows` y vale para todos los usuarios. Configura `PROJECT_PYTHON` para compilar con el Python del proyecto y no con el del sistema.
- **Detectar no es cargar:** en VS Code, que una skill exista no implica que el modelo la use; lo decide por la `description`, y los modelos locales fallan más. Se fuerza escribiendo `/nombre`.
- **Docs del equipo en una carpeta ignorada por git** (p. ej. `docs/` en el `.gitignore`): el buscador de Copilot no los ve y un grep ahí sale vacío. Busca con `includeIgnoredFiles: true` o léelos por ruta; si tus skills apuntan ahí, dilo en el router.
- **Rutas de Windows dentro de `sed` o `python -c`** en Git Bash: `\a`, `\r`… se interpretan como escapes y rompen el texto. Mejor un script aparte.
- **Repos de otro usuario de Windows:** git da *dubious ownership* → `git config --global --add safe.directory <ruta>`.
