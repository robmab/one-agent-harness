---
name: diagnose
description: "Depurar buscando la causa raíz antes de tocar nada: reproducir, seguir el dato por las capas de la aplicación y una hipótesis cada vez. Use when: un bug, un error o traza, algo que no funciona, sale vacío o se comporta raro, un error de instalación o del entorno (pip, venv, DLL, intérprete), una herramienta que falta o no conecta, o un arreglo anterior no ha funcionado; antes de proponer ningún arreglo."
---

# Depuración sistemática

**Regla de hierro: sin causa raíz no hay arreglo.** Parchear el síntoma es fallar, aunque desaparezca.

> **PLANTILLA · FILL-IN** la tabla de capas y las trampas del proyecto. El método ya vale tal cual. Cuando esté rellena, borra este bloque.

**Primero, la zona** que diste al leer el bug (si no la has dicho, dila ahora). Sin causa no hay arreglo en ninguna; lo que cambia es cuánto hay que demostrar:

| Si sale mal, duele… | Qué exiges |
|---|---|
| Casi nada | La causa, vista y dicha en una frase |
| Molesto | Reproducirlo y enseñar la causa |
| Caro | Lo anterior, qué dato del caso explica y una prueba escrita antes de arreglar |
| Irreversible | Lo mismo, cómo se vuelve atrás, y el arreglo espera el sí del usuario |

## 1. Investigar (antes de proponer nada)

- **Lee el error entero:** la traza del servidor, la consola del navegador y la pestaña Network. La línea y el fichero suelen dar la respuesta.
- **Si el ticket nombra un campo o una tabla que no existe con ese nombre**, pregúntale al usuario antes de elegir el que parece equivalente: si se refería a otro, el arreglo no cambia nada.
- **Reprodúcelo:** pasos exactos, con qué usuario y con qué datos. Si no se reproduce, recoge más datos; no adivines.
- **Mira qué ha cambiado:** `git log`, `git diff`, `git log -S "texto"` para ver cuándo entró algo.
- **Sigue el dato por las capas** hasta ver dónde se tuerce:

| Capa | Cómo mirarla |
|---|---|
| Base de datos | query de **solo lectura** |
| <!-- FILL-IN: modelo / servicio --> | lo que devuelve: print o log temporal |
| <!-- FILL-IN: controlador / API --> | qué sale; si es JSON, la respuesta en Network |
| <!-- FILL-IN: plantilla --> | el HTML ya renderizado, no la plantilla |
| <!-- FILL-IN: frontend --> | `console.log` y la consola |

## 2. Comparar con algo que funciona

Busca en el repo algo parecido que sí vaya. Apunta **todas** las diferencias, aunque parezcan tontas.

## 3. Una hipótesis cada vez

- Escríbela: "creo que es X porque Y".
- Pruébala con el cambio **mínimo**, una sola variable.
- Si no es eso, hipótesis nueva; no amontones arreglos encima.
- **Antes de decir «es el bug», di qué dato del caso explica.** Si no explica ninguno, es un fallo aparte: que exista en el código no lo convierte en la causa.
- Si no lo entiendes, dilo: "no entiendo X".

## 4. Arreglar

- **Antes, ten la reproducción a mano.** Mejor un test, si se puede, pero vale una lista de pasos, un script o una query para ver el fallo y luego ver que ya no está.
- **Un solo cambio, en el origen.** Nada de "de paso arreglo esto otro".
- **Comprueba con `verify`** y quita los print y logs temporales.
- **Si llevas 3 arreglos fallidos, para.** Seguramente el problema es de diseño, no de la línea. Explícalo y se decide antes de un cuarto intento.

## Trampas típicas

- **Nada de escrituras sin permiso** en la base de datos ni en entornos compartidos.
- **Caché:** el navegador cachea JS y CSS; recarga con Ctrl+F5 antes de dar por malo un cambio.
- **Datos:** si la BD de desarrollo es copia de producción o de un cliente, el fallo puede depender de esos datos. Prueba con otros.
- **Silencios:** un server con recarga automática puede quedarse caído tras un error de importación; mira su consola.
<!-- FILL-IN: trampas propias del proyecto (librerías que fallan en silencio, ficheros que se procesan antes de servirse, logs que hay que subir de nivel…). -->

## Señales de que te estás saltando esto

- "Pruebo a cambiar X a ver si va."
- "Seguramente es X", sin haberlo visto.
- Varios cambios a la vez y "a ver si ahora".
- Una lista de arreglos sin haber investigado.
- "Un intento más" cuando ya llevas dos.

Si te pillas en una, vuelve al paso 1.

---
Adaptada de `systematic-debugging` de [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` (2026-10-10) (MIT).
