# eval-tut

**Understanding LLM Evals** — a wiki-style HTML/JS course on evaluating LLM systems, built for entry-level readers.

Open `index.html` in a browser. No build step, no server, no external dependencies — plain HTML/CSS/JS, works from `file://`.

## Structure

```
index.html              course home
pages/                  27 course pages across 8 modules (0–7)
appendices/             A–F: math & stats mini-lessons for entry-level readers
glossary.html           every term, with site-wide hover tooltips
bibliography.html       annotated, verified citation universe
assets/
  style.css             design system
  wiki.js               sidebar nav, search, prev/next, glossary tooltips
  nav-data.js           sitemap (drives nav + search)
  glossary-data.js      glossary entries (drives tooltips + glossary page)
research/
  sources.json          the citation universe with planned claims
  sources/*.json        per-source verification notes (claims checked against the fetched primary source)
  AUTHORING.md          the style/provenance contract all pages follow
```

## Provenance

Every empirical claim in the course traces to a primary source in `research/sources.json`, and each source was fetched and verified (claims confirmed, corrected, or marked unverifiable) before authoring — see `research/sources/`. Pages cite inline and list their sources in a footer box.
