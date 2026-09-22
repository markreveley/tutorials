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
        if tag=='pre': self.active='term' in dict(attrs).get('class','').split()
    def handle_endtag(self,tag):
        if tag=='pre': self.active=False
    def handle_data(self,text):
        if self.active:
            self.lines.extend(line.strip() for line in text.splitlines() if line.strip().startswith('python3 '))


def verify():
    commands=[]
    for path in sorted(ROOT.rglob('*.html')):
        parser=Commands(); parser.feed(path.read_text())
        for line in parser.lines:
            if line not in commands: commands.append(line)
    # Also exercise the command-reference table's commands and important edge cases.
    for args in ['rate 0 10','power --sd 0.5 --delta 0.03','sample --trials 100 --p 0.7',
                 'multiple --tests 20','peek','bayes 8 10 --alpha 1 --beta 1']:
        line='python3 labs/stats_lab.py '+args
        if line not in commands: commands.append(line)
    output=['Statistics for Evals: actual local command transcript',
            'Authoring date: 2026-09-21',f'Python: {sys.version}',
            'Quiz stdin supplied by verifier: 1, 2, 3, 2, 2, 3 (one answer per line).',
            'All data are synthetic; no model calls or network requests.', '']
    for line in commands:
        args=shlex.split(line); args[0]=sys.executable
        result=subprocess.run(args,cwd=ROOT,text=True,input='1\n2\n3\n2\n2\n3\n' if args[-1]=='quiz' else '',
                              capture_output=True,timeout=30)
        output.extend(['$ '+line,result.stdout.rstrip(),result.stderr.rstrip(),f'[exit {result.returncode}]',''])
        if result.returncode:
            raise RuntimeError(f'{line} failed: {result.stderr}')
    target=ROOT/'research/verify/lab-transcript.txt'
    target.write_text('\n'.join(output).rstrip()+'\n')
    print(f'PASS: {len(commands)} documented and boundary commands executed; transcript saved.')


if __name__=='__main__': verify()
