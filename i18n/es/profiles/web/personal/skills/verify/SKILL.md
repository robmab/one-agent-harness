---
name: verify
description: "Antes de decir que algo está hecho, arreglado o que funciona, ejecutar la comprobación y enseñar el resultado; si no se puede comprobar, decirlo. Use when: vas a dar por terminada una tarea, decir que un bug está arreglado o que algo pasa, o antes de un commit o PR."
---

# Verificar antes de acabar

**CONCEPTO:** nada de "hecho" sin una prueba ejecutada en este mismo mensaje. Si no has lanzado el comando ahora y leído su salida, no puedes afirmarlo.

> **PERFIL · web.** Reglas generales de web, válidas para casi cualquier stack. Ajusta a tu stack lo marcado con `TUNE` y luego quita la marca.

## Antes de afirmar nada

1. **Qué lo demuestra:** elige el comando o la prueba que confirma la afirmación (tabla de abajo).
2. **Ejecútalo entero**, ahora; no te fíes de una ejecución anterior.
3. **Lee la salida completa:** código de salida, errores y avisos.
4. **¿Confirma lo que ibas a decir?** Si sí, dilo con la prueba. Si no, di el estado real.

## Qué prueba cada cosa en <PROJECT>

| Afirmación | Prueba | No vale |
|---|---|---|
| Encaja con el stack y compila | `py -3 <HARNESS>\personal\scripts\check.py [ficheros]` (sin ficheros, lo cambiado en git; solo mira las líneas cambiadas): 0 errores; los avisos, revísalos | "lo he hecho con cuidado" |
| Auditar un fichero **entero**, también lo antiguo ("audita este fichero", "¿qué incumple de los convenios?", antes de refactorizar) | el mismo comando con `--all <fichero>`; si salen muchos, **resúmelos por regla** en vez de listarlos uno a uno | revisar solo lo cambiado |
| Pasan los tests | <!-- TUNE: comando de tests --> con 0 fallos | "deberían pasar" |
| La pantalla funciona | cargarla con el server levantado: sin errores en la consola ni peticiones fallidas en Network | que la plantilla compile |
| Se ve bien (bordes, sombras, solapes) | captura con zoom, en reposo y en el estado tocado (abierto, hover, error) | solo medidas |
| Funciona en móvil | la misma pantalla a ancho de móvil (~375px): sin scroll horizontal ni solapes | "es responsive" |
| El endpoint responde | su respuesta en Network: el estado y el cuerpo esperados | "la pantalla lo enseña" |
| Los permisos aguantan | un usuario sin el permiso no entra: lo rechaza el endpoint, no solo se oculta el botón | "el botón no sale" |
| Bug arreglado | un test que fallaba antes del arreglo y ahora pasa; sin tests, repetir los pasos del síntoma original | "he cambiado el código" |
| Da lo mismo que algo que ya existe (función, endpoint, consulta) | comparado con **eso**, llamándolo o copiado tal cual, en un caso que no dé 0 | una consulta reescrita a mano: prueba tu lectura |
| Un subagente lo ha hecho | mirar el `git diff` tú mismo | fiarte de su informe |
| Cumple lo pedido | releer la petición punto por punto | que compile |
| <!-- TUNE: lint, build, migraciones, traducciones… --> | | |

**Ojo:** lo que toque la base de datos o un entorno compartido es una prueba válida, pero **siempre con permiso antes**.

## Probar en local

Sin credenciales aquí: si para probar hace falta una contraseña, pide que intervenga el usuario.
- **App:** <!-- TUNE: URL local; quién levanta el server -->
- **Base de datos:** <!-- TUNE: de dónde se lee su conexión -->: no la imprimas nunca.
- **Datos y trucos útiles:** <!-- TUNE: usuarios de cada rol, registros que cubran los casos límite -->

## En el navegador

- **La pestaña es la del usuario**: no le cambies el tamaño ni la dejes en otra vista.
- **Interceptar peticiones:** en otra pestaña, y quitado al acabar (`page.unrouteAll()`). Si algo se cuelga, sospecha antes de tu instrumentación.
- **Tres intentos fallidos sobre lo mismo: para** y busca la causa de fondo (`diagnose`) o pregunta.

## Si no se puede comprobar

Sin tests, sin server, sin datos: **dilo claro**, separando lo comprobado de lo que no:

```
Comprobado: sintaxis de servicios/pedidos.py (check.py OK).
Sin comprobar: la pantalla de edición, falta levantar el server. Para verlo: <pasos>.
```

## Señales de que te estás saltando esto

- Escribir "debería funcionar", "probablemente", "parece que" o "en principio".
- Un "¡Listo!" o "¡Perfecto!" antes de haber ejecutado nada.
- Ir a hacer commit o PR sin comprobar.
- Pensar "por esta vez no hace falta".

Si te pillas en una, para y vuelve al paso 1.

---
Adaptada de `verification-before-completion` de [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` (2026-10-10) (MIT).
