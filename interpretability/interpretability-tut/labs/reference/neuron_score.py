"""Score rule-form explanations of GPT-2 small MLP neurons by held-out prediction.

Procedure (documented so it can be repeated):
  1. Tokenise labs/data/corpus.txt; even 128-token chunks are the screening split,
     odd chunks are held out and are not touched until step 4.
  2. For each rule (a deterministic token predicate), find the neuron in every
     layer whose activation correlates best with the rule on the screening split.
     This is where selection bias enters: 12 x 3072 neurons were searched.
  3. Pre-register, per rule: held-out Pearson r >= 0.5, AND r above the 95th
     percentile of (a) 200 random neurons from the same layer and (b) 500 shuffled
     copies of the rule's labels.
  4. Score on the held-out split and print everything, including failures.

Run:  python labs/reference/neuron_score.py --rule digit
      python labs/reference/neuron_score.py --all
"""
import argparse

import numpy as np

from gpt2_common import corpus_chunks, load_gpt2, mlp_acts, pearson, token_rules
from sol_explanation_score import random_unit_control, shuffled_control, verdict

THRESHOLD = 0.5
N_RANDOM = 200
N_SHUFFLE = 500


def screen(model, train, rules):
    """Return {rule: (layer, neuron, train_r)} by exhaustive correlation search."""
    best = {r: (None, None, -1.0) for r in rules}
    for layer in range(model.cfg.n_layers):
        acts, strs = mlp_acts(model, train, layer)
        labels = token_rules(strs)
        a = acts - acts.mean(0); a_norm = np.linalg.norm(a, axis=0) + 1e-9
        for r in rules:
            y = labels[r]
            if y.std() == 0:
                continue
            yc = y - y.mean()
            corr = (a.T @ yc) / (a_norm * np.linalg.norm(yc))
            j = int(np.argmax(corr))
            if corr[j] > best[r][2]:
                best[r] = (layer, j, float(corr[j]))
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rule', default='digit')
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()
    model = load_gpt2()
    train, test, n_tok = corpus_chunks(model)
    rules = list(token_rules(['x']).keys()) if args.all else [args.rule]
    print(f'corpus: {n_tok} tokens -> {len(train)} screening chunks, {len(test)} held-out chunks of 128')
    print(f'pre-registered: held-out r >= {THRESHOLD} and above the 95th percentile of '
          f'{N_RANDOM} random same-layer neurons and of {N_SHUFFLE} label shuffles')
    best = screen(model, train, rules)
    print(f'\n{"rule":>13} {"layer":>5} {"neuron":>6} {"train r":>8} {"held-out r":>10} {"rand95":>7} {"shuf95":>7} {"|rand|max":>9}  base rate  verdict')
    for r in rules:
        layer, j, tr = best[r]
        if layer is None:
            print(f'{r:>13}  (rule never fires on the screening split)'); continue
        acts, strs = mlp_acts(model, test, layer)
        y = token_rules(strs)[r]
        if y.std() == 0:
            print(f'{r:>13} {layer:>5} {j:>6} {tr:>8.3f}   rule never fires on held-out split'); continue
        hr = pearson(acts[:, j], y)
        rand = random_unit_control(acts, y, j, n=N_RANDOM, seed=0)
        shuf = shuffled_control(acts[:, j], y, n=N_SHUFFLE, seed=0)
        v = verdict(hr, rand, shuf, THRESHOLD)
        r95, s95, rmax, ok = v['random_p95'], v['shuffled_p95'], float(np.abs(rand).max()), v['demonstrated']
        print(f'{r:>13} {layer:>5} {j:>6} {tr:>8.3f} {hr:>10.3f} {r95:>7.3f} {s95:>7.3f} {rmax:>9.3f}  {y.mean():>9.3f}  '
              f'{"demonstrated" if ok else "NOT demonstrated"}')


if __name__ == '__main__':
    main()
