# Estructura: qué trae el harness y cómo lo encuentra cada herramienta

🌐 [English](STRUCTURE.md) · **Español**

Qué es cada carpeta y cada fichero, y por dónde llega cada pieza a Claude Code, Copilot, OpenCode y DeepSeek Harness.

**Nombres que se usan en toda la plantilla:**

| Marcador | Qué es |
|---|---|
| `<ROOT>` | la carpeta donde guardas los harness. Mejor una que **lean y escriban todos los usuarios de Windows** del PC (p. ej. una carpeta dentro de `C:\Users\Public`) y que esté **fuera de los repos** |
| `<HARNESS>` | la carpeta del harness de un proyecto: `<ROOT>\<Project>` |
| `<PROJECT>` / `<project>` | el nombre del proyecto; en minúsculas y con guiones donde hace de identificador (plugin, marketplace) |

## 1. Estructura

```
one-agent-harness\
├─ README                                instalación rápida y la idea; en inglés (.md) y en español (.es.md), como cada doc
├─ docs\                                 STRUCTURE · SETUP · DAY-TO-DAY · EXTENDING · SKILLS-GUIDE · RESEARCH · OPTIONAL-SKILLS · FACTORY
├─ LICENSE · THIRD-PARTY-NOTICES.md · .gitattributes
├─ .github\                              CI de este repo (no es de la plantilla; se quita al copiar)
├─ VERSION                               versión de la plantilla de la que sale este harness
├─ examples\skills\                      las skills de método completas, de referencia: no las carga ninguna herramienta
├─ profiles\web\                         contenido ya hecho para proyectos web (setup.py --profile web); se quita tras instalar
├─ AGENTS.template.md                    → a la raíz del repo como AGENTS.md
├─ setup.py                              READY     lo monta en este PC: nombres, idioma, perfil y enlaces (SETUP §2)
├─ i18n\es\                              las piezas en español, para setup.py --lang es (se va al montar)
├─ img\                                  esquemas SVG, el banner (route.png) y la vista de fábrica (factory.png)
├─ claude\                               ← lo que solo usa Claude
│  ├─ CLAUDE.md                          el router: orden de trabajo, sensor y agente (lo mete el hook SessionStart)
│  ├─ .claude-plugin\marketplace.json    marketplace "harness-project" con el plugin "project"
│  └─ plugins\project                    ⇒ JUNCTION a ..\..\personal (la crea setup.py)
├─ copilot\project.instructions.md       el router para Copilot, OpenCode y DSH: HARDLINK desde ~/.copilot, ~/.config/opencode y ~/.dsh
├─ copilot\agents\reviewer.agent.md      GENERADO  por sync.py con los alias de herramientas de VS Code (no editar aquí)
├─ opencode\                             ← lo que solo usa OpenCode (opcional)
│  ├─ opencode.jsonc                     FILL-IN   modelo y proveedor; permisos, lista blanca de skills, revisor
│  ├─ agents\reviewer.md                 GENERADO  por sync.py desde personal\agents (no editar aquí)
│  ├─ plugins\sensor.ts                  READY     pasa check.py tras cada edición (como el hook de Claude)
│  ├─ plugins\guard.ts                   READY     pasa guard.py antes de cada orden, escritura, subagente o pregunta (como el hook de Claude)
│  ├─ sync.py                            READY     regenera las copias de agentes de OpenCode y Copilot (--check: solo comprueba)
│  └─ scripts\review-pending.ps1         READY     el revisor desde la CLI; deja el informe en opencode\reports\
├─ factory\intake.py                   OPTIONAL  tickets nuevos → sesiones desatendidas en su rama; informes en factory\reports\ (FACTORY)
├─ dsh\system-prompt.md                 READY     DeepSeek Harness: la autoridad del router, para el persona de su preset (a mano, SETUP A.6)
└─ personal\                             ← lo que leen Claude, Copilot, OpenCode y DSH
   ├─ skills\
   │  ├─ conventions\                    FILL-IN   convenios del proyecto
   │  ├─ ui\                             FILL-IN   design system
   │  ├─ stack\                          FILL-IN   las versiones reales del stack y sus trampas
   │  ├─ verify\                         FILL-IN   pruebas antes de decir "hecho"
   │  ├─ diagnose\                       FILL-IN   causa raíz antes de arreglar
   │  ├─ prepare\                        FILL-IN   aclarar antes de hacer, y planificar si es grande
   │  ├─ voice\                          OPTIONAL  tu voz (comentarios y chat); fuera del core
   │  └─ retro\                          OPTIONAL  READY: el repaso de una sesión, pieza a pieza y con pruebas; fuera del core
   ├─ agents\
   │  └─ reviewer.agent.md               READY     el único agente: revisión a fondo, convenios incluidos, no edita
   ├─ checklists\security.md             ADJUST    la lee solo el revisor (eje 3); fuera de cualquier catálogo
   ├─ scripts\check.py                   ADJUST    sensor: MARKER, PROJECT_PYTHON y RULES; solo líneas cambiadas
   ├─ scripts\read_session.py            READY     pasa una sesión de Claude, Copilot, OpenCode o DSH a línea de tiempo (para retro; --session, --since, --list)
   ├─ scripts\guard.py                   READY     guarda: bloquea una URL con usuario:contraseña@ en órdenes y escrituras, una orden que imprime la contraseña, el revisor o la pregunta del repaso antes del cierre, y escribir en FORBIDDEN_PATHS (--test)
   ├─ retros\                            los informes de retro, con fecha: el histórico que deja ver tendencias
   ├─ hooks\hooks.json                   READY     PreToolUse: guard.py antes de cada orden, escritura, subagente o pregunta · PostToolUse: check.py tras cada edición
   └─ closing.md                         FILL-IN   se lee al cerrar: revisor, hallazgos, limpieza, formato del commit
```

