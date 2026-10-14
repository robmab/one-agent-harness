# Investigación: de dónde sale esta plantilla

🌐 [English](RESEARCH.md) · **Español**

Investigación hecha el 2026-10-10 (las estrellas son de la API de GitHub de ese día). Explica qué es un harness, qué hay en GitHub y por qué la plantilla trae justo estas piezas. Cómo se monta está en el [README](README.es.md); qué hace cada pieza, en la [SKILLS-GUIDE](SKILLS-GUIDE.es.md).

---

## 1. Qué es un "harness"

Agente = modelo + harness. El harness es todo lo que rodea al modelo, y tiene dos tipos de piezas (Martin Fowler):

| Tipo | Qué es | Ejemplos | En la plantilla |
|---|---|---|---|
| **Guías** | lo que le llega al agente *antes* de actuar | `AGENTS.md`, skills | skills de conocimiento y de proceso |
| **Sensores de juicio** | otro modelo revisa *después* | agente revisor | `reviewer` (uno solo) |
| **Sensores automáticos** | comprobaciones fijas, baratas y deterministas *después* | linters, tests, hooks | `check.py` + hook |

Ideas clave de las fuentes:
- **Hacen falta las dos cosas:** solo guías da reglas que nadie comprueba; solo sensores, un agente que repite fallos.
- **`AGENTS.md` ya es el estándar entre herramientas** (estudio de 2.853 repos). Hay que tenerlo corto y meter cada regla solo después de un fallo real.
- **Lo portable** entre herramientas es `AGENTS.md`, los `SKILL.md`, los linters y el CI. Lo que dependa de una sola herramienta, cuanto menos mejor.
- **El harness pesa más que el modelo:** cambiarlo mueve los resultados más que muchos cambios de modelo, y lo que va bien con un modelo no se traslada al siguiente. Con modelos pequeños, menos es más.
- **Las skills se cargan por su `description`:** al principio solo sube el nombre y la descripción; el resto, cuando el modelo decide que aplica. La `description` es lo que manda.

## 2. Panorama en GitHub

### Paquetes de skills y metodología

| Repo | ⭐ | Qué es | Cuándo encaja |
|---|---|---|---|
| obra/superpowers | 297k | método completo: brainstorming, plan, TDD obligatorio, subagentes, review (MIT) | proyectos con tests; por piezas si no los hay |
| affaan-m/ECC | 276k | megapaquete: 284 skills y 68 subagentes | casi nunca: se come el contexto |
| anthropics/skills | 180k | skills de referencia del formato y de documentos | para aprender el formato |
| garrytan/gstack | 136k | 23 roles (CEO, QA, release…) | producto en solitario, solo Claude |
| addyosmani/agent-skills | 104k | 25 skills de ingeniería, portables a más de 70 agentes (MIT) | casi siempre, cogiendo piezas sueltas |
| wshobson/agents | 40k | marketplace de agentes para varias herramientas | para coger algún agente suelto |
| SuperClaude | 24k | personas y comandos | enfoque antiguo |

### Desarrollo guiado por especificaciones (SDD)

| Repo | ⭐ | Qué es | Cuándo encaja |
|---|---|---|---|
| github/spec-kit | 141k | el de GitHub, nativo de Copilot; mete `.specify/` en el repo | proyectos nuevos; Python 3.11 + uv |
| Fission-AI/OpenSpec | 72k | ligero, pensado para código existente; mete `openspec/` | código heredado con features gordas; decisión de equipo |
| gsd-build/get-shit-done | 64k | planes por oleadas con contexto limpio | parado desde mayo de 2026 |
| BMAD-METHOD | 54k | simula un equipo ágil entero | muy pesado (se habla de meses para dominarlo) |

**Conclusión:** ningún framework entero. Las piezas que rinden son pocas, cortas y adaptadas al proyecto, más un sensor automático. Los SDD (spec-kit, OpenSpec) solo si el equipo entero los adopta, porque escriben en el repo.

## 3. Las piezas de la plantilla

**Por qué estas:** las skills de conocimiento (convenios, diseño, estilo) dicen **cómo se escribe** y **cómo se habla**. Ninguna cubre **cómo trabaja el agente**: entender antes de hacer, diagnosticar antes de arreglar, demostrar antes de decir "hecho", ni revisar corrección, seguridad o rendimiento. Eso es lo que añaden las piezas adaptadas.

