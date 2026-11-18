"""Shared course authoring helpers; no runtime dependencies."""
from html import escape

MODULES = [
 ('Vectors', 'An activation is a vector. Add, scale, compare, and project it.'),
 ('Linear maps', 'Weight matrices map one space to another; shapes, composition, bases, and rank.'),
 ('Subspaces and fitting', 'Remove a direction cleanly, and fit a direction to labels by least squares.'),
 ('Spectra', 'Eigenvectors, covariance, PCA, and the SVD, read on a real activation matrix.'),
 ('Calculus and rigor', 'Gradients as directions, and whether a correlation with a direction is real.'),
]


def cite(key):
    from sources import SOURCES
    s = SOURCES[key]
    return f'<a class="cite" href="{s["url"]}" title="{escape(s["title"], quote=True)}">[{s["tag"]}]</a>'


def lab(commands, prompt, answer):
    terminal = '<pre class="term"><code>'+escape('\n'.join(commands))+'</code></pre>' if commands else ''
    return '<div class="lab"><span class="label">Practice</span><p>'+prompt+'</p>'+terminal+'<details><summary>What to look for</summary><p>'+answer+'</p></details></div>'


def out(text):
    """Verbatim terminal output copied from research/verify/lab-transcript.txt."""
    return '<pre class="term out"><code>'+escape(text.strip('\n'))+'</code></pre>'


def lesson(n, module, slug, title, lede, body, question, answer, practice, sources, kw=''):
    check = '<div class="exercise"><span class="label">Check your understanding</span><p>'+question+'</p><details><summary>Reveal the reasoning</summary><p>'+answer+'</p></details></div>'
    return dict(n=f'{n:02}',module=module,path=f'pages/{n:02}-{slug}.html',title=title,
                lede=lede,body=body+check+practice,sources=sources,kw=kw)
