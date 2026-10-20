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
from inference import LESSONS as INFERENCE
from structure import LESSONS as STRUCTURE
from measurement import LESSONS as MEASUREMENT
from decisions import LESSONS as DECISIONS
from screening import LESSONS as SCREENING
from reference_pages import REFERENCES

ROOT = Path(__file__).resolve().parents[1]
TITLE = 'Statistics for Evals'
LESSONS = FOUNDATIONS + INFERENCE + STRUCTURE + MEASUREMENT + DECISIONS + SCREENING


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
    side = f'<p class="site-title"><a href="{prefix}index.html">{TITLE}</a></p><p class="site-sub">from observations to defensible decisions</p>'
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
        src += '</ul><p>Examples and fixtures on this page are original and synthetic. Sources support the named methods; they are not reports of the fictional agents.</p></div>'
        shell(l['path'],l['title'],f'Module {l["module"]} · {MODULES[l["module"]][0]}',l['lede'],l['body']+src,nav)
    for r in REFERENCES:
        shell(r['path'],r['title'],r['kicker'],r['lede'],r['body'],nav)
    cards=''
    for i,(title,desc) in enumerate(MODULES):
        ls=[l for l in LESSONS if l['module']==i]
        cards+=f'<a class="modcard" href="{ls[0]["path"]}"><h3 id="module-{i}"><span class="n">{i}</span>{escape(title)}</h3><p>{desc}</p><div class="pages">{len(ls)} lessons · {ls[0]["n"]}–{ls[-1]["n"]}</div></a>'
    body='''<div class="keyidea"><span class="label">The professional target</span><p>Given an eval report, explain what it measures, whether the uncertainty calculation fits the data, and what decision the evidence supports.</p></div>
<p><a class="start-link" href="pages/00-orientation.html">Start with what statistics lets you say →</a></p>
<h2 id="outcomes">What you will be able to do</h2><ul><li>Define a score’s population, denominator, and run policy.</li><li>Read confidence intervals and compare systems on paired tasks.</li><li>Handle repeated runs, related repositories, missing outcomes, and task mixtures.</li><li>Evaluate a grader and inspect probability forecasts.</li><li>Plan sample sizes and avoid misleading comparisons or stopping rules.</li><li>Write an analysis and decision memo another engineer can reproduce.</li><li>Screen thousands of candidate neurons or features, count what chance would pass, and confirm a winner on held-out data.</li></ul>
<h2 id="modules">The course</h2><div class="modgrid">'''+cards+'''</div>
<h2 id="how">How to work through it</h2><p>This beginner course assumes percentages and averages, then builds the rest. Each lesson includes an eval scenario, worked reasoning, a pitfall, and a check with a revealable explanation. Selected lessons add terminal experiments where simulation makes the idea easier to see.</p>
<p>The running case compares two fictional agent versions. Start with independent tasks, then add repeated attempts, related repositories, and a sensitive category. All data are synthetic. Finish by defending a decision with a report template and a readiness rubric.</p>
<h2 id="practice">Practice locally</h2><p>Open this file directly in a browser. Reading needs no server or packages. For terminal labs, use Python 3.9+ and run from this course directory:</p>
<pre class="term"><code>python3 labs/stats_lab.py quiz
python3 labs/stats_lab.py compare</code></pre>
<p>Try the <a href="appendices/b-explorers.html">interactive calculators</a>, keep the <a href="appendices/a-math.html">math reference</a> nearby, or use the <a href="appendices/c-command-reference.html">command reference</a>. The <a href="appendices/d-reading-map.html">reading map</a> offers shorter routes for reviewing results or designing an experiment.</p>
<h2 id="siblings">Part of your evals curriculum</h2><p>This course follows the offline wiki format of <a href="../../evals/evals-tut/index.html">Understanding LLM Evals</a>, <a href="../../networking/networking-tut/index.html">Networking for LLM Evals</a>, and <a href="../../linux/linux-tut/index.html">Linux for Evals Engineers</a>: a searchable sidebar, glossary links, readable worked examples, and previous/next navigation.</p>
<div class="callout"><span class="label">Sources and scope</span><p>Original explanations and examples are supported by the <a href="bibliography.html">annotated primary-source bibliography</a>. The terminal code is deliberately small enough to inspect. It teaches statistical judgment and selected methods; it is not a general production analysis package.</p></div>'''
    shell('index.html',TITLE,'An offline wiki-course · Statistics for evaluation work',
          'The statistics you need to design evals, interpret uncertain results, compare agent versions, and defend a practical decision.',body,nav)
    gloss='<div data-glossary>'
    for slug,g in sorted(GLOSSARY.items(),key=lambda pair:pair[1]['name'].lower()):
        gloss+=f'<div class="gloss-entry"><h2 id="{slug}">{escape(g["name"])}</h2><p>{escape(g["defn"])}</p></div>'
    gloss+='</div>'
    shell('glossary.html','Glossary','Reference','Definitions in the language of eval work. Linked terms in lessons also show keyboard-accessible tooltips.',gloss,nav)
    bib='<p>These sources were opened and checked during authoring on 2026-09-21, and for module 6 on 2026-10-20. The notes identify the scope verified; they do not claim that an entire source or every linked method was independently reproduced. The local experiments validate the supplied implementations and synthetic examples.</p>'
    for key,s in SOURCES.items():
        bib+=f'<h2 id="{key}">{escape(s["tag"])}</h2><p><a href="{s["url"]}">{escape(s["title"])}</a></p><p>{escape(s["claims"])}</p>'
    bib+='<p>See <a href="research/source-checks.md">source-checking notes</a> and <a href="research/sources.json">the machine-readable source record</a>. No model-provider performance, prices, or current benchmark rankings are asserted.</p>'
    shell('bibliography.html','Annotated bibliography','Sources and provenance','Primary papers, institutional references, and official method documentation, with the verified scope of each source.',bib,nav)
    (ROOT/'assets/nav-data.js').write_text('window.NAV = '+json.dumps(nav,ensure_ascii=False,indent=2)+';\n')
    glossary={slug:dict(name=g['name'],short=g['short'],**{'def':g['defn']}) for slug,g in GLOSSARY.items()}
    (ROOT/'assets/glossary-data.js').write_text('window.GLOSSARY = '+json.dumps(glossary,ensure_ascii=False,indent=2)+';\n')
    (ROOT/'research/sources.json').write_text(json.dumps({key:dict(s,checked=s.get('checked','2026-09-21'),status='confirmed-with-stated-scope') for key,s in SOURCES.items()},ensure_ascii=False,indent=2)+'\n')
    (ROOT/'research/glossary.json').write_text(json.dumps(glossary,ensure_ascii=False,indent=2)+'\n')
    print(f'Built {len(LESSONS)} lessons, {len(REFERENCES)} appendices, home, glossary, and bibliography.')


if __name__=='__main__':
    build()
