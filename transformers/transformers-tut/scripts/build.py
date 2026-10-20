"""Build the offline HTML course from original lesson sources."""
import json
import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path

from common import MODULES
from sources import SOURCES
from glossary import GLOSSARY
from foundations import LESSONS as FOUNDATIONS
from heads import LESSONS as HEADS
from mlps import LESSONS as MLPS
from whole import LESSONS as WHOLE
from tooling import LESSONS as TOOLING
from reference_pages import REFERENCES

ROOT = Path(__file__).resolve().parents[1]
TITLE = 'Transformer Anatomy'
CHECKED = '2026-10-20'
LESSONS = FOUNDATIONS + HEADS + MLPS + WHOLE + TOOLING


class GlossLinks(HTMLParser):
    """Link first term mentions without rewriting code, headings, or other links."""
    def __init__(self, prefix):
        super().__init__(convert_charrefs=False)
        self.prefix, self.parts, self.seen, self.blocked = prefix, [], set(), 0
        self.excluded = {'a','code','pre','h1','h2','h3','h4','script','style','summary','label','button','svg','th'}
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
    nav = [dict(module='Start here',pages=[dict(path='index.html',title='Course home',n='',kw='overview prerequisites toolchain')])]
    for i,(title,_) in enumerate(MODULES):
        nav.append(dict(module=f'{i} · {title}', pages=[{k:l[k] for k in ('path','title','n','kw')} for l in LESSONS if l['module']==i]))
    nav.append(dict(module='Reference and practice',pages=[{k:r.get(k,'') for k in ('path','title','n','kw')} for r in REFERENCES]+[
        dict(path='glossary.html',title='Glossary',n='',kw='definitions terms'),
        dict(path='bibliography.html',title='Annotated bibliography',n='',kw='sources provenance papers')]))
    return nav


def shell(path,title,kicker,lede,body,nav):
    prefix = '../' if '/' in path else ''
    flat = [p for mod in nav for p in mod['pages']]
    side = f'<p class="site-title"><a href="{prefix}index.html">{TITLE}</a></p><p class="site-sub">from token ids to logits, one tensor at a time</p>'
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