| Pieza | Origen | Hueco que tapa | Adaptación |
|---|---|---|---|
| `verify-before-done` | superpowers `verification-before-completion` | el agente dice "hecho" sin haber ejecutado nada | tabla de comandos del proyecto y salida honrada «Sin comprobar» |
| `systematic-debugging` | superpowers `systematic-debugging` | arreglos a ciegas, parches sobre el síntoma | sin test obligatorio: vale una reproducción; tabla de capas del proyecto |
| `interview-me` | addyosmani `interview-me` | tickets ambiguos que el agente rellena inventando | mirar antes el repo; preguntas para el cliente; nada de ficheros en el repo |
| `official-sources` | addyosmani `source-driven-development` | código de memoria para la versión equivocada | el repo como primera fuente; tabla de versiones y trampas |
| `reviewer` (único agente) | addyosmani `code-review-and-quality` | nadie revisa corrección, seguridad ni rendimiento | 6 ejes con los convenios incluidos; lee las skills de conocimiento como checklists; contexto limpio; no edita; pasa antes el sensor |
| `check.py` + hook | propio | las reglas importantes dependían de la memoria del modelo | regex del stack + sintaxis, tras cada edición |

**Un solo agente:** la tendencia de tener muchos revisores especializados se descarta. Cada subagente empieza sin contexto, gasta más tokens y repasa otra vez el mismo diff. Un agente nuevo solo compensa por ojos frescos, permisos distintos o para aislar un trabajo pesado. Un "revisor de X" se hace como skill (checklist) que lee el `reviewer`.

**Probado en la práctica** (en el proyecto donde nació la plantilla):
- un modelo local escribió sintaxis de una versión posterior aunque la skill la prohibía: solo la cumplía invocándola a mano;
- un modelo potente acertó, pero dijo "validado" sin comprobar nada;
- con Claude y las skills, el resultado salió bien y comprobado en el navegador;
- el hook cazó el error en la línea exacta y sin falsos positivos.

### Descartadas
- `brainstorming`: es "MUST antes de cualquier cosa creativa", demasiado invasiva; `interview-me` cubre lo útil.
- `test-driven-development`, `writing-plans`, `executing-plans`, `subagent-driven-development`: TDD obligatorio, worktrees y planes pesados. Puede tener sentido en un proyecto con buena base de tests.
- `doubt-driven-development`: tira de las CLIs de Codex y Gemini.
- `constraint-driven-development`: escribe `CONSTRAINTS.md` en el repo.
- `context-engineering`: es lo que hace esta plantilla.
- `code-simplification`, `incremental-implementation`, `deprecation-and-migration`: solapan o son de uso puntual.
- `recibir-revision`, commits y planes de ticket: ruido para el flujo diario. En espera hasta que algo falle de verdad.

### Reglas al adaptar una skill de fuera
- En el idioma en que se habla con el modelo y recortada (los originales tienen entre 600 y 3.300 palabras; objetivo ≤ 600), con la `description` afinada para que se dispare cuando toca y no siempre.
- Crédito al pie: "Adaptada de <skill> de <repo> (MIT)".
- Que no escriba nada en el repo (ni planes, ni intents, ni worktrees).
- Probarla en Claude y en Copilot, también con un modelo local, antes de dar por buena la siguiente.

## Fuentes
- Martin Fowler, *Harness engineering for coding agent users*: https://martinfowler.com/articles/harness-engineering.html
- Addy Osmani, *Agent Harness Engineering*: https://addyosmani.com/blog/agent-harness-engineering/
- arXiv, *Harness Engineering for Agentic AI Coding Tools*: https://arxiv.org/html/2602.14690v5
- best-of-Agent-Harnesses: https://github.com/ryanalberts/best-of-agent-harnesses (y su comparativa de skill packs)
- Spec Kit vs BMAD vs OpenSpec: https://dev.to/willtorber/spec-kit-vs-bmad-vs-openspec-choosing-an-sdd-framework-in-2026-d3j
- Repos: obra/superpowers, addyosmani/agent-skills, github/spec-kit, Fission-AI/OpenSpec
