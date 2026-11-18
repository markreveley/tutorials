"""Transformer Anatomy: small inspection commands for GPT-2 small.

Every lesson's terminal output comes from this file. Run from the course directory:

    python labs/anatomy.py tokens "The cat sat on the mat"
    python labs/anatomy.py --help

Commands that need a model load `gpt2` from the local Hugging Face cache. Set
HF_HUB_OFFLINE=1 to avoid network lookups. `names` also needs transformer_lens
and nnsight; everything else needs only torch and transformers.
"""
import argparse
import math
import os
import sys
from pathlib import Path

os.environ.setdefault('HF_HUB_OFFLINE', '1')
os.environ.setdefault('TRANSFORMERS_VERBOSITY', 'error')
os.environ.setdefault('HF_HUB_DISABLE_PROGRESS_BARS', '1')

LABS = Path(__file__).resolve().parent
PROMPT = 'The cat sat on the mat'


def fmt(values, nd=4):
    return '[' + ', '.join(f'{float(v):.{nd}f}' for v in values) + ']'


def tokenizer():
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained('gpt2')


def model():
    import torch
    from transformers import GPT2LMHeadModel
    torch.manual_seed(0)
    m = GPT2LMHeadModel.from_pretrained('gpt2', attn_implementation='eager').eval()
    return m.requires_grad_(False)


# ---------------------------------------------------------------- tokens
def cmd_tokens(args):
    tok = tokenizer()
    for text in args.text:
        ids = tok.encode(text)
        print(f'{text!r}: {len(ids)} tokens')
        for i, tid in enumerate(ids):
            print(f'  {i:>2}  id={tid:<6} piece={tok.decode([tid])!r}  raw={tok.convert_ids_to_tokens(tid)!r}')
    if args.compare:
        a, b = args.compare
        print(f'{a!r} -> {tok.encode(a)}   {b!r} -> {tok.encode(b)}')


def cmd_bpe_demo(args):
    """Train a toy byte-pair encoder on a five-word corpus, printing each merge."""
    corpus = {'hug': 10, 'pug': 5, 'pun': 12, 'bun': 4, 'hugs': 5}
    words = {tuple(w): c for w, c in corpus.items()}
    print('corpus (word: count):', corpus)
    for step in range(args.merges):
        pairs = {}
        for word, count in words.items():
            for a, b in zip(word, word[1:]):
                pairs[(a, b)] = pairs.get((a, b), 0) + count
        best = max(pairs, key=lambda p: (pairs[p], [-ord(c) for c in ''.join(p)]))
        top = sorted(pairs.items(), key=lambda kv: -kv[1])[:4]
        print(f'step {step + 1}: pair counts {", ".join(f"{a}{b}={n}" for (a, b), n in top)} -> merge {best[0]!r}+{best[1]!r}')
        merged = {}
        for word, count in words.items():
            out, i = [], 0
            while i < len(word):
                if i + 1 < len(word) and (word[i], word[i + 1]) == best:
                    out.append(word[i] + word[i + 1]); i += 2
                else:
                    out.append(word[i]); i += 1
            merged[tuple(out)] = count
        words = merged
        print('        words now:', {' '.join(w): c for w, c in words.items()})


# ---------------------------------------------------------------- embeddings and stream
def cmd_embed(args):
    import torch
    tok, m = tokenizer(), model()
    ids = tok.encode(args.text)
    wte, wpe = m.transformer.wte.weight, m.transformer.wpe.weight
    print(f'wte shape {tuple(wte.shape)}, wpe shape {tuple(wpe.shape)}')
    for pos, tid in enumerate(ids[:args.positions]):
        e, p = wte[tid], wpe[pos]
        print(f'position {pos}, token {tid} ({tok.decode([tid])!r})')
        print(f'  wte[{tid}][:5] = {fmt(e[:5])}  |wte| = {e.norm():.3f}')
        print(f'  wpe[{pos}][:5]   = {fmt(p[:5])}  |wpe| = {p.norm():.3f}')
        print(f'  sum[:5]       = {fmt((e + p)[:5])}  |sum| = {(e + p).norm():.3f}')
    with torch.no_grad():
        h0 = m(torch.tensor([ids]), output_hidden_states=True).hidden_states[0][0]
    print(f'max |(wte+wpe) - hidden_states[0]| = {(wte[ids] + wpe[:len(ids)] - h0).abs().max():.2e}')


