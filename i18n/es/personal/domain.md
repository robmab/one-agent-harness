# Negocio de <PROJECT>

Reglas de negocio que no se ven leyendo una pantalla: dónde vive cada dato, qué lo cambia y qué trampas tiene. Si algo de aquí no cuadra con el código, manda el código: dilo y se corrige. Van nombres de funciones y no números de línea, que cambian.

**Índice:** <!-- FILL-IN: un área por sección. --> Lee solo la sección que toca.

<!-- FILL-IN: empieza vacío y añade una entrada solo cuando a una sesión le haya costado entender una regla. Ejemplo: -->
## Facturas (ejemplo: cámbialo)

- **Dos datos distintos:** `Invoice.issued_at` dice cuándo se emitió; `Invoice.sent_at`, cuándo llegó al cliente. Emitirla no la envía.
- **Quién lo escribe:** `Invoice.issue()` y el proceso nocturno. Para la lista al día, `grep` de la asignación.
- **Trampa:** una factura emitida no se edita: lleva una factura rectificativa.
