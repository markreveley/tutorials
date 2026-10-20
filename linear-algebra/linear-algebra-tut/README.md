# Linear Algebra for Interpretability

An introductory linear algebra course for interpretability work, in the same
offline wiki format as [Statistics for Evals](../../statistics/statistics-tut/index.html),
[Python for Model Internals](../../python/python-tut/index.html), and the other
courses in this repository.

Open **[index.html](index.html)** directly in a browser. No server, build step,
account, or external packages are needed to read it. Navigation, lesson text,
glossary definitions, and answers are static HTML; JavaScript adds search,
glossary tooltips, and two explorers.

The starting assumption is that you program and can follow a short argument, with
no linear algebra. The competence target is the **readiness review**: given a
cached activation matrix and a label vector, find a direction by least squares,
measure its projection on held-out tokens against two baselines, run PCA and SVD,
and say what each number means and what it does not establish.

## Included

- **16 lessons across five modules**: vectors, dot products and projection;
  matrices as maps, multiplication, bases, rank; orthogonality and least squares;
  eigenvectors, covariance, PCA, SVD; gradients, correlation baselines, and the
  readiness review with a rubric.
- **Every concept demonstrated on real GPT-2 small activations**: the residual
  stream after block 6 for 302 tokens of an original passage, plus the four weight
  matrices of one attention head, in `labs/data/` (864 KB, numpy only to use).
- **Four appendices**, **55 glossary terms**, and **8 verified sources** (two
  transformer-circuits papers, 3Blue1Brown's chapter list, ARENA's curriculum,
  four NumPy reference pages), with a checked-source record.
- **Two browser explorers**: 2-D projection with draggable vector and direction,
  and a 2×2 matrix SVD showing the unit circle's image.
- **16 lab commands**, one per lesson, plus **16 exercise stubs** with tests the
  learner makes pass.

## Terminal practice

From this directory, with Python 3.10+ and numpy:

```sh
python3 labs/linalg_lab.py --help
python3 labs/linalg_lab.py inspect
python3 labs/linalg_lab.py project --label is_digit
python3 -m unittest discover -s labs -p 'test_*.py' -v
```

`labs/linalg.py` holds the exercises as stubs; tests for unimplemented functions
are reported as skipped with the function name. `labs/reference.py` is the working
version, which the CLI uses so every command runs on a fresh checkout. The
fixture generator `labs/make_data.py` needs torch and transformers and is not
needed to read or run the course; see `labs/data/README.md`.

## Authoring and validation

Edit prose in `scripts/vectors.py`, `maps.py`, `subspaces.py`, `spectra.py`,
`rigor.py`; appendices in `scripts/reference_pages.py`; terms in
`scripts/glossary.py`; sources in `scripts/sources.py`. See
[the authoring guide](research/AUTHORING.md).

Regenerate and check (the verify step needs numpy, and torch for its last command):

```sh
python3 scripts/build.py
/home/user/.venv-ml/bin/python scripts/verify_commands.py
python3 scripts/check_outputs.py
python3 scripts/check_site.py
/home/user/.venv-ml/bin/python -m unittest discover -s labs -p 'test_*.py' -v
node scripts/check_calculators.js
node --check assets/wiki.js
node --check assets/explorers.js
```

Validation completed during authoring on 2026-10-20:

- 23 HTML pages checked for local links, fragments, assets, navigation, heading
  IDs, HTML nesting, glossary references, and required lesson components. Links to
  sibling courses authored in parallel are allowed to resolve later.
- 33 commands executed into `research/verify/lab-transcript.txt` (Python 3.13.16,
  numpy 2.5.4; torch 2.14.1+cpu and transformers 5.20.2 for the fixture, recorded
  in `labs/data/meta.json`). `scripts/check_outputs.py` confirms every output block
  quoted in a lesson appears verbatim in that transcript.
- 44 unit tests: 26 pass against the reference implementation and fixture, 18 skip
  until the learner implements the stubs; with `LINALG_MODULE=reference` all run.
- Node arithmetic checks for the two explorers and syntax checks passed.
- Rendered browser verification was not performed; the explorers' mathematics is
  checked, their layout and drag interaction are not.

All work is local to this course directory. Nothing was hosted or published.