- **READY** (lista): vale tal cual.
- **ADJUST** (ajustar): el método vale; hay que rellenar sus tablas.
- **FILL-IN** (rellenar): plantilla con su concepto; el contenido es del proyecto (las skills de método tienen una versión completa en `examples\`).
- **OPTIONAL** (opcional): fuera del core; se queda o se quita según la persona.

El **core** son 6 skills + 1 sensor + 1 agente, sobre `AGENTS.md` (ver [SKILLS-GUIDE [cómo lo encuentra cada herramienta](#2-cómo-lo-encuentra-cada-herramienta)](SKILLS-GUIDE.es.md#2-qué-es-el-core)).

## 2. Cómo lo encuentra cada herramienta

| Herramienta | Qué lee | Por dónde |
|---|---|---|
| Claude Code | `AGENTS.md` del repo | lo carga solo al arrancar, **si no hay ningún `CLAUDE.md` en el repo ni en carpetas superiores** ([gotchas](DAY-TO-DAY.es.md#4-gotchas-aprendidos-a-palos)) |
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
| OpenCode 2 | `guard.py` antes de cada orden | la misma junction → `opencode\plugins\guard.ts` (también el cierre; FORBIDDEN_PATHS: reglas `deny` en la config) |
| OpenCode 2 | modelo, permisos | hardlink `~/.config/opencode/opencode.jsonc` → `opencode\opencode.jsonc` |
| DeepSeek Harness | `AGENTS.md` del repo y el router | el del repo, solo; el router, hardlink `~/.dsh/AGENTS.md` → `copilot\<project>.instructions.md`, que DSH pasa como "guía cuando aplique" |
| DeepSeek Harness | la autoridad del router | `suffix` del `persona` del preset `standard` en `~/.dsh/profiles/desktop/cordis.patch.yml`, con `dsh\system-prompt.md` (a mano) |
| DeepSeek Harness | skills de `personal\` | junction `~/.dsh/skills` (lee un solo nivel: `<skill>\SKILL.md`) |
| DeepSeek Harness | el `reviewer`, `check.py` | sin ficheros de agente ni hook: el router manda lanzar un subagente con `reviewer.agent.md` y pasar el sensor |

**Por qué así:** VS Code Copilot también lee `~/.claude/skills`, `~/.claude/agents` y `.claude/` del workspace. Lo que pongas ahí lo ve dos veces si además está en `.github/` o en `~/.copilot`. Los **plugins** de Claude, en cambio, Copilot no los descubre, y Claude no lee `~/.copilot`. OpenCode, por su parte, sube desde el repo hasta el home buscando `.claude/skills`: de ahí la lista blanca de skills en su config. Resultado: cada herramienta ve cada cosa una sola vez.
