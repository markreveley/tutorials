"""Shared GPT-2 small helpers for the language experiments (reference code).

Loads GPT-2 small through TransformerLens 4 (TransformerBridge + compatibility
mode), tokenises the course corpus, and splits it into alternating 128-token
chunks: even chunks are the screening ("train") split, odd chunks are held out.
"""
import os
import re
from pathlib import Path

import numpy as np
import torch

os.environ.setdefault('HF_HUB_OFFLINE', '1')
os.environ.setdefault('TRANSFORMERS_VERBOSITY', 'error')
os.environ.setdefault('HF_HUB_DISABLE_PROGRESS_BARS', '1')

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / 'labs' / 'data' / 'corpus.txt'
CHUNK = 128


def load_gpt2():
    import logging
    logging.disable(logging.WARNING)
    from transformer_lens import TransformerBridge
    torch.manual_seed(0)
    model = TransformerBridge.boot_transformers('gpt2')
    model.enable_compatibility_mode()
    model.eval()
    return model


def corpus_chunks(model, text=None, chunk=CHUNK):
    """Return (train_chunks, test_chunks); each chunk is a 1-D LongTensor of
    `chunk` token ids with no BOS prepended (positions are relative to chunk)."""
    text = text if text is not None else CORPUS.read_text()
    # model.to_tokens truncates to the context window; use the tokenizer directly.
    toks = torch.tensor(model.tokenizer(text)['input_ids'])
    n = toks.shape[0] // chunk
    chunks = [toks[i * chunk:(i + 1) * chunk] for i in range(n)]
    return chunks[0::2], chunks[1::2], toks.shape[0]


PUNCT = {'.', ',', ';', ':', '?', '!'}


def token_rules(str_tokens):
    """Deterministic per-token indicators ("explanations" in rule form).
    Each rule maps a token's text and its predecessor to 0/1."""
    n = len(str_tokens)
    rules = {name: np.zeros(n, dtype=np.float32) for name in
             ('digit', 'capital', 'newline', 'punct', 'after_period', 'quote', 'the', 'space_word')}
    for i, t in enumerate(str_tokens):
        s = t.strip()
        prev = str_tokens[i - 1] if i > 0 else ''
        rules['digit'][i] = float(s.isdigit() and s != '')
        rules['capital'][i] = float(t.startswith(' ') and len(s) > 0 and s[0].isupper())
        rules['newline'][i] = float('\n' in t)
        rules['punct'][i] = float(s in PUNCT)
        rules['after_period'][i] = float(prev.strip().endswith('.') or '\n' in prev)
        rules['quote'][i] = float('"' in t)
        rules['the'][i] = float(s.lower() == 'the')
        rules['space_word'][i] = float(t.startswith(' ') and s.isalpha())
    return rules


def pearson(x, y):
    x = np.asarray(x, dtype=np.float64); y = np.asarray(y, dtype=np.float64)
    if x.std() == 0 or y.std() == 0:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def mlp_acts(model, chunks, layer):
    """Concatenate post-nonlinearity MLP activations [tokens, d_mlp] for a layer."""
    out, strs = [], []
    name = f'blocks.{layer}.mlp.hook_post'
    with torch.no_grad():
        for c in chunks:
            _, cache = model.run_with_cache(c[None], names_filter=lambda n: n == name)
            out.append(cache[name][0].numpy())
            strs.extend(model.to_str_tokens(c))
    return np.concatenate(out), strs
