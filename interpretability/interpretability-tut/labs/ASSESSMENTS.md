# Held-out assessment families (for a tutor; not published to learners)

The public labs are `protocol.py`, `explanation_score.py`, `probe.py`,
`patching.py`, `induction.py`, and `curve_detector.py`, each with a public test
file. A learner who makes the public tests pass has implemented the methods. The
families below check that they can run the protocol on something the reference
runs did not cover. Each family describes how to generate variants; concrete
instances are drawn fresh and not written here, per `dag-tests/CONTRACT.md`.

## A. New rule, same corpus
Give a contextual token predicate not among the eight in `gpt2_common.token_rules`
(examples of the kind: "token inside double quotes", "second token after a
newline", "a number followed by a unit word"). The learner must write the
pre-registration before screening, run the screening on even chunks only, score
on odd chunks with both controls, and hand in the report. Pass criteria follow
the lesson 15 rubric; the held-out r is not graded. Variant knobs: the rule, the
threshold justification, which layer range is allowed.

## B. Distribution shift
Supply 1,500-3,000 tokens of text in a different register (a tutor-written
dialogue, a list-heavy document, pseudo-code). The learner screens on the course
corpus and scores on the new text, or the reverse, as the variant specifies, and
must report the base rate on each split and the screening-to-held-out drop.
Pass: the drop is reported and diagnosed, not hidden.

## C. Neuron first
Name a layer and a selection statistic (highest variance, highest kurtosis,
highest fraction above half-max) on the screening split. The learner must form
an explanation from quantile bands only, pre-register, and score. Most variants
will fail the 0.5 threshold; pass is a correctly reported failure with a
diagnosis and a revised, unrun protocol.

## D. Vision stimulus family
Change the held-out stimulus family: new radii, extent, thickness, ink level,
a filled disc, or an angle stimulus. The learner must pre-register H1-H5
analogues with thresholds before rendering, run the screening with the course
stimuli, and report candidate and random-channel pass rates jointly. Variant
knobs: the family, K, the number of control channels. Pass requires the joint
control rate beside the candidate rate.

## E. Patching pair
Give a new clean/corrupted pair (two countries, two professions, two numbers)
or ask for one; the pair must tokenise to equal length. The learner pre-registers
the claim position, the control position, and the two thresholds, runs the
residual-stream table, and reports. A variant may ask for per-head `hook_z`
patching at the layers where the residual patch moves between positions.

## F. Induction threshold and copying
Vary sequence length (20, 50, 100), vocabulary range, and the number of seeds,
and require the copying score (direct logit attribution of each head's output
to the attended token) in addition to prefix matching. Pass: the grid and the
control column are reported for all heads, and the learner's threshold is
stated before the run.

## G. Write-up only
Give a short fictional interpretability write-up with three to five specific
rigor failures (threshold set after the run, control reported as "low", claim
worded causally from a probe, top-k examples as the only evidence, unit named
as a noun phrase). The learner must list the failures using the lesson 13
checklist and rewrite the claim in the correct order.

## Grading note
Every family is graded on the lesson 15 rubric. A pre-registration that was
visibly written after the result (threshold equal to the score, "looked?"
blank) fails regardless of the numbers. A failed pre-registered test reported
in full passes.
