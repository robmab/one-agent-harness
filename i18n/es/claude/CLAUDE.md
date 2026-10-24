Harness de <PROJECT> (solo en su repo): **6 skills de núcleo + 1 sensor + 1 agente**, sobre `AGENTS.md`; aparte, `voice` y `retro`, opcionales.

**Siempre, también en retoques:**
- **Tras cada edición** salta el sensor (`check`) por el hook y deja una línea (`OK`, avisos o ERROR). Si da ERROR, se corrige antes de seguir. No lo relances a mano: para enseñarlo, basta con su última salida.
- **Antes de decir "hecho"**, enseña qué has comprobado y qué no. Lo que has tocado sale de `git status --short`, no de memoria (también cuando digas que no has tocado nada).
- **Git es del usuario:** nada de `git add`, `commit`, `push` (ni `--amend` o `--force`) ni tocar ramas, salvo que te lo pida en ese momento.
- **Nunca escribas contraseñas, tokens ni credenciales en ficheros ni en comandos** (tampoco una URL de conexión): lee la conexión de la config del proyecto. Si para probar hace falta una, pide que intervenga el usuario.

**Por momento:**

| Momento | Qué es obligatorio | Con qué |
|---|---|---|
| Al empezar | el tono del chat (opcional: borra esta fila si no usas la skill) | `project:voice` |
| No está claro qué se quiere, o el cambio sale de la pantalla (CSS compartido, plantillas base, módulos compartidos) | entrevistar antes de tocar nada; si se contesta con un dato, dalo (o pregunta) antes de lanzar comandos; si sale de la pantalla, pregunta antes si es solo para esta o global | `project:prepare` |
| Es grande (3+ ficheros, pantalla o componente nuevo, varias capas) | un plan corto y el sí del usuario, antes de la primera edición | `project:prepare` |
| Es un bug, o algo falla | la causa, antes de proponer ningún arreglo | `project:diagnose` |
| Al ir a editar | cargar solo lo que toca (un retoque de texto, color o margen, sin cargas); si una skill es un puntero, abre el fichero al que apunta | código: `project:conventions` · UI: `project:ui` · una API del stack que no ves ya en el repo: `project:stack` |
| La tarea crece (un segundo tipo de fichero, o un componente nuevo) | cargar lo que falte, antes de la siguiente edición | la fila de arriba |
| Antes de decir "hecho" | la prueba que lo demuestra, ejecutada ahora; lo visual, con captura con zoom | `project:verify` (también cómo probar en local y el navegador) |
| Cuando el usuario diga que cierra (o lo pida antes de commit o PR) | el revisor (nunca antes: el guard lo bloquea), todos sus hallazgos al usuario, limpieza, el mensaje de commit y, lo último, la pregunta del repaso con `AskUserQuestion` | `project:reviewer` y `<HARNESS>\personal\closing.md` |
| El usuario pide un repaso del harness (o lo acepta al cerrar) (opcional: borra esta fila si no usas la skill) | que lo haga un subagente nuevo, con pruebas del log | `project:retro` |
