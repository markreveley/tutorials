"""Detect induction heads in GPT-2 small with a pre-registered test on repeated
random tokens (the definition used by Olsson et al. 2022).

Sequence: BOS + R + R where R is 50 uniformly random tokens. For a head, the
prefix-matching score is the mean attention from each token in the second copy
to the token that followed its earlier occurrence (offset = len(R) - 1).

Pre-registered: at least one head scores >= 0.5; on a non-repeated control
sequence (BOS + R + R' with R' fresh random tokens) the same heads score below
0.1 at that offset; and the model's average loss on the second copy is lower than
on the first copy (in-context learning on the repeat).

Run:  python labs/reference/induction_run.py
"""
import numpy as np
import torch

from gpt2_common import load_gpt2
from sol_induction import control_sequence, prefix_matching_score, repeated_sequence, verdict

SEQ, SEEDS = 50, 5
THRESHOLD = 0.5


def main():
    model = load_gpt2()
    n_layers, n_heads = model.cfg.n_layers, model.cfg.n_heads
    rep = torch.zeros(n_layers, n_heads); ctrl = torch.zeros(n_layers, n_heads)
    loss_first, loss_second = [], []
    for seed in range(SEEDS):
        toks = repeated_sequence(SEQ, seed, model.tokenizer.bos_token_id)
        toks_ctrl = control_sequence(SEQ, seed, model.tokenizer.bos_token_id)
        with torch.no_grad():
            logits, cache = model.run_with_cache(toks)
            _, cache_c = model.run_with_cache(toks_ctrl)
        lp = torch.log_softmax(logits[0], -1)
        nll = -lp[torch.arange(2 * SEQ), toks[0, 1:]]
        loss_first.append(nll[:SEQ].mean().item()); loss_second.append(nll[SEQ:].mean().item())
        for layer in range(n_layers):
            rep[layer] += prefix_matching_score(cache[f'blocks.{layer}.attn.hook_pattern'][0], SEQ) / SEEDS
            ctrl[layer] += prefix_matching_score(cache_c[f'blocks.{layer}.attn.hook_pattern'][0], SEQ) / SEEDS
    print(f'{SEEDS} random sequences of {SEQ} tokens, repeated once. Loss per token: first copy '
          f'{np.mean(loss_first):.2f}, second copy {np.mean(loss_second):.2f}')
    print('\nprefix-matching score, repeated sequence (rows: layers, columns: heads):')
    for layer in range(n_layers):
        print(f'  L{layer:<2} ' + ' '.join(f'{v:.2f}' for v in rep[layer].tolist()))
    v = verdict(rep, ctrl, float(np.mean(loss_first)), float(np.mean(loss_second)), threshold=THRESHOLD)
    hits = v['heads']
    print(f'\nheads with score >= {THRESHOLD}: {hits}')
    print('same heads on the non-repeated control sequence:')
    for l, h in hits:
        print(f'  L{l}H{h}: repeated {rep[l, h]:.2f}, control {ctrl[l, h]:.2f}')
    print(f'pre-registered test: {"pass" if v["passed"] else "FAIL"}')


if __name__ == '__main__':
    main()
