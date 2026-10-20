# Lab assessments

Three labs ship as stubs with published tests. This file describes the held-out
variant families a tutor should draw from once the published tests pass. The
variants themselves are not published, following `dag-tests/CONTRACT.md`.

Run the published tests from the course directory:

```sh
python -m unittest discover -s labs -p 'test_*.py' -v
```

`LAB_IMPL=reference` points the same tests at the author's solutions under
`labs/reference/`, for checking the tests; learners should not need it.

## Lab 1: `tokens.py` (lesson 01)

Published: `pair_counts`, `merge_pair`, `train_bpe`, `bpe_encode` on the five-word
corpus; `pieces` and `token_span` on the running prompt.

Held-out families:
- A different toy corpus with a tie in the first merge, testing the stated tie-break.
- A corpus where a merge creates a new pair that becomes the next best merge, testing
  that counts are recomputed after each merge rather than once.
- `bpe_encode` on a word containing a symbol absent from the corpus.
- `token_span` on a prompt where the target word is split into several tokens, where
  the span ends mid-token, and where the span starts at position 0.
- A prompt with a doubled space (`"  two spaces"`), asking for the token count and
  which token is the lone space.

## Lab 2: `attention.py` (lessons 05–06)

Published: softmax stability, causal mask, the three-token pencil case, agreement with
`scaled_dot_product_attention`, head split/merge, circuit shapes and rank.

Held-out families:
- A four-token pencil case with d_head = 16 (scale 1/4) and non-unit value vectors,
  computed by the tutor from e; the learner must produce both pattern and output.
- A query/key pair designed so that the unscaled scores saturate the softmax but the
  scaled ones do not, testing that the scale is applied before the softmax.
- Batched inputs with a head axis of size 1 and of size 12, checking broadcasting.
- `qk_circuit` and `ov_circuit` fed real GPT-2 weights for a named head, with the
  learner asked to verify rank 64 and to reproduce one pattern entry from the circuit.
- A non-causal case with an explicit key-padding mask (requires extending the signature).

## Lab 3: `gpt2_from_scratch.py` (lessons 04, 07, 10)

Published: layer norm and gelu_new pencil cases, component shapes, logits and every
cache key against transformers on the running prompt, agreement with TransformerLens
(no_processing) and nnsight at blocks 0, 5, 11.

Held-out families:
- A prompt of a different length (12–40 tokens) chosen by the tutor, same tolerances.
- Batch of two prompts of equal length; the cache must carry the batch axis.
- A perturbed-weights test: the tutor zeroes one head's `W_O` rows in both the
  learner's params and the Hugging Face model and checks that both change identically
  (tests that the head slicing is right).
- A "find the bug" variant: the tutor supplies an implementation with one of the
  lesson-10 table's mistakes and the learner must name it from the cache diff alone.
- A modified-architecture variant: implement RMSNorm in place of layer norm on the
  same weights (ignoring the bias) and report the logit change; or drop the position
  embedding and report which layers' patterns change most.
- Re-derive `resid_post.11` from Hugging Face outputs alone (hidden_states plus
  sub-module hooks) and match it to the learner's cache.

## Grading notes

A learner is ready when the published tests pass on first run after implementation,
one variant from each family passes without hints, and the learner can explain any
residual difference above 1e-4 as accumulation order or name the bug. Argmax
agreement alone is not sufficient (lesson 10).
