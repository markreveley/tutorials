"""Execute every published terminal command with the ML virtualenv and retain a real transcript.

Run with the authoring interpreter: /home/user/.venv-ml/bin/python scripts/verify_commands.py
Lessons show the learner's generic `python ...`; the transcript records what was actually run.
"""
import importlib.metadata as md
import os
import shlex
import subprocess
import sys
from html.parser import HTMLParser

from build import ROOT

ENV = dict(os.environ, HF_HUB_OFFLINE='1', HF_HUB_DISABLE_PROGRESS_BARS='1', TRANSFORMERS_VERBOSITY='error', PYTHONWARNINGS='ignore')
# Commands the learner runs before implementing the stubs are expected to fail; their exit code is recorded, not enforced.
MAY_FAIL = ('-m unittest', 'anatomy.py compare')
BOUNDARY = [
    'python labs/anatomy.py --help',
    'python labs/anatomy.py stream --position 0',
    'python labs/anatomy.py names --processing default',
    'python labs/anatomy.py compare --reference --tools',
]
REFERENCE_RUN = "python -m unittest discover -s labs -p 'test_*.py'"


class Commands(HTMLParser):
    def __init__(self): super().__init__(); self.active = False; self.lines = []
    def handle_starttag(self, tag, attrs):
        if tag == 'pre': self.active = 'term' in dict(attrs).get('class', '').split()
    def handle_endtag(self, tag):
        if tag == 'pre': self.active = False
    def handle_data(self, text):
        if self.active:
            self.lines.extend(line.strip() for line in text.splitlines() if line.strip().startswith('python '))


def run(line, env=ENV):
    args = shlex.split(line); args[0] = sys.executable
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=900, env=env)
    err = [l for l in result.stderr.splitlines() if 'Loading weights' not in l]
    if result.returncode and len(err) > 12:
        err = err[:4] + ['... (%d lines omitted) ...' % (len(err) - 8)] + err[-4:]
    return result.returncode, result.stdout.rstrip(), '\n'.join(err).rstrip()


def verify():
    commands = []
    for path in sorted(ROOT.rglob('*.html')):
        parser = Commands(); parser.feed(path.read_text())
        for line in parser.lines:
            if line not in commands: commands.append(line)
    for line in BOUNDARY:
        if line not in commands: commands.append(line)
    versions = ', '.join(f'{p} {md.version(p)}' for p in ('torch', 'transformers', 'transformer_lens', 'nnsight', 'numpy', 'tokenizers'))
    output = ['Transformer Anatomy: actual local command transcript',
              'Authoring date: 2026-10-20', f'Interpreter: {sys.executable}', f'Python: {sys.version.split()[0]}',
              f'Packages: {versions}', 'Environment: HF_HUB_OFFLINE=1; gpt2 loaded from the local Hugging Face cache; CPU only.',
              'Lessons print the generic command `python ...`; every run below used the interpreter named above.',
              'Commands marked MAY FAIL exercise learner stubs before implementation; their nonzero exit is expected.', '']
    for line in commands:
        code, out, err = run(line)
        tag = ' (MAY FAIL: learner stubs)' if any(m in line for m in MAY_FAIL) and 'reference' not in line else ''
        output.extend(['$ ' + line + tag, out, err, f'[exit {code}]', ''])
        if code and not tag:
            raise RuntimeError(f'{line} failed:\n{err}')
    code, out, err = run(REFERENCE_RUN, dict(ENV, LAB_IMPL='reference'))
    output.extend(['$ LAB_IMPL=reference ' + REFERENCE_RUN + '   (author check: tests against labs/reference/)', out, err, f'[exit {code}]', ''])
    if code:
        raise RuntimeError('reference tests failed:\n' + err)
    target = ROOT / 'research/verify/lab-transcript.txt'
    target.write_text('\n'.join(output).rstrip() + '\n')
    print(f'PASS: {len(commands) + 1} documented and boundary commands executed; transcript saved to {target.relative_to(ROOT)}.')


if __name__ == '__main__': verify()
