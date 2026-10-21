from common import lesson, lab, cite, transcript

LESSONS = [
lesson(14,5,'capstone','Capstone: pick a neuron by a documented procedure, pre-register, run, report',
 'The whole protocol on one GPT-2 small MLP neuron, end to end, with the reference run as a worked example and your own run as the deliverable.',
 '''<h2 id="the-task">The task</h2>
<p>Choose one MLP neuron of GPT-2 small by a procedure you write down before you run it. Write the pre-registration (Appendix A) before you look at the neuron on held-out text. Score the explanation on held-out tokens with at least two controls. Report the result in the order of lesson 13, whichever way it came out. The deliverable is a short document; a template is in <code>labs/report-template.md</code>.</p>
<p>The reference run that the course used for lessons 04 and 05 is one instance of this task with eight rules at once. Its documented procedure, from the script’s docstring:</p>
<pre><code>1. Tokenise labs/data/corpus.txt; even 128-token chunks are the screening split,
   odd chunks are held out and are not touched until step 4.
2. For each rule (a deterministic token predicate), find the neuron in every
   layer whose activation correlates best with the rule on the screening split.
   This is where selection bias enters: 12 x 3072 neurons were searched.
3. Pre-register, per rule: held-out Pearson r >= 0.5, AND r above the 95th
   percentile of (a) 200 random neurons from the same layer and (b) 500 shuffled
   copies of the rule's labels.
4. Score on the held-out split and print everything, including failures.</code></pre>
<h2 id="your-procedure">Your procedure must differ in at least one of these</h2>
<p>The point of the capstone is that you make the choices and own them. Pick at least one:</p>
<ul><li><strong>A new rule.</strong> Something contextual rather than token-local: “token inside a quotation,” “second token of a sentence,” “a number that is a quantity rather than a date.” Layer-0 neurons will not carry these; your screening will have to find deeper ones, and your held-out scores will be lower. That is the interesting regime.</li>
<li><strong>A new corpus.</strong> Write 2,000 tokens of your own prose of a different kind (code comments, dialogue, lists) and use the course corpus as the held-out set, or the reverse. This tests distribution shift, which the reference run does not.</li>
<li><strong>A different selection.</strong> Instead of the best-correlated neuron, take the neuron with the highest activation variance in layer 6 and try to explain it from its quantile bands (lesson 03), then pre-register before scoring. This is the harder, more realistic direction: neuron first, explanation second.</li>
<li><strong>A baseline control.</strong> Add a competing explanation to the controls (lesson 05) and require the claim to beat it by a pre-registered margin.</li></ul>
<h2 id="worked">The worked example, read as a capstone report</h2>
<p>Protocol: the four steps above, with the threshold and controls fixed in the script before it was run. Unit: chosen by step 2. Held-out: 12 chunks, 1,536 tokens, never decoded before scoring. Scoring: Pearson r on all held-out tokens. Result:</p>
'''+transcript('''         rule layer neuron  train r held-out r  rand95  shuf95 |rand|max  base rate  verdict
 after_period     2   2928    0.860      0.845   0.125   0.042     0.560      0.103  demonstrated''')+'''
<p>Not tested: whether the neuron does anything else (r² = 0.71, so 29% of its variance is unexplained by the rule); whether the model uses it (no intervention; lesson 10 would patch it); whether it holds on text unlike the corpus; whether its weak activations follow the rule (the score is dominated by the strong tail). Exploratory: lesson 03’s quantile bands suggest the weak region is also sentence starts, but that was a look, not a test. Revised protocol, not yet run: add a baseline control (“token is capitalised”), add a text of a different genre as a second held-out set, and pre-register a precision/recall operating point at activation &gt; 0.5.</p>
<h2 id="kl">The extension the 2026 debate asks for</h2>
<p>Lesson 13 left one test undesigned: Gao’s downstream-KL version. Here is its shape, for you to fill in and, if you have the time, run.</p>
<ol><li>Take the held-out chunks. Run the model normally and record the output distribution at every position.</li>
<li>Run again with a hook on <code>blocks.2.mlp.hook_post</code> that replaces neuron 2928’s activation at every position with the value your explanation predicts: for a rule-form explanation, the neuron’s mean activation on rule-positive screening tokens where the rule fires, and its mean on rule-negative tokens elsewhere.</li>
<li>Measure the mean KL divergence from the normal output distribution to the substituted one, over held-out positions.</li>
<li>Controls: the same substitution for the random neurons of the random-unit control; and substituting the neuron’s overall mean everywhere (mean ablation), which is the KL an explanation with no content would produce.</li>
<li>Pre-register: the explanation’s KL is below the mean-ablation KL by a stated fraction, and below the median of the random-neuron substitutions.</li></ol>
<p>This is the test Gao says would have flagged the cat-and-car explanation of 4e:55, and the one Cammarata says rewards details that do not matter. Both predictions are checkable on this neuron in a few minutes of CPU. If you run it, report it the same way.</p>
<h2 id="rubric-preview">How the capstone is read</h2>
<p>The readiness review on the next page gives the rubric. The short version: a reader should be able to re-run your test from the protocol alone, should see every control beside the score, and should know from your not-tested table exactly what your claim does not cover. A negative result that meets those three is a pass. A positive result that does not is not.</p>
<div class="evals"><span class="label">In interpretability work</span><p>The habit this capstone trains is the one the advice behind this course named as the barrier: the explanation that “cannot predict a neuron’s activations on held-out data has not been demonstrated.” You now have the procedure, the controls, the code, and two worked examples, one of which failed. Write the test before you look.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Iterating on the rule against the held-out split. The first time you score a revised rule on the same held-out chunks, they stop being held out. Keep a third split for the final score, or write the revised rule as a new pre-registration and score it on new text.</p></div>''',
 'You chose the neuron-first direction, wrote an explanation from the quantile bands, and your held-out r is 0.31 with rand95 = 0.14 and shuf95 = 0.05. Pass or fail, and what is the report?',
 'Fail against a 0.5 threshold, and the report says so, with the three numbers. The diagnosis: the explanation is above both nulls, so it captures something specific to this neuron, but explains about 10% of its variance; the neuron is either broader than the rule or the rule is the wrong shape (precision/recall would tell which). The revised protocol proposes a second rule and a new held-out split, labelled not yet run. That document is a contribution: it says what was tested and what a reader should not believe.',
 lab(['python labs/reference/neuron_score.py --all'],
 'Run the reference table once more as a baseline, then do the capstone with your own procedure. Use <code>labs/protocol.py</code> for the pre-registration and <code>labs/explanation_score.py</code> for the scoring, and write the report with <code>labs/report-template.md</code>.',
 'Your held-out scores for contextual rules will be well below the token-local ones in the table; 0.3 to 0.6 is the range to expect for a rule that is roughly right about a deeper neuron. The report is judged on the protocol and the controls, not on the size of r.'), ['gao2026','cammarata2026','bills2023']),

lesson(15,5,'readiness-review','Readiness review',
 'What you should now be able to do, how to check it, and the rubric for the capstone report.',
 '''<h2 id="target">The target, restated</h2>
<p>Replicate a vision-neuron claim on InceptionV1 and a language-neuron claim on GPT-2 small, with the prediction test written before looking. Both have been done in this course with the tests in the transcript, one of them twice because the first design could not work with these weights. The question is whether you can now do it without the course.</p>
<h2 id="self-check">Self-check</h2>
<table><tr><th>Can you…</th><th>Evidence</th></tr>
<tr><td>Fill every field of the protocol template for a claim you have not yet tested, including a threshold that respects the base rate?</td><td>Your capstone protocol; lesson 08’s failure as the counter-example</td></tr>
<tr><td>Explain why max-activating examples cannot establish an explanation, and show quantile bands instead?</td><td>Lesson 03; <code>maxact.py</code> on a neuron of your choice</td></tr>
<tr><td>Score a rule-form explanation on held-out tokens and read the four numbers (score, two controls, base rate)?</td><td><code>labs/explanation_score.py</code> tests green; lesson 05’s table read aloud</td></tr>
<tr><td>Say what each control rules out, and why a percentile rather than a maximum?</td><td>Lesson 05</td></tr>
<tr><td>Design a two-stage screen/held-out test for a vision unit, with a discriminating hypothesis (H2, H4) and a random-channel control?</td><td><code>labs/curve_detector.py</code> tests green; lesson 07’s not-tested table</td></tr>
<tr><td>Fit a probe, run its two controls, and word the claim as observational?</td><td><code>labs/probe.py</code> tests green</td></tr>
<tr><td>Write a logit-lens and direct-logit-attribution table whose parts sum to the logit, and say what it does not show?</td><td>Lesson 09; the 11.02 check</td></tr>
<tr><td>Run a residual-stream patch with a matched pair and a control position, and word the claim as interventional?</td><td><code>labs/patching.py</code> tests green</td></tr>
<tr><td>Detect induction heads from the definition alone, with the control sequence?</td><td><code>labs/induction.py</code> tests green</td></tr>
<tr><td>Read an SAE feature page as a protocol with missing fields?</td><td>Lesson 12’s practice</td></tr>
<tr><td>State the Gao–Cammarata disagreement in one paragraph, with what each would accept as evidence?</td><td>Lesson 13</td></tr>
<tr><td>Report a negative result at full resolution?</td><td>Your capstone, if it failed; lessons 06 and 08 if it did not</td></tr></table>
<h2 id="rubric">Capstone rubric</h2>
<table><tr><th>Criterion</th><th>Pass</th><th>Not yet</th></tr>
<tr><td>Procedure</td><td>The neuron’s selection is written such that a reader could repeat it and get the same neuron</td><td>“We picked an interesting neuron”</td></tr>
<tr><td>Pre-registration</td><td>All eight fields filled, dated, before the held-out score; the “looked?” field is honest</td><td>A field is blank, or the threshold was set after the run</td></tr>
<tr><td>Held-out data</td><td>Named, disjoint from screening, not decoded before scoring</td><td>Overlaps with the examples that suggested the claim</td></tr>
<tr><td>Score and base rate</td><td>Both reported; the score is on all held-out tokens or the regime is stated</td><td>A score without the data it was computed on</td></tr>
<tr><td>Controls</td><td>At least two, run as pre-registered, reported beside the score as percentiles</td><td>Controls missing, or reported as “low”</td></tr>
<tr><td>Verdict</td><td>Applies the pre-registered rule; the word “demonstrated” is used only if it passed</td><td>A failed threshold described as partial success</td></tr>
<tr><td>Not tested</td><td>A table of what the claim does not cover, written before the results discussion</td><td>Omitted, or buried in limitations</td></tr>
<tr><td>Exploratory</td><td>Anything learned after the run is labelled and separated</td><td>Post-hoc observations mixed with pre-registered ones</td></tr>
<tr><td>Wording</td><td>Correlational evidence is worded as “correlates” or “is readable”; “uses” only with an intervention</td><td>“The neuron is for X” from a correlation</td></tr>
<tr><td>Revised protocol</td><td>The next test is written and labelled not yet run</td><td>“Future work”</td></tr></table>
<h2 id="held-out-assessment">Held-out assessment</h2>
<p>A tutor has a set of variant tasks (described, not published, in <code>labs/ASSESSMENTS.md</code>) that change the rule, the corpus, the stimulus family, or the model layer, so that a learner who can only reproduce the reference runs will not pass and one who can run the protocol will. That is the same principle as this whole course applied to the course itself.</p>
<h2 id="next">After this course</h2>
<p>The methods here are the small end of the field. Nanda’s guide and ARENA’s Chapter 1 '''+cite('nanda')+''' '''+cite('arena')+''' take the same tools to circuits (indirect object identification), to superposition in toy models, and to training your own sparse autoencoders. The 2026 essay and its critique are the live argument; the companion paper the essay promises, and the post Gao promises, are the next things to read with the checklist from lesson 13 open. The vision replication you can extend today: add natural images with a clear licence, run the dataset-examples line of evidence the course could not, and test the paper’s purity claim. The language one you can extend tonight: the KL test in lesson 14.</p>
<div class="evals"><span class="label">In interpretability work</span><p>Everything in evals that you learned to do for a benchmark score (name the estimand, hold out, control, correct for multiple comparisons, report the negative) applies unchanged to a claim about a neuron. Interpretability is evaluation of explanations. You already had the habits; now you have the objects.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Finishing the course without a failed test of your own. If every pre-registration you wrote passed, your thresholds were too easy or your claims too safe. Lesson 08’s failure is the one to imitate: a strict line, missed for a reason you can name, reported in full.</p></div>''',
 'Your capstone passed every rubric row and your held-out r was 0.52, just over the 0.5 threshold. A reviewer asks whether 0.52 versus 0.50 means anything. What do you say?',
 'That the threshold was set in advance and the verdict follows it, so the result stands as “demonstrated at the pre-registered level,” and that the margin is small enough that a different held-out split could land on the other side: the right follow-up is a confidence interval on r from a bootstrap over held-out chunks (the statistics course’s tool), reported as exploratory, and a replication on new text as the next pre-registration. What you do not do is move the threshold or rerun until it clears comfortably.',
 lab(["python -m unittest discover -s labs -p 'test_*.py' -v"],
 'Run the full test-suite against your implementations. Then re-read your capstone report against the rubric, row by row, and mark each pass or not yet in the margin.',
 'Thirty-seven tests across six labs. If any fail, the failing test is the specification: read what it asks for, not what the reference does. The rubric rows most often marked “not yet” on a first pass are the not-tested table and the wording row.'), ['nanda','arena']),
]
