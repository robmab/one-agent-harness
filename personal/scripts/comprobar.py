"""Comprueba que el código del proyecto encaja con su stack real y que compila.

Uso:
    py -3 comprobar.py [ficheros...]   # sin ficheros: los cambiados según git
    py -3 comprobar.py --hook          # modo hook PostToolUse de Claude (lee el JSON por stdin)
    py -3 comprobar.py --selftest      # valida REGLAS y prueba el motor con ficheros de ejemplo

Salida: 0 si no hay errores (puede haber avisos), 1 si hay errores (2 en modo hook).
Solo usa la librería estándar.
"""
import json
import os
import re
import shutil
import subprocess
import sys

# ---------------------------------------------------------------------------
# RELLENAR: configuración del proyecto
# ---------------------------------------------------------------------------

# fichero o carpeta que identifica la raíz del repo (p. ej. 'manage.py', 'package.json'); None = cualquier repo git
MARCADOR = None

# python del proyecto para compilar los .py, relativo a la raíz del repo o absoluto; el primero que exista
# (vacío = se compila con el Python que lanza el script, y se avisa)
PYTHON_PROYECTO = [
    # os.path.join('..', 'env', 'Scripts', 'python.exe'),
    # os.path.join('.venv', 'Scripts', 'python.exe'),
]

EXTENSIONES = ('.py', '.js', '.html', '.css')
IGNORAR = ('.min.', '/node_modules/', '/dist/', '/build/', '/.venv/', '/vendor/')

# un .js con estas marcas pasa por un motor de plantillas antes de servirse: node no lo puede parsear
MARCAS_PLANTILLA = ('{{', '{%')

# reglas por línea: (nivel, extensiones, regex, mensaje). ERROR bloquea; AVISO solo informa
REGLAS = [
    # ejemplos, descomenta y adapta a las versiones reales del proyecto:
    # ('ERROR', ('.js', '.html'), r'\bv-slot\b', 'v-slot es de Vue 2.6; en este proyecto es <template slot="x" scope="props">'),
    # ('ERROR', ('.js', '.html'), r'\bdata-bs-[\w-]+', 'data-bs-* es de Bootstrap 5; aquí es data-toggle, data-target...'),
    # ('ERROR', ('.py',), r'\bmapped_column\b', 'eso es de SQLAlchemy 2.0; aquí 1.4'),
    # ('AVISO', ('.py', '.js'), r'\b(?:print\(|console\.log\(|debugger\b)', 'resto de depuración'),
]

# ---------------------------------------------------------------------------


