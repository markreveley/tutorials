# Test-first assessment layer for the Python course

This directory began as the specification for replacing the LeetCode-oriented
Python and Rust courses with function-first explanation DAGs. On 2026-10-20 the
DAG was retired as a **delivery format** and kept as an **assessment layer**:
the contract checker and the executable Python assessments remain; the graph
acceptance gate does not. See [ROADMAP.md](../ROADMAP.md) for the decision.

What remains active:

- [CONTRACT.md](CONTRACT.md) and `test_contract.py`: the explanation-DAG
  contract and its self-tests. The human acceptance checks in the contract
  (start at the function, explain this code, keep descending, measure the
  learner) still govern how lessons and assessments are reviewed.
- `test_python_evals.py`: executable assessments for the three functions in
  [`python/python-tut/labs/eval_pipeline.py`](../python/python-tut/labs/eval_pipeline.py),
  specified in [`python/python-tut/labs/ASSESSMENTS.md`](../python/python-tut/labs/ASSESSMENTS.md).
  Red on the supplied stubs; no reference solution is published.
- `test_sources.py`, `verify_beatcode.py`, and `fixtures/`: the pinned beatcode
  excerpts and their integrity checks, kept for the parked Rust course.

What was retired or parked:

- `test_courses.py` (the `dag/course.json` acceptance gate) moved to
  `previous-courses-to-re-author/retired/`. No course manifest will be authored.
- The LeetCode-era Python lessons and the Rust lessons, syllabus, and reading
  assessments stay under `previous-courses-to-re-author/`. Rust is deprioritised:
  the interpretability toolchain is Python, so Rust is not on the critical path.

## Run from the repository root

```sh
# Contract self-tests and source integrity: expected green.
python3 -m unittest discover -s dag-tests -p 'test_contract.py' -v
python3 -m unittest discover -s dag-tests -p 'test_sources.py' -v

# Learner assessments: red until the learner implements the stubs.
python3 -m unittest discover -s dag-tests -p 'test_python_evals.py' -v
```

Only Python's standard library is needed.

## Verified baseline — 2026-10-20

- 31 contract tests and 3 source-integrity tests pass.
- All 22 Python learner tests reach the intended unimplemented stubs (65 errors
  including individual table cases); no import or discovery errors, no skips.
- The relative links in this file and in the assessment brief resolve locally.

The automated checks establish structure, source identity, and specified code
behavior. They cannot establish teaching quality or personal fluency. Those
require the human checks in the contract and fresh learner attempts. The public
exercises are practice, not a held-out measurement of readiness.

## Beatcode reference

Cloned `https://github.com/ob6to8/beatcode.git` at commit
`b2042746329c21d6bb29deb0cec77ff666eac779` on 2026-09-21. Selected unaltered
function excerpts and the upstream license are retained in `fixtures/beatcode/`;
`fixtures/beatcode.lock.json` records immutable source URLs, line ranges, excerpt
hashes, and full source-file hashes.

```sh
python3 dag-tests/verify_beatcode.py /path/to/beatcode-checkout
```

Offline tests verify the retained excerpts. The command above additionally
compares them with a pinned checkout.
