---
name: retro
description: "Repaso (retro) de una sesión: cómo ha funcionado el harness, pieza a pieza y con pruebas sacadas del log, y qué cambiar para la próxima. Use when: el usuario lo pide ('repásalo', 'haz la retro', '¿cómo ha ido el harness?', 'informe del harness') o dice que sí al ofrecérselo al cerrar. NO durante el trabajo ni por iniciativa propia."
---

# Repasar

> **CONCEPTO:** el harness mirándose a sí mismo. Un subagente nuevo lee el log de la sesión y dice, por cada pieza que intervino, si ayudó, no hizo nada o estorbó, con la prueba. Sin esto, las reglas se acumulan y nadie comprueba si siguen haciendo falta, sobre todo cuando el modelo empieza a hacer solo lo que antes había que pedirle.

> **OPTIONAL · LISTA.** Fuera del core: mejora el harness, no el código. Vale tal cual; las rutas las pone `setup.py`. Si no la quieres, borra la carpeta, su fila en los dos routers y el paso 5 de `closing.md`.

El repaso lo hace **un subagente nuevo** (nunca un fork), que no ha hecho la sesión: quien la hizo es el peor juez de ella. Tú solo le pasas el encargo, guardas lo que devuelve y se lo cuentas al usuario.

## 1. El encargo

Lanza el subagente con **solo** esto (sin tu opinión de cómo fue):

```
Lee y sigue <HARNESS>\personal\skills\retro\report.md.
Herramienta: <claude | copilot | copilot-cli | opencode | dsh>
Sesión: <id>
Desde: <HH:MM en que empezó lo que se repasa, o "toda la sesión">
Intención: <qué se quería hacer en la sesión, en una línea>
```

- **El id, nunca "la más reciente":** sácalo de `py -3 <HARNESS>\personal\scripts\read_session.py <herramienta> --list` (la sesión principal, no la de un subagente). En algunas herramientas, el propio subagente del repaso pasaría a ser "la más reciente".
- **Herramienta:** `copilot` es el chat de Copilot; el agente de Copilot (y su CLI) es `copilot-cli`.
- **Intención:** la de lo que se repasa, sacada de los mensajes del usuario de ese tramo; no la del primer mensaje de la sesión, que en un chat largo puede ser de otro día.
- **Desde:** un chat de Copilot puede durar semanas. Pasa la hora en que empezó lo que se repasa (la de hoy, o la de la tarea), para que no lea días que no tocan.

Si tu herramienta no tiene subagentes, haz tú el repaso siguiendo `report.md`, y avisa al usuario de que lo has hecho con el contexto de la sesión encima.

## 2. Lo que devuelve

- **Guárdalo tal cual, con tu herramienta de crear ficheros** (no con `Set-Content`/`Out-File` de PowerShell 5.1, que rompe los acentos) en `<HARNESS>\personal\retros\AAAA-MM-DD-<herramienta>.md` (si ya existe, añade `-2`). El histórico es lo que deja ver si una pieza falla **varias sesiones seguidas**, y no solo una.
- **Al usuario:** el veredicto y los candidatos de mejora, por gravedad, y la ruta del informe.
- **Nada se cambia solo:** el repaso propone y el usuario decide. No toques el harness, ni siquiera lo evidente, sin su sí.

---
Adaptada de `retro` de [mattpocock/skills](https://github.com/mattpocock/skills) @ `a7d038f` (2026-09-24) (MIT): el subagente, la evaluación de cada pieza con pruebas y el histórico son propios de este harness.
