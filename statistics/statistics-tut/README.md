# Statistics for Evals

An introductory, evals-first statistics course in the same offline wiki format as
[Understanding LLM Evals](../../evals/evals-tut/index.html),
[Networking for LLM Evals](../../networking/networking-tut/index.html), and
[Linux for Evals Engineers](../../linux/linux-tut/index.html).

Open **[index.html](index.html)** directly in a browser. No server, build step,
account, or external packages are needed to read it. External reference links need
Internet access. Navigation, lesson text, glossary definitions, and answers are
static HTML; JavaScript adds search, glossary tooltips, and calculators.

The starting assumption is comfort with percentages and averages, with no previous
statistics course. The competence target is a **ten-minute result review**: explain
what an eval measures, whether the uncertainty calculation fits its data, and what
decision the evidence supports.

## Included

- **26 lessons across seven modules**, with worked eval examples, reasoning checks,
  revealable explanations, and practice on every page.
- Probability, sampling, confidence intervals, bootstrap, paired comparisons,
  hypothesis tests, power, repeated runs, clusters, slices and weights, missing
  outcomes, grader quality, calibration, Bayesian updates, multiple comparisons,
  stopping rules, reliability, rare failures, cost, latency, experiment design,
  and a closing module on correlation, permutation tests, screening thousands of
  candidate neurons or features, and confirming a winner on held-out data.
- **Four appendices**, **77 glossary terms**, and **24 annotated primary or official
  sources**, with a checked-source record.
- **Three browser calculators**: Wilson intervals with a plot, independent-pair
  sample-size planning, and alternative repeated-success events.
- **Twelve Python lab commands**, including a six-question interactive quiz, plus
  three inspectable synthetic datasets and an analysis-report template.
- An end-to-end lab and final decision memo with a readiness rubric.

The examples compare two fictional agent versions. The second fixture introduces
related repositories, repeated attempts, and a sensitive-task regression. All data
are synthetic; the course makes no claims about real provider performance.

## Terminal practice

From this directory, using Python 3.9 or newer:

```sh
python3 labs/stats_lab.py quiz
python3 labs/stats_lab.py compare
python3 labs/stats_lab.py sample --trials 100 --p 0.7
python3 labs/stats_lab.py compare --data labs/data/clustered_tasks.jsonl --unit cluster
python3 labs/stats_lab.py screen --data labs/data/candidates.jsonl
```

Run `python3 labs/stats_lab.py --help` for the other commands. Labs use only the
Python standard library. They run offline, print results, and save no learner data.
They do not make model calls or require Docker. A fixed seed makes simulations
repeatable; the output states the assumptions and distinguishes task count,
attempt count, and independent resampling units.

The teaching code intentionally supports a narrow analysis: binary outcomes,
equal A/B attempt counts within a task, equal task weighting, task or cluster
percentile bootstrap, and for module 6 Pearson and Spearman correlation with a
label-permutation test, Bonferroni, and Benjamini–Hochberg on a list of p-values. It is not a general production statistics package. Weighted,
missing-data, few-cluster, and more complex designs require appropriate methods.

## Authoring and validation

The checked-in HTML is ready to read. Edit prose in `scripts/foundations.py`,
`inference.py`, `structure.py`, `measurement.py`, `decisions.py`, and `screening.py`; reference pages
in `scripts/reference_pages.py`; terms in `scripts/glossary.py`; source records in
`scripts/sources.py`. The shared CSS and runtime extend the networking tutorial.
See [the authoring guide](research/AUTHORING.md).

Regenerate and check:

```sh
python3 scripts/build.py
python3 scripts/verify_commands.py
python3 scripts/check_site.py
python3 -m unittest discover -s labs -p 'test_*.py' -v
node scripts/check_calculators.js
node --check assets/wiki.js
node --check assets/explorers.js
```

Node is needed only for JavaScript authoring checks, not for reading or Python labs.
The fixture generator, `python3 labs/make_data.py`, is optional; fixtures are already
included. It writes only the three synthetic fixture files.

Validation completed during authoring:

- 33 HTML pages checked for local/sibling links, fragments, asset paths, navigation,
  heading IDs, HTML nesting, glossary references, and required lesson components.
- 21 Python checks passed, covering independent known values, exact enumeration,
  pairing, unequal cluster weighting, fixture regeneration, invalid input, quiz
  interaction, hand-computed correlations, exact permutation enumeration,
  closed-form normal-theory tails, and Benjamini–Hochberg on known p-value lists.
- 43 learner command and boundary invocations executed successfully; actual outputs
  are in [the verification transcript](research/verify/lab-transcript.txt).
- JavaScript arithmetic checks and syntax checks passed.
- Rendered browser verification was attempted but unavailable: the Browser runtime
  reported no connected browsers. Visual layout and live browser interactions have
  not been verified in this session. The module 6 additions (2026-10-20) were
  checked the same way, again without a rendered-browser pass; the one link to
  the forthcoming interpretability course is reported by the checker as a note
  until that course exists.

All new work is local to this course directory. No hosting or publication was done.
