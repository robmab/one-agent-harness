# El resumen del día

Cuando el usuario pide el del día (o el de varios días) en vez del de una sesión, lo haces tú, a partir de los repasos y de los logs:

- **Fuentes:** los repasos de ese día en `retros\` valen tal cual. Las sesiones sin repaso, léelas con `read_session.py <herramienta> --list --since AAAA-MM-DD` y luego `--session <id> --since AAAA-MM-DD --summary` (el log entero solo donde el resumen deje dudas). Deja fuera la sesión que escribe el resumen.
- **Guárdalo** en `<HARNESS>\personal\retros\AAAA-MM-DD-dia.md`, con: las fuentes; el veredicto en 3 o 4 líneas (cómo salió el trabajo y dónde falló el harness); una tabla de sesiones (sesión · hora · qué · el harness en una línea, o «repaso `<fichero>`»); lo que se repite ese día, con pruebas (hora y sesión); lo que fue bien, para no tocarlo; los candidatos de mejora por gravedad (fichero y cambio); la tendencia frente a los repasos anteriores; y los números del día (sesiones, llamadas, lanzamientos del revisor, ERROR del sensor).
- **Lo que el usuario pidió del harness desde una sesión de trabajo** (una regla, una columna de un informe, un formato) entra como candidato: si no, se pierde.
- No es un repaso pieza a pieza: una línea por sesión, y el detalle se queda en cada repaso. Aquí tampoco se cambia nada solo. Para un mes, lo mismo a partir de los resúmenes de los días.
