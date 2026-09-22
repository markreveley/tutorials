# Python and Rust course redesign: tests first

This is the test-first specification for replacing the two LeetCode-oriented
tutorials with function-first explanation DAGs. The lessons have not been
rewritten yet. Missing course manifests and unimplemented Python exercises
deliberately fail; they are not skipped or marked as expected failures.

The [September 20 direction](../../direction/2026-09-20/overview.md) sets the
Python target: implement, test, debug, adapt, and explain real evaluation work.
The September 21 request sets the Rust target: read and explain **beatcode**.
This does not add a Rust allocation to the direction document's 12-week plan
or make Beatbench a dependency of the Python course.

The [evals course](../evals/evals-tut/index.html) supplies measurement context;
the [networking readiness review](../networking/networking-tut/pages/23-readiness-review.html)
models observable explanation and diagnosis assessments.

## Run from the repository root

```sh
# Test the tests: valid DAGs pass, broken DAGs fail; verify source snapshots.
python3 -m unittest discover -s evals/courses/dag-tests -p 'test_contract.py' -v
python3 -m unittest discover -s evals/courses/dag-tests -p 'test_sources.py' -v

# Acceptance gates: RED until the courses and learner implementation exist.
python3 -m unittest discover -s evals/courses/dag-tests -p 'test_courses.py' -v
python3 -m unittest discover -s evals/courses/dag-tests -p 'test_python_evals.py' -v

# All of the above; intentionally nonzero during this tests-first stage.
python3 -m unittest discover -s evals/courses/dag-tests -v
```

Only Python's standard library is needed. These commands avoid the old Python
exercise discovery settings and the old Rust implementation drills.

## What to revies

- [DAG contract and human acceptance checks](CONTRACT.md): edge direction,
  levels, foundational stopping rule, source fidelity, and course scope.
- [Python assessment brief](../python/python-tut/dag/assessments/README.md):
  executable scorer, data-loader, and reporting tests, plus independent transfer.
- [Rust reading assessments](../rust/rust-tut/dag/assessments/reading.md):
  source navigation, prediction, explanation, and change-impact questions.
- [Rust assessor guide](rust-assessor-guide.md): evidence to listen for, kept
  separate from the learner prompts.

The automated checks establish structure, source identity, and specified code
behavior. They cannot establish teaching quality, a sound evaluation design,
or personal fluency. Those require the human checks and fresh learner attempts.
The public exercises are practice, not a held-out measurement of readiness.

## Verified baseline — 2026-09-21

- 31 contract tests and 3 source-integrity tests pass.
- All 9 retained excerpts match the pinned clone, including full-file hashes.
- Both course acceptance tests fail because `dag/course.json` is not authored.
- All 22 Python learner tests reach the intended unimplemented stubs (65
  errors including individual table cases); no import/discovery errors or skips.
- The new Markdown links resolve locally.
- 16 relevant upstream beatcode tests pass: `float_semantics`, `nonfinite`,
  `hardening`, `render_determinism`, and `render_hashes`. Run in the clone with
  `cargo test --offline --test float_semantics --test nonfinite --test hardening --test render_determinism --test render_hashes`.

The Rust prompts and answer guide were checked against the pinned code and
these tests. No learner has been assessed, and no full lesson DAG is claimed.

## Beatcode reference

Cloned `https://github.com/ob6to8/beatcode.git` at commit
`b2042746329c21d6bb29deb0cec77ff666eac779` on 2026-09-21 into
`/private/tmp/beatcode-course-reference-20260921`.
The clone is a disposable reference, not part of this repository. Selected
unaltered function excerpts and the upstream license are retained in
`fixtures/beatcode/`; `fixtures/beatcode.lock.json` records immutable source
URLs, line ranges, excerpt hashes, and full source-file hashes.

```sh
python3 evals/courses/dag-tests/verify_beatcode.py /private/tmp/beatcode-course-reference-20260921
```

Offline tests verify the retained excerpts. The command above additionally
compares them with the pinned checkout. A later upstream revision requires
reviewing the source and assessments before updating the lock. The README in
the pinned repo still calls it a specification seed; the reference selection
uses the actual implementation and tests present in that commit.
