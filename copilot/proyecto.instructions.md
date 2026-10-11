---
applyTo: "**"
description: "Router del harness de <PROYECTO>: orden de trabajo, sensor y el único agente de revisión"
---

Harness de <PROYECTO> (solo en su repo): **6 skills + 1 sensor + 1 agente**, sobre `AGENTS.md`. (Opcional, bórralo si no usas la skill) Al empezar, carga `estilo-comentarios` y lee su detalle (`<HARNESS>\personal\skills\estilo-comentarios\estilo_comentarios.md`) una sola vez.

Orden de trabajo: entender (si no está claro o es un bug) → hacer → comprobar → revisar. En cada momento:

- **ANTES de escribir código:** carga `convenios-codigo`. Si es UI, también `diseno-ui`; si toca una API o librería del stack, también `fuentes-oficiales`.
- **DESPUÉS de cada cambio de código:** lanza `py -3 <HARNESS>\personal\scripts\comprobar.py`. Si da ERROR, corrígelo antes de seguir.
- **ANTES de decir "hecho":** enseña la salida de ese comando y di qué has comprobado y qué no.
- **Para revisar:** el único agente es `revisor` (contexto limpio, no edita, convenios incluidos).

Cada skill dice cuándo usarla; esto solo marca el orden. Con modelos pequeños, este formato de "ANTES / DESPUÉS" funciona mucho mejor que una descripción general.
