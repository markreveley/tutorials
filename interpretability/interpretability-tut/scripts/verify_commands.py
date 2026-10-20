"""Execute every published command and retain a real transcript.

Commands are collected from <pre class="term"> blocks whose lines start with
"python " and are run with the interpreter running this script (the ML
virtualenv), offline, from the course root. Nothing shown on a page is typed in
by hand: lessons quote this transcript.
"""
from html.parser import HTMLParser
from importlib.metadata import version
import os
import platform
import shlex
import subprocess
import sys
import time

from build import ROOT

PACKAGES = ['torch', 'torchvision', 'transformers', 'transformer_lens', 'nnsight', 'numpy']


class Commands(HTMLParser):
    def __init__(self): super().__init__(); self.active=False; self.lines=[]
    def handle_starttag(self,tag,attrs):
        if tag=='pre':
            classes=dict(attrs).get('class','').split()
            self.active='term' in classes and 'out' not in classes
    def handle_endtag(self,tag):
        if tag=='pre': self.active=False
    def handle_data(self,text):
        if self.active:
            self.lines.extend(line.strip() for line in text.splitlines() if line.strip().startswith('python '))


def verify():
    commands=[]
    for path in sorted(ROOT.rglob('*.html')):
        parser=Commands(); parser.feed(path.read_text())
        for line in parser.lines:
            if line not in commands: commands.append(line)
    for line in ["python -m unittest discover -s labs -p 'test_*.py'",
                 "python labs/reference/curve_tuning.py --units 379,406,385,343,342,388,324,340,330,349"]:
        if line not in commands: commands.append(line)
    env=dict(os.environ, HF_HUB_OFFLINE='1', TRANSFORMERS_VERBOSITY='error', HF_HUB_DISABLE_PROGRESS_BARS='1',
             PYTHONWARNINGS='ignore', TOKENIZERS_PARALLELISM='false')
    output=['Interpretability Methods and Rigor: actual local command transcript',
            'Authoring date: 2026-10-20',
            f'Python: {sys.version}', f'Interpreter: {sys.executable}', f'Platform: {platform.platform()}',
            'Packages: '+', '.join(f'{p} {version(p)}' for p in PACKAGES),
            'Models: gpt2 (124M) from the local Hugging Face cache via TransformerLens TransformerBridge '
            'with compatibility mode; torchvision GoogLeNet IMAGENET1K_V1 from the local torch hub cache.',
            'All runs are CPU-only and offline (HF_HUB_OFFLINE=1). Seeds are fixed in the scripts.', '']
    for line in commands:
        args=shlex.split(line); args[0]=sys.executable
        runs=[(line,env,True)]
        if 'unittest' in line:
            # Against the learner stubs the suite fails by design (NotImplementedError);
            # against the reference solutions it must pass.
            runs=[(line+'   # learner stubs: expected to fail until implemented',env,False),
                  ('INTERP_LAB_IMPL=reference '+line,dict(env,INTERP_LAB_IMPL='reference'),True)]
        for shown,e,must_pass in runs:
            t=time.time()
            result=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,timeout=1800,env=e)
            err='\n'.join(l for l in result.stderr.splitlines() if 'warn' not in l.lower() and 'Loading weights' not in l)
            if 'unittest' in line:
                err='\n'.join(l for l in err.splitlines() if not l.startswith(('  File','    ','Traceback')))
            output.extend(['$ '+shown,result.stdout.rstrip(),err.rstrip(),f'[exit {result.returncode}; {time.time()-t:.0f} s]',''])
            if result.returncode and must_pass:
                raise RuntimeError(f'{line} failed:\n{result.stderr}')
    target=ROOT/'research/verify/lab-transcript.txt'
    target.write_text('\n'.join(output).rstrip()+'\n')
    print(f'PASS: {len(commands)} documented and boundary commands executed; transcript saved to {target.relative_to(ROOT)}.')


if __name__=='__main__': verify()
