# Roadmap: from evals to interpretability

State as of 2026-10-20. This file records the plan, the decisions behind it,
and the conventions every new course follows. It lives with the courses so a
future session can pick up without the conversation that produced it.

## The goal

A career in evals and interpretability. The advice this plan follows ranks the
technical barriers by how much they slow that down:

1. **Python and PyTorch.** The entire interpretability toolchain is Python.
2. **Linear algebra at a working level.** Projections, dot products, matrix
   multiplication, the intuition behind PCA and SVD. No proofs.
3. **Transformer anatomy.** Residual stream, attention heads, MLPs, gating,
   tokenization.
4. **Compute, but less than you would think.** GPT-2 small, Pythia, Gemma 2B,
   Qwen3-0.6B, and InceptionV1 run on a laptop or free Colab.
5. **Experimental rigor, the hard one.** An explanation that cannot predict a
   neuron's activations on held-out data has not been demonstrated. Write the
   prediction test before you look at the neuron. (The essay is Cammarata,
   "Neural Networks Are Already Clean", already-clean.goodfire.com, 2026; the
   critique is Leo Gao's reply on X, verbatim "if you can't simulate a neuron
   you haven't really explained it". The sentence above is the advisor's
   paraphrase. Both are verified in `evals/evals-tut/research/sources/`.)

## Where the repository stood

| Course | State | Serves |
|---|---|---|
| `evals/evals-tut` | Complete, 27 pages, source-verified | Evals half of the goal |
| `statistics/statistics-tut` | Complete, 24 lessons plus Python lab | Rigor (barrier 5) |
| `linux/linux-tut` | Complete, 29 lessons | Eval infrastructure |
| `networking/networking-tut` | Complete, 24 lessons plus lab | Eval infrastructure |
| `elixir/`, `beam/` | Complete | Not on the path; kept as is |
| `dag-tests/` | Contract and tests; no lessons authored | Assessment layer only (see below) |

Nothing in the repository covered barriers 1 to 4. Barrier 5 was covered in
spirit (name the estimand first, held-out grader validation, control checks,
ablations, multiple comparisons, stopping rules) but never framed for claims
about a model's internals.

## Decisions

- **Retire the explanation DAG as a delivery format; keep it as an assessment
  layer.** The contract tests and the three executable Python assessments
  stay. The `course.json` acceptance gate is parked. Lessons are authored in
  the existing wiki engine, which has produced four finished courses.
- **Deprioritise Rust.** The toolchain is Python. The Rust lessons, syllabus,
  reading assessments, and pinned beatcode fixtures stay parked under
  `dag-tests/previous-courses-to-re-author/`.
- **Ship the eval-pipeline exercises as the first Python labs.** They moved to
  `python/python-tut/labs/`; the new Python course builds on them.
- **Do not expand the four finished courses** except for the bridging pages
  below. They are already larger than the goal needs.

## The plan

Revisions to existing courses:

- **Evals course, new module "Evaluating explanations."** Scoring an
  explanation by held-out activation prediction, controls (random-neuron and
  shuffled-label baselines), and the critique that an explanation without a
  prediction test has not been demonstrated.
- **Statistics course, one new lesson.** Correlation, permutation tests, and
  multiple-comparison control when screening thousands of candidate neurons or
  features.

New courses, in the order the advice ranks them:

| # | Directory | Working title | Readiness test |
|---|---|---|---|
| 1 | `python/python-tut` | Python for Model Internals | Load GPT-2 small, cache activations with hooks, assert every shape, run the eval-pipeline labs green |
| 2 | `linear-algebra/linear-algebra-tut` | Linear Algebra for Interpretability | Project real activations onto a direction and explain what the projection measures; run PCA and SVD on an activation matrix and read the result |
| 3 | `transformers/transformers-tut` | Transformer Anatomy | Implement a GPT-2 forward pass from raw weights, match the reference logits, then re-derive the same activations with TransformerLens or nnsight |
| 4 | `interpretability/interpretability-tut` | Interpretability Methods and Rigor | Replicate a vision-neuron claim on InceptionV1 and a language-neuron claim on GPT-2 small, with the prediction test written before looking |

Courses 1 and 2 can be interleaved. Courses 3 and 4 depend on both. Compute
and toolchain setup is a lab-setup page in course 1, not a separate course.

## Shared conventions for the new courses

These bind every new course and the bridging pages. They are the conventions
the four finished courses already follow, plus what the ML toolchain adds.

**Engine.** Copy the statistics course's engine: `assets/style.css`,
`assets/wiki.js`, the `scripts/build.py` pattern (lessons authored as Python
data, HTML generated), `scripts/check_site.py`, and a glossary and
bibliography. Reading needs no server, build step, network, or JavaScript.
Each course is self-contained in its own directory. Link to sibling courses by
their `index.html` only, with relative paths such as
`../../statistics/statistics-tut/index.html`, so renumbering inside one course
never breaks another.

**Lesson shape.** Each lesson has a concrete implication for eval or
interpretability work, a worked example or mechanism, a pitfall, a judgment
question with a revealable explanation, and practice with an answer. Aim for
12 to 16 lessons of 1,200 to 1,800 words, plus a readiness review with a
rubric. Fewer complete lessons beat more thin ones.

**Terminal output is never invented.** Every command and every line of output
shown was executed, and the transcript is kept under `research/verify/`. The
authoring environment on 2026-10-20 was a virtualenv at `/home/user/.venv-ml`
with Python 3.13 and these versions, which the transcripts record:

| Package | Version | Note |
|---|---|---|
| torch | 2.14.1+cpu | CPU wheel from `download.pytorch.org/whl/cpu` |
| torchvision | 0.29.1+cpu | Must match the CPU torch wheel; a PyPI build fails to import |
| transformers | 5.20.2 | |
| transformer_lens | 4.2.0 | `HookedTransformer` was removed in 4.0. Use `TransformerBridge.boot_transformers("gpt2")` then `enable_compatibility_mode()`; cache keys such as `blocks.5.hook_resid_post` still work |
| nnsight | 0.8.1 | A `trace` block must run from a file or notebook cell, not from stdin |
| numpy | 2.5.4 | (system Python has 2.5.3; transcripts record the venv) |

Models cached and verified: `gpt2` (124M) via transformers, TransformerLens,
and nnsight; InceptionV1 as `torchvision.models.googlenet` with
`GoogLeNet_Weights.IMAGENET1K_V1`. Learner-facing install instructions are
generic (`pip install torch ...`); the transcripts pin what was actually run.

**Provenance.** General explanations (what a dot product is, how attention is
computed) need no citation. Every specific empirical claim about a paper,
model, or result traces to a source note under `research/` that records what
was fetched and checked, as the statistics course's `source-checks.md` does.
If a source cannot be fetched, the claim is omitted or marked unverified.
Never write a number from memory of a paper.

**Spec first.** Labs ship as stubs with tests the learner must make pass, in
the style of `python/python-tut/labs/eval_pipeline.py` and the Elixir course.
Shape assertions are tests. Each course describes held-out variant families
for a tutor to draw from but does not publish them, per `dag-tests/CONTRACT.md`.

**Rigor framing.** Wherever a lesson makes or checks a claim about a model,
the prediction test comes before the look: state what the claim predicts on
data not yet seen, state the control that would also pass if the claim were
empty, then run.

## Status log

- 2026-10-20: statistics module 6 (lessons 24–25) and evals module 8 (pages 27–29) added.
- 2026-10-20: plan written. DAG retired as delivery format. Eval-pipeline
  labs moved. Toolchain verified on CPU. Course authoring begins.
