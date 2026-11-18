from common import lesson, lab, cite

LESSONS = [
lesson(14,4,'grader-quality','Evaluate the grader as a measuring instrument',
 'A narrow interval around an unreliable grader’s score can make the wrong conclusion look convincing.',
 '''<h2 id="reference">First define a reference judgment</h2>
<p>A grader maps behavior to a label or score. To measure its quality, compare it with an independently adjudicated reference set under a written rubric. Human labels are measurements too: record disagreements, ambiguous cases, and adjudication rules. Let reference uncertainty remain visible rather than describing every human vote as unquestionable truth.</p>
<p>For this lesson, “positive” means a real failure that should be flagged. Choosing that orientation explicitly prevents confusion: a false negative is a missed failure; a false positive is a false alarm on acceptable behavior.</p>
<h2 id="matrix">Read a confusion matrix</h2>
<p>Consider an original hypothetical audit of 1,000 cases containing twenty reference failures.</p>
<table><tr><th></th><th>Reference failure</th><th>Reference acceptable</th></tr><tr><td>Grader flags failure</td><td>16 true positives</td><td>49 false positives</td></tr><tr><td>Grader passes</td><td>4 false negatives</td><td>931 true negatives</td></tr></table>
<p>Recall is the detected fraction of real failures: <code>16/20 = 80%</code>. Precision is the real-failure fraction of flags: <code>16/65 ≈ 24.6%</code>. Specificity is the correctly passed fraction of acceptable cases: <code>931/980 = 95%</code>. Accuracy is all correct labels divided by all cases: <code>947/1000 = 94.7%</code>. These definitions agree with the standard confusion-matrix metrics. '''+cite('metrics')+'''</p>
<p>An always-pass grader achieves 98% accuracy here while detecting no failures. Accuracy rewards the common class heavily. You need the error types relevant to the decision, not a single unlabeled headline number.</p>
<h2 id="base-rate">Why precision changes with prevalence</h2>
<p>Prevalence is the fraction of real failures in the population. Suppose the same 80% sensitivity and 95% specificity held in a population with 10% failures. Per 1,000 cases, you would expect 80 true flags and 45 false flags, so precision would be 80/125 = 64%. The grader’s conditional behavior is unchanged, but the mix of cases makes its flags more informative.</p>
<p>A failure-enriched grader audit is useful for estimating sensitivity. Its raw flag precision does not automatically estimate precision on ordinary traffic. To transport it, you need an appropriate prevalence and assumptions about conditional performance across populations. Oversampling rare failures is a sampling-design choice, not a reason to confuse the two populations.</p>
<h2 id="agreement">Agreement is another question</h2>
<p>When neither of two raters is a designated reference, report agreement rather than calling one “accurate.” Cohen’s kappa adjusts observed agreement pₒ by a chance-agreement quantity pₑ computed from the raters’ marginal label frequencies: <code>κ = (pₒ−pₑ)/(1−pₑ)</code>. It is a descriptive agreement measure under that chance model, not proof of validity. It can be unstable or undefined with degenerate margins. ''' + cite('agreement') + '''</p>
<p>Two graders can agree because they share the same blind spot. Inspect disagreements and shared mistakes against the rubric. For ordinal ratings, weighting disagreements requires an explicit distance choice; for multiple raters or missing labels, choose an agreement method matching that design.</p>
<h2 id="comparison">Check whether errors favor a version</h2>
<p>Aggregate grader quality can hide differential error. If the candidate uses more confident language and the grader rewards that style, B may receive more false passes. Blind model identities where feasible, vary response order in pairwise judgment, and audit each version and important slice. Validation data used to tune the grader should be separated from its final audit.</p>
<div class="evals"><span class="label">In eval work</span><p>Report raw counts with recall and precision: 16/20 detected failures carries much less information than the 1,000-case headline suggests about failure recall. Uncertainty for each metric must reflect its effective denominator and the reference sampling design.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Assuming a grader that is 95% accurate must preserve a two-point model difference. Which cases it mislabels and whether mistakes differ by version can matter more than its aggregate accuracy.</p></div>''',
 'Two judges agree on 97% of outputs. Can you conclude either is 97% accurate?',
 'No. Agreement has no truth reference by itself. They may share a systematic mistake or mostly see an easy majority class. Audit against a rubric-backed reference set, examine rare errors, and preserve human disagreement.',
 lab([], 'Recalculate all four metrics in the table. Then imagine an always-pass grader. State which error type matters if flags trigger human review versus automatic rejection.',
 'The always-pass grader has zero failure recall. Human-review capacity makes false alarms important; automatic rejection can impose additional costs on acceptable work. Both uses still require attention to missed important failures. Undefined precision when nothing is flagged should be labeled undefined, not silently invented.'), ['metrics','calibration','agreement']),

lesson(15,4,'calibration','When a model says “80% confident”',
 'Distinguish predicting a label from predicting a useful probability of that label.',
 '''<h2 id="calibration">Does the number match its frequency?</h2>
<p>A probability forecast is calibrated on a population if events assigned a given probability occur at about that frequency. Among many comparable cases assigned 0.8 success probability, roughly 80% should succeed. This is a property across cases under stated conditions, not a guarantee about an individual case. '''+cite('calibration')+'''</p>
<p>A model’s confident tone is not a probability forecast. If you ask it for a numerical confidence, define the event and collect the forecast before showing the outcome. A confidence about “the answer seems plausible” is not necessarily a probability of passing your rubric.</p>
<h2 id="diagram">Build a reliability diagram</h2>
<p>Group forecasts into prespecified probability bins. For each bin, compare the average forecast with the observed fraction of successes. Display the count, too: a bin with three outcomes cannot support the same precision as one with three thousand.</p>
<table><tr><th>Bin</th><th>Count</th><th>Mean forecast</th><th>Observed success</th></tr><tr><td>0.6–0.8</td><td>100</td><td>0.70</td><td>0.55</td></tr><tr><td>0.8–1.0</td><td>100</td><td>0.90</td><td>0.72</td></tr></table>
<p>This constructed example suggests overconfidence in both bins: forecasts exceed observed success. It does not establish what happens in unsampled bins or populations. Bin boundaries, sparse bins, and averaging can hide local patterns. A summary calibration error that changes when you change bins is not a complete assessment.</p>
<h2 id="scoring">Score probabilities directly</h2>
<div class="math">Brier score = average of (forecast probability − binary outcome)²</div>
<p>For each case, square the forecast’s distance from zero or one, then average; lower is better. With eight successes and two failures, a constant forecast of 0.9 gives <code>(8 × 0.1² + 2 × 0.9²)/10 = 0.17</code>. A constant 0.8 forecast gives 0.16 for those same outcomes.</p>
<p>Log loss instead scores <code>−[y log(p) + (1−y) log(1−p)]</code>. Correct confident predictions get small losses; confidently wrong predictions get large losses. A probability of zero for an event that occurs gives infinite loss mathematically. If software clips probabilities for numerical reasons, document the clipping convention.</p>
<p>These are proper scoring rules: under the scoring setup, the expected score is optimized by an honest probability forecast. A proper score captures more than calibration; discrimination and inherent outcome uncertainty also contribute. A lower Brier score therefore need not mean calibration alone improved. '''+cite('calibration')+'''</p>
<h2 id="use">Calibration and useful decisions</h2>
<p>A constant forecast equal to the population success rate can be calibrated while failing to distinguish easy from hard cases. To route uncertain work to humans, you need both useful discrimination and reliable probabilities in the region where the decision threshold lies.</p>
<p>Evaluate the actual abstention policy: coverage is the fraction handled automatically, and selective error is the error fraction among those handled. A system can make its accepted subset look better by handling almost nothing. Show both quantities, along with performance on critical slices.</p>
<p>If you fit a calibration transformation, fit it on development data and assess it on independent held-out data. Selecting the transformation and reporting performance on the same observations can be optimistic. Population shift can also change calibration after deployment.</p>
<div class="evals"><span class="label">In eval work</span><p>Keep forecast probabilities with task IDs and outcomes. For a model comparison, analyze paired loss differences and preserve the same grouping structure you used for success-rate comparisons.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Equating verbal certainty, classification accuracy, calibration, and discrimination. They measure different aspects of behavior and can move independently.</p></div>''',
 'A forecaster always says 70%, and exactly 70% of cases succeed. Is it useful for deciding which cases need review?',
 'It may be calibrated in aggregate, but it cannot rank cases because it gives every case the same forecast. Review routing needs information that separates higher- and lower-risk cases, assessed with coverage and selective error on appropriate data.',
 lab([], 'For a task that fails, calculate Brier loss for forecasts 0.6, 0.8, and 0.99. Then repeat for a task that succeeds. Explain what confidently wrong forecasts cost.',
 'On failure the losses are 0.36, 0.64, and 0.9801. On success they are 0.16, 0.04, and 0.0001. A proper scoring rule rewards useful confidence while penalizing unsupported certainty across repeated cases.'), ['calibration','metrics']),

lesson(16,4,'bayesian-updating','A Bayesian view of uncertainty',
 'Update an explicit prior with observed outcomes, and learn which assumptions a posterior probability still depends on.',
 '''<h2 id="question">A different kind of probability statement</h2>
<p>Frequentist confidence intervals describe repeated procedures with a fixed target. A Bayesian analysis represents uncertainty about a parameter with a probability distribution. After observing data, the posterior combines a prior distribution with a likelihood describing how the data arise.</p>
<div class="diagram">Prior uncertainty × likelihood of observed data
                  ↓ normalize
             Posterior uncertainty</div>
<p>This framework lets you ask “under this model and prior, what is the probability that the pass rate exceeds 0.8?” The conditions in that sentence are essential. A posterior is not an assumption-free probability of real-world success.</p>
<h2 id="beta">The Beta–Binomial example</h2>
<p>Let p be one stable Bernoulli success probability. A Beta distribution has two positive shape parameters, α and β, and lives between zero and one. A Beta(1,1) prior has uniform density on that interval. It is one possible weak prior for this parameterization, not a uniquely neutral choice.</p>
<p>With s successes in n independent trials, the posterior is:</p>
<div class="math">p | data ∼ Beta(α + s, β + n − s)</div>
<p>Add successes to the first prior shape and failures to the second. This follows by multiplying the Beta prior density by the binomial likelihood and collecting powers of p and 1−p. '''+cite('beta')+''' The posterior mean is <code>(α+s)/(α+β+n)</code>, which blends the prior mean with the observed rate.</p>
<p>For eight successes in ten trials, Beta(1,1) becomes Beta(9,3), with mean 0.75. A Beta(8,2) prior becomes Beta(16,4), with mean 0.8. Neither calculation changes the observations; the assumptions about uncertainty before seeing them changed.</p>
<h2 id="credible">Read a credible interval</h2>
<p>A 95% credible interval contains 95% of posterior probability under the model and prior. An equal-tail interval leaves 2.5% in each tail. It can differ from a frequentist interval in both interpretation and endpoints. Do not silently switch between them when reporting results.</p>
<p>The lab draws from the posterior using Python’s Beta sampler. The posterior mean is calculated exactly by the formula above; reported credible endpoints and threshold probabilities are Monte Carlo approximations. More posterior draws reduce simulation error, not uncertainty from having only ten observed trials.</p>
<h2 id="sensitivity">Vary the prior, inspect the model</h2>
<p>Try a weak prior, a more concentrated optimistic prior, and a skeptical prior. If the decision changes substantially, report that sensitivity. As appropriate data accumulate, prior influence often decreases, but even abundant data cannot repair a likelihood that ignores dependence or a systematically biased task sample.</p>
<p>This one-parameter model treats observations as iid Bernoulli draws with one marginal p. Repeated attempts on heterogeneous fixed tasks need more structure. For paired A/B data, independently drawing two posterior rates can discard the dependence that pairing captures. A Bayesian approach must preserve the experimental structure just as a bootstrap must.</p>
<div class="evals"><span class="label">In eval work</span><p>Posterior threshold probabilities can support a decision when paired with explicit utilities and a defensible model. Include the prior, likelihood, sampling assumptions, and sensitivity analysis in the report.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Choosing a prior after looking at results so the posterior clears a launch threshold. That reuses the data as unstated evidence and undermines the interpretation you are presenting.</p></div>''',
 'The lab reports a high posterior probability that p exceeds your threshold. Does that validate the grader or task selection?',
 'No. It is conditional on the supplied observations, likelihood, and prior. A biased grader or unrepresentative sample can produce a concentrated posterior for the wrong target. Validate the measuring process separately.',
 lab(['python3 labs/stats_lab.py bayes 8 10 --alpha 1 --beta 1 --threshold 0.8','python3 labs/stats_lab.py bayes 8 10 --alpha 8 --beta 2 --threshold 0.8','python3 labs/stats_lab.py bayes 8 10 --alpha 2 --beta 8 --threshold 0.8'],
 'Predict which prior gives the highest posterior mean. Compare threshold probabilities and intervals, then repeat each with 80 successes in 100 trials.',
 'The optimistic prior pushes the small-sample posterior upward; the skeptical prior pulls it downward. With more data at the same observed rate, the prior has less influence. The counts must still satisfy the likelihood’s independence assumptions.'), ['beta','wilson']),
]
