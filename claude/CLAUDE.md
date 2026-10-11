Harness de <PROYECTO> (solo en su repo): **6 skills + 1 sensor + 1 agente**, sobre `AGENTS.md`. (Opcional, bórralo si no usas la skill) Al empezar, carga `proyecto:estilo-comentarios` y lee su detalle (`<HARNESS>\personal\skills\estilo-comentarios\estilo_comentarios.md`) una sola vez.

Orden de trabajo: entender (si no está claro o es un bug) → hacer → comprobar → revisar. En cada momento:

- **ANTES de escribir código:** carga `proyecto:convenios-codigo`. Si es UI, también `proyecto:diseno-ui`; si toca una API o librería del stack, también `proyecto:fuentes-oficiales`.
- **DESPUÉS de cada cambio de código:** el sensor (`comprobar`) salta solo por hook. Si da ERROR, corrígelo antes de seguir.
- **ANTES de decir "hecho":** comprueba con `proyecto:verificar-antes-de-acabar` y di qué has comprobado y qué no.
- **Para revisar:** el único agente es `proyecto:revisor` (contexto limpio, no edita).

Cada skill dice cuándo usarla; esto solo marca el orden.
