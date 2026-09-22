from common import lesson, lab, cite

LESSONS = [
lesson(0,0,'orientation','What statistics lets you say',
 'Learn to turn an eval result into a claim whose scope, uncertainty, and practical meaning you can explain.',
 '''<h2 id="the-job">The job is to defend an inference</h2>
<p>You change an agent’s prompt and its pass rate rises from 72% to 78%. You now have several questions: did you test the same tasks, did the grader change, how much could the difference vary, and is the change worth its cost? Statistics gives you a language for answering these questions. It cannot choose the product’s priorities or rescue an eval that measures the wrong behavior.</p>
<p>An <strong>eval</strong> is a procedure: select tasks, run a specified system, observe its behavior, apply scoring rules, and summarize. A score is the end of that procedure. Your job is to understand the chain that produced it before interpreting its last number.</p>
<div class="diagram">decision → target population → task selection → runs → grading
         → paired observations → uncertainty → scoped conclusion</div>
<h2 id="running-case">Meet the running case</h2>
<p>In this course, A is a baseline agent and B is a candidate. They are fictional. The first dataset contains 200 paired tasks, one attempt per version. A passes 144; B passes 156. Later you will use 120 tasks from 30 repositories with three attempts per version per task. Those tasks are deliberately related, and the candidate behaves differently on routine and sensitive work. All numbers are synthetic teaching examples, never claims about a real model.</p>
<p>Keeping the example small lets you inspect the underlying observations. A dashboard that only retains 72% and 78% has already discarded useful information. By the end, you will know which rows, identifiers, and run metadata to preserve.</p>
<h2 id="abilities">Three professional abilities</h2>
<ul><li><strong>Discuss:</strong> explain why a higher score can still leave a decision unresolved, without calling the result “just noise.”</li>
<li><strong>Navigate:</strong> inspect a result file, find the independent unit, identify missing outcomes, and reproduce an estimate.</li>
<li><strong>Design:</strong> choose a metric, task sample, run budget, comparison, and stopping rule before seeing the result.</li></ul>
<p>The competence target is a ten-minute result review: given an eval report, identify what it estimates, whether the uncertainty calculation matches the data, and what decision the evidence supports. The final lesson asks you to write that review.</p>
<h2 id="prerequisites">Start with ordinary arithmetic</h2>
<p>You need fractions, percentages, and willingness to read a short formula. Every symbol is explained when introduced; there is no calculus prerequisite. The <a href="../appendices/a-math.html">math reference</a> is available whenever notation gets in the way. The sibling <a href="../../../evals/evals-tut/index.html">evals course</a> explains what makes a good evaluation; this course develops the statistical reasoning behind its measurements.</p>
<p>Read the pages in order the first time. Predict an answer before opening each reasoning check. A mistaken prediction is useful: it tells you which assumption you were carrying. Terminal exercises use Python 3.9 or newer, its standard library, and local files. No model, API key, installation of packages, or network is needed. Every shown command assumes your terminal is in <code>tutorials/statistics/statistics-tut</code>.</p>
<div class="evals"><span class="label">In eval work</span><p>A good report says “B improved observed success by six percentage points on these paired tasks; the interval still includes some deterioration.” It separates the observation from the generalization and the action.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>“Statistics will tell me which model is best.” It can quantify particular comparisons under particular assumptions. “Best” still requires a workload, priorities, and acceptable tradeoffs.</p></div>''',
 'A teammate gives you two percentages and asks which version to ship. What do you ask for first?',
 'Ask for the task-level results and identifiers, task selection process, scoring and timeout policies, run configurations, and the decision threshold. You need to establish whether the scores answer the same question before choosing a test.',
 lab(['python3 labs/stats_lab.py --help','python3 labs/stats_lab.py quiz'],
 'Open a terminal in the course directory. Inspect the available experiments, then try the six-question quiz as a baseline. It is fine to miss questions now.',
 'The quiz explains each answer and saves nothing. Revisit it after the course; being able to explain your choice matters more than remembering an option number.'), ['miller','asa']),

lesson(1,0,'quantities-and-denominators','Name the quantity before calculating it',
 'A fraction is only meaningful when you know what its numerator and denominator count.',
 '''<h2 id="estimand">The target has a name</h2>
<p>An <strong>estimand</strong> is the exact quantity you want to learn. “Agent quality” is too broad. “Probability that this agent completes a newly sampled support task within two minutes, with at most one retry, judged by rubric version 3” specifies a measurable target. The observed result is an estimate of that target.</p>
<p>Write down the population, unit, outcome, run policy, and aggregation. If the unit is a user session, ten tool calls inside that session are not ten independent sessions. If the outcome is successful completion before a deadline, passing after the deadline is not the specified success. If you change the retry budget, you are evaluating a different procedure.</p>
<h2 id="units">Rates, percentages, and percentage points</h2>
<div class="math">A = 144 / 200 = 0.72 = 72%<br>B = 156 / 200 = 0.78 = 78%<br>Absolute change = 78% − 72% = 6 percentage points</div>
<p>Divide passes by eligible tasks to get a rate. Multiply by 100 to express it as a percentage. Subtract percentages to get percentage points. The relative improvement is <code>(0.78 − 0.72) / 0.72 ≈ 8.3%</code>. The same result therefore has a six-point absolute improvement and an approximately 8.3% relative improvement. Label the scale.</p>
<p>Relative error reduction uses another denominator. Errors fall from 28% to 22%, so relative error reduction is <code>(0.28 − 0.22) / 0.28 ≈ 21.4%</code>. These are three descriptions of the same observations. None supplies uncertainty, and the biggest-looking number is not automatically the most useful one.</p>
<h2 id="denominators">A denominator is an inclusion policy</h2>
<p>Imagine 100 scheduled tasks: 72 pass, 18 complete and fail, and 10 time out. The completed-only success rate is 72/90 = 80%. The scheduled-task success rate, counting timeouts as unsuccessful, is 72/100 = 72%. Both arithmetic operations are correct. They answer different questions.</p>
<table><tr><th>Question</th><th>Numerator</th><th>Denominator</th></tr><tr><td>Delivered success under the deadline</td><td>72 passes</td><td>100 scheduled tasks</td></tr><tr><td>Success among completed tasks</td><td>72 passes</td><td>90 completed tasks</td></tr><tr><td>Completion rate</td><td>90 completions</td><td>100 scheduled tasks</td></tr></table>
<p>Do not automatically classify every infrastructure error as a model failure. Define the system boundary first. A delivered-service metric can include service failures; a capability study may separately diagnose broken task environments and rerun them under a documented, symmetric rule. The key is preserving every scheduled case and explaining its disposition.</p>
<h2 id="fixed-versus-future">A fixed set and future tasks are different targets</h2>
<p>If the question is simply “what fraction of these recorded outcomes passed?”, the arithmetic is exact once the labels are fixed. An interval becomes relevant when you generalize: to new tasks, future stochastic runs on these tasks, new graders, or a changing deployment population. State which source of variation you are modeling. Different questions need different repeated experiments.</p>
<div class="evals"><span class="label">In eval work</span><p>Before a launch comparison, write: “Equal-task average success over newly sampled tasks from the declared workload, three attempts per task, with timeouts counted under policy X.” That sentence determines what your analysis must preserve.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>A cleaner denominator can create an apparent improvement without changing a single successful outcome. Always display scheduled, completed, excluded, and scored counts beside a rate.</p></div>''',
 'Version B gets 80% after dropping timeouts; A gets 72% with timeouts included. Is that evidence of improvement?',
 'The reports use different inclusion policies. Recompute both under the same declared policy and compare completion rates. If B disproportionately times out on difficult cases, completed-only accuracy is a selected subset.',
 lab([], 'Write an estimand for an agent that edits repositories. Include population, time budget, retries, scoring, and weighting. Then rewrite it for the question “How reliable is it on these exact ten regression cases?”',
 'The first target concerns new tasks from a defined population. The second keeps tasks fixed and concerns future attempts under a fixed policy. A task bootstrap addresses the first kind of sampling uncertainty, not automatically the second.'), ['miller']),

lesson(2,0,'read-the-data','Read the observations before the average',
 'Understand the shape of your data and what an average hides before attaching an error bar.',
 '''<h2 id="rows">What does one row mean?</h2>
<p>A useful eval table retains task ID, related-group ID, system version, attempt number, outcome, grader version, elapsed time, and failure status. Never assume one row equals one independent piece of evidence. A row might be a tool call, an attempt, a task summary, or an entire run.</p>
<p>Our JSONL files have one JSON object per line and one task per object. Fields <code>a</code> and <code>b</code> contain binary outcomes for each version’s attempts. In the first dataset each list has one element. In the second it has three. The <code>cluster_id</code> records a shared repository, and <code>slice</code> records the task category. That structure is intentional: it keeps relationships visible.</p>
<h2 id="summaries">Mean, median, and spread</h2>
<p>The mean is the sum divided by the count. The median is the middle ordered value; for an even count we average the two middle values. Consider five hypothetical runtimes in seconds:</p>
<div class="diagram">Ordered runtimes:  1   1   2   2   24
Mean:             (1 + 1 + 2 + 2 + 24) / 5 = 6
Median:           middle value = 2</div>
<p>The mean is useful for total resource planning: these five jobs consume 30 task-seconds in total. The median describes a typical central observation. Neither is a substitute for the other. Reporting just the median hides the 24-second task; reporting just the mean makes it easy to imagine every task taking about six seconds.</p>
<p>A quantile marks a position in an ordered distribution. A 95th percentile, or p95, is near the upper tail. Sample quantile conventions differ. The lab uses linear interpolation at index <code>(n−1)q</code> in a zero-indexed sorted list. For the five runtimes, q = 0.95 gives index 3.8 and a value of 19.6 seconds. A nearest-rank convention gives 24. Neither creates enough observations to characterize a real p95 well.</p>
<h2 id="binary-and-graded">Know the score’s scale</h2>
<p>With pass=1 and fail=0, the mean is the pass rate. A fractional score such as 0.6 might mean three of five rubric points, an average of repeated binary outcomes, or a grader’s subjective rating. Those meanings matter. A binomial calculation for 0/1 trials does not automatically apply to fractional task scores.</p>
<p>Ordinal ratings such as poor/fair/good have an ordering but no guaranteed equal spacing. Turning them into 1/2/3 and averaging imposes a spacing assumption. A useful report retains the category counts and rubric so readers can assess whether the summary is meaningful.</p>
<h2 id="outliers">Investigate unusual observations</h2>
<p>An outlier may be a timestamp bug, a legitimate difficult task, or a distinct failure mechanism. Find its trace. Correct documented measurement errors; keep real slow tasks in a workload metric that is supposed to include them. If you report a trimmed mean, define the trimming rule and explain that it estimates something different from total average runtime.</p>
<div class="evals"><span class="label">In eval work</span><p>Compare distributions and counts by version and task category before inference. A sudden score increase accompanied by fewer rows, lost IDs, or a missing hard slice is a data-integrity lead, not a statistical discovery.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>A small standard error around a wrong aggregate is precise reporting of the wrong quantity. First establish the unit, scale, inclusion rules, and unusual cases.</p></div>''',
 'An agent’s median latency improves while total runtime and timeout rate get worse. Can both reports be true?',
 'Yes. More than half of cases may have become faster while a smaller tail became much slower or failed to complete. Inspect full timings and failure status. A successful-only median can also conceal excluded timeouts.',
 lab(['python3 labs/stats_lab.py compare --resamples 100'],
 'Open <a href="../labs/data/paired_tasks.jsonl">the data file</a> in a text editor and inspect a few records. Run the small resampling demonstration, then explain what three outcomes inside one task would mean for the task count.',
 'Three outcomes are three attempts on one task. The file retains task identity so averaging attempts or resampling related tasks does not require guessing relationships from row order.'), ['metrics','mean']),

lesson(3,1,'probability','Probability, conditioning, and independence',
 'Learn the small set of probability ideas that explains why an unchanged system can produce different scores.',
 '''<h2 id="binary">A pass is a random variable</h2>
<p>A random variable is a numeric outcome whose value is uncertain before observation. Let X be one if an agent passes a task and zero otherwise. If its pass probability under specified conditions is p, X has a Bernoulli distribution. With p = 0.7, the chance of a pass is 70%; a failure is still an ordinary possible outcome.</p>
<p>The expectation is the probability-weighted average of possible values. For this binary outcome, it is <code>1 × p + 0 × (1−p) = p</code>. An expected value of 0.7 does not imply an individual attempt can score 0.7. It describes the average over repetitions of the experiment.</p>
<h2 id="conditioning">Specify the condition</h2>
<p>Conditional probability restricts attention to some stated information. “Passes given a routine task” can differ from “passes given a sensitive task.” Suppose routine tasks are 80% of a hypothetical workload and pass with probability 0.9, while sensitive tasks are 20% and pass with probability 0.4.</p>
<div class="math">P(pass) = 0.8 × 0.9 + 0.2 × 0.4 = 0.80</div>
<p>The overall pass probability is the weighted average of the two within-category probabilities. If the task mix changes, the overall rate changes even when behavior within each category stays fixed. This is why an evaluation needs a population description.</p>
<p>Conditioning also explains grader statistics. “The grader flags a failure given that a real failure occurred” is not the same as “a real failure occurred given that the grader flagged it.” Reversing the condition silently changes the denominator. You will work through that distinction in <a href="14-grader-quality.html">grader quality</a>.</p>
<h2 id="independent">When can you multiply?</h2>
<p>Independence means learning one outcome does not change the distribution of the other. Two independent attempts each passing with probability 0.7 both pass with probability <code>0.7 × 0.7 = 0.49</code>. At least one passes with probability <code>1 − 0.3 × 0.3 = 0.91</code>. We count “at least one” by subtracting the probability that both fail.</p>
<p>Without independence, use the conditional probability: <code>P(A and B) = P(A) × P(B given A)</code>. A shared broken service, common source document, or leaked answer can connect outcomes. A different random seed does not remove every shared cause.</p>
<h2 id="binomial">From attempts to a count</h2>
<p>The number of passes in n independent Bernoulli trials with the same p follows a binomial distribution. Its expected count is np. In ten trials at p = 0.7, that is seven passes. It does not mean every batch contains exactly seven.</p>
<p>Task heterogeneity needs care. Conditional on a fixed collection of tasks, each task may have a different pass probability, so the total need not be binomial with one shared p. Independently sampling new task-and-attempt pairs from a stable mixture can instead produce binary observations with the same marginal p. The sampling story determines which model fits.</p>
<div class="evals"><span class="label">In eval work</span><p>Write the event precisely: “success on the next randomly selected task under this run policy.” A probability without its task distribution and conditions is easy to overgeneralize.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>“Each call was separate, so the observations are independent.” Shared tasks, repositories, outages, sessions, and evaluators can produce dependence across separate calls.</p></div>''',
 'Two attempts have a 70% marginal pass rate. Can you conclude there is a 91% chance at least one passes?',
 'Only with the needed independence and common-policy assumptions. If both outcomes always match, the chance of at least one pass is 70%. Inspect how retries share state and conditions before multiplying probabilities.',
 lab(['python3 labs/stats_lab.py sample --p 0.7 --trials 10 --experiments 2000'],
 'Predict whether every ten-task sample will score 70%. Run the simulation and inspect the histogram. Repeat with 100 trials.',
 'The simulator holds the true p fixed but observed rates vary. Larger independent samples concentrate more tightly. This simulator explicitly generates iid trials; that assumption must be justified for real eval data.'), ['binomial']),

lesson(4,1,'sampling','Sampling: which world does the score describe?',
 'A large sample only helps if its selection process connects it to the population you care about.',
 '''<h2 id="frame">Population, frame, sample</h2>
<p>The population is the world your claim addresses. The sampling frame is the accessible source you draw from. The sample is what you actually observe. For an assistant, the population might be next month’s user tasks, the frame last month’s eligible logged tasks, and the sample 500 randomly chosen records. Each transition introduces a question.</p>
<p>Are users who opted out absent from the frame? Did logging miss long sessions? Does next month introduce a new language? Statistical sampling uncertainty concerns variation inside a stated selection model. It does not by itself account for unrepresented users or future distribution shift.</p>
<div class="diagram">Target: future eligible work
   ↓ approximation and time shift
Frame: available, consented historical cases
   ↓ sampling policy
Sample: selected cases
   ↓ exclusions and execution
Analyzed data: recorded, scored outcomes</div>
<h2 id="selection">Random selection and deliberate coverage</h2>
<p>Random sampling makes selection probabilities explicit. It does not guarantee that every small sample resembles the population. Stratified sampling divides the frame into categories and samples within each, which can ensure meaningful coverage of rare categories. If you oversample a category, you may need weights to estimate the original workload average.</p>
<p>A deliberately difficult challenge set serves a different purpose. It can reveal whether a failure is possible, exercise an important boundary, or track regressions. Its failure fraction is not automatically a prevalence estimate for production traffic. Preserve its value by naming its intended use.</p>
<p>For a small regression suite, a fixed-set report may be entirely appropriate: these exact cases passed or failed under these conditions. Avoid attaching a population interpretation that the selection process cannot support.</p>
<h2 id="more-data">Why more data cannot remove every error</h2>
<p>Suppose all your sampled tasks are English summaries, but your deployment also answers Spanish questions and edits code. A million summaries can estimate behavior on that summarization frame precisely. It cannot fill the missing task categories. More observations reduce random sampling variation under a model; they do not necessarily reduce selection bias.</p>
<p>Repeatedly taking fresh random samples from the same incomplete frame gives you repeated versions of the same omission. When a score matters, inspect both the uncertainty calculation and the frame’s coverage. These are separate pieces of evidence.</p>
<h2 id="splits">Separate development from confirmation</h2>
<p>You may inspect development tasks, fix failure modes, and iterate. That is useful engineering. A held-out evaluation asks whether the changes transfer to cases that did not guide those choices. Split at the level that prevents leakage: repository, user, document, or template when its descendants are related. Randomly splitting individual paraphrases from the same source can leave near-duplicates on both sides.</p>
<p>Keep a manifest recording where tasks came from, selection rules, grouping, exclusions, and split assignment. If someone asks why a result should generalize, that manifest is often more useful than another decimal place.</p>
<div class="evals"><span class="label">In eval work</span><p>Build two explicitly named assets when needed: a representative sample for population estimates and a failure-focused suite for diagnostics. They can inform the same decision while answering different questions.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Calling a convenience sample “representative” because it contains many rows. Representativeness concerns how cases enter the dataset, not simply its size.</p></div>''',
 'You collect 1,000 examples by searching logs for “user complained.” What can the failure rate tell you?',
 'It describes the selected complaint-linked cases under your labeling policy. Without a known selection mechanism relating those cases to all eligible interactions, it does not estimate the overall failure rate. It can still be excellent material for error analysis.',
 lab([], 'Design a sample for an agent serving routine and sensitive tasks. Specify a frame, a random selection rule, a grouping ID, and one likely coverage gap.',
 'A defensible answer names the accessible population and its omissions, preserves related-group IDs, and reserves independent groups for confirmation. If you sample equal numbers from unequal categories, state whether the final target is category-balanced or traffic-weighted.'), ['miller','blocks']),

lesson(5,1,'spread-and-standard-error','Spread of outcomes versus uncertainty of an average',
 'Standard deviation and standard error answer different questions. Learn to recognize both in an eval report.',
 '''<h2 id="spread">Measure the scatter</h2>
<p>Take four hypothetical task scores: 0, 0, 1, 1. Their mean is 0.5. Deviations from the mean are −0.5, −0.5, +0.5, +0.5. Squaring makes them all 0.25, so the squared deviations sum to 1.</p>
<div class="math">Sample variance s² = 1 / (4 − 1) = 1/3<br>Sample standard deviation s = √(1/3) ≈ 0.577</div>
<p>For independent observations from a common distribution with finite variance, dividing by n−1 corrects the usual sample variance for having estimated the center from those same observations. The square root returns to the original score scale. Standard deviation describes how individual scores vary around their mean.</p>
<h2 id="se">Now repeat the whole measurement</h2>
<p>Imagine independently sampling four new tasks and calculating another mean. Repeat that entire process many times. The means themselves have a distribution. Its standard deviation is the standard error of the mean. You usually have one dataset, so you estimate that standard error.</p>
<div class="math">Estimated SE(mean) = s / √n</div>
<p>Take the observed standard deviation and divide by the square root of the independent sample count. The formula requires the relevant independence and common-population assumptions. NIST’s mean interval uses this quantity together with a suitable critical value. '''+cite('mean')+'''</p>
<p>For the four scores, estimated SE is about 0.289. This is a tiny sample: mechanically calculating an SE does not establish that a normal interval will have good coverage. The next lesson develops that distinction.</p>
<h2 id="binary">The binary shortcut</h2>
<p>A Bernoulli outcome has population variance <code>p(1−p)</code>. At p = 0.7, that is 0.21, with standard deviation about 0.458. The mean of 100 independent trials has theoretical standard error <code>√(0.21/100) ≈ 0.0458</code>, or 4.58 percentage points. With 400 trials it is about 2.29 points.</p>
<p>When p is unknown, substituting the observed pass fraction gives the familiar plug-in formula <code>√(p̂(1−p̂)/n)</code>. The hat means “estimated from data.” It differs slightly from using the sample standard deviation with its n−1 denominator. Both become close for large n; neither fixes dependence or extreme small-sample behavior.</p>
<h2 id="square-root">What the square root costs</h2>
<p>To halve this standard error while holding the outcome distribution and independence assumptions fixed, you need four times as many observations. Ten times the sample size reduces it by about √10, not by ten. This is why a small effect can be expensive to distinguish reliably.</p>
<p>Do not confuse adding distinct tasks with rerunning the same tasks. New tasks can reduce uncertainty from task selection. More attempts estimate each observed task’s behavior more precisely. Both can help, but they act on different parts of the variation; <a href="11-clusters-and-repeats.html">lesson 11</a> separates them.</p>
<div class="evals"><span class="label">In eval work</span><p>If a chart labels error bars “±1 SD,” ask whether it means variation across task scores, repeated run means, or bootstrap estimates. These describe different distributions. Label the object whose spread is being displayed.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Duplicating every observation four times can trick a naive formula into halving its reported SE. No new evidence was collected. The apparent precision comes from a false independence assumption.</p></div>''',
 'A report says task-score SD is 0.4 across 100 independent tasks. Does that imply uncertainty of 40 percentage points around the mean?',
 'No. The estimated SE of the mean is 0.4/√100 = 0.04, or four percentage points, under the independence model. Individual outcomes remain much more variable. An interval adds a method and coverage assumptions.',
 lab(['python3 labs/stats_lab.py sample --trials 100 --seed 7','python3 labs/stats_lab.py sample --trials 400 --seed 7'],
 'Predict the ratio of the two theoretical SEs. Run both experiments and compare the empirical SD of estimates with the theoretical SE.',
 'The theoretical SE halves. The empirical SD is close but not identical because the simulation itself uses finitely many experiments. Increasing experiments improves the simulation estimate; increasing trials improves each simulated eval.'), ['mean','binomial']),
]
