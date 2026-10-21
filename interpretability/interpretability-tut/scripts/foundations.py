from common import lesson, lab, cite

LESSONS = [
lesson(0,0,'orientation','A claim about a model’s internals is a hypothesis',
 'What it means to say a neuron, a direction, or a head “does” something, and what it would take to have shown it.',
 '''<h2 id="the-claim">Every explanation is a claim about the future</h2>
<p>“Neuron 2928 in layer 2 fires at the start of a sentence.” That sentence looks like a description. It is a prediction. It says that on text the neuron has never seen, its activation will be high on sentence-initial tokens and low elsewhere, and if that is not what happens, the sentence is false. The whole discipline of this course is in treating interpretability claims that way: as hypotheses that predict something, that could have come out otherwise, and that have not been demonstrated until they did come out that way on data chosen before anyone looked.</p>
<p>This is the same move you made in the <a href="../../../statistics/statistics-tut/index.html">statistics course</a> when you named the estimand before computing anything, and in the <a href="../../../evals/evals-tut/index.html">evals course</a> when you validated a grader on a held-out set. The objects are different. The habit is identical.</p>
<h2 id="why-now">Why this is the hard barrier</h2>
<p>The toolchain, the linear algebra, and the transformer anatomy are all learnable from documentation. Rigor is not, because the failure is invisible from inside. When you look at the ten inputs that most excite a unit, your eye finds the pattern, and the pattern feels like understanding. The feeling is real. The understanding may not be. In 2026 two researchers who worked on the same OpenAI neuron-explanation project disagreed in public about exactly this. Nick Cammarata’s essay opens: “I think I have good news about the nature of neural networks,” and argues that “a network’s own mechanisms are its legible building blocks” '''+cite('cammarata2026')+'''. Leo Gao’s reply two days later grants the observation and refuses the conclusion: “To be able to claim that we understand a neuron, it’s insufficient for things to look kinda nice. If you can’t simulate the neuron in a way that doesn’t degrade the model, you don’t really understand the neuron” '''+cite('gao2026')+'''.</p>
<p>Both are careful people. Both looked at the same kind of evidence. The disagreement is about what counts as demonstrated, and that is a question you can settle for yourself, on a laptop, with the methods in this course. The course does not take a side on how clean networks are. It takes a side on method: a test written before the look is worth more than any number of looks.</p>
<h2 id="demonstrated">What “demonstrated” means here</h2>
<p>A demonstrated explanation of a unit has four properties, and the rest of the course is a tour of how to get each one.</p>
<table><tr><th>Property</th><th>What it rules out</th><th>Lessons</th></tr>
<tr><td>It predicts behaviour on held-out data</td><td>Fitting a story to the examples that suggested it</td><td>01, 04</td></tr>
<tr><td>Its score was defined before the run</td><td>Choosing the metric that flatters the result</td><td>01, 05</td></tr>
<tr><td>It beats controls that an empty claim would pass</td><td>Scores that any unit or any rule would get</td><td>05, 07</td></tr>
<tr><td>Its failure would have been reported</td><td>The file drawer</td><td>13</td></tr></table>
<p>Notice what is not on the list. It does not say the explanation must be causal, or complete, or stated in natural language, or that the unit must be monosemantic. Those are stronger claims with their own tests (lessons 10 and 12). A claim can be modest and demonstrated, or ambitious and not. Modest and demonstrated is a contribution.</p>
<h2 id="two-models">Two models you can run</h2>
<p>Everything in the labs runs on a CPU in under two minutes per command. For vision, the model is torchvision’s GoogLeNet, the InceptionV1 architecture, loaded with its ImageNet weights '''+cite('torchvision')+'''. For language, it is GPT-2 small, 124 million parameters, loaded through TransformerLens so that every activation has a name. Lesson 06 will make an important point about the vision model: its weights are not the weights the Distill papers studied, so a unit number from a paper does not name the same unit here. That turned a planned replication into a different and better exercise.</p>
<div class="diagram">claim → prediction on unseen data → scoring function → controls → threshold
      → run → report (pass or fail) → what it does and does not establish</div>
<div class="evals"><span class="label">In interpretability work</span><p>When a colleague shows you a neuron and says what it does, your first question is not “is that right?” It is “what did you predict, on what data, and what would a random neuron have scored?” If there is no answer, there is no result yet; there is a lead.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Treating the strength of a pattern in top examples as evidence of its generality. The top examples were selected for being extreme; they are the one place a unit is guaranteed to look clean. Gao’s post describes a neuron whose strongest examples are dogs on bicycles, whose weaker ones are just dogs, and asks whether you can therefore conclude it is a dogs-on-bicycles neuron: “I argue we cannot” '''+cite('gao2026')+'''.</p></div>''',
 'A write-up says: “We found a neuron that detects dates. Its top 20 activations are all on year tokens like 1911 and 2007.” What has been shown, and what has not?',
 'Shown: on the inputs that most excite the neuron, year tokens dominate. Not shown: that year tokens generally excite it (recall), that non-year tokens do not (precision), that the neuron’s weaker activations follow the same rule, or that a random neuron scored against the same rule would not look similar. The claim is a hypothesis with a promising lead; lesson 04 turns it into a test.',
 lab([], 'Write down one claim you have read or heard about what some unit in some model does. Rewrite it as a prediction: on what data, what number, how large. Then write the control: what would also produce that number if the claim were empty?',
 'Most claims become much narrower when written as predictions, and that is the point. “Detects dates” might become “activation above 1.0 on at least 80% of four-digit year tokens in held-out text, and on fewer than 5% of other tokens.” The control is a random neuron of the same layer scored the same way.'), ['cammarata2026','gao2026','torchvision']),

lesson(1,0,'the-protocol','The protocol: write the test before you look',
 'The pre-registration template, field by field, and the lab that refuses to run until it is filled in.',
 '''<h2 id="order">The order of operations</h2>
<p>The protocol is one rule with consequences: decide how you will judge the claim before you see the evidence that will judge it. Written out, it has eight fields, and <a href="../appendices/a-protocol-template.html">Appendix A</a> keeps a copy. The lab <code>labs/protocol.py</code> encodes it as a <code>Preregistration</code> record whose <code>run()</code> raises <code>ProtocolError</code> if any field is blank or still says “TODO”, and whose <code>judge()</code> returns “demonstrated” only when the score meets the threshold and beats every control’s 95th percentile.</p>
<pre><code>CLAIM        one falsifiable sentence
UNIT         model, layer, hook point, index, and how it was chosen
HELD-OUT     the data the score is computed on, untouched by the choosing
SCORING      the function from claim and data to a number
PREDICTION   the number, as an inequality
THRESHOLD    the pass line, fixed now, justified by the control
CONTROLS     at least two; for each, what passing would mean
FAILURE      what you will write if it fails
LOOKED?      whether you have already seen the held-out data</code></pre>
<h2 id="fields">Each field, and the way it goes wrong</h2>
<p><strong>Claim.</strong> “Related to punctuation” cannot fail. “Fires on sentence-final punctuation and not on commas” can. Write the one that can.</p>
<p><strong>Unit and how it was chosen.</strong> If you searched 36,864 neurons for the one that best fits your rule, say so, because the search is where selection bias enters. The best of thirty-six thousand random correlations is not small. In lesson 04 the screening split absorbs that bias and the held-out split measures what is left.</p>
<p><strong>Held-out.</strong> Data that played no part in forming or choosing the claim. Not “other examples I also looked at.” The cleanest version is a split made before the investigation started, as the labs do with alternating 128-token chunks of the corpus. For vision (lesson 06) the held-out data are stimuli rendered with parameters the screening never used.</p>
<p><strong>Scoring.</strong> One function, named. Correlation between the rule’s predictions and the activations; F1 of the rule as a classifier of “fires”; recovered fraction of a logit difference; prefix-matching score. Each measures something different (lesson 04 compares them). Pick before you run, because after you run you will know which one looks best.</p>
<p><strong>Prediction and threshold.</strong> A number and a line. The line should be justified by what the control is expected to reach, with margin, not by what you hope the unit reaches. Lesson 08 shows a threshold that was badly chosen in exactly this way, and the test failed because of it. That failure is reported as a failure.</p>
<p><strong>Controls.</strong> A control is a comparison that would also pass if the claim were empty. Random unit, shuffled labels, baseline explanation, rotated stimulus, unrelated position. Lesson 05 is about what each one rules out. Two is the minimum because they rule out different things.</p>
<p><strong>Failure.</strong> Write the sentence now: “If r on held-out tokens is below 0.5, the rule is not a demonstrated explanation of this neuron, and we report r and both control percentiles.” Writing it now makes it much harder not to write it later.</p>
<p><strong>Looked?</strong> Honesty field. If you have already decoded the held-out chunks and seen where the neuron fires, the test is a post-hoc fit. It can still be informative; it is not a pre-registration.</p>
<h2 id="example">The protocol as code</h2>
<pre><code>from protocol import Preregistration, run, ProtocolError

p = Preregistration(
    claim='L2/2928 fires on the first token of a sentence',
    unit='gpt2 blocks.2.mlp.hook_post[:, 2928], chosen by screening on even chunks',
    heldout_data='odd 128-token chunks of labs/data/corpus.txt',
    scoring='Pearson r between rule indicator and activation',
    prediction='r >= 0.5', threshold=0.5,
    controls=['random_unit', 'shuffled_labels'],
    failure_means='not a demonstrated explanation; report r and control percentiles')

result = run(p, experiment)   # experiment() returns (score, {control: scores})
print(result['verdict'])      # 'demonstrated' or 'not demonstrated'</code></pre>
<p>The tests in <code>labs/test_protocol.py</code> check that an incomplete protocol is refused before the experiment function is even called, that the pre-registered controls must actually be reported, and that a control scoring as high as the claim defeats it even above threshold. Make them pass before lesson 04.</p>
<div class="evals"><span class="label">In interpretability work</span><p>Cammarata’s essay describes a test of this shape done at scale: for twenty Qwen3-32B neurons, “Reading only a neuron’s explanation, an agent wrote five new examples that should drive it and five near misses that shouldn’t,” and calls positive controls “one of many tools for criticizing an explanation of a neuron” '''+cite('cammarata2026')+'''. The structure is the protocol: predictions from the explanation alone, on inputs not yet seen. What the essay and Gao disagree about is whether that structure, applied to strong examples, is enough.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Pre-registering after a pilot on the same data. If you ran the rule on the held-out chunks “just to see,” then wrote the threshold, the chunks are no longer held out. Split again, or report it as exploratory.</p></div>''',
 'You screened 500 candidate units for the one most correlated with “token is a digit” and found r = 0.97 on the screening data. A teammate says the held-out test is a formality since 0.97 cannot be luck. Is it?',
 'The held-out test is not a formality, but not mainly because 0.97 could be luck on 500 draws (it cannot, at that sample size). It is because the screening score is the maximum over a search, so it is biased upward by an amount you do not know, and because the controls have not been run: the held-out test is also where you learn what a random unit scores against the same rule, and whether the rule’s score survives the shift to new text. Report the held-out number, not the screening one.',
 lab(["python -m unittest discover -s labs -p 'test_protocol.py' -v"],
 'Implement <code>labs/protocol.py</code> until its tests pass. Then fill in a protocol for a claim of your own about any GPT-2 neuron you have not yet looked at, and keep it for the capstone.',
 'The hardest test is usually the one that checks <code>judge()</code> against a control whose 95th percentile is above the score: your implementation must compare against the percentile, not the mean and not the single maximum. The protocol is only as strict as its weakest control.'), ['cammarata2026','gao2026']),

lesson(2,0,'the-objects','The objects: neurons, directions, heads, features',
 'What the things you make claims about actually are, how each is read out of a forward pass, and why “native neuron” and “learned feature” are different kinds of object.',
 '''<h2 id="neurons">Neurons</h2>
<p>A neuron is one coordinate of an activation vector at one point in the network. In GPT-2 small’s MLP, the hook <code>blocks.L.mlp.hook_post</code> has shape <code>[batch, position, 3072]</code>, and neuron <em>j</em> of layer <em>L</em> is column <em>j</em>, a scalar per token. In GoogLeNet, <code>inception3b</code> outputs <code>[batch, 480, 28, 28]</code>, and a “neuron” is one of the 480 channels, a scalar per spatial position; the labs read the centre of the map. In both cases the value is after the nonlinearity, so it is zero or positive for ReLU and can be slightly negative for GELU.</p>
<p>The <a href="../../../transformers/transformers-tut/index.html">transformer anatomy course</a> derived these shapes from the weights. Here the only thing that matters is that a neuron is a scalar function of the input, which is exactly what makes it testable: predict the scalar, compare.</p>
<h2 id="directions">Directions</h2>
<p>A direction is a unit vector in activation space, and projecting the residual stream onto it gives a scalar too. A neuron is the special case where the direction is a coordinate axis. A linear probe (lesson 08) is a direction learned from labels. A sparse-autoencoder feature (lesson 12) is a direction learned without labels. The <a href="../../../linear-algebra/linear-algebra-tut/index.html">linear algebra course</a> covered what a projection measures; the point for rigor is that a direction is also a hypothesis, and a learned direction is a hypothesis chosen by a search, so it needs the same held-out test as a neuron found by screening.</p>
<h2 id="heads">Attention heads</h2>
<p>A head is not a scalar. It is a pattern, <code>blocks.L.attn.hook_pattern</code> of shape <code>[batch, heads, query, key]</code>, with each query row summing to one, plus the information it moves along that pattern. Claims about heads are usually claims about the pattern under a constructed input (“attends to the token after the previous occurrence of the current token”) or about the effect of the moved information on the logits. Lesson 11 turns the first kind into a score; lesson 09 covers the second.</p>
<h2 id="features">Native neurons versus learned features</h2>
<p>Olah et al. define features as directions and say that in the circuits agenda they are “often simply individual neurons” '''+cite('zoomin')+'''. The same paper names the problem: “Neural networks often contain ‘polysemantic neurons’ that respond to multiple unrelated inputs,” with the example 4e:55, “a polysemantic neuron which responds to cat faces, fronts of cars, and cat legs,” and offers superposition, a circuit spreading a feature across many neurons, as the reason. Anthropic’s 2023 response was dictionary learning: train a sparse autoencoder to re-express a one-layer model’s 512-neuron MLP in a larger set of sparse directions, and report that “Sparse autoencoders produce interpretable features that are effectively invisible in the neuron basis” '''+cite('monosemantic')+'''.</p>
<p>The 2026 essay argues for going back: “This means we can study networks directly, instead of first untangling them,” and revisits the famous example, “The most famous polysemantic neuron is 4e:55 of InceptionV1, which looked like an arbitrary mixture of cats and cars,” concluding “it’s not a cat and car neuron, it’s a V-shape neuron” '''+cite('cammarata2026')+'''. Whether that reading is right is testable in the way this course tests things: does “V-shape” predict 4e:55’s activations on held-out images better than “cat or car” does? Gao’s reply says the old explanation would in fact have failed such a test, since it “would fail to fire on a ton of V shaped objects, and also it would falsely fire on a bunch of round dogs and cars” '''+cite('gao2026')+'''. Notice that both sides agree on the test; the course is about running it.</p>
<table><tr><th>Object</th><th>Read out as</th><th>Chosen by</th><th>Tested by</th></tr>
<tr><td>Native neuron</td><td>one coordinate after the nonlinearity</td><td>index, or a screening rule</td><td>held-out activation prediction</td></tr>
<tr><td>Probe direction</td><td>projection of the residual stream</td><td>supervised fit</td><td>held-out accuracy versus controls</td></tr>
<tr><td>SAE feature</td><td>sparse latent of a second model</td><td>unsupervised fit</td><td>the same as a neuron, plus reconstruction and downstream loss</td></tr>
<tr><td>Attention head</td><td>a pattern and an output</td><td>index</td><td>pattern score on constructed input; patching</td></tr></table>
<h2 id="reading">Reading activations with TransformerLens 4</h2>
<pre><code>from transformer_lens import TransformerBridge
model = TransformerBridge.boot_transformers("gpt2")
model.enable_compatibility_mode()          # restores the blocks.L.* hook names
toks = model.to_tokens("The capital of France is")
logits, cache = model.run_with_cache(toks)
cache["blocks.2.mlp.hook_post"].shape      # torch.Size([1, 6, 3072])
cache["blocks.5.attn.hook_pattern"].shape  # torch.Size([1, 12, 6, 6])</code></pre>
<p>Two practical notes from the authoring runs. <code>model.to_tokens</code> truncates to the 1,024-token context window, so the labs tokenise the corpus with <code>model.tokenizer</code> directly and chunk it themselves. And the booted model takes about twenty seconds to load on a CPU, so each reference script loads it once and does all its work in that process.</p>
<div class="evals"><span class="label">In interpretability work</span><p>Nanda’s guide lists the techniques you should be able to “code it up yourself on a simple model like GPT-2 Small” '''+cite('nanda')+''' and recommends TransformerLens for small models. The reason to own the code is rigor: a hook you wrote is a hook whose indexing you can check.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Reading a channel’s activation at the wrong place. GoogLeNet’s inception3b map is 28×28; the centre cell sees a receptive field around the image centre, so a stimulus drawn at the corner tests a different neuron-position pair. The labs draw every stimulus through the centre and read the central 2×2 cells.</p></div>''',
 'Someone reports that “direction d in layer 6, found by a probe, encodes sentence boundaries with 98.5% accuracy.” Which of the four objects is this, how was it chosen, and what does the choosing imply for the test?',
 'It is a learned direction, chosen by a supervised fit to labels. The fit searched all 768 dimensions for the combination that best predicts the labels, so accuracy on the fitting data is biased upward and only held-out accuracy counts. The base rate matters too: if 90% of tokens are non-boundaries, 98.5% must be compared with 90%, and with a probe fitted on shuffled labels. Lesson 08 runs exactly this and the pre-registered threshold fails.',
 lab(['python labs/reference/maxact.py --layer 2 --neuron 2928'],
 'Run the max-activating-examples script on neuron 2928 of layer 2 and read only the first block of output, the top ten. Write one sentence saying what the neuron does. Keep it; lesson 03 shows the rest of the output.',
 'Most readers write “fires at the start of a new paragraph” or “after a full stop.” Both are reasonable from the top ten. The quantile bands further down show how far each generalises.'), ['zoomin','monosemantic','cammarata2026','gao2026','nanda']),
]
