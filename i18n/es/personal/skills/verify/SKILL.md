---
name: verify
description: "Antes de decir que algo está hecho, arreglado o que funciona, ejecutar la comprobación y enseñar el resultado; si no se puede comprobar, decirlo. Use when: vas a dar por terminada una tarea, decir que un bug está arreglado o que algo pasa, decir que algo ya está hecho, ya existe o ya está en producción, o antes de un commit o PR."
---

# Verificar antes de acabar

> **CONCEPTO:** nada de "hecho" sin una comprobación ejecutada en ese mismo mensaje y su salida leída; lo que no se puede comprobar se dice. Evita que el agente dé por bueno un éxito que no ha visto.

> **PLANTILLA · FILL-IN** cada apartado. Ejemplo completo: [examples/skills/verify](../../../examples/skills/verify/SKILL.md). Cuando esté relleno, borra este bloque.

## Antes de afirmar nada
<!-- FILL-IN: los pasos. P. ej.: elegir la prueba que lo demuestra, ejecutarla ahora, leer la salida entera, decirlo con la prueba. -->

## Cuánta prueba, según la zona

La zona cambia cuánto se comprueba, no la regla: nada de "hecho" sin una prueba ejecutada ahora.

| Zona | Prueba |
|---|---|
| Casi nada | Una mirada y el sensor |
| Molesto | Una comprobación real de lo pedido |
| Caro | La PRUEBA del plan, ejecutada y enseñada |
| Irreversible | Lo mismo, y lo que no tiene vuelta atrás lo ejecuta el usuario |

## Qué prueba cada cosa

| Afirmación | Prueba | No vale |
|---|---|---|
| Encaja con el stack y compila | `py -3 <HARNESS>\personal\scripts\check.py` (sin ficheros, lo cambiado en git): 0 errores | "lo he hecho con cuidado" |
| <!-- FILL-IN: p. ej. Pasan los tests --> | <!-- el comando de tests, 0 fallos --> | <!-- "deberían pasar" --> |
| Bug arreglado | un test que fallaba antes del arreglo y ahora pasa (si el proyecto tiene tests); si no, los pasos del síntoma original | "he cambiado el código" |
| Algo "ya está", también en producción | `git branch -a --contains <sha>`: di en qué rama | el commit en tu rama |

## Probar en local
<!-- FILL-IN: sin credenciales (si para probar hace falta una contraseña, pide que intervenga el usuario). URL local y quién levanta el server, de dónde se lee la conexión a la BD, datos útiles. -->

## En el navegador
<!-- FILL-IN (si el agente usa uno). P. ej.: la pestaña es la del usuario; su pantalla también (nada de capturas del escritorio ni de listar o cambiar sus ventanas sin que lo pida); intercepta peticiones en otra pestaña; tras 3 intentos fallidos, para. -->

## Si no se puede comprobar
<!-- FILL-IN: cómo decirlo. P. ej. "Comprobado: … / Sin comprobar: …, porque …". -->

## Señales de alarma
<!-- FILL-IN: 2-3. P. ej.: "debería funcionar"; "¡Listo!" antes de ejecutar nada; fiarse de un subagente sin el diff. -->
