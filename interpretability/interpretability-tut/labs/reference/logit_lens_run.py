"""Logit lens and direct logit attribution on GPT-2 small.

Logit lens: apply the final layer norm and the unembedding to the residual stream
after each block and read the top token and the KL divergence to the final
distribution. Direct logit attribution: project each block's attention and MLP
output (through the final layer norm scale) onto the unembedding row of the
target token, so the contributions sum to the final logit.

Run:  python labs/reference/logit_lens_run.py --prompt "The capital of France is"
"""
import argparse

import torch

from gpt2_common import load_gpt2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prompt', default='The capital of France is')
    ap.add_argument('--target', default=' Paris')
    args = ap.parse_args()
    model = load_gpt2()
    toks = model.to_tokens(args.prompt)
    with torch.no_grad():
        logits, cache = model.run_with_cache(toks)
    final = torch.log_softmax(logits[0, -1], -1)
    target = model.to_single_token(args.target)
    print(f'prompt {args.prompt!r}; final top token {model.to_string(final.argmax())!r}, '
          f'target {args.target!r} rank {(final > final[target]).sum().item() + 1}')
    print(f'\n{"after":>8} {"top token":>14} {"p(top)":>7} {"p(target)":>9} {"KL to final":>11}')
    W_U = model.W_U  # [d_model, vocab]
    for layer in range(model.cfg.n_layers):
        resid = cache[f'blocks.{layer}.hook_resid_post'][0, -1]
        with torch.no_grad():
            lens = torch.log_softmax(model.ln_final(resid[None, None])[0, 0] @ W_U + model.b_U, -1)
        kl = float((final.exp() * (final - lens)).sum())
        top = lens.argmax()
        print(f'{"block " + str(layer):>8} {model.to_string(top)!r:>14} {lens[top].exp():7.3f} '
              f'{lens[target].exp():9.3f} {kl:11.3f}')
    # Direct logit attribution. The final layer norm is x -> (x - mean(x)) / scale * w + b,
    # and centring is linear, so each component's contribution is ((c - mean(c)) * w / scale) @ u.
    scale = cache['ln_final.hook_scale'][0, -1].detach()
    w, b = model.ln_final.w.detach(), model.ln_final.b.detach()
    u = W_U[:, target].detach()

    def dla(c):
        c = c.detach()
        return float(((c - c.mean()) * w / scale) @ u)

    print(f'\nDirect logit attribution to {args.target!r} (each part passed through the final layer norm):')
    total = 0.0
    for layer in range(model.cfg.n_layers):
        attn = dla(cache[f'blocks.{layer}.hook_attn_out'][0, -1])
        mlp = dla(cache[f'blocks.{layer}.hook_mlp_out'][0, -1])
        total += attn + mlp
        print(f'  block {layer:>2}: attention {attn:+7.2f}   mlp {mlp:+7.2f}')
    embed = dla(cache['hook_embed'][0, -1] + cache['hook_pos_embed'][0, -1])
    bias = float(b @ u + model.b_U[target])
    print(f'  embeddings {embed:+7.2f}; layer-norm and unembed biases {bias:+7.2f}')
    print(f'  sum of parts {total + embed + bias:+7.2f}; logit from the forward pass {float(logits[0, -1, target]):+7.2f}')


if __name__ == '__main__':
    main()
