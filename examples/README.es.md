# Ejemplos: las skills de método completas

🌐 [English](README.md) · **Español**

Las skills de la plantilla (`personal\skills\`) vienen como **plantillas**: cada una empieza con su concepto y deja sus apartados en `FILL-IN`. Aquí están las **versiones completas** de las cuatro skills de método, tal como estaban en la v0.4.0, para copiar una o sacar ideas.

**No las carga ninguna herramienta:** `setup.py` solo enlaza `personal\skills\`. Son de referencia, no forman parte del harness.

| Ejemplo | Qué cubre | De dónde sale |
|---|---|---|
| `prepare` | aclarar antes de hacer (una pregunta cada vez, con tu suposición) y, si es grande, un plan corto que aprueba el usuario; el detalle de la entrevista en `interview.md` | addyosmani `interview-me` + la idea de superpowers `writing-plans` |
| `diagnose` | causa raíz antes de arreglar: reproducir, seguir el dato por las capas, una hipótesis cada vez | superpowers `systematic-debugging` |
| `verify` | nada de "hecho" sin una prueba ejecutada y leída; cómo probar en local y en el navegador | superpowers `verification-before-completion` |
| `stack` | código para las versiones reales del stack: primero el repo, luego la doc de esa versión | addyosmani `source-driven-development` |

`conventions`, `ui` y `voice` no tienen ejemplo: su contenido es del proyecto (o tuyo) desde la primera línea.

## Cómo usar uno

1. **Cópialo encima de la plantilla** (con sus ficheros al lado): `examples\skills\<nombre>\` → `personal\skills\<nombre>\`.
2. **Rellena lo que siga marcado como `FILL-IN`** (las tablas del proyecto: capas, comandos, versiones) y cambia `<PROJECT>` y `<HARNESS>`: `setup.py` no toca esta carpeta.
3. **Deja la línea `**CONCEPTO:**`** arriba, o escríbela si partes de la tuya: es lo que le dice al modelo por qué están las reglas.
4. **Quita lo que no uses.** Son ejemplos, no la norma: una skill más corta que encaje en tu proyecto funciona mejor que una completa que no.

En el repo de la plantilla, las versiones en español están en `i18n\es\examples\`; con `setup.py --lang es` se instalan aquí, con los mismos nombres.