def raiz_repo(ruta):
    carpeta = os.path.dirname(os.path.abspath(ruta)) if os.path.isfile(ruta) else os.path.abspath(ruta)
    try:
        return subprocess.run(['git', '-C', carpeta, 'rev-parse', '--show-toplevel'],
                              capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def es_proyecto(raiz):
    return bool(raiz) and (MARCADOR is None or os.path.exists(os.path.join(raiz, MARCADOR)))


def python_del_proyecto(raiz):
    for candidato in PYTHON_PROYECTO:
        ruta = candidato if os.path.isabs(candidato) else os.path.join(raiz, candidato)
        if os.path.isfile(ruta):
            return os.path.abspath(ruta)
    return None


def ficheros_cambiados(raiz):
    salida = set()
    for args in (['diff', '--name-only'], ['diff', '--cached', '--name-only'], ['ls-files', '--others', '--exclude-standard']):
        res = subprocess.run(['git', '-C', raiz] + args, capture_output=True, text=True)
        salida.update(l.strip() for l in res.stdout.splitlines() if l.strip())
    return [os.path.join(raiz, f) for f in sorted(salida)]


def relevante(ruta):
    r = ruta.replace('\\', '/')
    return r.endswith(EXTENSIONES) and not any(i in r for i in IGNORAR) and os.path.isfile(ruta)


def comprobar(ruta, raiz):
    hallazgos = []  # (nivel, linea, mensaje)
    ext = os.path.splitext(ruta)[1]
    with open(ruta, encoding='utf-8', errors='replace') as f:
        texto = f.read()
    for n, linea in enumerate(texto.splitlines(), 1):
        for nivel, exts, patron, mensaje in REGLAS:
            if ext in exts and re.search(patron, linea):
                hallazgos.append((nivel, n, mensaje))
    hallazgos += sintaxis(ruta, ext, texto, raiz)
    return sorted(set(hallazgos), key=lambda h: (h[1], h[0]))


def sintaxis(ruta, ext, texto, raiz):
    if ext == '.py':
        python = python_del_proyecto(raiz)
        aviso = [] if python else [('AVISO', 0, 'sin python del proyecto configurado: compilado con el del sistema')]
        res = subprocess.run([python or sys.executable, '-m', 'py_compile', ruta], capture_output=True, text=True)
        if res.returncode:
            return aviso + [('ERROR', 0, 'py_compile: ' + (res.stderr.strip().splitlines() or ['falla'])[-1])]
        return aviso
    if ext == '.js':
        if any(m in texto for m in MARCAS_PLANTILLA):
            return []
        if not shutil.which('node'):
            return [('AVISO', 0, 'no hay node: sintaxis JS sin comprobar')]
        res = subprocess.run(['node', '--check', ruta], capture_output=True, text=True)
        if res.returncode:
            detalle = next((l for l in res.stderr.splitlines() if 'Error' in l), 'falla')
            return [('ERROR', 0, 'node --check: ' + detalle.strip())]
    return []


def informe(resultados, raiz):
    lineas = []
    for ruta, hallazgos in resultados:
        rel = os.path.relpath(ruta, raiz) if raiz else ruta
        for nivel, n, mensaje in hallazgos:
            lineas.append(f'{nivel} {rel}:{n}  {mensaje}' if n else f'{nivel} {rel}  {mensaje}')
    errores = sum(1 for _, h in resultados for x in h if x[0] == 'ERROR')
    avisos = sum(1 for _, h in resultados for x in h if x[0] == 'AVISO')
    return lineas, errores, avisos


def modo_hook():
    try:
        datos = json.load(sys.stdin)
    except ValueError:
        return 0
    ruta = (datos.get('tool_input') or {}).get('file_path') or ''
    if not ruta or not relevante(ruta):
        return 0
    raiz = raiz_repo(ruta)
    if not es_proyecto(raiz):
        return 0
    lineas, errores, avisos = informe([(ruta, comprobar(ruta, raiz))], raiz)
    if errores:
        print('comprobar encontró problemas en lo que acabas de editar:\n' + '\n'.join(lineas), file=sys.stderr)
        return 2
    if avisos:
        print(json.dumps({'hookSpecificOutput': {
            'hookEventName': 'PostToolUse',
            'additionalContext': 'comprobar (avisos, revisa si aplican):\n' + '\n'.join(lineas)}}))
    return 0


def selftest():
    import tempfile
    fallos = []

    # las REGLAS del proyecto, bien formadas
    for i, regla in enumerate(REGLAS):
        if len(regla) != 4:
            fallos.append(f'REGLAS[{i}]: tiene que tener 4 campos (nivel, extensiones, regex, mensaje)')
            continue
        nivel, exts, patron, mensaje = regla
        if nivel not in ('ERROR', 'AVISO'):
            fallos.append(f'REGLAS[{i}]: el nivel tiene que ser ERROR o AVISO, no {nivel!r}')
        if not isinstance(exts, tuple) or not exts or not all(isinstance(e, str) and e.startswith('.') for e in exts):
            fallos.append(f'REGLAS[{i}]: las extensiones van en una tupla, p. ej. (\'.js\',) o (\'.py\', \'.js\')')
        try:
            re.compile(patron)
        except re.error as e:
            fallos.append(f'REGLAS[{i}]: la regex no compila: {e}')
        if not mensaje:
            fallos.append(f'REGLAS[{i}]: falta el mensaje (di qué poner en su lugar)')

    # el motor, con reglas de ejemplo sobre ficheros temporales
    demo = [('ERROR', ('.js',), r'\bv-slot\b', 'demo-error'), ('AVISO', ('.js',), r'console\.log\(', 'demo-aviso')]
    casos = {
        'malo.js': ('var x = "v-slot";\nconsole.log(x);\n', {'demo-error', 'demo-aviso'}, True),
        'bien.js': ('var x = 1;\n', set(), False),
        'roto.py': ('def f(:\n    pass\n', set(), True),
        'bien.py': ('x = 1\n', set(), False),
    }
    guardadas = REGLAS[:]
    REGLAS[:] = demo
    try:
        with tempfile.TemporaryDirectory() as d:
            for nombre, (texto, esperados, con_error) in casos.items():
                ruta = os.path.join(d, nombre)
                with open(ruta, 'w', encoding='utf-8') as f:
                    f.write(texto)
                hallazgos = comprobar(ruta, d)
                mensajes = {m for _, _, m in hallazgos}
                if not esperados <= mensajes:
                    fallos.append(f'motor: en {nombre} faltan {sorted(esperados - mensajes)}')
                if con_error != any(n == 'ERROR' for n, _, _ in hallazgos):
                    fallos.append(f'motor: en {nombre} se esperaba {"algún" if con_error else "ningún"} ERROR, salió {hallazgos}')
            if relevante(os.path.join(d, 'x.min.js')):
                fallos.append('motor: los .min.* tendrían que ignorarse')
    finally:
        REGLAS[:] = guardadas
    if es_proyecto(None):
        fallos.append('motor: sin repo git no tendría que considerarse proyecto')

    print('\n'.join(fallos) if fallos else f'selftest OK: {len(REGLAS)} reglas bien formadas y el motor funciona.')
    return 1 if fallos else 0


def main():
    for flujo in (sys.stdout, sys.stderr):
        flujo.reconfigure(encoding='utf-8')
    if '--hook' in sys.argv:
        return modo_hook()
    if '--selftest' in sys.argv:
        return selftest()

    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    raiz = raiz_repo(args[0] if args else os.getcwd())
    if not es_proyecto(raiz):
        print('No estoy en el repo del proyecto (o no hay git).')
        return 1
    ficheros = [os.path.abspath(a) for a in args] if args else ficheros_cambiados(raiz)
    ficheros = [f for f in ficheros if relevante(f)]
    if not ficheros:
        print('Nada que comprobar (ningún fichero de código cambiado).')
        return 0

    lineas, errores, avisos = informe([(f, comprobar(f, raiz)) for f in ficheros], raiz)
    print('\n'.join(lineas) if lineas else 'Sin problemas.')
    print(f'\n{len(ficheros)} ficheros · {errores} errores · {avisos} avisos')
    return 1 if errores else 0


if __name__ == '__main__':
    sys.exit(main())
