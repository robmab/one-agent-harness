# One Agent Harness

🌐 [English](README.md) · **Español**

<p align="center"><img src="img/route.png" alt="Una llama escaladora (el modelo) sube por una pared con un arnés del que cuelgan seis piezas (las skills); un aparato autoblocante (el sensor) la sujeta y otra llama la asegura desde abajo (el agente). Un cartel dice AGENTS.md, empieza aquí. Los nombres de las versiones son los anclajes de la vía: Anchor, Belay, Carabiner, Descender y Hexcentric en la cima" width="100%"></p>

[![CI](https://github.com/robmab/one-agent-harness/actions/workflows/ci.yml/badge.svg)](https://github.com/robmab/one-agent-harness/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/robmab/one-agent-harness)](https://github.com/robmab/one-agent-harness/releases)
[![License: MIT](https://img.shields.io/github/license/robmab/one-agent-harness)](LICENSE)

Plantilla para montar el harness de IA de **cualquier proyecto**: skills, agentes, un sensor automático e instrucciones, compartidos entre todos los usuarios de Windows del PC y entre Claude Code, GitHub Copilot (VS Code) y OpenCode 2, **sin tocar el workspace** si no quieres.

## En uso real, a diario

No es una demo: es el harness que uso **cada día en mi trabajo**, sobre una aplicación web grande, en producción y mantenida por un equipo. La plantilla es ese mismo harness quitando todo lo específico del proyecto, y **evoluciona con él**: cuando algo estorba o falla en una sesión real, se arregla allí primero y luego se trae aquí.

- **Probado en sesiones de trabajo reales** con Claude Code, GitHub Copilot en VS Code (modelos en la nube) y OpenCode 2 con un modelo local (llama.cpp).
- **Cada regla sale de algo que pasó de verdad.** El revisor lee solo el diff porque leyendo ficheros enteros se hacía eterno; el sensor calla en las líneas que solo se han movido porque el ruido constante enseña a ignorarlo; el router dice quién hace el commit porque un modelo lo hizo por su cuenta.
- **Al día:** las mejoras salen como [releases](https://github.com/robmab/one-agent-harness/releases), con notas de lo aprendido.

> **Es inerte:** no la carga ninguna herramienta. No se usa aquí: se **copia** a `<ROOT>\<Project>`, se rellena y se conecta. Cada pieza pendiente está marcada con `FILL-IN`.

> **Idioma:** la plantilla (skills, agente, router y scripts) está **en inglés**, y `setup.py --lang es` la monta en español; la documentación, en inglés y en español (`*.es.md`). Escribe las skills, y sobre todo su `description`, **en el idioma en que hablas con el modelo**: el modelo compara lo que le pides con las descripciones, y unas instrucciones en tu idioma mantienen en él sus respuestas y sus comentarios. En otro idioma, tradúcelas al rellenarlas. *Hasta la v0.3.0 la plantilla estaba en español; las [notas de la v0.3.5](https://github.com/robmab/one-agent-harness/releases) traen los nombres antiguos.*

**Nombres que se usan en toda la plantilla:**

| Marcador | Qué es |
|---|---|
| `<ROOT>` | la carpeta donde guardas los harness. Mejor una que **lean y escriban todos los usuarios de Windows** del PC (p. ej. una carpeta dentro de `C:\Users\Public`) y que esté **fuera de los repos** |
| `<HARNESS>` | la carpeta del harness de un proyecto: `<ROOT>\<Project>` |
| `<PROJECT>` / `<project>` | el nombre del proyecto; en minúsculas y con guiones donde hace de identificador (plugin, marketplace) |

| Documento | Para qué |
|---|---|
| **README** (este) | qué trae, cómo montar un proyecto nuevo y cómo convivir con otros |
| [SKILLS-GUIDE](SKILLS-GUIDE.es.md) | qué hace cada pieza, de qué tipo es, en qué momento entra y qué hay que rellenar |
| [RESEARCH](RESEARCH.es.md) | de dónde sale todo: qué es un harness, repos analizados, skills adaptadas y descartadas |
| [OPTIONAL-SKILLS](OPTIONAL-SKILLS.es.md) | catálogo de skills opcionales: qué aporta cada una, cuándo meterla, qué ruido mete y cuáles se desaconsejan |
| [AGENTS.template.md](AGENTS.template.md) *(EN)* | el índice que va en la raíz del repo del proyecto |
| [LICENSE](LICENSE) · [THIRD-PARTY-NOTICES](THIRD-PARTY-NOTICES.md) | licencia MIT y créditos de las skills adaptadas (§9) |

![Qué llega a cada herramienta y por dónde](img/wiring.es.svg)

---

## 1. Estructura

```
one-agent-harness\
├─ README · SKILLS-GUIDE · RESEARCH · OPTIONAL-SKILLS   cada uno en inglés (.md) y en español (.es.md)
├─ LICENSE · THIRD-PARTY-NOTICES.md · .gitattributes
├─ .github\                              CI de este repo (no es de la plantilla; se quita al copiar)
├─ VERSION                               versión de la plantilla de la que sale este harness
├─ AGENTS.template.md                    → a la raíz del repo como AGENTS.md
├─ setup.py                              READY     lo monta en este PC: nombres, idioma y enlaces (§3.2)
├─ i18n\es\                              las piezas en español, para setup.py --lang es (se va al montar)
├─ img\                                  esquemas SVG y el banner (route.png)
├─ claude\                               ← lo que solo usa Claude
│  ├─ CLAUDE.md                          el router: orden de trabajo, sensor y agente (lo mete el hook SessionStart)
│  ├─ .claude-plugin\marketplace.json    marketplace "harness-project" con el plugin "project"
│  └─ plugins\project                    ⇒ JUNCTION a ..\..\personal (la crea setup.py)
├─ copilot\project.instructions.md       el router para Copilot y OpenCode: HARDLINK desde ~/.copilot y ~/.config/opencode (setup.py)
├─ copilot\agents\reviewer.agent.md      GENERADO  por sync.py con los alias de herramientas de VS Code (no editar aquí)
├─ opencode\                             ← lo que solo usa OpenCode (opcional)
│  ├─ opencode.jsonc                     FILL-IN   modelo y proveedor; permisos, lista blanca de skills, revisor
│  ├─ agents\reviewer.md                 GENERADO  por sync.py desde personal\agents (no editar aquí)
│  ├─ plugins\sensor.ts                  READY     pasa check.py tras cada edición (como el hook de Claude)
│  ├─ sync.py                            READY     regenera las copias de agentes de OpenCode y Copilot (--check: solo comprueba)
│  └─ scripts\review-pending.ps1         READY     el revisor desde la CLI; deja el informe en opencode\reports\
└─ personal\                             ← lo que leen Claude, Copilot y OpenCode
   ├─ skills\
   │  ├─ code-conventions\               FILL-IN   convenios del proyecto
   │  ├─ ui-design\                      FILL-IN   design system
   │  ├─ official-sources\               ADJUST    tabla del stack y trampas
   │  ├─ verify-before-done\             ADJUST    comandos de prueba
   │  ├─ systematic-debugging\           ADJUST    capas y trampas
   │  ├─ interview-me\                   READY
   │  └─ comment-style\                  OPTIONAL  tu voz (comentarios y chat); fuera del core
   ├─ agents\
   │  └─ reviewer.agent.md               READY     el único agente: revisión a fondo, convenios incluidos, no edita
   ├─ checklists\security.md             ADJUST    la lee solo el revisor (eje 3); fuera de cualquier catálogo
   ├─ scripts\check.py                   ADJUST    sensor: MARKER, PROJECT_PYTHON y RULES; solo líneas cambiadas
   └─ hooks\hooks.json                   READY     PostToolUse: pasa check.py tras cada edición
```

- **READY** (lista): vale tal cual.
- **ADJUST** (ajustar): el método vale; hay que rellenar sus tablas.
- **FILL-IN** (rellenar): plantilla vacía; el contenido es del proyecto.
- **OPTIONAL** (opcional): fuera del core; se queda o se quita según la persona.

El **core** son 6 skills + 1 sensor + 1 agente, sobre `AGENTS.md` (ver [SKILLS-GUIDE §2](SKILLS-GUIDE.es.md#2-qué-es-el-core)).

## 2. Cómo lo encuentra cada herramienta

| Herramienta | Qué lee | Por dónde |
|---|---|---|
| Claude Code | `AGENTS.md` del repo | lo carga solo al arrancar, **si no hay ningún `CLAUDE.md` en el repo ni en carpetas superiores** (§6) |
| Claude Code | plugin `project` (skills, agentes y hook) | marketplace local en `~/.claude/settings.json`; el plugin es la junction `claude\plugins\project` |
| Claude Code | `claude\CLAUDE.md` | hook `SessionStart` que hace `cat` del fichero |
| Copilot (VS Code) | `AGENTS.md` y `.github/` del repo, si los hay | el propio repo |
| Copilot (VS Code) | skills de `personal\`, agentes de `copilot\agents\` (copia generada) | junctions `~/.copilot/skills` y `~/.copilot/agents` |
| Copilot (VS Code y CLI) | el router `copilot\<project>.instructions.md` | hardlink en `~/.copilot/copilot-instructions.md`; se carga siempre |
| Copilot (VS Code) | `check.py` | no hay hook: se lo ordena el router ("DESPUÉS de cada cambio"), o lo lanzas tú |
| OpenCode 2 | `AGENTS.md` del repo y el router | el del repo, solo; el router, hardlink `~/.config/opencode/AGENTS.md` → `copilot\<project>.instructions.md`. **No lee `CLAUDE.md`** |
| OpenCode 2 | skills de `personal\` y del repo | junction `~/.config/opencode/skills`; las del repo, campo `skills` de la config. Filtradas por la lista blanca |
| OpenCode 2 | el `reviewer` | junction `~/.config/opencode/agents` → `opencode\agents` (copia generada) |
| OpenCode 2 | `check.py` tras cada edición | junction `~/.config/opencode/plugins` → `opencode\plugins\sensor.ts` |
| OpenCode 2 | modelo, permisos | hardlink `~/.config/opencode/opencode.jsonc` → `opencode\opencode.jsonc` |

**Por qué así:** VS Code Copilot también lee `~/.claude/skills`, `~/.claude/agents` y `.claude/` del workspace. Lo que pongas ahí lo ve dos veces si además está en `.github/` o en `~/.copilot`. Los **plugins** de Claude, en cambio, Copilot no los descubre, y Claude no lee `~/.copilot`. OpenCode, por su parte, sube desde el repo hasta el home buscando `.claude/skills`: de ahí la lista blanca de skills en su config. Resultado: cada herramienta ve cada cosa una sola vez.

## 3. Montar un proyecto nuevo

Requisitos: Claude Code (usa Git Bash para los hooks en Windows), VS Code con Copilot, OpenCode 2 si lo usas, y el lanzador `py` de Python. Nada necesita admin. **`setup.py` es solo para Windows, de momento:** en Linux o macOS, sigue el [montaje a mano](#anexo-montaje-a-mano) con symlinks y `python3`.

### 3.1 Copiar

```powershell
git clone <url-de-este-repo> '<HARNESS>'
Remove-Item '<HARNESS>\.git', '<HARNESS>\.github' -Recurse -Force
```

El `.git` se borra para que el harness del proyecto no quede atado a la plantilla, y `.github` porque solo tiene el CI de este repo. Más fácil todavía: descarga **Source code (zip)** de la [última release](https://github.com/robmab/one-agent-harness/releases/latest), que ya viene sin los dos. **No borres `VERSION`:** dice de qué versión de la plantilla sale el harness, y así más adelante puedes ver qué ha cambiado desde entonces (en las [releases](https://github.com/robmab/one-agent-harness/releases)). Si quieres versionarlo, haz después tu propio `git init`. Si ya tienes la plantilla en local, vale igual con `Copy-Item <plantilla> '<HARNESS>' -Recurse`, quitando también su `.git`.

**Ponlo donde quieras, en el mismo disco que los perfiles de usuario** (normalmente `C:`): el router y la config de OpenCode se enlazan con hardlinks, que no cruzan de un disco a otro. Tus repos pueden estar en cualquier sitio.

### 3.2 Lanzar setup.py

```powershell
py -3 <HARNESS>\setup.py --project "Mi Proyecto"
```

Hace lo que antes eran cinco pasos a mano (están en el [anexo](#anexo-montaje-a-mano), para ver qué hace o repetir uno a mano):

- **Nombres:** `<PROJECT>` y `<HARNESS>` en todos los ficheros (sin BOM, y con `/` en JSON y TypeScript, donde una `\` sería un escape); el marketplace y el plugin (`harness-mi-proyecto`, `mi-proyecto`: el prefijo de las skills en Claude); el router, renombrado a `mi-proyecto.instructions.md`.
- **Idioma** (`--lang es`): lo que lee el modelo (skills, agente, router, `CLAUDE.md`, checklist, `AGENTS.template.md` y los mensajes del sensor) en español, con nombres en español (`convenios-codigo`, `revisor`…). Por defecto, `en`. **Se elige una vez**, antes de rellenarlo: lo que escribas después es tuyo y no se puede traducir por ti.
- **Enlaces,** por herramienta y usuario: la junction del plugin, el `settings.json` de Claude (marketplace, plugin y hook `SessionStart`), el `~/.copilot` de Copilot y el `~/.config/opencode` de OpenCode. Si una carpeta ya tiene otras cosas (skills de otro proyecto), enlaza skill a skill y deja lo demás como está; si hay un fichero en medio (otro router), para y te avisa (§5).
- **Lo demás:** las copias generadas del agente (`sync.py`), el `--selftest` del sensor y la lista de lo que queda por rellenar (`FILL-IN`).

| Opción | Para qué |
|---|---|
| `--tools claude,copilot` | solo algunas herramientas (por defecto: `claude,copilot,opencode`) |
| `--users rober,ana` | otros usuarios de Windows del PC (por defecto, tú); sus perfiles, en el disco del harness |
| `--lang es` | las piezas en español (solo la primera vez) |
| `--vscode-permissions` | VS Code lee el harness y lanza el sensor sin preguntar (§3.5) |
| `--dry-run` | dice lo que haría, sin tocar nada |
| `--force` | sustituye un fichero que estorba, con copia de seguridad antes |

Lo que monta queda apuntado en `.setup.json`, a su lado. Lanzarlo otra vez no rompe nada: lo que ya está bien, lo deja como está. Antes de cambiar un `settings.json` por primera vez guarda una copia al lado (`settings.json.before-harness`), y solo esa.

### 3.3 Rellenar

Para ver todo lo pendiente:

```powershell
Select-String -Path '<HARNESS>\*' -Pattern 'FILL-IN' -Recurse
```

Orden recomendado (de más a menos uso):

1. **`code-conventions`:** lo que más entra. Si el equipo ya tiene sus convenios en el repo, aquí solo un puntero.
2. **`official-sources`:** la tabla del stack con versiones reales y las trampas.
3. **`check.py`:**
   - `MARKER`: un fichero que solo exista en ese repo. **Obligatorio si convives con otros proyectos** (§5).
   - `PROJECT_PYTHON`, si hay Python.
   - `RULES`: las trampas del paso 2 que se puedan pillar con una regex. Después, `py -3 <HARNESS>\personal\scripts\check.py --selftest` comprueba que estén bien escritas.
4. **`verify-before-done`:** los comandos reales de tests, lint y build.
5. **`systematic-debugging`:** las capas de la aplicación y sus trampas.
6. **`ui-design`:** si hay interfaz.
7. **`AGENTS.template.md`:** a la raíz del repo como `AGENTS.md`, si el repo es tuyo o el equipo está de acuerdo.

(Con `--lang es`, las mismas piezas con su nombre en español: `convenios-codigo`, `fuentes-oficiales`…)

### 3.4 Verificar

1. **Claude**, en una **sesión nueva** desde el repo (no un fork): "¿qué skills y agentes tienes, te ha llegado el hook y tienes AGENTS.md?". Deben salir `<project>:*`, el texto de `CLAUDE.md` y `AGENTS.md`.
2. **El sensor:** con una regla de `RULES` ya puesta, pídele a Claude que escriba en un fichero de prueba del repo algo que la incumpla. Justo tras la edición le debe llegar el `ERROR`. Luego, borra el fichero.
3. **VS Code:** recarga la ventana. Deben salir las skills (`/interview-me`…) y el agente `reviewer` en el selector, **una sola vez**.
4. **El router en VS Code:** paleta → "Chat: Configure Instructions" → debe salir `copilot-instructions` **una sola vez**. En un chat nuevo, "¿cuál es el único agente de revisión y en qué orden trabajas?" → `reviewer` y las fases.
5. **OpenCode**, desde el repo: `opencode run "sin tocar ficheros: cuál es el único agente de revisión, qué lanzas tras cada cambio y qué skills tienes"` → `reviewer`, el comando del sensor y **solo** las skills del harness. `opencode plugin list` → `sensor-<PROJECT>`. Para el sensor, la misma prueba que en Claude: el resultado de `write` debe traer el `ERROR`.

### 3.5 Mantenerlo a punto

- **`py -3 <HARNESS>\setup.py --check`** revisa todos los enlaces y ajustes y repara lo que es seguro reparar: un enlace que falta, un hardlink que ha roto un editor al guardar sustituyendo el fichero (si el texto sigue siendo el mismo) o una copia del agente desfasada. Si la copia de fuera tiene otro texto, no elige por ti: te dice cuál es más reciente.
- **Otro usuario u otra herramienta más tarde:** `setup.py --users ana` o `setup.py --tools opencode`.
- **Las confirmaciones de VS Code** (`--vscode-permissions`): el harness está fuera del workspace, así que Copilot pide confirmación cada vez que lee algo de él (en uso real, unas diez por sesión) y cuando el sensor va encadenado a otro comando. La opción añade dos ajustes al `settings.json` de VS Code de cada usuario: `github.copilot.chat.additionalReadAccessPaths` con la carpeta del harness, y una regla de `chat.tools.terminal.autoApprove` solo para el script del sensor. Recarga la ventana después. Solo se confía en **leer** el harness, no en cambiarlo: que un modelo reescriba sus propias reglas es algo que tienes que ver. No uses `chat.tools.global.autoApprove` (aprobar todo): quitaría también las confirmaciones que te protegen (base de datos, borrados, push).
- **`setup.py --uninstall`** (`--tools` y `--users` lo acotan): quita los enlaces y ajustes, solo los que apuntan a este harness. El harness se queda como está.

## 4. Día a día

- **Skill nueva:** `personal\skills\<nombre>\SKILL.md`. La ven todos los usuarios y las herramientas sin más; **en OpenCode, añádela también a la lista blanca** de `opencode\opencode.jsonc`.
- **Agente nuevo: en principio, no.** El harness tiene **un solo agente**, el `reviewer`. Un "revisor de X" se hace como skill con su checklist y se añade a la tabla de checklists del `reviewer` (ver [SKILLS-GUIDE §6](SKILLS-GUIDE.es.md#6-antes-de-añadir-algo-nuevo)). Solo compensa otro agente si hacen falta ojos frescos, permisos distintos o aislar un trabajo pesado que no cubra nada más. Si llega el caso: `personal\agents\<nombre>.agent.md` con frontmatter **de Claude** (`name`, `description`, `tools: Read, Grep…`); Copilot lo detecta igual (probado). Para OpenCode, después `py -3 <HARNESS>\opencode\sync.py`.
- **Revisión desde la CLI de OpenCode:** desde el repo, `& <HARNESS>\opencode\scripts\review-pending.ps1` lanza el `reviewer` sobre lo pendiente sin commitear (o `-Branch main` para la rama) y deja el informe con fecha en `opencode\reports\`. Sin código cambiado, sale sin despertar al modelo. Sirve a mano, con un alias, programado o en un hook `pre-push` local. En modo script lo que está en `ask` se rechaza: el informe lo dice.
- **Antes de añadir nada, pasa el filtro** de la [SKILLS-GUIDE §6](SKILLS-GUIDE.es.md#6-antes-de-añadir-algo-nuevo):
  - conocimiento que el modelo no puede saber,
  - o un fallo visto que se repite.

  Si se puede comprobar con una regex, mejor una regla nueva en `RULES` que una skill. **Antes de darla por buena, pásala por todo el repo (`--all`) y por las líneas añadidas en el historial**: una regla con falsos positivos bloquea al agente o acaba ignorada.
- **Checklist nueva para el revisor** (algo que solo sirve para revisar) → `personal\checklists\<nombre>.md` y una fila en la tabla de fuentes del `reviewer`, con sus ejes.

### Qué va en cada fichero de instrucciones

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

### Escribir una skill que funcione

- **`name`** igual que la carpeta, en minúsculas, números y guiones, **sin `_`**: si no, falla en silencio.
- **La `description` es lo único que ve el modelo** hasta que decide cargarla. Tiene que decir **cuándo** usarla, no resumir lo que hace, y llevar **palabras concretas** de las peticiones reales ("componente", "slot", "query"…). Si es genérica, no se dispara.
- **Corta:** 600 palabras como mucho, con tablas antes que párrafos. Si necesita más, un índice y ficheros al lado que se lean bajo demanda.
- **Si es del proyecto**, la primera línea: "Si no estás en el repo de <PROJECT>, ignora esta skill". Las skills de Claude valen en todos los proyectos.
- **Que no escriba en el repo** (planes, intents, ficheros de trabajo) y que pida permiso para la BD.
- **Si es adaptada,** el crédito al pie, con el commit de origen ("Adaptada de X de [repo] @ `sha` (fecha) (MIT)"), y su aviso de copyright en `THIRD-PARTY-NOTICES.md`.
- **Revisar el upstream** (cada pocos meses): por cada skill adaptada, diff de su repo desde el commit del pie (`git diff <sha>..HEAD -- skills/<nombre>/`). Entra solo lo que pase el filtro de la SKILLS-GUIDE §6; si se aplica algo, se actualiza el commit del pie.
- **Probarla en las dos herramientas,** en sesión nueva y sin invocarla a mano: ¿entra sola cuando toca? Y comprobar el resultado, no solo que la cargue. Con modelos locales pequeños, contar con invocarla a mano (`/nombre`).

## 5. Convivir con otros proyectos

Las herramientas no separan por proyecto. Ojo con esto:

- **Claude: los plugins valen en todas partes.** Las skills de cada proyecto entran en cualquier repo. Por eso:
  - cada plugin tiene un nombre distinto, y así su prefijo (`proyecto-a:`, `proyecto-b:`);
  - las skills del proyecto empiezan con "si no estás en el repo de X, ignora";
  - el `CLAUDE.md` del hook empieza con "si estás en el repo de X…". Los `SessionStart` de todos los proyectos se ejecutan en cada sesión.

  Alternativa sin probar: activar el plugin solo en ese repo, en su `.claude/settings.local.json` (local, no se sube), en vez de en el `settings.json` del usuario.
- **El sensor:** el hook de cada plugin salta en **todas** las ediciones. Con `MARKER = None` se ejecutaría también en los repos de otros proyectos. **Pon siempre un `MARKER`** para que solo actúe en el suyo.
- **Copilot no tiene prefijos y `~/.copilot/skills` es una sola carpeta:**
  - **Lo del método** (`interview-me`, `systematic-debugging`, `verify-before-done`, `comment-style`, `reviewer`) es igual en todos los proyectos: enlaza **una sola copia**.
  - **Lo del proyecto** (`code-conventions`, `ui-design`, `official-sources`) chocaría por nombre. Mejor en el `.github/` del repo, si se puede; si no, renómbralo con prefijo (`<project>-conventions`).
  - **El `reviewer`** también es del método, pero lee las checklists por ruta: con varios proyectos, haz una copia por proyecto (`<project>-reviewer`) que apunte a las suyas.
  - Para mezclar proyectos, `~/.copilot/skills` pasa a ser una carpeta normal con **una junction por skill**:

    ```powershell
    New-Item -ItemType Junction -Path "$HOME\.copilot\skills\<skill>" -Target "<HARNESS>\personal\skills\<skill>"
    ```
- **OpenCode:** `~/.config/opencode` tiene un solo `AGENTS.md`, una sola config y una carpeta de skills, como `~/.copilot`: junta los routers en un fichero, une las configs (la lista blanca, con las skills de todos) y usa una junction por skill. Los plugins sí conviven: cada uno lleva su `id` (`sensor-<PROJECT>`) y su `MARKER`.
- **Si el equipo ya tiene skills y agentes en el repo** (`.github/`): Copilot ya los ve; **no los copies a `personal\`**. Para Claude, crea un plugin aparte en `claude\plugins\<project>-repo\` (con su `.claude-plugin\plugin.json`) con **punteros**: un `SKILL.md` con la misma `description` y el cuerpo "Lee `<ruta en el repo>` desde la raíz del repo y síguelo; si no existe, avisa". Nunca en `~/.claude/skills` ni en `.claude/` del repo, porque VS Code los duplicaría.

## 6. Gotchas (aprendidos a palos)

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
- **`py -3` y no `python`:** el lanzador está en `C:\Windows` y vale para todos los usuarios. Configura `PROJECT_PYTHON` para compilar con el Python del proyecto y no con el del sistema.
- **Detectar no es cargar:** en VS Code, que una skill exista no implica que el modelo la use; lo decide por la `description`, y los modelos locales fallan más. Se fuerza escribiendo `/nombre`.
- **Docs del equipo en una carpeta ignorada por git** (p. ej. `docs/` en el `.gitignore`): el buscador de Copilot no los ve y un grep ahí sale vacío. Busca con `includeIgnoredFiles: true` o léelos por ruta; si tus skills apuntan ahí, dilo en el router.
- **Rutas de Windows dentro de `sed` o `python -c`** en Git Bash: `\a`, `\r`… se interpretan como escapes y rompen el texto. Mejor un script aparte.
- **Repos de otro usuario de Windows:** git da *dubious ownership* → `git config --global --add safe.directory <ruta>`.

## 7. Añadir otra herramienta (OpenCode, Cursor…)

1. **Averigua dónde busca,** en su documentación oficial: instrucciones, skills y agentes, a nivel usuario y de workspace. Y si lee rutas de **otras** herramientas (como VS Code lee `~/.claude`).
2. **Cruza con lo que ya le llega:** ¿`AGENTS.md`? ¿`.github/`? ¿`~/.claude` o `~/.copilot`? Lo que ya le llegue **no** se enlaza otra vez. Ojo también con lo que encuentra **subiendo** desde el repo (OpenCode llega hasta el home).
3. **Lo personal:** si su carpeta de usuario está vacía, una junction entera a `personal\{skills,agents}`; si no, una por skill.
4. **Formato:** `SKILL.md` es estándar. Si no acepta el frontmatter de Claude para agentes, ponle una carpeta propia `<herramienta>\agents\` con punteros.
5. **Instrucciones globales:** por hook o config de usuario, nunca con un fichero de instrucciones en una carpeta superior al repo.
6. **Verifica** en sesión nueva que lo ve y que las demás no empiezan a duplicar.

OpenCode es el ejemplo ya hecho (§A.5): el paso 2 destapó la búsqueda hasta el home (lista blanca), y el paso 4, que no acepta el frontmatter de agentes de Claude (copia generada).

## 8. Comprobaciones (CI)

En cada push, el [CI](.github/workflows/ci.yml) valida la propia plantilla:
- **Estructura** ([`validate.py`](.github/scripts/validate.py)): frontmatter de skills y agente (`name` igual que la carpeta, sin `_`; el agente original con los nombres de herramienta de Claude), sin BOM, JSON válidos, sin `strict`/`version` en el marketplace, que exista el script del hook, SVG bien formados, `VERSION` en SemVer, enlaces y anclas de los Markdown, y ninguna ruta de usuario real. Y en OpenCode: la config se parsea, la lista blanca incluye todas las skills de `personal\skills`, las copias generadas del agente están al día (la de OpenCode sin `tools:`, la de Copilot con los nombres de VS Code), y existe el script que lanza el plugin. Y las traducciones de `i18n\`: una por cada pieza que lee el modelo, con las mismas líneas y encabezados que la inglesa (así un cambio en una se nota en la otra), y los nombres que reciben tras `setup.py`.
- **Sensor:** `check.py --selftest` en Ubuntu y Windows (`RULES` bien escritas y el motor sobre ficheros de ejemplo), en los dos idiomas.
- **`setup.py`** ([`test_setup.py`](.github/scripts/test_setup.py), Windows): sobre una copia temporal y perfiles falsos, uno de ellos ya en uso, en cada idioma: instalar, volver a lanzarlo sin cambios, `--check` reparando un hardlink roto y una junction que falta (y sin tocar una copia con otro texto), y `--uninstall` dejando los perfiles como estaban.

Al publicar una release, además comprueba que `VERSION` coincida con el tag ([release.yml](.github/workflows/release.yml)). En local: `python .github/scripts/validate.py`.

## 9. Licencia

[MIT](LICENSE). Algunas skills y el agente `reviewer` están adaptados de [obra/superpowers](https://github.com/obra/superpowers) y [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), los dos con licencia MIT. Sus avisos de copyright están en [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). Si adaptas otra skill de fuera, añade ahí su aviso.

## Anexo: montaje a mano

Lo que hace `setup.py`, paso a paso: para entenderlo, para repetir un paso a mano o para montarlo en Linux o macOS (allí, symlinks con `ln -s` en vez de junctions y hardlinks, y `python3` en vez de `py -3`). El orden: A.1 y A.2 una vez, de A.3 a A.5 en cada usuario.

### A.1 Poner nombre

1. **Marketplace y plugin** (`claude\.claude-plugin\marketplace.json`): `harness-project` → `harness-<project>` y `project` → `<project>`, en minúsculas y con guiones.
   - El nombre del plugin es el **prefijo de las skills en Claude** (`<project>:code-conventions`), así que tiene que ser distinto en cada proyecto.
   - **No pongas `"strict"` ni `"version"`** en esa entrada (§6).
2. **En `claude\CLAUDE.md`**, el prefijo `project:` por el nuevo.
3. **`<PROJECT>` y `<HARNESS>` en todos los ficheros.** Hay que guardar **sin BOM**: un BOM delante del `---` del frontmatter rompe la skill sin avisar. Por eso no vale `Set-Content` de PowerShell 5.1:

```powershell
$h = 'RUTA_REAL_DEL_HARNESS'   # la ruta de verdad, sin marcadores: es lo que se escribirá en los ficheros
$utf8 = New-Object System.Text.UTF8Encoding($false)
Get-ChildItem $h -Recurse -File -Include *.md,*.py,*.ts,*.json,*.jsonc,*.ps1 | ForEach-Object {
  $t = [IO.File]::ReadAllText($_.FullName)
  # en JSON y TypeScript una \ empieza un escape: ahí la ruta va con /
  $p = if ($_.Extension -in '.json', '.jsonc', '.ts') { $h.Replace('\', '/') } else { $h }
  $n = $t.Replace('<PROJECT>', 'NombreReal').Replace('<HARNESS>', $p)
  if ($n -ne $t) { [IO.File]::WriteAllText($_.FullName, $n, $utf8) }
}
```

### A.2 Junction del plugin

```powershell
$a = '<HARNESS>'
New-Item -ItemType Junction -Path "$a\claude\plugins\<project>" -Target "$a\personal"
```

(Si la carpeta `claude\plugins` no existe, créala antes. El nombre de la junction tiene que coincidir con el `source` del marketplace.)

### A.3 Conectar Claude (en cada usuario)

`C:\Users\<usuario>\.claude\settings.json`, fusionando con lo que ya haya:

```json
{
  "extraKnownMarketplaces": {
    "harness-<project>": {
      "source": { "source": "directory", "path": "<HARNESS>\\claude" }
    }
  },
  "enabledPlugins": {
    "<project>@harness-<project>": true
  },
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command", "command": "cat \"<HARNESS>/claude/CLAUDE.md\"" } ] }
    ]
  }
}
```

Ojo con las barras: en `"path"` van **dobles** (`C:\\ruta\\al\\harness\\claude`), porque es JSON; en el `cat` del hook van **normales** (`C:/ruta/al/harness/claude/CLAUDE.md`), porque lo ejecuta Git Bash.

El hook del sensor no va aquí: lo trae el propio plugin (`personal\hooks\hooks.json`).

### A.4 Conectar Copilot (en cada usuario)

**Si `~/.copilot/skills` y `~/.copilot/agents` están vacías o no existen:**

```powershell
$a = '<HARNESS>'
$u = 'NOMBRE_USUARIO'
foreach ($d in @{ skills = "$a\personal\skills"; agents = "$a\copilot\agents" }.GetEnumerator()) {
  $l = "C:\Users\$u\.copilot\$($d.Key)"
  if (Test-Path $l) { [IO.Directory]::Delete($l) }   # falla si no está vacía: revisa antes qué hay
  New-Item -ItemType Junction -Path $l -Target $d.Value   # agents: la copia generada con los alias de VS Code
}
```

`copilot\agents\` lo genera `opencode\sync.py`: VS Code no conoce los nombres de herramienta de Claude (`Read, Grep…`) y deja al agente **sin herramientas**, así que su copia lleva `tools: [read, search, execute]`. No edites `personal\agents\` desde Copilot: VS Code puede restaurar luego su propia copia del fichero con sus nombres de herramienta, y el agente de Claude se queda sin herramientas (si pasa, `sync.py` se niega a generar y el CI falla).

**Si ya apuntan a otro proyecto**, no se pueden enlazar dos veces: mira §5.

**Opcional: que no pida permiso para el harness** (lo que hace `--vscode-permissions`, §3.5). En el `settings.json` de VS Code de cada usuario (`%APPDATA%\Code\User\settings.json`), por ejemplo con `<HARNESS>` = `C:\Harness\Proyecto` (en JSON cada `\` va doble, y dentro de la regex se vuelve a doblar):

```jsonc
// leer el harness sin pedir permiso; editar sigue limitado al workspace
"github.copilot.chat.additionalReadAccessPaths": [
  "C:\\Harness\\Proyecto"
],
// el sensor (solo ese script, con o sin ficheros) sin pedir permiso
"chat.tools.terminal.autoApprove": {
  "/^py -3 C:\\\\Harness\\\\Proyecto\\\\personal\\\\scripts\\\\check\\.py(\\s|$)/": true
}
```

Recarga la ventana después.

**El router de Copilot** (`copilot\project.instructions.md`; renómbralo a `<project>.instructions.md`) lleva `applyTo: "**"`. Tanto el **chat de VS Code** como Copilot CLI leen `~/.copilot/copilot-instructions.md`, así que basta un hardlink ahí. No lo pongas también en `prompts\` del perfil: VS Code lo cargaría dos veces. Es un fichero suelto: una junction no vale (solo carpetas) y un symlink necesita admin o el modo desarrollador. Se enlaza con **hardlinks**, que no necesitan nada (mismo disco), y el original sigue en el harness:

```powershell
$r = '<HARNESS>\copilot\<project>.instructions.md'
foreach ($l in @("C:\Users\$u\.copilot\copilot-instructions.md")) {   # lo leen el chat de VS Code y Copilot CLI
  if (Test-Path $l) { Remove-Item -LiteralPath $l }   # ficheros sueltos, no junctions
  New-Item -ItemType HardLink -Path $l -Target $r
}
```

En `~/.copilot` solo cabe uno: con varios proyectos, junta sus routers en ese fichero (cada bloque con su "solo si estás en el repo de X").

### A.5 Conectar OpenCode (en cada usuario, opcional)

Para OpenCode 2 (CLI y Desktop comparten servidor y config). Antes, en `opencode\opencode.jsonc`, rellena el modelo y el proveedor (viene preparado para un servidor local compatible con OpenAI, como llama.cpp; con uno en la nube, bórralos) y, si el equipo tiene skills en el repo, su ruta en `"skills"`.

```powershell
$a = '<HARNESS>'
$c = "C:\Users\$u\.config\opencode"   # lo crea OpenCode al arrancar; deja service.json, borra restos de v1 (package.json, node_modules)
New-Item -ItemType HardLink -Path "$c\opencode.jsonc" -Target "$a\opencode\opencode.jsonc"
New-Item -ItemType HardLink -Path "$c\AGENTS.md"      -Target "$a\copilot\<project>.instructions.md"   # el mismo router que Copilot
New-Item -ItemType Junction -Path "$c\skills"         -Target "$a\personal\skills"
New-Item -ItemType Junction -Path "$c\agents"         -Target "$a\opencode\agents"
New-Item -ItemType Junction -Path "$c\plugins"        -Target "$a\opencode\plugins"
```

- **El router** es el de Copilot: OpenCode 2 solo lee `AGENTS.md` y el global es `~/.config/opencode/AGENTS.md`, fuera del repo. El frontmatter `applyTo` le llega como texto y no molesta.
- **El `reviewer`** de `opencode\agents\` es una **copia generada**: OpenCode ignora el agente entero si su frontmatter lleva `tools:`. El mismo script escribe la de Copilot (`copilot\agents\`, con los nombres de herramienta de VS Code). Tras tocar `personal\agents\`, `py -3 <HARNESS>\opencode\sync.py` (la CI avisa si se te olvida). Lo propio de OpenCode (subagente, pasos, sin editar) va en `agents` de la config.
- **El sensor** es el plugin `opencode\plugins\sensor.ts`: tras cada `write`/`edit`/`patch` pasa `check.py --hook` y añade su salida al resultado de la herramienta, como el hook de Claude.
- **La lista blanca de skills** (`permissions`, acción `skill`) deja ver solo las del harness: OpenCode sube desde el repo hasta el home buscando `.claude/skills` y `.agents/skills`, y se trae las de otras herramientas. **Cada skill nueva, a la lista** (la CI lo comprueba).
- **Búsqueda web gratis:** el MCP `ddg-search` (DuckDuckGo, por `uvx`; instala `uv` en cada usuario con `winget install astral-sh.uv`). Buscar no pregunta; **leer páginas sí**, porque una web puede esconder instrucciones para el modelo. Añade a las reglas `allow` de `webfetch` la documentación oficial de tu stack.
- **Con un modelo local** de un solo slot (llama.cpp con `parallel = 1`): el agente `title` va desactivado, porque su petición echaba la caché del turno principal en cada sesión nueva (14-22 s medidos).
