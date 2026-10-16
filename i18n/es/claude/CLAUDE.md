Harness de <PROJECT> (solo en su repo): **6 skills + 1 sensor + 1 agente**, sobre `AGENTS.md`.

**Siempre, también en retoques:**
- **Tras cada edición** salta el sensor (`check`) por el hook y deja una línea (`OK`, avisos o ERROR). Si da ERROR, se corrige antes de seguir.
- **Antes de decir "hecho"**, enseña qué has comprobado y qué no.
- **Git es del usuario:** nada de `git add`, `commit`, `push` (ni `--amend` o `--force`) ni tocar ramas, salvo que te lo pida en ese momento.
- **Nunca guardes contraseñas, tokens ni credenciales en ficheros.** Si para probar hace falta una, pide que intervenga el usuario.

**Por momento:**

| Momento | Qué es obligatorio | Con qué |
|---|---|---|
| Al empezar | el tono del chat (opcional: borra esta fila si no usas la skill) | `project:voz` (su detalle, `<HARNESS>\personal\skills\voz\detalle.md`, al escribir el primer comentario) |
| No está claro qué se quiere | entrevistar antes de tocar nada | `project:preparar` |
| Es grande (3+ ficheros, pantalla o componente nuevo, varias capas) | un plan corto y el sí del usuario, antes de la primera edición | `project:preparar` |
| Es un bug, o algo falla | la causa, antes de proponer ningún arreglo | `project:diagnosticar` |
| Al ir a editar | cargar solo lo que toca (un retoque de texto, color o margen, sin cargas); si una skill es un puntero, abre el fichero al que apunta | código: `project:convenios` · UI: `project:ui` · una API del stack que no ves ya en el repo: `project:stack` |
| La tarea crece (un segundo tipo de fichero, o un componente nuevo) | cargar lo que falte, antes de la siguiente edición | la fila de arriba |
| Antes de decir "hecho" | la prueba que lo demuestra, ejecutada ahora; lo visual, con captura con zoom | `project:comprobar` (también cómo probar en local y el navegador) |
| Al cerrar (o antes de commit o PR) | el revisor, todos sus hallazgos al usuario, limpieza y el mensaje de commit | `project:revisor` y `<HARNESS>\personal\cierre.md` |