def cmd_stream(args):
    import torch
    sys.path.insert(0, str(LABS / 'reference'))
    from gpt2_from_scratch_reference import forward_with_cache, load_params
    tok = tokenizer()
    ids = torch.tensor([tok.encode(args.text)])
    params = load_params()
    with torch.no_grad():
        logits, cache = forward_with_cache(ids, params)
    pos = args.position if args.position >= 0 else ids.shape[1] + args.position
    print(f'{args.text!r}: {ids.shape[1]} tokens; reporting position {pos} ({tok.decode([ids[0, pos].item()])!r})')
    print(f'{"layer":>5} {"|resid_pre|":>12} {"|attn_out|":>11} {"|mlp_out|":>10} {"|resid_post|":>13}')
    for i in range(12):
        r = lambda k: cache[f'{k}.{i}'][0, pos].norm().item()
        print(f'{i:>5} {r("resid_pre"):>12.2f} {r("attn_out"):>11.2f} {r("mlp_out"):>10.2f} {r("resid_post"):>13.2f}')
    total = cache['embed'] + cache['pos_embed']
    for i in range(12):
        total = total + cache[f'attn_out.{i}'] + cache[f'mlp_out.{i}']
    print(f'max |embed + pos + sum(attn_out) + sum(mlp_out) - resid_post.11| = {(total - cache["resid_post.11"]).abs().max():.2e}')


# ---------------------------------------------------------------- norms
def cmd_layernorm_demo(args):
    import torch
    x = torch.tensor([1.0, 3.0, 5.0, 7.0])
    mean, var = x.mean(), x.var(unbiased=False)
    print(f'x = {fmt(x)}  mean = {mean:.4f}  variance (population) = {var:.4f}  std = {var.sqrt():.4f}')
    ln = (x - mean) / torch.sqrt(var + 1e-5)
    print(f'LayerNorm(x) with gamma=1, beta=0, eps=1e-5 = {fmt(ln)}')
    print(f'torch.nn.functional.layer_norm agrees: {fmt(torch.nn.functional.layer_norm(x, (4,), eps=1e-5))}')
    rms = torch.sqrt((x ** 2).mean())
    print(f'RMSNorm(x) with weight=1: rms = {rms:.4f}, output = {fmt(x / rms)}')
    gamma, beta = torch.tensor([2.0, 1.0, 0.5, 1.0]), torch.tensor([0.0, 1.0, 0.0, -1.0])
    W = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [2.0, -1.0]])
    b = torch.tensor([0.5, 0.0])
    y1 = (ln * gamma + beta) @ W + b
    W_fold, b_fold = gamma[:, None] * W, beta @ W + b
    y2 = ln @ W_fold + b_fold
    print('folding: (ln*gamma+beta) @ W + b  =', fmt(y1))
    print('         ln @ (gamma[:,None]*W) + (beta@W + b) =', fmt(y2))


# ---------------------------------------------------------------- attention
HAND_Q = [[0.0, 2.0, 0.0, 0.0], [2.0, 0.0, 0.0, 0.0], [2.0, 2.0, 0.0, 0.0]]
HAND_K = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [1.0, 1.0, 0.0, 0.0]]
HAND_V = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]


