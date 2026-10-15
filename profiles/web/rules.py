"""Sensor rules of the web profile: setup.py --profile web puts this RULES list into personal/scripts/check.py."""

RULES = [
    # general web rules, valid for most stacks
    ('WARNING', ('.js', '.html'), r'\bconsole\.log\(|\bdebugger\b', 'debugging leftover'),
    ('WARNING', ('.js', '.html'), r'\beval\(', 'eval(): avoid it (security, and it hides errors)'),
    ('WARNING', ('.js', '.html'), r'\.innerHTML\s*=|\bv-html\b|dangerouslySetInnerHTML',
     'HTML injected as is: if it can carry user data, escape it (XSS)'),
    ('WARNING', ('.css', '.html'), r'!important', '!important: fix the specificity instead'),
    ('WARNING', ('.html',), r'\sstyle="[^"{]', 'inline style: use a class and the design variables'),
    ('WARNING', ('.html',), r'target="_blank"(?![^>]*\brel=)', 'target="_blank" without rel="noopener"'),
    ('WARNING', ('.py',), r'\b(?:execute|text|raw)\(\s*f["\']', 'SQL built with an f-string: use parameters'),
    ('WARNING', ('.js',), r'\b(?:query|execute)\(\s*`[^`]*\$\{', 'SQL built with a template literal: use parameters'),
    # TUNE: your stack's rules (versions, forbidden classes, the project's own traps). Examples:
    # ('ERROR', ('.js', '.html'), r'\bv-slot\b', 'v-slot is Vue 2.6; in this project it is <template slot="x" scope="props">'),
    # ('ERROR', ('.js', '.html'), r'\bdata-bs-[\w-]+', 'data-bs-* is Bootstrap 5; here it is data-toggle, data-target...'),
]
