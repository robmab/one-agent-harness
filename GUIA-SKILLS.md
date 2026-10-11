# Guía del core: qué hace cada pieza, cuándo entra y qué hay que rellenar

Esta guía es el **mapa de uso** de la plantilla: qué piezas trae, de qué tipo es cada una, en qué momento del trabajo actúa y cuánto hay que rellenar para un proyecto nuevo. Cómo se monta está en el [README](README.es.md); de dónde sale cada cosa, en [INVESTIGACION](INVESTIGACION.md).

> **La idea en una línea:** agente = modelo + harness. Las **guías** le dicen al agente qué saber y cómo trabajar *antes* de escribir; los **sensores** comprueban *después* lo que ha escrito. Solo guías: reglas que nadie comprueba. Solo sensores: un agente que repite los mismos fallos.

---

## 1. Los 3 tipos de pieza

![Los 3 tipos: conocimiento, proceso y control](img/tipos.svg)

| Tipo | Pregunta | Qué cubre | Piezas |
|---|---|---|---|
| 🔵 **Conocimiento** | ¿qué tiene que saber? | lo que el modelo no puede deducir leyendo el código ni sabe de memoria | `convenios-codigo`, `diseno-ui`, `fuentes-oficiales`, `estilo-comentarios` |
| 🟢 **Proceso** | ¿cómo tiene que trabajar? | las manías del modelo: inventarse requisitos, parchear a ciegas, decir "hecho" sin probar | `entrevistame`, `depuracion-sistematica`, `verificar-antes-de-acabar` |
| 🟠 **Control** | ¿quién lo comprueba? | mirar lo que ya está escrito, con una herramienta (fijo) o con otro modelo (juicio) | `comprobar` + hook, `revisor` |

Conocimiento y proceso son **guías** (skills, `SKILL.md`). Control son **sensores**: no son skills, sino un script y **un solo agente**. El revisor usa las skills de conocimiento como checklists (§6).

**Estado en la plantilla:**
- **LISTA:** vale tal cual.
- **AJUSTAR:** el método vale; hay que rellenar sus tablas del proyecto.
- **RELLENAR:** plantilla vacía; el contenido es del proyecto.
- **OPCIONAL:** fuera del core (`estilo-comentarios`).

## 2. Qué es el core

![Core = 6 skills + 1 sensor + 1 agente, sobre AGENTS.md; lo opcional, fuera](img/core.svg)

**Core = lo que aplica a cualquier tarea del proyecto, sea el módulo que sea:**

> **6 skills + 1 sensor + 1 agente**, sobre `AGENTS.md`

| Pieza | Qué es | Estado en la plantilla |
|---|---|---|
| **6 skills** | conocimiento: `convenios-codigo`, `diseno-ui`, `fuentes-oficiales`. Proceso: `entrevistame`, `depuracion-sistematica`, `verificar-antes-de-acabar` | 2 RELLENAR, 3 AJUSTAR, 1 LISTA |
| **1 sensor** | `comprobar` + hook | AJUSTAR (`MARCADOR`, `REGLAS`…) |
| **1 agente** | `revisor` | LISTA |
| **base** | `AGENTS.md`, el índice que entra siempre | `AGENTS.plantilla.md` |

Se puede ver también por de dónde sale el contenido:
- **Del proyecto:** `AGENTS.md`, `convenios-codigo`, `diseno-ui`, la tabla de `fuentes-oficiales` y las `REGLAS` del sensor. Se rellena para cada proyecto, o se apunta al repo del equipo si ya lo tiene.
- **Del método:** las tres skills de proceso, el motor del sensor y el agente `revisor`. Valen para cualquier proyecto sin tocarlos (o casi).

**Opcional · fuera del core:**
- **Personal:** `estilo-comentarios`, tu voz en comentarios y chat. Cada uno tendría el suyo.
- **Lo de un módulo o pantalla concreta:** skills que solo entran bajo demanda, con una `description` muy precisa para que no se disparen en cualquier tarea.
- **Lo que está en espera:** commits, planes de ticket, traducciones, migraciones, recibir revisiones. Solo entran si algo falla de verdad y se repite (§6).

## 3. El flujo de trabajo

![Flujo de un ticket: arrancar, entender, hacer, comprobar, revisar](img/flujo.svg)

