"""Attention lab: one head by hand, then the pieces a multi-head layer needs.

Implement every function that raises NotImplementedError, then run:

    python -m unittest discover -s labs -p 'test_attention.py' -v

Conventions: q, k, v have shape (..., seq, d_head); any leading axes (batch,
head) broadcast. Patterns have shape (..., seq_query, seq_key).
"""
import math

import torch


def softmax(x, dim=-1):
    """Numerically stable softmax: subtract the row max before exponentiating."""
    raise NotImplementedError('lesson 05')


def causal_mask(seq_len):
    """Boolean (seq_len, seq_len) tensor: True where query position i may attend to key position j (j <= i)."""
    raise NotImplementedError('lesson 05')


def attention(q, k, v, causal=True):
    """Scaled dot-product attention. Returns (out, pattern).

    scores = q k^T / sqrt(d_head); masked positions get -inf before the softmax;
    out = pattern @ v. Do not call torch.nn.functional.scaled_dot_product_attention;
    the tests compare against it.
    """
    raise NotImplementedError('lesson 05')


def split_heads(x, n_head):
    """(batch, seq, d_model) -> (batch, n_head, seq, d_head), with d_head = d_model // n_head."""
    raise NotImplementedError('lesson 06')


def merge_heads(x):
    """(batch, n_head, seq, d_head) -> (batch, seq, n_head * d_head). Inverse of split_heads."""
    raise NotImplementedError('lesson 06')


def qk_circuit(W_Q, W_K):
    """W_Q W_K^T: the (d_model, d_model) bilinear form that scores a query residual against a key residual.

    W_Q, W_K: (d_model, d_head) for one head.
    """
    raise NotImplementedError('lesson 06')


def ov_circuit(W_V, W_O):
    """W_V W_O: the (d_model, d_model) map from an attended residual vector to what the head writes.

    W_V: (d_model, d_head), W_O: (d_head, d_model) for one head.
    """
    raise NotImplementedError('lesson 06')