def cmd_attention_demo(args):
    import torch
    q, k, v = (torch.tensor(t) for t in (HAND_Q, HAND_K, HAND_V))
    d_head = q.shape[-1]
    print(f'3 tokens, d_head = {d_head}, scale = 1/sqrt({d_head}) = {1 / math.sqrt(d_head)}')
    scores = q @ k.T / math.sqrt(d_head)
    print('scores = Q K^T / sqrt(d_head):')
    for row in scores: print('  ', fmt(row, 2))
    mask = torch.triu(torch.ones(3, 3, dtype=torch.bool), 1)
    masked = scores.masked_fill(mask, float('-inf'))
    print('after causal mask (future positions -> -inf):')
    for row in masked: print('  ', '[' + ', '.join('-inf' if math.isinf(x) else f'{x:.2f}' for x in row) + ']')
    pattern = torch.softmax(masked, -1)
    print('pattern = softmax over each row:')
    for row in pattern: print('  ', fmt(row))
    out = pattern @ v
    print('output = pattern @ V:')
    for row in out: print('  ', fmt(row))
    sdpa = torch.nn.functional.scaled_dot_product_attention(q[None, None], k[None, None], v[None, None], is_causal=True)[0, 0]
    print(f'max |output - torch sdpa(is_causal=True)| = {(out - sdpa).abs().max():.1e}')


def cmd_heads(args):
    import torch
    tok, m = tokenizer(), model()
    ids = tok.encode(args.text)
    with torch.no_grad():
        out = m(torch.tensor([ids]), output_attentions=True)
    pattern = out.attentions[args.layer][0, args.head]
    pieces = [tok.decode([t]) for t in ids]
    print(f'layer {args.layer} head {args.head}, attention pattern shape {tuple(out.attentions[args.layer].shape)} = (batch, head, query, key)')
    print(' ' * 14 + ''.join(f'{p[:7]:>8}' for p in pieces))
    for i, row in enumerate(pattern):
        print(f'{pieces[i][:12]:>12}: ' + ''.join(f'{x:8.2f}' for x in row))
    print(f'row sums: {fmt(pattern.sum(-1), 2)}')
    attn = m.transformer.h[args.layer].attn
    W = attn.c_attn.weight
    d = m.config.n_embd
    dh = d // m.config.n_head
    s = slice(args.head * dh, (args.head + 1) * dh)
    W_Q, W_K, W_V = W[:, 0:d][:, s], W[:, d:2 * d][:, s], W[:, 2 * d:][:, s]
    W_O = attn.c_proj.weight[s, :]
    QK, OV = W_Q @ W_K.T, W_V @ W_O
    print(f'W_Q, W_K, W_V for this head: {tuple(W_Q.shape)} each; W_O rows for this head: {tuple(W_O.shape)}')
    print(f'QK circuit W_Q W_K^T: shape {tuple(QK.shape)}, rank {torch.linalg.matrix_rank(QK).item()}')
    print(f'OV circuit W_V W_O: shape {tuple(OV.shape)}, rank {torch.linalg.matrix_rank(OV).item()}')


# ---------------------------------------------------------------- MLPs
def cmd_mlp_demo(args):
    import torch
    tok, m = tokenizer(), model()
    ids = tok.encode(args.text)
    acts = {}
    h = m.transformer.h[args.layer].mlp.act.register_forward_hook(lambda mod, i, o: acts.setdefault('post', o))
    with torch.no_grad():
        m(torch.tensor([ids]))
    h.remove()
    post = acts['post'][0]
    print(f'layer {args.layer} MLP: c_fc.weight {tuple(m.transformer.h[args.layer].mlp.c_fc.weight.shape)}, '
          f'c_proj.weight {tuple(m.transformer.h[args.layer].mlp.c_proj.weight.shape)}')
    print(f'post-GELU activations shape {tuple(post.shape)} = (seq, d_mlp)')
    for pos, t in enumerate(ids):
        top = post[pos].topk(3)
        print(f'  pos {pos} {tok.decode([t])!r}: top neurons {top.indices.tolist()} values {fmt(top.values, 2)}; '
              f'fraction > 0: {(post[pos] > 0).float().mean():.2f}')
    for x in (-2.0, -1.0, 0.0, 1.0, 2.0):
        exact = 0.5 * x * (1 + math.erf(x / math.sqrt(2)))
        approx = 0.5 * x * (1 + math.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * x ** 3)))
        print(f'  gelu({x:+.0f}): exact {exact:+.4f}  tanh approximation (gelu_new) {approx:+.4f}')


