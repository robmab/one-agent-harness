# Cerrar la sesión

Léelo al cerrar la sesión, o antes de un commit o un PR. Va en este orden.

## 1. El revisor

Una sola vez, con todo el diff de la sesión (si el cambio es grande o delicado, al terminarlo, sin esperar al cierre). Pásale **solo** esto:

```
Alcance: <ficheros o commits de la sesión>
Intención: <qué se quería hacer, en una línea>
```

Nada de qué has comprobado ni de dónde tiene que mirar: que lo saque él.

## 2. Lo que encontró, entero

- Corrige lo que sea tuyo y compruébalo de nuevo.
- **Cuéntale al usuario todos los hallazgos**, también los que no arreglas (lo ya decidido, lo preexistente): que no se queden en el informe del revisor.

## 3. Limpieza

Borra **todos** los scripts temporales que creaste, y cualquier dato de prueba que no te hayan pedido conservar (o di cuál queda y cómo quitarlo).

## 4. El mensaje de commit

Solo ahora, con el revisor pasado. El commit y el push son del usuario: no ejecutes `git add`, `git commit` ni `git push`.

- **Formato:** <!-- FILL-IN: el formato del equipo, p. ej. `[fix] #<ticket>: <título tal cual>. <descripción corta y no técnica>` -->
- Lo que no sepas (el ticket, por ejemplo) queda como hueco `<…>`, nunca inventado.
- Propón el mensaje entero, con la descripción ya escrita, aunque te pidan "solo la estructura".
