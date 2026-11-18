# Next: linux-tut open items

State as of 2026-09-21. The course is complete (29 lessons, appendices A–G, glossary,
bibliography) and `node research/qa.js` passes. Written by Claude Fable 5.1 (research and most
pages), finished on Claude Opus 5 after the Fable credits ran out.

## Planned

- **Independent review by OpenAI Astra** (GPT-6 Astra, the model used for the direction
  reviews). Give it `research/AUTHORING.md`, `research/PAGE-BRIEFS.md`, `research/sources/`,
  and `research/verify/`. Ask it to check: claims that drifted from their source notes, terminal
  output that doesn't match the recorded sessions, contradictions between pages, and the voice
  difference between the Fable-written and Opus-written pages. It needs Docker on this machine to
  re-run commands.

## Decisions

- **Running-example residual risks:** in the hardened build, `grader/test_hidden.py` imports the
  agent's `wordfreq` module into the grader's own process, and reads `data/sample.txt` from the
  submitted tree (the agent could edit it). Page 26 teaches both as audit findings with fixes.
  **Decided 2026-09-21: leave as is**, as teaching material. If they are ever fixed, re-run
  pages 22, 23, 26 and 28 to regenerate their output.
- **Page length:** 20 of 29 lessons exceed the 2,300-word prose target (max 2,862, page 9).
  Accepted as is on 2026-09-21.
- **Raw downloads in git:** `research/verify/_raw-*/` (810 files, 69 MB) went into commit
  `dd59922`, which has been pushed. It's now in `.gitignore`; untrack with
  `git rm -r --cached 'evals/courses/linux/linux-tut/research/verify/_raw-*'`. It stays in history
  unless rewritten.

## Known limits of the verification

- **Not executed (no VM available):** the VM-lab parts. These are systemd output on page 13,
  host nftables and `DOCKER-USER` rules on page 19, and the VM setup on page 1. They are
  described or quoted from docs and labelled that way.
- **Authoring-machine quirks:** all executed output comes from Docker Desktop 28.1.1 on an
  Apple Silicon Mac (arm64, LinuxKit kernel, seccomp unconfined by default, no AppArmor).
  Pages flag these where they show. A native Linux host will differ in places; see the "Known
  quirks" section of `research/AUTHOR-BRIEF.md`.
- **Fast-moving numbers:** the Terminal-Bench scores and the Inspect defaults are dated
  2026-09. Re-verify them before reuse.
- **Tag normalisation:** pages cite `[man7.org]`, `[Debian 12 Notes]`, and
  `[Homebrew: coreutils]`, which have no source note of their own. The bibliography lists them
  under "Cited in passing".

## Editing rules

`research/AUTHORING.md` (including its 2026-09-21 addendum) binds all edits. After editing, run
`python3 research/build-glossary.py` if glossary parts changed, then `node research/qa.js`.
