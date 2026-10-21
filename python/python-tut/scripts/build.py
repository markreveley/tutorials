"""Build the offline HTML course from original lesson sources."""
import json
import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import MODULES, ROOT, run
from sources import SOURCES
from glossary import GLOSSARY
from orientation import LESSONS as ORIENTATION
from pythonic import LESSONS as PYTHONIC
from tensors import LESSONS as TENSORS
from models import LESSONS as MODELS
from review import LESSONS as REVIEW
from reference_pages import REFERENCES

TITLE = 'Python for Model Internals'
SUBTITLE = 'from syntax to shapes to cached activations'
LESSONS = ORIENTATION + PYTHONIC + TENSORS + MODELS + REVIEW
CHECKED = '2026-10-20'


class GlossLinks(HTMLParser):
    """Link first term mentions without rewriting code, headings, or other links."""
    def __init__(self, prefix):
        super().__init__(convert_charrefs=False)
        self.prefix, self.parts, self.seen, self.blocked = prefix, [], set(), 0
        self.excluded = {'a','code','pre','h1','h2','h3','h4','script','style','summary','label','button','svg'}
        self.names = {g['name'].lower(): slug for slug,g in GLOSSARY.items()}
        self.pattern = re.compile(r'(?<![\w-])('+'|'.join(re.escape(s) for s in sorted(self.names,key=len,reverse=True))+r')(?![\w-])', re.I)
    def handle_starttag(self, tag, attrs):
        if tag in self.excluded: self.blocked += 1
        self.parts.append(self.get_starttag_text())
    def handle_startendtag(self, tag, attrs): self.parts.append(self.get_starttag_text())
    def handle_endtag(self, tag):
        self.parts.append(f'</{tag}>')
        if tag in self.excluded: self.blocked = max(0,self.blocked-1)
    def handle_entityref(self, name): self.parts.append('&'+name+';')
    def handle_charref(self, name): self.parts.append('&#'+name+';')
    def handle_data(self, data):
        def link(m):
            slug = self.names[m[0].lower()]
            if slug in self.seen: return m[0]
            self.seen.add(slug)
            return f'<a class="term" data-g="{slug}" href="{self.prefix}glossary.html#{slug}">{m[0]}</a>'
        self.parts.append(data if self.blocked else self.pattern.sub(link,data))


def navigation():
    nav = [dict(module='Start here',pages=[dict(path='index.html',title='Course home',n='',kw='overview prerequisites setup')])]
    for i,(title,_) in enumerate(MODULES):
        nav.append(dict(module=f'{i} · {title}', pages=[{k:l[k] for k in ('path','title','n','kw')} for l in LESSONS if l['module']==i]))
    nav.append(dict(module='Reference and practice',pages=[{k:r.get(k,'') for k in ('path','title','n','kw')} for r in REFERENCES]+[
        dict(path='glossary.html',title='Glossary',n='',kw='definitions terms'),
        dict(path='bibliography.html',title='Annotated bibliography',n='',kw='sources provenance attribution')]))
    return nav


