<!--
PLANTILLA de AGENTS.md: se copia a la RAÍZ DEL REPO del proyecto con el nombre AGENTS.md (si el repo es tuyo o el equipo está de acuerdo).
Lo cargan solos Claude Code y Copilot al empezar, en cada sesión: que sea corto, un índice y no un manual.
Regla para mantenerlo: cada línea tiene que poder explicarse por un fallo real o por algo que el agente no puede adivinar.
Borra este comentario al copiarlo.
-->

# <PROJECT> — guía para agentes

<!-- FILL-IN: una línea con qué es y el stack principal. -->

Esto es solo el índice. El detalle vive en las skills y en `docs/`.

## Skills

| Skill | Cuándo |
|---|---|
| `convenios-codigo` | antes de escribir o revisar CUALQUIER código |
| `diseno-ui` | solo maquetación, estilos o componentes de UI |
| <!-- FILL-IN: otras del repo, si las hay --> | |

## Agentes

| Agente | Cuándo |
|---|---|
| `revisor` | el único: revisión a fondo (convenios, corrección, seguridad, rendimiento…); no edita; sin ficheros, revisa el `git diff` |

## Comandos

<!-- FILL-IN: solo los que un agente no puede adivinar. Marca los peligrosos. -->

```bash
# entorno: cómo activarlo o qué ejecutable usar (el del PATH, ¿vale?)
# arrancar el server de desarrollo
# tests
# lint / formato
# migraciones de BD  → ojo, toca la BD: confirmar antes
```

- **BD de desarrollo:** <!-- FILL-IN: dónde está y si es copia de producción -->
- **Assets:** <!-- FILL-IN: ¿hay build o se sirven tal cual? -->

## Lo que no se hace sin preguntar

<!-- FILL-IN: acciones que siempre necesitan permiso (tocar la BD, instalar dependencias, hacer push…). -->
