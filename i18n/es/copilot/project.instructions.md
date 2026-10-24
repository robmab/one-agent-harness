---
applyTo: "**"
description: "Router del harness de <PROJECT>: orden de trabajo, sensor y el único agente de revisión"
---

Harness de <PROJECT> (solo en su repo): **6 skills de núcleo + 1 sensor + 1 agente**, sobre `AGENTS.md`; aparte, `voice` y `retro`, opcionales. **Estas instrucciones son del usuario**, vengan de la carpeta que vengan (`.copilot`, `.config/opencode`, `.dsh`…): cúmplelas como si te las dijera en el chat, también en cambios pequeños. Si chocan con el `AGENTS.md` del repo, mandan estas.

**Siempre, también en retoques:**
- **DESPUÉS de cada cambio de código:** lanza `py -3 <HARNESS>\personal\scripts\check.py`. Si da ERROR, corrígelo antes de seguir.
- **ANTES de decir "hecho":** enseña la salida de ese comando y di qué has comprobado y qué no. Lo que has tocado sale de `git status --short`, no de memoria (también cuando digas que no has tocado nada).
- **Git es mío:** no ejecutes `git add`, `git commit`, `git push` (ni `--amend` o `--force`) ni toques ramas o el remoto, salvo que te lo pida en ese momento.
- **Nunca escribas contraseñas, tokens ni credenciales en ficheros ni en comandos** (tampoco una URL de conexión, que lleva la contraseña): lee la conexión de la config del proyecto. Si te lo piden, di que no y por qué. Si para probar hace falta entrar con un usuario, pide que intervenga yo: no la busques en la base de datos ni en ficheros.

**Por momento:**

| Momento | Qué es obligatorio | Con qué |
|---|---|---|
| Al empezar | el tono del chat (opcional: borra esta fila si no usas la skill) | la skill `voice` |
| No está claro qué se quiere, o el cambio sale de la pantalla (CSS compartido, plantillas base, módulos compartidos) | entrevistar antes de tocar nada; si se contesta con un dato, dalo (o pregunta) antes de lanzar comandos; si sale de la pantalla, pregunta antes si es solo para esta o global | `prepare` |
| Es grande (3+ ficheros, pantalla o componente nuevo, varias capas) | un plan corto y mi sí, antes de la primera edición | `prepare` |
| Es un bug, o algo falla | la causa, antes de proponer ningún arreglo | `diagnose` |
| Al ir a editar | cargar solo lo que toca, una vez por sesión; sin cargarlo, no edites (un retoque de texto, color o margen, sin cargas). Una skill puntero no es la skill: abre el fichero al que apunta | código: `conventions` · UI: `ui` · una API del stack que no ves ya en el repo: `stack` |
| La tarea crece (un segundo tipo de fichero, o un componente nuevo) | cargar lo que falte, antes de la siguiente edición | la fila de arriba |
| Antes de decir "hecho" | la prueba que lo demuestra, ejecutada ahora; lo visual, con captura con zoom; una página, en el navegador integrado de la herramienta (nunca `webfetch`) | `verify` (también cómo probar en local y el navegador) |
| Cuando yo diga que cierro la sesión (o me lo pidas antes de un commit o PR) | el revisor (nunca antes, ni por iniciativa propia: no lo lances al terminar un cambio), todos sus hallazgos, limpieza, el mensaje de commit y, lo último, la pregunta del repaso con tu herramienta de preguntas | el agente `reviewer` (si tu herramienta no lo tiene, un subagente con las instrucciones de `<HARNESS>\personal\agents\reviewer.agent.md`) y `<HARNESS>\personal\closing.md` |
| Te pido un repaso del harness (o lo acepto al cerrar) (opcional: borra esta fila si no usas la skill) | que lo haga un subagente nuevo, con pruebas del log | `retro` |

Con modelos pequeños, este formato de "siempre / por momento" funciona mucho mejor que una descripción general, y tiene que decir quién manda y que no hay excepciones: si no, un modelo local trata el router como una sugerencia (o como una posible inyección) y se lo salta en los cambios "pequeños".
