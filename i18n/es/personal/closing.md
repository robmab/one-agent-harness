# Cerrar la sesión

Léelo al cerrar la sesión, o antes de un commit o un PR. Va en este orden.

## 1. El revisor

**Solo cuando el usuario diga que cierra la sesión** (o lo pida antes de un commit o un PR). Al terminar un cambio, no: se lanza al cierre, no al acabar cada tarea. Una sola vez, con todo el diff de la sesión. Pásale **solo** esto:

```
Alcance: <ficheros o commits de la sesión>
Intención: <qué se quería hacer, en una línea>
```

Nada más: ni qué has comprobado, ni dónde tiene que mirar, ni una lista de cosas a revisar. Que lo saque él.

**Si el diff es grande** (`git diff HEAD --stat` pasa de ~30 ficheros, p. ej. un cambio repetido en muchas plantillas), en el alcance van con nombre los ficheros de lógica y, del resto, una muestra de 3 o 4 y el patrón del cambio. Míralo a los 3 minutos: si a los 5 no ha dado ni una vuelta, páralo y relánzalo acotado.

<!-- CHOOSE: cómo se revisa. Por defecto, un revisor recorre los 6 ejes (arriba). La alternativa, un subagente por eje, centra a cada uno y deja usar un modelo distinto por eje, pero cuesta unas 6 veces más tokens y mete ruido: pruébala solo si las retros enseñan un eje que se queda corto una y otra vez. En Claude Code un subagente no puede lanzar otros (compruébalo en tu herramienta), así que los lanzas todos desde aquí. Para usarla, cambia la frase "Una sola vez, con todo el diff de la sesión." del párrafo de arriba por esta:
**Una sola vez, con todo el diff de la sesión, un revisor por eje y a la vez:** seis lanzamientos con el mismo encargo más `Eje: <1-6>`. Para un modelo distinto por eje, haz una copia del agente por modelo (`reviewer-<modelo>`, mira la nota al principio del revisor). Cuando vuelvan los seis, **los juntas tú** antes del §2: un solo informe, sin duplicados (el mismo `fichero:línea` desde dos ejes es un hallazgo, con los dos ejes y la gravedad mayor), y el veredicto y la segunda pasada del más estricto. -->

**No lo esperes en bucle** (`Start-Sleep`, `sleep`, listar agentes una y otra vez): si tu herramienta avisa cuando el subagente termina, cierra el turno o sigue con otra cosa y retoma con el aviso. Si se cuelga, dilo y vuelve a lanzarlo con el mismo encargo, sin sustituirlo por una revisión hecha a mano.

## 2. Lo que encontró, entero

- Corrige lo que sea tuyo y compruébalo de nuevo.
- **Approver manual (una pasada):** si un arreglo cambia la lógica (no solo un texto, un comentario o un nombre; una guarda nueva, una condición o un cálculo **sí** son lógica), no relances el revisor por tu cuenta: dilo en la tabla (qué quedó sin revisar, y si toca un fichero compartido) y pregúntale al usuario si quiere otra pasada sobre eso. Si el revisor recomendó una segunda pasada, díselo en la misma pregunta; si dijo que no hace falta, no la ofrezcas. Si se lanza, acotada a lo que cambiaron los arreglos, no a todo el diff.
  <!-- CHOOSE: el modo del approver. El manual (arriba) encaja con una persona que revisa el diff igualmente: con una pasada basta. Para un flujo desatendido, cambia el punto de arriba por este:
  - **Approver automático (por rondas):** tras tus arreglos, vuelve a lanzar el revisor con el mismo encargo, acotado a lo que cambiaron los arreglos. Repite hasta que no quede ningún 🔴 ni 🟠, **como mucho 3 rondas**; entonces para y dile al usuario qué sigue abierto. Lo que se sale de la tarea nunca entra en el bucle: va a la tabla. Cada ronda va en la tabla. -->
- **Si un hallazgo choca con algo que el usuario decidió en la sesión** (un nombre, una ubicación, un enfoque), no se aplica: va a la tabla, junto a lo que decidió, y que elija.
- **Si un hallazgo se va a otro ticket**, dalo ya redactado en la tabla: título y dos líneas de descripción.
- **Cuéntale al usuario todos los hallazgos, en una tabla:** hallazgo · gravedad (bloqueante, importante, menor) · estado (arreglado; no, y por qué; ya decidido). Uno por fila, también los que no arreglas y también las **preguntas** (💭) del revisor, con lo que has visto o con "sin mirar". Antes de cerrar, coteja la tabla con el informe del revisor: que no se quede ninguno fuera.
- **Debajo de la tabla, siempre, la fila "Fuera del alcance (no tocado)"**: lo que se dejó para otro ticket u otro momento, o dijiste que quedaba por hacer, en toda la sesión, no solo lo del revisor (repasa tus mensajes), cada uno con su título y sus dos líneas; o "ninguno".

