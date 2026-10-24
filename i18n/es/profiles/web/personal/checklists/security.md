# Checklist de seguridad — <PROJECT>

> **PERFIL · web.** Puntos generales de web, válidos para casi cualquier stack. Ajusta a tu stack lo marcado con `TUNE` y luego quita la marca.
>
> La lee el agente `reviewer` en el **eje 3**, punto por punto. No es una skill: no entra en ningún catálogo y el agente principal no la carga al escribir. Si en los logs se ve que el agente escribe código inseguro de forma repetida, se sube a skill (`personal\skills\seguridad\SKILL.md`, con `name` y `description`) y el revisor la sigue leyendo igual.
>
> Lo que se pueda pillar con una regex va también a las `RULES` de `check.py`.

| # | Comprobación | Cómo se ve en el código | Si falla |
|---|---|---|---|
| 1 | **Permisos en cada punto de entrada** | cada ruta, endpoint o controlador nuevo comprueba permisos en el servidor (decorador, middleware o guard); ocultar un botón no es un permiso <!-- TUNE: cómo se declaran en tu framework --> | 🔴 |
| 2 | **Datos de otro (IDOR)** | un id que llega por URL o formulario se usa sin comprobar que pertenece al usuario o a su ámbito | 🔴 |
| 3 | **SQL con parámetros** | nada de concatenar ni interpolar valores en las consultas: el ORM o parámetros enlazados <!-- TUNE: cómo se ve en tu ORM o driver --> | 🔴 |
| 4 | **XSS** | datos de usuario pintados sin escapar: `innerHTML`, `v-html`, `dangerouslySetInnerHTML`, el filtro "safe" de la plantilla <!-- TUNE: la salida sin escapar de tu motor de plantillas --> | 🔴 si viene del usuario · 🟡 si es contenido propio |
| 5 | **Secretos** | claves, tokens o contraseñas en el código, en ficheros versionados o en el bundle del front | 🔴 |
| 6 | **Datos personales** | datos personales en logs, en respuestas con más campos de los necesarios, o exportaciones sin permiso <!-- TUNE: qué datos sensibles maneja el proyecto --> | 🟠 |
| 7 | **IA** (si la hay) | qué datos personales se envían; límites de consumo; la respuesta tratada como dato (nunca como HTML ni como instrucciones) | 🟠 |
| 8 | **Subida de ficheros** | tipo y tamaño validados, nombre saneado, guardado fuera de lo que se sirve tal cual | 🟠 |
| 9 | **Cambios por GET** | acciones que crean, modifican o borran datos accesibles por GET | 🟠 |
| 10 | **CSRF** | los formularios y peticiones que cambian datos llevan la protección CSRF del framework (token o cookies same-site) | 🟠 |
| 11 | **Errores expuestos** | trazas o mensajes de excepción devueltos al usuario | 🟡 |
<!-- TUNE (opcional): puntos propios del proyecto que ya hayan dado problemas. -->

Cada hallazgo, en el informe del revisor, con su número de esta tabla: `(eje 3 · #2)`.

Puntos adaptados de `security-and-hardening` de [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) @ `1be8e34` (2026-10-10) (MIT).
