# What remains for Python for Model Internals

State on 2026-10-20: all 17 lessons, two appendices, glossary, bibliography,
labs, transcript and checks are complete. Nothing blocks the next course.
Optional follow-ups, in priority order:

1. **Rendered browser check.** `check_site.py` validates structure, links and
   verified output; nobody has looked at the pages in a browser. Check the
   dark terminal blocks (`pre.term`) and the `namemap` table on a narrow
   screen.
2. **Sibling links.** `check_site.py` currently allows missing targets for the
   three courses being authored in parallel (`PENDING_SIBLINGS`). Once they
   exist, remove that allowance so a broken link fails the check again.
3. **Readiness-review producer.** Lesson 16 specifies `labs/cache_run.py` and
   leaves it to the learner. If a tutor wants a reference producer, keep it
   outside the repository, per the no-published-solutions rule.
4. **Word counts.** Lessons run 1,032–1,314 words including pasted output and
   source notes, at the low end of the 1,200–1,800 target. Candidates to
   deepen if wanted: lesson 06 (more indexing drill) and lesson 11 (a second
   custom module with buffers).
5. **ROADMAP versions.** The authoring run had numpy 2.5.4; the roadmap table
   says 2.5.3. The transcript is authoritative; the coordinator may want to
   update the table.
