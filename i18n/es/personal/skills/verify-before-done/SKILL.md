---
name: verificar-antes-de-acabar
description: "Antes de decir que algo está hecho, arreglado o que funciona, ejecutar la comprobación y enseñar el resultado; si no se puede comprobar, decirlo. Use when: vas a dar por terminada una tarea, decir que un bug está arreglado o que algo pasa, o antes de un commit o PR."
---

# Verificar antes de acabar

> **CONCEPTO:** nada de "hecho" sin una comprobación ejecutada en ese mismo mensaje y su salida leída; lo que no se puede comprobar se dice. Evita que el agente dé por bueno un éxito que no ha visto.

> **PLANTILLA · FILL-IN** cada apartado. Ejemplo completo: [examples/skills/verificar-antes-de-acabar](../../../examples/skills/verificar-antes-de-acabar/SKILL.md). Cuando esté relleno, borra este bloque.

## Antes de afirmar nada
<!-- FILL-IN: los pasos. P. ej.: elegir la prueba que lo demuestra, ejecutarla ahora, leer la salida entera, decirlo con la prueba. -->

## Qué prueba cada cosa

| Afirmación | Prueba | No vale |
|---|---|---|
| Encaja con el stack y compila | `py -3 <HARNESS>\personal\scripts\check.py` (sin ficheros, lo cambiado en git): 0 errores | "lo he hecho con cuidado" |
| <!-- FILL-IN: p. ej. Pasan los tests --> | <!-- el comando de tests, 0 fallos --> | <!-- "deberían pasar" --> |

## Probar en local
<!-- FILL-IN: sin credenciales (si para probar hace falta una contraseña, pide que intervenga el usuario). URL local y quién levanta el server, de dónde se lee la conexión a la BD, datos útiles. -->

## En el navegador
<!-- FILL-IN (si el agente usa uno). P. ej.: la pestaña es la del usuario; intercepta peticiones en otra pestaña; tras 3 intentos fallidos, para. -->

## Si no se puede comprobar
<!-- FILL-IN: cómo decirlo. P. ej. "Comprobado: … / Sin comprobar: …, porque …". -->

## Señales de alarma
<!-- FILL-IN: 2-3. P. ej.: "debería funcionar"; "¡Listo!" antes de ejecutar nada; fiarse de un subagente sin el diff. -->