def cmd_swiglu_demo(args):
    import torch
    x = torch.tensor([[1.0, 2.0]])
    W = torch.tensor([[2.0, 0.0], [-1.0, 1.0]])    # gate projection
    V = torch.tensor([[1.0, 1.0], [1.0, 0.0]])     # up projection
    W2 = torch.tensor([[1.0], [1.0]])              # down projection
    xW, xV = x @ W, x @ V
    print(f'x = {fmt(x[0], 1)}; xW (gate) = {fmt(xW[0], 1)}; xV (up) = {fmt(xV[0], 1)}')
    swish = xW * torch.sigmoid(xW)
    print(f'Swish_1(xW) = xW * sigmoid(xW) = {fmt(swish[0])}   (sigmoid(2) = {torch.sigmoid(torch.tensor(2.0)):.4f})')
    gated = swish * xV
    print(f'Swish_1(xW) * xV (elementwise) = {fmt(gated[0])}')
    print(f'FFN_SwiGLU(x) = (Swish_1(xW) * xV) W2 = {fmt((gated @ W2)[0])}')
    print(f'torch.nn.functional.silu agrees with Swish_1: {fmt(torch.nn.functional.silu(xW)[0])}')


# ---------------------------------------------------------------- unembedding
def cmd_logit_lens(args):
    import torch
    tok, m = tokenizer(), model()
    ids = tok.encode(args.text)
    with torch.no_grad():
        out = m(torch.tensor([ids]), output_hidden_states=True)
    pos = len(ids) - 1
    print(f'{args.text!r}: predicting what follows {tok.decode([ids[pos]])!r} (position {pos})')
    W_U = m.lm_head.weight
    print(f'lm_head.weight is transformer.wte.weight: {m.lm_head.weight.data_ptr() == m.transformer.wte.weight.data_ptr()}')
    for layer in range(12):
        resid = out.hidden_states[layer + 1][0, pos] if layer < 11 else None
        if layer == 11:
            resid = out.hidden_states[12][0, pos]  # hidden_states[12] is already after ln_f
            logits = resid @ W_U.T
        else:
            logits = m.transformer.ln_f(resid) @ W_U.T
        probs = logits.softmax(-1)
        top = probs.topk(3)
        print(f'  after block {layer:>2}: ' + '  '.join(f'{tok.decode([i])!r} {p:.3f}' for p, i in zip(top.values.tolist(), top.indices.tolist())))
    final = out.logits[0, pos]
    print(f'final logits: shape {tuple(out.logits.shape)}; max |logit lens at block 11 - model logits| = {(logits - final).abs().max():.1e}')


def cmd_softmax_demo(args):
    import torch
    z = torch.tensor([2.0, 1.0, 0.0])
    for T in (1.0, 2.0, 0.5):
        print(f'logits {fmt(z, 1)} / T={T}: softmax = {fmt(torch.softmax(z / T, -1))}')
    print(f'adding 10 to every logit changes nothing: {fmt(torch.softmax(z + 10, -1))}')


# ---------------------------------------------------------------- whole model
def cmd_config(args):
    m = model()
    c = m.config
    print(f'n_layer={c.n_layer} n_head={c.n_head} n_embd={c.n_embd} n_positions={c.n_positions} vocab_size={c.vocab_size} '
          f'activation={c.activation_function} layer_norm_epsilon={c.layer_norm_epsilon} tie_word_embeddings={c.tie_word_embeddings}')
    d, L, V, P, M = c.n_embd, c.n_layer, c.vocab_size, c.n_positions, 4 * c.n_embd
    wte, wpe = V * d, P * d
    ln = 2 * d
    attn = d * 3 * d + 3 * d + d * d + d
    mlp_ = d * M + M + M * d + d
    block = 2 * ln + attn + mlp_
    total = wte + wpe + L * block + ln
    print(f'wte = {V} x {d} = {wte:,}')
    print(f'wpe = {P} x {d} = {wpe:,}')
    print(f'per block: ln_1 {ln:,} + attn (c_attn {d * 3 * d + 3 * d:,} + c_proj {d * d + d:,}) + ln_2 {ln:,} + mlp (c_fc {d * M + M:,} + c_proj {M * d + d:,}) = {block:,}')
    print(f'{L} blocks = {L * block:,}; ln_f = {ln:,}')
    print(f'derived total = {total:,}')
    counted = sum(p.numel() for p in m.parameters())
    print(f'sum of parameter.numel() over the model = {counted:,}  (lm_head shares wte, so it is not counted twice)')
    print(f'match: {total == counted}')


