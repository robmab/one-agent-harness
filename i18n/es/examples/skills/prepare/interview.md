# Entrevista: cómo hacerla

Detalle de la parte "Entrevista" de `prepare`. Léelo cada vez que vayas a entrevistar.

Lo que se pide y lo que se necesita no suelen coincidir: "un listado" puede ser "saber qué clientes no han pagado". El momento barato de descubrirlo es **antes** de escribir código.

## 0. Antes de suponer, mira

Si el ticket nombra una pantalla, un dato o una funcionalidad, búscalo en el repo y mira **qué hace ahora**. Así las suposiciones tienen base: "ahora el informe suma las dos columnas; supongo que quieren verlas por separado". Solo leer: nada de tocar código ni base de datos.

## 1. Hipótesis con número

Antes de preguntar, escribe en una línea lo que crees que se quiere y cuánta confianza tienes:

```
HIPÓTESIS: quieres que el responsable vea las incidencias abiertas sin entrar una a una.
CONFIANZA: ~40% (falta: para qué rol exactamente y si es para todos los usuarios)
```

Por debajo de ~70%, di qué falta.

## 2. Una pregunta cada vez, con tu suposición

```
P: ¿Esto es para todos los usuarios o solo para el que abrió el ticket?
SUPONGO: para todos, pero solo visible con permiso de responsable.
```

**Espera la respuesta antes de la siguiente.** Nada de listas de preguntas: la tercera suele depender de la primera. A veces, suponer en contra viene bien, para que no te diga que sí por educación.

## Qué suele faltar

Pregunta solo lo que no esté claro:

- **Quién:** qué rol lo usa y desde dónde (escritorio o móvil).
- **Ámbito:** para todos, para un cliente o configurable.
- **Datos:** ¿hace falta un campo o tabla nueva? Eso implica una migración.
- **Éxito:** cómo sabremos que está bien: qué ve el usuario o qué deja de pasar.
- **Límites:** plazo, rendimiento, no romper algo que ya existe.
- **Fuera de alcance:** qué NO se hace ahora.
<!-- FILL-IN (opcional): lo que suele faltar en los tickets de este proyecto en concreto. -->

**Si no sabes la respuesta** (depende del cliente o de quien abrió el ticket), no la inventamos: va a una lista de **preguntas para el cliente** y seguimos con lo demás.

## 3. Ojo con las respuestas "de manual"

"Que sea escalable", "lo estándar", "como lo hacen todos"… suenan bien, pero no dicen nada. Pregunta: *"si no tuvieras que justificarlo ante nadie, ¿qué querrías de verdad?"*.

## 4. Devuélvelo resumido

Cuando puedas **predecir mis respuestas a tus 3 siguientes preguntas**, para y resume:

```
Esto es lo que entiendo:
- Qué:            ...
- Para quién:     ...
- Por qué ahora:  ...
- Bien hecho si:  ...
- Límite:         ...
- Fuera:          ...
- Preguntas para el cliente: ... (si hay)
¿Sí, no o retocamos?
```

La línea **"Fuera"** no se salta: la mitad de los malentendidos son de lo que no se hace.

## 5. Sí explícito y parar

- **Un "lo que veas" o un "vale, venga" no es un sí:** vuelve a preguntar con dos opciones concretas.
- **Con un sí claro, entrega el resumen, ofrece el siguiente paso** (plan si es grande, código, o preguntar al cliente) **y para.** Ni código ni herramientas en ese mismo turno.
- **Si tras varias preguntas tu confianza no sube,** dilo: "falta algo de base, ¿paramos y lo miramos desde otro lado?".

## Señales de alarma

- Dos o más preguntas en el mismo mensaje.
- Una pregunta sin tu suposición.
- Dar por buena una respuesta de manual sin rascar.
- Empezar a planificar o programar antes del sí.
- Inventar lo que solo sabe el cliente.
- Guardar el resumen en un fichero del repo: se queda en el chat salvo que se pida.