def shell(path,title,kicker,lede,body,nav):
    prefix = '../' if '/' in path else ''
    flat = [p for mod in nav for p in mod['pages']]
    side = f'<p class="site-title"><a href="{prefix}index.html">{TITLE}</a></p><p class="site-sub">{SUBTITLE}</p>'
    for mod in nav:
        side += '<div class="nav-module"><span class="mod-label">'+escape(mod['module'])+'</span>'
        for p in mod['pages']:
            current = ' class="current" aria-current="page"' if p['path']==path else ''
            side += f'<a href="{prefix}{p["path"]}"{current}>{escape(p["n"])} {escape(p["title"])}</a>'
        side += '</div>'
    footer = ''
    if path != 'index.html':
        idx = next(i for i,p in enumerate(flat) if p['path']==path)
        footer = '<nav class="pagenav" aria-label="Previous and next page">'
        for offset,label,cls in [(-1,'← Previous','prev'),(1,'Next →','next')]:
            if 0 <= idx+offset < len(flat):
                p=flat[idx+offset]
                footer += f'<a class="{cls}" href="{prefix}{p["path"]}"><span class="dir">{label}</span>{escape(p["title"])}</a>'
        footer += '</nav>'
    if path.startswith('pages/'):
        parser=GlossLinks(prefix); parser.feed(body); body=''.join(parser.parts)
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · {TITLE}</title><meta name="description" content="{escape(lede,quote=True)}">
<link rel="stylesheet" href="{prefix}assets/style.css"></head><body>
<a class="skip-link" href="#main">Skip to content</a><div class="layout"><aside class="sidebar" data-nav aria-label="Course navigation">{side}</aside>
<div class="content"><main class="page" id="main"><p class="kicker">{escape(kicker)}</p><h1>{escape(title)}</h1><p class="lede">{lede}</p>
{body}
{footer}</main></div></div>
<script src="{prefix}assets/nav-data.js"></script><script src="{prefix}assets/glossary-data.js"></script><script src="{prefix}assets/wiki.js"></script></body></html>
'''
    (ROOT/path).write_text(html)


def home_body():
    cards=''
    for i,(title,desc) in enumerate(MODULES):
        ls=[l for l in LESSONS if l['module']==i]
        span = ls[0]['n'] if len(ls)==1 else f'{ls[0]["n"]}–{ls[-1]["n"]}'
        cards+=f'<a class="modcard" href="{ls[0]["path"]}"><h3 id="module-{i}"><span class="n">{i}</span>{escape(title)}</h3><p>{desc}</p><div class="pages">{len(ls)} {"lesson" if len(ls)==1 else "lessons"} · {span}</div></a>'
    return '''<div class="keyidea"><span class="label">The readiness target</span><p>Load GPT-2 small, cache its residual stream for a set of prompts with forward hooks, assert every shape, save the activations with a manifest, and have the eval-pipeline labs green.</p></div>
