from common import cite, term, out

REFERENCES = [
 dict(path='appendices/a-shapes-and-notation.html',title='Shapes and notation',kicker='Appendix A',n='A',kw='shapes notation tensor table d_model d_head d_mlp symbols',
 lede='Every symbol used in the lessons, every parameter tensor of GPT-2 small with its shape, and every activation shape, in one place.',
 body='''<h2 id="symbols">Symbols</h2>
<table><tr><th>Symbol</th><th>GPT-2 small</th><th>Meaning</th></tr>
<tr><td>b, s</td><td>—</td><td>batch size and sequence length of one input</td></tr>
<tr><td>d_model (n_embd)</td><td>768</td><td>width of the residual stream</td></tr>
<tr><td>n_layer</td><td>12</td><td>number of blocks</td></tr>
<tr><td>n_head</td><td>12</td><td>heads per block</td></tr>
<tr><td>d_head</td><td>64</td><td>d_model / n_head</td></tr>
<tr><td>d_mlp (n_inner)</td><td>3072</td><td>MLP hidden width, 4 × d_model</td></tr>
<tr><td>d_vocab</td><td>50257</td><td>vocabulary size</td></tr>
<tr><td>n_ctx (n_positions)</td><td>1024</td><td>context window</td></tr>
<tr><td>ε</td><td>1e-5</td><td>layer-norm epsilon</td></tr>
<tr><td>x, W_Q, W_K, W_V, W_O</td><td>—</td><td>a residual row vector and one head's four matrices; row-vector convention, q = x W_Q</td></tr>
<tr><td>W_in, W_out</td><td>(768, 3072), (3072, 768)</td><td>MLP up- and down-projection (c_fc, c_proj)</td></tr>
<tr><td>W_U</td><td>(768, 50257)</td><td>unembedding = wteᵀ</td></tr></table>
<h2 id="parameters">Parameter tensors</h2>
<p>From the installed checkpoint:</p>'''+term(['python labs/anatomy.py shapes'])+out('python labs/anatomy.py shapes')+'''
<h2 id="activations">Activation shapes</h2>
<table><tr><th>Activation</th><th>Shape</th><th>Hugging Face</th><th>TransformerLens 4</th><th>nnsight</th></tr>
<tr><td>token ids</td><td>(b, s)</td><td>input_ids</td><td>input to run_with_cache</td><td>input to trace</td></tr>
<tr><td>token / position embedding</td><td>(b, s, 768) / (b, s, 768)</td><td>wte(ids) / wpe(pos)</td><td>hook_embed / hook_pos_embed</td><td>transformer.wte.output / wpe.output</td></tr>
<tr><td>residual into block i</td><td>(b, s, 768)</td><td>hidden_states[i]</td><td>blocks.i.hook_resid_pre</td><td>transformer.h[i].input</td></tr>
<tr><td>q, k, v, z per head</td><td>(b, s, 12, 64)</td><td>internal (b, 12, s, 64)</td><td>blocks.i.attn.hook_q / _k / _v / _z</td><td>—</td></tr>
<tr><td>scores, pattern</td><td>(b, 12, s, s)</td><td>attentions[i] (eager only)</td><td>blocks.i.attn.hook_attn_scores / hook_pattern</td><td>hook on attn</td></tr>
<tr><td>attention write</td><td>(b, s, 768)</td><td>hook on h[i].attn</td><td>blocks.i.hook_attn_out</td><td>transformer.h[i].attn.output[0]</td></tr>
<tr><td>residual after attention</td><td>(b, s, 768)</td><td>—</td><td>blocks.i.hook_resid_mid</td><td>transformer.h[i].mlp.input (pre-norm input is ln_2's)</td></tr>
<tr><td>MLP pre / post activation</td><td>(b, s, 3072)</td><td>hook on h[i].mlp.act</td><td>blocks.i.mlp.hook_pre / hook_post</td><td>transformer.h[i].mlp.act.input / .output</td></tr>
<tr><td>MLP write</td><td>(b, s, 768)</td><td>hook on h[i].mlp</td><td>blocks.i.hook_mlp_out</td><td>transformer.h[i].mlp.output</td></tr>
<tr><td>residual after block i</td><td>(b, s, 768)</td><td>hidden_states[i+1] for i &lt; 11</td><td>blocks.i.hook_resid_post</td><td>transformer.h[i].output</td></tr>
<tr><td>after ln_f</td><td>(b, s, 768)</td><td>hidden_states[12]</td><td>ln_final.hook_out</td><td>transformer.ln_f.output</td></tr>
<tr><td>logits</td><td>(b, s, 50257)</td><td>logits</td><td>return value</td><td>lm_head.output</td></tr></table>
<p>The rows with three library names were verified numerically in <a href="../pages/13-naming-maps.html">lesson 13</a>; the q/k/v/z and resid_mid rows are from the installed package's cache (shapes printed in the lesson-13 output) and were not cross-checked against the other libraries.</p>'''),

 dict(path='appendices/b-command-reference.html',title='Command reference',kicker='Appendix B',n='B',kw='commands anatomy.py reference tests',
 lede='Every sub-command of labs/anatomy.py, the lesson it belongs to, and the test commands. All run from the course directory.',
 body='''<h2 id="setup">Environment</h2>
<p>A Python environment with <code>torch</code>, <code>transformers</code> (5.x), <code>transformer_lens</code> (4.x), and <code>nnsight</code>, with <code>gpt2</code> in the Hugging Face cache. The authoring versions are recorded at the top of <a href="../research/verify/lab-transcript.txt">the transcript</a>. Set <code>HF_HUB_OFFLINE=1</code> to avoid network lookups; the tool sets it by default.</p>
<h2 id="commands">Inspection commands</h2>
<table><tr><th>Command</th><th>Lesson</th><th>Shows</th></tr>
<tr><td><code>tokens TEXT... [--compare A B]</code></td><td>01</td><td>token ids, decoded pieces, raw pieces with Ġ</td></tr>
<tr><td><code>bpe-demo [--merges N]</code></td><td>01</td><td>toy byte-pair training on the five-word corpus</td></tr>
<tr><td><code>embed [TEXT] [--positions N]</code></td><td>02</td><td>wte and wpe rows and their sum; check against hidden_states[0]</td></tr>
<tr><td><code>stream [TEXT] [--position P]</code></td><td>03</td><td>residual norms and every write per block; the sum identity</td></tr>
<tr><td><code>layernorm-demo</code></td><td>04, 14</td><td>LayerNorm, RMSNorm, and folding on [1, 3, 5, 7]</td></tr>
<tr><td><code>attention-demo</code></td><td>05</td><td>one head on the three-token pencil example, checked against torch</td></tr>
<tr><td><code>heads [TEXT] --layer L --head H</code></td><td>06</td><td>a real attention pattern and the ranks of its QK and OV circuits</td></tr>
<tr><td><code>mlp-demo [TEXT] --layer L</code></td><td>07</td><td>top neurons per position, fraction active, GELU values</td></tr>
<tr><td><code>swiglu-demo</code></td><td>08</td><td>SwiGLU on a two-vector</td></tr>
<tr><td><code>logit-lens [TEXT]</code></td><td>09</td><td>top-3 tokens after every block at the last position</td></tr>
<tr><td><code>softmax-demo</code></td><td>09, 12</td><td>softmax and temperature on [2, 1, 0]</td></tr>
<tr><td><code>config</code></td><td>00, 11</td><td>config values and the parameter-count derivation</td></tr>
<tr><td><code>shapes</code></td><td>11, A</td><td>every state-dict tensor with shape and size</td></tr>
<tr><td><code>generate [TEXT] [--tokens N] [--temperature T] [--seed S]</code></td><td>12</td><td>greedy and sampled continuations; cached versus uncached greedy</td></tr>
<tr><td><code>names [TEXT] [--layer L] [--processing none|default]</code></td><td>13</td><td>the three-library naming table with max differences</td></tr>
<tr><td><code>compare [TEXT] [--reference] [--tools]</code></td><td>10, 15</td><td>your forward pass (or the author's) against transformers, TransformerLens, nnsight</td></tr></table>
<h2 id="tests">Lab tests</h2>'''+term(["python -m unittest discover -s labs -p 'test_tokens.py' -v","python -m unittest discover -s labs -p 'test_attention.py' -v","python -m unittest discover -s labs -p 'test_gpt2_from_scratch.py' -v","python -m unittest discover -s labs -p 'test_*.py' -v"])+'''
<p>Tests that need torch or transformers skip with a message when those are absent. Before the stubs are implemented the tests fail with <code>NotImplementedError</code>; the transcript records that starting state and a passing run against the author's reference solutions under <code>labs/reference/</code>, which are used only to generate verified output and are not the learner's starting point.</p>
<h2 id="help">Help</h2>'''+term(['python labs/anatomy.py --help'])+out('python labs/anatomy.py --help')),
]
