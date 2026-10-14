# Skills opcionales: el catálogo

🌐 [English](OPTIONAL-SKILLS.md) · **Español**

Skills **interesantes pero no necesarias**, sacadas sobre todo de los dos repos que mejor encajan: [obra/superpowers](https://github.com/obra/superpowers) y [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), los dos con licencia MIT. Están revisadas una a una (2026-10-11): qué aportan, **qué señal** indica que merece la pena meterla y **qué ruido** mete si se pone sin necesidad.

> **Por defecto, ninguna.** El core (6 skills + 1 sensor + 1 agente, ver [SKILLS-GUIDE §2](SKILLS-GUIDE.es.md#2-qué-es-el-core)) cubre el trabajo diario. Cada skill que se añade:
> - **ocupa sitio siempre:** su `description` está en el catálogo aunque no se use;
> - **compite con las demás:** cuantas más hay, más se dispara la que no toca, sobre todo con modelos locales;
> - **puede contradecir al core:** otra forma de depurar, de planificar, de revisar…;
> - **pesa:** las originales tienen entre 400 y 4.900 palabras.
>
> Una opcional solo entra con una **señal concreta**: un fallo que se repite o una situación que vuelve a menudo. Nunca "por si acaso".

---

## Cómo meter una (si hay señal)

1. **Una sola cada vez.** Si metes tres y algo va peor, no sabrás cuál ha sido.
2. **Adáptala, no la copies:**
   - en el idioma en que hablas con el modelo y recortada a 600 palabras como mucho;
   - con la `description` estrecha, que diga **cuándo** y con palabras concretas;
   - sin escribir en el repo;
   - con el crédito "Adaptada de X (MIT)" al pie y su aviso de copyright en `THIRD-PARTY-NOTICES.md`.
3. **Si solo la va a usar el revisor** (una checklist de seguridad o de rendimiento), no la metas en `skills\`. Guárdala en `personal\checklists\`, fuera del catálogo, y añádela a la tabla de checklists del `reviewer`. Así no le añade ruido al agente principal.
4. **Pruébala dos semanas** en trabajo real: ¿entra cuando toca? ¿se dispara cuando no? ¿el resultado es mejor?
5. **Si no aporta, fuera.** Quitarla no cuesta nada.

---

## 1. Ya cubiertas por el core: no meter

Duplicarían algo que ya está, y dos skills para el mismo momento se pisan.

| Skill (origen) | Ya la cubre | Por qué no |
|---|---|---|
| `debugging-and-error-recovery` (addy) | `systematic-debugging` | mismo método; la del core viene de la versión de superpowers, más estricta |
| `code-review-and-quality`, `requesting-code-review` (addy, sp) | agente `reviewer` | el revisor ya usa sus ejes |
| `interview-me` (addy) | `interview-me` | es su origen |
| `source-driven-development` (addy) | `official-sources` | es su origen |
| `verification-before-completion` (sp) | `verify-before-done` | es su origen |
| `context-engineering`, `using-agent-skills` (addy) | el propio harness | son skills para montar lo que ya está montado |

---

## 2. Opcionales con sentido

### Antes de programar: definir y planificar

| Skill (origen) · palabras | Qué aporta | Métela si… | Ruido si no |
|---|---|---|---|
| `planning-and-task-breakdown` (addy) · 1.700 | parte el trabajo en tareas ordenadas y comprobables | llegan tickets gordos y el agente intenta hacerlo todo de golpe | en tickets normales, planifica lo que se hace en diez minutos |
| `writing-plans` (sp) · 1.600 | planes muy detallados, con fichero, código y comprobación por tarea | delegas tareas largas a un agente que trabaja solo | escribe planes en ficheros del repo; mucha ceremonia |
| `spec-driven-development` (addy) · 2.000 | escribe la especificación (PRD) antes del código | features nuevas grandes, con varias personas implicadas | duplica a `interview-me` en lo pequeño; papeleo |
| `idea-refine` (addy) · 1.300 | genera variantes de una idea y luego las cierra | diseñas algo nuevo desde cero, sin requisitos | en mantenimiento, abre opciones que nadie pidió |
| `api-and-interface-design` (addy) · 2.200 | contratos estables entre módulos o entre front y back, endpoints | estás diseñando una API pública o una integración | en código interno, sobrediseño |

### Mientras programas

| Skill (origen) · palabras | Qué aporta | Métela si… | Ruido si no |
|---|---|---|---|
| `incremental-implementation` (addy) · 1.500 | cambios en trozos finos, cada uno comprobable | el agente toca 15 ficheros de golpe y luego no sabe qué rompió | frena los cambios pequeños |
| `code-simplification` (addy) · 2.000 | simplificar sin cambiar el comportamiento | hay módulos heredados que se refactorizan a menudo | se pone a "mejorar" lo que no se le ha pedido |
| `frontend-ui-engineering` (addy) · 1.600 | UI accesible (WCAG), responsive y con estado bien llevado | la accesibilidad es requisito | solapa con `ui-design`; coge solo lo de accesibilidad |
| `test-driven-development` (addy o sp) · 1.500-2.400 | rojo-verde-refactor obligatorio | **hay una base de tests que funciona** y el equipo la mantiene | sin tests es dañina: la de superpowers **borra el código escrito antes que su test** |
| `performance-optimization` (addy) · 2.500 | medir, perfilar y optimizar (N+1, Core Web Vitals…) | hay un problema de rendimiento **medido** | optimiza sin medir; mejor como checklist del revisor |

### Revisar y cerrar

| Skill (origen) · palabras | Qué aporta | Métela si… | Ruido si no |
|---|---|---|---|
| `receiving-code-review` (sp) · 900 | comprobar cada comentario de revisión antes de aplicarlo; nada de "¡tienes razón!" | recibes muchos comentarios de PR o de otros revisores y el agente los aplica a ciegas | tú ya decides qué se aplica del `reviewer` |
| `security-and-hardening` (addy) · 2.500 | modelo de amenazas, OWASP, secretos, subida de ficheros, funciones con IA | el proyecto maneja datos sensibles o pagos, o abre APIs al exterior | el revisor ya tiene un eje de seguridad; mejor como **checklist** suya |
| `git-workflow-and-versioning` (addy) · 2.200 | commits atómicos, ramas, partir trabajo desordenado en commits limpios | delegas commits y ramas al agente | su `description` dice "cualquier cambio de código": se dispararía siempre |
| `finishing-a-development-branch` (sp) · 1.300 | al acabar: merge, PR, conservar o descartar la rama | trabajas con muchas ramas cortas | da por hecho que hay tests y worktrees |
| `documentation-and-adrs` (addy) · 1.600 | dejar escritas las decisiones de arquitectura (ADR) | se toman decisiones gordas que luego nadie recuerda | documenta cosas triviales |

### Producción e infraestructura

| Skill (origen) · palabras | Qué aporta | Métela si… | Ruido si no |
|---|---|---|---|
| `deprecation-and-migration` (addy) · 2.000 | retirar código o APIs; migraciones de BD sin parada (expand/contract) | hay una migración grande en marcha (de versión, de esquema, de sistema) | en el día a día no aplica |
| `observability-and-instrumentation` (addy) · 2.200 | logs, métricas, trazas y alertas | hay problemas en producción que no se pueden diagnosticar | llena el código de logs |
| `ci-cd-and-automation` (addy) · 1.600 | pipelines, quality gates en CI | se está montando o cambiando el CI | si no hay CI que tocar, no aplica |
| `shipping-and-launch` (addy) · 1.800 | checklist de salida a producción, rollout por fases, rollback | se hacen lanzamientos con riesgo | si el despliegue es rutinario, no aplica |
| `browser-testing-with-devtools` (addy) · 2.100 | probar en un navegador real: DOM, consola, red, rendimiento | Copilot o una herramienta sin navegador, **con el MCP chrome-devtools** instalado | Claude ya tiene navegador propio; sin el MCP no funciona |

### Meta: para escribir skills

| Skill (origen) · palabras | Qué aporta | Uso recomendado |
|---|---|---|
| `writing-skills` (sp) · 3.800 | cómo escribir skills que se disparen bien; probarlas como si fueran tests | **solo como lectura** al escribir una skill nueva; lo esencial ya está en el [README §4](README.es.md#4-día-a-día) |
| `skill-creator` ([anthropics/skills](https://github.com/anthropics/skills)) | guía oficial del formato | igual: como lectura; revisa su licencia antes de copiar nada (no todo el repo es MIT) |

---

## 3. Desaconsejadas: perjudican

Aunque vengan de repos muy usados, chocan con el diseño de este harness:

| Skill (origen) | Por qué no |
|---|---|
| `brainstorming` (sp) | su `description` es "**MUST** antes de cualquier trabajo creativo": se dispara en casi todo y frena |
| `using-superpowers` (sp) | obliga a invocar skills **antes de cualquier respuesta**, incluso para preguntar; ruido puro |
| `subagent-driven-development`, `executing-plans`, `dispatching-parallel-agents` (sp) | flujo multiagente con planes en ficheros (la primera tiene 4.900 palabras): justo lo contrario de "un solo agente" |
| `using-git-worktrees` (sp) | crea worktrees y ramas por su cuenta |
| `constraint-driven-development` (addy) | escribe un `CONSTRAINTS.md` en el repo y vigila el diff; 3.500 palabras |
| `doubt-driven-development` (addy) | la revisión adversaria la hace llamando a las CLIs de Codex o Gemini; para eso ya está el `reviewer` |
| `diagnosing-superpowers` (sp) | solo sirve si usas superpowers entero |
| **Paquetes enteros** (superpowers, ECC, BMAD, GStack, SuperClaude) | cientos de skills o un método completo que sustituye al tuyo; ver [RESEARCH](RESEARCH.es.md) |

---

## 4. Propias, en espera

No vienen de ningún repo: son ideas que salieron al diseñar el harness y que se quedan fuera **hasta que algo falle de verdad**:

| Idea | Se haría si… |
|---|---|
| **Mensajes de commit** con el formato del equipo | delegas los commits al agente y hay un formato acordado (si cada uno lo escribe a su manera, no hay nada que fijar) |
| **Plan de ticket** en trozos, en el orden del stack | los tickets gordos salen mal por hacerse de golpe (ver `planning-and-task-breakdown`) |
| **Traducciones** (extraer, editar y compilar) | el ciclo falla a menudo (comillas, catálogos sin recompilar) |
| **Migración o campo nuevo en BD**, de punta a punta | el agente se salta pasos al añadir campos |
| **Skills de un módulo o pantalla** | trabajas a menudo en esa pantalla y el agente reinventa sus componentes: puntero bajo demanda con una `description` muy precisa |

Antes de escribir cualquiera de estas, mira si el fallo cabe como **regla en `check.py`**: es más fiable y no ocupa contexto.
