"""Activation patching on GPT-2 small with a clean/corrupted prompt pair.

Clean:     "The capital of France is"  -> expected " Paris"
Corrupted: "The capital of Italy is"   -> expected " Rome"
Metric: logit(" Paris") - logit(" Rome") at the final position. We run the
corrupted prompt and patch in the clean residual stream (hook_resid_post) at one
layer and one position, then report how much of the clean-minus-corrupted metric
gap is recovered.

Pre-registered: patching at the country token position recovers > 50% of the gap
at some layer; patching at position 0 ("The") recovers < 10% at every layer
(control: a position that carries no information about the country).

Run:  python labs/reference/patch_run.py
"""
import torch

from gpt2_common import load_gpt2
from sol_patching import make_patch_hook, recovered_fraction, verdict

CLEAN, CORRUPT = 'The capital of France is', 'The capital of Italy is'


def metric(model, logits, a=' Paris', b=' Rome'):
    ia, ib = model.to_single_token(a), model.to_single_token(b)
    return float(logits[0, -1, ia] - logits[0, -1, ib])


def main():
    model = load_gpt2()
    clean, corrupt = model.to_tokens(CLEAN), model.to_tokens(CORRUPT)
    assert clean.shape == corrupt.shape, 'prompts must tokenise to the same length'
    strs = model.to_str_tokens(CLEAN)
    print('tokens:', strs)
    with torch.no_grad():
        clean_logits, clean_cache = model.run_with_cache(clean)
        corrupt_logits = model(corrupt)
    m_clean, m_corrupt = metric(model, clean_logits), metric(model, corrupt_logits)
    print(f'metric logit(Paris)-logit(Rome): clean {m_clean:+.3f}, corrupted {m_corrupt:+.3f}')
    country_pos = [i for i, s in enumerate(strs) if s.strip() == 'France'][0]
    print(f'{"layer":>5} ' + ' '.join(f'{"pos" + str(p):>8}' for p in range(clean.shape[1])) + '   (recovered fraction)')
    table = {}
    for layer in range(model.cfg.n_layers):
        name = f'blocks.{layer}.hook_resid_post'
        row = []
        for pos in range(clean.shape[1]):
            hook = make_patch_hook(clean_cache[name], pos)
            with torch.no_grad():
                patched = model.run_with_hooks(corrupt, fwd_hooks=[(name, hook)])
            row.append(recovered_fraction(m_clean, m_corrupt, metric(model, patched)))
        table[layer] = row
        print(f'{layer:>5} ' + ' '.join(f'{f:>8.2f}' for f in row))
    v = verdict(table, country_pos, 0)
    print(f'\ncountry position (index {country_pos}): best recovery {v["best_claim"]:.2f} -> '
          f'{"pass" if v["claim_passed"] else "FAIL"} (> 0.50 pre-registered)')
    print(f'position 0 control: largest recovery {v["worst_control"]:.2f} -> '
          f'{"pass" if v["control_passed"] else "FAIL"} (< 0.10 pre-registered)')


if __name__ == '__main__':
    main()
