# Interpretability Methods and Rigor

The capstone of the evals-and-interpretability path, in the same offline wiki
format as [Statistics for Evals](../../statistics/statistics-tut/index.html) and
[Understanding LLM Evals](../../evals/evals-tut/index.html). It assumes the
[Python](../../python/python-tut/index.html),
[linear algebra](../../linear-algebra/linear-algebra-tut/index.html), and
[transformer anatomy](../../transformers/transformers-tut/index.html) courses.

Open **[index.html](index.html)** directly in a browser. No server, build step,
account, or packages are needed to read it. The labs need a Python environment
with torch (CPU), torchvision, transformers, transformer_lens 4, and numpy, with
GPT-2 small and torchvision's GoogLeNet weights cached.

The competence target: given a claim about what a neuron, direction, head, or
feature does, write the test that would show it on data not yet seen, with the
control that would pass if the claim were empty, run it, and report the result
either way.

## Included

- **16 lessons across six modules**: the protocol (write the prediction test
  before you look), the objects, max-activating examples and quantile sampling,
  held-out explanation scoring, controls with worked numbers, a two-lesson
  vision replication on InceptionV1 (torchvision GoogLeNet) with synthetic
  stimuli and feature visualisation in plain torch, linear probes, the logit
  lens and direct logit attribution, activation patching, induction heads,
  sparse-autoencoder features, writing it up, a capstone, and a readiness
  review with a rubric.
- **Three appendices** (the pre-registration template, a command reference, a
  reading map), **56 glossary terms**, and **15 verified sources** including the
  2026 essay *Neural Networks Are Already Clean* and Leo Gao's reply, both
  fetched and quoted verbatim.
- **Six labs** as stubs with 37 tests, a protocol lab whose `run()` refuses to
  execute until the pre-registration is complete, and reference implementations
  that produced every shown output.
- A **3,270-token original corpus** for the language labs and rendered stimuli
  for the vision labs. No natural images ship with the course.

## What the replications found

All numbers are in [the transcript](research/verify/lab-transcript.txt).

- **Vision.** The Distill *Curve Detectors* unit numbers do not transfer to
  torchvision's GoogLeNet, which is an independent training run; the ten named
  units behaved like random channels on a pre-registered test (20% passing all
  four held-out hypotheses against 23% of random channels). The family-level
  claim replicated: screening all 480 inception3b channels on dark arcs and
  testing the top 12 on held-out stimuli (new radii and thickness, inverted
  contrast, straight lines), 12/12 passed all four hypotheses against 22/100
  random channels, every candidate was silent at the opposite orientation, and
  the preferred orientations covered the circle with no gap above 70°.
- **Language.** For eight token-level rules, exhaustive screening of GPT-2
  small's 36,864 MLP neurons on a screening split found neurons whose held-out
  correlation with the rule was 0.53–0.998, above the 95th percentiles of 200
  random same-layer neurons (0.07–0.23) and 500 label shuffles (about 0.05).
  Activation patching on a France/Italy pair recovered the full logit
  difference from the country position through layer 7 and from the final
  position at layer 11, with a zero control. Eight heads scored at least 0.5
  on the prefix-matching test with 0.00–0.01 on the non-repeated control.
- **A pre-registered test that failed.** The layer-6 probe reached 98.5%
  held-out accuracy but the threshold (majority + 10 points) ignored a 89.7%
  base rate and could not be met; it is reported as a failure with the
  diagnosis.

## Terminal practice

From this directory, with the ML environment's interpreter as `python`:

```sh
python labs/reference/curve_tuning.py
python labs/reference/neuron_score.py --rule digit
python labs/reference/patch_run.py
python -m unittest discover -s labs -p 'test_*.py'
```

The tests fail on the stubs by design. `INTERP_LAB_IMPL=reference` runs them
against the solutions in `labs/reference/sol_*.py`.

## Authoring and validation

Edit prose in `scripts/foundations.py`, `evidence.py`, `vision.py`,
`language.py`, `features.py`, `capstone.py`; appendices in
`scripts/reference_pages.py`; terms in `scripts/glossary.py`; sources in
`scripts/sources.py`. See [the authoring guide](research/AUTHORING.md) and
[the source-checking notes](research/source-checks.md).

```sh
python3 scripts/build.py
python scripts/verify_commands.py      # the ML environment's interpreter
python3 scripts/check_site.py
python -m unittest discover -s labs -p 'test_*.py' -v
node --check assets/wiki.js
```

Validation completed during authoring on 2026-10-20:

- 22 HTML pages checked for local and sibling links, fragments, asset paths,
  navigation, heading IDs, HTML nesting, glossary references, and required
  lesson components; lessons run 1,120–1,876 words.
- 23 published and boundary commands executed by `verify_commands.py` with the
  ML environment's interpreter (Python 3.13, torch 2.14.1+cpu, torchvision
  0.29.1+cpu, transformers 5.20.2, transformer_lens 4.2.0, numpy 2.5.4); every
  output block on a lesson page was cross-checked line by line against the
  transcript.
- 37 lab tests pass against the reference solutions and fail against the
  stubs as intended; `node --check` passes on the runtime script.
- Rendered browser verification was not performed in the authoring session.
