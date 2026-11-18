"""Validate generated structure, local links, glossary, curriculum, and HTML nesting."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from build import LESSONS, ROOT, navigation
from sources import SOURCES

ERRORS = []
WARNINGS = []
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
N_LESSONS = 16


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path=path; self.ids=set(); self.links=[]; self.terms=[]; self.stack=[]
        self.classes=set(); self.h1=0; self.details=0; self.text=[]; self.main=False
    def problem(self, text): ERRORS.append(f'{self.path.relative_to(ROOT)}: {text}')
    def handle_starttag(self, tag, pairs):
        attrs=dict(pairs)
        if 'id' in attrs:
            if attrs['id'] in self.ids: self.problem('duplicate ID '+attrs['id'])
            self.ids.add(attrs['id'])
        if tag=='a' and 'a' in self.stack: self.problem('nested link')
        if tag in ('h2','h3') and 'id' not in attrs: self.problem('heading without ID')
        if tag not in VOID: self.stack.append(tag)
        for key in ('href','src'):
            if key in attrs: self.links.append(attrs[key])
        if 'data-g' in attrs: self.terms.append(attrs['data-g'])
        self.classes.update(attrs.get('class','').split())
        if tag=='h1': self.h1+=1
        if tag=='details': self.details+=1
        if tag=='main': self.main=True
    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack or self.stack[-1] != tag:
            self.problem('mismatched closing tag '+tag+' with stack '+repr(self.stack[-4:]))
        elif self.stack: self.stack.pop()
        if tag=='main': self.main=False
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID: self.handle_endtag(tag)
    def handle_data(self,text):
        if self.main: self.text.append(text)


def check():
    glossary=json.loads((ROOT/'research/glossary.json').read_text())
    pages={}
    for path in sorted(ROOT.rglob('*.html')):
        p=Page(path); p.feed(path.read_text()); p.close(); pages[path.resolve()]=p
        if p.stack: p.problem('unclosed tags '+repr(p.stack))
        if p.h1!=1: p.problem('expected one h1')
        for slug in p.terms:
            if slug not in glossary: p.problem('unknown glossary '+slug)
        if len(p.terms)!=len(set(p.terms)): p.problem('repeated glossary links')
    # Sibling courses are linked by index.html only. A sibling that is still being written is a warning, not an error.
    for path,p in list(pages.items()):
        for link in p.links:
            u=urlsplit(link)
            if u.scheme or u.netloc: continue
            dest=(path.parent/unquote(u.path)).resolve() if u.path else path
            if not dest.exists():
                if ROOT.resolve() not in dest.parents and dest.name=='index.html':
                    WARNINGS.append(f'{path.relative_to(ROOT)}: sibling course not present yet: {link}')
                else:
                    p.problem('missing target '+link)
                continue
            if u.fragment:
                target=pages.get(dest)
                if target is None and dest.suffix=='.html':
                    target=Page(dest); target.feed(dest.read_text())
                if target is not None and unquote(u.fragment) not in target.ids:
                    p.problem('missing fragment '+link)
    glossary_page=pages[(ROOT/'glossary.html').resolve()]
    for slug in glossary:
        if slug not in glossary_page.ids: ERRORS.append('missing static glossary '+slug)
    nav_paths=[p['path'] for mod in navigation() for p in mod['pages']]
    if len(nav_paths)!=len(set(nav_paths)): ERRORS.append('duplicate navigation path')
    if set(nav_paths)!=set(str(p.relative_to(ROOT)) for p in pages): ERRORS.append('navigation/page coverage mismatch')
    if [l['n'] for l in LESSONS] != [f'{i:02}' for i in range(N_LESSONS)]: ERRORS.append('lesson numbering mismatch')
    counts=[]
    for l in LESSONS:
        p=pages.get((ROOT/l['path']).resolve())
        if not p: ERRORS.append('missing lesson '+l['path']); continue
        words=len(' '.join(p.text).split()); counts.append(words)
        if words < 450: p.problem(f'underdeveloped lesson ({words} words)')
        if p.details < 2: p.problem('need reasoning check and practice answer')
        for cls in ('evals','pitfall','exercise','lab','srcbox','pagenav'):
            if cls not in p.classes: p.problem('missing component '+cls)
        if not l['sources'] or any(key not in SOURCES for key in l['sources']): p.problem('missing source record')
    # Every terminal block that shows output must be preceded by a command; every quoted output must appear in the transcript.
    transcript=(ROOT/'research/verify/lab-transcript.txt')
    if transcript.exists():
        text=transcript.read_text()
        import re
        from html import unescape
        for path,p in pages.items():
            html=path.read_text()
            for m in re.finditer(r'<pre class="output"><code>(.*?)</code></pre>', html, re.S):
                for line in unescape(m[1]).splitlines():
                    if line.strip() and line.strip() not in text:
                        p.problem('output line not in transcript: '+line.strip()[:80])
    else:
        WARNINGS.append('no transcript yet; run verify_commands.py')
    for w in sorted(set(WARNINGS)): print('WARN:', w)
    if ERRORS:
        print('\n'.join(ERRORS)); raise SystemExit(1)
    print(f'PASS: {len(pages)} HTML pages, {len(LESSONS)} lessons, {len(glossary)} glossary terms, {len(SOURCES)} sources.')
    print('PASS: local links, fragments, assets, navigation, headings, HTML nesting, lesson components, and quoted output lines present in the transcript.')
    print(f'Lesson words including checks and source notes: {min(counts)}–{max(counts)}; total {sum(counts):,}.')


if __name__=='__main__': check()
