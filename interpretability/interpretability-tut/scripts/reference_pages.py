from common import cite

REFERENCES = [
 dict(path='appendices/a-protocol-template.html',title='The pre-registration template',kicker='Appendix A',n='A',kw='template protocol preregistration checklist prediction test controls threshold',
 lede='Fill this in before you look at the unit. Every field has a reason; a blank field is a hole a reviewer will find.',
 body='''<h2 id="template">The template</h2>
<p>Copy the block below into your notes (or fill a <code>Preregistration</code> from <code>labs/protocol.py</code>, whose <code>run()</code> refuses to execute while any field is a placeholder). Date it. Do not edit it after the run; append instead.</p>
<pre><code>CLAIM        What the unit does, in one sentence a sceptic could falsify.
UNIT         Model, layer, hook point, index. One unit, or a named family and the rule that picked it.
HELD-OUT     Which data the score will be computed on, and why that data played no part in choosing the claim.
SCORING      The function that turns the claim into a number on that data (correlation, F1, recovered fraction, prefix-matching score).
PREDICTION   The number the claim predicts, as an inequality.
THRESHOLD    The pass line. Fixed now. Justified by what the control is expected to reach, not by what you hope to see.
CONTROLS     At least two. For each: what it would show if it passed too.
FAILURE      What you will conclude, and write up, if the test fails.
LOOKED?      Have you already seen the unit's activations on the held-out data? If yes, this is not a pre-registration.</code></pre>
<h2 id="worked">A filled example from this course</h2>
<pre><code>CLAIM        GPT-2 small MLP neuron L2/2928 fires on the first token of a sentence.
UNIT         gpt2 (124M), blocks.2.mlp.hook_post[:, 2928], chosen by exhaustive screening on the screening split only.
HELD-OUT     The odd 128-token chunks of labs/data/corpus.txt (12 chunks, 1,536 tokens). Screening used only the even chunks.
SCORING      Pearson r between the rule indicator (previous token ends with "." or contains a newline) and the activation.
PREDICTION   r >= 0.5 on the held-out chunks.
THRESHOLD    0.5, and r must exceed the 95th percentile of 200 random same-layer neurons and of 500 label shuffles.
CONTROLS     random neuron (same layer): shows how much of the score the rule gets from any neuron;
             shuffled labels: shows what a meaningless rule scores on this neuron.
FAILURE      The rule is not a demonstrated explanation of L2/2928; report the held-out r and both control percentiles anyway.
LOOKED?      No: the held-out chunks were not decoded or inspected before scoring.</code></pre>
<h2 id="why">Why each field exists</h2>
<table><tr><th>Field</th><th>The mistake it prevents</th></tr>
<tr><td>Held-out</td><td>Scoring on the examples that suggested the claim, which selection bias inflates.</td></tr>
<tr><td>Scoring</td><td>Choosing the metric that happens to look best after the run.</td></tr>
<tr><td>Prediction</td><td>Claims that cannot fail: “the neuron is related to punctuation.”</td></tr>
<tr><td>Threshold</td><td>Moving the pass line to wherever the result landed.</td></tr>
<tr><td>Controls</td><td>A score that any unit, or any rule, would have reached.</td></tr>
<tr><td>Failure</td><td>Quietly not writing up the negative result.</td></tr>
<tr><td>Looked?</td><td>Calling a post-hoc fit a prediction.</td></tr></table>
<p>The same fields apply to vision stimuli (lesson 06), probes (08), patching (10), and heads (11); the <a href="../pages/01-the-protocol.html">protocol lesson</a> walks through filling them.</p>'''),
 dict(path='appendices/b-command-reference.html',title='Command reference',kicker='Appendix B',n='B',kw='commands reference scripts labs run',
 lede='Every command on these pages, what it runs, and roughly how long it takes on a four-core CPU. Outputs are in the transcript.',
 body='''<h2 id="setup">Environment</h2>
<p>The labs need torch (CPU), torchvision, transformers, transformer_lens 4, and numpy, with GPT-2 small in the Hugging Face cache and torchvision’s GoogLeNet weights in the torch hub cache. Run everything from the course directory with <code>HF_HUB_OFFLINE=1</code> once the models are cached. <code>python</code> on these pages means that environment’s interpreter; the versions actually used are at the top of <a href="../research/verify/lab-transcript.txt">the transcript</a>.</p>
<h2 id="commands">Commands</h2>
<table><tr><th>Command</th><th>Lesson</th><th>What it does</th><th>Time</th></tr>
<tr><td><code>python labs/reference/curve_tuning.py</code></td><td>06, 07</td><td>Screens inception3b with dark arcs, then tests the top 12 channels on held-out stimuli with 100 random-channel controls</td><td>~80 s</td></tr>
<tr><td><code>python labs/reference/curve_tuning.py --units 379,…</code></td><td>06</td><td>Tests the Distill unit numbers directly (expected not to transfer)</td><td>~80 s</td></tr>
<tr><td><code>python labs/reference/feature_vis.py --unit 177 --out …</code></td><td>06</td><td>Gradient-ascent feature visualisation of one channel in plain torch</td><td>~25 s</td></tr>
<tr><td><code>python labs/reference/maxact.py --layer 2 --neuron 2928</code></td><td>03</td><td>Top-k activations versus random draws from activation quantile bands</td><td>~30 s</td></tr>
<tr><td><code>python labs/reference/neuron_score.py --rule digit</code></td><td>04</td><td>Screens all 36,864 MLP neurons for one rule on the screening split, scores the winner on held-out tokens with both controls</td><td>~60 s</td></tr>
<tr><td><code>python labs/reference/neuron_score.py --all</code></td><td>05, 14</td><td>The same for all eight rules</td><td>~70 s</td></tr>
<tr><td><code>python labs/reference/probe_run.py --layer 6</code></td><td>08</td><td>Logistic probe on hook_resid_post with shuffled-label and random-direction controls</td><td>~40 s</td></tr>
<tr><td><code>python labs/reference/logit_lens_run.py</code></td><td>09</td><td>Logit lens per block and direct logit attribution for one prompt</td><td>~25 s</td></tr>
<tr><td><code>python labs/reference/patch_run.py</code></td><td>10</td><td>Residual-stream patching over every layer and position for a clean/corrupted pair</td><td>~40 s</td></tr>
<tr><td><code>python labs/reference/induction_run.py</code></td><td>11</td><td>Prefix-matching scores for all 144 heads on repeated random tokens, with a non-repeated control</td><td>~30 s</td></tr>
<tr><td><code>python -m unittest discover -s labs -p 'test_*.py'</code></td><td>all</td><td>The learner tests; they fail on the stubs by design. <code>INTERP_LAB_IMPL=reference</code> runs them against the solutions</td><td>~5 s</td></tr></table>
<h2 id="hooks">Hook points used</h2>
<table><tr><th>Name</th><th>Shape for GPT-2 small</th><th>Used in</th></tr>
<tr><td><code>blocks.L.mlp.hook_post</code></td><td>[batch, pos, 3072]</td><td>neuron scoring, max-activating examples</td></tr>
<tr><td><code>blocks.L.hook_resid_post</code></td><td>[batch, pos, 768]</td><td>probes, logit lens, patching</td></tr>
<tr><td><code>blocks.L.attn.hook_pattern</code></td><td>[batch, 12, pos, pos]</td><td>induction heads</td></tr>
<tr><td><code>blocks.L.hook_attn_out</code>, <code>blocks.L.hook_mlp_out</code></td><td>[batch, pos, 768]</td><td>direct logit attribution</td></tr>
<tr><td><code>ln_final.hook_scale</code></td><td>[batch, pos, 1]</td><td>direct logit attribution</td></tr></table>
<p>TransformerLens 4 loads the model with <code>TransformerBridge.boot_transformers("gpt2")</code> followed by <code>enable_compatibility_mode()</code>; the names above are the compatibility names. '''+cite('nanda')+''' recommends TransformerLens for models of this size.</p>'''),
 dict(path='appendices/c-reading-map.html',title='Reading map',kicker='Appendix C',n='C',kw='reading map routes shorter path review',
 lede='Shorter routes through the course for three purposes.',
 body='''<h2 id="review">Reviewing someone else’s interpretability claim (90 minutes)</h2>
<p>Lessons <a href="../pages/00-orientation.html">00</a>, <a href="../pages/01-the-protocol.html">01</a>, <a href="../pages/03-max-activating-examples.html">03</a>, <a href="../pages/05-controls.html">05</a>, and <a href="../pages/13-writing-it-up.html">13</a>. Then apply the checklist in lesson 13 to the claim.</p>
<h2 id="replicate">Replicating a vision claim on a laptop (half a day)</h2>
<p>Lessons <a href="../pages/01-the-protocol.html">01</a>, <a href="../pages/06-vision-replication.html">06</a>, and <a href="../pages/07-vision-controls.html">07</a>; the <a href="a-protocol-template.html">template</a>; <code>labs/curve_detector.py</code> and its tests.</p>
<h2 id="language">Explaining a language-model neuron (a day)</h2>
<p>Lessons <a href="../pages/02-the-objects.html">02</a> to <a href="../pages/05-controls.html">05</a>, <a href="../pages/12-sae-features.html">12</a>, <a href="../pages/13-writing-it-up.html">13</a>, and the <a href="../pages/14-capstone.html">capstone</a>; <code>labs/protocol.py</code> and <code>labs/explanation_score.py</code>.</p>
<h2 id="papers">Where the papers fit</h2>
<table><tr><th>Source</th><th>Lessons</th></tr>
<tr><td>Olah et al. 2020, Zoom In</td><td>02, 06</td></tr>
<tr><td>Cammarata et al. 2020, Curve Detectors</td><td>06, 07</td></tr>
<tr><td>Bills et al. 2023; Huang et al. 2023</td><td>04, 05, 13</td></tr>
<tr><td>Olsson et al. 2022</td><td>11</td></tr>
<tr><td>Bricken et al. 2023; Gao et al. 2024</td><td>12</td></tr>
<tr><td>Cammarata 2026; Gao 2026</td><td>00, 03, 12, 13</td></tr></table>'''),
]