def cmd_shapes(args):
    m = model()
    print(f'{"tensor":<36} {"shape":<16} {"params":>12}')
    total = 0
    for name, t in m.state_dict().items():
        if '.h.' in name and not name.startswith('transformer.h.0.'):
            continue
        n = t.numel(); total += 0 if name == 'lm_head.weight' else n
        print(f'{name:<36} {str(tuple(t.shape)):<16} {n:>12,}' + ('   (tied to wte; not counted)' if name == 'lm_head.weight' else ''))
    print('transformer.h.1 ... transformer.h.11 repeat the twelve h.0 tensors with the same shapes.')
    print(f'state_dict entries: {len(m.state_dict())}')


def cmd_generate(args):
    import torch
    tok, m = tokenizer(), model()
    ids = torch.tensor([tok.encode(args.text)])
    torch.manual_seed(args.seed)
    greedy = m.generate(ids, max_new_tokens=args.tokens, do_sample=False, pad_token_id=tok.eos_token_id)
    print(f'greedy:        {tok.decode(greedy[0])!r}')
    torch.manual_seed(args.seed)
    sampled = m.generate(ids, max_new_tokens=args.tokens, do_sample=True, temperature=args.temperature, top_k=0, pad_token_id=tok.eos_token_id)
    print(f'T={args.temperature}, seed {args.seed}: {tok.decode(sampled[0])!r}')
    # Greedy decoding by hand, with and without a KV cache, to show both agree.
    with torch.no_grad():
        out = m(ids, use_cache=True)
        past, cur, cached = out.past_key_values, out.logits[:, -1].argmax(-1, keepdim=True), []
        for _ in range(args.tokens):
            cached.append(cur.item())
            out = m(cur, past_key_values=past, use_cache=True)
            past, cur = out.past_key_values, out.logits[:, -1].argmax(-1, keepdim=True)
        seq, plain = ids, []
        for _ in range(args.tokens):
            nxt = m(seq).logits[:, -1].argmax(-1, keepdim=True)
            plain.append(nxt.item()); seq = torch.cat([seq, nxt], 1)
    print(f'hand-rolled greedy with KV cache:    {cached}')
    print(f'hand-rolled greedy recomputing all:  {plain}')
    print(f'identical: {cached == plain}; cache holds {len(past)} layers of (key, value), key shape {tuple(past.layers[0].keys.shape) if hasattr(past, "layers") else tuple(past[0][0].shape)}')


