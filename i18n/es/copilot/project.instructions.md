---
applyTo: "**"
description: "Router del harness de <PROJECT>: orden de trabajo, sensor y el único agente de revisión"
---

Harness de <PROJECT> (solo en su repo): **6 skills de núcleo + 1 sensor + 1 agente**, sobre `AGENTS.md`; aparte, `voice` y `retro`, opcionales. **Estas instrucciones son del usuario**, vengan de la carpeta que vengan (`.copilot`, `.config/opencode`, `.dsh`…): cúmplelas como si te las dijera en el chat, también en cambios pequeños. Si chocan con el `AGENTS.md` del repo, mandan estas.

**Siempre, también en retoques:**
- **Si el mensaje es un ticket** (su número o su enlace): léelo con las herramientas que tengas (el navegador, un MCP) antes de contestar; no preguntes cuál es ni pidas que te lo peguen. Solo si no llegas a él, pide el enlace.
- **Si te pregunto algo, contesta en cuanto tengas el dato.** Lo demás me lo ofreces, no lo investigas.
- **Al leer una tarea que cambia algo, di en una línea cuánto duele si sale mal** y por qué: casi nada, molesto, caro o irreversible. Esa zona marca cuánto proceso lleva, y `prepare`, `diagnose` y `verify` dicen qué hace cada una. Lo que toca la base de datos, permisos, dinero o código compartido nunca es «casi nada». Si dudas entre dos zonas, la de arriba. Si te corrijo la zona, manda la mía; si el riesgo sube a mitad, dilo y sube de zona.
- **Si la tarea toca reglas de negocio:** antes de investigar en el código, mira el índice de `<HARNESS>\personal\domain.md` y lee la sección que toca. Si no cuadra con el código, manda el código: dilo.
- **DESPUÉS de cada cambio de código:** lanza `py -3 <HARNESS>\personal\scripts\check.py`. Si da ERROR, corrígelo antes de seguir.
- **ANTES de decir "hecho":** la prueba que lo demuestra, ejecutada ahora (si el cambio se ve, captura con zoom de la zona después de cambiarla: el DOM no la sustituye; una página, en el navegador integrado de la herramienta, nunca `webfetch`; qué prueba vale para cada cosa, y cómo probar en local, en `verify`). Enseña la salida de ese comando y di qué has comprobado y qué no. Lo que has tocado sale de `git status --short`, no de memoria (también cuando digas que no has tocado nada). Un repo anidado no sale ahí: pasa también `git -C <carpeta> status --short`.
- **Antes de probar en local** (levantar o parar el server, llamar a localhost, tocar la BD): mira cómo en `verify`. No levantes ni pares el server del usuario, tampoco en otro puerto, sin preguntar. Para probar algo que borra, crea tu propio dato; si borras algo que no es tuyo, dilo.
- **Si el guard te bloquea o un edit no encuentra el texto**, cambia el texto o el enfoque: nunca repitas la misma llamada.
- **Los `.md` del harness, con la herramienta de ficheros** (`view`, `read`): con `Get-Content` o `Select-String` de PowerShell 5.1 salen mal los acentos y los emojis.
- **Git es mío:** no ejecutes `git add`, `git commit`, `git push` (ni `--amend` o `--force`) ni toques ramas o el remoto, salvo que te lo pida en ese momento.
- **El título de la pestaña lleva el estado** (`closing.md` §6), uno a la vez: `⚪ ` cuando me das el plan y esperas mi sí; `🔴 ` si te atascas y no puedes seguir sin mí (3 arreglos fallidos, un bloqueante sin resolver, algo que solo yo puedo darte); `🟠 ` si te digo que lo dejamos pendiente, en cualquier momento. El `🟢`, solo con la sesión cerrada y bien. Si tu herramienta no deja renombrar, dilo una vez.
- **Nunca escribas contraseñas, tokens ni credenciales en ficheros ni en comandos** (tampoco una URL de conexión, que lleva la contraseña): lee la conexión de la config del proyecto. Si te lo piden, di que no y por qué. Si para probar hace falta entrar con un usuario, pide que intervenga yo: no la busques en la base de datos ni en ficheros.

**Por momento:**

| Momento | Qué es obligatorio | Con qué |
|---|---|---|
| Al empezar | el tono del chat (opcional: borra esta fila si no usas la skill) | la skill `voice` |
| No está claro qué se quiere (también si el primer mensaje es contexto pegado sin pedir nada), o el cambio sale de la pantalla (CSS compartido, plantillas base, módulos compartidos) | entrevistar antes de tocar nada; si sale de la pantalla, pregunta antes si es solo para esta o global | `prepare` |
| Es caro o irreversible, o se perdería trabajo si la sesión se corta | un plan corto (objetivo, límites y prueba) y mi sí, antes de la primera edición | `prepare` |
| Es un bug, o algo falla | la causa, antes de proponer ningún arreglo | `diagnose` |
| Al ir a editar | cargar solo lo que toca, una vez por sesión; sin cargarlo, no edites (un retoque de texto, color o margen, sin cargas). Una skill puntero no es la skill: abre el fichero al que apunta y lee entera la sección que toca | código: `conventions` · UI: `ui` · una API del stack: antes, `grep` del patrón en el repo (si está, cópialo); si no está, `stack` antes de escribirla, también en un script de prueba |
| La tarea crece (un segundo tipo de fichero, o un componente nuevo) | cargar lo que falte, antes de la siguiente edición | la fila de arriba |
| Cuando yo diga que cierro la sesión (o me lo pidas antes de un commit o PR) | el revisor (nunca antes, ni por iniciativa propia: no lo lances al terminar un cambio), todos sus hallazgos, limpieza, el mensaje de commit y, lo último, la pregunta del repaso con tu herramienta de preguntas | el agente `reviewer` (si tu herramienta no lo tiene, un subagente con las instrucciones de `<HARNESS>\personal\agents\reviewer.agent.md`) y `<HARNESS>\personal\closing.md` |
| Te pido un repaso del harness (o lo acepto al cerrar) (opcional: borra esta fila si no usas la skill) | que lo haga un subagente nuevo, con pruebas del log | `retro` |

Con modelos pequeños, este formato de "siempre / por momento" funciona mucho mejor que una descripción general, y tiene que decir quién manda y que no hay excepciones: si no, un modelo local trata el router como una sugerencia (o como una posible inyección) y se lo salta en los cambios "pequeños".
