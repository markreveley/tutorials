# What remains

The course is complete to the brief: 16 lessons (00–15, including the readiness
review), four appendices, glossary, bibliography, labs with stubs and tests, the
real GPT-2 fixture, two browser explorers, and a verified transcript. Every check
in README.md passes. Nothing in scope is unfinished. Items a later session could
take up:

1. **Rendered browser verification.** The explorers' arithmetic is checked by
   `scripts/check_calculators.js`, but no browser was opened in this session. Open
   `appendices/b-explorers.html`, drag both handles in the projection explorer,
   and enter the four example matrices in the SVD explorer; check layout at phone
   width.
2. **Sibling links.** Lessons and the index link to
   `../../interpretability/interpretability-tut/index.html` and
   `../../transformers/transformers-tut/index.html`, which did not exist on disk at
   authoring time. `scripts/check_site.py` lists any still missing.
3. **Statistics course cross-reference.** Lesson 14 links to the statistics
   course's index only. If that course's new lesson on correlation, permutation
   tests and screening gets a stable page name, the link can stay at index level
   per the shared conventions; no change needed.
4. **Second fixture (optional, out of brief).** The held-out variant families in
   lesson 15 describe a second passage or layer; generating one with
   `labs/make_data.py` parameterised by passage and layer would let a tutor run
   them without writing code. Keep it unpublished per `dag-tests/CONTRACT.md`.
