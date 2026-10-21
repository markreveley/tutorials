"""Top-k versus quantile sampling for one GPT-2 small MLP neuron.

Shows the ten strongest activations (the usual "max-activating examples") and
then random tokens drawn from fixed activation quantile bands, so the learner can
see how much of the neuron's behaviour the top-k view leaves out.

Run:  python labs/reference/maxact.py --layer 0 --neuron 0
"""
import argparse

import numpy as np

from gpt2_common import corpus_chunks, load_gpt2, mlp_acts


def context(strs, i, width=4):
    left = ''.join(strs[max(0, i - width):i]).replace('\n', '\\n')
    tok = strs[i].replace('\n', '\\n')
    right = ''.join(strs[i + 1:i + 3]).replace('\n', '\\n')
    return f'{left}[{tok}]{right}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--layer', type=int, required=True)
    ap.add_argument('--neuron', type=int, required=True)
    ap.add_argument('--k', type=int, default=10)
    args = ap.parse_args()
    model = load_gpt2()
    train, test, _ = corpus_chunks(model)
    acts, strs = mlp_acts(model, train + test, args.layer)
    a = acts[:, args.neuron]
    n = len(a)
    print(f'layer {args.layer} neuron {args.neuron}: {n} tokens; activation mean {a.mean():.3f}, '
          f'sd {a.std():.3f}, max {a.max():.3f}; fraction > 0: {(a > 0).mean():.3f}; '
          f'fraction > 0.5*max: {(a > 0.5 * a.max()).mean():.4f}')
    print(f'\nTop {args.k} activations (what a max-activating-examples view shows):')
    for i in np.argsort(-a)[:args.k]:
        print(f'  {a[i]:7.3f}  {context(strs, i)}')
    rng = np.random.default_rng(0)
    qs = [(0.99, 1.0), (0.9, 0.99), (0.5, 0.9), (0.0, 0.5)]
    print('\nRandom tokens from activation quantile bands (what the top-k view hides):')
    for lo, hi in qs:
        lo_v, hi_v = np.quantile(a, lo), np.quantile(a, hi)
        idx = np.where((a >= lo_v) & (a <= hi_v))[0]
        pick = rng.choice(idx, size=min(4, len(idx)), replace=False)
        print(f'  band {lo:.2f}-{hi:.2f} (activation {lo_v:.3f} to {hi_v:.3f}, {len(idx)} tokens):')
        for i in sorted(pick, key=lambda i: -a[i]):
            print(f'    {a[i]:7.3f}  {context(strs, i)}')


if __name__ == '__main__':
    main()
