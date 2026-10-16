---
name: preparar
description: "Antes de programar: sacar lo que de verdad hay que hacer (preguntas de una en una, cada una con tu suposición) y, si la tarea es grande, bajarlo a un plan corto que aprueba el usuario. Use when: te lo piden ('entrevístame', 'pregúntame', '¿lo tenemos claro?', 'planifícalo', 'hazme un plan'); un ticket no deja claro para quién es, por qué o cuándo está bien hecho; o la tarea toca 3 o más ficheros, crea una pantalla o un componente, o cruza capas. NO para tareas claras y pequeñas (renombrar, mover, un retoque) ni para bugs (eso es diagnosticar)."
---

# Preparar

**CONCEPTO:** todo lo que pasa antes de escribir código, en una skill: sacar lo que de verdad se quiere y, si la tarea es grande, un plan corto que aprueba el usuario. Evita que el agente rellene los huecos inventando.

> **PERFIL · web.** Reglas generales de web, válidas para casi cualquier stack. Ajusta a tu stack lo marcado con `TUNE` y luego quita la marca.

Elige la rama y **lee solo su detalle**:

| Situación | Rama | Detalle |
|---|---|---|
| No está claro qué se quiere | **Entrevista** | [entrevista.md](./entrevista.md) |
| Está claro, pero es grande (3+ ficheros, pantalla o componente nuevo, varias capas) | **Plan** | [plan.md](./plan.md) |
| Las dos cosas | Entrevista y, con el sí, plan | los dos, en ese orden |
| Es un bug | Ninguna: `diagnosticar` | — |
| Un retoque claro (uno o dos ficheros) | Ninguna: se hace directo | — |

**Abre siempre el detalle de la rama antes de empezar:** ahí está cómo se hace.

---
Entrevista adaptada de `interview-me` de [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) @ `1be8e34` (2026-10-10) (MIT). Plan inspirado en `writing-plans` de [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` (MIT).
