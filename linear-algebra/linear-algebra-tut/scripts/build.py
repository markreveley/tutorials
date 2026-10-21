"""Build the offline HTML course from original lesson sources."""
import json
import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path

from common import MODULES
from sources import SOURCES
from glossary import GLOSSARY
from vectors import LESSONS as VECTORS
from maps import LESSONS as MAPS
from subspaces import LESSONS as SUBSPACES
from spectra import LESSONS as SPECTRA
from rigor import LESSONS as RIGOR
from reference_pages import REFERENCES

ROOT = Path(__file__).resolve().parents[1]
TITLE = 'Linear Algebra for Interpretability'
SUBTITLE = 'from activation vectors to directions you can defend'
CHECK_DATE = '2026-10-20'
LESSONS = VECTORS + MAPS + SUBSPACES + SPECTRA + RIGOR


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
    nav = [dict(module='Start here',pages=[dict(path='index.html',title='Course home',n='',kw='overview beginner prerequisites')])]
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
<script src="{prefix}assets/nav-data.js"></script><script src="{prefix}assets/glossary-data.js"></script><script src="{prefix}assets/wiki.js"></script><script src="{prefix}assets/explorers.js"></script></body></html>
'''
    (ROOT/path).write_text(html)


def build():
    nav = navigation()
    for l in LESSONS:
        src = '<div class="srcbox"><span class="label">Sources and further reading</span><ul>'
        for key in l['sources']:
            s=SOURCES[key]
            src += f'<li><a href="{s["url"]}">{escape(s["title"])}</a></li>'
        src += '</ul><p>The activations and weights on this page are real GPT-2 small values from the course fixture (<code>labs/data/README.md</code>); the passage they were computed on is original. Mathematical explanations are original; sources support named results, library behaviour, and any statement about models.</p></div>'
        shell(l['path'],l['title'],f'Module {l["module"]} · {MODULES[l["module"]][0]}',l['lede'],l['body']+src,nav)
    for r in REFERENCES:
        shell(r['path'],r['title'],r['kicker'],r['lede'],r['body'],nav)
    cards=''
    for i,(title,desc) in enumerate(MODULES):
        ls=[l for l in LESSONS if l['module']==i]
        cards+=f'<a class="modcard" href="{ls[0]["path"]}"><h3 id="module-{i}"><span class="n">{i}</span>{escape(title)}</h3><p>{desc}</p><div class="pages">{len(ls)} lessons · {ls[0]["n"]}–{ls[-1]["n"]}</div></a>'
    body='''<div class="keyidea"><span class="label">The professional target</span><p>Given a cached activation matrix and a label vector, find a direction, measure its projection on held-out tokens, run PCA and SVD, and say in plain words what every number means and what it does not.</p></div>
