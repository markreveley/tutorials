# Authoring Linear Algebra for Interpretability

## Audience and outcome

Write for a programmer (Elixir and Rust) with no working linear algebra who is
moving toward mechanistic interpretability. Explain each idea in ordinary language,
show it on a two-dimensional example that can be checked by hand, then show it on
the real GPT-2 activations in `labs/data/`. No proofs; numerical checks instead.
The target is the readiness review in lesson 15: find a direction, test it held
out, run PCA and SVD, and narrate every number with what it does not establish.

Follow the statistics course's offline wiki conventions: cream reading surfaces,
serif text, searchable sidebar, glossary, linked lessons, reasoning checks, source
notes, previous/next navigation. No external assets, fonts, requests or packages
at read time. Reading must work without JavaScript.

## Page requirements

Every lesson needs: an interpretability implication (`div.evals`, labelled "In
interpretability work"), a worked example or mechanism, a pitfall, a judgment
question with a revealable explanation, and practice with an answer. Give each
h2/h3 an ID. Explain symbols right after a formula. Write shapes next to every
product. The build links first glossary mentions automatically, excluding
headings, code and existing links.

Every concept is demonstrated on the fixture, not only on toy vectors. The fixture
is one layer of real activations plus one real head's weights; the passage is
original prose written in `labs/make_data.py`.

## Terminal output is never invented

Commands shown in `<pre class="term">` are executed by `scripts/verify_commands.py`
and the transcript is saved to `research/verify/lab-transcript.txt`. Output quoted
in a lesson goes through `common.out(...)`, which renders `pre.term.out`;
`scripts/check_outputs.py` fails the build if any quoted block is not verbatim in
the transcript. If a lab command changes, rebuild, re-verify, and update the quoted
block from the transcript, never from memory. Numbers in prose must come from the
transcript; cross-check them when editing.

## Claims about models

Pure mathematics needs no citation. Any statement about transformers, GPT-2,
superposition, or low-rank circuits is either (a) stated as geometry about the
fixture ("on these 301 tokens…"), or (b) a short quotation from a source recorded
in `scripts/sources.py` and `research/source-checks.md`. Never write a number from
memory of a paper. Do not generalise from the fixture to GPT-2 in general; the
lessons model the discipline of saying "on this passage, at this layer".

## Labs

`labs/linalg.py` holds the learner's stubs; `labs/reference.py` the working
versions; `labs/linalg_lab.py` the CLI used by the lessons (it imports the
reference so it works on a fresh checkout). Tests in `labs/test_linalg.py` use
hand-computed 2-D values and invariants, and skip with the function name while a
stub is unimplemented; `labs/test_reference.py` reruns them against the reference
and checks the fixture and CLI. Keep implementations a few lines each. numpy only
on the learner path; torch only in `make_data.py` and the cross-check script.

## Changes and checks

Edit the Python sources under `scripts/`, then run, from this directory:

```
python3 scripts/build.py
/home/user/.venv-ml/bin/python scripts/verify_commands.py
python3 scripts/check_outputs.py
python3 scripts/check_site.py
/home/user/.venv-ml/bin/python -m unittest discover -s labs -p 'test_*.py' -v
node scripts/check_calculators.js
node --check assets/wiki.js
node --check assets/explorers.js
```

`verify_commands.py` must run with a Python that has numpy (and torch for the last
cross-check command). A structural check is not a rendered-browser check; say which
you did.
