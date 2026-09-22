# Research brief — source verification (linux-tut)

You are a verification agent for the course "Linux for Evals Engineers" at
`/Users/mark/dev/repos/_do/evals/courses/linux/linux-tut/`. Read `research/AUTHORING.md`
(the provenance section) and `research/sources.json` first.

You own ONE group (R1…R7, given in your prompt). For every source in `research/sources.json`
whose `group` is yours:

1. FETCH the primary source(s) (WebFetch; WebSearch only to locate a moved URL or a better
   primary source). Do not rely on memory. If a page is too large for one fetch, fetch the
   specific sub-page/section, or use `curl -sL URL | …` via Bash to grep the raw text
   (man7.org pages and RFCs are plain and grep well; save downloads under your scratch dir
   `research/verify/_raw-<group>/`, which is disposable).
2. For each planned claim decide: `confirmed`, `corrected` (say exactly what is true instead),
   or `unverifiable` (source silent / inaccessible). Record an exact quote (≤60 words) and its
   location (section heading / man-page section). Numbers, defaults and lists must be exact and
   current — where docs have changed from common folklore, that's a `corrected` and the most
   valuable thing you can find.
3. Where a claim says "verify by running", run it in Docker (`docker run --rm ubuntu:24.04 …`;
   images ubuntu:24.04, debian:bookworm-slim, alpine:3.20 are pulled; name any containers
   `lt-<group>-*` and remove them; never prune) and record the command + output as the quote,
   location "executed <image>".
4. Add `extra_findings`: other verified facts from the same source that a course page on the
   topic would want (each with quote + location). Be generous — authors may ONLY use what is in
   your notes. Think about what a page teaching this topic to an evals engineer will need to assert.
5. Write one note per source to `research/sources/<id>.json` using `note_format` from
   sources.json (include `tag`, `fetched_on`: today's date 2026-09-20, canonical `citation.url`).
   Valid JSON, UTF-8. If the true identifier differs (e.g. a wrong issue number), fix `id`/`tag`
   and say so in `teaching_notes`.
6. Sibling-course notes (`../../evals/evals-tut/research/sources/*.json`) may be read as leads,
   but re-fetch anything you reuse.

Primary sources only: man7.org, docs.kernel.org, gnu.org, pubs.opengroup.org, rfc-editor.org,
docs.docker.com, official project docs/repos, arXiv/USENIX papers, the organisation's own posts.
No blogs/StackOverflow/Wikipedia as evidence (fine as leads).

When done, reply with a SHORT report (≤25 lines): files written, count of
confirmed/corrected/unverifiable, and the corrections/surprises authors most need to know.
