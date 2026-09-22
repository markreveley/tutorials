from common import lesson, lab, cite

LESSONS = [
lesson(6,1,'confidence-intervals','Confidence intervals and what they cover',
 'An error bar is a statement about a procedure under assumptions, not a guarantee that the benchmark measured the right thing.',
 '''<h2 id="repetition">Imagine repeating the procedure</h2>
<p>You observe 72 passes in 100 independent sampled task-and-attempt pairs. The estimate is 72%. A confidence interval adds a range constructed by a stated method. A nominal 95% method aims to contain the fixed target in approximately 95% of repeated experiments under its assumptions. Some methods are exact or conservative; approximate methods can miss that nominal rate.</p>
<p>After you observe the data, the interval’s endpoints are fixed. In this frequentist interpretation, “there is a 95% probability the parameter is inside this realized interval” is not the definition. You can still use the interval to express the precision of the procedure and the values reasonably compatible with the data and model. '''+cite('mean')+'''</p>
<h2 id="wilson">A useful interval for binary outcomes</h2>
<p>A common shortcut is <code>p̂ ± 1.96 × √(p̂(1−p̂)/n)</code>. It treats the estimated rate as approximately normal with a plug-in standard error. Near zero or one, or with small counts, it behaves badly. Ten passes out of ten gives an estimated SE of zero and the interval [100%, 100%], which expresses certainty the data do not warrant.</p>
<p>The Wilson interval comes from a different construction: invert a score test rather than attaching a symmetric margin to the observed rate. Its endpoints stay between zero and one. The <a href="../appendices/a-math.html#wilson">math reference</a> gives the full formula and definitions. '''+cite('wilson')+'''</p>
<table><tr><th>Observed outcomes</th><th>Observed rate</th><th>95% Wilson interval</th></tr><tr><td>72 / 100</td><td>72.0%</td><td>62.5% to 79.9%</td></tr><tr><td>10 / 10</td><td>100.0%</td><td>72.2% to 100.0%</td></tr></table>
<p>These numbers are calculated by the included lab. Ten successes leave considerable uncertainty about the underlying success probability. Wilson intervals are approximate binomial intervals, not universal solutions for clusters or graded scores.</p>
<h2 id="different-bars">Identify the interval’s object</h2>
<p>An interval for the mean success rate differs from a prediction interval for a future measurement. The first concerns an unknown average. The second must also accommodate variation in the future observation itself. A narrow estimate of average latency does not mean every future task will finish near that average.</p>
<p>A 95% interval is also not the central 95% of your raw task scores. With binary outcomes, the latter will often span 0 and 1 regardless of how precisely the mean is known. Ask which distribution each interval summarizes.</p>
<h2 id="limits">What is outside the error bar?</h2>
<p>At n = 100 and p = 0.7, enumerating every possible binomial outcome gives this Wilson procedure about 93.72% actual coverage. The nominal 95% label is an approximation, and finite discrete samples need not achieve it exactly.</p><p>A task-sampling interval does not generally include grader mistakes, omitted languages, changing model versions, hidden retries, or future workload shift. Those require better measurement, additional data, or explicit modeling. Listing these limitations is part of interpreting the result, not a reason to abandon uncertainty estimates.</p>
<div class="evals"><span class="label">In eval work</span><p>Report the numerator and denominator, estimate, interval method, confidence level, sampling unit, and intended population. “72/100; 95% Wilson interval 62.5–79.9%, assuming independent sampled cases” is substantially more useful than “72% ± error.”</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>An interval that excludes zero does not prove the model is useful, and an interval that includes zero does not prove no effect exists. Both the effect size and what you would act on matter.</p></div>''',
 'A team reports 100% success on ten cases and says its confidence interval has zero width. What likely happened?',
 'It may have used a plug-in normal standard error, which collapses when the observed rate is one. Use an appropriate binomial interval if the iid model applies, and inspect task selection and dependence. Perfect observed performance does not establish perfect future performance.',
 lab(['python3 labs/stats_lab.py rate 72 100','python3 labs/stats_lab.py rate 10 10','python3 labs/stats_lab.py sample --p 0.7 --trials 100'],
 'Calculate two intervals, then observe their coverage over simulated experiments. Explain what the coverage percentage counts.',
 'Coverage counts experiments whose calculated interval contains the simulator’s known p. It does not count the fraction of raw outcomes inside the interval. You can also vary counts in the <a href="../appendices/b-explorers.html">interactive calculators</a>.'), ['wilson','mean']),

lesson(7,1,'bootstrap','Bootstrap: repeat the analysis on resampled data',
 'Use resampling to understand uncertainty while preserving the relationships your experiment created.',
 '''<h2 id="recipe">An empirical stand-in for the population</h2>
<p>A bootstrap approximates sampling variation using the observed sample as a stand-in for the unknown distribution. Draw observations with replacement, recalculate the statistic, and repeat. “With replacement” means a sampled observation is eligible to be selected again. A resample can contain one original observation several times and omit another.</p>
<div class="diagram">Observed independent units: [A, B, C, D]
Example resample:           [B, B, D, A]
Next resample:              [C, A, C, D]
For each resample: calculate the same statistic again</div>
<p>A percentile interval takes the 2.5th and 97.5th percentiles of the bootstrap estimates for a nominal 95% interval. It is simple to inspect, which is why the teaching lab uses it. Other constructions, such as basic and BCa intervals, have different behavior; none removes the need to match the sampling design. '''+cite('bootstrap')+'''</p>
<h2 id="unit">Choose what gets resampled</h2>
<p>If A and B answered the same tasks, one independent unit contains both versions’ scores. Resample the pair together and recompute B−A. If tasks share a source repository, a unit may need to contain every task and both versions from that repository. The shape of the unit reflects what could have been independently sampled.</p>
<p>For a task-weighted average with unequal cluster sizes, resample clusters and recompute the total and task count for every draw. Averaging cluster means equally would target a different weighting. Our implementation concatenates the selected groups’ task differences before averaging, preserving this distinction.</p>
<h2 id="what-varies">Two types of randomness</h2>
<p>The bootstrap resample count controls Monte Carlo error: how accurately the simulation approximates its own bootstrap distribution. The number of observed independent units controls how much evaluation evidence you have. Raising resamples from 4,000 to 40,000 does not turn 200 real tasks into 2,000 tasks.</p>
<p>A fixed random seed makes the computational experiment reproducible. It is not a statistical guarantee. With different seeds, endpoints can differ slightly. If they change enough to reverse a borderline decision, increase resamples and assess whether the underlying data support such a precise decision at all.</p>
<h2 id="failure">When a bootstrap cannot help</h2>
<p>If every observed outcome is one, every ordinary resample is also all ones. The percentile interval collapses. Resampling cannot invent an unobserved failure or recover a missing task category. Sparse tails, very few independent groups, extreme quantiles, and biased samples need particular care.</p>
<p>Resampling all rows independently when they share repositories underestimates uncertainty from repository selection. Nesting another arbitrary bootstrap inside the first is not an automatic repair: the stages must match the actual sampling design. In our task-population analysis, observed task means are the units; we do not add a second within-task resampling step.</p>
<div class="evals"><span class="label">In eval work</span><p>Ask an analyst to describe one bootstrap draw in ordinary words. “Select repositories with replacement and keep each selected repository’s task pairs together” is assessable. “The library handles uncertainty” is not enough to review.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Calling a percentile interval “distribution free” as if it has no assumptions. Its usefulness still depends on the sample, independent units, statistic, and approximation quality.</p></div>''',
 'Your bootstrap uses 50,000 resamples but only six independent repositories. What did the larger resample count fix?',
 'It reduced Monte Carlo noise in approximating the bootstrap distribution. It did not supply additional repositories or guarantee accurate coverage with six groups. More independently sampled repositories may be the more valuable next measurement.',
 lab(['python3 labs/stats_lab.py compare --resamples 4000 --seed 7','python3 labs/stats_lab.py compare --resamples 4000 --seed 19'],
 'Run the same paired analysis with two seeds. Identify which values must stay fixed and which can change. Read <code>labs/stats.py</code> to inspect a resample.',
 'Task counts and observed A, B, and B−A estimates stay fixed. Bootstrap interval endpoints can move because the simulated resamples change. This is computational randomness, not a new agent run.'), ['bootstrap','miller']),

lesson(8,2,'paired-comparisons','Compare models by keeping the pairs',
 'The uncertainty you need is uncertainty in the change, measured on the tasks the two systems share.',
 '''<h2 id="difference">Start with one difference per task</h2>
<p>Suppose both versions answer the same task. Let its difference be B’s score minus A’s score. A binary task difference is +1 when only B passes, −1 when only A passes, and 0 when they agree. Average these differences to estimate the average change.</p>
<p>NIST’s paired analysis operates on within-pair differences. In evals, retaining task identity often makes this the natural comparison. '''+cite('paired')+''' Pairing does not require identical sampled text or matching random seeds: it requires a meaningful shared task or matched unit. Reset the environment so the first version’s work cannot help the second.</p>
<h2 id="table">Read the running dataset</h2>
<table><tr><th>Outcome on a task</th><th>Count</th><th>Contribution to B−A</th></tr><tr><td>Both pass</td><td>120</td><td>0</td></tr><tr><td>A only passes</td><td>24</td><td>−24</td></tr><tr><td>B only passes</td><td>36</td><td>+36</td></tr><tr><td>Neither passes</td><td>20</td><td>0</td></tr></table>
<div class="math">Average difference = (36 − 24) / 200 = 0.06</div>
<p>B gains twelve net successful tasks out of 200: six percentage points. That is also 78% minus 72%. The paired table preserves how the versions disagree; two headline rates alone do not.</p>
<p>Consider another table with the same margins: 140 both pass, four A-only passes, sixteen B-only passes, and forty neither. The observed difference is still six points, but it arises from twenty discordant pairs rather than sixty. The variation of the differences is different. Identical marginal scores can therefore support different uncertainty statements.</p>
<h2 id="why">Why pairing often helps</h2>
<div class="math">Var(B − A) = Var(B) + Var(A) − 2 Cov(A, B)</div>
<p>The variation of a difference includes how the two scores move together, measured by covariance. If shared task difficulty makes both versions tend to pass and fail together, covariance is positive and pairing can improve precision. That benefit is not unconditional: negative covariance would increase difference variance. Preserve the actual pairing rather than assuming a particular correlation.</p>
<h2 id="result">Read an interval for the change</h2>
<p>For the running fixture, the lab’s seeded percentile bootstrap gives approximately −1.5 to +13.5 percentage points. The observed result favors B, but the interval spans modest harm and substantial benefit. The exact discordance test gives a two-sided p-value near 0.155 under its null model. The next lesson explains what that means.</p>
<p>You should report the change and interval directly. Overlap between separate model intervals is not a reliable substitute for an interval on the paired difference. It discards the covariance that defines the comparison.</p>
<div class="evals"><span class="label">In eval work</span><p>Join result files by stable task IDs, verify uniqueness, and audit missing counterparts. Pairing rows by their position after one version has dropped failures can silently compare different tasks.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Dropping every task either version failed to complete can select easier cases and change the target. Decide and document the handling of missing counterparts before running the comparison.</p></div>''',
 'Both versions scored 75%, but they fail different cases. Has the candidate changed nothing?',
 'The net observed mean change is zero, but behavior may have changed substantially. Inspect discordant cases and slices. A launch decision can depend on which failures appeared, not only their net count.',
 lab(['python3 labs/stats_lab.py compare'],
 'Predict A’s passes and B’s passes from the four-cell table. Run the command, then explain the estimate, interval, and discordant counts to a teammate in three sentences.',
 'A passes 144/200 and B 156/200. B’s observed advantage is six points; the interval remains compatible with some loss. The 36 improvements and 24 regressions are a concrete queue for error analysis.'), ['paired','miller','binomial']),

lesson(9,2,'hypothesis-tests','Tests, p-values, and practical decisions',
 'Learn what a test actually asks, then separate statistical evidence from the size of change you care about.',
 '''<h2 id="null">A test needs a specified null</h2>
<p>A null hypothesis is a statistical claim you assess against observations. For the paired binary comparison, a useful null says the two types of discordance are equally likely. Conditional on a task being discordant, B wins with probability one half. Independent discordant pairs then give a binomial count.</p>
<p>In our example, B wins 36 of 60 discordant pairs. A two-sided exact McNemar test computes how unusual an imbalance at least this large would be under the symmetric null. It can be calculated as twice the fair-binomial probability of 24 or fewer wins, capped at one. This is the binomial test specialized to a fair null. '''+cite('binomial')+'''</p>
<h2 id="meaning">Read the direction of the probability</h2>
<p>A p-value is a probability of a statistic at least as extreme as the observed one, under the specified null and assumptions. A value of 0.155 does not mean there is a 15.5% chance the versions are equal or an 84.5% chance B is better. It is a statement about possible data under a model, not a posterior probability of that model.</p>
<p>The ASA’s guidance explicitly distinguishes p-values from hypothesis probabilities and effect importance. '''+cite('asa')+''' A small p-value can motivate scrutiny of the null model, but it does not identify which assumption failed. A grader change, selection difference, or confounded run order can also produce a difference.</p>
<h2 id="errors">The two decision errors</h2>
<p>A Type I error rejects a true null. A test’s alpha, often chosen as 0.05, is a planned upper error rate under its assumptions, not a universal definition of scientific truth. A Type II error fails to reject when a specified alternative is true. Power is one minus that second error probability.</p>
<p>Power depends on the particular alternative. A design can reliably detect a twenty-point change while usually missing a two-point change. A failure to reject zero can therefore reflect limited information, rather than equality. Say “inconclusive for this effect” when that is what the data support.</p>
<h2 id="margins">Compare with practical margins</h2>
<p>Suppose switching costs make gains below three points uninteresting. An interval from +0.2 to +1.0 points may provide strong evidence of a positive effect while remaining too small to motivate the switch. Conversely, an interval from −2 to +12 leaves a worthwhile gain plausible but unresolved.</p>
<p>For noninferiority, define an acceptable loss margin m before observing data. With B−A, you seek evidence that the difference is above −m, using a predeclared one-sided analysis. For equivalence, you seek evidence the difference lies within both margins. A common two-one-sided-test procedure at alpha 0.05 checks containment of a 90% two-sided interval in those bounds under the matching model. Merely including zero in an ordinary 95% interval proves neither claim. ''' + cite('equivalence') + '''</p>
<div class="evals"><span class="label">In eval work</span><p>Put three things in the decision discussion: observed effect, uncertainty range, and the practical threshold. If they point in different directions, state the unresolved tradeoff rather than hiding it behind a significance label.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Changing a two-sided test to one-sided after seeing the direction of the result changes the error properties. Set the direction and decision rule in advance.</p></div>''',
 'A candidate has an interval of −4 to +4 points. Your equivalence margin is ±1 point. Can you declare equivalence because zero is inside?',
 'No. The interval allows changes much larger than the equivalence margins. You need an analysis capable of ruling out practically important differences in both directions, using a predeclared equivalence procedure.',
 lab([], 'Write a decision sentence for each interval: [−2,+12], [+0.2,+1.0], and [+4,+8] percentage points. Assume a three-point gain is needed to justify switching and all comparisons are otherwise valid.',
 'The first leaves both harm and worthwhile benefit plausible. The second supports a small positive change that falls short of the required gain. The third supports a gain above the stated threshold under its interval assumptions. Cost, critical regressions, and validity still belong in the decision.'), ['asa','binomial','paired','equivalence']),

lesson(10,2,'sample-size','Sample size: plan the precision you need',
 'Choose a meaningful effect and a defensible variance assumption before spending your eval budget.',
 '''<h2 id="question">There is no universal task count</h2>
<p>“How many examples do I need?” is incomplete. To estimate one rate to a chosen precision, you need a margin of error and an outcome model. To detect a difference, you need its size, a test, an error threshold, desired power, and a variance assumption. Clustering and stratification can change the calculation.</p>
<p>For an iid binary rate near 50%, the approximate 95% margin of error is <code>1.96 × √(0.25/n)</code>. Solving for a margin of five percentage points gives about 385 observations. Near 50% is a conservative planning choice for Bernoulli variance; it does not make a convenience sample representative.</p>
<h2 id="paired">Plan for paired differences</h2>
<p>For an approximately normal mean of independent paired differences, a common large-sample planning approximation is:</p>
<div class="math">n ≈ [(z<sub>1−α/2</sub> + z<sub>power</sub>) × s<sub>d</sub> / δ]²</div>
<p>The numerator combines the two-sided test threshold and desired-power threshold, then multiplies by the assumed standard deviation of task differences. Divide by the effect δ you want to detect and square. Round upward. A z value is a quantile of the standard normal distribution; the lab computes it. This is an approximation, not an exact design guarantee. '''+cite('miller')+'''</p>
<p>With difference SD 0.5, a three-point effect (δ = 0.03), alpha 0.05, and power 0.8, the lab plans 2,181 independent pairs. The assumed SD belongs to B−A, not to A alone. A pilot on representative, independently selected units can inform it, but a noisy pilot should motivate sensitivity checks.</p>
<h2 id="sensitivity">Ask what could change the answer</h2>
<p>Halving the target effect approximately quadruples the task requirement when other assumptions stay fixed. Strong positive pairing can lower difference variance. Related tasks can reduce the effective information. A tiny rare-failure slice may require its own plan even if the overall average has ample precision.</p>
<p>Run the planning calculation with several plausible difference SDs. If the budget works only under the most optimistic assumption, state that risk before collecting data. For complex clustered, weighted, or sequential designs, simulate the actual proposed sampling and analysis rather than applying an independent-pair formula unchanged.</p>
<h2 id="which-budget">Tasks, attempts, and grader effort</h2>
<p>Budget for distinct tasks, repeated attempts, and validation of the grader. If the main uncertainty is how performance varies between repositories, adding independent repositories may help more than rerunning one repository a hundred times. If each observed task’s behavior is very unstable, repeats can help. If grader labels are unreliable, more unreviewed labels can precisely reproduce the wrong score.</p>
<p>The formula above plans rejection of a zero-effect null when the true effect is δ. It does not plan proof that the effect exceeds a separate deployment margin. To support a gain above three points when you expect five, the gap to the decision boundary is only two points; use a design matching that hypothesis.</p>
<div class="evals"><span class="label">In eval work</span><p>Record the smallest effect that changes your decision, the assumed paired SD, how that assumption was obtained, and the planned stopping point. A reviewer can then assess whether “no clear difference” was an expected possibility.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Computing “observed power” from the final observed effect adds little to the result. After data collection, report the interval and what important effects it does or does not rule out.</p></div>''',
 'You planned to detect a six-point effect but now care about three points. Can the same task count promise the same power?',
 'Generally no. Under the same approximate independent-pair variance model, halving the effect needs about four times as many pairs. Revisit the budget or accept a less precise decision; do not hide the changed requirement.',
 lab(['python3 labs/stats_lab.py power --delta 0.06 --sd 0.5','python3 labs/stats_lab.py power --delta 0.03 --sd 0.5','python3 labs/stats_lab.py power --delta 0.03 --sd 0.35'],
 'Predict which plan requires the most pairs. Run all three and explain why a smaller difference SD changes the budget.',
 'A smaller target effect raises the requirement; a smaller difference SD lowers it. The results count independent pairs. They are not permissions to substitute correlated attempts for new tasks.'), ['miller','mean']),
]
