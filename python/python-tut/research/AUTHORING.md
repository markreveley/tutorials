# Authoring Python for Model Internals

## Audience and outcome

Write for a professional programmer whose languages are Elixir and Rust, who
has spec-and-test habits, and who has never had to be fluent in Python. Do not
explain what a function or a loop is. Do explain, by contrast with what they
know, where Python's semantics differ: names bind to mutable objects, errors
are exceptions, hints are documentation. From module 2 on, shapes are the
spine: every lesson asks the reader to predict a shape before it shows one.

The competence target is the readiness review: cache GPT-2 small's residual
stream with hooks, assert every shape, save with a manifest, labs green.

Follow the statistics, evals, networking and Linux siblings' offline wiki
conventions: cream reading surfaces, serif text, searchable sidebar, glossary,
reasoning checks, source notes, previous/next navigation. Keep the runtime
free of external assets, requests, fonts, and packages. Static reading must
work without JavaScript.

## Page requirements

Every lesson needs a concrete eval or interpretability implication (`evals`
box), a worked mechanism (usually one example script and its output), a
pitfall, a judgment question with a revealable explanation, and practice with
an answer. Give each h2/h3 an ID. Write the shape as a sentence the first
time it appears: `(2, 5, 768)` is "two prompts, five positions, 768 features".
Link to sibling courses by `index.html` only.

## Terminal output is never invented

A lesson shows a command with `run('python3 ...')` from `scripts/common.py`.
That registers the command; `scripts/verify_commands.py` runs every registered
command through the shell with the launching interpreter's `bin` first on
PATH, `HF_HUB_OFFLINE=1`, and records stdout, stderr, exit code and timing in
`research/verify/lab-transcript.txt` and `outputs.json`. The next build pastes
each command's stdout beside it. `check_site.py` fails on a terminal block
without a recorded output and on a registered command without one.

Consequences: edit an example script, then re-run verify and build, or the
page shows stale output and the check does not know. Keep scripts
deterministic (seeds, no timestamps, no memory addresses). Install steps that
cannot be executed by the verifier go in a `code(..., 'sh')` listing and the
prose says they are instructions, not a transcript. Run the verifier from the
ML virtualenv; the transcript header records which interpreter ran.

## Labs

Labs are stubs with tests, in the style of `labs/eval_pipeline.py`: the test
file is the spec, red until implemented, no solution in the repository. Tests
that need torch or the cached `gpt2` weights skip with a message rather than
fail. `test_environment.py` is the exception: it passes as shipped and tests
the machine. Validate a test file against a private reference implementation
outside the repository before shipping it, and record the count in the report.
Describe held-out variant families in `labs/ASSESSMENTS.md` without publishing
cases.

## Provenance

General Python and PyTorch explanations are original and need no citation.
Specific API behaviours the text relies on (broadcasting rules, hook
signatures, what `hidden_states` contains, what compatibility mode changes)
cite the official page in `scripts/sources.py` with the verified scope, and
`research/source-checks.md` says what was fetched. Where a page did not state
something the course relies on, say so and point at the transcript. Never
write a number from memory of a paper.

## Changes and checks

Edit the Python sources, then: build, verify, build, check, run the lab tests,
`node --check assets/wiki.js`. A structural check is not rendered browser
verification; report the distinction.
