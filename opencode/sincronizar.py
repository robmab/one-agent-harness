"""Genera los agentes de OpenCode a partir de los compartidos con Claude y Copilot.

OpenCode 2 ignora un agente entero si su frontmatter trae `tools: Read, Grep, ...`
(el formato de Claude y Copilot), así que aquí va una copia sin esa línea. Lo propio
de OpenCode (subagente, pasos, edición denegada) está en `opencode.jsonc`.

Lánzalo después de tocar `personal\\agents\\*.agent.md`:  py -3 sincronizar.py
Con --check no escribe nada: sale con 1 si alguna copia está desactualizada.
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(AQUI, '..', 'personal', 'agents')
DESTINO = os.path.join(AQUI, 'agents')


def generado(texto, nombre_origen):
    # Fuera la línea `tools:` del frontmatter, que en OpenCode tumba el agente
    cabecera, cuerpo = texto.split('\n---', 1)
    cabecera = re.sub(r'(?m)^tools:.*\n?', '', cabecera).rstrip('\n')
    aviso = '<!-- Generado por opencode/sincronizar.py desde personal/agents/%s: no lo edites aquí -->\n' % nombre_origen
    return cabecera + '\n---' + cuerpo.replace('\n', '\n' + aviso, 1)


def pares():
    """(fichero de origen, fichero generado, texto esperado) de cada agente."""
    for nombre_origen in sorted(n for n in os.listdir(ORIGEN) if n.endswith('.agent.md')):
        with io.open(os.path.join(ORIGEN, nombre_origen), encoding='utf-8-sig') as f:
            texto = f.read().replace('\r\n', '\n')
        destino = os.path.join(DESTINO, nombre_origen.replace('.agent.md', '.md'))
        yield nombre_origen, destino, generado(texto, nombre_origen)


def actual(ruta):
    if not os.path.isfile(ruta):
        return None
    with io.open(ruta, encoding='utf-8') as f:
        return f.read().replace('\r\n', '\n')


def main():
    if '--check' in sys.argv:
        viejos = [os.path.basename(d) for _, d, esperado in pares() if actual(d) != esperado]
        print('Desactualizados: ' + ', '.join(viejos) if viejos else 'Al día.')
        return 1 if viejos else 0
    os.makedirs(DESTINO, exist_ok=True)
    hechos = []
    for _, destino, esperado in pares():
        with io.open(destino, 'w', encoding='utf-8', newline='') as f:
            f.write(esperado)
        hechos.append(os.path.basename(destino))
    print('Generados: ' + ', '.join(hechos))
    return 0


if __name__ == '__main__':
    sys.exit(main())