| Fase | Qué pasa | Piezas |
|---|---|---|
| **0 · Arrancar** | al abrir sesión entra el índice del repo y tu forma de hablar | `AGENTS.md` (siempre), `estilo-comentarios` (hook `SessionStart` en Claude) |
| **1 · Entender** | si no está claro qué piden: preguntas de una en una, mirando antes el repo. Si es un bug: reproducir, localizar la capa y una hipótesis cada vez | `entrevistame`, `depuracion-sistematica` |
| **2 · Hacer** | escribe con los convenios, el design system si es UI y las versiones reales del stack. **Tras cada edición**, el hook pasa el comprobador: si hay error, Claude lo corrige antes de seguir (el bucle naranja) | `convenios-codigo`, `diseno-ui`, `fuentes-oficiales`, `comprobar` |
| **3 · Comprobar** | antes de decir "hecho": comando ejecutado y salida leída, o el navegador si es una pantalla. Lo que no se pueda probar se dice: «Sin comprobar» | `verificar-antes-de-acabar` (+ el comprobador a mano en Copilot) |
| **4 · Revisar y cerrar** | revisión a fondo con contexto limpio, convenios incluidos, usando las skills de conocimiento como checklists. No edita: decides tú qué se aplica y haces el commit | `revisor` |

Si en la fase 3 algo no está hecho, se vuelve a la 2. Si en la 2 aparece un bug, se pasa por `depuracion-sistematica`.

## 4. Fichas

### 🔵 `convenios-codigo` · RELLENAR
- **Qué:** cómo se escribe el código del proyecto: stack, nombrado, dónde va la lógica, base de datos, frontend, anti-patrones y formato.
- **Qué rellenar:** las secciones de la plantilla, con reglas de una línea que valgan siempre (700 palabras como mucho). Si el equipo ya tiene convenios en su repo, solo un puntero a ese fichero.
- **Entra:** sola, antes de escribir o revisar cualquier código.

### 🔵 `diseno-ui` · RELLENAR
- **Qué:** el design system: tokens, componentes canónicos, patrones de pantalla, responsive.
- **Qué rellenar:** las secciones. Si crece, un índice aquí y el detalle en ficheros al lado que se lean bajo demanda.
- **Entra:** sola, **solo** con maquetación, estilos o componentes de UI.

### 🔵 `fuentes-oficiales` · AJUSTAR
- **Qué:** las versiones reales del stack, sus trampas y el orden para informarse: repo → trampas → doc oficial de esa versión.
- **Tapa:** que el modelo escriba de memoria la última versión de cada librería. Visto en la práctica: un modelo local metió `slot-scope` (Vue 2.5) en un proyecto con Vue 2.3: el slot salía vacío sin avisar.
- **Qué rellenar:** la tabla del stack (versión, dónde se ve, doc de esa versión) y las trampas, una línea por trampa con lo que **sí** se usa.
- **Entra:** sola con modelos buenos. Con modelos locales pequeños, a mano: `/fuentes-oficiales`.

### 🔵 `estilo-comentarios` · OPCIONAL (fuera del core)
- **Qué:** tu voz: cómo quieres los comentarios (longitud, tono, cuándo sí y cuándo no) y el tono del chat.
- **Qué rellenar:** tus reglas, y en el detalle, **ejemplos reales tuyos**. Si no te importa cómo comenta el agente, bórrala.
- **Entra:** Claude, por el hook `SessionStart`; Copilot, según el modelo (o `/estilo-comentarios`).

### 🟢 `entrevistame` · LISTA
- **Qué:** cuando un ticket no está claro, ni para el agente ni para ti. Primero **mira en el repo** qué hace hoy eso; luego hipótesis con %, **una pregunta cada vez con su suposición**, y un resumen con la línea "Fuera" obligatoria. Lo que solo sabe el cliente va a una lista de **preguntas para el cliente**.
- **Opcional:** lo que suele faltar en los tickets de ese proyecto.
- **Entra:** cuando se lo pides ("entrevístame", "no sé a qué se refiere este ticket") o si el ticket no deja claro el qué, para quién o por qué. Nunca en tareas mecánicas.

### 🟢 `depuracion-sistematica` · AJUSTAR
- **Qué:** sin causa raíz no hay arreglo. Reproducir → seguir el dato por las capas → una hipótesis cada vez → un solo arreglo. **Con 3 arreglos fallidos, para**: el problema es de diseño.
- **Qué rellenar:** la tabla de capas de la aplicación y cómo mirar cada una, y las trampas propias del proyecto.
- **Entra:** sola, ante un bug o un error, antes de proponer ningún arreglo.

### 🟢 `verificar-antes-de-acabar` · AJUSTAR
- **Qué:** nada de "hecho" sin una prueba ejecutada en ese mismo mensaje, y una salida honrada: «Comprobado» / «Sin comprobar».
- **Tapa:** visto en la práctica: un modelo potente dijo "validado sin errores de editor" sin haber ejecutado nada.
- **Qué rellenar:** las filas de la tabla con los comandos reales (tests, lint, build…).
- **Entra:** sola, al ir a dar algo por terminado o antes de un commit.

### 🟠 `comprobar` + hook · AJUSTAR
- **Qué:** `personal\scripts\comprobar.py`, solo con la librería estándar.
  - Pasa las `REGLAS` (regex con `ERROR` o `AVISO`) por los ficheros.
  - Compila los `.py` con el Python del proyecto.
  - Pasa `node --check` por los `.js` que no lleven plantillas.
