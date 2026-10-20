from common import cite, run, code

REFERENCES = [
 dict(path='appendices/a-shapes.html',title='Shape reference',kicker='Appendix A',n='A',kw='shape cheat sheet broadcasting einsum GPT-2 dimensions axis',
 lede='The shapes you will meet in GPT-2 small, the rules that combine them, and the expressions that read them. Keep it open while you work.',
 body='''<h2 id="gpt2">GPT-2 small by the numbers</h2>
<table><tr><th>Quantity</th><th>Value</th><th>Where it appears</th></tr>
<tr><td>vocab</td><td>50257</td><td>last axis of logits; rows of <code>wte.weight</code></td></tr>
<tr><td>context (n_positions)</td><td>1024</td><td>rows of <code>wpe.weight</code>; maximum <code>seq</code></td></tr>
<tr><td>d_model (n_embd, hidden_size)</td><td>768</td><td>last axis of every residual-stream tensor</td></tr>
<tr><td>layers (n_layer)</td><td>12</td><td><code>transformer.h[0..11]</code>; 13 hidden states</td></tr>
<tr><td>heads (n_head)</td><td>12</td><td>axis 1 of attention patterns</td></tr>
<tr><td>d_head</td><td>64</td><td>768 / 12; the summed axis in attention scores</td></tr>
<tr><td>d_mlp</td><td>3072</td><td>4 × 768; <code>mlp.c_fc.weight</code> is (768, 3072)</td></tr>
<tr><td>parameters</td><td>124,439,808</td><td><code>sum(p.numel() for p in model.parameters())</code></td></tr></table>
<h2 id="tensors">The tensors and their shapes</h2>
<table><tr><th>Tensor</th><th>Shape</th><th>Read as</th></tr>
<tr><td><code>input_ids</code>, <code>attention_mask</code></td><td>(batch, seq)</td><td>one id or one mask bit per position</td></tr>
<tr><td>embedding output, residual after any block</td><td>(batch, seq, 768)</td><td>one 768-vector per position</td></tr>
<tr><td><code>hidden_states</code></td><td>tuple of 13 × (batch, seq, 768)</td><td>[0] embeddings; [i+1] after block i; [12] after ln_f</td></tr>
<tr><td>logits</td><td>(batch, seq, 50257)</td><td>scores for the next token at every position</td></tr>
<tr><td>next-token logits</td><td>(batch, 50257)</td><td><code>logits[:, -1]</code> (last real position only if unpadded or left-padded)</td></tr>
<tr><td>attention pattern</td><td>(batch, 12, seq, seq)</td><td>[b, h, q, k]: query q attends to key k; rows sum to 1</td></tr>
<tr><td>queries, keys, values per head</td><td>(batch, 12, seq, 64)</td><td>after splitting 768 into 12 × 64</td></tr>
<tr><td>a direction</td><td>(768,)</td><td>projects a cache with <code>bsd,d-&gt;bs</code></td></tr>
<tr><td>a gradient</td><td>the shape of what it is with respect to</td><td><code>acts.grad</code> is (batch, seq, 768)</td></tr></table>
<h2 id="rules">The rules</h2>
<p><strong>Indexing:</strong> each integer index removes an axis; each slice keeps it; <code>None</code> adds one; <code>...</code> stands for all leading axes. Basic slices are views; boolean and list indexing copy.</p>
<p><strong>Broadcasting:</strong> align shapes at the right, pad the shorter with ones on the left, and at each position the sizes must be equal or one of them 1; the result takes the larger. In place, the result may not be larger than the in-place operand. '''+cite('np-broadcast')+''' '''+cite('torch-broadcast')+'''</p>
<p><strong>Reductions:</strong> the named axis disappears; <code>keepdims=True</code> keeps it as size 1; <code>argmax</code> returns indices with the same shape rule.</p>
<p><strong>einsum:</strong> one letter per axis per operand; a letter missing from the output is summed; a letter repeated in one operand takes the diagonal; always write the <code>-&gt;</code>. '''+cite('np-einsum')+'''</p>
<p><strong>Views:</strong> <code>view</code>, <code>transpose</code>, <code>permute</code>, <code>squeeze</code>, slices and <code>from_numpy</code> share storage; <code>reshape</code> may or may not; <code>clone</code> and <code>copy</code> do not. '''+cite('torch-views')+'''</p>
<h2 id="expressions">Expressions to recognise on sight</h2>
<table><tr><th>Expression</th><th>Shape</th><th>Meaning</th></tr>
<tr><td><code>acts[:, -1]</code></td><td>(batch, 768)</td><td>last position of every prompt</td></tr>
<tr><td><code>acts[0, -1]</code></td><td>(768,)</td><td>one vector</td></tr>
<tr><td><code>acts.mean(-1, keepdim=True)</code></td><td>(batch, seq, 1)</td><td>per-position mean, ready to subtract</td></tr>
<tr><td><code>acts.norm(dim=-1)</code></td><td>(batch, seq)</td><td>residual norm per position</td></tr>
<tr><td><code>torch.einsum("bsd,d-&gt;bs", acts, v)</code></td><td>(batch, seq)</td><td>projection onto a direction</td></tr>
<tr><td><code>torch.einsum("bhqd,bhkd-&gt;bhqk", q, k) / 8</code></td><td>(batch, 12, seq, seq)</td><td>scaled attention scores (√64 = 8)</td></tr>
<tr><td><code>pattern @ v</code></td><td>(batch, 12, seq, 64)</td><td>attention-weighted values</td></tr>
<tr><td><code>(acts * mask[..., None]).sum(1) / mask.sum(1, keepdim=True)</code></td><td>(batch, 768)</td><td>masked mean over positions</td></tr>
<tr><td><code>logits[:, -1].softmax(-1).topk(5)</code></td><td>values and indices (batch, 5)</td><td>top next tokens</td></tr>
<tr><td><code>torch.stack(out.hidden_states)</code></td><td>(13, batch, seq, 768)</td><td>all layers in one tensor</td></tr></table>
<h2 id="asserts">The asserts to copy</h2>
'''+code('''assert acts.shape == (batch, seq, 768), acts.shape
assert acts.dtype == torch.float32, acts.dtype
assert not acts.requires_grad
assert torch.isfinite(acts).all()
assert pattern.shape[-2:] == (seq, seq) and torch.allclose(pattern.sum(-1), torch.ones_like(pattern[..., 0]))''')+'''
<p>Write the shape comment next to every tensor assignment. A comment that says <code># (batch, seq, 768)</code> is cheaper than the hour you spend when it is not there.</p>'''),

 dict(path='appendices/b-commands.html',title='Command and lab reference',kicker='Appendix B',n='B',kw='commands scripts tests labs unittest verify',
 lede='Every script and test in the course, in the order you meet them, with the one line that runs each.',
 body='''<h2 id="scripts">Example scripts</h2>
<p>All run from the course directory, <code>tutorials/python/python-tut</code>. Scripts that load GPT-2 set <code>HF_HUB_OFFLINE=1</code> themselves; run once online first to populate the cache.</p>
<table><tr><th>Lesson</th><th>Command</th><th>Shows</th></tr>
<tr><td>00, 01</td><td><code>python3 labs/examples/check_setup.py</code></td><td>versions and a (2, 5, 768) tensor</td></tr>
<tr><td>02</td><td><code>python3 labs/examples/names_and_objects.py</code></td><td>aliasing, copies, mutable defaults</td></tr>
<tr><td>03</td><td><code>python3 labs/examples/records_and_errors.py</code></td><td>JSON traps, JSONL line numbers, exceptions</td></tr>
<tr><td>05</td><td><code>python3 labs/examples/generators_and_dataclasses.py</code></td><td>lazy iteration, frozen records, hints</td></tr>
<tr><td>06</td><td><code>python3 labs/examples/arrays.py</code></td><td>shape, dtype, indexing, views</td></tr>
<tr><td>07</td><td><code>python3 labs/examples/broadcast_drill.py</code></td><td>ten shape pairs and keepdims</td></tr>
<tr><td>08</td><td><code>python3 labs/examples/reductions_einsum.py</code></td><td>axis reductions and einsum strings</td></tr>
<tr><td>09</td><td><code>python3 labs/examples/tensors.py</code></td><td>dtype enforcement, views, in-place, no_grad</td></tr>
<tr><td>10</td><td><code>python3 labs/examples/autograd_fit.py</code></td><td>gradients, a fit, accumulation</td></tr>
<tr><td>11</td><td><code>python3 labs/examples/module_tree.py</code></td><td>a tiny MLP and GPT-2's tree</td></tr>
<tr><td>12</td><td><code>python3 labs/examples/gpt2_next_token.py</code></td><td>ids, logits, top tokens, hidden states, padding</td></tr>
<tr><td>13</td><td><code>python3 labs/examples/hooks_cache.py</code></td><td>twelve hooks, asserts, save, a leaked hook</td></tr>
<tr><td>14</td><td><code>python3 labs/examples/three_tools.py</code></td><td>one activation three ways</td></tr>
<tr><td>15</td><td><code>python3 labs/examples/reproducibility.py</code></td><td>seeds, memory, safetensors, manifest</td></tr></table>
<h2 id="labs">Labs: stubs and their tests</h2>
<table><tr><th>Stub</th><th>Test</th><th>Needs</th><th>Lessons</th></tr>
<tr><td><code>labs/eval_pipeline.py</code></td><td><code>dag-tests/test_python_evals.py</code> (from the repository root)</td><td>standard library</td><td>03, 04</td></tr>
<tr><td><code>labs/shapes.py</code></td><td><code>labs/test_shapes.py</code></td><td>numpy</td><td>07, 08</td></tr>
<tr><td><code>labs/hooks.py</code></td><td><code>labs/test_hooks.py</code></td><td>torch, transformers, cached gpt2 (skips otherwise)</td><td>13</td></tr>
<tr><td><code>labs/manifest.py</code></td><td><code>labs/test_manifest.py</code></td><td>numpy</td><td>15</td></tr>
<tr><td>(none)</td><td><code>labs/test_environment.py</code></td><td>passes as shipped; skips what is missing</td><td>01</td></tr></table>
'''+run("python3 -m unittest discover -s labs -p 'test_*.py' 2>&1 | tail -1", note='The shipped state: red until you implement the stubs. The environment tests are the ones already passing.')+'''
<p>Run one file with <code>-p 'test_shapes.py'</code>; see every test name with <code>-v</code>. The eval-pipeline tests run from the repository root: <code>python3 -m unittest discover -s dag-tests -p 'test_python_evals.py' -v</code>.</p>
<h2 id="authoring">Authoring checks</h2>
<p>For whoever maintains the course. The verifier runs every command on this site with the interpreter it is launched with, so launch it from the virtualenv.</p>
'''+code('''python3 scripts/build.py                      # HTML from scripts/*.py
python3 scripts/verify_commands.py            # run every shown command; write research/verify/
python3 scripts/build.py                      # paste the recorded outputs into the pages
python3 scripts/check_site.py                 # links, nesting, components, verified outputs
python3 -m unittest discover -s labs -p 'test_*.py' -v
node --check assets/wiki.js''', 'sh')+'''
<p>See <a href="../research/AUTHORING.md">the authoring guide</a>.</p>'''),
]
