"""Shared course authoring helpers; no runtime dependencies."""
from html import escape

MODULES = [
 ('Claims and the protocol', 'A claim about a model’s internals is a hypothesis. Write the prediction test, the control, and the threshold before you look.'),
 ('Evidence that misleads and evidence that counts', 'Max-activating examples, held-out prediction scoring, and the controls that tell an explanation from a coincidence.'),
 ('Vision replication on a CPU', 'InceptionV1 curve detectors with synthetic stimuli: screen, pre-register, test on held-out stimuli, and report what did and did not replicate.'),
 ('Language methods on GPT-2 small', 'Probes, the logit lens, activation patching, and induction heads, each with a test written before the look.'),
 ('Features and the write-up', 'Sparse-autoencoder features, the Gao critique, and the checklist that separates a demonstrated explanation from a story.'),
 ('Capstone', 'Pick a neuron by a documented procedure, pre-register, run on held-out text, report. Then the readiness review.'),
]


def cite(key):
    from sources import SOURCES
    s = SOURCES[key]
    return f'<a class="cite" href="{s["url"]}" title="{escape(s["title"], quote=True)}">[{s["tag"]}]</a>'


def lab(commands, prompt, answer):
    terminal = '<pre class="term"><code>'+escape('\n'.join(commands))+'</code></pre>' if commands else ''
    return '<div class="lab"><span class="label">Practice</span><p>'+prompt+'</p>'+terminal+'<details><summary>What to look for</summary><p>'+answer+'</p></details></div>'


def transcript(text):
    """Verbatim output from research/verify/lab-transcript.txt, shown as a terminal block."""
    return '<pre class="term out"><code>'+escape(text.strip('\n'))+'</code></pre>'


def lesson(n, module, slug, title, lede, body, question, answer, practice, sources, kw=''):
    check = '<div class="exercise"><span class="label">Check your understanding</span><p>'+question+'</p><details><summary>Reveal the reasoning</summary><p>'+answer+'</p></details></div>'
    return dict(n=f'{n:02}',module=module,path=f'pages/{n:02}-{slug}.html',title=title,
                lede=lede,body=body+check+practice,sources=sources,kw=kw)
