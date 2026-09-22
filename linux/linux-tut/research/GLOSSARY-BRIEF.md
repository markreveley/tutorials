# Glossary brief (linux-tut)

Course: "Linux for Evals Engineers" at `/Users/mark/dev/repos/_do/evals/courses/linux/linux-tut/`.
Read `research/AUTHORING.md` fully (audience, voice, slug list) and `assets/nav-data.js` (the page
list — you will link to these pages). For format and tone, read the first ~10 entries of the
sibling glossary `../../evals/evals-tut/research/gloss-part1.json`.

Write the glossary entries for the slug categories named in your prompt, as ONE JSON object
`{ "<slug>": { "name", "short", "def", "also"?, "see"? }, … }` saved to the file named in
your prompt. Cover EVERY slug in your categories, exactly as spelled; no extra slugs.

- `name`: display name, Title Case for concepts; literal lowercase for commands/files (`chmod`, `jq`, `/dev/null`).
- `short`: ONE sentence, ≤ 35 words, plain text (no HTML) — shown in hover tooltips. Must stand alone for a reader who has never seen the term.
- `def`: 70–140 words, entry-level, *derived not memorized*: what it is, why it exists, and — for
  most entries — one sentence on why an evals engineer cares (what goes wrong in a sandbox /
  benchmark / transcript). May contain `<code>` and 1–3 links to course pages using
  SINGLE-quoted root-relative hrefs: `<a href='pages/10-signals-exit-codes.html'>…</a>`. Pick the
  page(s) from nav-data.js where the term is actually taught. Escape `<`, `>`, `&` in code.
- `also`: comma-separated synonyms/abbreviations if any. `see`: 2–5 related slugs — ONLY slugs
  from the canonical list in AUTHORING.md (any category).
- Accuracy: stick to mechanics that are stable and that you are certain of. For specific
  defaults/numbers (signal numbers 9/15, exit codes 126/127/137, RFC 1918 ranges, port ranges,
  default umask 022) you may state the universally documented values; for anything you are
  less than certain of, verify against man7.org / docs.docker.com / docs.kernel.org (WebFetch)
  or by running it (`docker run --rm ubuntu:24.04 …`), or phrase it without the number.
  Reference platform is Ubuntu 24.04.
- No hype, no filler. Second person is fine.

Validate: `python3 -c "import json;d=json.load(open('<file>'));print(len(d))"` and check every
`see` slug and every href path exists (slug list in AUTHORING.md, paths in nav-data.js).
Reply with a ≤8-line report: file, entry count, anything you were unsure about.
