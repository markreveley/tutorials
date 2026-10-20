"""Author's reference solution for labs/gpt2_from_scratch.py.

It exists so that the course can show verified terminal output for the capstone
before the learner has written their own. The learner-facing file is a stub.
Set LAB_IMPL=reference to point the tests at this file (see labs/ASSESSMENTS.md).
"""
import math

import torch

CONFIG = dict(n_layer=12, n_head=12, d_model=768, d_mlp=3072, n_ctx=1024, d_vocab=50257, eps=1e-5)


def load_params(model_name='gpt2'):
    """Return GPT-2's weights as a flat dict of plain tensors keyed by Hugging Face names."""
    from transformers import GPT2LMHeadModel
    model = GPT2LMHeadModel.from_pretrained(model_name)
    params = {}
    for name, tensor in model.state_dict().items():
        if name == 'lm_head.weight':
            continue  # tied to transformer.wte.weight; see lesson 09
        params[name.removeprefix('transformer.')] = tensor.detach().clone()
    return params


def block_params(params, i):
    """Short names for the twelve tensors of block i."""
    p = f'h.{i}.'
    return dict(
        ln_1_w=params[p + 'ln_1.weight'], ln_1_b=params[p + 'ln_1.bias'],
        c_attn_w=params[p + 'attn.c_attn.weight'], c_attn_b=params[p + 'attn.c_attn.bias'],
        c_proj_w=params[p + 'attn.c_proj.weight'], c_proj_b=params[p + 'attn.c_proj.bias'],
        ln_2_w=params[p + 'ln_2.weight'], ln_2_b=params[p + 'ln_2.bias'],
        c_fc_w=params[p + 'mlp.c_fc.weight'], c_fc_b=params[p + 'mlp.c_fc.bias'],
        mlp_proj_w=params[p + 'mlp.c_proj.weight'], mlp_proj_b=params[p + 'mlp.c_proj.bias'],
    )


def layer_norm(x, weight, bias, eps=1e-5):
    mean = x.mean(-1, keepdim=True)
    var = x.var(-1, keepdim=True, unbiased=False)
    return (x - mean) / torch.sqrt(var + eps) * weight + bias


def gelu_new(x):
    return 0.5 * x * (1.0 + torch.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * x ** 3)))


def causal_attention(x, bp, n_head):
    batch, seq, d_model = x.shape
    d_head = d_model // n_head
    qkv = x @ bp['c_attn_w'] + bp['c_attn_b']
    q, k, v = qkv.split(d_model, dim=-1)
    q = q.view(batch, seq, n_head, d_head).transpose(1, 2)
    k = k.view(batch, seq, n_head, d_head).transpose(1, 2)
    v = v.view(batch, seq, n_head, d_head).transpose(1, 2)
    scores = q @ k.transpose(-1, -2) / math.sqrt(d_head)
    mask = torch.triu(torch.ones(seq, seq, dtype=torch.bool), diagonal=1)
    scores = scores.masked_fill(mask, float('-inf'))
    pattern = torch.softmax(scores, dim=-1)
    z = (pattern @ v).transpose(1, 2).reshape(batch, seq, d_model)
    return z @ bp['c_proj_w'] + bp['c_proj_b'], pattern


def mlp(x, bp):
    pre = x @ bp['c_fc_w'] + bp['c_fc_b']
    post = gelu_new(pre)
    return post @ bp['mlp_proj_w'] + bp['mlp_proj_b'], post


def forward_with_cache(tokens, params, cfg=CONFIG):
    if tokens.dim() == 1:
        tokens = tokens[None]
    seq = tokens.shape[1]
    cache = {}
    cache['embed'] = params['wte.weight'][tokens]
    cache['pos_embed'] = params['wpe.weight'][torch.arange(seq)][None]
    resid = cache['embed'] + cache['pos_embed']
    for i in range(cfg['n_layer']):
        bp = block_params(params, i)
        cache[f'resid_pre.{i}'] = resid
        attn_out, pattern = causal_attention(layer_norm(resid, bp['ln_1_w'], bp['ln_1_b'], cfg['eps']), bp, cfg['n_head'])
        cache[f'pattern.{i}'] = pattern
        cache[f'attn_out.{i}'] = attn_out
        resid = resid + attn_out
        cache[f'resid_mid.{i}'] = resid
        mlp_out, post = mlp(layer_norm(resid, bp['ln_2_w'], bp['ln_2_b'], cfg['eps']), bp)
        cache[f'mlp_post.{i}'] = post
        cache[f'mlp_out.{i}'] = mlp_out
        resid = resid + mlp_out
        cache[f'resid_post.{i}'] = resid
    cache['ln_final'] = layer_norm(resid, params['ln_f.weight'], params['ln_f.bias'], cfg['eps'])
    logits = cache['ln_final'] @ params['wte.weight'].T
    return logits, cache


def forward(tokens, params, cfg=CONFIG):
    return forward_with_cache(tokens, params, cfg)[0]
