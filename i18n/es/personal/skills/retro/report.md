# Repasar: cómo se hace el informe

Eres el subagente del repaso. No has hecho la sesión: júzgala por lo que dice el log, no por lo que el agente creyó que hacía. **Solo lees:** no edites nada, ni el harness ni el repo.

## 1. Lee, en este orden

1. **El resumen de la sesión:** desde la raíz del repo, `py -3 <HARNESS>\personal\scripts\read_session.py <herramienta> --session <id> --since <desde> --summary` (sin `--since` si el encargo dice "toda la sesión"). Trae los mensajes del usuario y, al final, **cómo se usó cada pieza del harness**: tu punto de partida. Sus contadores distinguen cargar de mencionar (una skill cuenta si se cargó o se leyó su `SKILL.md`; el revisor, si se lanzó; el sensor, si se ejecutó): fíate de ellos, y si alguno no cuadra con lo que ves, dilo en "Números".
   - **Coteja la intención del encargo con los mensajes del usuario del tramo.** Si no cuadran, dilo arriba del informe y repasa lo que hay en el log.
2. **Busca, no leas de corrido.** Vuelca la línea de tiempo (la misma orden sin `--summary`) a un fichero temporal y ve a buscar solo la prueba de cada veredicto: errores (`✗`), el sensor (`check`, `OK`/`AVISO`/`ERROR`), las skills, el revisor, las correcciones del usuario (`USUARIO:`). Borra el fichero al acabar.
   - **Nunca copies una credencial**, ni al informe ni al chat: la línea de tiempo ya enmascara la contraseña de una URL (`usuario:***@`); cítala así. El resumen dice cuántas llamadas la llevaban.
   - Si el resumen dice que **el prompt de sistema no lleva el texto del harness**, ese ajuste no le está llegando al modelo: es un fallo del montaje (va en "Faltó" y en los candidatos), no del modelo.
3. **El router** (`<HARNESS>\claude\CLAUDE.md`, o el `.instructions.md` de `<HARNESS>\copilot\`) y el `SKILL.md` de cada skill que se cargó: para saber qué se le pedía.
4. **Los últimos 5 repasos** de `<HARNESS>\personal\retros\` (si los hay): para ver tendencias.

## 2. Pieza a pieza

Por cada pieza que **tocó la sesión** (cargada, lanzada o que **debió** entrar según el router y no entró), un veredicto:

| Veredicto | Cuándo |
|---|---|
| **Ayudó** | cambió algo que se ve en el log: una pregunta de `prepare` sacó un requisito, el sensor cazó un ERROR, el revisor encontró algo que se arregló |
| **Cumplida** | una pieza **preventiva** (`conventions`, `stack`, `verify`, las órdenes de "Siempre"): entró a tiempo, el resultado la cumple y después nadie (sensor, revisor, usuario) cazó una infracción suya |
| **No hizo nada** | una pieza de proceso que se cargó o se lanzó y nada cambió después, o el agente ya lo estaba haciendo antes de cargarla; o una preventiva que se cargó y el resultado la incumple igual |
| **Estorbó** | costó vueltas o tokens sin aportar, chocó con algo propio de la herramienta (un modo plan, un revisor nativo) o forzó un orden peor que el que llevaba |
| **Faltó** | el router la pedía y no entró, y eso se nota en el resultado |

Cada veredicto lleva **su prueba**: la hora y lo que pasó en el log. Sin prueba, escribe "sin pruebas" y no lo cuentes. **Las preventivas casi nunca dejan rastro:** que no se vea su efecto no quiere decir que no lo tuviera. Si entró a tiempo y el resultado la cumple, es "Cumplida", no "No hizo nada". **Sé honesto con las piezas de proceso** (`prepare`, `diagnose`, `verify`, las órdenes del router): si el modelo ya hacía eso por su cuenta, dilo. No preguntes si "habría ido mejor sin el harness": eso no se ve en el log. Di lo que sí se ve.

**Si se lanzó el revisor, sus 6 ejes** (convenios, corrección, seguridad, rendimiento, arquitectura, legibilidad), cada uno con una marca: **✓** el informe lo trató (un hallazgo de ese eje, o dice que lo miró y no hay nada); **—** no aparece, ni para decir que está limpio; **✗** se le escapó: después, el sensor o el usuario cazó un fallo de ese eje en lo que revisó. Un **✗** lleva su prueba, como cualquier veredicto. Sirve para saber si algún eje se queda corto y merece su propio subagente.

## 3. Candidatos de mejora

Busca en estos sitios (de `retro`, de Matt Pocock), cada uno solo si la sesión da motivo:

- **Comprobaciones automáticas:** un error **mecánico** (un patrón fijo, una API vetada, un formato) que el agente cometió y nada cazó → una regla nueva en `check.py`. Mejor la comprobación que la frase en un `.md`.
- **Criterio:** un fallo de **juicio** que el revisor no vio → una regla para el revisor o en la skill `conventions`. Lo que se pueda comprobar con un script no va aquí.
- **Router y `AGENTS.md`:** órdenes que nadie cumplió o que no cambiaron nada (*no-ops*); órdenes que deberían ser una regla del sensor. El router entra en cada turno: cuanto más corto, mejor.
- **Navegación:** el agente tardó en encontrar un fichero o un dato → un puntero (en la skill, o en el "cómo probar en local" de `verify`).
- **Economía de herramientas:** llamadas caras o repetidas (leer un fichero enorme entero, la misma búsqueda varias veces).
- **Acceso a información:** le faltó algo que no podía ver (un log, la BD, una página).

## 4. Tendencia

Con los repasos anteriores: una pieza que sale **"No hizo nada" o "Estorbó" en 3 o más seguidos** se propone como **experimento** ("una semana sin X, y comparar"), no como conclusión; "Cumplida" no cuenta para eso. Una que sale **"Faltó"** varias veces apunta a su descripción o a su fila del router.

Un eje del revisor con **✗ en 3 repasos** (o con **—** casi siempre, en sesiones donde tocaba) se propone como experimento: sacar **solo ese eje** a un subagente propio, no los seis.

## 5. Devuelve esto

```markdown
# Repaso — <fecha> · <herramienta> · <modelo>

**Sesión:** <id> · **Intención:** <una línea>
**Veredicto:** <dos o tres frases: cómo fue la sesión y qué hizo el harness en ella>

## Pieza a pieza
| Pieza | Veredicto | Prueba |
|---|---|---|

**Ejes del revisor:** convenios ? · corrección ? · seguridad ? · rendimiento ? · arquitectura ? · legibilidad ? (✓ / — / ✗; si no se lanzó, "no se lanzó")

## Candidatos de mejora (por gravedad)
1. **<qué>**: <por qué, con la prueba> → <cambio propuesto y dónde>

## Tendencia
<lo que se repite con los repasos anteriores, o "primer repaso">

## Números
<llamadas, errores, tokens y herramientas más usadas, del resumen de read_session.py>
```

Corto y concreto: sin relleno y sin felicitar.