<p><a class="start-link" href="pages/00-orientation.html">Start with why an activation is a vector →</a></p>
<h2 id="outcomes">What you will be able to do</h2><ul><li>Read an activation vector, a weight matrix, and a batch of activations as shapes, and predict the shape of any product before computing it.</li><li>Project activations onto a direction and explain what the scalar per token measures.</li><li>Say why a direction need not be a neuron, and what rank and near-orthogonality mean in 768 dimensions.</li><li>Remove a direction from activations and know what that does and does not erase.</li><li>Fit a direction to labels by least squares and check it on tokens you did not fit on.</li><li>Run PCA and SVD on an activation matrix and on a weight product, read the variance explained and the singular values, and name what they do not tell you.</li><li>Compute the gradient of a dot product and a norm, and test whether a correlation with a direction is real.</li></ul>
<h2 id="modules">The course</h2><div class="modgrid">'''+cards+'''</div>
<h2 id="how">How to work through it</h2><p>The course assumes no linear algebra. It assumes you write programs, can follow a short argument, and want the geometry rather than the proofs. Every idea is shown twice: once on a two-dimensional example you can draw, then on real activations from GPT-2 small cached in <code>labs/data/</code>. Each lesson ends with a reasoning check and a practice command whose output is reproduced from a saved transcript.</p>
<p>The fixture is one layer of the residual stream for 302 tokens of an original passage, plus the four weight matrices of one attention head. Nothing is simulated. The first token has an activation about thirty-six times larger than the others; the lessons use that fact rather than hide it.</p>
<h2 id="practice">Practice locally</h2><p>Open this file directly in a browser. Reading needs no server or packages. For the labs you need Python 3.10 or newer and numpy; torch is needed only to regenerate the fixture, which is already included. Run from this course directory:</p>
<pre class="term"><code>python3 labs/linalg_lab.py --help
python3 labs/linalg_lab.py inspect
python3 -m unittest discover -s labs -p 'test_*.py' -v</code></pre>
<p>The exercises live in <code>labs/linalg.py</code> as stubs; the tests skip until you implement each one. Try the <a href="appendices/b-explorers.html">projection and SVD explorers</a>, keep the <a href="appendices/a-math.html">notation reference</a> nearby, use the <a href="appendices/c-command-reference.html">command reference</a>, and follow the <a href="appendices/d-reading-map.html">reading map</a> to the matching 3Blue1Brown chapter and ARENA exercise for each lesson.</p>
<h2 id="siblings">Part of your interpretability curriculum</h2><p>This course sits between <a href="../../python/python-tut/index.html">Python for Model Internals</a>, which teaches how the fixture was cached, and <a href="../../transformers/transformers-tut/index.html">Transformer Anatomy</a>, which uses these matrices inside attention. <a href="../../interpretability/interpretability-tut/index.html">Interpretability Methods and Rigor</a> turns the final lessons into prediction tests on neurons and features, and the <a href="../../statistics/statistics-tut/index.html">statistics course</a> supplies the uncertainty language that lesson 14 only sketches.</p>
<div class="callout"><span class="label">Sources and scope</span><p>Pure mathematics is explained without citation. Statements about models are either stated as geometry or cited to the <a href="bibliography.html">annotated bibliography</a>. The lab code is small enough to read in one sitting; it teaches the moves, it is not a library.</p></div>'''
    shell('index.html',TITLE,'An offline wiki-course · Linear algebra for interpretability work',
          'The dot products, projections, matrix products, PCA and SVD you need to read activations as vectors, shown on real GPT-2 small activations.',body,nav)
    gloss='<div data-glossary>'
    for slug,g in sorted(GLOSSARY.items(),key=lambda pair:pair[1]['name'].lower()):
        gloss+=f'<div class="gloss-entry"><h2 id="{slug}">{escape(g["name"])}</h2><p>{escape(g["defn"])}</p></div>'
    gloss+='</div>'
    shell('glossary.html','Glossary','Reference','Definitions in the language of activations and directions. Linked terms in lessons also show keyboard-accessible tooltips.',gloss,nav)
    bib=f'<p>These sources were opened and checked during authoring on {CHECK_DATE}. The notes identify the scope verified; they do not claim that an entire source was independently reproduced. The local labs validate the supplied implementations on the real fixture.</p>'
    for key,s in SOURCES.items():
        bib+=f'<h2 id="{key}">{escape(s["tag"])}</h2><p><a href="{s["url"]}">{escape(s["title"])}</a></p><p>{escape(s["claims"])}</p>'
    bib+='<p>See <a href="research/source-checks.md">source-checking notes</a> and <a href="research/sources.json">the machine-readable source record</a>. No number from any paper is quoted from memory; every number in the lessons comes from the fixture transcript.</p>'
    shell('bibliography.html','Annotated bibliography','Sources and provenance','Primary papers, institutional references, and official method documentation, with the verified scope of each source.',bib,nav)
    (ROOT/'assets/nav-data.js').write_text('window.NAV = '+json.dumps(nav,ensure_ascii=False,indent=2)+';\n')
    glossary={slug:dict(name=g['name'],short=g['short'],**{'def':g['defn']}) for slug,g in GLOSSARY.items()}
    (ROOT/'assets/glossary-data.js').write_text('window.GLOSSARY = '+json.dumps(glossary,ensure_ascii=False,indent=2)+';\n')
    (ROOT/'research/sources.json').write_text(json.dumps({key:dict(s,checked=CHECK_DATE,status='confirmed-with-stated-scope') for key,s in SOURCES.items()},ensure_ascii=False,indent=2)+'\n')
    (ROOT/'research/glossary.json').write_text(json.dumps(glossary,ensure_ascii=False,indent=2)+'\n')
    print(f'Built {len(LESSONS)} lessons, {len(REFERENCES)} appendices, home, glossary, and bibliography.')


if __name__=='__main__':
    build()
