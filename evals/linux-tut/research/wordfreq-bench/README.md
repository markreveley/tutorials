# wordfreq-bench — the course's running example

A toy agentic benchmark, small enough to read in five minutes, used by many pages. Authors: use
these files verbatim (copy them into your verification containers); do not fork the design.

| Path | What it is |
|---|---|
| `app/` | The task repo the agent sees at `/app`: buggy `wordfreq.py`, `data/sample.txt`, one visible test. Task: make it count case-insensitively and ignore punctuation. |
| `grader/` | Hidden tests, `expected.json`, and `run-tests.sh` (shellcheck-clean; writes one JSON result line; exit status = test status; 60 s timeout). |
| `solution/` | The oracle fix. |
| `Dockerfile.sloppy` | Deliberately bad build: full git history with the fix on branch `upstream-fix`, grader shipped world-readable in `/opt/grader`, solution COPY'd then `rm`'d (still in a layer), agent is root. Needs `./make-sloppy-repo.sh` first. Tag: `wordfreq-bench:sloppy`. |
| `Dockerfile` | Hardened build: exported tree (no `.git`), no grader or solution in the image, user `agent` (uid 1001). Tag: `wordfreq-bench:hardened`. |
| `run-hardened.sh` | The full locked-down `docker run` line (non-root, cap-drop ALL, no-new-privileges, read-only root + tmpfs /tmp + volume for /app, no network, memory/cpu/pids limits, init). |
| `grade.sh` | Grades from OUTSIDE: `docker cp` the finished `/app` out, run hidden tests against the copy in a fresh network-less read-only container. |
| `gen_results.py` | Deterministic 192-line `results.jsonl` (3 models × 8 tasks × 8 epochs) for the text-fu page. |

Note for pages 7–8 (in-box permissions variant): to teach mode bits, start from
`wordfreq-bench:hardened`, and as root add `/opt/grader` (root:root, mode 700) containing
`grader/` — then show user `agent` being denied, and the three ways that protection fails.
Ubuntu 24.04's image already has a user `ubuntu` at uid 1000, which is why `agent` is 1001.
