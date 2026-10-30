Harness de <PROJECT> (solo en su repo): **6 skills de núcleo + 1 sensor + 1 agente**, sobre `AGENTS.md`; aparte, `voice` y `retro`, opcionales.

**Siempre, también en retoques:**
- **Si el mensaje es un ticket** (su número o su enlace): léelo con las herramientas que tengas (el navegador, un MCP) antes de contestar; no preguntes cuál es ni pidas que te lo peguen. Solo si no llegas a él, pide el enlace.
- **Si el usuario pregunta algo, contesta en cuanto tengas el dato.** Lo demás se lo ofreces, no lo investigas.
- **Tras cada edición** salta el sensor (`check`) por el hook y deja una línea (`OK`, avisos o ERROR). Si da ERROR, se corrige antes de seguir. No lo relances a mano: para enseñarlo, basta con su última salida.
- **Antes de decir "hecho"**, la prueba que lo demuestra, ejecutada ahora (si el cambio se ve, captura con zoom de la zona después de cambiarla: el DOM no la sustituye; qué prueba vale para cada cosa, y cómo probar en local, en `project:verify`), y qué has comprobado y qué no. Lo que has tocado sale de `git status --short`, no de memoria (también cuando digas que no has tocado nada). Un repo anidado no sale ahí: pasa también `git -C <carpeta> status --short`.
- **Antes de probar en local** (levantar o parar el server, llamar a localhost, tocar la BD): mira cómo en `project:verify`. No levantes ni pares el server del usuario, tampoco en otro puerto, sin preguntar. Para probar algo que borra, crea tu propio dato; si borras algo que no es tuyo, dilo.
- **Si el guard te bloquea o un edit no encuentra el texto**, cambia el texto o el enfoque: nunca repitas la misma llamada.
- **Git es del usuario:** nada de `git add`, `commit`, `push` (ni `--amend` o `--force`) ni tocar ramas, salvo que te lo pida en ese momento.
- **El título de la pestaña lleva el estado** (`closing.md` §6), uno a la vez: `⚪ ` cuando das el plan y esperas el sí del usuario; `🔴 ` si te atascas y no puedes seguir sin el usuario (3 arreglos fallidos, un bloqueante sin resolver, algo que solo el usuario puede darte); `🟠 ` si dice que lo deja pendiente, en cualquier momento. El `🟢`, solo con la sesión cerrada y bien. Si tu herramienta no deja renombrar, dilo una vez.
- **Nunca escribas contraseñas, tokens ni credenciales en ficheros ni en comandos** (tampoco una URL de conexión): lee la conexión de la config del proyecto. Si para probar hace falta una, pide que intervenga el usuario.

**Por momento:**

| Momento | Qué es obligatorio | Con qué |
|---|---|---|
| Al empezar | el tono del chat (opcional: borra esta fila si no usas la skill) | `project:voice` |
| No está claro qué se quiere (también si el primer mensaje es contexto pegado sin pedir nada), o el cambio sale de la pantalla (CSS compartido, plantillas base, módulos compartidos) | entrevistar antes de tocar nada; si sale de la pantalla, pregunta antes si es solo para esta o global | `project:prepare` |
| Es grande (3+ ficheros, pantalla o componente nuevo, varias capas) | un plan corto y el sí del usuario, antes de la primera edición | `project:prepare` |
| Es un bug, o algo falla | la causa, antes de proponer ningún arreglo | `project:diagnose` |
| Al ir a editar | cargar solo lo que toca (un retoque de texto, color o margen, sin cargas); si una skill es un puntero, abre el fichero al que apunta y lee entera la sección que toca | código: `project:conventions` · UI: `project:ui` · una API del stack: antes, `grep` del patrón en el repo (si está, cópialo); si no está, `project:stack` antes de escribirla, también en un script de prueba |
| La tarea crece (un segundo tipo de fichero, o un componente nuevo) | cargar lo que falte, antes de la siguiente edición | la fila de arriba |
| Cuando el usuario diga que cierra (o lo pida antes de commit o PR) | el revisor (nunca antes: el guard lo bloquea), todos sus hallazgos al usuario, limpieza, el mensaje de commit y, lo último, la pregunta del repaso con `AskUserQuestion` | `project:reviewer` y `<HARNESS>\personal\closing.md` |
| El usuario pide un repaso del harness (o lo acepta al cerrar) (opcional: borra esta fila si no usas la skill) | que lo haga un subagente nuevo, con pruebas del log | `project:retro` |
