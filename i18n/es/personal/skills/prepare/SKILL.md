---
name: prepare
description: "Antes de programar: sacar lo que de verdad hay que hacer (preguntas de una en una, cada una con tu suposición) y, si duele cuando sale mal, bajarlo a un plan corto que aprueba el usuario. Use when: te lo piden ('entrevístame', 'pregúntame', '¿lo tenemos claro?', 'planifícalo'); un ticket no deja claro para quién es, por qué o cuándo está bien hecho; o la tarea es cara o irreversible si sale mal, o se perdería trabajo si la sesión se corta. NO para tareas que apenas duelen ni para bugs (eso es diagnose)."
---

# Entrevístame (y planifica)

> **CONCEPTO:** todo lo que pasa antes de escribir código, en una skill. Lo que se pide y lo que se necesita no suelen coincidir, y el momento barato de descubrirlo es antes de programar; si duele cuando sale mal, lleva un plan corto que el usuario aprueba antes de la primera edición. Evita que el agente rellene los huecos inventando.

> **PLANTILLA · FILL-IN** cada apartado. Ejemplo completo: [examples/skills/prepare](../../../examples/skills/prepare/SKILL.md). Cuando esté relleno, borra este bloque.

**Primero, la zona** que diste al leer la tarea (si no la has dicho, dila ahora). Decide cuánto de esta skill aplica:

| Si sale mal, duele… | Qué haces |
|---|---|
| Casi nada | Nada de aquí: se hace directo |
| Molesto | Una línea de plan; entrevista solo si hay duda |
| Caro | El **Plan** entero: objetivo, límites y prueba, y el sí del usuario |
| Irreversible | Lo mismo, y además qué puede salir mal, cómo se vuelve atrás y qué ejecuta el usuario |

**La prueba:** si la sesión se cortara ahora, ¿otra persona podría terminarla con el pedido y el diff? Si no, como mínimo es cara. El número de ficheros no decide la zona.

| Situación | Qué haces |
|---|---|
| No está claro qué se quiere | **Entrevista** |
| Es cara o irreversible | **Plan** |
| Es un bug | `diagnose`; si el arreglo es caro o irreversible, después **Plan** |

## Entrevista
<!-- FILL-IN: cómo preguntar. P. ej.: mirar antes en el repo qué hace hoy; una pregunta cada vez, con tu suposición; un resumen con la línea "Fuera"; un sí explícito y parar. -->

## Qué suele faltar
<!-- FILL-IN: lo que dejan fuera los tickets de este proyecto. P. ej.: qué rol, qué clientes, un campo nuevo (migración), cómo sabremos que está bien. -->

## Plan
<!-- FILL-IN: siempre objetivo, límites y prueba (lo que demuestra que está hecho), y un paso cada vez, comprobado antes del siguiente. la forma del plan. P. ej.: 10-20 líneas sin código; pasos en orden de capas, cada uno con cómo se comprueba; qué reutiliza; qué no se toca; el sí del usuario antes de editar; al acabar, lo hecho repasado contra los pasos. -->

## Señales de alarma
<!-- FILL-IN: 2-3. P. ej.: dos preguntas en un mensaje; programar antes del sí; planificar un retoque de un fichero. -->
