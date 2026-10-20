"""Execute every published Python command and retain a real transcript."""
from html.parser import HTMLParser
from pathlib import Path
import shlex
import subprocess
import sys
from build import ROOT


class Commands(HTMLParser):
    def __init__(self): super().__init__(); self.active=False; self.lines=[]
    def handle_starttag(self,tag,attrs):
        if tag=='pre': cls=dict(attrs).get('class','').split(); self.active='term' in cls and 'out' not in cls
    def handle_endtag(self,tag):
        if tag=='pre': self.active=False
    def handle_data(self,text):
        if self.active:
            self.lines.extend(line.strip() for line in text.splitlines() if line.strip().startswith('python3 ') and 'make_data' not in line)


def verify():
    commands=[]
    for path in sorted(ROOT.rglob('*.html')):
        parser=Commands(); parser.feed(path.read_text())
        for line in parser.lines:
            if line not in commands: commands.append(line)
    # Also exercise boundary cases and the reference run of the exercise tests.
    for args in ['project --label after_period --token 100','probe --label capitalised --ridge 100',
                 'pca --keep-first --k 5','correlation --label after_period --perms 100','similar --token 0']:
        line='python3 labs/linalg_lab.py '+args
        if line not in commands: commands.append(line)
    commands.append('python3 -m unittest discover -s labs -p \'test_*.py\'')
    commands.append('python3 research/verify/crosscheck_transformerlens.py')
    import numpy
    output=['Linear Algebra for Interpretability: actual local command transcript',
            'Authoring date: 2026-10-20',f'Python: {sys.version}',f'numpy: {numpy.__version__}',
            'Fixture: labs/data (GPT-2 small, blocks.6.hook_resid_post, 302 tokens; layer 7 head 0 weights). See labs/data/meta.json for torch/transformers versions.',
            'The last command loads GPT-2 through TransformerLens and needs torch; every other command needs numpy only.', '']
    for line in commands:
        args=shlex.split(line); args[0]=sys.executable
        result=subprocess.run(args,cwd=ROOT,text=True,input='',capture_output=True,timeout=600)
        if 'crosscheck' in line:
            result_stderr='\n'.join(l for l in result.stderr.splitlines() if 'warn' not in l.lower() and 'Loading' not in l)
            result=subprocess.CompletedProcess(args,result.returncode,result.stdout,result_stderr)
        output.extend(['$ '+line,result.stdout.rstrip(),result.stderr.rstrip(),f'[exit {result.returncode}]',''])
        if result.returncode:
            raise RuntimeError(f'{line} failed: {result.stderr}')
    target=ROOT/'research/verify/lab-transcript.txt'
    target.write_text('\n'.join(output).rstrip()+'\n')
    print(f'PASS: {len(commands)} documented and boundary commands executed; transcript saved.')


if __name__=='__main__': verify()
