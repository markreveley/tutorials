# Tutorials: a path from software engineering to evals and interpretability

This repository is a self-authored curriculum with one objective: a career in
AI evaluation and mechanistic interpretability, starting from a software
background (the earlier work in this repository is in Elixir and Rust) and no
machine-learning background.

Every course here is an offline wiki: open its `index.html` in a browser. No
server, build step, account, or network is needed to read. Each lesson has a
worked example, a pitfall, a judgment question with a revealable answer, and
practice. Labs are stubs with tests that the learner makes pass. Every
terminal output shown was actually executed and its transcript is kept under
each course's `research/verify/`. Every empirical claim traces to a fetched
source note under `research/`. [ROADMAP.md](ROADMAP.md) records the plan,
the decisions behind it, and the pinned toolchain.

## The objective, and what gets in the way

The advice this curriculum follows names five barriers, ranked by how much
they slow the objective down:

| # | Barrier | Covered by |
|---|---|---|
| 1 | Python and PyTorch: the whole toolchain is Python; shapes take months | Python for Model Internals |
| 2 | Linear algebra at a working level: projections, PCA, SVD, no proofs | Linear Algebra for Interpretability |
| 3 | Transformer anatomy: residual stream, heads, MLPs, gating, tokens | Transformer Anatomy |
| 4 | Compute: small models on a laptop or CPU are enough for native-neuron work | Lab-setup lessons in every ML course; nothing needs a GPU |
| 5 | Experimental rigor: an explanation that cannot predict held-out activations is not demonstrated | Statistics for Evals, the evals course's module 8, and Interpretability Methods and Rigor |

## The tracks and what each enables

### Evals track

**Understanding LLM Evals** (`evals/evals-tut`, 30 pages). Enables you to
turn a vague complaint into a measurable failure mode, build code, human,
and LLM-judge graders and validate the graders themselves, read any
benchmark's scoring harness and predict how its number can mislead, and
recognise contamination, judge bias, and leaderboard distortion. Its final
module, Evaluating explanations, carries that discipline over to claims
about a model's internals: scoring an explanation on held-out data, the
controls that would also pass if the claim were empty, and the standard a
write-up must meet before it says a neuron has been explained.

**Statistics for Evals** (`statistics/statistics-tut`, 26 lessons). Enables
the ten-minute result review: given an eval report, say what it measures,
whether the uncertainty calculation fits the data, and what decision the
evidence supports. Covers intervals, bootstrap, paired comparisons, clustered
data, missing outcomes, grader quality, multiple comparisons, and stopping
rules. Its final module teaches correlation, permutation tests, and
false-discovery control when screening thousands of candidate neurons, which
is the statistics interpretability actually uses.

**Linux for Evals Engineers** (`linux/linux-tut`, 29 lessons). Enables the
ten-minute audit: dropped onto an unfamiliar box as root, say what is
running, what is mounted and whether it is read-only, who owns what, what
the box can reach, and where the logs are, and why each answer matters for
whether a score can be trusted. Built for agentic evals, where the thing
under test acts inside a Linux sandbox.

**Networking for LLM Evals** (`networking/networking-tut`, 24 lessons).
Enables you to follow one eval request from a worker to a model and back,
make runs reliable under latency, rate limits, timeouts, and retries,
diagnose infrastructure failures with evidence, and design and defend an
eval architecture with its trust boundaries.

### Interpretability track

**Python for Model Internals** (`python/python-tut`, 17 lessons). Enables
you to read and write everyday Python without translating from Elixir or
Rust, write the test first with unittest, predict the shape of any array
expression before running it, use torch tensors and autograd correctly, load
GPT-2 small, capture activations with forward hooks, TransformerLens 4, and
nnsight, and save artifacts another person can check. Readiness test: cache
the residual stream for a set of prompts with every shape asserted, and have
the eval-pipeline labs green.

**Linear Algebra for Interpretability** (`linear-algebra/linear-algebra-tut`,
16 lessons). Enables the central interpretability move: project activations
onto a direction and say what the scalar per token measures. Also linear
maps as shapes, why a direction need not be a neuron, removing a direction,
fitting a direction to labels and checking it on held-out tokens, PCA and
SVD on real activation matrices, gradients as directions, and testing whether
a correlation is real. Every lesson computes on a real GPT-2 activation
fixture.

**Transformer Anatomy** (`transformers/transformers-tut`, 16 lessons).
Enables you to trace one residual-stream vector from embedding to logits and
name every write to it, compute an attention head by hand and describe a real
one as QK and OV circuits, locate a neuron in an MLP, compute GELU and SwiGLU
and say which models use which, and find the same activation under its
Hugging Face, TransformerLens, and nnsight names. Readiness test: implement
a GPT-2 forward pass from raw weights that matches the reference logits.

**Interpretability Methods and Rigor** (`interpretability/interpretability-tut`,
16 lessons). Enables the skill the advice calls the one that separates a
blog post from a contribution: given a claim about a neuron, direction, head,
or feature, write the test that would show it on data not yet seen, with the
control that would pass if the claim were empty, then run it and report the
result either way. Covers why max-activating examples mislead, explanation
scoring, probes, the logit lens, activation patching, induction heads, and
sparse-autoencoder features, with a vision replication on InceptionV1 and
language replications on GPT-2 small, all on a CPU. Two of its own results
failed or did not transfer, and the course teaches them as written.

### Off the path, kept

**Elixir** (`elixir/`) and the **BEAM memory model** (`beam/`) predate the
objective. They are complete and are the origin of the spec-first,
proof-minded habits the rest of the curriculum relies on, but they are not
part of the recommended order. The parked Python and Rust LeetCode courses and
the Rust reading assessments live under `dag-tests/previous-courses-to-re-author/`;
`dag-tests/` itself is now the test-first assessment layer for the Python labs.

## Recommended order

Each course can be read alone, but the dependencies are real, and the two
tracks are meant to be interleaved rather than finished one after the other.

1. **Understanding LLM Evals**, modules 0 to 7. The conceptual base for
   everything else, and no code required.
2. **Python for Model Internals** and **Statistics for Evals** together.
   Python is barrier 1 and has no prerequisite. The statistics course's labs
   are standard-library Python, so they double as Python practice. Do the
   three eval-pipeline labs early; they are the first assessed work.
3. **Linear Algebra for Interpretability**, interleaved with the second half
   of the Python course. Lesson 14 sends you back to the statistics course's
   module 6 (correlation and screening) when you reach it.
4. **Transformer Anatomy**, once you can predict tensor shapes and project
   onto a direction. Its capstone is the from-raw-weights forward pass.
5. **Evals module 8, Evaluating explanations**, immediately before the
   interpretability course. It states the standard the capstone must meet.
6. **Interpretability Methods and Rigor**, last. It assumes all of the above
   and ends with a pre-registered neuron study you run yourself.
7. **Linux** and **Networking** whenever eval-infrastructure work demands
   them. They are self-contained and do not block the interpretability track.
   For agentic-eval roles, read Linux before applying.

Each course ends in a readiness review with a rubric. Treat passing the
public lab tests as practice, not proof: the assessment briefs describe
held-out variant families a tutor can draw from, and fluency is claimed only
after an unseen variant.

## Toolchain

The evals, statistics, linux, and networking courses need only Python 3.9+
and the standard library for their labs. The four interpretability-track
courses need a CPU-only PyTorch environment; each course's lab-setup lesson
gives the install, and ROADMAP.md pins the versions every transcript was
produced with. GPT-2 small and InceptionV1 are the only models used, and both
run on a laptop.
