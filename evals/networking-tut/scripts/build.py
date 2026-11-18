"""Generate a dependency-free, file://-compatible course from original content."""
import json
import re
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from course_content import MODULES, LESSONS, SOURCES

ROOT=Path(__file__).resolve().parents[1]
TITLE='Networking for LLM Evals'
glossary_path=ROOT/'research/glossary.json'
GLOSSARY=json.loads(glossary_path.read_text()) if glossary_path.exists() else {}

class GlossLinks(HTMLParser):
    """Link the first mention of a term, preserving existing markup and links."""
    def __init__(self, prefix):
        super().__init__(convert_charrefs=False)
        self.prefix=prefix; self.parts=[]; self.blocked=0; self.seen=set()
        self.excluded={'a','code','pre','h1','h2','h3','h4','script','style','summary'}
        self.names={entry['name'].lower():slug for slug,entry in GLOSSARY.items()}
        self.pattern=re.compile(r'(?<![\w-])('+'|'.join(re.escape(name) for name in sorted(self.names,key=len,reverse=True))+r')(?![\w-])',re.I) if self.names else None
    def handle_starttag(self,tag,attrs):
        if tag in self.excluded: self.blocked+=1
        self.parts.append(self.get_starttag_text())
    def handle_startendtag(self,tag,attrs): self.parts.append(self.get_starttag_text())
    def handle_endtag(self,tag):
        self.parts.append(f'</{tag}>')
        if tag in self.excluded: self.blocked=max(0,self.blocked-1)
    def handle_entityref(self,name): self.parts.append('&'+name+';')
    def handle_charref(self,name): self.parts.append('&#'+name+';')
    def handle_data(self,data):
        if self.blocked or not self.pattern: self.parts.append(data); return
        def link(match):
            slug=self.names[match[0].lower()]
            if slug in self.seen: return match[0]
            self.seen.add(slug)
            return f'<a class="term" data-g="{slug}" href="{self.prefix}glossary.html#{slug}">{match[0]}</a>'
        self.parts.append(self.pattern.sub(link,data))

def page(path,title,kicker,lede,body):
    prefix='../' if '/' in path else ''
    if path.startswith('pages/'):
        parser=GlossLinks(prefix); parser.feed(body); body=''.join(parser.parts)
    html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · {TITLE}</title><meta name="description" content="{escape(lede,quote=True)}">
<link rel="stylesheet" href="{prefix}assets/style.css"></head><body>
<a class="skip-link" href="#main">Skip to lesson</a><div class="layout"><aside class="sidebar" data-nav aria-label="Course navigation"></aside>
<div class="content"><main class="page" id="main"><p class="kicker">{kicker}</p><h1>{escape(title)}</h1><p class="lede">{lede}</p>
{body}
</main></div></div><script src="{prefix}assets/nav-data.js"></script><script src="{prefix}assets/glossary-data.js"></script><script src="{prefix}assets/wiki.js"></script><script src="{prefix}assets/explorers.js"></script></body></html>'''
    (ROOT/path).write_text(html)

nav=[dict(module='Start here',pages=[dict(path='index.html',title='Course home',n='',kw='overview')])]
for i,(title,desc) in enumerate(MODULES):
    pages=[{k:l[k] for k in ('n','path','title','kw')} for l in LESSONS if l['module']==i]
    if pages: nav.append(dict(module=f'{i} · {title}',pages=pages))
for lesson in LESSONS:
    src=''
    if lesson['sources']:
        src='<div class="srcbox"><span class="label">Sources &amp; further reading</span><ul>'+''.join(f'<li><a href="{SOURCES[k][1]}">{escape(SOURCES[k][0])}</a> — {SOURCES[k][2]}</li>' for k in lesson['sources'])+'</ul></div>'
    page(lesson['path'],lesson['title'],f'Module {lesson["module"]} · {MODULES[lesson["module"]][0]}',lesson['lede'],lesson['body']+src)

body='''<div class="keyidea"><span class="label">The premise of this course</span><p>An eval is also a distributed system. Its requests cross machines, networks, and trust boundaries. Understanding those crossings lets you build reliable runs, investigate failures, and tell a model problem from an infrastructure problem.</p></div>
<p><a class="start-link" href="pages/00-orientation.html">Start with the professional baseline →</a></p>
<h2 id="outcomes">What you’ll be able to do</h2><ul>
<li>Trace an API call through DNS, connections, TLS, HTTP, proxies, and a model service.</li>
<li>Explain an infrastructure diagram and ask concrete questions about its dependencies.</li>
<li>Diagnose failures from the worker’s environment using commands and evidence.</li>
<li>Choose deadlines, retries, and concurrency without silently distorting an evaluation.</li>
<li>Design a small eval system and defend its network and measurement decisions.</li></ul>
<h2 id="modules">The modules</h2><div class="modgrid">'''
for i,(title,desc) in enumerate(MODULES):
    lessons=[l for l in LESSONS if l['module']==i]
    tag='a' if lessons else 'div'
    href=f' href="{lessons[0]["path"]}"' if lessons else ''
    body+=f'<{tag} class="modcard"{href}><h3><span class="n">{i}</span>{title}</h3><p>{desc}</p><div class="pages">{len(lessons)} lessons</div></{tag}>'
body+='''</div><h2 id="how-to-use">A course you can work through</h2><p>Start from zero, follow one eval request, and add the infrastructure around it. Lessons include worked examples, diagrams, common mistakes, and questions with explanations. The local lab lets you observe real HTTP responses, slow requests, retries, and streaming without a model API key.</p>
<p>Read in sequence, or use the sidebar search to find a topic. Technical terms link to the glossary. The appendix reading map points into the book when you want more depth.</p>'''
extras=ROOT/'scripts/reference_pages.py'
if extras.exists():
    from reference_pages import REFERENCES
    refs=[]
    for ref in REFERENCES:
        page(ref['path'],ref['title'],ref['kicker'],ref['lede'],ref['body'])
        refs.append(dict(path=ref['path'],title=ref['title'],n=ref.get('n',''),kw=ref.get('kw','')))
    nav.append(dict(module='Reference & practice',pages=refs))
    body+='''<h2 id="reference">Keep these nearby</h2><ul><li><a href="glossary.html">Glossary</a> — networking vocabulary in plain language.</li><li><a href="appendices/a-calculators.html">Network calculators</a> — work through subnet and throughput examples.</li><li><a href="appendices/b-commands.html">Command reference</a> — what to run, what it establishes, and what it does not.</li><li><a href="appendices/c-reading-map.html">Book reading map</a> — a focused route through <em>Computer Networks: A Systems Approach</em>.</li><li><a href="bibliography.html">Annotated bibliography</a> — primary sources and attribution.</li></ul>'''
body+='''<div class="callout"><span class="label">About the sources</span><p>Concepts draw on Larry Peterson and Bruce Davie’s <a href="https://7e.systemsapproach.org/part_one.html">Computer Networks: A Systems Approach</a>. This is an independently written, task-focused companion, with original eval scenarios and exercises. Implementation details link to official documentation. Hypothetical measurements are labeled as examples.</p></div>'''
page('index.html',TITLE,'A wiki-course · From first principles to infrastructure fluency','The networking you need to discuss, design, and navigate the infrastructure behind LLM evaluations. Start with no networking background; finish with a request you can trace, a failure you can investigate, and a design you can explain.',body)
(ROOT/'assets/nav-data.js').write_text('window.NAV = '+json.dumps(nav,indent=2)+';\n')
print(f'Built {len(LESSONS)} lessons and course home.')