# ---------------------------------------------------------------- tooling
def cmd_names(args):
    """Verify the activation naming map across Hugging Face, TransformerLens 4, and nnsight."""
    import torch
    import importlib.metadata as md
    tok, hf = tokenizer(), model()
    ids = torch.tensor([tok.encode(args.text)])
    with torch.no_grad():
        ref = hf(ids, output_hidden_states=True, output_attentions=True)
    print(f'versions: transformers {md.version("transformers")}, transformer_lens {md.version("transformer_lens")}, nnsight {md.version("nnsight")}, torch {md.version("torch")}')
    from transformer_lens import TransformerBridge
    bridge = TransformerBridge.boot_transformers('gpt2')
    bridge.enable_compatibility_mode(no_processing=args.processing == 'none', disable_warnings=True)
    logits_tl, cache = bridge.run_with_cache(ids)
    from nnsight import TransformersModel
    nn = TransformersModel('gpt2', task='text-generation', device_map='cpu', dispatch=True)
    L = args.layer
    with nn.trace(ids):
        n_embed = nn.transformer.wte.output.save()
        n_pos = nn.transformer.wpe.output.save()
        n_in = nn.transformer.h[L].input.save()
        n_attn = nn.transformer.h[L].attn.output[0].save()
        n_mlp = nn.transformer.h[L].mlp.output.save()
        n_block = nn.transformer.h[L].output.save()
        n_lnf = nn.transformer.ln_f.output.save()
        n_logits = nn.lm_head.output.save()
    mlp_post = {}
    h = hf.transformer.h[L].mlp.act.register_forward_hook(lambda mod, i, o: mlp_post.setdefault('v', o))
    with torch.no_grad():
        hf(ids)
    h.remove()
    hf_resid_post = ref.hidden_states[L + 1] if L < 11 else None
    rows = [
        ('token embedding', 'wte(ids)', 'hook_embed', 'transformer.wte.output', hf.transformer.wte(ids), cache['hook_embed'], n_embed),
        ('position embedding', 'wpe(pos)', 'hook_pos_embed', 'transformer.wpe.output', hf.transformer.wpe(torch.arange(ids.shape[1]))[None], cache['hook_pos_embed'], n_pos),
        (f'residual into block {L}', f'hidden_states[{L}]', f'blocks.{L}.hook_resid_pre', f'transformer.h[{L}].input', ref.hidden_states[L], cache[f'blocks.{L}.hook_resid_pre'], n_in),
        (f'attention output {L}', '(hook)', f'blocks.{L}.hook_attn_out', f'transformer.h[{L}].attn.output[0]', n_attn, cache[f'blocks.{L}.hook_attn_out'], n_attn),
        (f'attention pattern {L}', f'attentions[{L}]', f'blocks.{L}.attn.hook_pattern', '(hook)', ref.attentions[L], cache[f'blocks.{L}.attn.hook_pattern'], ref.attentions[L]),
        (f'MLP activations {L}', '(hook on mlp.act)', f'blocks.{L}.mlp.hook_post', f'transformer.h[{L}].mlp.act.output', mlp_post['v'], cache[f'blocks.{L}.mlp.hook_post'], mlp_post['v']),
        (f'MLP output {L}', '(hook)', f'blocks.{L}.hook_mlp_out', f'transformer.h[{L}].mlp.output', n_mlp, cache[f'blocks.{L}.hook_mlp_out'], n_mlp),
        (f'residual after block {L}', f'hidden_states[{L + 1}]' if L < 11 else '(not exposed: [12] is after ln_f)', f'blocks.{L}.hook_resid_post', f'transformer.h[{L}].output', hf_resid_post if hf_resid_post is not None else n_block, cache[f'blocks.{L}.hook_resid_post'], n_block),
        ('after final layer norm', 'hidden_states[12]', 'ln_final.hook_out', 'transformer.ln_f.output', ref.hidden_states[12], cache['ln_final.hook_out'], n_lnf),
        ('logits', 'logits', 'output of run_with_cache', 'lm_head.output', ref.logits, logits_tl, n_logits),
    ]
    print(f'prompt {args.text!r}, {ids.shape[1]} tokens, block {L}, TransformerLens processing: {args.processing}')
    print(f'{"activation":<24} {"Hugging Face":<22} {"TransformerLens":<32} {"nnsight":<34} {"shape":<16} {"max|HF-TL|":>10} {"max|HF-nn|":>10}')
    for label, hfn, tln, nnn, a, b, c in rows:
        print(f'{label:<24} {hfn:<22} {tln:<32} {nnn:<34} {str(tuple(a.shape)):<16} {(a - b).abs().max():>10.1e} {(a - c).abs().max():>10.1e}')
    pre = cache['ln_final.hook_normalized']
    w, b = hf.transformer.ln_f.weight, hf.transformer.ln_f.bias
    print(f'note: ln_final.hook_normalized is before the affine step: max |hook_normalized * weight + bias - hidden_states[12]| = {(pre * w + b - ref.hidden_states[12]).abs().max():.1e}; '
          f'the same holds for blocks.N.ln1.hook_normalized and ln2.hook_normalized')
    if args.processing == 'default':
        d = ref.logits - logits_tl
        print(f'with default processing: logits differ by a per-position constant (center_unembed): max|diff - row mean| = {(d - d.mean(-1, keepdim=True)).abs().max():.1e}; '
              f'log-softmax max diff = {(ref.logits.log_softmax(-1) - logits_tl.log_softmax(-1)).abs().max():.1e}')
        r, hh = cache[f'blocks.{L}.hook_resid_post'], n_block
        print(f'resid_post after removing each vector\'s mean over d_model (center_writing_weights): max diff = {((r - r.mean(-1, keepdim=True)) - (hh - hh.mean(-1, keepdim=True))).abs().max():.1e}')
    print(f'note: bridge.to_tokens(text) prepends <|endoftext|> (50256) as BOS by default: {bridge.to_tokens(args.text)[0, :3].tolist()}; this run passed the Hugging Face ids directly, with no BOS, to all three libraries')
    print(f'TransformerLens cache has {len(cache)} entries; block-{L} entries: ' + ', '.join(k.removeprefix(f'blocks.{L}.') for k in cache if k.startswith(f'blocks.{L}.')))


