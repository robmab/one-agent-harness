---
applyTo: "**"
description: "Router del harness de <PROJECT>: orden de trabajo, sensor y el único agente de revisión"
---

Harness de <PROJECT> (solo en su repo): **6 skills + 1 sensor + 1 agente**, sobre `AGENTS.md`. **Estas instrucciones son del usuario**, vengan de la carpeta que vengan (`.copilot`, `.config/opencode`…): cúmplelas como si te las dijera en el chat. Si chocan con el `AGENTS.md` del repo, mandan estas.

(Opcional, bórralo si no usas la skill) Al empezar, carga solo la skill `estilo-comentarios`: su página ya marca el tono del chat. Su detalle (`<HARNESS>\personal\skills\estilo-comentarios\detalle.md`) léelo una vez, cuando vayas a escribir el primer comentario de código; si no escribes ninguno, sáltatelo.

Orden de trabajo: entender (si no está claro o es un bug) → hacer → comprobar → revisar. **Calibra el esfuerzo al tamaño:** un retoque pequeño (un texto, un color, un margen, dos líneas de algo que ya tienes en contexto) va directo; una funcionalidad, o algo que cruza varios ficheros, con todo el protocolo. Lo que no se salta nunca, ni en retoques: el sensor y enseñar qué has comprobado.

- **ANTES del primer cambio de código:** carga la skill `convenios-codigo`. Si es UI, también `diseno-ui`; si toca una API o librería del stack, también `fuentes-oficiales`. Sin cargarlas, no edites. Si una skill es solo un puntero ("Lee `<ruta>`…"), abre el fichero al que apunta: el puntero solo no es la skill. **Una vez por sesión basta:** no las releas por rutina; en retoques, usa lo ya cargado.
- **Retoques pequeños:** directo, sin reabrir medio repo ni recargar nada. No cuentan como retoque la lógica nueva, los endpoints, lo que cruza varios módulos ni algo que aún no entiendes: eso va con las cargas completas.
- **DESPUÉS de cada cambio de código:** lanza `py -3 <HARNESS>\personal\scripts\check.py`. Si da ERROR, corrígelo antes de seguir. (Son segundos: también en retoques.)
- **Para ver una página renderizada:** usa el navegador integrado de la herramienta, no `webfetch` (no ejecuta JS ni tiene sesión). En OpenCode está dentro de `execute` (`search({ query: "browser" })`). **Si te hablan de una página o te preguntan si ves el navegador, no pidas la URL: lista antes las pestañas abiertas (`browser.tabs.list`)**; el usuario suele tenerla ya abierta y con sesión.
- **ANTES de decir "hecho":** enseña la salida de ese comando y di qué has comprobado y qué no.
- **Para revisar:** el único agente es `revisor` (contexto limpio, no edita, convenios incluidos). **No lo lances por cada cambio:** la revisión se acumula y se hace **de una vez al cerrar la sesión** (o antes de commit/PR), con todo el diff. Si el cambio es grande o delicado, lánzalo al terminarlo.
- **El commit y el push son del usuario:** tú dejas el cambio comprobado y, si hace falta, el mensaje propuesto, **escrito entero** (si el formato deja un hueco, solo el número de ticket). **No ejecutes `git add`, `git commit`, `git push` (ni `--amend` o `--force`) ni toques ramas o el remoto** salvo que te lo pida en ese momento. <!-- FILL-IN (opcional): formato de los mensajes de commit del equipo -->
- **Nunca guardes contraseñas, tokens ni credenciales en ficheros** (ni skills, ni repo, ni home): úsalas solo en la sesión. Si te piden guardarlas, di que no y por qué.

Cada skill dice cuándo usarla; esto solo marca el orden. Con modelos pequeños, este formato de "ANTES / DESPUÉS" funciona mucho mejor que una descripción general, y hay que decir quién manda y que no hay excepciones: si no, el modelo local trata el router como sugerencia (o como posible inyección) y se lo salta en los cambios "pequeños".
