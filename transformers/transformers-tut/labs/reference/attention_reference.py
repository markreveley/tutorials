"""Author's reference solution for labs/attention.py (see labs/ASSESSMENTS.md)."""
import math

import torch


def softmax(x, dim=-1):
    shifted = x - x.max(dim=dim, keepdim=True).values
    e = shifted.exp()
    return e / e.sum(dim=dim, keepdim=True)


def causal_mask(seq_len):
    return torch.tril(torch.ones(seq_len, seq_len, dtype=torch.bool))


def attention(q, k, v, causal=True):
    d_head = q.shape[-1]
    scores = q @ k.transpose(-1, -2) / math.sqrt(d_head)
    if causal:
        scores = scores.masked_fill(~causal_mask(q.shape[-2]), float('-inf'))
    pattern = softmax(scores, dim=-1)
    return pattern @ v, pattern


def split_heads(x, n_head):
    batch, seq, d_model = x.shape
    return x.view(batch, seq, n_head, d_model // n_head).transpose(1, 2)


def merge_heads(x):
    batch, n_head, seq, d_head = x.shape
    return x.transpose(1, 2).reshape(batch, seq, n_head * d_head)


def qk_circuit(W_Q, W_K):
    return W_Q @ W_K.T


def ov_circuit(W_V, W_O):
    return W_V @ W_O