def cmd_compare(args):
    """Compare a from-scratch forward pass against transformers, TransformerLens 4, and nnsight."""
    import torch
    if args.reference:
        sys.path.insert(0, str(LABS / 'reference'))
        import gpt2_from_scratch_reference as impl
        print('using labs/reference/gpt2_from_scratch_reference.py (the author\'s solution)')
    else:
        sys.path.insert(0, str(LABS))
        import gpt2_from_scratch as impl
        print('using labs/gpt2_from_scratch.py (your implementation)')
    tok, hf = tokenizer(), model()
    ids = torch.tensor([tok.encode(args.text)])
    params = impl.load_params()
    with torch.no_grad():
        ref = hf(ids, output_hidden_states=True, output_attentions=True)
        logits, cache = impl.forward_with_cache(ids, params)
    print(f'{args.text!r}: {ids.shape[1]} tokens; logits shape {tuple(logits.shape)}')
    print(f'max |logits - transformers logits| = {(logits - ref.logits).abs().max():.2e}  (largest |logit| = {ref.logits.abs().max():.1f})')
    print(f'argmax next token agrees at every position: {(logits.argmax(-1) == ref.logits.argmax(-1)).all().item()}')
    for i in (0, 5, 10):
        print(f'max |resid_post.{i} - hidden_states[{i + 1}]| = {(cache[f"resid_post.{i}"] - ref.hidden_states[i + 1]).abs().max():.2e}; '
              f'max |pattern.{i} - attentions[{i}]| = {(cache[f"pattern.{i}"] - ref.attentions[i]).abs().max():.2e}')
    print(f'max |ln_final - hidden_states[12]| = {(cache["ln_final"] - ref.hidden_states[12]).abs().max():.2e}')
    if args.tools:
        from transformer_lens import TransformerBridge
        bridge = TransformerBridge.boot_transformers('gpt2')
        bridge.enable_compatibility_mode(no_processing=True, disable_warnings=True)
        tl_logits, tl_cache = bridge.run_with_cache(ids)
        print(f'TransformerLens (no_processing): max |resid_post.5 - blocks.5.hook_resid_post| = {(cache["resid_post.5"] - tl_cache["blocks.5.hook_resid_post"]).abs().max():.2e}; '
              f'max |mlp_post.5 - blocks.5.mlp.hook_post| = {(cache["mlp_post.5"] - tl_cache["blocks.5.mlp.hook_post"]).abs().max():.2e}; '
              f'max |logits - TL logits| = {(logits - tl_logits).abs().max():.2e}')
        from nnsight import TransformersModel
        nn = TransformersModel('gpt2', task='text-generation', device_map='cpu', dispatch=True)
        with nn.trace(ids):
            n5 = nn.transformer.h[5].output.save()
            nl = nn.lm_head.output.save()
        print(f'nnsight: max |resid_post.5 - transformer.h[5].output| = {(cache["resid_post.5"] - n5).abs().max():.2e}; max |logits - lm_head.output| = {(logits - nl).abs().max():.2e}')
    top = logits[0, -1].softmax(-1).topk(3)
    print('top next tokens: ' + ', '.join(f'{tok.decode([i])!r} {p:.3f}' for p, i in zip(top.values.tolist(), top.indices.tolist())))


