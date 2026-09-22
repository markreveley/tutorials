# Source checking and provenance

Checked on 2026-09-21 using fetched primary papers, institutional references, and
project-owned documentation. `sources.json` records each URL and the specific
claim scope that was checked. This is not a claim that every statement in each
source was independently validated. External links require Internet access; the
course itself and its labs do not.

## Sources inspected

- Miller, *Adding Error Bars to Evals*, v1 HTML, sections 2–5: sampling units,
  repeated answers, paired differences, clustering, and planning. The course does
  not reproduce its model tables or assume a universal recommended task count.
- NIST/SEMATECH: proportion intervals (Wilson and exact binomial construction),
  mean intervals, paired observations, randomized blocks, and Bonferroni bounds.
- ASA 2016 release containing the six p-value principles: interpretation,
  threshold decisions, effect magnitude, and reporting.
- SciPy method documentation: bootstrap resampling, paired indices, interval
  variants, degeneracy, and binomial testing. The local implementation explicitly
  chooses a percentile bootstrap and does not imply it matches a library default.
- scikit-learn: classification metrics, Cohen's kappa, and calibration; especially
  the distinction between a proper score and calibration alone.
- statsmodels: paired equivalence tests and multiple-test corrections.
- The Book of Statistical Proofs: Beta–Binomial posterior derivation.
- Howard et al.: abstract establishing the time-uniform coverage target of
  confidence sequences. The course does not claim to implement such a method.
- Chen et al., *Evaluating Large Language Models Trained on Code*, v2 HTML,
  section 2.1: the pass@k event and combinatorial estimator.

## Original material

All fictional agents, task counts, confusion matrices, arithmetic examples,
exercises, and datasets are original teaching constructions. They are not
summaries of real provider performance or production measurements. General
mathematical explanations are written independently; sources are cited where a
method or attributed principle is introduced. No long quotations are reproduced.

The two fixture files are constructed, not random samples from a real population.
Their inferential interpretation is explicitly hypothetical. They illustrate how
an analysis changes when its assumptions change; they do not validate interval
coverage. Separate binomial simulation and exact-enumeration checks study the
Wilson procedure under a known iid model. At n=100 and p=0.7 its exact coverage is
about 93.72%, demonstrating why 95% is a nominal approximate level.

## Executable evidence

`verify/lab-transcript.txt` contains actual command outputs, seeds, options, exit
codes, and the Python version. `scripts/verify_commands.py` regenerates that record
by executing published command blocks, plus reference and boundary cases. Quiz
answers are supplied to stdin and disclosed. No terminal output is invented.

`labs/test_stats.py` checks known numerical values, algebraic invariants, exact
binomial enumeration, subset-enumerated reliability, cluster weighting, pairing,
fixture integrity, invalid input, and the quiz. Browser arithmetic has separate
Node checks in `scripts/check_calculators.js`; generated HTML and links have a
structural validator in `scripts/check_site.py`.

The Browser skill was attempted for rendered UI verification, but its runtime
reported no available browsers and an empty browser list. Visual layout and live
browser interactions were therefore not verified in this session. Reuse of the
sibling course's design and runtime does not substitute for that verification.
