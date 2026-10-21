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

## Module 6 additions, checked 2026-10-20

Fetched with the WebFetch tool; each entry records what was read and what was not.

- Benjamini & Hochberg (1995), *Controlling the False Discovery Rate*, JRSS-B
  57(1):289–300, DOI 10.1111/j.2517-6161.1995.tb02031.x. The Wiley page returned
  HTTP 403 and JSTOR returned an error page; a PDF found on a university site was a
  scanned image with no extractable text. Bibliographic data (title, authors,
  journal, volume, issue, pages, year) were verified from the Crossref record for
  the DOI. No sentence from the paper is quoted or paraphrased as the paper's own
  wording; the FDR definition and the step-up rule are taken from the SciPy and
  statsmodels documentation below, which cite the paper.
- SciPy `false_discovery_control`: FDR defined as the expected proportion of
  rejected null hypotheses that are actually true; `bh` for independent tests or
  positive regression dependence, `by` for arbitrary dependence; references to
  Benjamini & Hochberg 1995 and Benjamini & Yekutieli 2001 confirmed.
- SciPy `pearsonr`: the deviation cross-product formula, range −1 to +1, the
  normality assumption behind the default p-value, and the `PermutationMethod`
  option that routes to `permutation_test`.
- SciPy `spearmanr`: a nonparametric measure of monotonicity, range, p-value only
  accurate for very large samples with a permutation test recommended otherwise,
  and the undefined-for-constant-input behavior. The page does not state its tie
  handling; the lab's average-rank convention is documented in `stats.py`.
- SciPy `permutation_test`: the `pairings` type for correlation tests, the
  (count+1)/(resamples+1) convention with the observed statistic included, and
  exact enumeration when the resample count reaches the number of distinct
  permutations. The lab's `permutation_pvalue` follows the same conventions.
- scikit-learn cross-validation guide §3.1: testing on training data is a
  methodological mistake, and tuning against a test set leaks knowledge into the
  evaluation, motivating a held-out validation set.
- OpenAI automated-interpretability repository, `scoring.py`: `correlation_score`
  returns `np.corrcoef(real_activations, predicted_activations)[0, 1]`, and the
  aggregate score computes the correlation over all activations rather than
  averaging per-sequence correlations. The paper page for *Language models can
  explain neurons in language models* rendered only its table of contents, so the
  course makes no claim about the paper's text, its held-out protocol, or results.
- NIST e-Handbook: the scatter-plot and linear-correlation-plot pages were fetched
  but neither defines the correlation coefficient, so the SciPy pages are cited for
  the coefficients instead. The existing NIST Bonferroni citation is reused.

The eight-pair pencil example, the sixty-candidate fixture, and all screening
counts are original. The exact permutation p-values (0.0030 and 0.0046 over 40,320
orderings), the normal-theory comparison (0.0231), and every screening count in
lessons 24–25 were produced by the lab and are recorded in the transcript. The
Pearson value 0.7776 was cross-checked against `numpy.corrcoef` in a separate
environment. The normal-theory tail used only in the simulation was checked
against closed forms at n = 3, 4, and 6 in `labs/test_stats.py`.

## Original material

All fictional agents, task counts, confusion matrices, arithmetic examples,
exercises, and datasets are original teaching constructions. They are not
summaries of real provider performance or production measurements. General
mathematical explanations are written independently; sources are cited where a
method or attributed principle is introduced. No long quotations are reproduced.

The three fixture files are constructed, not random samples from a real population.
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
