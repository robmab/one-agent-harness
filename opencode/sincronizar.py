"""Genera las copias de los agentes para OpenCode y Copilot a partir de los de Claude.

El original (`personal\\agents\\*.agent.md`) lo lee Claude tal cual, con `tools: Read, Grep, ...`.
Cada herramienta nombra sus herramientas a su manera, así que aquí van dos copias:
- OpenCode 2 ignora un agente entero si su frontmatter trae `tools:` → copia sin esa línea
  (lo propio de OpenCode, como pasos y edición denegada, está en `opencode.jsonc`).
- VS Code no conoce los nombres de Claude y deja al agente sin herramientas → copia con sus alias.

Lánzalo después de tocar `personal\\agents\\*.agent.md`:  py -3 sincronizar.py
Con --check no escribe nada: sale con 1 si alguna copia está desactualizada.
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(AQUI, '..', 'personal', 'agents')
# (carpeta de destino, extensión, línea `tools:` que la sustituye; None = quitarla)
DESTINOS = [
    (os.path.join(AQUI, 'agents'), '.md', None),
    (os.path.join(AQUI, '..', 'copilot', 'agents'), '.agent.md', 'tools: [read, search, execute]'),
]


def generado(texto, nombre_origen, tools):
    cabecera, cuerpo = texto.split('\n---', 1)
    cabecera = re.sub(r'(?m)^tools:.*\n?', '' if tools is None else tools + '\n', cabecera).rstrip('\n')
    aviso = '<!-- Generado por opencode/sincronizar.py desde personal/agents/%s: no lo edites aquí -->\n' % nombre_origen
    return cabecera + '\n---' + cuerpo.replace('\n', '\n' + aviso, 1)


def pares():
    """(fichero de origen, fichero generado, texto esperado) de cada agente y destino."""
    for nombre_origen in sorted(n for n in os.listdir(ORIGEN) if n.endswith('.agent.md')):
        with io.open(os.path.join(ORIGEN, nombre_origen), encoding='utf-8-sig') as f:
            texto = f.read().replace('\r\n', '\n')
        for carpeta, ext, tools in DESTINOS:
            destino = os.path.join(carpeta, nombre_origen.replace('.agent.md', ext))
            yield nombre_origen, destino, generado(texto, nombre_origen, tools)


def actual(ruta):
    if not os.path.isfile(ruta):
        return None
    with io.open(ruta, encoding='utf-8') as f:
        return f.read().replace('\r\n', '\n')


def nombre(ruta):
    return os.path.relpath(ruta, os.path.join(AQUI, '..')).replace('\\', '/')


def main():
    if '--check' in sys.argv:
        viejos = [nombre(d) for _, d, esperado in pares() if actual(d) != esperado]
        print('Desactualizados: ' + ', '.join(viejos) if viejos else 'Al día.')
        return 1 if viejos else 0
    hechos = []
    for _, destino, esperado in pares():
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with io.open(destino, 'w', encoding='utf-8', newline='') as f:
            f.write(esperado)
        hechos.append(nombre(destino))
    print('Generados: ' + ', '.join(hechos))
    return 0


if __name__ == '__main__':
    sys.exit(main())
