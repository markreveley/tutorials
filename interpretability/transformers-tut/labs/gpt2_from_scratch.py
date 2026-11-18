"""Capstone lab: GPT-2 small forward pass from raw weights.

Implement every function that raises NotImplementedError, then run:

    python -m unittest discover -s labs -p 'test_gpt2_from_scratch.py' -v
    python labs/anatomy.py compare --tools

`load_params` and `block_params` are given: loading weights is not the lesson.
Weight convention: Hugging Face stores GPT-2's linear layers as Conv1D with
weight shape (in_features, out_features), so a projection is `x @ W + b`.
"""
import math

import torch

CONFIG = dict(n_layer=12, n_head=12, d_model=768, d_mlp=3072, n_ctx=1024, d_vocab=50257, eps=1e-5)


def load_params(model_name='gpt2'):
    """Return GPT-2's weights as a flat dict of plain tensors keyed by Hugging Face names.

    Keys look like 'wte.weight', 'wpe.weight', 'h.0.ln_1.weight', ..., 'ln_f.bias'.
    'lm_head.weight' is dropped because it is the same tensor as 'wte.weight'.
    """
    from transformers import GPT2LMHeadModel
    model = GPT2LMHeadModel.from_pretrained(model_name)
    params = {}
    for name, tensor in model.state_dict().items():
        if name == 'lm_head.weight':
            continue
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
    """Normalise the last axis to mean 0 and variance 1 (population variance), then scale and shift."""
    raise NotImplementedError('lesson 04: subtract the mean, divide by sqrt(var + eps), multiply by weight, add bias')


def gelu_new(x):
    """GPT-2's tanh approximation of GELU: 0.5 x (1 + tanh(sqrt(2/pi) (x + 0.044715 x^3)))."""
    raise NotImplementedError('lesson 07')


def causal_attention(x, bp, n_head):
    """Multi-head causal self-attention on an already-normalised input.

    x: (batch, seq, d_model). bp: block_params(...) for this block.
    Returns (out, pattern): out is (batch, seq, d_model), the vector added to the
    residual stream; pattern is (batch, n_head, seq, seq) with rows summing to 1.
    """
    raise NotImplementedError('lessons 05-06: project to q,k,v; split heads; scale; mask; softmax; weight v; merge; project out')


def mlp(x, bp):
    """The MLP block. Returns (out, post): out is (batch, seq, d_model); post is the (batch, seq, d_mlp) activations after GELU."""
    raise NotImplementedError('lesson 07')


def forward_with_cache(tokens, params, cfg=CONFIG):
    """Run the model and keep every intermediate activation.

    Returns (logits, cache). logits: (batch, seq, d_vocab). cache keys:
    'embed', 'pos_embed', and for each block i: 'resid_pre.i', 'pattern.i',
    'attn_out.i', 'resid_mid.i', 'mlp_post.i', 'mlp_out.i', 'resid_post.i';
    then 'ln_final'. The tests compare these to transformers, TransformerLens, and nnsight.
    """
    raise NotImplementedError('lesson 10')


def forward(tokens, params, cfg=CONFIG):
    """Logits only."""
    return forward_with_cache(tokens, params, cfg)[0]
