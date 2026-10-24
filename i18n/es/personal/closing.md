# Cerrar la sesión

Léelo al cerrar la sesión, o antes de un commit o un PR. Va en este orden.

## 1. El revisor

**Solo cuando el usuario diga que cierra la sesión** (o lo pida antes de un commit o un PR). Al terminar un cambio, no: se lanza al cierre, no al acabar cada tarea. Una sola vez, con todo el diff de la sesión. Pásale **solo** esto:

```
Alcance: <ficheros o commits de la sesión>
Intención: <qué se quería hacer, en una línea>
```

Nada más: ni qué has comprobado, ni dónde tiene que mirar, ni una lista de cosas a revisar. Que lo saque él.

<!-- CHOOSE: cómo se revisa. Por defecto, un revisor recorre los 6 ejes (arriba). La alternativa, un subagente por eje, centra a cada uno y deja usar un modelo distinto por eje, pero cuesta unas 6 veces más tokens y mete ruido: pruébala solo si las retros enseñan un eje que se queda corto una y otra vez. En Claude Code un subagente no puede lanzar otros (compruébalo en tu herramienta), así que los lanzas todos desde aquí. Para usarla, cambia la frase "Una sola vez, con todo el diff de la sesión." del párrafo de arriba por esta:
**Una sola vez, con todo el diff de la sesión, un revisor por eje y a la vez:** seis lanzamientos con el mismo encargo más `Eje: <1-6>`. Para un modelo distinto por eje, haz una copia del agente por modelo (`reviewer-<modelo>`, mira la nota al principio del revisor). Cuando vuelvan los seis, **los juntas tú** antes del §2: un solo informe, sin duplicados (el mismo `fichero:línea` desde dos ejes es un hallazgo, con los dos ejes y la gravedad mayor), y el veredicto y la segunda pasada del más estricto. -->

**No lo esperes en bucle** (`Start-Sleep`, `sleep`, listar agentes una y otra vez): si tu herramienta avisa cuando el subagente termina, cierra el turno o sigue con otra cosa y retoma con el aviso. Si se cuelga, dilo y vuelve a lanzarlo con el mismo encargo, sin sustituirlo por una revisión hecha a mano.

## 2. Lo que encontró, entero

- Corrige lo que sea tuyo y compruébalo de nuevo.
- **Approver manual (una pasada):** si un arreglo cambia la lógica (no solo un texto, un comentario o un nombre; una guarda nueva, una condición o un cálculo **sí** son lógica), no relances el revisor por tu cuenta: dilo en la tabla (qué quedó sin revisar, y si toca un fichero compartido) y pregúntale al usuario si quiere otra pasada sobre eso. Si el revisor recomendó una segunda pasada, díselo en la misma pregunta.
  <!-- CHOOSE: el modo del approver. El manual (arriba) encaja con una persona que revisa el diff igualmente: con una pasada basta. Para un flujo desatendido, cambia el punto de arriba por este:
  - **Approver automático (por rondas):** tras tus arreglos, vuelve a lanzar el revisor con el mismo encargo, acotado a lo que cambiaron los arreglos. Repite hasta que no quede ningún 🔴 ni 🟠, **como mucho 3 rondas**; entonces para y dile al usuario qué sigue abierto. Lo que se sale de la tarea nunca entra en el bucle: va a la tabla. Cada ronda va en la tabla. -->
- **Si un hallazgo se va a otro ticket**, dalo ya redactado en la tabla: título y dos líneas de descripción.
- **Cuéntale al usuario todos los hallazgos, en una tabla:** hallazgo · gravedad (bloqueante, importante, menor) · estado (arreglado; no, y por qué; ya decidido). Uno por fila, también los que no arreglas. Antes de cerrar, coteja la tabla con el informe del revisor: que no se quede ninguno fuera.

## 3. Limpieza

Borra **todos** los scripts temporales que creaste, y cualquier dato de prueba que no te hayan pedido conservar (o di cuál queda y cómo quitarlo). **Lo que el usuario te pidió crear se queda** mientras siga probando: para borrarlo, pregúntale antes. Después, `git status --short` y enséñalo: la lista de lo tocado sale de ahí, no de memoria. Si hay un fichero que el usuario decidió no cambiar, deshazlo o pregúntale.

**Debajo, una línea si algo toca zona delicada:** la base de datos (modelos, SQL, migraciones), código compartido, permisos o autenticación, configuración. Por ejemplo: «Mira con calma: `app/models/order.py` (BD)». Es solo un aviso para que sepa dónde mirar: no cambia nada más del cierre. Si no toca nada de eso, no pongas la línea.

<!-- TUNE: las zonas delicadas de este proyecto (carpetas del núcleo, CSS compartido o plantillas base, facturación…). -->

## 4. El mensaje de commit

Solo ahora, con el revisor pasado y sus arreglos hechos, **y en cuanto lo estén**: no esperes a que el usuario repita que cierra. Si el diff cambia después, vuelve a proponerlo. El commit y el push son del usuario: no ejecutes `git add`, `git commit` ni `git push`.

- **Formato:** <!-- FILL-IN: el formato del equipo, p. ej. `[fix] #<ticket>: <título tal cual>. <descripción corta y no técnica>` -->
- Lo que no sepas (el ticket, por ejemplo) queda como hueco `<…>`, nunca inventado.
- Propón el mensaje entero, con la descripción ya escrita, aunque te pidan "solo la estructura".

## 5. El repaso, si lo quiere

**Es el último paso del cierre: sin esta pregunta, el cierre no está hecho.** Después del mensaje de cierre, hazla **con tu herramienta de preguntas**, no como texto: `vscode_askQuestions` en el chat de Copilot, `ask_user` en Copilot CLI, `ask_user_question` en DeepSeek, `question` en OpenCode (si no tienes ninguna, en un mensaje aparte que solo lleve la pregunta). La pregunta: **"¿Quieres el repaso del harness de esta sesión?"**. Si dice que sí, carga la skill `retro`. Si dice que no, o no contesta, nada más. **En una sesión de la fábrica** (desatendida, de `factory/intake.py`) no hay a quién preguntar: acaba el informe con "Repaso: pendiente". Cuando el usuario apruebe después esa rama, hazla entonces, sobre la sesión que dice el informe.
