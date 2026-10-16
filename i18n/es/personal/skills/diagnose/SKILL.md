---
name: diagnosticar
description: "Depurar buscando la causa raíz antes de tocar nada: reproducir, seguir el dato por las capas de la aplicación y una hipótesis cada vez. Use when: un bug, un error o traza, algo que no funciona, sale vacío o se comporta raro, o un arreglo anterior no ha funcionado; antes de proponer ningún arreglo."
---

# Depuración sistemática

> **CONCEPTO:** sin causa raíz no hay arreglo. Parchear el síntoma es un fallo aunque desaparezca; sin esto, el agente apila suposiciones y al tercer intento ha roto otra cosa.

> **PLANTILLA · FILL-IN** cada apartado. Ejemplo completo: [examples/skills/diagnosticar](../../../examples/skills/diagnosticar/SKILL.md). Cuando esté relleno, borra este bloque.

## 1. Investigar

| Capa | Cómo mirarla |
|---|---|
| <!-- FILL-IN: p. ej. Base de datos --> | <!-- p. ej. una consulta de solo lectura --> |
| <!-- FILL-IN: p. ej. API --> | <!-- p. ej. la respuesta en la pestaña Red --> |

<!-- FILL-IN: antes de las capas, p. ej.: leer el error entero, reproducirlo, mirar qué ha cambiado (git log). -->

## 2. Comparar con algo que funciona
<!-- FILL-IN: p. ej. buscar algo parecido en el repo que funcione y apuntar todas las diferencias. -->

## 3. Una hipótesis cada vez
<!-- FILL-IN: p. ej. "creo que es X porque Y", probado con el cambio más pequeño. -->

## 4. Arreglar
<!-- FILL-IN: p. ej. un solo cambio y en el origen; si el proyecto tiene tests, la reproducción se queda como test de regresión; tras 3 arreglos fallidos, parar y replantear. -->

## Trampas del proyecto
<!-- FILL-IN: lo que aquí falla en silencio (caché, datos, un server que se queda caído…). -->

## Señales de alarma
<!-- FILL-IN: 2-3. P. ej.: "pruebo a cambiar X a ver"; varios cambios a la vez. -->
