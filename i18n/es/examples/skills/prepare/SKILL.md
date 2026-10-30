---
name: prepare
description: "Antes de programar: sacar lo que de verdad hay que hacer (preguntas de una en una, cada una con tu suposición) y, si duele cuando sale mal, bajarlo a un plan corto que aprueba el usuario. Use when: te lo piden ('entrevístame', 'pregúntame', '¿lo tenemos claro?', 'planifícalo', 'hazme un plan'); un ticket no deja claro para quién es, por qué o cuándo está bien hecho; o la tarea es cara o irreversible si sale mal, o se perdería trabajo si la sesión se corta. NO para tareas que apenas duelen (renombrar, mover, un retoque) ni para bugs (eso es diagnose)."
---

# Entrevístame (y planifica)

**Primero, la zona** que diste al leer la tarea (si no la has dicho, dila ahora). Decide cuánto de esta skill aplica:

| Si sale mal, duele… | Qué haces |
|---|---|
| Casi nada | Nada de aquí: se hace directo |
| Molesto | Una línea de plan; entrevista solo si hay duda |
| Caro | El **Plan** entero: objetivo, límites y prueba, y el sí del usuario |
| Irreversible | Lo mismo, y además qué puede salir mal, cómo se vuelve atrás y qué ejecuta el usuario |

**La prueba:** si la sesión se cortara ahora, ¿otra persona podría terminarla con el pedido y el diff? Si no, como mínimo es cara. El número de ficheros no decide la zona.

Dos pasos antes de escribir código; usa el que toque:

| Situación | Qué haces |
|---|---|
| No está claro qué se quiere | **Entrevista** |
| Es cara o irreversible | **Plan** |
| Las dos cosas | Entrevista y, con el sí, plan |
| Es un bug | `diagnose`; si el arreglo es caro o irreversible, después **Plan** |

## Entrevista

Lo que se pide y lo que se necesita no suelen coincidir. Lo esencial:

1. **Mira antes en el repo** qué hace hoy esa pantalla o ese dato (solo leer).
2. **Hipótesis con % de confianza**; por debajo de ~70 %, di qué falta.
3. **Una pregunta cada vez, con tu suposición**, y espera la respuesta.
4. **Resumen** (qué, para quién, por qué, bien hecho si, límite, fuera) cuando puedas predecir mis 3 siguientes respuestas.
5. **Sí explícito y parar.**

Cómo hacerlo, qué suele faltar y las señales de alarma: [interview.md](./interview.md). Léelo **cada vez que vayas a entrevistar**.

## Plan

Cuando la zona es cara o irreversible. **Antes de la primera edición**, y con el modo plan de la herramienta si lo tiene.

1. **Busca lo que ya existe:** los componentes compartidos del proyecto y alguna pantalla parecida. Reutilizar antes que crear.
2. **Escribe el plan, de 10 a 20 líneas y sin código:**

   ```
   OBJETIVO: <una línea; si vienes de la entrevista, su "Qué">
   PASOS (en orden de capas, quita las que no apliquen):
   1. migración             → ficheros · cómo se comprueba
   2. modelo                → …
   3. endpoint (permiso)    → …
   4. plantilla             → …
   5. código del front      → …
   6. estilos               → …
   REUTILIZA: <componentes compartidos o código que ya existe>
   NO SE TOCA: <lo que queda fuera>
   PRUEBA: <qué demuestra que está hecho; si no se puede comprobar, no está definido>
   RIESGOS: <qué otra pantalla puede romper>
   VUELTA ATRÁS: <solo si es irreversible: cómo se deshace y qué ejecuta el usuario>
   ```

   Cada paso se tiene que poder comprobar (el sensor, la pantalla, una consulta), sin "ya se verá", y lo compruebas antes de empezar el siguiente.
3. **Repásalo contra el proyecto:** <!-- FILL-IN: lo que aquí se suele olvidar, p. ej. la caché de CSS/JS, las traducciones, el permiso del endpoint, una migración --> ¿reutiliza lo compartido?
4. **Repásalo contra la petición**, punto por punto: ni de más ni de menos.
5. **Enséñalo y espera un sí claro**, como en la entrevista. Ni código ni ediciones en ese turno.

Si al hacerlo un paso cambia, dilo antes de seguir. Al cerrar, el OBJETIVO y los ficheros del plan son el alcance y la intención que le pasas al `reviewer`.

## Señales de alarma del plan

- Código en el plan, pasos tipo "ajustar lo que haga falta" o sin forma de comprobarlos.
- Un componente nuevo sin haber mirado lo compartido.
- Editar antes del sí.
- Planificar lo que no duele: lo de «casi nada» se hace directo.

---
Entrevista adaptada de `interview-me` de [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) @ `1be8e34` (2026-10-10) (MIT). Plan inspirado en `writing-plans` de [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` (MIT).
