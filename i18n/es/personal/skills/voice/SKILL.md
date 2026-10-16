---
name: voz
description: "Estilo de los comentarios del código (longitud, tono, cuándo se comenta y cuándo no) y tono del chat con el usuario. Use when: escribir o revisar comentarios de código, o al empezar la conversación."
---

# Estilo de comentarios y tono

> **CONCEPTO:** tu voz: cómo comenta el agente el código y cómo te habla. Sin esto, los comentarios salen largos, impersonales y explicando lo obvio.

> **OPTIONAL · PLANTILLA · FILL-IN.**
> - Fuera del core: es **tu** forma de escribir, y cada persona tiene la suya. Si no te importa cómo comenta el agente, bórrala (y su línea en `claude\CLAUDE.md` y en el router).
> - Aquí, las 5-6 reglas que más te importan. El detalle (ejemplos tuyos, muletillas, lo que odias) va en `detalle.md`, que se lee una vez, al escribir el primer comentario.
> - Cuando esté rellena, borra este bloque.

<!-- FILL-IN: ejemplo de reglas, cámbialas por las tuyas:
- **Longitud:** máximo una línea; si no cabe, no se comenta.
- **Qué se comenta:** secciones y el porqué; nunca una corrección ("arreglé X" va al commit).
- **Tono:** coloquial o formal; primera persona o impersonal.
- **Idioma:** el de los comentarios del código y el del chat.
- **Apaños temporales:** cómo se marcan (`TEMP`, `TODO`…).
- **El chat:** si el mismo tono vale para lo que te contesta el agente.
-->

<!-- FILL-IN: 2-3 "antes → después" de tu propio código, para que los primeros comentarios salgan bien (el detalle trae más). Por ejemplo:
- `// Sincroniza los iconos del menú con el estado real de las cards` → `// Los iconos del menú van a la par de las cards`
- `// Corregido: antes el nivel se perdía al filtrar` → sin comentario (es una corrección: va al commit)
-->

Detalle (ejemplos y voz): [detalle.md](./detalle.md). Léelo una vez, al **escribir o repasar** el primer comentario de la sesión; para el tono del chat basta con esta página. No lo releas después.
