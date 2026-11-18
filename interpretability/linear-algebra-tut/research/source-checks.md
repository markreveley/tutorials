# Source checking and provenance

Checked on 2026-10-20. Pages were fetched with curl and stripped to text locally
(the two transformer-circuits pages are several megabytes of inline images), then
searched for the exact passages quoted. `sources.json` is generated from
`scripts/sources.py` and records each URL and the scope checked.

## Sources inspected

- **Elhage et al. 2021, A Mathematical Framework for Transformer Circuits**
  (transformer-circuits.pub/2021/framework). Quoted: "The residual stream is simply
  the sum of the output of all the previous layers and the original embedding";
  "the residual stream doesn't have a 'privileged basis'; we could rotate it by
  rotating all the matrices interacting with it, without changing model behavior";
  W_O W_V and W_Q^T W_K "can always be thought of as individual, low-rank
  matrices"; "The OV and QK matrices are extremely low-rank. They are 50,000 ×
  50,000 matrices, but only rank d_head (64 or 128)"; the SVD of W_OV with right
  singular vectors describing the subspace "read in" and left singular vectors the
  subspace written to; privileged bases exist for "tokens, attention patterns and
  MLP activations". Author list and date (Dec 22, 2021) confirmed from the page.
- **Elhage et al. 2022, Toy Models of Superposition**
  (transformer-circuits.pub/2022/toy_model). Quoted: toy models "investigate how
  and when models represent more features than they have dimensions. We call this
  phenomenon superposition"; "Superposition simply means that there are more
  features than dimensions"; "Although it's only possible to have n orthogonal
  vectors in an n-dimensional space, it's possible to have exp(n) many 'almost
  orthogonal' (< ε cosine similarity) vectors in high-dimensional spaces" with the
  Johnson–Lindenstrauss lemma cited. Author list and date (Sept 14, 2022) confirmed.
  The course quotes definitions and the geometric fact only; it makes no claim
  about which features GPT-2 holds in superposition.
- **3Blue1Brown, Essence of linear algebra.** The topic page is client-rendered, so
  each of the sixteen lesson pages (3blue1brown.com/lessons/<slug>) was fetched and
  its `<title>` and "Chapter N" marker read. Titles and numbers are recorded in
  `scripts/sources.py` and used in Appendix D.
- **ARENA curriculum** (learn.arena.education, chapters 0 and 1; the GitHub README
  of ARENA_3.0 and arena.education/curriculum for chapter summaries). Section
  numbers and titles as displayed on 2026-10-20: 0.0 Prerequisites, 0.1 Ray
  Tracing, 0.4 Backpropagation; 1.1 Transformers from Scratch, 1.2 Intro to Mech
  Interp, 1.3.1 Linear Probes, 1.3.2 Function Vectors & Model Steering, 1.3.3
  Interpretability with SAEs, 1.4.1 Indirect Object Identification, 1.5.2 Grokking
  & Modular Arithmetic, 1.5.3 OthelloGPT, 1.5.4 Superposition & SAEs. ARENA
  renumbers between iterations; the reading map says so.
- **NumPy reference**: `numpy.linalg.svd` (descending singular values, Vh,
  full_matrices shapes, reconstruction), `numpy.linalg.lstsq` (minimum-norm
  solution, empty residuals condition), `numpy.linalg.eigh` (ascending order,
  one triangle read), `numpy.einsum` (convention and the matrix product, inner
  product and trace examples).

## Original material

All mathematical explanations are original. The passage the fixture was computed on
is original prose written for the course (`labs/make_data.py`). The labels were
computed from token strings. No text from any source is reproduced beyond the short
quotations above.

## Fixture provenance

`labs/data/README.md` documents the fixture. `research/verify/make-data-output.txt`
is the generator's output (model, layer, versions, float16 rounding error).
`research/verify/fixture-crosscheck.txt` compares the saved activations with
TransformerLens 4.2.0 `blocks.6.hook_resid_post` on the same text with
`prepend_bos=False`: the largest difference is 5.45 on an entry of magnitude about
2,937, a relative error of 0.19%. The float16 rounding alone accounts for 0.73 of
that; the rest is implementation differences between the two libraries' forward
passes. Both numbers are reported rather than smoothed over.

## Executable evidence

`research/verify/lab-transcript.txt` holds the actual output of every command shown
in the lessons, plus boundary cases, the unit tests, and the TransformerLens
cross-check, with Python and numpy versions. `scripts/check_outputs.py` confirms
that every output block quoted in a lesson appears verbatim in that transcript.
Browser arithmetic has separate Node checks in `scripts/check_calculators.js`.
Rendered browser verification of the explorers was not performed in this session;
their mathematics is checked, their layout is not.

One authoring error is worth recording: an early draft of lesson 12 quoted a
transcript line that did not exist (a "0.4001" the lab never printed). It was
caught by rereading the transcript before `check_outputs.py` existed; the checker
now makes that class of error fail the build.
