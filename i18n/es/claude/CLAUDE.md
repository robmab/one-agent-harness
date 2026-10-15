Harness de <PROJECT> (solo en su repo): **6 skills + 1 sensor + 1 agente**, sobre `AGENTS.md`. (Opcional, bórralo si no usas la skill) Al empezar, carga solo `project:estilo-comentarios`: su página ya marca el tono del chat. Su detalle (`<HARNESS>\personal\skills\estilo-comentarios\detalle.md`) léelo una vez, al escribir el primer comentario de código.

Orden de trabajo: entender (si no está claro o es un bug) → hacer → comprobar → revisar. En cada momento:

- **ANTES de escribir código:** carga `project:convenios-codigo`. Si es UI, también `project:diseno-ui`; si toca una API o librería del stack, también `project:fuentes-oficiales`. Si una skill es solo un puntero ("Lee `<ruta>`…"), abre el fichero al que apunta. Si un retoque crece (un segundo tipo de fichero, un componente nuevo), carga lo que falte antes de la siguiente edición.
- **DESPUÉS de cada cambio de código:** el sensor (`check`) salta solo por hook y deja una línea (`OK`, avisos o ERROR). Si da ERROR, corrígelo antes de seguir.
- **ANTES de decir "hecho":** comprueba con `project:verificar-antes-de-acabar` y di qué has comprobado y qué no.
- **Para revisar:** el único agente es `project:revisor` (contexto limpio, no edita), de una vez al cerrar la sesión (o antes de commit/PR), con todo el diff. Al lanzarlo, pásale solo el alcance (ficheros o commits de la sesión) y qué se quería hacer, en 2-4 líneas: ni qué has comprobado ni dónde mirar.
- **En el navegador:** la pestaña es la del usuario: no le cambies el tamaño, y las intercepciones de red, en otra pestaña y quitadas al acabar. Lo visual se comprueba con captura con zoom. Cómo probar en local: el apartado "Probar en local" de `project:verificar-antes-de-acabar`.
- **El commit y el push son del usuario:** deja el cambio comprobado y propón el mensaje entero. No ejecutes `git add`, `git commit`, `git push` (ni `--amend` o `--force`) ni toques ramas salvo que te lo pida en ese momento.
- **Nunca guardes contraseñas, tokens ni credenciales en ficheros** (skills, repo ni home): úsalas solo en la sesión. Si para probar hace falta un usuario o una contraseña, pide que intervenga el usuario.

Cada skill dice cuándo usarla; esto solo marca el orden.
