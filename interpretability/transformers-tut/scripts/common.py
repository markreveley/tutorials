"""Shared course authoring helpers; no runtime dependencies."""
from html import escape

MODULES = [
 ('The object of study', 'Tokens in, logits out, and the residual stream that every part reads from and writes to.'),
 ('Attention', 'One head computed by hand, then heads as two low-rank circuits.'),
 ('MLPs and the output', 'Neurons, gated MLPs, and how the stream becomes a next-token distribution.'),
 ('The whole model', 'A forward pass from raw weights, every tensor shape, and generation with a cache.'),
 ('Tooling and variants', 'The same activation in three libraries, what Llama-style models change, and the readiness review.'),
]

PYTHON = 'python'   # the learner's command; verify_commands.py substitutes the authoring interpreter


def cite(key):
    from sources import SOURCES
    s = SOURCES[key]
    return f'<a class="cite" href="{s["url"]}" title="{escape(s["title"], quote=True)}">[{s["tag"]}]</a>'


def term(commands):
    return '<pre class="term"><code>' + escape('\n'.join(commands)) + '</code></pre>'


_TRANSCRIPT = None


def transcript():
    """Parse research/verify/lab-transcript.txt into {command: output}. Empty before verify_commands.py has run."""
    global _TRANSCRIPT
    if _TRANSCRIPT is None:
        from pathlib import Path
        _TRANSCRIPT = {}
        path = Path(__file__).resolve().parents[1] / 'research/verify/lab-transcript.txt'
        if path.exists():
            cmd, lines = None, []
            for line in path.read_text().splitlines():
                if line.startswith('$ '):
                    cmd, lines = line[2:].split('   (')[0].replace(' (MAY FAIL: learner stubs)', ''), []
                    _TRANSCRIPT[cmd] = lines
                elif line.startswith('[exit '):
                    cmd = None
                elif cmd is not None:
                    lines.append(line)
    return _TRANSCRIPT


def out(command, drop=(), keep=None):
    """Verified terminal output for `command`, copied from the transcript at build time.

    drop: substrings; lines containing any of them are omitted. keep: slice of lines to show.
    A command that is not yet in the transcript renders a placeholder that check_site.py rejects.
    """
    lines = transcript().get(command)
    if lines is None:
        return '<pre class="output"><code>(output not yet verified: run scripts/verify_commands.py, then rebuild)</code></pre>'
    lines = [l for l in lines if not any(d in l for d in drop)]
    if keep is not None:
        lines = lines[keep]
    text = '\n'.join(lines).strip('\n')
    return '<pre class="output"><code>' + escape(text) + '</code></pre>'


def lab(commands, prompt, answer):
    terminal = term(commands) if commands else ''
    return '<div class="lab"><span class="label">Practice</span><p>' + prompt + '</p>' + terminal + '<details><summary>What to look for</summary><p>' + answer + '</p></details></div>'


def lesson(n, module, slug, title, lede, body, question, answer, practice, sources, kw=''):
    check = '<div class="exercise"><span class="label">Check your understanding</span><p>' + question + '</p><details><summary>Reveal the reasoning</summary><p>' + answer + '</p></details></div>'
    return dict(n=f'{n:02}', module=module, path=f'pages/{n:02}-{slug}.html', title=title,
                lede=lede, body=body + check + practice, sources=sources, kw=kw)
