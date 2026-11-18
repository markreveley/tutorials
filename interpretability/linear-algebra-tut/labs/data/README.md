# Real activation fixture: GPT-2 small, residual stream after block 6

These files are **real model activations**, not synthetic data. They were produced
once by `../make_data.py` on 2026-10-20 and committed so that the labs need only
numpy. Nothing in the course is simulated: every number printed by
`labs/linalg_lab.py` is computed from these files.

| File | Contents | Shape / size |
|---|---|---|
| `activations.npy` | float16 residual-stream vectors, one row per token | (302, 768), 464 KB |
| `tokens.json` | the 302 token strings, GPT-2 token ids, positions 0..301 | 5.7 KB |
| `labels.json` | four binary per-token labels computed from the token strings | 3.7 KB |
| `weights.npz` | float16 weights of one attention head: layer 7, head 0 | W_Q, W_K, W_V (768, 64); W_O (64, 768); 394 KB |
| `meta.json` | model name, layer, library versions, rounding error, norms | 0.7 KB |

## Origin and selection

- Model: `gpt2` (GPT-2 small, 124M parameters) loaded with `transformers`,
  weights from the Hugging Face hub, run on CPU with no sampling involved.
- Input: one original passage of 1,345 characters written for this course (the
  fictional record-keeping of a harbour town; see `PASSAGE` in `make_data.py`).
  It tokenises to 302 tokens with no beginning-of-sequence token prepended. It was
  written to contain many numbers and sentence boundaries so that simple labels
  exist for every token.
- Layer: `hidden_states[7]` from `output_hidden_states=True`, which is the residual
  stream **after** transformer block 6 (blocks are numbered 0..11). In
  TransformerLens naming this is `blocks.6.hook_resid_post`. The cross-check in
  `../../research/verify/fixture-crosscheck.txt` ran TransformerLens 4.2.0 on the
  same text with `prepend_bos=False` and found the two libraries agree to within
  0.19% of the largest activation.
- Storage: float16. The largest rounding error against the float32 forward pass is
  0.73 on an entry of magnitude about 2,900 (`meta.json`), that is a relative
  error of about 2.5e-4. Typical entries have magnitude 1 to 10 and are rounded to
  about three decimal places.
- Head weights: in the `transformers` GPT-2 implementation `c_attn.weight` has
  shape (768, 2304) holding `[Q | K | V]`, and head h uses columns `64h:64h+64` of
  each block; `c_proj.weight` is (768, 768) and head h's output rows are
  `64h:64h+64`. Biases and layer norm are omitted on purpose: the lessons use the
  matrices as linear maps, and the transformers course covers the rest.

## Labels

Each label is a list of 302 integers in `labels.json`, computed only from the
token strings (never from the activations):

- `is_digit` (45 ones): the token, stripped of a leading space, is all digits.
- `after_period` (23 ones): the previous token is `.`, `?` or `!` (position 0 is 0).
- `starts_with_space` (241 ones): the token string begins with a space.
- `capitalised` (29 ones): the first non-space character is upper case.

`reference.load_fixture()` adds `position` (0..301) as a fifth, continuous label.

## Two facts you will see immediately

1. **Position 0 is an outlier.** The first token's vector has norm 3,047 while the
   median token has norm 85. Most commands exclude it (`skip_first=True`) and say
   so. This is an observed property of this fixture, which the lessons treat as a
   lesson about norms and about PCA, not as a claim about why GPT-2 does it.
2. **A few coordinates are large at every token.** Coordinate 447 has mean 45.8
   and coordinate 138 varies with standard deviation 45; most coordinates have
   standard deviation around 1. Lesson 06 uses this to show that the neuron basis
   is one basis among many.

## Regenerating

`python labs/make_data.py` from the course directory, in an environment with
`torch`, `transformers` and `numpy` (the versions used are in `meta.json`). The
first run downloads GPT-2 (about 500 MB). The output is deterministic apart from
floating-point differences between machines, which float16 storage hides.
