"""Reglas del sensor del perfil web: setup.py --profile web mete esta lista RULES en personal/scripts/check.py."""

RULES = [
    # siempre activa: una contraseña escrita en una URL (en Claude ya la para guard.py; esta pilla al resto)
    ('ERROR', ('.py', '.js', '.ts', '.html', '.ps1', '.sh'), r'\b[a-z][a-z0-9+.-]*://[^\s:/@\"\'`]+:(?!\*+@|<[^>]*>@|\{[^}]*\}@|\$\w+@)[^\s@\"\'`/]+@',
     'contraseña en claro (usuario:contraseña@ en una URL): lee la conexión del fichero de configuración'),
    # reglas generales de web, válidas para casi cualquier stack
    ('WARNING', ('.js', '.html'), r'\bconsole\.log\(|\bdebugger\b', 'resto de depuración'),
    ('WARNING', ('.js', '.html'), r'\beval\(', 'eval(): evítalo (seguridad, y esconde errores)'),
    ('WARNING', ('.js', '.html'), r'\.innerHTML\s*=|\bv-html\b|dangerouslySetInnerHTML',
     'HTML metido tal cual: si puede llevar datos del usuario, escápalo (XSS)'),
    ('WARNING', ('.css', '.html'), r'!important', '!important: arregla la especificidad en su lugar'),
    ('WARNING', ('.html',), r'\sstyle="[^"{]', 'estilo en línea: usa una clase y las variables de diseño'),
    ('WARNING', ('.html',), r'target="_blank"(?![^>]*\brel=)', 'target="_blank" sin rel="noopener"'),
    ('WARNING', ('.py',), r'\b(?:execute|text|raw)\(\s*f["\']', 'SQL montado con una f-string: usa parámetros'),
    ('WARNING', ('.js',), r'\b(?:query|execute)\(\s*`[^`]*\$\{', 'SQL montado con una plantilla de texto: usa parámetros'),
    # TUNE: las reglas de tu stack (versiones, clases prohibidas, trampas propias del proyecto). Ejemplos:
    # ('ERROR', ('.js', '.html'), r'\bv-slot\b', 'v-slot es de Vue 2.6; en este proyecto es <template slot="x" scope="props">'),
    # ('ERROR', ('.js', '.html'), r'\bdata-bs-[\w-]+', 'data-bs-* es de Bootstrap 5; aquí es data-toggle, data-target...'),
]
