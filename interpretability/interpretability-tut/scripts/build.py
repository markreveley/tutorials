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
from evidence import LESSONS as EVIDENCE
from vision import LESSONS as VISION
from language import LESSONS as LANGUAGE
from features import LESSONS as FEATURES
from capstone import LESSONS as CAPSTONE
from reference_pages import REFERENCES

ROOT = Path(__file__).resolve().parents[1]
TITLE = 'Interpretability Methods and Rigor'
LESSONS = FOUNDATIONS + EVIDENCE + VISION + LANGUAGE + FEATURES + CAPSTONE
CHECKED = '2026-10-20'


class GlossLinks(HTMLParser):
    """Link first term mentions without rewriting code, headings, or other links."""
    def __init__(self, prefix):
        super().__init__(convert_charrefs=False)
        self.prefix, self.parts, self.seen, self.blocked = prefix, [], set(), 0
        self.excluded = {'a','code','pre','h1','h2','h3','h4','script','style','summary','label','button','svg','blockquote'}
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
        dict(path='bibliography.html',title='Annotated bibliography',n='',kw='sources provenance quotes')]))
    return nav


def shell(path,title,kicker,lede,body,nav):
    prefix = '../' if '/' in path else ''
    flat = [p for mod in nav for p in mod['pages']]
    side = f'<p class="site-title"><a href="{prefix}index.html">{TITLE}</a></p><p class="site-sub">write the prediction test before you look</p>'
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
        src += '</ul><p>Quotations were checked against the fetched sources; every number from a run on this course’s machine is in <a href="../research/verify/lab-transcript.txt">the transcript</a>. Numbers from papers are only those listed in the <a href="../bibliography.html">bibliography</a> as verified.</p></div>'
        shell(l['path'],l['title'],f'Module {l["module"]} · {MODULES[l["module"]][0]}',l['lede'],l['body']+src,nav)
    for r in REFERENCES:
        shell(r['path'],r['title'],r['kicker'],r['lede'],r['body'],nav)
    cards=''
    for i,(title,desc) in enumerate(MODULES):
        ls=[l for l in LESSONS if l['module']==i]
        cards+=f'<a class="modcard" href="{ls[0]["path"]}"><h3 id="module-{i}"><span class="n">{i}</span>{escape(title)}</h3><p>{desc}</p><div class="pages">{len(ls)} lessons · {ls[0]["n"]}–{ls[-1]["n"]}</div></a>'
    body='''<div class="keyidea"><span class="label">The professional target</span><p>Given a claim about what a neuron, direction, head, or feature does, write the test that would show it on data not yet seen, with the control that would pass if the claim were empty, then run it and report the result either way.</p></div>
<p><a class="start-link" href="pages/00-orientation.html">Start with what “demonstrated” means →</a></p>
<h2 id="outcomes">What you will be able to do</h2><ul><li>Turn an interpretability claim into a pre-registered prediction test with held-out data, a scoring function, controls, and a threshold.</li><li>Explain why max-activating examples mislead and sample activations so they do not.</li><li>Score an explanation by held-out activation prediction and read the random-unit and shuffled-label controls.</li><li>Replicate a vision-neuron claim on InceptionV1 and a language claim on GPT-2 small on a CPU, with the test written first.</li><li>Use probes, the logit lens, activation patching, and induction-head detection, and say what each does and does not establish.</li><li>Read a sparse-autoencoder feature’s explanation and its score, and write up a result, including a negative one, so that it is a contribution.</li></ul>
<h2 id="modules">The course</h2><div class="modgrid">'''+cards+'''</div>
<h2 id="how">How to work through it</h2><p>This is the capstone of the evals-and-interpretability path. It assumes the <a href="../../python/python-tut/index.html">Python for Model Internals</a>, <a href="../../linear-algebra/linear-algebra-tut/index.html">Linear Algebra for Interpretability</a>, and <a href="../../transformers/transformers-tut/index.html">Transformer Anatomy</a> courses, and it leans on the <a href="../../statistics/statistics-tut/index.html">statistics</a> and <a href="../../evals/evals-tut/index.html">evals</a> courses for controls, multiple comparisons, and held-out validation. Each lesson has a worked mechanism, a pitfall, a check with a revealable explanation, and practice. Where a lesson runs code, the output shown was produced on the authoring machine and is kept verbatim in the transcript; replications that failed are reported as failed.</p>
<h2 id="practice">Practice locally</h2><p>Reading needs no server or packages. The labs need a Python environment with torch (CPU is enough), torchvision, transformers, transformer_lens 4, and numpy, with GPT-2 small and torchvision’s GoogLeNet weights cached. From this directory:</p>
<pre class="term"><code>python labs/reference/curve_tuning.py
python labs/reference/neuron_score.py --rule digit
python -m unittest discover -s labs -p 'test_*.py'</code></pre>
<p>In every command on these pages, <code>python</code> means the interpreter of that environment. The learner labs in <code>labs/</code> are stubs with tests; the reference implementations in <code>labs/reference/</code> produced the outputs shown and are there to read after you have tried. The <a href="appendices/a-protocol-template.html">protocol template</a> and the <a href="appendices/b-command-reference.html">command reference</a> are the two pages to keep open.</p>
<h2 id="siblings">Part of your curriculum</h2><p>This course follows the offline wiki format of <a href="../../evals/evals-tut/index.html">Understanding LLM Evals</a> and <a href="../../statistics/statistics-tut/index.html">Statistics for Evals</a>: a searchable sidebar, glossary links, worked examples, and previous/next navigation.</p>
<div class="callout"><span class="label">Sources and scope</span><p>Original explanations are supported by the <a href="bibliography.html">annotated bibliography</a>, which records what was checked in each source. The 2026 essay by Nick Cammarata and the reply by Leo Gao were fetched and are quoted verbatim where used. Experiments use torchvision’s GoogLeNet weights and GPT-2 small; neither is the model the cited papers studied, and the lessons say so wherever it matters.</p></div>'''
    shell('index.html',TITLE,'An offline wiki-course · Capstone of the evals and interpretability path',
          'How to make a claim about a model’s internals that survives a test written before you looked: the methods, the controls, and two replications you can run on a laptop.',body,nav)
    gloss='<div data-glossary>'
    for slug,g in sorted(GLOSSARY.items(),key=lambda pair:pair[1]['name'].lower()):
        gloss+=f'<div class="gloss-entry"><h2 id="{slug}">{escape(g["name"])}</h2><p>{escape(g["defn"])}</p></div>'
    gloss+='</div>'
    shell('glossary.html','Glossary','Reference','Definitions in the language of the course. Linked terms in lessons also show keyboard-accessible tooltips.',gloss,nav)
    bib=f'<p>These sources were fetched and checked during authoring on {CHECKED}. The notes identify the scope verified; they do not claim that an entire source was independently reproduced. Every quotation in the lessons appears verbatim in the fetched text; see <a href="research/source-checks.md">the source-checking notes</a>.</p>'
    for key,s in SOURCES.items():
        bib+=f'<h2 id="{key}">{escape(s["tag"])}</h2><p><a href="{s["url"]}">{escape(s["title"])}</a></p><p>{escape(s["claims"])}</p>'
    bib+='<p>See also <a href="research/sources.json">the machine-readable source record</a>. No claim is made about any model not run here beyond what the verified scope states.</p>'
    shell('bibliography.html','Annotated bibliography','Sources and provenance','Primary papers, the 2026 essay and its critique, and tool documentation, with the verified scope of each.',bib,nav)
    (ROOT/'assets/nav-data.js').write_text('window.NAV = '+json.dumps(nav,ensure_ascii=False,indent=2)+';\n')
    glossary={slug:dict(name=g['name'],short=g['short'],**{'def':g['defn']}) for slug,g in GLOSSARY.items()}
    (ROOT/'assets/glossary-data.js').write_text('window.GLOSSARY = '+json.dumps(glossary,ensure_ascii=False,indent=2)+';\n')
    (ROOT/'research/sources.json').write_text(json.dumps({key:dict(s,checked=CHECKED,status='confirmed-with-stated-scope') for key,s in SOURCES.items()},ensure_ascii=False,indent=2)+'\n')
    (ROOT/'research/glossary.json').write_text(json.dumps(glossary,ensure_ascii=False,indent=2)+'\n')
    print(f'Built {len(LESSONS)} lessons, {len(REFERENCES)} appendices, home, glossary, and bibliography.')


if __name__=='__main__':
    build()
