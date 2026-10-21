# Python for Model Internals

An offline wiki-course on Python, NumPy and PyTorch for someone who programs
professionally in another language and is moving toward evals and mechanistic
interpretability. It follows the format of
[Statistics for Evals](../../statistics/statistics-tut/index.html),
[Understanding LLM Evals](../../evals/evals-tut/index.html),
[Networking for LLM Evals](../../networking/networking-tut/index.html) and
[Linux for Evals Engineers](../../linux/linux-tut/index.html), and it is the
first of the four new courses in the repository [roadmap](../../ROADMAP.md).

Open **[index.html](index.html)** directly in a browser. No server, build step,
account, or external packages are needed to read it. Navigation, lesson text,
glossary definitions, answers, and terminal output are static HTML; JavaScript
adds search and glossary tooltips.

The readiness target: **load GPT-2 small, cache its residual stream for a set
of prompts with forward hooks, assert every shape, save the activations with a
manifest, and have the eval-pipeline labs green.**

## Included

- **17 lessons across five modules**: orientation and setup; Python by contrast
  with Elixir and Rust; arrays and tensors (shapes are the spine); models as
  objects (nn.Module, GPT-2 small, hooks, TransformerLens 4, nnsight,
  artifacts); and a readiness review with a rubric.
- **Two appendices**: a shape reference and a command reference.
- **41 glossary terms** and **18 checked official sources** with a source record.
- **14 example scripts** in `labs/examples/`, each the subject of one lesson,
  whose real output is pasted into the page from the verification transcript.
- **Four labs with tests**: the eval pipeline (three stubs, tested from the
  repository root), `shapes.py`, `hooks.py` and `manifest.py` (43 tests, red
  until implemented), plus `test_environment.py`, which passes as shipped and
  checks the toolchain. Held-out variant families are described, not
  published, in `labs/ASSESSMENTS.md`.

## Terminal practice

From this directory, in a virtualenv with numpy, torch (CPU build),
transformers, safetensors, and optionally transformer-lens and nnsight
(lesson 01 has the install steps). GPT-2 small is downloaded once and then
read offline.

```sh
python3 labs/examples/check_setup.py
python3 -m unittest discover -s labs -p 'test_environment.py' -v
python3 -m unittest discover -s labs -p 'test_*.py' -v
```

The eval-pipeline tests run from the repository root:

```sh
python3 -m unittest discover -s dag-tests -p 'test_python_evals.py' -v
```

Every command shown in a lesson was executed by `scripts/verify_commands.py`
with the interpreter recorded at the top of
[the transcript](research/verify/lab-transcript.txt) (Python 3.13, torch
2.14.1+cpu, transformers 5.20.2, transformer_lens 4.2.0, nnsight 0.8.1,
numpy 2.5.4). The output beside each command is what that run printed.
Learner-facing instructions use generic `python3` and `pip install`.

## Authoring and validation

Edit prose in `scripts/orientation.py`, `pythonic.py`, `tensors.py`,
`models.py` and `review.py`; appendices in `scripts/reference_pages.py`; terms
in `scripts/glossary.py`; sources in `scripts/sources.py`. The engine
(`build.py`, `common.py`, `check_site.py`, `verify_commands.py`, the CSS and
runtime) is copied from the statistics course with one addition: a `run()`
helper registers each shown command, the verifier executes the registry, and
the build pastes the recorded output into the page. `check_site.py` fails on
any terminal block without recorded output. See
[the authoring guide](research/AUTHORING.md).

```sh
python3 scripts/build.py
/path/to/venv/bin/python scripts/verify_commands.py
python3 scripts/build.py
python3 scripts/check_site.py
/path/to/venv/bin/python -m unittest discover -s labs -p 'test_*.py' -v
node --check assets/wiki.js
```

Node is needed only for the JavaScript syntax check. Rendered browser
verification was not performed during authoring; structural checks are not
evidence of layout.

All work is local to this course directory. No hosting or publication was done.
