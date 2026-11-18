"""Shared course authoring helpers; no runtime dependencies."""
from html import escape

MODULES = [
 ('Ask a measurable question', 'Define the score, the population, and the decision before doing arithmetic.'),
 ('Understand uncertainty', 'Build probability, sampling, and error bars from small worked examples.'),
 ('Compare systems', 'Keep task pairs together, interpret tests, and plan an informative experiment.'),
 ('Respect the data structure', 'Handle repeated runs, related tasks, slices, weights, and missing outcomes.'),
 ('Measure the measuring instrument', 'Evaluate graders, probability forecasts, and Bayesian updates.'),
 ('Make defensible decisions', 'Avoid selection traps, measure reliability, and write a result you can defend.'),
 ('Screen many candidates', 'Correlate, test by shuffling, count what chance alone would pass, and confirm on data the screen never saw.'),
]


def cite(key):
    from sources import SOURCES
    s = SOURCES[key]
    return f'<a class="cite" href="{s["url"]}" title="{escape(s["title"], quote=True)}">[{s["tag"]}]</a>'


def lab(commands, prompt, answer):
    terminal = '<pre class="term"><code>'+escape('\n'.join(commands))+'</code></pre>' if commands else ''
    return '<div class="lab"><span class="label">Practice</span><p>'+prompt+'</p>'+terminal+'<details><summary>What to look for</summary><p>'+answer+'</p></details></div>'


def lesson(n, module, slug, title, lede, body, question, answer, practice, sources, kw=''):
    check = '<div class="exercise"><span class="label">Check your understanding</span><p>'+question+'</p><details><summary>Reveal the reasoning</summary><p>'+answer+'</p></details></div>'
    return dict(n=f'{n:02}',module=module,path=f'pages/{n:02}-{slug}.html',title=title,
                lede=lede,body=body+check+practice,sources=sources,kw=kw)
