# one-agent-harness

🌐 [English](README.md) · **Español**

<p align="center"><img src="img/route.svg" alt="Un escalador (el modelo) con un arnés del que cuelgan seis piezas (las skills), un aparato autoblocante (el sensor) y quien le asegura (el agente). Los nombres de las versiones son los anclajes de la vía: Anchor, Belay, Carabiner, Descender y Hexcentric en la cima" width="100%"></p>

[![CI](https://github.com/robmab/one-agent-harness/actions/workflows/ci.yml/badge.svg)](https://github.com/robmab/one-agent-harness/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/robmab/one-agent-harness)](https://github.com/robmab/one-agent-harness/releases)
[![License: MIT](https://img.shields.io/github/license/robmab/one-agent-harness)](LICENSE)

Plantilla para montar el harness de IA de **cualquier proyecto**: skills, agentes, un sensor automático e instrucciones, compartidos entre todos los usuarios de Windows del PC y entre Claude Code, GitHub Copilot (VS Code) y OpenCode 2, **sin tocar el workspace** si no quieres.

Sale de un harness ya montado y probado en un proyecto real (2026-10-10), quitando todo lo específico de ese proyecto.

> **Es inerte:** no la carga ninguna herramienta. No se usa aquí: se **copia** a `<RAIZ>\<Proyecto>`, se rellena y se conecta. Cada pieza pendiente está marcada con `RELLENAR`.

**Nombres que se usan en toda la plantilla:**

| Marcador | Qué es |
|---|---|
| `<RAIZ>` | la carpeta donde guardas los harness. Mejor una que **lean y escriban todos los usuarios de Windows** del PC (p. ej. una carpeta dentro de `C:\Users\Public`) y que esté **fuera de los repos** |
| `<HARNESS>` | la carpeta del harness de un proyecto: `<RAIZ>\<Proyecto>` |
| `<PROYECTO>` / `<proyecto>` | el nombre del proyecto; en minúsculas y con guiones donde hace de identificador (plugin, marketplace) |

| Documento | Para qué |
|---|---|
| **README** (este) | qué trae, cómo montar un proyecto nuevo y cómo convivir con otros |
| [GUIA-SKILLS](GUIA-SKILLS.md) | qué hace cada pieza, de qué tipo es, en qué momento entra y qué hay que rellenar |
| [INVESTIGACION](INVESTIGACION.md) | de dónde sale todo: qué es un harness, repos analizados, skills adaptadas y descartadas |
| [SKILLS-OPCIONALES](SKILLS-OPCIONALES.md) | catálogo de skills opcionales: qué aporta cada una, cuándo meterla, qué ruido mete y cuáles se desaconsejan |
| [AGENTS.plantilla.md](AGENTS.plantilla.md) | el índice que va en la raíz del repo del proyecto |
| [LICENSE](LICENSE) · [THIRD-PARTY-NOTICES](THIRD-PARTY-NOTICES.md) | licencia MIT y créditos de las skills adaptadas (§9) |

![Qué llega a cada herramienta y por dónde](img/cableado.svg)

---

## 1. Estructura

```
one-agent-harness\
├─ README.md (inglés) · README.es.md · GUIA-SKILLS.md · INVESTIGACION.md · SKILLS-OPCIONALES.md
├─ LICENSE · THIRD-PARTY-NOTICES.md · .gitattributes
├─ .github\                             CI de este repo (no es de la plantilla; se quita al copiar)
├─ VERSION                             versión de la plantilla de la que sale este harness
├─ AGENTS.plantilla.md                   → a la raíz del repo como AGENTS.md
├─ img\                                  esquemas SVG y el banner (route.svg)
├─ claude\                               ← lo que solo usa Claude
│  ├─ CLAUDE.md                          el router: orden de trabajo, sensor y agente (lo mete el hook SessionStart)
│  ├─ .claude-plugin\marketplace.json    marketplace "harness-proyecto" con el plugin "proyecto"
│  └─ plugins\proyecto                   ⇒ JUNCTION a ..\..\personal (se crea al montar, §3.3)
├─ copilot\proyecto.instructions.md      el router para Copilot y OpenCode: HARDLINK desde ~/.copilot (§3.6) y ~/.config/opencode (§3.7)
├─ opencode\                             ← lo que solo usa OpenCode (opcional, §3.7)
│  ├─ opencode.jsonc                     RELLENAR  modelo y proveedor; permisos, lista blanca de skills, revisor
│  ├─ agents\revisor.md                  GENERADO  por sincronizar.py desde personal\agents (no editar aquí)
│  ├─ plugins\sensor.ts                  LISTA     pasa comprobar.py tras cada edición (como el hook de Claude)
│  └─ sincronizar.py                     LISTA     regenera agents\ (--check: solo comprueba)
└─ personal\                             ← lo que leen Claude, Copilot y OpenCode
   ├─ skills\
   │  ├─ convenios-codigo\               RELLENAR  convenios del proyecto
   │  ├─ diseno-ui\                      RELLENAR  design system
   │  ├─ fuentes-oficiales\              AJUSTAR   tabla del stack y trampas
   │  ├─ verificar-antes-de-acabar\      AJUSTAR   comandos de prueba
   │  ├─ depuracion-sistematica\         AJUSTAR   capas y trampas
   │  ├─ entrevistame\                   LISTA
   │  └─ estilo-comentarios\             OPCIONAL  tu voz (comentarios y chat); fuera del core
   ├─ agents\
   │  └─ revisor.agent.md                LISTA     el único agente: revisión a fondo, convenios incluidos, no edita
   ├─ checklists\seguridad.md            AJUSTAR   la lee solo el revisor (eje 3); fuera de cualquier catálogo
   ├─ scripts\comprobar.py               AJUSTAR   sensor: MARCADOR, PYTHON_PROYECTO y REGLAS; solo líneas cambiadas
   └─ hooks\hooks.json                   LISTA     PostToolUse: pasa comprobar.py tras cada edición
```

- **LISTA:** vale tal cual.
- **AJUSTAR:** el método vale; hay que rellenar sus tablas.
- **RELLENAR:** plantilla vacía; el contenido es del proyecto.
- **OPCIONAL:** fuera del core; se queda o se quita según la persona.

El **core** son 6 skills + 1 sensor + 1 agente, sobre `AGENTS.md` (ver [GUIA-SKILLS §2](GUIA-SKILLS.md#2-qué-es-el-core)).

## 2. Cómo lo encuentra cada herramienta

| Herramienta | Qué lee | Por dónde |
|---|---|---|
| Claude Code | `AGENTS.md` del repo | lo carga solo al arrancar, **si no hay ningún `CLAUDE.md` en el repo ni en carpetas superiores** (§6) |
| Claude Code | plugin `proyecto` (skills, agentes y hook) | marketplace local en `~/.claude/settings.json`; el plugin es la junction `claude\plugins\proyecto` |
| Claude Code | `claude\CLAUDE.md` | hook `SessionStart` que hace `cat` del fichero |
| Copilot (VS Code) | `AGENTS.md` y `.github/` del repo, si los hay | el propio repo |
| Copilot (VS Code) | skills y agentes de `personal\` | junctions `~/.copilot/skills` y `~/.copilot/agents` |
| Copilot (VS Code y CLI) | el router `copilot\<proyecto>.instructions.md` | hardlink en `~/.copilot/copilot-instructions.md`; se carga siempre |
| Copilot (VS Code) | `comprobar.py` | no hay hook: se lo ordena el router ("DESPUÉS de cada cambio"), o lo lanzas tú |
| OpenCode 2 | `AGENTS.md` del repo y el router | el del repo, solo; el router, hardlink `~/.config/opencode/AGENTS.md` → `copilot\<proyecto>.instructions.md`. **No lee `CLAUDE.md`** |
| OpenCode 2 | skills de `personal\` y del repo | junction `~/.config/opencode/skills`; las del repo, campo `skills` de la config. Filtradas por la lista blanca |
| OpenCode 2 | el `revisor` | junction `~/.config/opencode/agents` → `opencode\agents` (copia generada) |
| OpenCode 2 | `comprobar.py` tras cada edición | junction `~/.config/opencode/plugins` → `opencode\plugins\sensor.ts` |
| OpenCode 2 | modelo, permisos | hardlink `~/.config/opencode/opencode.jsonc` → `opencode\opencode.jsonc` |

**Por qué así:** VS Code Copilot también lee `~/.claude/skills`, `~/.claude/agents` y `.claude/` del workspace. Lo que pongas ahí lo ve dos veces si además está en `.github/` o en `~/.copilot`. Los **plugins** de Claude, en cambio, Copilot no los descubre, y Claude no lee `~/.copilot`. OpenCode, por su parte, sube desde el repo hasta el home buscando `.claude/skills`: de ahí la lista blanca de skills en su config. Resultado: cada herramienta ve cada cosa una sola vez.

## 3. Montar un proyecto nuevo

Requisitos: Claude Code (usa Git Bash para los hooks en Windows), VS Code con Copilot, OpenCode 2 si lo usas, y el lanzador `py` de Python. Las junctions **no necesitan admin**.

### 3.1 Copiar

```powershell
git clone <url-de-este-repo> '<HARNESS>'
Remove-Item '<HARNESS>\.git', '<HARNESS>\.github' -Recurse -Force
```

El `.git` se borra para que el harness del proyecto no quede atado a la plantilla, y `.github` porque solo tiene el CI de este repo. Más fácil todavía: descarga **Source code (zip)** de la [última release](https://github.com/robmab/one-agent-harness/releases/latest), que ya viene sin los dos. **No borres `VERSION`:** dice de qué versión de la plantilla sale el harness, y así más adelante puedes ver qué ha cambiado desde entonces (en las [releases](https://github.com/robmab/one-agent-harness/releases)). Si quieres versionarlo, haz después tu propio `git init`. Si ya tienes la plantilla en local, vale igual con `Copy-Item <plantilla> '<HARNESS>' -Recurse`, quitando también su `.git`.

### 3.2 Poner nombre

1. **Marketplace y plugin** (`claude\.claude-plugin\marketplace.json`): `harness-proyecto` → `harness-<proyecto>` y `proyecto` → `<proyecto>`, en minúsculas y con guiones.
   - El nombre del plugin es el **prefijo de las skills en Claude** (`<proyecto>:convenios-codigo`), así que tiene que ser distinto en cada proyecto.
   - **No pongas `"strict"` ni `"version"`** en esa entrada (§6).
2. **En `claude\CLAUDE.md`**, el prefijo `proyecto:` por el nuevo.
3. **`<PROYECTO>` y `<HARNESS>` en todos los ficheros.** Hay que guardar **sin BOM**: un BOM delante del `---` del frontmatter rompe la skill sin avisar. Por eso no vale `Set-Content` de PowerShell 5.1:

```powershell
$h = 'RUTA_REAL_DEL_HARNESS'   # la ruta de verdad, sin marcadores: es lo que se escribirá en los ficheros
$utf8 = New-Object System.Text.UTF8Encoding($false)
Get-ChildItem $h -Recurse -File -Include *.md,*.py,*.ts,*.jsonc | ForEach-Object {
  $t = [IO.File]::ReadAllText($_.FullName)
  $n = $t.Replace('<PROYECTO>', 'NombreReal').Replace('<HARNESS>', $h)
  if ($n -ne $t) { [IO.File]::WriteAllText($_.FullName, $n, $utf8) }
}
```

### 3.3 Junction del plugin

```powershell
$a = '<HARNESS>'
New-Item -ItemType Junction -Path "$a\claude\plugins\<proyecto>" -Target "$a\personal"
```

(Si la carpeta `claude\plugins` no existe, créala antes. El nombre de la junction tiene que coincidir con el `source` del marketplace.)

### 3.4 Rellenar

Para ver todo lo pendiente:

```powershell
Select-String -Path '<HARNESS>\*' -Pattern 'RELLENAR' -Recurse
```

Orden recomendado (de más a menos uso):

1. **`convenios-codigo`:** lo que más entra. Si el equipo ya tiene sus convenios en el repo, aquí solo un puntero.
2. **`fuentes-oficiales`:** la tabla del stack con versiones reales y las trampas.
3. **`comprobar.py`:**
   - `MARCADOR`: un fichero que solo exista en ese repo. **Obligatorio si convives con otros proyectos** (§5).
   - `PYTHON_PROYECTO`, si hay Python.
   - `REGLAS`: las trampas del paso 2 que se puedan pillar con una regex. Después, `py -3 <HARNESS>\personal\scripts\comprobar.py --selftest` comprueba que estén bien escritas.
4. **`verificar-antes-de-acabar`:** los comandos reales de tests, lint y build.
5. **`depuracion-sistematica`:** las capas de la aplicación y sus trampas.
6. **`diseno-ui`:** si hay interfaz.
7. **`AGENTS.plantilla.md`:** a la raíz del repo como `AGENTS.md`, si el repo es tuyo o el equipo está de acuerdo.

### 3.5 Conectar Claude (en cada usuario)

`C:\Users\<usuario>\.claude\settings.json`, fusionando con lo que ya haya:

```json
{
  "extraKnownMarketplaces": {
    "harness-<proyecto>": {
      "source": { "source": "directory", "path": "<HARNESS>\\claude" }
    }
  },
  "enabledPlugins": {
    "<proyecto>@harness-<proyecto>": true
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

### 3.6 Conectar Copilot (en cada usuario)

**Si `~/.copilot/skills` y `~/.copilot/agents` están vacías o no existen:**

```powershell
$a = '<HARNESS>'
$u = 'NOMBRE_USUARIO'
foreach ($d in 'skills','agents') {
  $l = "C:\Users\$u\.copilot\$d"
  if (Test-Path $l) { [IO.Directory]::Delete($l) }   # falla si no está vacía: revisa antes qué hay
  New-Item -ItemType Junction -Path $l -Target "$a\personal\$d"
}
```

**Si ya apuntan a otro proyecto**, no se pueden enlazar dos veces: mira §5.

**El router de Copilot** (`copilot\proyecto.instructions.md`; renómbralo a `<proyecto>.instructions.md`) lleva `applyTo: "**"`. Tanto el **chat de VS Code** como Copilot CLI leen `~/.copilot/copilot-instructions.md`, así que basta un hardlink ahí. No lo pongas también en `prompts\` del perfil: VS Code lo cargaría dos veces. Es un fichero suelto: una junction no vale (solo carpetas) y un symlink necesita admin o el modo desarrollador. Se enlaza con **hardlinks**, que no necesitan nada (mismo disco), y el original sigue en el harness:

```powershell
$r = '<HARNESS>\copilot\<proyecto>.instructions.md'
foreach ($l in @("C:\Users\$u\.copilot\copilot-instructions.md")) {   # lo leen el chat de VS Code y Copilot CLI
  if (Test-Path $l) { Remove-Item -LiteralPath $l }   # ficheros sueltos, no junctions
  New-Item -ItemType HardLink -Path $l -Target $r
}
```

En `~/.copilot` solo cabe uno: con varios proyectos, junta sus routers en ese fichero (cada bloque con su "solo si estás en el repo de X").

### 3.7 Conectar OpenCode (en cada usuario, opcional)

Para OpenCode 2 (CLI y Desktop comparten servidor y config). Antes, en `opencode\opencode.jsonc`, rellena el modelo y el proveedor (viene preparado para un servidor local compatible con OpenAI, como llama.cpp; con uno en la nube, bórralos) y, si el equipo tiene skills en el repo, su ruta en `"skills"`.

```powershell
$a = '<HARNESS>'
$c = "C:\Users\$u\.config\opencode"   # lo crea OpenCode al arrancar; deja service.json, borra restos de v1 (package.json, node_modules)
New-Item -ItemType HardLink -Path "$c\opencode.jsonc" -Target "$a\opencode\opencode.jsonc"
New-Item -ItemType HardLink -Path "$c\AGENTS.md"      -Target "$a\copilot\<proyecto>.instructions.md"   # el mismo router que Copilot
New-Item -ItemType Junction -Path "$c\skills"         -Target "$a\personal\skills"
New-Item -ItemType Junction -Path "$c\agents"         -Target "$a\opencode\agents"
New-Item -ItemType Junction -Path "$c\plugins"        -Target "$a\opencode\plugins"
```

- **El router** es el de Copilot: OpenCode 2 solo lee `AGENTS.md` y el global es `~/.config/opencode/AGENTS.md`, fuera del repo. El frontmatter `applyTo` le llega como texto y no molesta.
- **El `revisor`** de `opencode\agents\` es una **copia generada**: OpenCode ignora el agente entero si su frontmatter lleva `tools:`. Tras tocar `personal\agents\`, `py -3 <HARNESS>\opencode\sincronizar.py` (la CI avisa si se te olvida). Lo propio de OpenCode (subagente, pasos, sin editar) va en `agents` de la config.
- **El sensor** es el plugin `opencode\plugins\sensor.ts`: tras cada `write`/`edit`/`patch` pasa `comprobar.py --hook` y añade su salida al resultado de la herramienta, como el hook de Claude.
- **La lista blanca de skills** (`permissions`, acción `skill`) deja ver solo las del harness: OpenCode sube desde el repo hasta el home buscando `.claude/skills` y `.agents/skills`, y se trae las de otras herramientas. **Cada skill nueva, a la lista** (la CI lo comprueba).
- **Con un modelo local** de un solo slot (llama.cpp con `parallel = 1`): el agente `title` va desactivado, porque su petición echaba la caché del turno principal en cada sesión nueva (14-22 s medidos).

### 3.8 Verificar

1. **Claude**, en una **sesión nueva** desde el repo (no un fork): "¿qué skills y agentes tienes, te ha llegado el hook y tienes AGENTS.md?". Deben salir `<proyecto>:*`, el texto de `CLAUDE.md` y `AGENTS.md`.
2. **El sensor:** con una regla de `REGLAS` ya puesta, pídele a Claude que escriba en un fichero de prueba del repo algo que la incumpla. Justo tras la edición le debe llegar el `ERROR`. Luego, borra el fichero.
3. **VS Code:** recarga la ventana. Deben salir las skills (`/entrevistame`…) y el agente `revisor` en el selector, **una sola vez**.
4. **El router en VS Code:** paleta → "Chat: Configure Instructions" → debe salir `copilot-instructions` **una sola vez**. En un chat nuevo, "¿cuál es el único agente de revisión y en qué orden trabajas?" → `revisor` y las fases.
5. **OpenCode**, desde el repo: `opencode run "sin tocar ficheros: cuál es el único agente de revisión, qué lanzas tras cada cambio y qué skills tienes"` → `revisor`, el comando del sensor y **solo** las skills del harness. `opencode plugin list` → `sensor-<PROYECTO>`. Para el sensor, la misma prueba que en Claude: el resultado de `write` debe traer el `ERROR`.

## 4. Día a día

- **Skill nueva:** `personal\skills\<nombre>\SKILL.md`. La ven todos los usuarios y las herramientas sin más; **en OpenCode, añádela también a la lista blanca** de `opencode\opencode.jsonc`.
- **Agente nuevo: en principio, no.** El harness tiene **un solo agente**, el `revisor`. Un "revisor de X" se hace como skill con su checklist y se añade a la tabla de checklists del `revisor` (ver [GUIA-SKILLS §6](GUIA-SKILLS.md#6-antes-de-añadir-algo-nuevo)). Solo compensa otro agente si hacen falta ojos frescos, permisos distintos o aislar un trabajo pesado que no cubra nada más. Si llega el caso: `personal\agents\<nombre>.agent.md` con frontmatter **de Claude** (`name`, `description`, `tools: Read, Grep…`); Copilot lo detecta igual (probado). Para OpenCode, después `py -3 <HARNESS>\opencode\sincronizar.py`.
- **Antes de añadir nada, pasa el filtro** de la [GUIA-SKILLS §6](GUIA-SKILLS.md#6-antes-de-añadir-algo-nuevo):
  - conocimiento que el modelo no puede saber,
  - o un fallo visto que se repite.

  Si se puede comprobar con una regex, mejor una regla nueva en `REGLAS` que una skill. **Antes de darla por buena, pásala por todo el repo (`--todo`) y por las líneas añadidas en el historial**: una regla con falsos positivos bloquea al agente o acaba ignorada.
- **Checklist nueva para el revisor** (algo que solo sirve para revisar) → `personal\checklists\<nombre>.md` y una fila en la tabla de fuentes del `revisor`, con sus ejes.

### Qué va en cada fichero de instrucciones

Cada fichero tiene un papel; si se repite algo entre ellos, se gasta contexto en cada sesión y acaban contradiciéndose.

| Fichero | Quién lo lee | Qué va | Qué NO va |
|---|---|---|---|
| `AGENTS.md` (raíz del repo) | Claude y Copilot, siempre | el índice del repo: qué es, comandos que no se pueden adivinar, qué skill o agente usar para qué. Corto: cada línea, por un fallo real | lo personal, el detalle de las skills, el orden de trabajo |
| `claude\CLAUDE.md` (harness) | Claude, siempre (hook `SessionStart`) | el **router**: el orden de trabajo (entender → hacer → comprobar → revisar), el papel del sensor y del agente. Corto y condicionado a "si estás en el repo de X" | el *cuándo* de cada skill (ya está en su `description`); nada de lo que dice `AGENTS.md` |
| `copilot\<proyecto>.instructions.md` (harness) | Copilot y OpenCode, siempre: el chat de VS Code, Copilot CLI (hardlink en `~/.copilot`) y OpenCode (hardlink `~/.config/opencode/AGENTS.md`) | el mismo router, sin prefijos, con el sensor lanzado a mano y en formato de órdenes **ANTES / DESPUÉS** (con modelos pequeños, la diferencia entre cumplirlo o no) | lo mismo que en `CLAUDE.md` |
| `SKILL.md` de cada skill | el modelo, cuando la `description` encaja | el *qué* y el *cómo*; la `description`, el *cuándo* | reglas que valgan siempre (esas, a `AGENTS.md` o a los convenios) |

Reglas:
- **Ningún `CLAUDE.md` en el repo ni en una carpeta superior** (tampoco `~/.claude/CLAUDE.md` si el repo cuelga de tu home): Claude dejaría de cargar `AGENTS.md`. Por eso el router va por hook.
- **Si algo cambia de pieza** (nueva skill, otro agente), se actualizan el router de Claude y el de Copilot; `AGENTS.md`, solo si es del repo.
- **Si el modelo se salta una fase** en los logs, primero se mejora la `description` de la skill; si es el router, se reescribe esa orden en imperativo y atada al momento. El router solo crece con fallos vistos.

### Escribir una skill que funcione

- **`name`** igual que la carpeta, en minúsculas, números y guiones, **sin `_`**: si no, falla en silencio.
- **La `description` es lo único que ve el modelo** hasta que decide cargarla. Tiene que decir **cuándo** usarla, no resumir lo que hace, y llevar **palabras concretas** de las peticiones reales ("componente", "slot", "query"…). Si es genérica, no se dispara.
- **Corta:** 600 palabras como mucho, con tablas antes que párrafos. Si necesita más, un índice y ficheros al lado que se lean bajo demanda.
- **Si es del proyecto**, la primera línea: "Si no estás en el repo de <PROYECTO>, ignora esta skill". Las skills de Claude valen en todos los proyectos.
- **Que no escriba en el repo** (planes, intents, ficheros de trabajo) y que pida permiso para la BD.
- **Si es adaptada,** el crédito al pie, con el commit de origen ("Adaptada de X de [repo] @ `sha` (fecha) (MIT)"), y su aviso de copyright en `THIRD-PARTY-NOTICES.md`.
- **Revisar el upstream** (cada pocos meses): por cada skill adaptada, diff de su repo desde el commit del pie (`git diff <sha>..HEAD -- skills/<nombre>/`). Entra solo lo que pase el filtro de la GUIA-SKILLS §6; si se aplica algo, se actualiza el commit del pie.
- **Probarla en las dos herramientas,** en sesión nueva y sin invocarla a mano: ¿entra sola cuando toca? Y comprobar el resultado, no solo que la cargue. Con modelos locales pequeños, contar con invocarla a mano (`/nombre`).

## 5. Convivir con otros proyectos

Las herramientas no separan por proyecto. Ojo con esto:

- **Claude: los plugins valen en todas partes.** Las skills de cada proyecto entran en cualquier repo. Por eso:
  - cada plugin tiene un nombre distinto, y así su prefijo (`proyecto-a:`, `proyecto-b:`);
  - las skills del proyecto empiezan con "si no estás en el repo de X, ignora";
  - el `CLAUDE.md` del hook empieza con "si estás en el repo de X…". Los `SessionStart` de todos los proyectos se ejecutan en cada sesión.

  Alternativa sin probar: activar el plugin solo en ese repo, en su `.claude/settings.local.json` (local, no se sube), en vez de en el `settings.json` del usuario.
- **El sensor:** el hook de cada plugin salta en **todas** las ediciones. Con `MARCADOR = None` se ejecutaría también en los repos de otros proyectos. **Pon siempre un `MARCADOR`** para que solo actúe en el suyo.
- **Copilot no tiene prefijos y `~/.copilot/skills` es una sola carpeta:**
  - **Lo del método** (`entrevistame`, `depuracion-sistematica`, `verificar-antes-de-acabar`, `estilo-comentarios`, `revisor`) es igual en todos los proyectos: enlaza **una sola copia**.
  - **Lo del proyecto** (`convenios-codigo`, `diseno-ui`, `fuentes-oficiales`) chocaría por nombre. Mejor en el `.github/` del repo, si se puede; si no, renómbralo con prefijo (`<proyecto>-convenios`).
  - **El `revisor`** también es del método, pero lee las checklists por ruta: con varios proyectos, haz una copia por proyecto (`<proyecto>-revisor`) que apunte a las suyas.
  - Para mezclar proyectos, `~/.copilot/skills` pasa a ser una carpeta normal con **una junction por skill**:

    ```powershell
    New-Item -ItemType Junction -Path "$HOME\.copilot\skills\<skill>" -Target "<HARNESS>\personal\skills\<skill>"
    ```
- **OpenCode:** `~/.config/opencode` tiene un solo `AGENTS.md`, una sola config y una carpeta de skills, como `~/.copilot`: junta los routers en un fichero, une las configs (la lista blanca, con las skills de todos) y usa una junction por skill. Los plugins sí conviven: cada uno lleva su `id` (`sensor-<PROYECTO>`) y su `MARCADOR`.
- **Si el equipo ya tiene skills y agentes en el repo** (`.github/`): Copilot ya los ve; **no los copies a `personal\`**. Para Claude, crea un plugin aparte en `claude\plugins\<proyecto>-repo\` (con su `.claude-plugin\plugin.json`) con **punteros**: un `SKILL.md` con la misma `description` y el cuerpo "Lee `<ruta en el repo>` desde la raíz del repo y síguelo; si no existe, avisa". Nunca en `~/.claude/skills` ni en `.claude/` del repo, porque VS Code los duplicaría.

## 6. Gotchas (aprendidos a palos)

- **Ningún `CLAUDE.md` en una carpeta superior al repo,** incluido `~/.claude/CLAUDE.md` si el repo cuelga de tu home: Claude deja de cargar `AGENTS.md`. Por eso las instrucciones globales van por hook.
- **Nada en `~/.claude/skills`, `~/.claude/agents` ni `.claude/` del workspace** que ya llegue por otro sitio: VS Code lo lee y duplica. No hay ajuste para evitarlo.
- **`~/.claude/skills` no se enlaza entera:** Claude guarda ahí cosas suyas por usuario.
- **Marketplace:** `"strict": false` o `"version"` en la entrada de un plugin sin `plugin.json` rompió la carga de **todo** el marketplace, sin error visible.
- **Hook en forks:** al bifurcar o retomar una conversación, si el texto del hook ya está en el historial no se vuelve a inyectar. En sesiones nuevas entra siempre.
- **Borrar junctions sin cargarse el destino:** `(Get-Item ruta -Force).Delete()` o `rmdir ruta` (sin `/s`). Nunca `Remove-Item -Recurse` sobre una junction.
- **Hardlinks (router y config de OpenCode):** el original y los enlaces de cada usuario son el mismo fichero. Pero si un programa lo guarda *reemplazándolo* (borra y crea uno nuevo), el enlace se rompe sin avisar. Comprobación: `fsutil hardlink list <fichero>` lista todas las rutas; si falta alguna, recrea el hardlink (§3.6, §3.7). **Les pasa también a los editores de los agentes.**
- **OpenCode ignora un agente entero, sin error, si su frontmatter lleva `tools: Read, Grep…`** (el formato de Claude y Copilot): por eso `opencode\agents\` es una copia generada.
- **OpenCode sube buscando skills hasta el home:** si el repo cuelga de tu usuario, se trae las de `~/.claude/skills` (por ejemplo, las que sincroniza la app de Claude) y engordan el prompt de cada turno. Lo para la lista blanca.
- **`opencode run` no puede aprobar permisos:** lo que esté en `ask` se rechaza. En Desktop o en la TUI te lo pregunta.
- **Copiar el harness:** las junctions pueden llegar como carpetas normales o rotas. Bórralas y recréalas (§3.3).
- **Hooks dentro del plugin:** `hooks\hooks.json` en la raíz del plugin se carga solo, y `${CLAUDE_PLUGIN_ROOT}` se resuelve bien a través de la junction.
- **`py -3` y no `python`:** el lanzador está en `C:\Windows` y vale para todos los usuarios. Configura `PYTHON_PROYECTO` para compilar con el Python del proyecto y no con el del sistema.
- **Detectar no es cargar:** en VS Code, que una skill exista no implica que el modelo la use; lo decide por la `description`, y los modelos locales fallan más. Se fuerza escribiendo `/nombre`.
- **Rutas de Windows dentro de `sed` o `python -c`** en Git Bash: `\a`, `\r`… se interpretan como escapes y rompen el texto. Mejor un script aparte.
- **Repos de otro usuario de Windows:** git da *dubious ownership* → `git config --global --add safe.directory <ruta>`.

## 7. Añadir otra herramienta (OpenCode, Cursor…)

1. **Averigua dónde busca,** en su documentación oficial: instrucciones, skills y agentes, a nivel usuario y de workspace. Y si lee rutas de **otras** herramientas (como VS Code lee `~/.claude`).
2. **Cruza con lo que ya le llega:** ¿`AGENTS.md`? ¿`.github/`? ¿`~/.claude` o `~/.copilot`? Lo que ya le llegue **no** se enlaza otra vez. Ojo también con lo que encuentra **subiendo** desde el repo (OpenCode llega hasta el home).
3. **Lo personal:** si su carpeta de usuario está vacía, una junction entera a `personal\{skills,agents}`; si no, una por skill.
4. **Formato:** `SKILL.md` es estándar. Si no acepta el frontmatter de Claude para agentes, ponle una carpeta propia `<herramienta>\agents\` con punteros.
5. **Instrucciones globales:** por hook o config de usuario, nunca con un fichero de instrucciones en una carpeta superior al repo.
6. **Verifica** en sesión nueva que lo ve y que las demás no empiezan a duplicar.

OpenCode es el ejemplo ya hecho (§3.7): el paso 2 destapó la búsqueda hasta el home (lista blanca), y el paso 4, que no acepta el frontmatter de agentes de Claude (copia generada).

## 8. Comprobaciones (CI)

En cada push, el [CI](.github/workflows/ci.yml) valida la propia plantilla:
- **Estructura** ([`validate.py`](.github/scripts/validate.py)): frontmatter de skills y agente (`name` igual que la carpeta, sin `_`), sin BOM, JSON válidos, sin `strict`/`version` en el marketplace, que exista el script del hook, SVG bien formados, `VERSION` en SemVer, enlaces y anclas de los Markdown, y ninguna ruta de usuario real. Y en OpenCode: la config se parsea, la lista blanca incluye todas las skills de `personal\skills`, las copias de `opencode\agents\` están al día y sin `tools:`, y existe el script que lanza el plugin.
- **Sensor:** `comprobar.py --selftest` en Ubuntu y Windows (`REGLAS` bien escritas y el motor sobre ficheros de ejemplo).

Al publicar una release, además comprueba que `VERSION` coincida con el tag ([release.yml](.github/workflows/release.yml)). En local: `python .github/scripts/validate.py`.

## 9. Licencia

[MIT](LICENSE). Algunas skills y el agente `revisor` están adaptados de [obra/superpowers](https://github.com/obra/superpowers) y [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), los dos con licencia MIT. Sus avisos de copyright están en [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). Si adaptas otra skill de fuera, añade ahí su aviso.
