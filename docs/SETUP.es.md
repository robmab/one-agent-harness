# Montar un proyecto

🌐 [English](SETUP.md) · **Español**

Desde copiar la plantilla hasta comprobar que cada herramienta la ve; además, cómo convivir con otros proyectos y cómo hacerlo todo a mano.

Requisitos: Claude Code (usa Git Bash para los hooks en Windows), VS Code con Copilot, OpenCode 2 y DeepSeek Harness si los usas, y Python 3: el lanzador `py` en Windows, `python3` en Linux y macOS. Nada necesita admin. Los comandos de abajo son los de Windows; en Linux y macOS, `python3 <HARNESS>/setup.py` con las mismas opciones.

> **Linux y macOS:** `setup.py` enlaza con symlinks y escribe `python3` y rutas con `/` donde la plantilla tiene `py -3` y `\`. El CI lo prueba de punta a punta en los dos sistemas (con perfiles falsos), pero aún no se ha probado en una máquina real con las herramientas: si algo falla, [abre una issue](https://github.com/robmab/one-agent-harness/issues).

## 1. Copiar

```powershell
git clone <url-de-este-repo> '<HARNESS>'
Remove-Item '<HARNESS>\.git', '<HARNESS>\.github' -Recurse -Force
```

```bash
git clone <url-de-este-repo> <HARNESS> && rm -rf <HARNESS>/.git <HARNESS>/.github   # Linux y macOS
```

El `.git` se borra para que el harness del proyecto no quede atado a la plantilla, y `.github` porque solo tiene el CI de este repo. Más fácil todavía: descarga **Source code (zip)** de la [última release](https://github.com/robmab/one-agent-harness/releases/latest), que ya viene sin los dos. **No borres `VERSION`:** dice de qué versión de la plantilla sale el harness, y así más adelante puedes ver qué ha cambiado desde entonces (en las [releases](https://github.com/robmab/one-agent-harness/releases)). Si quieres versionarlo, haz después tu propio `git init`. Si ya tienes la plantilla en local, vale igual con `Copy-Item <plantilla> '<HARNESS>' -Recurse`, quitando también su `.git`.

**Ponlo donde quieras.** En Windows, **en el mismo disco que los perfiles de usuario** (normalmente `C:`): el router y la config de OpenCode se enlazan con hardlinks, que no cruzan de un disco a otro. En Linux y macOS todo son symlinks, así que en cualquier sitio. Tus repos pueden estar donde sea.

## 2. Lanzar setup.py

```powershell
py -3 <HARNESS>\setup.py --project "Mi Proyecto"
```

```bash
python3 <HARNESS>/setup.py --project "Mi Proyecto"   # Linux y macOS
```

Hace lo que antes eran cinco pasos a mano (están en el [anexo](#anexo-montaje-a-mano), para ver qué hace o repetir uno a mano):

- **Nombres:** `<PROJECT>` y `<HARNESS>` en todos los ficheros (sin BOM, y con `/` en JSON y TypeScript, donde una `\` sería un escape); el marketplace y el plugin (`harness-mi-proyecto`, `mi-proyecto`: el prefijo de las skills en Claude); el router, renombrado a `mi-proyecto.instructions.md`. En Linux y macOS, además, `python3` en vez de `py -3` y `/` en las rutas.
- **Idioma** (`--lang es`): lo que lee el modelo (skills, agente, router, `CLAUDE.md`, checklist, `AGENTS.template.md` y los mensajes del sensor) en español; los nombres (skills, agente, ficheros) quedan en inglés, así la documentación y las órdenes son las mismas en los dos idiomas. Por defecto, `en`. **Se elige una vez**, antes de rellenarlo: lo que escribas después es tuyo y no se puede traducir por ti.
- **Perfil** (`--profile web`): copia encima de la plantilla las skills rellenas del perfil, su checklist de seguridad y las `RULES` del sensor, antes de poner los nombres. Sin él, la plantilla limpia. **Se elige una vez**, como el idioma. Lo que un perfil no puede saber (las versiones, carpetas y comandos de tu stack) queda marcado con `TUNE`.
- **Enlaces,** por herramienta y usuario (junctions y hardlinks en Windows, symlinks en Linux y macOS): el enlace del plugin, el `settings.json` de Claude (marketplace, plugin y hook `SessionStart`), el `~/.copilot` de Copilot, el `~/.config/opencode` de OpenCode y el `~/.dsh` de DeepSeek Harness (su prompt de sistema va a mano, [A.6](#a6-conectar-deepseek-harness-en-cada-usuario-opcional)). Si una carpeta ya tiene otras cosas (skills de otro proyecto), enlaza skill a skill y deja lo demás como está; si hay un fichero en medio (otro router), para y te avisa ([convivir](#6-convivir-con-otros-proyectos)).
- **Lo demás:** las copias generadas del agente (`sync.py`), el `--selftest` del sensor y la lista de lo que queda por rellenar (`FILL-IN`) o por ajustar (`TUNE`).

| Opción | Para qué |
|---|---|
| `--tools claude,copilot` | solo algunas herramientas (por defecto: `claude,copilot,opencode,dsh`) |
| `--users rober,ana` | Windows: otros usuarios del PC (por defecto, tú); sus perfiles, en el disco del harness. En Linux y macOS, lánzalo como cada usuario (`sudo -u ana python3 <HARNESS>/setup.py`; ese usuario necesita poder escribir en la carpeta del harness) |
| `--lang es` | las piezas en español (solo la primera vez) |
| `--vscode-permissions` | VS Code lee el harness y lanza el sensor sin preguntar ([mantenerlo a punto](#5-mantenerlo-a-punto)) |
| `--dry-run` | dice lo que haría, sin tocar nada |
| `--force` | sustituye un fichero que estorba, con copia de seguridad antes |

Lo que monta queda apuntado en `.setup.json`, a su lado. Lanzarlo otra vez no rompe nada: lo que ya está bien, lo deja como está. Antes de cambiar un `settings.json` por primera vez guarda una copia al lado (`settings.json.before-harness`), y solo esa.

## 3. Rellenar

Para ver todo lo pendiente:

```powershell
Select-String -Path '<HARNESS>\*' -Pattern 'FILL-IN' -Recurse
```

Cada skill empieza con su **concepto** y deja sus apartados en `FILL-IN`. Para las de método (`prepare`, `diagnose`, `verify`, `stack`) puedes partir de su versión completa en [examples](../examples/README.es.md) y adaptarla.

Orden recomendado (de más a menos uso):

1. **`conventions`:** lo que más entra. Si el equipo ya tiene sus convenios en el repo, aquí solo un puntero.
2. **`stack`:** la tabla del stack con versiones reales y las trampas.
3. **`check.py`:**
   - `MARKER`: un fichero que solo exista en ese repo. **Obligatorio si convives con otros proyectos** ([convivir](#6-convivir-con-otros-proyectos)).
   - `PROJECT_PYTHON`, si hay Python.
   - `RULES`: las trampas del paso 2 que se puedan pillar con una regex. Después, `py -3 <HARNESS>\personal\scripts\check.py --selftest` comprueba que estén bien escritas.
4. **`verify`:** los comandos reales de tests, lint y build.
5. **`diagnose`:** las capas de la aplicación y sus trampas.
6. **`ui`:** si hay interfaz.
7. **`AGENTS.template.md`:** a la raíz del repo como `AGENTS.md`, si el repo es tuyo o el equipo está de acuerdo.


## 4. Verificar

1. **Claude**, en una **sesión nueva** desde el repo (no un fork): "¿qué skills y agentes tienes, te ha llegado el hook y tienes AGENTS.md?". Deben salir `<project>:*`, el texto de `CLAUDE.md` y `AGENTS.md`.
2. **El sensor:** con una regla de `RULES` ya puesta, pídele a Claude que escriba en un fichero de prueba del repo algo que la incumpla. Justo tras la edición le debe llegar el `ERROR`. Luego, borra el fichero.
3. **VS Code:** recarga la ventana. Deben salir las skills (`/prepare`…) y el agente `reviewer` en el selector, **una sola vez**.
4. **El router en VS Code:** paleta → "Chat: Configure Instructions" → debe salir `copilot-instructions` **una sola vez**. En un chat nuevo, "¿cuál es el único agente de revisión y en qué orden trabajas?" → `reviewer` y las fases.
5. **OpenCode**, desde el repo: `opencode run "sin tocar ficheros: cuál es el único agente de revisión, qué lanzas tras cada cambio y qué skills tienes"` → `reviewer`, el comando del sensor y **solo** las skills del harness. `opencode plugin list` → `sensor-<PROJECT>`. Para el sensor, la misma prueba que en Claude: el resultado de `write` debe traer el `ERROR`.
6. **DeepSeek Harness**, tras reiniciar la app, en una sesión nueva desde el repo: "sin tocar ficheros: cuál es el único agente de revisión, qué lanzas tras cada cambio, qué skills tienes y qué tienes que hacer antes de la primera edición de código" → el `reviewer` (o un subagente con sus instrucciones), el comando del sensor, las skills del harness y cargar `conventions`.

## 5. Mantenerlo a punto

- **`py -3 <HARNESS>\setup.py --check`** revisa todos los enlaces y ajustes y repara lo que es seguro reparar: un enlace que falta, un hardlink que ha roto un editor al guardar sustituyendo el fichero (si el texto sigue siendo el mismo) o una copia del agente desfasada. Si la copia de fuera tiene otro texto, no elige por ti: te dice cuál es más reciente.
- **Otro usuario u otra herramienta más tarde:** `setup.py --users ana` o `setup.py --tools dsh`.
- **Las confirmaciones de VS Code** (`--vscode-permissions`): el harness está fuera del workspace, así que Copilot pide confirmación cada vez que lee algo de él (en uso real, unas diez por sesión) y cuando el sensor va encadenado a otro comando. La opción añade dos ajustes al `settings.json` de VS Code de cada usuario: `github.copilot.chat.additionalReadAccessPaths` con la carpeta del harness, y una regla de `chat.tools.terminal.autoApprove` solo para el script del sensor. Recarga la ventana después. Solo se confía en **leer** el harness, no en cambiarlo: que un modelo reescriba sus propias reglas es algo que tienes que ver. No uses `chat.tools.global.autoApprove` (aprobar todo): quitaría también las confirmaciones que te protegen (base de datos, borrados, push).
- **`setup.py --uninstall`** (`--tools` y `--users` lo acotan): quita los enlaces y ajustes, solo los que apuntan a este harness. El harness se queda como está.

## 6. Convivir con otros proyectos

Las herramientas no separan por proyecto. Ojo con esto:

- **Claude: los plugins valen en todas partes.** Las skills de cada proyecto entran en cualquier repo. Por eso:
  - cada plugin tiene un nombre distinto, y así su prefijo (`proyecto-a:`, `proyecto-b:`);
  - las skills del proyecto empiezan con "si no estás en el repo de X, ignora";
  - el `CLAUDE.md` del hook empieza con "si estás en el repo de X…". Los `SessionStart` de todos los proyectos se ejecutan en cada sesión.

  Alternativa sin probar: activar el plugin solo en ese repo, en su `.claude/settings.local.json` (local, no se sube), en vez de en el `settings.json` del usuario.
- **El sensor:** el hook de cada plugin salta en **todas** las ediciones. Con `MARKER = None` se ejecutaría también en los repos de otros proyectos. **Pon siempre un `MARKER`** para que solo actúe en el suyo.
- **Copilot no tiene prefijos y `~/.copilot/skills` es una sola carpeta:**
  - **Lo del método** (`prepare`, `diagnose`, `verify`, `voice`, `retro`, `reviewer`) es igual en todos los proyectos: enlaza **una sola copia**.
  - **Lo del proyecto** (`conventions`, `ui`, `stack`) chocaría por nombre. Mejor en el `.github/` del repo, si se puede; si no, renómbralo con prefijo (`<project>-conventions`).
  - **El `reviewer`** también es del método, pero lee las checklists por ruta: con varios proyectos, haz una copia por proyecto (`<project>-reviewer`) que apunte a las suyas.
  - Para mezclar proyectos, `~/.copilot/skills` pasa a ser una carpeta normal con **una junction por skill**:

    ```powershell
    New-Item -ItemType Junction -Path "$HOME\.copilot\skills\<skill>" -Target "<HARNESS>\personal\skills\<skill>"
    ```
- **OpenCode:** `~/.config/opencode` tiene un solo `AGENTS.md`, una sola config y una carpeta de skills, como `~/.copilot`: junta los routers en un fichero, une las configs (la lista blanca, con las skills de todos) y usa una junction por skill. Los plugins sí conviven: cada uno lleva su `id` (`sensor-<PROJECT>`) y su `MARKER`.
- **DeepSeek Harness:** `~/.dsh` tiene un solo `AGENTS.md` y una carpeta de skills, como `~/.copilot`: junta los routers y usa una junction por skill. El `suffix` del preset también es un solo texto: pon ahí el de cada proyecto, cada parte empezando por "En el repo de X".
- **Si el equipo ya tiene skills y agentes en el repo** (`.github/`): Copilot ya los ve; **no los copies a `personal\`**. Para Claude, crea un plugin aparte en `claude\plugins\<project>-repo\` (con su `.claude-plugin\plugin.json`) con **punteros**: un `SKILL.md` con la misma `description` y el cuerpo "Lee `<ruta en el repo>` desde la raíz del repo y síguelo; si no existe, avisa". Nunca en `~/.claude/skills` ni en `.claude/` del repo, porque VS Code los duplicaría.

## Anexo: montaje a mano

Lo que hace `setup.py`, paso a paso: para entenderlo o para repetir un paso a mano. Está escrito para Windows; en Linux y macOS, symlinks (`ln -s`) en vez de junctions y hardlinks, `python3` en vez de `py -3`, y `/` en las rutas. El orden: A.1 y A.2 una vez, de A.3 a A.5 en cada usuario.

### A.1 Poner nombre

1. **Marketplace y plugin** (`claude\.claude-plugin\marketplace.json`): `harness-project` → `harness-<project>` y `project` → `<project>`, en minúsculas y con guiones.
   - El nombre del plugin es el **prefijo de las skills en Claude** (`<project>:conventions`), así que tiene que ser distinto en cada proyecto.
   - **No pongas `"strict"` ni `"version"`** en esa entrada ([gotchas](DAY-TO-DAY.es.md#4-gotchas-aprendidos-a-palos)).
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

**Opcional: que no pida permiso para el harness** (lo que hace `--vscode-permissions`, [mantenerlo a punto](#5-mantenerlo-a-punto)). En el `settings.json` de VS Code de cada usuario (`%APPDATA%\Code\User\settings.json`), por ejemplo con `<HARNESS>` = `C:\Harness\Proyecto` (en JSON cada `\` va doble, y dentro de la regex se vuelve a doblar):

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
- **El guard** es el plugin `opencode\plugins\guard.ts`: antes de cada orden, escritura, subagente o pregunta pasa `guard.py --hook` con el id de la sesión, así lee los mensajes del usuario de la base de datos de OpenCode y funciona como en Claude: credenciales, y el revisor o la pregunta del repaso antes del cierre. Una orden o un subagente bloqueados solo enseñan el aviso; una escritura falla con él. Cada ruta de `FORBIDDEN_PATHS` va además en la config como regla `edit` → `deny`.
- **La lista blanca de skills** (`permissions`, acción `skill`) deja ver solo las del harness: OpenCode sube desde el repo hasta el home buscando `.claude/skills` y `.agents/skills`, y se trae las de otras herramientas. **Cada skill nueva, a la lista** (la CI lo comprueba).
- **Búsqueda web gratis:** el MCP `ddg-search` (DuckDuckGo, por `uvx`; instala `uv` en cada usuario con `winget install astral-sh.uv`). Buscar no pregunta; **leer páginas sí**, porque una web puede esconder instrucciones para el modelo. Añade a las reglas `allow` de `webfetch` la documentación oficial de tu stack.
- **Con un modelo local** de un solo slot (llama.cpp con `parallel = 1`): el agente `title` va desactivado, porque su petición echaba la caché del turno principal en cada sesión nueva (14-22 s medidos).

### A.6 Conectar DeepSeek Harness (en cada usuario, opcional)

Para la app DeepSeek Harness (DSH). Lee el `~/.dsh/AGENTS.md` global y las skills de `~/.dsh/skills\<skill>\SKILL.md` (un solo nivel), además del `AGENTS.md` del repo.

```powershell
$a = '<HARNESS>'
$d = "C:\Users\$u\.dsh"
New-Item -ItemType HardLink -Path "$d\AGENTS.md" -Target "$a\copilot\<project>.instructions.md"   # el mismo router que Copilot
New-Item -ItemType Junction -Path "$d\skills"    -Target "$a\personal\skills"   # si ya tiene otras: una junction por skill
```

- **La autoridad del router (a mano):** DSH pasa `~/.dsh/AGENTS.md` dentro de un recordatorio que lo llama "guía cuando aplique". El texto de `dsh\system-prompt.md` la sube desde el prompt de sistema, pero tiene que ir en el **preset del agente**: cada preset (`standard` es el de por defecto) monta su propio `persona`, que tapa el `personaSuffix` global de la fila `system-prompt`, y un patch sustituye la config entera (no la mezcla). Así que, en `~/.dsh/profiles/desktop/cordis.patch.yml`:
  1. Saca el preset de la app: copia la carpeta del perfil a un `DSH_HOME` de pruebas (el perfil `desktop` lo gestiona la app) y lanza `dsh --profile <copia> --dump-default-config`.
  2. Pega su entrada `- id: preset-standard` entera en `cordis.patch.yml` y añade, bajo el `prefix` de su fila `persona`, un `suffix: >-` con el texto de `dsh\system-prompt.md` (sin su comentario).
  3. Compruébalo con `--dump-config` sobre la copia (sin errores `dsh:` y con el `suffix` dentro de `preset-standard`), reinicia la app y, en una sesión nueva, mira que el prompt de sistema lo lleva: `read_session.py dsh --summary` lo dice.

  Cuando la app se actualice, vuelve a comparar el preset con `--dump-default-config`: la copia no lo sigue.
- **Servidores MCP** (tu Chrome, por ejemplo, si el router lee de ahí el gestor de incidencias): una fila nueva va dentro de una lista `- insert:` de `cordis.patch.yml` (una fila suelta con `id` solo modifica una que ya exista): `id: mcp-<nombre>`, `name: '@deepseek-ai/dsh-mcp-client'` y, en `config`, `serverName`, `transport: stdio`, `command` y `args`, con la versión fijada. Compruébalo con `--dump-config` como en el paso 3.
- **El `reviewer`:** DSH no tiene ficheros de agente (los define con presets), así que la fila de cierre del router manda lanzar un subagente con las instrucciones de `personal\agents\reviewer.agent.md`.
- **El sensor:** sin hook, como en Copilot (hay un plugin que ejecuta el `hooks.json` de Claude, pero es experimental): el router manda lanzar `check.py` tras cada cambio.
- **Sus logs** (`~/.dsh/sessions`, en zstd) los lee `read_session.py dsh` para el repaso; hace falta Python 3.14.
