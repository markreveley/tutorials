from common import lesson, lab, cite, term, out

LESSONS = [
lesson(10,3,'forward-pass-from-raw-weights','The full forward pass from raw weights',
 'The capstone: load Hugging Face\'s state dict, write the model in plain tensor operations, and match the reference logits. This is the readiness test\'s first half.',
 '''<h2 id="the-task">The task</h2>
<p>Everything from lessons 02 to 09 is one function. Given token ids and the 148 weight tensors, produce logits that agree with <code>GPT2LMHeadModel</code>. The stub in <code>labs/gpt2_from_scratch.py</code> gives you the loader and asks for six functions: <code>layer_norm</code>, <code>gelu_new</code>, <code>causal_attention</code>, <code>mlp</code>, <code>forward_with_cache</code>, and <code>forward</code>. The reference solution used to produce this course's transcripts is about 90 lines; a readable version of yours should be under 200. The tests compare logits, every residual checkpoint, every attention pattern, and the MLP activations, then repeat the comparison against TransformerLens 4 and nnsight.</p>
<p>Before you write anything, run the comparison against the stub to see the starting state, and against the reference to see the target:</p>'''+term(['python labs/anatomy.py compare'])+out('python labs/anatomy.py compare')+'''
<p>That is the expected failure. The target looks like this:</p>'''+term(['python labs/anatomy.py compare --reference --tools'])+out('python labs/anatomy.py compare --reference --tools')+'''
<p>The largest logit on the prompt is about 134 and the largest discrepancy is 3.05e-05: agreement to roughly seven significant figures, which is float32 arithmetic done in a different order. The tests allow 1e-3 on logits and residuals, generous enough to admit any correct implementation and tight enough to reject every mistake in the list below.</p>
<h2 id="skeleton">The skeleton</h2>
<p>Here is the structure, written out as the operations rather than as code, with the Hugging Face tensor each step uses. <code>x</code> is the residual stream, shape <code>(batch, seq, 768)</code>.</p>
<ol>
<li><strong>Embed.</strong> <code>x = wte.weight[ids] + wpe.weight[0:seq]</code>. Record <code>embed</code>, <code>pos_embed</code>.</li>
<li><strong>For each block i = 0 … 11:</strong>
 <ol>
 <li>Record <code>resid_pre.i = x</code>.</li>
 <li><code>a = layer_norm(x, ln_1.weight, ln_1.bias)</code>; <code>attn_out, pattern = causal_attention(a, block, 12)</code>. Record <code>pattern.i</code>, <code>attn_out.i</code>.</li>
 <li><code>x = x + attn_out</code>. Record <code>resid_mid.i</code>.</li>
 <li><code>m = layer_norm(x, ln_2.weight, ln_2.bias)</code>; <code>mlp_out, post = mlp(m, block)</code>. Record <code>mlp_post.i</code>, <code>mlp_out.i</code>.</li>
 <li><code>x = x + mlp_out</code>. Record <code>resid_post.i</code>.</li>
 </ol></li>
<li><strong>Finish.</strong> <code>ln_final = layer_norm(x, ln_f.weight, ln_f.bias)</code>; <code>logits = ln_final @ wte.weight.T</code>.</li>
</ol>
<p>Inside <code>causal_attention</code>: <code>qkv = a @ c_attn.weight + c_attn.bias</code>, shape <code>(batch, seq, 2304)</code>; split the last axis into three 768-blocks; reshape each to <code>(batch, seq, 12, 64)</code> and transpose to <code>(batch, 12, seq, 64)</code>; <code>scores = q @ kᵀ / 8</code>; fill the strict upper triangle with −∞; softmax over the last axis; <code>z = pattern @ v</code>; transpose back and reshape to <code>(batch, seq, 768)</code>; <code>out = z @ c_proj.weight + c_proj.bias</code>. Inside <code>mlp</code>: <code>post = gelu_new(m @ c_fc.weight + c_fc.bias)</code>, <code>out = post @ c_proj.weight + c_proj.bias</code>.</p>
<h2 id="where-it-goes-wrong">The ways it goes wrong</h2>
<p>These are the errors the tolerance is designed to catch, in roughly the order people make them. Each is also a lesson's pitfall.</p>
<table><tr><th>Mistake</th><th>Symptom</th><th>Lesson</th></tr>
<tr><td>Transposing Conv1D weights (treating (768, 2304) as nn.Linear)</td><td>Shape error, or garbage logits if shapes happen to match (c_proj is square)</td><td>07, 11</td></tr>
<tr><td>Exact GELU instead of the tanh approximation</td><td>Logits off by ~1e-3 to 1e-2, argmax usually agrees</td><td>07</td></tr>
<tr><td>Sample variance in layer norm</td><td>Small uniform drift, grows with depth</td><td>04</td></tr>
<tr><td>Splitting heads as (batch, seq, 64, 12) instead of (batch, seq, 12, 64)</td><td>Patterns wrong at block 0; the HF comparison of pattern.0 fails first</td><td>06</td></tr>
<tr><td>Mask with 0 instead of −∞, or no mask</td><td>Rows do not sum to 1, or upper triangle nonzero; later positions leak into earlier ones</td><td>05</td></tr>
<tr><td>Forgetting the attention or MLP bias</td><td>Residuals off from block 0; the stream-identity test still passes because the error is consistent</td><td>03</td></tr>
<tr><td>Applying ln_f before recording resid_post.11, or using hidden_states[12] as resid_post.11</td><td>resid_post.11 off by hundreds; everything else fine</td><td>09, 13</td></tr>
<tr><td>Unembedding with wte instead of wteᵀ</td><td>Shape error (768 vs 50257)</td><td>09</td></tr></table>
<h2 id="the-diff">Reading the diff</h2>
<p>When the numbers disagree, the cache tells you where. The tests check <code>resid_post.i</code> for every <em>i</em>; the first failing block is where the bug lives, and within it, <code>pattern.i</code> (attention scores), <code>attn_out.i</code> (value/output path), and <code>mlp_post.i</code> (GELU and the up-projection) locate it further. A bug in layer norm shows up at <code>resid_post.0</code> already; a bug only in <code>ln_f</code> shows up only in the logits. Discrepancies that are small (1e-5) and grow slowly with depth are accumulation-order noise and are not bugs. Discrepancies that are constant across positions are usually a missing bias; discrepancies confined to position 0 usually involve the mask.</p>
<div class="evals"><span class="label">In interpretability work</span><p>Owning a forward pass you wrote is what lets you trust a hook. When a library reports an activation under some name, you can compute the same quantity yourself and check it to 1e-4, which is exactly what lesson 13 does. Every intervention experiment (ablating a head, patching a residual vector) is a modified forward pass; if you can write the unmodified one, the modified one is a few lines.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Optimising before matching. Fused QKV reshapes, in-place masking, einsum tricks, and half precision all change the accumulation order or the rounding. Write the obvious version, match to 1e-4, keep it as the oracle, and only then make a fast version that you test against it.</p></div>''',
 'Your logits match Hugging Face to 2e-3 everywhere and the argmax agrees at every position, but the test fails. What is the most likely cause, and why does the test not accept 2e-3?',
 'Most likely the exact GELU was used instead of gelu_new; a float32 accumulation-order difference is two orders of magnitude smaller than 2e-3, so a 2e-3 discrepancy is a systematic error. The tolerance rejects it because small systematic errors compound: at a different prompt or a longer sequence the argmax can flip, and more importantly any activation you later compare to a library\'s will carry the error, which makes the naming map in lesson 13 untrustworthy.',
 lab(["python -m unittest discover -s labs -p 'test_gpt2_from_scratch.py' -v",'python labs/anatomy.py compare --tools'],
 'Implement the six functions, then run the tests and the comparison. Keep the output of the first comparison that passes; it is your evidence for the readiness review.',
 'A passing run shows every max-difference at 1e-4 or below and "argmax next token agrees at every position: True"; the TransformerLens line (no_processing) and the nnsight line agree with your cache to the same order. The tests also check that your cache has 148 parameter tensors, that patterns match attentions to 1e-4, and that the stream equals the sum of its writes.'),
 ['hf-gpt2','gpt2-paper'], kw='forward pass from scratch state_dict capstone match logits tolerance Conv1D'),

lesson(11,3,'shapes-and-parameter-counts','Shapes and parameter counts: deriving 124M from the config',
 'Every tensor in GPT-2 small, its shape, and its size, added up by hand to the exact number the weights contain, with one historical discrepancy explained.',
 '''<h2 id="every-tensor">Every tensor</h2>
<p>The state dict has 149 entries: two embedding tables, twelve tensors in each of twelve blocks, two for the final layer norm, and the tied output matrix. Listing block 0 is enough, since blocks 1 to 11 have identical shapes:</p>'''+term(['python labs/anatomy.py shapes'])+out('python labs/anatomy.py shapes')+'''
<p>Every two-dimensional weight is stored as (in, out) because the layers are <code>Conv1D</code> modules, which compute <code>x @ weight + bias</code> '''+cite('hf-gpt2')+'''. The exception is <code>lm_head.weight</code>, an <code>nn.Linear</code> stored as (out, in) = (50257, 768), which is why the unembedding is <code>wteᵀ</code> in the capstone: it is the same tensor, used transposed.</p>
<h2 id="derivation">The derivation</h2>
<p>With d = 768, L = 12, V = 50,257, P = 1,024, and M = 4d = 3,072:</p>
<table><tr><th>Component</th><th>Expression</th><th>Count</th></tr>
<tr><td>wte</td><td>V × d = 50,257 × 768</td><td>38,597,376</td></tr>
<tr><td>wpe</td><td>P × d = 1,024 × 768</td><td>786,432</td></tr>
<tr><td>ln_1, ln_2 (per block)</td><td>2 × 2d</td><td>3,072</td></tr>
<tr><td>attn.c_attn (per block)</td><td>d × 3d + 3d = 1,769,472 + 2,304</td><td>1,771,776</td></tr>
<tr><td>attn.c_proj (per block)</td><td>d × d + d = 589,824 + 768</td><td>590,592</td></tr>
<tr><td>mlp.c_fc (per block)</td><td>d × M + M = 2,359,296 + 3,072</td><td>2,362,368</td></tr>
<tr><td>mlp.c_proj (per block)</td><td>M × d + d = 2,359,296 + 768</td><td>2,360,064</td></tr>
<tr><td>one block</td><td>sum of the five rows above</td><td>7,087,872</td></tr>
<tr><td>12 blocks</td><td>12 × 7,087,872</td><td>85,054,464</td></tr>
<tr><td>ln_f</td><td>2d</td><td>1,536</td></tr>
<tr><td><strong>total</strong></td><td>38,597,376 + 786,432 + 85,054,464 + 1,536</td><td><strong>124,439,808</strong></td></tr></table>
<p>The config command performs the same sum and compares it with <code>sum(p.numel() for p in model.parameters())</code>, which counts the tied matrix once:</p>'''+term(['python labs/anatomy.py config'])+out('python labs/anatomy.py config', keep=slice(1, None))+'''
<p>Two observations fall out. The embedding table is 31% of the model; the attention and MLP matrices of one block are about 7.1M, of which the MLP is two thirds. And biases and layer-norm parameters are a rounding error: about 0.1% of the total.</p>
<h2 id="117-vs-124">117M or 124M?</h2>
<p>The GPT-2 paper's Table 2 lists the smallest model as 117M parameters with 12 layers and d_model 768 '''+cite('gpt2-paper')+'''. The OpenAI model card for the same release describes the sizes as 124 million, 355 million, 774 million, and 1.5 billion '''+cite('gpt2-card')+'''. The weights in the Hugging Face checkpoint contain 124,439,808 learned scalars, and the derivation above reproduces that number from the config. This course therefore says 124M, and treats the paper's figure as a number whose derivation is not given. The method is the point: when two sources disagree about a model, the weights settle it, and the command that counted them is recorded.</p>
<h2 id="shapes-in-flight">Shapes in flight</h2>
<p>Parameters are static; activations depend on the input. For batch <em>b</em> and sequence length <em>s</em>:</p>
<table><tr><th>Activation</th><th>Shape</th><th>TransformerLens name</th></tr>
<tr><td>token ids</td><td>(b, s)</td><td>input</td></tr>
<tr><td>residual stream</td><td>(b, s, 768)</td><td>blocks.i.hook_resid_pre / _mid / _post</td></tr>
<tr><td>q, k, v, z per head</td><td>(b, s, 12, 64)</td><td>blocks.i.attn.hook_q / _k / _v / _z</td></tr>
<tr><td>attention scores and pattern</td><td>(b, 12, s, s)</td><td>blocks.i.attn.hook_attn_scores / hook_pattern</td></tr>
<tr><td>MLP hidden</td><td>(b, s, 3072)</td><td>blocks.i.mlp.hook_pre / hook_post</td></tr>
<tr><td>logits</td><td>(b, s, 50257)</td><td>return value of run_with_cache</td></tr></table>
<p>TransformerLens keeps the head axis after the sequence axis for q, k, v, and z, and before it for scores and patterns; Hugging Face's internal attention uses (b, 12, s, 64) throughout. Lesson 13's table records which is which, and the shapes column of the <code>names</code> output is the check.</p>
<div class="evals"><span class="label">In interpretability work</span><p>Shape assertions are tests. A hook that receives (1, 12, 6, 6) when you expected (1, 6, 12, 64) has told you that you hooked the pattern, not z; an <code>assert tensor.shape == (b, s, 768)</code> at the top of every analysis function costs nothing and catches the silent transposes that produce plausible-looking nonsense. Know the shapes table well enough to write those asserts without looking.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Counting <code>len(state_dict)</code> as the number of parameter tensors, or summing <code>numel()</code> over the state dict. The state dict has 149 entries because the tied <code>lm_head.weight</code> appears under its own name; the model has 148 distinct parameter tensors. Summing over the state dict double-counts 38.6M.</p></div>''',
 'GPT-2 medium has 24 layers and d_model 1024, with the same vocabulary, context length, and 4× MLP ratio. Derive its parameter count to the nearest thousand without running anything, then say which single line of the derivation you would check against the weights first.',
 'wte 50,257 × 1,024 = 51,463,168; wpe 1,048,576; per block: ln 4,096 + c_attn 1,024 × 3,072 + 3,072 = 3,148,800 + c_proj 1,048,576 + 1,024 = 1,049,600 + c_fc 1,024 × 4,096 + 4,096 = 4,198,400 + mlp c_proj 4,096 × 1,024 + 1,024 = 4,195,328, total 12,596,224 per block; 24 blocks = 302,309,376; ln_f 2,048; total ≈ 354,823,168, which is the "355M" of the model card. Check the head count first (the derivation does not depend on it, but d_head = 1024/16 = 64 confirms the config), and then c_attn\'s shape, since a model with separate q, k, v matrices would store three (1024, 1024) tensors instead.',
 lab(['python labs/anatomy.py shapes','python labs/anatomy.py config'],
 'Add up the five per-block lines by hand and confirm 7,087,872. Then write the GPT-2 medium derivation above into a short Python expression and check it against the model card\'s 355M.',
 '3,072 + 1,771,776 + 590,592 + 2,362,368 + 2,360,064 = 7,087,872. The medium derivation gives 354,823,168, which rounds to 355M. If you have the medium checkpoint cached, sum(p.numel() for p in model.parameters()) will confirm it; if not, the derivation is your only evidence and you should say so.'),
 ['gpt2-paper','gpt2-card','hf-gpt2'], kw='parameter count shapes state dict 124M 117M Conv1D tied lm_head'),

lesson(12,3,'generation-and-the-kv-cache','Generation and the KV cache',
 'A language model becomes a text generator by sampling one token and appending it. The cache that makes this fast follows from the causal mask, and the output shows it is exact.',
 '''<h2 id="loop">The loop</h2>
<p>Generation is a loop around the forward pass: run the model on the prompt, take the logits at the last position, pick a token, append it, repeat. Greedy decoding picks the argmax every time; sampling draws from the softmax, optionally after dividing the logits by a temperature. Nothing in the model changes between steps; only the input grows.</p>'''+term(['python labs/anatomy.py generate'])+out('python labs/anatomy.py generate')+'''
<p>Greedy decoding from the running prompt produces <code>", and the cat sat on"</code>: a comma (the top token from the logit lens in lesson 09, probability 0.237), then a loop back into the prompt's own phrase. The sampled continuation with seed 0 at temperature 1.0 is different and is reproducible only with that seed. The six greedy token ids are printed twice, computed two ways, and they agree.</p>
<h2 id="temperature">Temperature and the softmax</h2>
<p>Dividing logits by a temperature <em>T</em> before the softmax changes the shape of the distribution without changing the ranking. Lesson 09's demo showed [2, 1, 0] becoming [0.665, 0.245, 0.090] at <em>T</em> = 1, flatter [0.507, 0.307, 0.186] at <em>T</em> = 2, and sharper [0.867, 0.117, 0.016] at <em>T</em> = 0.5. As <em>T</em> → 0 the softmax puts all its mass on the argmax, which is greedy decoding; <em>T</em> = 1 is the model's own distribution. Top-k and nucleus sampling truncate the distribution before drawing; the demo passes <code>top_k=0</code> so that the only modification is the temperature.</p>
<h2 id="why-caching-works">Why caching works</h2>
<p>Recomputing the whole sequence each step costs O(<em>s</em>²) attention work per step. The causal mask makes most of it redundant. Position <em>j</em>'s key and value in every layer depend only on the residual stream at position <em>j</em>, which depends only on positions ≤ <em>j</em>. Appending a token at position <em>s</em> therefore does not change any key or value at positions 0 to <em>s</em> − 1, in any layer. So you can store them. At each new step you run only the new position through the model: compute its query, key, and value in each layer, attend from its query to the stored keys, append its own key and value to the store, and continue. The attention computation per step becomes O(<em>s</em>) and the rest of the block (layer norms, MLP, projections) runs on one position instead of <em>s</em>.</p>
<p>The demo does this by hand with <code>use_cache=True</code> and <code>past_key_values</code>, and in parallel recomputes the full sequence every step. The two lists of token ids are identical, which is the claim: caching changes the cost, not the result. The cache after six prompt tokens and six generated tokens holds, per layer, a key tensor of shape (1, 12, 12, 64): batch, heads, twelve positions, d_head. That is the (b, n_head, s, d_head) layout from lesson 11, grown by one position per step.</p>
<div class="math">cache size = 2 × n_layer × b × n_head × s × d_head floats<br>= 2 × 12 × 1 × 12 × s × 64 = 18,432 × s floats for GPT-2 small</div>
<p>For a 1,024-token context that is about 19M floats, 75 MB in float32, per sequence: small for GPT-2, and the reason grouped-query attention (lesson 14) exists for large models, where the cache rather than the weights limits batch size.</p>
<h2 id="what-the-cache-is-not">What the cache is not</h2>
<p>The cache stores keys and values, not the residual stream. If an interpretability experiment patches the residual stream at an earlier position during generation, the cached keys and values at that position are stale and the generation continues from the unpatched values. Libraries differ in whether they recompute; when in doubt, generate without a cache, or patch and re-run the prefix.</p>
<div class="evals"><span class="label">In interpretability work</span><p>Most interpretability experiments do not need generation at all: a single forward pass on a fixed prompt gives every activation and every logit. When a claim is about generated text ("the model continues with X"), it is really a claim about a sequence of forward passes, each conditioned on the previous choices, and the sampling policy (greedy, temperature, seed) is part of the experiment's specification. Record it.</p></div>
<div class="pitfall"><span class="label">Pitfall</span><p>Comparing a sampled continuation across runs or models without fixing the seed and the sampling parameters, then reading the difference as a difference in the models. The demo's sampled line changes with the seed; the greedy line does not. Use greedy decoding, or many samples with reported statistics, when the continuation is the measurement.</p></div>''',
 'During cached generation you zero out the layer-5 MLP output at position 2 of the prompt, then generate ten tokens. Which later computations see the change, and which do not?',
 'If the prefix is run once with the intervention and its keys and values cached, every later position attends to the intervened keys and values at position 2 in layers 6 to 11 (and the layer-5 attention keys/values are unaffected because they were computed before the MLP). But the residual stream at position 2 is never recomputed, so nothing downstream of position 2 that depends on its post-intervention stream in layer 5 itself changes beyond what flows through keys and values. If instead the intervention is applied as a hook on every forward step but the cache was built without it, the cached keys and values at position 2 are stale and the generated tokens attend to the unintervened values. The experiment must say which.',
 lab(['python labs/anatomy.py generate --temperature 0.5 --seed 1','python labs/anatomy.py generate "The capital of France is" --tokens 4'],
 'Rerun with a lower temperature and another seed, then on a prompt with a strongly expected continuation. Watch whether the sampled line moves toward the greedy line.',
 'At temperature 0.5 the sampled continuation is more likely to coincide with the greedy one, since the distribution is sharper; with a different seed it may still differ. On the capital prompt the greedy continuation is whatever the model\'s argmax chain produces, printed exactly; the hand-rolled cached and uncached lists agree again, because the identity does not depend on the prompt.'),
 ['vaswani','hf-gpt2'], kw='generation sampling temperature greedy KV cache past_key_values'),
]
