---
name: conventions
description: "Convenios de código de <PROJECT>: dónde va la lógica, endpoints y permisos, base de datos, frontend, tests y anti-patrones. Use when: antes de escribir o revisar CUALQUIER código de <PROJECT>."
---

# Convenios de código — <PROJECT>

**CONCEPTO:** las reglas que valen siempre para el código del proyecto, cargadas antes de escribir o revisar nada. Sin ellas, el agente escribe "buen código" en general, no código que encaje aquí.

> **PERFIL · web.** Reglas generales de web, válidas para casi cualquier stack. Ajusta a tu stack lo marcado con `TUNE` y luego quita la marca.

Si no estás en el repo de <PROJECT>, ignora esta skill.

## Stack técnico
<!-- TUNE: lenguajes y frameworks principales. Las versiones exactas y sus trampas van en `stack`. -->

## Nombrado
- Un solo idioma para los identificadores en todo el proyecto, y un estilo por tipo de fichero.
<!-- TUNE: camelCase o snake_case por lenguaje; nombres de ficheros y carpetas. -->

## Arquitectura: dónde va cada cosa
- **La lógica de negocio en el modelo o en un servicio,** no en el controlador ni en la plantilla: un cálculo sobre una entidad es un método de esa entidad.
- **Controladores finos:** leen la petición, llaman a la lógica y devuelven la respuesta.
- **Las piezas compartidas** (usadas en 2 o más pantallas), en un sitio común; las de una pantalla, junto a esa pantalla.
<!-- TUNE: las carpetas del proyecto para modelos, servicios, controladores, plantillas y componentes. -->

## Endpoints y permisos
- **Un permiso en cada punto de entrada,** comprobado en el servidor; el endpoint de una pantalla usa el mismo permiso que la pantalla.
- **Valida la entrada en el servidor,** pronto, y retorna pronto. Nunca te fíes de lo que manda el front (campos ocultos, botones deshabilitados).
- **Los cambios, solo por POST, PUT o DELETE,** nunca por GET.

## Base de datos
- **Cambios de esquema con migraciones,** nunca a mano en una base de datos compartida.
- **Consultas con parámetros,** nunca concatenando ni interpolando valores.
- **Escrituras en una BD o un entorno compartidos:** pide permiso antes.
<!-- TUNE: la herramienta de migraciones y dónde viven. -->

## Frontend
- **Textos visibles traducibles** con la función de i18n del proyecto, nunca escritos a mano en un idioma.
- **Sin estilos en línea ni valores sueltos:** colores, radios y espaciados salen de las variables de diseño (`ui`).
- **Assets versionados:** cuando cambia un CSS o un JS, cambia también su caché (`?v=`, un hash).
- **Accesibilidad mínima:** cada campo con su label, imágenes con `alt`, foco visible y contraste suficiente.
- **Sin restos de depuración** (`console.log`, `debugger`) ni claves o secretos en el front.
<!-- TUNE: el framework y su patrón de componentes; cómo se cargan los assets. -->

## Tests
- **Si el proyecto tiene tests:** la lógica de negocio, los cálculos, los permisos y cada bug arreglado llevan el suyo; la maquetación y el código de unión, no.
- **Los casos los decide el usuario;** el agente los escribe, y al revisar se miran las aserciones, no el montaje.
<!-- TUNE: el framework, dónde viven los tests y cómo se lanza uno solo. -->

## Anti-patrones — NO HACER
- Reescribir lo que funciona para "ordenarlo", o cambiar una API sin preguntar.
- Añadir una librería para algo que el stack ya hace.
- Copiar un componente que ya existe en vez de reutilizarlo.
<!-- TUNE: lo que ya ha hecho daño en este proyecto. El revisor trata esta sección como crítica. -->

## Formato y comentarios
- **Líneas de unos 100 caracteres:** parte las condiciones, llamadas y objetos largos en vez de dejarlos largos.
- **Comentarios cortos** que digan qué o por qué; un arreglo no se comenta (va en el commit).
<!-- TUNE: el formateador o linter del proyecto. -->
