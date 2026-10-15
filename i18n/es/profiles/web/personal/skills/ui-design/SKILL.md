---
name: diseno-ui
description: "Design system de <PROJECT>: componentes, colores, tipografía, espaciado, estados de pantalla y maquetación. Use when: SOLO maquetación, estilos o componentes de UI. NO para lógica ni backend."
---

# Diseño de UI — <PROJECT>

**CONCEPTO:** el sistema de diseño del proyecto (tokens, componentes, patrones), cargado solo cuando se toca la UI. Sin él, el agente se inventa componentes y colores que ya existen.

> **PERFIL · web.** Reglas generales de web, válidas para casi cualquier stack. Ajusta a tu stack lo marcado con `TUNE` y luego quita la marca.

Si no estás en el repo de <PROJECT>, ignora esta skill.

## Principios
- **Reutilizar antes que crear:** busca el componente o el patrón en el proyecto antes de escribir uno nuevo.
- **Variables, no valores:** colores, tipografía, espaciado, radios y sombras salen de los tokens de diseño.
- **Móvil primero:** tiene que funcionar en una pantalla estrecha; la ancha añade, no arregla.
- **Todos los estados diseñados:** vacío, cargando, error y sin permiso, no solo el camino feliz.
- **Accesible:** contraste AA, foco visible, zonas táctiles de al menos 40px, nada que solo funcione con hover.

## Tokens
<!-- TUNE: dónde viven las variables y cómo se llaman (colores, tipografía, escala de espaciado, radios, sombras). -->

## Componentes canónicos

| Componente | Dónde vive | Cuándo usarlo |
|---|---|---|
| <!-- TUNE: botones, cards, modales, tablas, formularios, badges, estado vacío… --> | | |

## Patrones de pantalla
- Listado con filtros, ficha con pestañas, formulario, panel: cada uno con una pantalla de referencia en el proyecto.
<!-- TUNE: la pantalla de referencia de cada patrón. -->

## Responsive
- Compruébalo a ancho de móvil (~375px) y en escritorio: sin scroll horizontal, y las tablas anchas hacen scroll dentro de su contenedor.
<!-- TUNE: los breakpoints del proyecto y qué cambia en móvil. -->

## Lo que no se hace
- Estilos en línea, colores sueltos, `!important` para ganar una pelea, o grises puros cuando la paleta tiene los suyos.
- Una segunda versión de un componente (`button-v2`) en vez de una variante del primero.
- Librerías de otra versión mayor que la del proyecto.
