# Transformer Anatomy

Course 3 of the path from evals to mechanistic interpretability, in the same offline
wiki format as [Statistics for Evals](../../statistics/statistics-tut/index.html),
[Understanding LLM Evals](../../evals/evals-tut/index.html), and the other courses in
this repository. It follows [Python for Model Internals](../../python/python-tut/index.html)
and [Linear Algebra for Interpretability](../../linear-algebra/linear-algebra-tut/index.html)
and leads into [Interpretability Methods and Rigor](../../interpretability/interpretability-tut/index.html).

Open **[index.html](index.html)** directly in a browser. No server, build step, account,
or network is needed to read it. JavaScript adds search and glossary tooltips; the text,
navigation, and answers are static HTML.

The readiness test: implement a GPT-2 small forward pass from raw weights, match the
reference logits, then re-derive the same activations with TransformerLens 4 and nnsight.

## Included

- **16 lessons in five modules**: orientation; tokenization; embeddings and positions;
  the residual stream; layer norm; attention by hand; attention as QK and OV circuits;
  the MLP block; gated MLPs (SwiGLU); unembedding and the logit lens; the forward pass
  from raw weights (capstone); shapes and parameter counts; generation and the KV cache;
  naming maps across Hugging Face, TransformerLens 4, and nnsight; architectural variants
  (RMSNorm, RoPE, SwiGLU, GQA); and a readiness review with a rubric.
- **Two appendices** (shapes and notation; command reference), **51 glossary terms**, and
  **20 annotated sources** with a checked-source record.
- **Pencil examples** that recompute by hand and are also checked by tests: a three-token
  attention head, layer norm and RMSNorm on `[1, 3, 5, 7]`, SwiGLU on a two-vector, a
  five-word byte-pair corpus, softmax on `[2, 1, 0]`, and the 124,439,808 parameter count.
- **Three labs as stubs with tests** under `labs/`: `tokens.py`, `attention.py`, and
  `gpt2_from_scratch.py`, plus `anatomy.py`, a sixteen-command inspection tool whose
  output every lesson quotes.

## Terminal practice

From this directory, in an environment with `torch`, `transformers` (5.x),
`transformer_lens` (4.x), and `nnsight`, and GPT-2 small in the Hugging Face cache:

```sh
python labs/anatomy.py --help
python labs/anatomy.py tokens "The cat sat on the mat"
python labs/anatomy.py attention-demo
python labs/anatomy.py names
python -m unittest discover -s labs -p 'test_*.py' -v
```

Tests that need torch or transformers skip with a message when they are missing. Before
the stubs are implemented the tests fail with `NotImplementedError`, which is the intended
starting state. `labs/reference/` holds the author's solutions; they exist only so that the
course can show verified output for the capstone (`anatomy.py compare --reference`) and so
the tests can be checked (`LAB_IMPL=reference python -m unittest ...`). Learners should not
read them first. `labs/ASSESSMENTS.md` describes held-out variant families for tutors.

## Authoring and validation

Edit prose in `scripts/foundations.py` (lessons 00–04), `heads.py` (05–06), `mlps.py`
(07–09), `whole.py` (10–12), and `tooling.py` (13–15); appendices in
`scripts/reference_pages.py`; terms in `scripts/glossary.py`; sources in `scripts/sources.py`.
Terminal output in lessons is never typed in: `out(command)` copies it from
`research/verify/lab-transcript.txt` at build time, and `check_site.py` rejects any output
line that is not in the transcript. See [the authoring guide](research/AUTHORING.md).

Regenerate and check (the first build renders placeholders until the transcript exists):

```sh
python3 scripts/build.py
/home/user/.venv-ml/bin/python scripts/verify_commands.py
python3 scripts/build.py
python3 scripts/check_site.py
/home/user/.venv-ml/bin/python -m unittest discover -s labs -p 'test_*.py' -v
node --check assets/wiki.js
```

The authoring environment on 2026-10-20 was `/home/user/.venv-ml` with Python 3.13,
torch 2.14.1+cpu, transformers 5.20.2, transformer_lens 4.2.0, nnsight 0.8.1,
numpy 2.5.4; the transcript records the exact versions and every command run.

Validation completed during authoring:

- 21 HTML pages checked for local links, fragments, assets, navigation, heading IDs,
  HTML nesting, glossary references, required lesson components, and transcript-backed output.
- 24 lab tests pass against the reference solutions; the same suite reports
  `NotImplementedError` against the learner stubs, as recorded in the transcript.
- The reference forward pass matches Hugging Face logits to 3.05e-05 on the running
  prompt (largest logit 133.8) and 9.2e-05 on an eighteen-token prompt; residual
  activations match TransformerLens 4 (`no_processing=True`) and nnsight to about 1e-4.
- Rendered browser verification was not performed in this session.

All work is local to this course directory. No hosting or publication was done.