def build():
    nav = navigation()
    for l in LESSONS:
        src = '<div class="srcbox"><span class="label">Sources and further reading</span><ul>'
        for key in l['sources']:
            s=SOURCES[key]
            src += f'<li><a href="{s["url"]}">{escape(s["title"])}</a></li>'
        src += '</ul><p>Mechanism explanations and pencil examples on this page are original. Sources support the named architectural facts; every number shown in a terminal block was produced by running the command.</p></div>'
        shell(l['path'],l['title'],f'Module {l["module"]} · {MODULES[l["module"]][0]}',l['lede'],l['body']+src,nav)
    for r in REFERENCES:
        shell(r['path'],r['title'],r['kicker'],r['lede'],r['body'],nav)
    cards=''
    for i,(title,desc) in enumerate(MODULES):
        ls=[l for l in LESSONS if l['module']==i]
        cards+=f'<a class="modcard" href="{ls[0]["path"]}"><h3 id="module-{i}"><span class="n">{i}</span>{escape(title)}</h3><p>{desc}</p><div class="pages">{len(ls)} lessons · {ls[0]["n"]}–{ls[-1]["n"]}</div></a>'
    body='''<div class="keyidea"><span class="label">The readiness test</span><p>Implement a GPT-2 forward pass from raw weights, match the reference logits, then re-derive the same activations with TransformerLens and nnsight.</p></div>
<p><a class="start-link" href="pages/00-orientation.html">Start with the function from token ids to logits →</a></p>
<h2 id="outcomes">What you will be able to do</h2><ul><li>Say what a token is, why <code>" the"</code> and <code>"the"</code> differ, and what a token boundary does to a claim about a model.</li><li>Trace one residual-stream vector from embedding to logits and name every write to it.</li><li>Compute one attention head by hand on three tokens, and describe a real head as a QK circuit and an OV circuit.</li><li>Locate a neuron in an MLP, compute GELU and SwiGLU on a pencil example, and say which models use which.</li><li>Write a 150-line GPT-2 forward pass that matches Hugging Face to about 1e-4 and derive its 124,439,808 parameters from the config.</li><li>Find the same activation under its Hugging Face, TransformerLens 4, and nnsight names, with a verified table.</li></ul>
<h2 id="modules">The course</h2><div class="modgrid">'''+cards+'''</div>
<h2 id="how">How to work through it</h2><p>This course assumes the <a href="../../python/python-tut/index.html">Python for Model Internals</a> and <a href="../../linear-algebra/linear-algebra-tut/index.html">Linear Algebra for Interpretability</a> courses: you can load GPT-2, index tensors, and read a matrix product. Each lesson has a worked mechanism, an implication for interpretability work, a pitfall, a check with a revealable explanation, and practice. Pencil examples use numbers you can recompute by hand; terminal blocks show real output from the commands above them.</p>
<p>Read the lessons in order the first time. The three labs under <code>labs/</code> are stubs with tests: tokenization drills (lesson 01), one attention head (lessons 05–06), and the capstone forward pass (lesson 10). The <a href="pages/15-readiness-review.html">readiness review</a> is a rubric for the test above.</p>
<h2 id="practice">Practice locally</h2><p>Open this file directly in a browser; reading needs no server or packages. For the terminal work, use a Python environment with <code>torch</code>, <code>transformers</code>, <code>transformer_lens</code> (4.x), and <code>nnsight</code> installed and GPT-2 small in the Hugging Face cache, then run from this course directory:</p>
<pre class="term"><code>python labs/anatomy.py --help
python labs/anatomy.py tokens "The cat sat on the mat"
python -m unittest discover -s labs -p 'test_*.py' -v</code></pre>
<p>The <a href="appendices/a-shapes-and-notation.html">shapes and notation appendix</a> lists every tensor; the <a href="appendices/b-command-reference.html">command reference</a> lists every inspection command with the lesson it belongs to.</p>
<h2 id="siblings">Part of the path to interpretability</h2><p>This is course 3 of 4 on the path from evals to mechanistic interpretability. It follows <a href="../../python/python-tut/index.html">Python for Model Internals</a> and <a href="../../linear-algebra/linear-algebra-tut/index.html">Linear Algebra for Interpretability</a>, and leads into <a href="../../interpretability/interpretability-tut/index.html">Interpretability Methods and Rigor</a>. The rigor habits come from <a href="../../statistics/statistics-tut/index.html">Statistics for Evals</a> and <a href="../../evals/evals-tut/index.html">Understanding LLM Evals</a>: state what a claim predicts before looking.</p>
<div class="callout"><span class="label">Sources and scope</span><p>Architectural facts are supported by the <a href="bibliography.html">annotated bibliography</a> or by the installed model's config and weights, with the command recorded. The code is small enough to read in full. It teaches anatomy on GPT-2 small; it is not a general or fast implementation.</p></div>'''
    shell('index.html',TITLE,'An offline wiki-course · Transformer anatomy for interpretability',
          'Residual stream, attention heads, MLP layers, gated MLPs, and tokenization, built up to a GPT-2 forward pass from raw weights that matches the reference.',body,nav)
    gloss='<div data-glossary>'
    for slug,g in sorted(GLOSSARY.items(),key=lambda pair:pair[1]['name'].lower()):
        gloss+=f'<div class="gloss-entry"><h2 id="{slug}">{escape(g["name"])}</h2><p>{escape(g["defn"])}</p></div>'
    gloss+='</div>'
    shell('glossary.html','Glossary','Reference','Definitions in the language of model internals. Linked terms in lessons also show keyboard-accessible tooltips.',gloss,nav)
    bib=f'<p>These sources were opened and checked during authoring on {CHECKED}. The notes identify the scope verified; they do not claim that an entire source was independently reproduced. Facts about the installed GPT-2 checkpoint were verified against its config and state dict, with the commands recorded in the <a href="research/verify/lab-transcript.txt">transcript</a>.</p>'
    for key,s in SOURCES.items():
        bib+=f'<h2 id="{key}">{escape(s["tag"])}</h2><p><a href="{s["url"]}">{escape(s["title"])}</a></p><p>{escape(s["claims"])}</p>'
    bib+='<p>See <a href="research/source-checks.md">source-checking notes</a> and <a href="research/sources.json">the machine-readable source record</a>. No benchmark results or model-quality claims are asserted.</p>'
    shell('bibliography.html','Annotated bibliography','Sources and provenance','Primary papers, library documentation, and installed model code, with the verified scope of each source.',bib,nav)
    (ROOT/'assets/nav-data.js').write_text('window.NAV = '+json.dumps(nav,ensure_ascii=False,indent=2)+';\n')
    glossary={slug:dict(name=g['name'],short=g['short'],**{'def':g['defn']}) for slug,g in GLOSSARY.items()}
    (ROOT/'assets/glossary-data.js').write_text('window.GLOSSARY = '+json.dumps(glossary,ensure_ascii=False,indent=2)+';\n')
    (ROOT/'research/sources.json').write_text(json.dumps({key:dict(s,checked=CHECKED,status='confirmed-with-stated-scope') for key,s in SOURCES.items()},ensure_ascii=False,indent=2)+'\n')
    (ROOT/'research/glossary.json').write_text(json.dumps(glossary,ensure_ascii=False,indent=2)+'\n')
    print(f'Built {len(LESSONS)} lessons, {len(REFERENCES)} appendices, home, glossary, and bibliography.')


if __name__=='__main__':
    build()
