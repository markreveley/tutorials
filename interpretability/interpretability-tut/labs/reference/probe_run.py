"""Linear probe on GPT-2 small residual-stream activations with controls.

Label: the token is the first token of a sentence (its predecessor ends with a
full stop or contains a newline). Probe: logistic regression fitted by gradient
descent in numpy on the screening split; accuracy reported on the held-out split.
Controls: the same fit on shuffled labels (held-out accuracy should fall to the
majority-class rate) and a random direction with a fitted threshold.

Pre-registered: at layer 6 the probe beats the majority-class baseline by at
least 10 percentage points on held-out tokens and beats both controls.

Run:  python labs/reference/probe_run.py --layer 6 --rule after_period
"""
import argparse

import numpy as np
import torch

from gpt2_common import corpus_chunks, load_gpt2, token_rules
from sol_probe import (accuracy, fit_logistic, majority_rate, predict, random_direction_control,
                       shuffled_label_control, verdict)


def resid(model, chunks, layer):
    name = f'blocks.{layer}.hook_resid_post'
    xs, strs = [], []
    with torch.no_grad():
        for c in chunks:
            _, cache = model.run_with_cache(c[None], names_filter=lambda n: n == name)
            xs.append(cache[name][0].numpy()); strs.extend(model.to_str_tokens(c))
    return np.concatenate(xs).astype(np.float64), strs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--layer', type=int, default=6)
    ap.add_argument('--rule', default='after_period')
    ap.add_argument('--shuffles', type=int, default=20)
    args = ap.parse_args()
    model = load_gpt2()
    train, test, _ = corpus_chunks(model)
    xtr, str_tr = resid(model, train, args.layer); ytr = token_rules(str_tr)[args.rule].astype(np.float64)
    xte, str_te = resid(model, test, args.layer); yte = token_rules(str_te)[args.rule].astype(np.float64)
    majority = majority_rate(yte)
    print(f'layer {args.layer}, label "{args.rule}": train {len(ytr)} tokens ({ytr.mean():.3f} positive), '
          f'held-out {len(yte)} tokens ({yte.mean():.3f} positive); majority-class accuracy {majority:.3f}')
    probe = fit_logistic(xtr, ytr)
    acc_tr = accuracy(probe, xtr, ytr); acc_te = accuracy(probe, xte, yte)
    print(f'probe: train accuracy {acc_tr:.3f}, held-out accuracy {acc_te:.3f}')
    shuf = shuffled_label_control(xtr, ytr, xte, yte, n=args.shuffles, seed=0)
    print(f'shuffled-label control ({args.shuffles} fits): held-out accuracy mean {np.mean(shuf):.3f}, '
          f'max {np.max(shuf):.3f}')
    rand = random_direction_control(xtr, ytr, xte, yte, n=args.shuffles, seed=0)
    print(f'random-direction control ({args.shuffles} directions): held-out accuracy mean {np.mean(rand):.3f}, '
          f'max {np.max(rand):.3f}')
    ok = verdict(acc_te, majority, shuf, rand, margin=0.10)['passed']
    print(f'pre-registered test (held-out >= majority + 0.10 and above both controls): '
          f'{"pass" if ok else "FAIL"}')
    pred = predict(probe, xte)
    tpr = (pred[yte == 1] == 1).mean(); tnr = (pred[yte == 0] == 0).mean()
    print(f'exploratory, NOT pre-registered: held-out recall on positives {tpr:.3f}, on negatives {tnr:.3f}, '
          f'balanced accuracy {(tpr + tnr) / 2:.3f}; the largest gain over majority that any probe could '
          f'reach here is {1 - majority:.3f}')


if __name__ == '__main__':
    main()
