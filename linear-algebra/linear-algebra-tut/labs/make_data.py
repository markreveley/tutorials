"""Generate the real activation fixture once. Learners do not need to run this.

Runs GPT-2 small (124M) on an original passage written for this course, caches
the residual stream after block 6 for every token, and writes:

  data/activations.npy  float16, shape (n_tokens, 768): hidden_states[7] from
                        transformers, which is the residual stream after block
                        6 (blocks.6.hook_resid_post in TransformerLens naming).
  data/tokens.json      the token strings, their ids, and positions.
  data/labels.json      simple per-token labels computed from the token strings.
  data/weights.npz      float16: the four weight matrices of one attention head
                        (layer 7, head 0): W_Q, W_K, W_V of shape (768, 64) and
                        W_O of shape (64, 768). These are real GPT-2 weights,
                        included so the matrix lessons act on real maps.
  data/meta.json        model, layer, versions, and passage statistics.

Usage (from the course directory, inside an environment with torch,
transformers, and numpy):

  python labs/make_data.py

The passage is original prose. It deliberately mixes dates, counts, and
sentence boundaries so that several easy labels exist for every token.
"""
import json
import platform
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parent / 'data'
MODEL = 'gpt2'
LAYER = 6  # residual stream after block 6 == hidden_states[LAYER + 1]
HEAD_LAYER, HEAD = 7, 0  # the attention head whose weights are saved; it reads the cached stream
D_HEAD = 64

PASSAGE = """The harbour town of Weston Hollow kept careful records. In 1842 the council counted 311 households, 4 mills, and 27 fishing boats. By 1871 the count had risen to 902 households and 63 boats. The old ledger lists every vessel by name.

Each spring the river rose about 2 metres and flooded the lower streets. The flood of 1896 reached 3.4 metres and destroyed 18 houses. After that year the town built a stone wall 640 metres long. It took 5 years and cost 12,000 pounds.

The school opened in 1903 with 48 pupils and 2 teachers. By 1930 it taught 215 children. A second building was added in 1951. The library next door holds 9,400 books and opens 6 days a week.

Trains arrived in 1888. The line carried 14 passenger services a day and 3 goods trains at night. The station closed in 1964, and the platform is now a garden with 40 rose bushes.

Today the town has 2,850 residents. The harbour still shelters 11 working boats. Visitors come in July and August, when the population roughly doubles. A ferry crosses to the island every 90 minutes, and the crossing takes 25 minutes in calm weather.

The museum keeps the original ledger in a glass case. Its pages record births, deaths, cargo, and weather. The entry for 14 March 1842 notes 7 inches of snow and a late tide. The entry for 2 June 1871 records the first steam engine seen in the bay."""


def labels_for(tokens):
    """Per-token binary labels computed from the token strings alone."""
    is_digit = [int(t.strip().isdigit()) for t in tokens]
    after_period = [0] + [int(tokens[i - 1].strip() in {'.', '?', '!'}) for i in range(1, len(tokens))]
    starts_with_space = [int(t.startswith(' ')) for t in tokens]
    capitalised = [int(t.strip()[:1].isupper()) for t in tokens]
    return dict(is_digit=is_digit, after_period=after_period,
                starts_with_space=starts_with_space, capitalised=capitalised)


def main():
    import torch
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer
    torch.manual_seed(0)
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL)
    model.eval()
    enc = tok(PASSAGE, return_tensors='pt')
    ids = enc['input_ids']
    with torch.no_grad():
        out = model(**enc, output_hidden_states=True)
    hidden = out.hidden_states[LAYER + 1][0]  # (n_tokens, 768), residual stream after block LAYER
    acts = hidden.to(torch.float16).numpy()
    tokens = [tok.decode([i]) for i in ids[0].tolist()]
    DATA.mkdir(exist_ok=True)
    np.save(DATA / 'activations.npy', acts)
    (DATA / 'tokens.json').write_text(json.dumps(dict(
        tokens=tokens, ids=ids[0].tolist(), positions=list(range(len(tokens)))), ensure_ascii=False, indent=0) + '\n')
    (DATA / 'labels.json').write_text(json.dumps(labels_for(tokens)) + '\n')
    # One real attention head's weights. In the transformers GPT-2 implementation
    # c_attn.weight has shape (768, 2304) = [Q | K | V] and head h uses columns
    # h*64:(h+1)*64 of each block; c_proj.weight has shape (768, 768) and head h's
    # output map is rows h*64:(h+1)*64. Biases are omitted: the lessons treat the
    # matrices as linear maps.
    block = model.transformer.h[HEAD_LAYER]
    w_attn = block.attn.c_attn.weight.detach()
    sl = slice(HEAD * D_HEAD, (HEAD + 1) * D_HEAD)
    W_Q, W_K, W_V = (w_attn[:, 768 * i:768 * (i + 1)][:, sl].numpy() for i in range(3))
    W_O = block.attn.c_proj.weight.detach()[sl, :].numpy()
    np.savez(DATA / 'weights.npz', W_Q=W_Q.astype(np.float16), W_K=W_K.astype(np.float16),
             W_V=W_V.astype(np.float16), W_O=W_O.astype(np.float16))
    meta = dict(model=MODEL, layer=LAYER, hook='blocks.6.hook_resid_post (TransformerLens name) == hidden_states[7] (transformers)',
                n_tokens=len(tokens), d_model=int(acts.shape[1]), dtype='float16',
                python=platform.python_version(), torch=torch.__version__, transformers=transformers.__version__,
                numpy=np.__version__, passage_chars=len(PASSAGE),
                fp16_max_abs_error=float(np.abs(hidden.numpy() - acts.astype(np.float32)).max()),
                head=dict(layer=HEAD_LAYER, head=HEAD, d_head=D_HEAD, shapes=dict(W_Q=list(W_Q.shape), W_K=list(W_K.shape), W_V=list(W_V.shape), W_O=list(W_O.shape))),
                first_token_norm=float(np.linalg.norm(hidden[0].numpy())), median_token_norm=float(np.median(np.linalg.norm(hidden.numpy(), axis=1))))
    (DATA / 'meta.json').write_text(json.dumps(meta, indent=2) + '\n')
    print(json.dumps(meta, indent=2))
    print('first tokens:', tokens[:12])


if __name__ == '__main__':
    main()
