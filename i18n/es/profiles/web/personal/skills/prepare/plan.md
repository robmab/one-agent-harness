# Plan: cómo hacerlo

Detalle de la rama "Plan" de `prepare`. Léelo cada vez que la tarea sea grande: 3 o más ficheros, una pantalla o un componente nuevo, o algo que cruza capas. **Antes de la primera edición**, y con el modo plan de la herramienta si lo tiene.

## 1. Busca lo que ya existe

Los componentes compartidos del proyecto y alguna pantalla parecida. Reutilizar antes que crear.

## 2. Escribe el plan, de 10 a 20 líneas y sin código

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
RIESGOS: <qué otra pantalla puede romper>
```

Cada paso se tiene que poder comprobar (el sensor, la pantalla, una consulta), sin "ya se verá".

## 3. Repásalo contra el proyecto

¿Reutiliza componentes compartidos?; la caché de cada CSS o JS tocado; textos visibles traducibles; el permiso del endpoint, el mismo que el de su pantalla; una migración si hay datos nuevos; los estados vacío, carga y error; móvil. <!-- TUNE: qué más se suele olvidar en tu proyecto. -->

## 4. Repásalo contra la petición

Punto por punto: ni de más ni de menos.

## 5. Enséñalo y espera un sí claro

Como en la entrevista. Ni código ni ediciones en ese turno.

## Mientras lo haces y al acabar

- Si un paso cambia, dilo antes de seguir.
- **Al acabar, repasa lo hecho contra los PASOS:** cada cosa en el sitio que dice el plan; si algo ha quedado en otro, dilo antes de cerrar.
- Al cerrar, el OBJETIVO y los ficheros del plan son el alcance y la intención que le pasas al `reviewer`.

## Señales de alarma

- Código en el plan, pasos tipo "ajustar lo que haga falta" o sin forma de comprobarlos.
- Un componente nuevo sin haber mirado lo compartido.
- Editar antes del sí.
- Planificar un retoque: con uno o dos ficheros claros, se hace directo.
