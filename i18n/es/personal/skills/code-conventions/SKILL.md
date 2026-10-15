---
name: convenios-codigo
description: "Convenios de código de <PROJECT>: nombrado, dónde va la lógica, base de datos, frontend y anti-patrones. Use when: antes de escribir o revisar CUALQUIER código de <PROJECT>."
---

# Convenios de código — <PROJECT>

> **CONCEPTO:** las reglas que valen siempre para el código del proyecto, cargadas antes de escribir o revisar nada. Sin ellas, el agente escribe "buen código" en general, no código que encaje aquí.

> **PLANTILLA · FILL-IN.**
> - Es la skill que más entra: antes de escribir o revisar cualquier código. Solo reglas que valgan **siempre**; lo de un módulo concreto, a otra skill.
> - Objetivo: 700 palabras como mucho, reglas de una línea y sin ejemplos largos.
> - Si el proyecto ya tiene sus convenios en un repo de equipo, no los copies aquí: deja solo "Lee `<ruta>` desde la raíz del repo y síguelo; si no existe, avisa".
> - Cuando esté rellena, borra este bloque.

Si no estás en el repo de <PROJECT>, ignora esta skill.

## Stack técnico
<!-- FILL-IN: lenguajes y frameworks principales. Las versiones exactas y sus trampas van en `fuentes-oficiales`. -->

## Nombrado
<!-- FILL-IN: idioma de los nombres; camelCase o snake_case por lenguaje; nombres de ficheros y carpetas. -->

## Arquitectura: dónde va cada cosa
<!-- FILL-IN: dónde vive la lógica de negocio (modelos, servicios…); controladores o vistas finos; utilidades compartidas. -->

## Base de datos
<!-- FILL-IN: cómo se cambian las tablas (migraciones, scripts…), qué no se hace nunca a mano y qué necesita permiso. -->

## Frontend
<!-- FILL-IN: framework y patrón de componentes; arquitectura CSS, variables y colores; cómo se cargan los assets. -->

## Anti-patrones — NO HACER
<!-- FILL-IN: lo que ya ha hecho daño alguna vez. El revisor trata esta sección como crítica. -->

## Formato y comentarios
<!-- FILL-IN: longitud de línea, formateador o linter del proyecto, estilo de comentarios del equipo. -->