<p><a class="start-link" href="pages/00-orientation.html">Start with what this course makes you able to do →</a></p>
<h2 id="outcomes">What you will be able to do</h2><ul><li>Read and write everyday Python without translating from Elixir or Rust in your head: names, mutation, dicts, exceptions, generators, dataclasses.</li><li>Write the test first, then the function, with <code>unittest</code>, and keep the eval-pipeline labs green.</li><li>Predict the shape of an array expression before running it, including broadcasting, reductions and einsum.</li><li>Use torch tensors with the right dtype and device, know when you hold a view, and keep autograd out of your inference code.</li><li>Read a model as a module tree, run GPT-2 small, and get logits, next-token predictions and hidden states.</li><li>Capture activations with forward hooks, with TransformerLens 4, and with nnsight, and know which numbers differ and why.</li><li>Save activations and a manifest that another person can check.</li></ul>
<h2 id="modules">The course</h2><div class="modgrid">'''+cards+'''</div>
<h2 id="how">How to work through it</h2><p>This course assumes you can read and write code in some language and have never had to be fluent in Python. Syntax takes weeks; comfort with tensors and shapes takes months, so shapes are the spine of the course: every lesson from 06 on asks you to predict a shape before it shows one. Each lesson has a concrete implication for eval or interpretability work, a worked mechanism, a pitfall, a judgment question with a revealable explanation, and practice with an answer.</p>
<p>Every command shown was executed, and the output printed next to it is the real output from that run, kept in <a href="research/verify/lab-transcript.txt">the verification transcript</a> with the package versions that produced it. Nothing was typed in by hand.</p>
<h2 id="practice">Practice locally</h2><p>Open this file directly in a browser. Reading needs no server or packages. For the terminal work, follow <a href="pages/01-lab-setup.html">lesson 01</a> to create a virtualenv with a CPU-only torch, then run from this course directory:</p>
'''+run('python3 labs/examples/check_setup.py')+run("python3 -m unittest discover -s labs -p 'test_environment.py' -v")+'''
<p>The labs are stubs with tests: <a href="labs/shapes.py">shapes.py</a>, <a href="labs/hooks.py">hooks.py</a>, <a href="labs/manifest.py">manifest.py</a>, and the <a href="labs/eval_pipeline.py">eval pipeline</a> whose spec is <a href="labs/ASSESSMENTS.md">ASSESSMENTS.md</a>. Their tests are red until you implement them. The <a href="appendices/a-shapes.html">shape reference</a> and the <a href="appendices/b-commands.html">command reference</a> are there for when you forget.</p>
<h2 id="siblings">Part of the path from evals to interpretability</h2><p>This is the first barrier on the roadmap. It is followed by <a href="../../linear-algebra/linear-algebra-tut/index.html">Linear Algebra for Interpretability</a>, <a href="../../transformers/transformers-tut/index.html">Transformer Anatomy</a> and <a href="../../interpretability/interpretability-tut/index.html">Interpretability Methods and Rigor</a>. The rigor that lessons here gesture at is taught in <a href="../../statistics/statistics-tut/index.html">Statistics for Evals</a>, and what an eval is for in <a href="../../evals/evals-tut/index.html">Understanding LLM Evals</a>. All five share this offline wiki format.</p>
<div class="callout"><span class="label">Sources and scope</span><p>General explanations are original. Where a lesson quotes specific library behaviour, the <a href="bibliography.html">annotated bibliography</a> records which official page was checked and for what. The code is deliberately small enough to inspect; it teaches habits, not a library.</p></div>'''


def build():
    nav = navigation()
    for l in LESSONS:
        src = '<div class="srcbox"><span class="label">Sources and further reading</span><ul>'
        for key in l['sources']:
            s=SOURCES[key]
            src += f'<li><a href="{s["url"]}">{escape(s["title"])}</a></li>'
        src += '</ul><p>Explanations on this page are original. Sources support the specific library behaviours named; terminal output is from the recorded run.</p></div>'
        shell(l['path'],l['title'],f'Module {l["module"]} · {MODULES[l["module"]][0]}',l['lede'],l['body']+src,nav)
    for r in REFERENCES:
        shell(r['path'],r['title'],r['kicker'],r['lede'],r['body'],nav)
    shell('index.html',TITLE,'An offline wiki-course · Python and PyTorch for evals and interpretability',
          'Enough Python, NumPy and PyTorch to load a model, read its activations by shape, and test what you built.',home_body(),nav)
    gloss='<div data-glossary>'
    for slug,g in sorted(GLOSSARY.items(),key=lambda pair:pair[1]['name'].lower()):
        gloss+=f'<div class="gloss-entry"><h2 id="{slug}">{escape(g["name"])}</h2><p>{escape(g["defn"])}</p></div>'
    gloss+='</div>'
    shell('glossary.html','Glossary','Reference','Definitions in the language of model-internals work. Linked terms in lessons also show keyboard-accessible tooltips.',gloss,nav)
    bib=f'<p>These pages were opened and checked during authoring on {CHECKED}. The notes identify the scope verified; they do not claim that an entire source was independently reproduced. Where a page did not state something the course relies on, the local transcript is the evidence and the note says so.</p>'
    for key,s in SOURCES.items():
        bib+=f'<h2 id="{key}">{escape(s["tag"])}</h2><p><a href="{s["url"]}">{escape(s["title"])}</a></p><p>{escape(s["claims"])}</p>'
    bib+='<p>See <a href="research/source-checks.md">source-checking notes</a> and <a href="research/sources.json">the machine-readable source record</a>.</p>'
    shell('bibliography.html','Annotated bibliography','Sources and provenance','Official documentation pages checked for the specific behaviours the lessons quote.',bib,nav)
    (ROOT/'assets/nav-data.js').write_text('window.NAV = '+json.dumps(nav,ensure_ascii=False,indent=2)+';\n')
    glossary={slug:dict(name=g['name'],short=g['short'],**{'def':g['defn']}) for slug,g in GLOSSARY.items()}
    (ROOT/'assets/glossary-data.js').write_text('window.GLOSSARY = '+json.dumps(glossary,ensure_ascii=False,indent=2)+';\n')
    (ROOT/'research/sources.json').write_text(json.dumps({key:dict(s,checked=CHECKED,status='confirmed-with-stated-scope') for key,s in SOURCES.items()},ensure_ascii=False,indent=2)+'\n')
    (ROOT/'research/glossary.json').write_text(json.dumps(glossary,ensure_ascii=False,indent=2)+'\n')
    print(f'Built {len(LESSONS)} lessons, {len(REFERENCES)} appendices, home, glossary, and bibliography.')


if __name__=='__main__':
    build()