## 3. Limpieza

Borra **todos** los scripts temporales que creaste, lo que clonaste o copiaste en una carpeta temporal (un repo, un backup), y cualquier dato de prueba que no te hayan pedido conservar (o di cuál queda y cómo quitarlo). **Lo que el usuario te pidió crear se queda** mientras siga probando: para borrarlo, pregúntale antes. Después, `git status --short` (y el de cada repo anidado que hayas tocado) y enséñalo: la lista de lo tocado sale de ahí, no de memoria. Di qué ficheros nuevos quedan sin `git add`. Si hay un fichero que el usuario decidió no cambiar, deshazlo o pregúntale. Si tocaste el router, dile al usuario que reinicie la herramienta (lo carga al arrancar) y que en la próxima sesión `read_session.py --summary` no debe decir que faltan filas. Si hay algo en el índice (`git add`) que no pusiste tú, dilo tal cual, sin adivinar quién fue: el revisor no escribe.

**Debajo, una línea si algo toca zona delicada:** la base de datos (modelos, SQL, migraciones), código compartido, permisos o autenticación, configuración. Por ejemplo: «Mira con calma: `app/models/order.py` (BD)». Es solo un aviso para que sepa dónde mirar: no cambia nada más del cierre. Si no toca nada de eso, no pongas la línea.

**Y otra si queda algo por hacer al desplegar** (traducciones, una migración, una variable de entorno). Dila aunque ya la hayas dicho antes.

<!-- TUNE: las zonas delicadas de este proyecto (carpetas del núcleo, CSS compartido o plantillas base, facturación…). -->

## 4. El mensaje de commit

Solo ahora, con el revisor pasado y sus arreglos hechos, **y en cuanto lo estén**: no esperes a que el usuario repita que cierra. Si el diff cambia después, o aparece un repo que no habías visto, vuelve a proponerlo. El commit y el push son del usuario: no ejecutes `git add`, `git commit` ni `git push`.

- **Formato:** <!-- FILL-IN: el formato del equipo, p. ej. `[fix] #<ticket>: <título tal cual>. <descripción corta y no técnica>` -->
- Lo que no sepas (el ticket, por ejemplo) queda como hueco `<…>`, nunca inventado.
- Propón el mensaje entero, con la descripción ya escrita, aunque te pidan "solo la estructura".

## 5. El repaso, si lo quiere

**Es el penúltimo paso del cierre: sin esta pregunta, el cierre no está hecho.** Después del mensaje de cierre, hazla **con tu herramienta de preguntas**, no como texto: `vscode_askQuestions` en el chat de Copilot, `ask_user` en Copilot CLI, `ask_user_question` en DeepSeek, `question` en OpenCode (si no tienes ninguna, en un mensaje aparte que solo lleve la pregunta). La pregunta: **"¿Quieres el repaso del harness de esta sesión?"**. Si dice que sí, carga la skill `retro`. Si dice que no, o no contesta, nada más. **En una sesión de la fábrica** (desatendida, de `factory/intake.py`) no hay a quién preguntar: acaba el informe con "Repaso: pendiente". Cuando el usuario apruebe después esa rama, hazla entonces, sobre la sesión que dice el informe.

## 6. El estado, en el título

Un círculo delante del título de la pestaña enseña de un vistazo cómo va cada sesión, y qué le toca al usuario. Deja el título como está y solo añade, cambia o quita el prefijo; uno a la vez. Sin círculo, el agente está trabajando: al retomar una ⚪ o una 🔴, quítalo.

| Estado | Cuándo |
|---|---|
| ⚪ | analizada y a la espera de empezar: has dado el plan y esperas el sí del usuario, o una sesión de la fábrica paró en `before-code` |
| 🔴 | atascada: no puedes seguir sin el usuario (3 arreglos fallidos, un bloqueante sin resolver, algo que solo el usuario puede darte). Di en el mensaje qué necesitas. Una duda normal no es 🔴: pregunta y ya |
| 🟠 | pendiente: el usuario dice que lo deja, en cualquier momento, no solo al cerrar. Cuando se retome y se cierre, pasa a 🟢 |
| 🟢 | cerrada y bien: revisor decidido, arreglos hechos y, si lo ha pedido, repaso terminado |

Si tu herramienta no deja renombrar, dilo una vez.
