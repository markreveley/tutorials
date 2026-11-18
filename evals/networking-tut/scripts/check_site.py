"""Check generated static pages, links, glossary targets, and curriculum coverage."""
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
from course_content import LESSONS, SOURCES

ROOT=Path(__file__).resolve().parents[1]
errors=[]
glossary=json.loads((ROOT/'research/glossary.json').read_text())

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.links=[]; self.terms=[]; self.h1=0; self.details=0; self.anchors=0; self.text=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids: errors.append(f'{current}: duplicate id {attrs["id"]}')
            self.ids.add(attrs['id'])
        for key in ('href','src'):
            if key in attrs: self.links.append(attrs[key])
        if 'data-g' in attrs: self.terms.append(attrs['data-g'])
        if tag=='h1': self.h1+=1
        if tag=='details': self.details+=1
        if tag=='a':
            if self.anchors: errors.append(f'{current}: nested anchor')
            self.anchors+=1
    def handle_endtag(self,tag):
        if tag=='a': self.anchors=max(0,self.anchors-1)
    def handle_data(self,data): self.text.append(data)

pages={}
for path in ROOT.rglob('*.html'):
    current=str(path.relative_to(ROOT)); parsed=Page(); parsed.feed(path.read_text()); pages[path.resolve()]=parsed
    if parsed.h1!=1: errors.append(f'{current}: expected one h1')
    for slug in parsed.terms:
        if slug not in glossary: errors.append(f'{current}: unknown glossary term {slug}')

gloss=pages[(ROOT/'glossary.html').resolve()]
for slug in glossary:
    if slug not in gloss.ids: errors.append('Missing static glossary anchor: '+slug)
for path,parsed in pages.items():
    for link in parsed.links:
        split=urlsplit(link)
        if split.scheme or split.netloc: continue
        target=(path.parent/unquote(split.path)).resolve() if split.path else path
        if not target.is_relative_to(ROOT.resolve()): errors.append(f'{path.name}: link leaves course: {link}'); continue
        if not target.exists(): errors.append(f'{path.name}: missing target {link}'); continue
        if split.fragment and target in pages and unquote(split.fragment) not in pages[target].ids:
            errors.append(f'{path.name}: missing fragment {link}')

nav=json.loads((ROOT/'assets/nav-data.js').read_text().removeprefix('window.NAV = ').removesuffix(';\n'))
nav_paths=[p['path'] for mod in nav for p in mod['pages']]
if len(nav_paths)!=len(set(nav_paths)): errors.append('Duplicate navigation entries')
if len(LESSONS)!=24: errors.append('Expected 24 complete lessons')
for lesson in LESSONS:
    path=(ROOT/lesson['path']).resolve(); page=pages.get(path)
    if not page: errors.append(f'Missing lesson: {lesson["path"]}'); continue
    if not page.details: errors.append(f'Missing reasoning exercise: {lesson["path"]}')
    if not lesson['sources']: errors.append(f'Missing source list: {lesson["path"]}')
    if lesson['path'] not in nav_paths: errors.append(f'Missing nav: {lesson["path"]}')
    if len(' '.join(page.text).split())<300: errors.append(f'Underdeveloped lesson: {lesson["path"]}')
for path in nav_paths:
    if not (ROOT/path).exists(): errors.append('Missing nav target: '+path)

if errors:
    print('\n'.join(errors)); raise SystemExit(1)
words=sum(len(' '.join(parsed.text).split()) for parsed in pages.values())
print(f'PASS: {len(pages)} pages, {len(LESSONS)} lessons, {len(glossary)} glossary entries, {len(SOURCES)} sources.')
print(f'PASS: internal links, fragments, assets, navigation, glossary references, and lesson checks ({words:,} rendered-page words).')
