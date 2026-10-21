# Authoring Interpretability Methods and Rigor

## Audience and outcome

Write for a learner who has done the Python, linear-algebra, transformer-anatomy,
statistics, and evals courses, writes spec-first code for a living, and has not
yet made a claim about a model's internals that survived a test written in
advance. The outcome is that they can: state such a claim as a prediction on
held-out data, fix its score, controls, and threshold before looking, run it on
a CPU, and report it in either direction. Every lesson serves that outcome;
methods are taught as instruments of the protocol, not as a catalogue.

Follow the statistics course's offline wiki conventions: cream reading surfaces,
serif text, searchable sidebar, glossary tooltips, linked lessons, reasoning
checks, source notes, and previous/next navigation. No external assets, fonts,
requests, or packages at read time. Static reading works without JavaScript.

## Page requirements

Every lesson has a concrete implication for interpretability or eval work (the
`evals` box, labelled "In interpretability work"), a worked mechanism or run, a
pitfall, a judgment question with a revealable explanation, and practice with an
answer. Give each h2/h3 an ID. Explain symbols after a formula. Link neighbouring
lessons and the sibling courses by `index.html` only.

Where a lesson shows a run, the output is a verbatim block from
`research/verify/lab-transcript.txt`, inserted with `common.transcript()`, and
the command that produced it appears in a `<pre class="term">` block on the same
page so `scripts/verify_commands.py` re-executes it. A number from a run that is
not in the transcript may not appear in a lesson.

## Rigor discipline

The prediction test comes before the look in every lesson that makes a claim:
state what the claim predicts on data not yet seen, state the control that would
pass if the claim were empty, fix the threshold, then run. Report failures at
the same resolution as passes; the course contains two (the named-unit vision
test and the probe threshold) and they stay. Label post-hoc numbers
"exploratory, not pre-registered" in the script output itself, not only in prose.

Distinguish correlational from interventional evidence in the wording of every
claim. Say which model and which weights were run; the vision model is not the
model the cited papers studied and the lessons must say so wherever a unit
number or a paper result is mentioned.

## Provenance

Every quotation is verbatim from a source fetched on the checking date and
recorded in `scripts/sources.py` and `research/source-checks.md`. Never write a
number from memory of a paper; if the source cannot be fetched, omit the claim
or mark it unverified. The 2026 essay and critique were fetched and are quoted;
their numbers are reported as their authors' estimates.

## Labs

Learner-facing files under `labs/` are stubs with docstrings and tests. The
reference implementations under `labs/reference/` produced the transcript; the
`sol_*.py` modules there have the same API as the stubs so that
`INTERP_LAB_IMPL=reference` runs the public tests against them. Every lab's tests
check a control as well as the claim. Held-out variant families for a tutor are
described in `labs/ASSESSMENTS.md` and not published.

## Changes and checks

Edit the Python authoring sources (`scripts/foundations.py`, `evidence.py`,
`vision.py`, `language.py`, `features.py`, `capstone.py`, `reference_pages.py`,
`glossary.py`, `sources.py`), rebuild, re-verify, and re-check. If a reference
script changes, the transcript changes, and every lesson block that quotes it
must be re-read against the new transcript before the build is committed.
