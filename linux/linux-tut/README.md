# linux-tut

**Linux for Evals Engineers** — a wiki-style HTML/JS course that teaches Linux to someone who
wants to be employable doing AI evaluation work, especially agentic evals, where the thing under
test is a model acting inside a Linux sandbox. Sibling of `../../evals/evals-tut`
("Understanding LLM Evals") and `../../networking/networking-tut` ("Networking for LLM Evals"),
built on the same engine; its evals-first conventions follow the networking course.

Open `index.html` in a browser. No build step, no server, no external dependencies — plain
HTML/CSS/JS, works from `file://`.

The competence target is the **ten-minute audit**: dropped into an unfamiliar Linux box as root,
within ten minutes you can say what is running, what is mounted and whether it is read-only, who
owns what, what the box can reach, and where the logs are — and why each answer matters for
whether an eval score can be trusted.

## Structure

```
index.html              course home
pages/                  29 lessons: orientation + lab setup, then 7 modules
appendices/             A–G: command reference, exit codes, bit/CIDR math, regex, macOS vs Linux, man pages, skills checklist
glossary.html           every term, with site-wide hover tooltips
bibliography.html       annotated, verified citation universe
assets/
  style.css             design system (eval-tut lineage + terminal, lab, and "in eval work" components)
  wiki.js               sidebar nav, search, prev/next, glossary tooltips
  nav-data.js           sitemap + site title (drives nav + search)
  glossary-data.js      glossary entries (generated from research/gloss-part*.json by research/build-glossary.py)
research/
  AUTHORING.md          the style/provenance contract all pages follow
  PAGE-BRIEFS.md        the design brief for every page
  sources.json          the citation universe with planned claims
  sources/*.json        per-source verification notes (claims checked against the fetched primary source)
  verify/*.txt          the real terminal sessions (run in Docker) behind each page's commands and output
  qa.js                 link / slug / nav / escaping / required-box checker  (node research/qa.js)
  build-glossary.py     assembles assets/glossary-data.js from gloss-part*.json
  wordfreq-bench/       the running example: toy agentic benchmark, sloppy + hardened builds
  verify/_raw-*/        research agents' fetched source pages (scratch; gitignored)
```

## Provenance

Two standards (see `research/AUTHORING.md`):

- **Mechanics you can run** — every command and every line of terminal output shown was executed
  in a real Linux container (Ubuntu 24.04 unless stated); the sessions are in `research/verify/`.
- **Facts about the world** — every default, guarantee, number, incident, and quote traces to a
  primary source in `research/sources.json` that was fetched and verified (confirmed, corrected,
  or marked unverifiable) before authoring — see `research/sources/`. Pages cite inline and list
  their sources in a footer box.

## Labs

Every course page ends with a lab. Page 1 sets up the two lab environments: a disposable Docker
container (most pages) and a real VM (systemd, firewalls, root-level namespace work).
