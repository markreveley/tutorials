"""Shared course authoring helpers; no runtime dependencies beyond the standard library."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / 'research/verify/outputs.json'

MODULES = [
 ('Orientation and setup', 'What the course makes you able to do, and a working CPU-only toolchain.'),
 ('Python for someone coming from Elixir and Rust', 'Names, mutation, records, exceptions, tests, and the idioms you will read every day.'),
 ('Arrays and tensors', 'Shape, dtype, broadcasting, reductions, einsum, views, and autograd: the spine of the course.'),
 ('Models as objects', 'Modules, GPT-2 small, hooks, three interpretability toolkits, and reproducible artifacts.'),
 ('Readiness', 'Cache the residual stream with hooks, assert every shape, and ship a manifest.'),
]

# Every command shown in a lesson is registered here; scripts/verify_commands.py
# runs them and scripts/build.py pastes the recorded output next to the command.
COMMANDS = []


def _recorded():
    if OUTPUTS.exists():
        return json.loads(OUTPUTS.read_text())
    return {}


def run(command, cwd='course', expect=0, note=''):
    """Register a learner command and render it with its verified output."""
    entry = dict(command=command, cwd=cwd, expect=expect)
    if entry not in COMMANDS:
        COMMANDS.append(entry)
    rec = _recorded().get(command)
    if rec is None:
        body = '(output not yet verified: run scripts/verify_commands.py, then rebuild)'
        status = 'unverified'
    else:
        body = rec['stdout'].rstrip('\n')
        status = 'verified'
    prefix = '' if cwd == 'course' else f'cd {cwd} && '
    head = f'<span class="prompt">$ </span>{escape(prefix + command)}'
    text = escape(body) if body else '(no output)'
    caption = f'<span class="termnote">{escape(note)}</span>' if note else ''
    return f'<pre class="term" data-status="{status}"><code>{head}\n{text}</code></pre>{caption}'


def cite(key):
    from sources import SOURCES
    s = SOURCES[key]
    return f'<a class="cite" href="{s["url"]}" title="{escape(s["title"], quote=True)}">[{s["tag"]}]</a>'


def code(text, lang='python'):
    """A static code listing (not executed)."""
    return f'<pre class="code" data-lang="{lang}"><code>{escape(text.strip("\n"))}</code></pre>'


def lab(prompt, answer, commands=()):
    terminal = ''.join(run(**c) if isinstance(c, dict) else run(c) for c in commands)
    return '<div class="lab"><span class="label">Practice</span><p>'+prompt+'</p>'+terminal+'<details><summary>What to look for</summary><p>'+answer+'</p></details></div>'


def lesson(n, module, slug, title, lede, body, question, answer, practice, sources, kw=''):
    check = '<div class="exercise"><span class="label">Check your understanding</span><p>'+question+'</p><details><summary>Reveal the reasoning</summary><p>'+answer+'</p></details></div>'
    return dict(n=f'{n:02}', module=module, path=f'pages/{n:02}-{slug}.html', title=title,
                lede=lede, body=body+check+practice, sources=sources, kw=kw)
