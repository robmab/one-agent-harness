# Ampliar: otra herramienta y las comprobaciones

🌐 [English](EXTENDING.md) · **Español**

Cómo añadir una herramienta que el harness aún no cubre, y qué comprueba el CI en cada push.

## 1. Añadir otra herramienta (OpenCode, Cursor…)

1. **Averigua dónde busca,** en su documentación oficial: instrucciones, skills y agentes, a nivel usuario y de workspace. Y si lee rutas de **otras** herramientas (como VS Code lee `~/.claude`).
2. **Cruza con lo que ya le llega:** ¿`AGENTS.md`? ¿`.github/`? ¿`~/.claude` o `~/.copilot`? Lo que ya le llegue **no** se enlaza otra vez. Ojo también con lo que encuentra **subiendo** desde el repo (OpenCode llega hasta el home).
3. **Lo personal:** si su carpeta de usuario está vacía, una junction entera a `personal\{skills,agents}`; si no, una por skill.
4. **Formato:** `SKILL.md` es estándar. Si no acepta el frontmatter de Claude para agentes, ponle una carpeta propia `<herramienta>\agents\` con punteros.
5. **Instrucciones globales:** por hook o config de usuario, nunca con un fichero de instrucciones en una carpeta superior al repo.
6. **Verifica** en sesión nueva que lo ve y que las demás no empiezan a duplicar.

OpenCode es el ejemplo ya hecho ([A.5](SETUP.es.md#a5-conectar-opencode-en-cada-usuario-opcional)): el paso 2 destapó la búsqueda hasta el home (lista blanca), y el paso 4, que no acepta el frontmatter de agentes de Claude (copia generada).

## 2. Comprobaciones (CI)

En cada push, el [CI](../.github/workflows/ci.yml) valida la propia plantilla:
- **Estructura** ([`validate.py`](../.github/scripts/validate.py)): frontmatter de skills y agente (cada skill con un `Use when` en su descripción y una línea `**CONCEPT:**`; `name` igual que la carpeta, sin `_`; el agente original con los nombres de herramienta de Claude), sin BOM, JSON válidos, sin `strict`/`version` en el marketplace, que exista el script del hook, SVG bien formados, `VERSION` en SemVer, enlaces y anclas de los Markdown, y ninguna ruta de usuario real. Y en OpenCode: la config se parsea, la lista blanca incluye todas las skills de `personal\skills`, las copias generadas del agente están al día (la de OpenCode sin `tools:`, la de Copilot con los nombres de VS Code), y existe el script que lanza el plugin. Y las traducciones de `i18n\`: una por cada pieza que lee el modelo, con las mismas líneas y encabezados que la inglesa (así un cambio en una se nota en la otra), y los nombres que reciben tras `setup.py`.
- **Sensor:** `check.py --selftest` en Ubuntu y Windows (`RULES` bien escritas y el motor sobre ficheros de ejemplo), en los dos idiomas.
- **`setup.py`** ([`test_setup.py`](../.github/scripts/test_setup.py), en Windows, Linux y macOS): sobre una copia temporal y perfiles falsos, uno de ellos ya en uso, en cada idioma: instalar, volver a lanzarlo sin cambios, `--check` reparando un hardlink roto y una junction que falta (y sin tocar una copia con otro texto), y `--uninstall` dejando los perfiles como estaban.

Al publicar una release, además comprueba que `VERSION` coincida con el tag ([release.yml](../.github/workflows/release.yml)). En local: `python .github/scripts/validate.py`.
