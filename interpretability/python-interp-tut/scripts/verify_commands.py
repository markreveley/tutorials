"""Execute every command a lesson shows and keep the real transcript and outputs.

Run with the virtualenv interpreter so `python3` resolves to it:
    /home/user/.venv-ml/bin/python scripts/verify_commands.py
Commands run through the shell with the interpreter's bin directory first on
PATH, so the command text in the lessons is exactly what was executed.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import COMMANDS, ROOT  # noqa: E402
import build  # noqa: E402  (importing registers every lesson and appendix command)
build.home_body()  # the home page's commands register when its body is rendered

REPO = ROOT.parents[1]


def versions():
    out = []
    for name in ['numpy', 'torch', 'transformers', 'transformer_lens', 'nnsight', 'safetensors']:
        try:
            import importlib.metadata as m
            out.append(f'{name} {m.version(name)}')
        except Exception:
            out.append(f'{name} (not installed)')
    return out


def verify():
    env = dict(os.environ)
    env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env.get('PATH', '')
    env.setdefault('HF_HUB_OFFLINE', '1')
    env.setdefault('HF_HUB_DISABLE_PROGRESS_BARS', '1')
    env.setdefault('TRANSFORMERS_VERBOSITY', 'error')
    env.setdefault('PYTHONWARNINGS', 'ignore')
    env['PYTHONHASHSEED'] = '0'
    env['COLUMNS'] = '100'
    transcript = ['Python for Model Internals: actual local command transcript',
                  'Authoring date: 2026-10-20', f'Interpreter: {sys.executable}', f'Python: {sys.version}',
                  'Versions: ' + ', '.join(versions()),
                  'Environment: HF_HUB_OFFLINE=1 (GPT-2 small read from the local Hugging Face cache); CPU only.',
                  'Commands run through the shell with the virtualenv bin directory first on PATH, so `python3` is the interpreter above.', '']
    outputs = {}
    for entry in COMMANDS:
        cmd, cwd, expect = entry['command'], entry['cwd'], entry['expect']
        workdir = ROOT if cwd == 'course' else (ROOT / cwd).resolve()
        start = time.perf_counter()
        result = subprocess.run(cmd, shell=True, cwd=workdir, env=env, text=True, capture_output=True, timeout=900)
        elapsed = time.perf_counter() - start
        shown = cmd if cwd == 'course' else f'cd {cwd} && {cmd}'
        transcript.extend([f'$ {shown}', f'[cwd {workdir.relative_to(REPO)}; {elapsed:.1f}s]', result.stdout.rstrip(),
                           ('[stderr]\n' + result.stderr.rstrip()) if result.stderr.strip() else '', f'[exit {result.returncode}]', ''])
        if result.returncode != expect:
            raise RuntimeError(f'{cmd} exited {result.returncode}, expected {expect}:\n{result.stderr}')
        outputs[cmd] = dict(stdout=result.stdout, exit=result.returncode, cwd=cwd, seconds=round(elapsed, 1))
    (ROOT / 'research/verify').mkdir(parents=True, exist_ok=True)
    (ROOT / 'research/verify/lab-transcript.txt').write_text('\n'.join(line for line in transcript if line is not None).rstrip() + '\n')
    (ROOT / 'research/verify/outputs.json').write_text(json.dumps(outputs, indent=1, ensure_ascii=False) + '\n')
    print(f'PASS: {len(COMMANDS)} documented commands executed; transcript and outputs saved. Rebuild to paste outputs into the pages.')


if __name__ == '__main__':
    verify()