# ---------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='command', required=True)
    p = sub.add_parser('tokens', help='show GPT-2 token ids and pieces'); p.add_argument('text', nargs='+'); p.add_argument('--compare', nargs=2, metavar=('A', 'B')); p.set_defaults(fn=cmd_tokens)
    p = sub.add_parser('bpe-demo', help='train a toy byte-pair encoder step by step'); p.add_argument('--merges', type=int, default=3); p.set_defaults(fn=cmd_bpe_demo)
    p = sub.add_parser('embed', help='token and position embeddings for a prompt'); p.add_argument('text', nargs='?', default=PROMPT); p.add_argument('--positions', type=int, default=2); p.set_defaults(fn=cmd_embed)
    p = sub.add_parser('stream', help='residual stream norms layer by layer'); p.add_argument('text', nargs='?', default=PROMPT); p.add_argument('--position', type=int, default=-1); p.set_defaults(fn=cmd_stream)
    p = sub.add_parser('layernorm-demo', help='LayerNorm, RMSNorm, and folding on a 4-vector'); p.set_defaults(fn=cmd_layernorm_demo)
    p = sub.add_parser('attention-demo', help='one head on a 3-token pencil example'); p.set_defaults(fn=cmd_attention_demo)
    p = sub.add_parser('heads', help='one real GPT-2 attention pattern and its QK/OV circuits'); p.add_argument('text', nargs='?', default=PROMPT); p.add_argument('--layer', type=int, default=0); p.add_argument('--head', type=int, default=0); p.set_defaults(fn=cmd_heads)
    p = sub.add_parser('mlp-demo', help='MLP activations and GELU values'); p.add_argument('text', nargs='?', default=PROMPT); p.add_argument('--layer', type=int, default=0); p.set_defaults(fn=cmd_mlp_demo)
    p = sub.add_parser('swiglu-demo', help='SwiGLU on a 2-vector'); p.set_defaults(fn=cmd_swiglu_demo)
    p = sub.add_parser('logit-lens', help='unembed every block\'s residual stream'); p.add_argument('text', nargs='?', default=PROMPT); p.set_defaults(fn=cmd_logit_lens)
    p = sub.add_parser('softmax-demo', help='softmax and temperature on three logits'); p.set_defaults(fn=cmd_softmax_demo)
    p = sub.add_parser('config', help='derive the parameter count from the config'); p.set_defaults(fn=cmd_config)
    p = sub.add_parser('shapes', help='every tensor in the state dict with its shape'); p.set_defaults(fn=cmd_shapes)
    p = sub.add_parser('generate', help='greedy and sampled generation, with and without a KV cache'); p.add_argument('text', nargs='?', default=PROMPT); p.add_argument('--tokens', type=int, default=6); p.add_argument('--temperature', type=float, default=1.0); p.add_argument('--seed', type=int, default=0); p.set_defaults(fn=cmd_generate)
    p = sub.add_parser('names', help='verify activation names across HF, TransformerLens 4, and nnsight'); p.add_argument('text', nargs='?', default=PROMPT); p.add_argument('--layer', type=int, default=5); p.add_argument('--processing', choices=['none', 'default'], default='none'); p.set_defaults(fn=cmd_names)
    p = sub.add_parser('compare', help='compare labs/gpt2_from_scratch.py with the reference model'); p.add_argument('text', nargs='?', default=PROMPT); p.add_argument('--reference', action='store_true'); p.add_argument('--tools', action='store_true'); p.set_defaults(fn=cmd_compare)
    args = ap.parse_args(argv)
    args.fn(args)


if __name__ == '__main__':
    main()
