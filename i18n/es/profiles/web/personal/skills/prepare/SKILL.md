---
name: prepare
description: "Antes de programar: sacar lo que de verdad hay que hacer (preguntas de una en una, cada una con tu suposición) y, si duele cuando sale mal, bajarlo a un plan corto que aprueba el usuario. Use when: te lo piden ('entrevístame', 'pregúntame', '¿lo tenemos claro?', 'planifícalo', 'hazme un plan'); un ticket no deja claro para quién es, por qué o cuándo está bien hecho; o la tarea es cara o irreversible si sale mal, o se perdería trabajo si la sesión se corta. NO para tareas que apenas duelen (renombrar, mover, un retoque) ni para bugs (eso es diagnose)."
---

# Preparar

**CONCEPTO:** todo lo que pasa antes de escribir código, en una skill: sacar lo que de verdad se quiere y, si duele cuando sale mal, un plan corto que aprueba el usuario. Evita que el agente rellene los huecos inventando.

> **PERFIL · web.** Reglas generales de web, válidas para casi cualquier stack. Ajusta a tu stack lo marcado con `TUNE` y luego quita la marca.

**Primero, la zona** que diste al leer la tarea (si no la has dicho, dila ahora). Decide cuánto de esta skill aplica:

| Si sale mal, duele… | Qué haces |
|---|---|
| Casi nada | Nada de aquí: se hace directo |
| Molesto | Una línea de plan; entrevista solo si hay duda |
| Caro | El **Plan** entero: objetivo, límites y prueba, y el sí del usuario |
| Irreversible | Lo mismo, y además qué puede salir mal, cómo se vuelve atrás y qué ejecuta el usuario |

**La prueba:** si la sesión se cortara ahora, ¿otra persona podría terminarla con el pedido y el diff? Si no, como mínimo es cara. El número de ficheros no decide la zona.

Elige la rama y **lee solo su detalle**:

| Situación | Rama | Detalle |
|---|---|---|
| No está claro qué se quiere | **Entrevista** | [interview.md](./interview.md) |
| Es cara o irreversible | **Plan** | [plan.md](./plan.md) |
| Las dos cosas | Entrevista y, con el sí, plan | los dos, en ese orden |
| Es un bug | `diagnose`; si el arreglo es caro o irreversible, después **Plan** | [plan.md](./plan.md) |
| Casi nada, o molesta y clara | Ninguna: se hace directo (si es molesta, con su línea de plan) | — |

**Abre siempre el detalle de la rama antes de empezar:** ahí está cómo se hace.

---
Entrevista adaptada de `interview-me` de [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) @ `1be8e34` (2026-10-10) (MIT). Plan inspirado en `writing-plans` de [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` (MIT).