- **Qué rellenar:**
  - `MARCADOR`: un fichero que solo exista en ese repo. Obligatorio si convives con otros proyectos.
  - `PYTHON_PROYECTO`.
  - `REGLAS`: las trampas de `fuentes-oficiales` que se puedan pillar con una regex. Es la forma más fiable de que no se repitan.
- **Entra:**
  - **Claude:** automático, tras **cada** edición (hook `PostToolUse` del plugin). Un error le llega como bloqueante y lo corrige antes de seguir.
  - **Copilot:** no hay hook; lo lanza `verificar` o tú:
    ```bash
    py -3 <HARNESS>/personal/scripts/comprobar.py
    ```
    (Sin argumentos revisa lo cambiado en git.)

### 🟠 `revisor` · LISTA
- **Qué:** el **único agente** del harness. Hace una revisión a fondo con contexto limpio, en 6 ejes: **convenios**, corrección, seguridad, rendimiento, arquitectura y legibilidad.
  - Antes pasa el comprobador y lee como **checklists** las skills de conocimiento que tocan: `convenios-codigo` siempre, `diseno-ui` si hay UI y `fuentes-oficiales` si se usan APIs del stack. Las que sigan sin rellenar, se las salta y lo dice.
  - **No edita:** cada hallazgo va con `fichero:línea` y su arreglo propuesto (lo mecánico, como cambio exacto), y termina con un veredicto.
- **Opcional:** las trampas del proyecto que hay que mirar siempre (cómo se declaran los permisos, el N+1 típico del ORM…) y otras checklists propias.
- **Entra:** a mano, antes del commit o de la PR, o para revisar una rama.

## 5. Cómo entra cada pieza

| Pieza | Claude Code | Copilot (VS Code) |
|---|---|---|
| `AGENTS.md` | siempre, al arrancar | siempre |
| `estilo-comentarios` | hook `SessionStart` | según el modelo; si no, `/estilo-comentarios` |
| `convenios-codigo`, `diseno-ui` | sola, por su `description` | sola |
| `fuentes-oficiales`, `depuracion-sistematica`, `verificar-antes-de-acabar` | sola, por su `description` | con modelos buenos, sola; con locales, a mano: `/nombre` |
| `entrevistame` | cuando se lo pides o el ticket es ambiguo | ídem, o `/entrevistame` |
| `comprobar` | **automático** tras cada edición | a mano o desde `verificar` |
| `revisor` | a mano (subagente) | a mano (selector de agentes) |

**Para saber si una skill ha entrado:**
- **Claude:** sale "Habilidad ejecutada /<proyecto>:…" en la respuesta.
- **Copilot:** despliega las referencias usadas de la respuesta y mira si aparece el `SKILL.md`.

Si no entra cuando debería, **primero se mejora la `description`** (palabras concretas que enganchen); solo como último recurso se fuerza.

## 6. Antes de añadir algo nuevo

Cada skill cuesta aunque no se use: su `description` está siempre en el catálogo, y cuantas más hay, más se dispara la que no toca. El criterio:

| Tipo | Se añade cuando… | No se añade si… |
|---|---|---|
| 🔵 Conocimiento | hay algo que el modelo **no puede saber** ni deducir del código | ya está en los convenios o se ve leyendo el repo |
| 🟢 Proceso | hemos **visto** al modelo fallar así, y se repite | es "por si acaso" o lo haces tú en diez segundos |
| 🟠 Control | una regla importa y se puede comprobar con una herramienta | depende del juicio de cada caso (eso va al `revisor`) |

Si un fallo concreto se repite, lo primero es ver si cabe como **regla nueva en `REGLAS`**: es lo más fiable y no gasta contexto. Qué se podría añadir si hay señal, y qué conviene no meter, está en el catálogo de [SKILLS-OPCIONALES](SKILLS-OPCIONALES.md).

### Un solo agente; los demás revisores, como skills

Se puso de moda tener muchos revisores (de seguridad, de rendimiento, de accesibilidad…). Aquí no: **un agente nuevo solo compensa** si hacen falta ojos frescos, permisos distintos o aislar un trabajo pesado. Las tres cosas ya las cubren el `revisor` y los agentes de búsqueda que traen las herramientas.

Cada subagente empieza sin contexto, gasta bastantes más tokens y pierde parte de lo que descubre al devolver el resultado. Además, varios revisores repasan el mismo diff varias veces.

**Si hace falta un "revisor de X":**
1. Se escribe como **skill** con su checklist (`revision-accesibilidad`, por ejemplo).
2. Se añade a la tabla de checklists del `revisor`, con su "cuándo".
3. Lo que se pueda comprobar con una regex, a `REGLAS`.

Así sigue habiendo una sola pasada, un solo informe y un agente que no toca el código.

Cómo escribir una skill para que funcione está en el [README §4](README.es.md#4-día-a-día).
