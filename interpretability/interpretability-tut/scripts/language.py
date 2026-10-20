from common import lesson, lab, cite, transcript

LESSONS = [
lesson(8,3,'linear-probes','Language I: linear probes, with a threshold that failed',
 'A logistic probe on GPT-2 residual activations with a held-out split, a shuffled-label control, and a random-direction control. The pre-registered test fails, and the reason is instructive.',
 '''<h2 id="what-a-probe-is">What a probe claims</h2>
<p>A linear probe is a classifier fitted on activations to predict a label. If it reaches high accuracy on held-out tokens, the label is linearly readable from the residual stream at that layer. That is the whole claim. It does not say the model uses the direction, that the direction is a single feature, or that anything would change if you removed it; lesson 10 is about those. The probe’s value is that it is cheap and its test is exactly the held-out-accuracy test you already know from the <a href="../../../evals/evals-tut/index.html">evals course</a>.</p>
<p>The reference script fits logistic regression in numpy (no sklearn in the environment, and none needed) on <code>blocks.6.hook_resid_post</code>, 768 dimensions, standardised, 300 gradient steps with a small L2 penalty. The label is the same sentence-start rule as the neuron in lesson 04. Pre-registered: at layer 6, held-out accuracy at least 10 percentage points above the majority rate and above both controls.</p>
'''+transcript('''layer 6, label "after_period": train 1664 tokens (0.090 positive), held-out 1536 tokens (0.103 positive); majority-class accuracy 0.897
probe: train accuracy 0.999, held-out accuracy 0.985
shuffled-label control (20 fits): held-out accuracy mean 0.834, max 0.861
random-direction control (20 directions): held-out accuracy mean 0.882, max 0.894
pre-registered test (held-out >= majority + 0.10 and above both controls): FAIL
exploratory, NOT pre-registered: held-out recall on positives 0.930, on negatives 0.991, balanced accuracy 0.961; the largest gain over majority that any probe could reach here is 0.103''')+'''
<h2 id="why-it-failed">Why the test failed</h2>
<p>The probe is good: 98.5% held-out, 93% recall on the 10% of tokens that are sentence starts, far above a shuffled-label fit (max 86.1%) and a random direction (max 89.4%). The test failed because the threshold was wrong. With a majority rate of 89.7%, a gain of 10 percentage points requires 99.7% accuracy; the most any probe could gain is 10.3 points. The threshold was written as if the base rate were 50%, which it is not. The author of the threshold (the course) did not compute the base rate on the held-out split before fixing the line.</p>
<p>This is reported as a failure because it is one. The protocol says what to do: the pre-registered result stands, the exploratory numbers are labelled exploratory, and the next pre-registration fixes the threshold properly. Three ways to do that: state the threshold as a fraction of the achievable gain (“recover at least 80% of the gap between majority and 100%”); use balanced accuracy, which has a majority rate of 50% by construction; or pre-register precision and recall at a fixed operating point. Any of the three would have passed here. None of them was written down, so none of them counts.</p>
<h2 id="controls">What the two controls ruled out</h2>
<p>The shuffled-label control refits the probe on permuted labels and scores it on the real held-out labels. Its mean of 83.4% is <em>below</em> the majority rate, which tells you something about the probe: with meaningless labels, the fit learns noise and predicts the positive class more often than it should. A probe fit on real labels that scored near 83% would be indistinguishable from this; 98.5% is not.</p>
<p>The random-direction control projects the activations onto a random unit vector, picks the best threshold on the training split, and scores held-out. It reaches 89.4% at best, essentially the majority rate. The point of this control is specific: it rules out the possibility that any direction, with a tuned threshold, reaches the probe’s accuracy because the label is trivially separable (for instance if the activations had a huge norm difference on positives). They do not; the probe found a particular direction.</p>
<h2 id="layer">Why layer 6, and what to do with layers</h2>
<p>The sentence-start label is computable from the previous token alone, so a layer-0 probe would likely do about as well, and this is the kind of fact that a layer sweep reveals and a single layer hides. The reference script takes <code>--layer</code>; the practice below asks you to run it at 0 and 11. A probe’s accuracy as a function of layer is a description of where a label is readable, which is a more useful object than a single number, and a sweep is also a place where you can fool yourself by reporting the best layer: pre-register the layer, or report all of them.</p>
<h2 id="lab">The lab</h2>
<p><code>labs/probe.py</code> asks for the fit, the prediction, the majority rate, the two controls, and a <code>verdict</code> that takes the margin as a parameter. The tests use synthetic data with a hidden direction and 15% positives; the shuffled control must fall to about the majority rate, the random-direction control must stay below the probe, and a dataset with no signal must not pass.</p>
<div class="evals"><span class="label">In interpretability work</span><p>Before fixing a probe threshold, print the majority rate on the held-out split and the maximum achievable gain. Then write the threshold as a fraction of that gain. The failed test above cost nothing but a paragraph; in a paper it would have cost the result.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Reading probe accuracy as evidence that the model “knows” or “uses” the property. Huang et al. put the distinction as observational versus intervention modes: “The observational mode only evaluates whether a concept is encoded, as opposed to used” '''+cite('huang2023')+'''. A probe is observational.</p></div>''',
 'A probe for “token is inside a quotation” reaches 96% held-out at layer 8 and 95% at layer 0. The author reports layer 8 as where the model represents quotation state. What is wrong?',
 'The one-point difference between layers is within what a shuffled-label control would need to be compared against, and layer 0 is nearly the embedding, which cannot represent context, so most of the 95% is coming from token identity (quote marks and the words that follow them) rather than quotation state. The right analysis reports all layers, compares each against its controls, and uses a label that cannot be read from the current token alone. If layer 8 is not clearly above layer 0 after that, the claim about representation has not been made.',
 lab(['python labs/reference/probe_run.py --layer 6','python labs/reference/probe_run.py --layer 0','python labs/reference/probe_run.py --layer 11',"python -m unittest discover -s labs -p 'test_probe.py' -v"],
 'Run the probe at layers 0 and 11 and compare with layer 6. Then implement <code>labs/probe.py</code>. Finally, rewrite the lesson’s failed pre-registration with a threshold that respects the base rate and say what it would have concluded.',
 'If layer 0 is close to layer 6, the label is mostly token-local and the probe says little about layer 6 in particular. A threshold like “balanced accuracy ≥ 0.90 and above both controls” would have passed with 0.961; write that in the protocol notes as the revised, and now pre-registered, test for your own next run.'), ['huang2023','nanda']),

lesson(9,3,'logit-lens','Language II: the logit lens and direct logit attribution',
 'Reading intermediate residual states as if they were final, decomposing a logit into component contributions, and the known ways each one misleads.',
 '''<h2 id="lens">The logit lens</h2>
<p>nostalgebraist’s 2020 observation: “GPT's probabilistic predictions are a linear function of the activations in its final layer. If one applies the same function to the activations of intermediate GPT layers, the resulting distributions make intuitive sense” '''+cite('logitlens')+'''. Apply the final layer norm and the unembedding to <code>blocks.L.hook_resid_post</code> and you get, for each layer, the distribution the model would output if that layer were the last. The post’s summary: “At some point in the middle, GPT will have formed a ‘pretty good guess’ as to the next token, and the later layers seem to be refining these guesses in light of one another.”</p>
<p>The reference script runs it on “The capital of France is” and reports the top token, its probability, the probability of “ Paris”, and the KL divergence from the layer’s distribution to the final one:</p>
'''+transcript('''prompt 'The capital of France is'; final top token ' now', target ' Paris' rank 93

   after      top token  p(top) p(target) KL to final
 block 0         ' not'   0.384     0.000       3.244
 block 1         ' now'   0.337     0.000       4.099
 block 2         ' now'   0.471     0.000       4.170
 block 3         ' now'   0.558     0.000       4.159
 block 4         ' now'   0.653     0.000       3.950
 block 5         ' now'   0.672     0.000       4.805
 block 6         ' now'   0.550     0.000       3.373
 block 7         ' now'   0.741     0.000       3.811
 block 8         ' now'   0.574     0.000       2.637
 block 9         ' now'   0.333     0.005       1.491
block 10         ' now'   0.204     0.002       0.318
block 11         ' now'   0.048     0.002       0.000''')+'''
<p>First, the model. GPT-2 small does not answer this prompt with “ Paris”; its top token is “ now” and Paris is ranked 93rd. That is a fact about a 124M-parameter model and the course reports it rather than choosing a prompt that works. Second, the lens. The intermediate distributions are confidently wrong in a way the final one is not: block 7 puts 74% on “ now”, the final layer 5%. The KL to the final distribution falls from about 4 to 0.3 over the last three blocks, which is where the lens says the output is formed. The “pretty good guess” pattern the post describes for GPT-2 XL is not what this prompt shows for GPT-2 small; what it shows is a prediction that the last three layers mostly dismantle.</p>
<h2 id="failure-modes">What the lens cannot tell you</h2>
<p>The post’s own caveat: “The logit lens show us some of what is going on, not all of it.” Three specific failure modes.</p>
<p><strong>The unembedding is not the right reader for early layers.</strong> The lens assumes each layer’s residual state is in the final layer’s coordinates. Early layers write features the later layers transform before unembedding; applying the final map to them reads those features through the wrong lens, and the confident “ now” at block 7 may be a feature that later layers use for something else entirely. A low lens probability for the right answer at layer 4 does not mean the answer is absent at layer 4.</p>
<p><strong>KL is not a distance.</strong> The post added this after a comment: “The KL divergence is not a metric: it is not symmetric and does not obey the triangle inequality,” so the picture of the state “travelling” from input to output along a path is a metaphor, and KL(final‖layer) and KL(layer‖final) tell different stories.</p>
<p><strong>It is a look, not a test.</strong> Nothing about the lens is pre-registered. It is a way of generating hypotheses (“block 9 is where the model starts to move toward the answer”), and lesson 10 is how such a hypothesis is tested: patch block 9 and see whether the answer moves.</p>
<h2 id="dla">Direct logit attribution</h2>
<p>The residual stream is a sum: embeddings plus every block’s attention output plus every block’s MLP output. The final logit of a token is a linear function of that sum through the final layer norm, and layer-norm centring is linear, so the logit decomposes exactly into one term per component. Each term is ((c − mean(c)) · w / scale) · u, where c is the component’s output at the last position, w and scale are the final layer norm’s weight and the normalisation scale actually used on this input, and u is the target token’s column of the unembedding. The biases of the layer norm and unembedding make one more term. The script checks that the terms add up:</p>
'''+transcript('''Direct logit attribution to ' Paris' (each part passed through the final layer norm):
  block  0: attention   -0.04   mlp   -0.05
  block  1: attention   +0.07   mlp   -0.04
  block  2: attention   +0.09   mlp   -0.05
  block  3: attention   +0.05   mlp   +0.15
  block  4: attention   +0.14   mlp   +0.24
  block  5: attention   +0.15   mlp   -0.17
  block  6: attention   +0.48   mlp   +0.39
  block  7: attention   +0.21   mlp   +0.11
  block  8: attention   +0.29   mlp   +0.81
  block  9: attention   +1.90   mlp   +0.72
  block 10: attention   +0.48   mlp   +0.56
  block 11: attention   +0.90   mlp   +2.07
  embeddings   -0.01; layer-norm and unembed biases   +1.59
  sum of parts  +11.02; logit from the forward pass  +11.02''')+'''
<p>The sum matches the forward pass to two decimals, which is the first thing to check whenever you write attribution code; an earlier version of this script omitted the centring and the biases and was off by 1.6. Block 9’s attention (+1.90) and block 11’s MLP (+2.07) contribute most to the Paris logit. That is consistent with the lens table, where Paris first gets measurable probability after block 9. It is still correlational: a large direct contribution says the component writes in the Paris direction, not that the model’s answer depends on it, and the Paris logit here is a losing logit.</p>
<h2 id="limits-of-dla">What attribution misses</h2>
<p>Direct logit attribution measures only the direct path from a component to the output. A component whose output is read by a later block and transformed before reaching the logits contributes indirectly, and that contribution is assigned to the later block. For an answer that depends on composition (attention moving the country name, an MLP converting it to a capital), the attribution lands on the last step. The “found it in block 11” result is therefore often an artefact of where the direct path ends. Patching (lesson 10) follows the indirect paths; attribution does not.</p>
<div class="evals"><span class="label">In interpretability work</span><p>Use the lens and attribution to choose which layer and position to patch, then patch. Report lens tables as what they are: the output you would get if the model stopped early, which it does not.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Choosing the prompt after seeing which prompts the lens tells a clean story on. GPT-2 small fails the France prompt; the course keeps it. A clean story selected from twenty prompts is a top-k example of a different kind.</p></div>''',
 'The lens shows “ Paris” rising from rank 93 at block 11 to rank 1 at block 11 on a different prompt where the model is right. A colleague says block 9’s attention “retrieves the capital.” What two further results would you want before agreeing?',
 'First, that the +1.90 direct contribution survives patching: replace block 9’s attention output at the last position with its value from a corrupted prompt and see whether the answer degrades (lesson 10). Second, that the contribution is specific: direct attribution on a control prompt with a different country should move to that country’s capital, and attribution to a random token should be small. Without those, “retrieves” is a description of a projection, not a mechanism.',
 lab(['python labs/reference/logit_lens_run.py','python labs/reference/logit_lens_run.py --prompt "The capital of Italy is" --target " Rome"'],
 'Run the lens on the Italy prompt. Compare the rank of “ Rome” with that of “ Paris” on the France prompt, and compare which blocks carry the largest direct attributions.',
 'Whatever the ranks are, the comparison is what matters: if the same blocks dominate for both targets, the mechanism is at least prompt-general; if they differ, you have a hypothesis for a patching experiment. Resist reading either run alone as “where the model knows capitals.”'), ['logitlens']),

lesson(10,3,'causal-interventions','Causal interventions: activation patching with a clean/corrupted pair',
 'Correlational evidence says a component carries information; interventional evidence says the model uses it. Patching the residual stream of GPT-2 small, with a pre-registered claim and a control position.',
 '''<h2 id="the-distinction">Represents versus uses</h2>
<p>Everything so far has been correlational: a neuron’s activation co-varies with a rule, a probe reads a label, a component’s output projects onto a token. Huang et al. frame the gap as two modes: the observational mode “only evaluates whether a concept is encoded, as opposed to used,” and the intervention mode construes an explanation E of neuron a “as a claim that the neuron a is a causal mediator of the concept denoted by E” '''+cite('huang2023')+'''. Their audit of GPT-4’s explanations of GPT-2 XL neurons found that in the intervention mode, “we are unable to find evidence that neurons are causal mediators of the concepts denoted by the explanations.” Explanations that scored well observationally did not, in their tests, correspond to neurons the model relied on.</p>
<p>Activation patching is the basic interventional tool. Take two inputs that differ in one respect the claim is about: a clean prompt that produces the behaviour and a corrupted one that does not. Run the corrupted prompt, but at one layer and one position replace the activation with its value from the clean run. If the behaviour comes back, the information the claim is about passed through that activation.</p>
<h2 id="the-run">The run</h2>
<p>Clean: “The capital of France is”; corrupted: “The capital of Italy is”. Metric: logit(“ Paris”) − logit(“ Rome”) at the last position, which is +1.405 on the clean prompt and −4.417 on the corrupted one (the model prefers neither capital as its top token, as lesson 09 showed, but it does prefer the right one of the two). Patched residual stream, <code>blocks.L.hook_resid_post</code>, every layer, every position. Reported as the fraction of the clean-minus-corrupted gap recovered.</p>
<p>Pre-registered: patching at the country token’s position recovers more than 50% of the gap at some layer; patching at position 0, the token “The”, which carries no information about which country, recovers less than 10% at every layer.</p>
'''+transcript('''tokens: ['<|endoftext|>', 'The', ' capital', ' of', ' France', ' is']
metric logit(Paris)-logit(Rome): clean +1.405, corrupted -4.417
layer     pos0     pos1     pos2     pos3     pos4     pos5   (recovered fraction)
    0     0.00     0.00     0.00     0.00     1.00    -0.01
    1     0.00     0.00     0.00     0.00     1.00    -0.00
    2     0.00     0.00     0.00     0.00     1.00    -0.00
    3     0.00     0.00     0.00     0.00     0.99     0.00
    4     0.00     0.00     0.00     0.00     1.01     0.03
    5     0.00     0.00     0.00     0.00     1.00     0.03
    6     0.00     0.00     0.00     0.00     0.98     0.08
    7     0.00     0.00     0.00     0.00     0.98     0.08
    8     0.00     0.00     0.00     0.00     0.87     0.15
    9     0.00     0.00     0.00     0.00     0.29     0.70
   10     0.00     0.00     0.00     0.00     0.12     0.85
   11     0.00     0.00     0.00     0.00     0.00     1.00

country position (index 4): best recovery 1.01 -> pass (> 0.50 pre-registered)
position 0 control: largest recovery 0.00 -> pass (< 0.10 pre-registered)''')+'''
<p>Read the two columns that move. At the country position (index 4, “ France”), patching any layer from 0 to 7 recovers essentially the whole gap, which says the country identity sits at that position in the residual stream through those layers. From layer 8 the recovery at position 4 falls and the recovery at the final position rises; by layer 11 patching the final position alone recovers everything. The information moves from the country token to the final token between layers 8 and 10, which is where attention must be carrying it. Lesson 09’s attribution put the largest attention contribution at block 9; patching makes that a causal statement rather than a projection.</p>
<p>The control column (position 0) is 0.00 at every layer, as pre-registered. Positions 1 to 3 (“The capital of”) are also zero, which was not pre-registered but is what the claim predicts.</p>
<h2 id="what-patching-shows">What this does and does not establish</h2>
<p>It establishes that the residual stream at the country position, up to layer 7, is sufficient to switch the model’s preference between Paris and Rome, and that by layer 11 the final position is sufficient. It does not establish which heads move the information (patch <code>hook_z</code> per head to find out), which MLPs convert country to capital (patch MLP outputs), or that the same structure holds for other country pairs (run them). It establishes nothing about why GPT-2 small’s top token is “ now”. A patching table is a map of where a difference travels, for one pair of prompts.</p>
<h2 id="pairs">Choosing the pair</h2>
<p>The clean/corrupted pair defines what “the information” means. France/Italy differ in the country and therefore the capital; they match in length, syntax, and every other token, so the only thing the patch can carry is the country. A pair that also differed in length, or in the determiner, would let the patch carry those too, and the recovery would be uninterpretable. The reference script asserts the two prompts tokenise to the same length, because a position-wise patch between different lengths is meaningless.</p>
<h2 id="lab">The lab</h2>
<p><code>labs/patching.py</code> asks for the model-free parts: <code>recovered_fraction</code>, a <code>make_patch_hook</code> that overwrites exactly one position in place and returns the tensor, and the <code>verdict</code> with claim and control positions. The tests check that the hook leaves every other position untouched and that the recovery metric is zero when the patch does nothing and one when it restores the clean metric.</p>
<div class="evals"><span class="label">In interpretability work</span><p>Interventional evidence is the standard for “uses.” Olsson et al. list direct ablation among their six arguments and are careful about its reach: “When we directly ‘knock out’ induction heads at test-time in small models, the amount of in-context learning greatly decreases” '''+cite('olsson2022')+''', with “in small models” doing real work in that sentence.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Patching with a corrupted input that is noise rather than a matched prompt. Replacing an activation with zeros or Gaussian noise takes the model off-distribution, and the recovery you measure is partly recovery from the damage. A matched corrupted prompt keeps every activation in distribution.</p></div>''',
 'Patching layer 3 at the country position recovers 99% of the gap. A colleague says “layer 3 computes the capital.” What does the table actually show about layer 3?',
 'It shows that the residual stream at the country position after layer 3 contains whatever distinguishes France from Italy as far as the capital decision needs, which is also true after layer 0 (recovery 1.00). The country token’s embedding already carries that distinction; layers 0 to 7 preserve it at that position. The conversion to a capital happens somewhere the patch at position 4 stops working and the patch at position 5 starts, layers 8 to 10, and even that is a statement about where information moves, not what computes it.',
 lab(['python labs/reference/patch_run.py',"python -m unittest discover -s labs -p 'test_patching.py' -v"],
 'Run the patching table, then implement <code>labs/patching.py</code>. Then change the pair to Spain/Portugal (Madrid/Lisbon), pre-register the same two predictions, and run.',
 'The pair must tokenise to the same length or the script will refuse. Before running, write what you expect the position-4 column to look like; if the structure differs from France/Italy, you have found that the mechanism is pair-specific, which is a result.'), ['huang2023','olsson2022']),

lesson(11,3,'induction-heads','Attention heads: induction heads by a pre-registered test on repeated random tokens',
 'A behavioural definition that fixes its own test data, the prefix-matching score, a non-repeated control, and what GPT-2 small’s heads do on it.',
 '''<h2 id="definition">A definition that is a test</h2>
<p>Olsson et al. define induction heads behaviourally, on constructed input: “induction heads are any heads that empirically increase the likelihood of [B] given [A][B]...[A] when shown a repeated sequence of completely random tokens,” with two properties. “Prefix matching: The head attends back to previous tokens that were followed by the current and/or recent tokens.” “Copying: The head’s output increases the logit corresponding to the attended-to token” '''+cite('olsson2022')+'''. They explain why the sequence is random: “By defining induction heads in terms of their behavior on repeated copies of random sequences, we can be confident that it's actually relying on induction rather than, say, a simple copying head.” Random tokens have no n-gram statistics to exploit; the only way to predict the second copy is to look back.</p>
<p>This is a definition that comes with its own held-out data: every new random seed is a fresh test. The course tests the prefix-matching property. Build BOS + R + R where R is 50 random tokens; for each position in the second copy, read the head’s attention to the position just after that token’s first occurrence; average. A head doing pure induction scores 1; a head attending uniformly over 100 positions scores about 0.01.</p>
<p>Pre-registered: at least one head in GPT-2 small scores at least 0.5 (the paper reports “a continuum” and sets no numeric threshold, so 0.5 is the course’s own line); every such head scores below 0.1 on a control sequence BOS + R + R′ with a fresh second block, where there is nothing to match; and the loss on the second copy is lower than on the first, which is the in-context learning the paper ties to these heads.</p>
'''+transcript('''5 random sequences of 50 tokens, repeated once. Loss per token: first copy 12.38, second copy 0.43

prefix-matching score, repeated sequence (rows: layers, columns: heads):
  L0  0.01 0.00 0.01 0.00 0.00 0.00 0.01 0.00 0.01 0.01 0.01 0.01
  L1  0.00 0.00 0.00 0.00 0.00 0.01 0.01 0.01 0.01 0.01 0.01 0.00
  L2  0.00 0.02 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00
  L3  0.00 0.00 0.00 0.00 0.01 0.00 0.00 0.00 0.00 0.00 0.00 0.00
  L4  0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.01 0.00 0.00 0.00
  L5  0.46 0.91 0.00 0.00 0.00 0.95 0.00 0.00 0.01 0.02 0.02 0.00
  L6  0.00 0.00 0.01 0.00 0.02 0.00 0.02 0.00 0.00 0.92 0.03 0.00
  L7  0.00 0.22 0.84 0.00 0.00 0.00 0.04 0.10 0.00 0.00 0.91 0.05
  L8  0.00 0.39 0.01 0.03 0.00 0.00 0.17 0.00 0.01 0.02 0.06 0.01
  L9  0.26 0.17 0.11 0.00 0.08 0.01 0.51 0.02 0.05 0.46 0.00 0.04
  L10 0.39 0.54 0.04 0.15 0.05 0.00 0.33 0.53 0.04 0.00 0.19 0.26
  L11 0.02 0.05 0.03 0.00 0.03 0.10 0.05 0.06 0.01 0.33 0.44 0.01

heads with score >= 0.5: [(5, 1), (5, 5), (6, 9), (7, 2), (7, 10), (9, 6), (10, 1), (10, 7)]
same heads on the non-repeated control sequence:
  L5H1: repeated 0.91, control 0.00
  L5H5: repeated 0.95, control 0.00
  L6H9: repeated 0.92, control 0.00
  L7H2: repeated 0.84, control 0.00
  L7H10: repeated 0.91, control 0.00
  L9H6: repeated 0.51, control 0.00
  L10H1: repeated 0.54, control 0.01
  L10H7: repeated 0.53, control 0.00
pre-registered test: pass''')+'''
<h2 id="reading">Reading the grid</h2>
<p>Layers 0 to 4 are flat: no head in the first five layers attends to the induction target more than 2% of the time. Then five heads in layers 5 to 7 score above 0.84, and a looser group in layers 9 and 10 sits around 0.5. The paper’s “continuum” is visible: the scores are not two clusters but a tail, and the threshold at 0.5 cuts it at a place the course chose. Had it been 0.8, five heads; at 0.3, fourteen. Report the grid, not just the list, so a reader can move the line.</p>
<p>The control column is the result’s backbone. Every head that scores high on the repeat scores 0.00 or 0.01 on the control, where the second block is fresh random tokens and the “induction target” position holds nothing related. The heads are not attending to a fixed offset of 49; they are attending to a match. And the loss falls from 12.38 nats per token on the first copy, which is chance on a 50,257-token vocabulary with random tokens, to 0.43 on the second: the model predicts the repeat almost perfectly, which is what the heads are for.</p>
<p>The copying property was not tested. It needs the head’s output projected onto the attended token’s unembedding, a direct-logit-attribution per head of the kind lesson 09 built. It is the natural extension and the lab leaves it as practice.</p>
<h2 id="why-this-is-rigorous">Why this is the cleanest test in the course</h2>
<p>Everything about it was fixed by the definition before anyone looked at a head: the stimulus, the score, the control, the prediction. There was no screening step, so no selection bias; all 144 heads were scored and all 144 are shown. There is no corpus, so no question of distribution shift within the data. New seeds are free. The 2022 paper is a model of making a claim testable by writing the test into the definition, and that is why the ARENA curriculum uses locating induction heads with TransformerLens as its first interpretability exercise '''+cite('arena')+'''.</p>
<h2 id="lab">The lab</h2>
<p><code>labs/induction.py</code> asks for <code>repeated_sequence</code>, <code>control_sequence</code> (same first block, fresh second block), <code>prefix_matching_score</code> over an attention pattern of shape <code>[heads, pos, pos]</code>, and the <code>verdict</code>. The tests build a synthetic pattern where head 0 attends exactly to the induction target and head 1 attends uniformly, and check the scores are 1 and about 0.05; they also check that a head which scores high on the control fails the verdict.</p>
<div class="evals"><span class="label">In interpretability work</span><p>When a claim comes with a behavioural definition on constructed input, you have been handed a pre-registration. Use it exactly, then vary one thing at a time (sequence length, vocabulary range, number of repeats) and report what breaks.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Scoring attention to the induction target without the control. A head that always attends to position i − 49 for some unrelated reason would score high on the repeat; only the control, where i − 49 holds an unrelated token, distinguishes it. In this run no such head existed, but the control is what lets you say so.</p></div>''',
 'A head scores 0.55 on the repeated sequence and 0.40 on the control. Is it an induction head?',
 'By the pre-registered test, no: the control line was 0.1. A head attending 40% to a fixed offset regardless of content is doing something positional, and the extra 15% on the repeat may be a small induction component or noise across five seeds. Report it as a positional head with a possible weak induction component, run more seeds, and if the gap is stable, test the copying property to see whether the attended token’s logit actually rises.',
 lab(['python labs/reference/induction_run.py',"python -m unittest discover -s labs -p 'test_induction.py' -v"],
 'Run the detector, implement <code>labs/induction.py</code>, then add the copying score: for each high-scoring head, project its output at each second-copy position onto the unembedding of the attended token, through the final layer norm as in lesson 09, and report the mean.',
 'The copying score should be positive for the strong layer-5 to layer-7 heads. If it is near zero for a head with a high prefix-matching score, that head attends to the right place but does not write the token: by the paper’s definition it is not an induction head, and your detector just became stricter than the course’s.'), ['olsson2022','arena']),
]
