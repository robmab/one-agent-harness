---
name: verify
description: "Antes de decir que algo está hecho, arreglado o que funciona, ejecutar la comprobación y enseñar el resultado; si no se puede comprobar, decirlo. Use when: vas a dar por terminada una tarea, decir que un bug está arreglado o que algo pasa, decir que algo ya está hecho, ya existe o ya está en producción, o antes de un commit o PR."
---

# Verificar antes de acabar

**Regla de hierro: nada de "hecho" sin una prueba ejecutada en este mismo mensaje.** Si no has lanzado el comando ahora y leído su salida, no puedes afirmarlo.

> **PLANTILLA · FILL-IN** las filas de la tabla con los comandos reales del proyecto. El resto ya vale tal cual. Cuando esté rellena, borra este bloque.

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
| Pasan los tests | <!-- FILL-IN: comando de tests --> con 0 fallos | "deberían pasar" |
| La pantalla funciona | cargar la página con el server levantado y mirar la consola del navegador | que la plantilla compile |
| Se ve bien (bordes, sombras, solapes) | captura con zoom, en reposo y en el estado que fallaba | solo medidas |
| Un control que no se puede fotografiar (un `<select>` abierto, un valor por defecto) | el DOM (`options`, `selected`, `value`) y la consola limpia | "se ve bien" |
| Bug arreglado | repetir los pasos del síntoma original y que ya no salga | "he cambiado el código" |
| Da lo mismo que algo que ya existe (otra función, un endpoint, una consulta) | comparar con **esa** función llamándola, o con su consulta copiada tal cual; y con un caso que no dé 0 | una consulta reescrita a mano "al estilo de": prueba tu lectura del código, no el código |
| Un subagente lo ha hecho | mirar el `git diff` tú mismo | fiarte de su informe |
| Cumple lo pedido | releer la petición punto por punto | que compile |
| Algo "ya está", también en producción | `git branch -a --contains <sha>`: di en qué rama | el commit en tu rama |
| <!-- FILL-IN: lint, build, migraciones, traducciones… --> | | |

**Ojo:** lo que toque la base de datos o un entorno compartido es una prueba válida, pero **siempre con permiso antes**.

## Probar en local

<!-- FILL-IN: sin credenciales (si para probar hace falta una contraseña, pide que intervenga el usuario). -->
- **App:** <!-- FILL-IN: URL local; quién levanta el server -->
- **Base de datos:** <!-- FILL-IN: de dónde se lee su conexión -->
- **Datos y trucos útiles:** <!-- FILL-IN -->
- **Scripts de usar y tirar** (una consulta, una comprobación): en la carpeta temporal, leyendo la conexión del fichero de configuración; **nunca la imprimas** (lleva la contraseña). Bórralos todos al acabar la tarea. Para retocar uno, edítalo con Edit (falla si no encuentra el texto), no con un `str.replace` desde otro script, que no avisa si no cambia nada.

## En el navegador

- **La pestaña es la del usuario**: no le cambies el tamaño ni la dejes en otra vista.
- **Interceptar peticiones:** en otra pestaña, y quitado al acabar (`page.unrouteAll()`). Si algo se cuelga, sospecha antes de tu instrumentación.
- **Tres intentos fallidos sobre lo mismo: para** y busca la causa de fondo (`diagnose`) o pregunta.

## Si no se puede comprobar

Pasa a menudo: no hay tests, el server no está levantado o faltan datos. No pasa nada, pero **dilo claro** y separa lo comprobado de lo que no:

```
Comprobado: sintaxis de servicios/pedidos.py (check.py OK).
Sin comprobar: la pantalla de edición, falta levantar el server. Para verlo: <pasos>.
```

## Señales de que te estás saltando esto

- Escribir "debería funcionar", "probablemente", "parece que" o "en principio".
- Un "¡Listo!" o "¡Perfecto!" antes de haber ejecutado nada.
- Ir a hacer commit o PR sin comprobar.
- Pensar "por esta vez no hace falta".
- Dar por bueno el informe de un subagente sin mirar el diff.

Si te pillas en una, para y vuelve al paso 1.

| Excusa | Realidad |
|---|---|
| "Estoy seguro" | Estar seguro no es una prueba |
| "Es un cambio pequeño" | Los pequeños también rompen |
| "Ya lo probé antes" | Antes no vale, tiene que ser después del último cambio |
| "Compila" o "el editor no se queja" | Compilar no es funcionar |

---
Adaptada de `verification-before-completion` de [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` (2026-10-10) (MIT).
