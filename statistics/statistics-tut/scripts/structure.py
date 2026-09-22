from common import lesson, lab, cite

LESSONS = [
lesson(11,3,'clusters-and-repeats','Repeated runs and related tasks',
 'Count independent evidence at the level your claim requires, while retaining what repeated attempts teach you.',
 '''<h2 id="hierarchy">Draw the hierarchy first</h2>
<p>The second fixture has 30 repositories, four tasks per repository, and three attempts per version per task. That means 120 tasks and 360 attempts per version. It does not mean 360 independent samples of repositories. Tasks from one repository share patterns; repeated attempts also share a task.</p>
<div class="diagram">30 repositories
 └─ 4 tasks each: 120 task pairs
     └─ 3 attempts/version/task: 360 outcomes per version</div>
<p>A cluster is a group whose observations can be related. If your inference concerns newly sampled repositories, preserve repositories as the independent sampling units. If relatedness instead crosses repositories through a common template or shared outage, repository grouping alone may be insufficient. The grouping variable should reflect the dependency you need to model.</p>
<h2 id="repeats">What does another attempt buy?</h2>
<p>For task i, imagine a stable success probability pᵢ under the run policy. Repeating the task estimates pᵢ more precisely. Sampling new tasks teaches you how pᵢ varies across the population. For n independent tasks and k conditionally independent attempts per task, a useful variance decomposition is:</p>
<div class="math">Var(overall mean) = Var(pᵢ)/n + E[pᵢ(1−pᵢ)]/(n k)</div>
<p>The first term is variation from selecting tasks; the second is variation from finite attempts on those tasks. Increasing k reduces only the second term in this model. The decomposition needs independently sampled tasks, a stable per-task probability, and independent attempts conditional on task. It does not model arbitrary shared outages. '''+cite('miller')+'''</p>
<h2 id="analysis">Averaging and resampling in the lab</h2>
<p>The lab first averages each version’s attempts within a task, then computes that task’s B−A difference. With <code>--unit task</code>, it resamples those task differences independently. With <code>--unit cluster</code>, it resamples repository groups, keeping all task differences inside each selected repository together.</p>
<p>This estimates a task-weighted population contrast under independent sampling of the chosen top-level units. Within-task noise is already present in the observed task means. The lab does not add a second bootstrap of attempts. If the target instead keeps these exact tasks fixed and asks about future attempts only, use an analysis conditional on those tasks rather than task-population resampling.</p>
<h2 id="result">Same estimate, different precision</h2>
<p>The candidate’s observed gain is ten percentage points. The task bootstrap gives approximately +5.56 to +14.44 points; the repository bootstrap gives approximately +1.11 to +18.89 points with the course’s fixed seed. The estimate does not change. The interval changes because the analysis recognizes how much independent evidence was collected.</p>
<p>The fixture intentionally makes tasks within repositories strongly related. It demonstrates a mechanism, not an empirical estimate of real repository correlation. Thirty repositories still leave limitations; the sensitive slice contains only ten, so its bootstrap interval deserves additional caution.</p>
<div class="evals"><span class="label">In eval work</span><p>Show counts at every level. “30 repositories, 120 tasks, three attempts per model per task” lets readers evaluate a claim that “360 samples” obscures.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Pseudoreplication occurs when correlated measurements are counted as independent evidence. Repeated runs are valuable, but their value does not come from relabeling them as new tasks.</p></div>''',
 'A launch rule requires the lower endpoint to exceed +3 points. The task interval clears it; the repository interval does not. Which should drive the rule?',
 'Use the analysis matching the predeclared sampling design and intended population. If repositories are the independent sampled units, the repository result leaves the required gain unresolved. Choosing the narrower method because it passes is outcome-driven selection.',
 lab(['python3 labs/stats_lab.py compare --data labs/data/clustered_tasks.jsonl --unit task','python3 labs/stats_lab.py compare --data labs/data/clustered_tasks.jsonl --unit cluster'],
 'Predict which numbers remain identical. Compare estimates, interval widths, and independent-unit counts. Explain the task-mode caution message.',
 'The observed mean stays at +10 points. Repository resampling widens this fixture’s interval because related tasks move together. The task-mode result is intentionally provided as a comparison, not as a justified default for clustered data.'), ['miller','bootstrap']),

lesson(12,3,'slices-and-weights','Slices, weights, and misleading averages',
 'Decide whose tasks the average represents and inspect important subgroups without turning every slice into a discovery.',
 '''<h2 id="mixture">An average has weights</h2>
<p>A stratum is a defined subgroup, such as task type or language. A slice is a practical label for a subgroup you inspect. An overall average combines subgroup results using weights, whether you choose them explicitly or let dataset counts choose them implicitly.</p>
<p>Suppose a fixture includes 80 routine and 40 sensitive tasks. A pooled task mean gives routine tasks two thirds of the weight. An equal-category macro-average gives each category one half. A traffic-weighted mean uses the deployment mix. These are different estimands, not interchangeable formatting options.</p>
<div class="math">Overall change = w × routine change + (1−w) × sensitive change</div>
<p>Multiply each category’s change by its target proportion and add. The weights must describe the population or normative priority you intend to measure. If categories overlap, this simple partition formula cannot be used without resolving double counting.</p>
<h2 id="running">A gain that hides a regression</h2>
<p>In the clustered fixture, the routine category improves by about 23.33 percentage points; the sensitive category worsens by about 16.67 points. With two-thirds routine weight, the overall change is +10 points. Equal category weighting gives about +3.33 points. A hypothetical workload with 20% routine and 80% sensitive work gives about −8.67 points.</p>
<p>All three summaries use the same category changes. Before selecting one, ask what population or priority the report is supposed to represent. A high-impact category can also have a guardrail independent of the average. A weighted benefit elsewhere need not compensate for a critical failure.</p>
<h2 id="simpson">Different mixes can reverse a comparison</h2>
<table><tr><th>System</th><th>Easy tasks</th><th>Hard tasks</th><th>Overall</th></tr><tr><td>A</td><td>81/90 = 90%</td><td>2/10 = 20%</td><td>83/100 = 83%</td></tr><tr><td>B</td><td>19/20 = 95%</td><td>24/80 = 30%</td><td>43/100 = 43%</td></tr></table>
<p>B’s observed within-category rates are higher, but its overall score is lower because it saw mostly hard tasks. This is a constructed example of a mix-driven reversal. It does not prove a causal advantage within categories: different task selection may still confound those comparisons. A matched task set and common weights provide a more interpretable design.</p>
<h2 id="uncertainty">Weight the uncertainty calculation too</h2>
<p>If the sampling design fixes category counts, a stratified bootstrap typically resamples independent units within categories and then applies the target weights. Do not bootstrap a pooled file and assume it reproduces a design that intentionally fixed stratum counts. If repositories span categories, preserving repository dependence and category design together requires a suitable method.</p>
<p>The course CLI reports the included sample’s equal-task mean and can filter one slice. It does not implement general survey weights or a stratified design. Use the arithmetic above to understand sensitivity; do not attach the CLI’s unweighted interval to a newly weighted estimate.</p>
<div class="evals"><span class="label">In eval work</span><p>Predeclare a primary aggregate and a small set of important guardrails. Use other slices to find hypotheses for follow-up. A discovered weak slice can be operationally important even when it is not a confirmatory statistical finding.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Searching dozens of slices and presenting the largest observed gain as if it were planned. The selection process affects how confidently you can generalize that result.</p></div>''',
 'Your eval oversamples rare, sensitive tasks to get more information. Must you discard those extra tasks to report production performance?',
 'No. Keep the data and use a design-aware weighted estimator for a specified production mixture, with uncertainty that respects the sampling design. Also report the sensitive slice directly. The weights and the extra diagnostic coverage serve different purposes.',
 lab(['python3 labs/stats_lab.py compare --data labs/data/clustered_tasks.jsonl --unit cluster --slice routine','python3 labs/stats_lab.py compare --data labs/data/clustered_tasks.jsonl --unit cluster --slice sensitive'],
 'Inspect the two category changes and their group counts. Compute the overall change at routine weights of 2/3, 1/2, and 1/5.',
 'The changes are approximately +10, +3.33, and −8.67 points. The sensitive-slice interval is based on only ten independent repositories in this teaching model. Do not treat an exploratory slice interval as automatically adjusted for all slices you might inspect.'), ['miller','metrics']),

lesson(13,3,'missingness-and-timeouts','Missing outcomes, timeouts, and selection',
 'A result that is absent from the file is still part of the experiment you scheduled.',
 '''<h2 id="ledger">Start with a task ledger</h2>
<p>Before execution, create the list of scheduled tasks and planned attempts. Afterward, reconcile every expected outcome against it. Completed failures, timeouts, cancelled work, harness errors, missing logs, and excluded tasks are different statuses. Collapsing them into a blank field loses the evidence needed to interpret the score.</p>
<p>A missing outcome is not automatically a zero, and it is not automatically eligible for deletion. The correct handling depends on the estimand. A delivered-service success metric can count an exhausted timeout budget as unsuccessful delivery. A separate capability analysis may need to distinguish that from a task image that never started.</p>
<h2 id="selection">Why complete cases can mislead</h2>
<p>Suppose A passes 70 of 100 scheduled tasks and all attempts finish. B passes 72, fails 18, and times out on 10. B’s completed-only rate is 80%, while A’s is 70%. Under scheduled-task success, B’s rate is 72%, an observed gain of two points. Excluding B’s timeouts creates an eight-point change in its own reported rate.</p>
<p>If slow failures are more likely to go missing, the observed subset is selected by the outcome process. Independence of tasks does not fix that selection. Compare missingness rates by version, task category, input length, and run conditions; investigate traces for the missing cases.</p>
<h2 id="bounds">Use simple sensitivity bounds</h2>
<p>When ten of 100 scheduled binary outcomes are genuinely unknown and 72 known outcomes passed, the scheduled pass rate lies between 72% and 82% depending on those ten labels. This is a missing-data range, not a sampling confidence interval. It identifies how much the missing outcomes alone could change the answer.</p>
<div class="math">Worst case = known passes / scheduled count<br>Best case = (known passes + unknown outcomes) / scheduled count</div>
<p>Assign every unknown a failure for the lower bound and a success for the upper bound. If a decision changes across these possibilities, recovering outcomes or justifying a missingness model may be more urgent than collecting more unrelated tasks.</p>
<h2 id="latency">A timeout is partial timing information</h2>
<p>If a task is terminated at 60 seconds, you know it did not finish within the allowed window. You do not know its natural completion time. That is censoring: you have partial information rather than a complete duration.</p>
<p>You can legitimately report observed wall time consumed under the 60-second policy, including terminated attempts. That target differs from eventual completion time with no deadline. Do not replace every timeout with 60 and label the resulting percentile “uncensored completion latency.” Choose a policy metric or use an appropriate time-to-event analysis with explicit assumptions.</p>
<h2 id="reruns">Rerun rules belong in the protocol</h2>
<p>Rerunning only the candidate’s failed tasks until they pass changes its effective attempt budget. Rerunning a documented broken environment under a symmetric rule can be justified, but retain the original status and reason. Report the system’s behavior under the policy you actually executed.</p>
<div class="evals"><span class="label">In eval work</span><p>Connect this audit to the <a href="../../../networking/networking-tut/pages/11-timeouts-and-retries.html">networking lesson on retries</a> and the <a href="../../../linux/linux-tut/pages/25-how-harnesses-use-linux.html">Linux harness lesson</a>. Infrastructure behavior can change which outcomes enter a statistical table.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Encoding missing as zero and then claiming you made no assumptions. That encoding is a scoring policy; write it down and ensure it answers the intended question.</p></div>''',
 'A candidate looks faster after you remove every timeout. What evidence would distinguish real speed improvement from selection?',
 'Compare scheduled counts, timeout fractions, task-level paired elapsed times under a common policy, and the types of tasks removed. Report successful-only latency as a conditional metric alongside completion rates. Recover missing records before inferring an unconditional speed gain.',
 lab([], 'For 200 scheduled tasks, 130 known passes, 50 known failures, and 20 unknown outcomes, calculate completed-case accuracy and worst/best scheduled-task rates. Choose what to report.',
 'Completed-case accuracy is 130/180 ≈ 72.2%. The scheduled-task range is 65% to 75% before sampling uncertainty. Report all counts, why the twenty are unknown, and the analysis or recovery policy. Do not call this range a 95% interval.'), ['miller','blocks']),
]
