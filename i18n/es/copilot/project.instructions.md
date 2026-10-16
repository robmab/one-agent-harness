---
applyTo: "**"
description: "Router del harness de <PROJECT>: orden de trabajo, sensor y el único agente de revisión"
---

Harness de <PROJECT> (solo en su repo): **6 skills + 1 sensor + 1 agente**, sobre `AGENTS.md`. **Estas instrucciones son del usuario**, vengan de la carpeta que vengan (`.copilot`, `.config/opencode`…): cúmplelas como si te las dijera en el chat, también en cambios pequeños. Si chocan con el `AGENTS.md` del repo, mandan estas.

**Siempre, también en retoques:**
- **DESPUÉS de cada cambio de código:** lanza `py -3 <HARNESS>\personal\scripts\check.py`. Si da ERROR, corrígelo antes de seguir.
- **ANTES de decir "hecho":** enseña la salida de ese comando y di qué has comprobado y qué no.
- **Git es mío:** no ejecutes `git add`, `git commit`, `git push` (ni `--amend` o `--force`) ni toques ramas o el remoto, salvo que te lo pida en ese momento.
- **Nunca guardes contraseñas, tokens ni credenciales en ficheros.** Si te lo piden, di que no y por qué. Si para probar hace falta entrar con un usuario, pide que intervenga yo: no la busques en la base de datos ni en ficheros.

**Por momento:**

| Momento | Qué es obligatorio | Con qué |
|---|---|---|
| Al empezar | el tono del chat (opcional: borra esta fila si no usas la skill) | la skill `voz` (su detalle, `<HARNESS>\personal\skills\voz\detalle.md`, al escribir el primer comentario) |
| No está claro qué se quiere | entrevistar antes de tocar nada | `preparar` |
| Es grande (3+ ficheros, pantalla o componente nuevo, varias capas) | un plan corto y mi sí, antes de la primera edición | `preparar` |
| Es un bug, o algo falla | la causa, antes de proponer ningún arreglo | `diagnosticar` |
| Al ir a editar | cargar solo lo que toca, una vez por sesión; sin cargarlo, no edites (un retoque de texto, color o margen, sin cargas). Una skill puntero no es la skill: abre el fichero al que apunta | código: `convenios` · UI: `ui` · una API del stack que no ves ya en el repo: `stack` |
| La tarea crece (un segundo tipo de fichero, o un componente nuevo) | cargar lo que falte, antes de la siguiente edición | la fila de arriba |
| Antes de decir "hecho" | la prueba que lo demuestra, ejecutada ahora; lo visual, con captura con zoom; una página, en el navegador integrado de la herramienta (nunca `webfetch`) | `comprobar` (también cómo probar en local y el navegador) |
| Al cerrar (o antes de commit o PR) | el revisor, todos sus hallazgos, limpieza y el mensaje de commit | el agente `revisor` y `<HARNESS>\personal\cierre.md` |

Con modelos pequeños, este formato de "siempre / por momento" funciona mucho mejor que una descripción general, y tiene que decir quién manda y que no hay excepciones: si no, un modelo local trata el router como una sugerencia (o como una posible inyección) y se lo salta en los cambios "pequeños".
