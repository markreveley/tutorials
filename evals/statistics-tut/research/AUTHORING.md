# Authoring Statistics for Evals

## Audience and outcome

Write for a technical learner who knows percentages and averages and wants to do
practical eval work. Explain every new statistical idea in ordinary language,
then demonstrate it on an eval. Derive the rule when a small example can make it
understandable. The target is an inspectable analysis and a defensible decision.

Follow the networking, Linux, and evals siblings' offline wiki conventions:
cream reading surfaces, serif text, searchable sidebar, glossary, linked lessons,
reasoning checks, source notes, and previous/next navigation. Keep the runtime free
of external assets, requests, fonts, and packages. Static reading and navigation
must remain possible without JavaScript.

## Page requirements

Every lesson needs a concrete eval implication, a worked example or mechanism,
a pitfall, a judgment question with a revealable explanation, and practice with
an answer. Add terminal work only where it improves learning. Do not manufacture
commands for inherently conceptual decisions.

Give each h2/h3 an ID. Explain symbols immediately after a formula. State units,
notably proportions versus percentage points. Link neighboring concepts and
relevant sibling pages. The build links first glossary mentions automatically,
excluding headings, code, and existing links.

## Statistical discipline

Name the estimand and independent unit before choosing an interval or test.
Preserve pairing and related groups. Distinguish fixed task sets from new task
populations, attempts from tasks, and simulation draws from collected evidence.
State missing-outcome, weighting, run-policy, and stopping assumptions. Treat
nonsignificance, equivalence, and practical usefulness as distinct claims.

Wilson and percentile bootstrap intervals are approximate. Do not suggest that a
nominal coverage level is achieved exactly for every sample size and distribution.
Do not add a nested bootstrap merely because data have several levels; match the
sampling design and inference target. Rare-event and all-success cases require
special attention because naive resampling can collapse.

## Provenance

All examples and fixtures are original synthetic constructions. Mark any future
real data clearly, with its origin and selection process. Support named methods
and external claims with primary or official sources; record what was checked in
`scripts/sources.py` and `research/source-checks.md`. Do not invent terminal output:
run learner commands using `scripts/verify_commands.py` and retain the transcript.
General explanations need not be paraphrases of sources; keep them original.

## Changes and checks

Edit the Python authoring sources, then regenerate HTML. Keep mathematical
implementations small and auditable. Run the checks listed in README after changes
that affect content, commands, links, or arithmetic. A structural or mathematical
check is not evidence of rendered browser verification; report the distinction.
