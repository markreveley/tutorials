# Source checking and provenance

Checked on 2026-10-20. `sources.json` records each URL and the claim scope verified.
This is not a claim that every statement in each source was validated. Where a PDF
was fetched, its text was extracted with `pdftotext` and the quoted passages located
by search; where a page was fetched as HTML, the relevant passages were read directly.
Facts about the installed GPT-2 checkpoint were verified by running commands against
it; those commands and their output are in `verify/lab-transcript.txt`.

## Papers and reports

- Vaswani et al. 2017, arXiv:1706.03762 (PDF). Verified: eq. 1 Attention(Q,K,V) =
  softmax(QKᵀ/√d_k)V; the sentence on large dot products pushing softmax into small-
  gradient regions motivating 1/√d_k; MultiHead = Concat(head_1..head_h)W^O with
  head_i = Attention(QW_i^Q, KW_i^K, VW_i^V); h = 8, d_k = d_v = d_model/h = 64;
  FFN(x) = max(0, xW_1 + b_1)W_2 + b_2 with d_model 512 and d_ff 2048; masking by
  setting illegal connections to −∞; sharing the embedding matrix with the pre-softmax
  linear transformation (§3.4).
- Radford et al. 2019, GPT-2 paper (PDF from cdn.openai.com). Verified in §2.3: layer
  normalization moved to the input of each sub-block with an additional layer norm
  after the final self-attention block; residual-layer weights scaled by 1/√N at
  initialization; vocabulary expanded to 50,257; context size 1024; batch size 512.
  Table 2: 117M / 12 layers / d_model 768; 345M / 24 / 1024; 762M / 36 / 1280;
  1542M / 48 / 1600. The course reports the installed checkpoint's 124,439,808 and
  notes the discrepancy with 117M without asserting a cause.
- openai/gpt-2 model_card.md (GitHub). Verified: sizes described as 124M, 355M, 774M,
  1.5B; trained on WebText. The card does not describe architecture.
- Elhage et al. 2021, A Mathematical Framework for Transformer Circuits (HTML, fetched
  and text-extracted locally because the page is 770k characters including inline
  images). Verified passages: layers read and write subspaces of the residual stream;
  "the residual stream doesn't have a privileged basis"; virtual weights as the product
  of one layer's output weights with a later layer's input weights; QK circuit computes
  the attention pattern and OV circuit computes how each token affects the output if
  attended to, as the low-rank matrices W_Q^T W_K and W_O W_V (their column-vector
  convention; the course uses row vectors and says so); h(x)_i = W_O Σ_j A_ij v_j;
  section "Attention Heads are Independent and Additive".
- Shazeer 2020, arXiv:2002.05202 (PDF). Verified eqs. 3–6: Swish_β(x) = xσ(βx);
  SwiGLU(x,W,V,b,c,β) = Swish_β(xW+b) ⊗ (xV+c); FFN_SwiGLU(x,W,V,W_2) =
  (Swish_1(xW) ⊗ xV)W_2 without biases; three weight matrices with d_ff reduced by
  2/3 to hold parameters constant; GEGLU and SwiGLU gave the best perplexities in §3.2.
  No table values are reproduced in the course.
- Touvron et al. 2023, LLaMA, arXiv:2302.13971 (PDF). Verified §2.2: pre-normalization
  of each sub-layer input with RMSNorm; SwiGLU with dimension 2/3·4d; rotary embeddings
  at each layer replacing absolute positional embeddings. Table 2: 6.7B (4096, 32
  heads, 32 layers), 13.0B (5120, 40, 40), 32.5B (6656, 52, 60), 65.2B (8192, 64, 80).
- Yang et al. 2025, Qwen3 Technical Report, arXiv:2505.09388 (HTML). Verified §2: dense
  models use GQA, SwiGLU, RoPE, RMSNorm with pre-normalization; QKV bias removed;
  QK-Norm introduced. Table 1: Qwen3-0.6B 28 layers, 16/8 heads, tie embedding yes,
  32K context; 1.7B 28, 16/8, yes; 4B 36, 32/8, yes, 128K; 8B 36, 32/8, no; 14B 40,
  40/8, no; 32B 64, 64/8, no. Sizes 0.6B to 235B, dense and MoE.
- Su et al. 2021, RoFormer, arXiv:2104.09864 (abstract). Verified: rotation-matrix
  encoding of absolute position giving relative-position dependence in attention.
- Zhang & Sennrich 2019, RMSNorm, arXiv:1910.07467 (abstract). Verified: drops
  re-centering, normalizes by root mean square.
- Ainslie et al. 2023, GQA, arXiv:2305.13245 (abstract). Verified: intermediate number
  of key/value heads between MQA and MHA.
- Sennrich, Haddow & Birch 2015, arXiv:1508.07909 (abstract). Verified: subword units
  for rare words, BPE among the segmentation methods.
- Hendrycks & Gimpel 2016, GELU, arXiv:1606.08415 (PDF). Verified: GELU(x) = xΦ(x) =
  x·½[1 + erf(x/√2)]; approximations 0.5x(1 + tanh[√(2/π)(x + 0.044715x³)]) and
  xσ(1.702x).
- nostalgebraist 2020, "interpreting GPT: the logit lens" (LessWrong). Verified: applying
  the final projection to intermediate layers gives distributions that converge toward
  the final output, often well before the last layer.

## Library documentation

- TransformerLens, "Migrating to TransformerLens 4.0": 4.0 removes the legacy Hooked*
  stack; HookedTransformer → TransformerBridge.boot_transformers(name) +
  enable_compatibility_mode(); compatibility mode reproduces LayerNorm folding,
  center_writing_weights, center_unembed; omit it for raw HF weights.
- TransformerLens, "TransformerBridge Compatibility Mode": the signature with
  fold_ln, center_writing_weights, center_unembed, fold_value_biases defaulting to
  True; no_processing=True; folding means logits will not match HF; center_unembed
  makes logits mean-zero without affecting argmax; legacy hook names resolve on every
  bridge; the call mutates weights in place and must not be repeated.
- TransformerLens, "The Hook System": run_with_cache returns (logits, cache); example
  keys blocks.0.attn.hook_q, blocks.5.hook_resid_post, blocks.5.attn.hook_z,
  ln_final.hook_normalized. The full list of 40 block hooks in lesson 13 came from
  running the installed package, not from this page.
- nnsight, Quickstart: TransformersModel('openai-community/gpt2', task=
  'text-generation', device_map=..., dispatch=True); pass task explicitly offline;
  model.trace; values must be .save()d.
- nnsight, Getting Activations: .output and .input; modules must be requested in the
  order they run or OutOfOrderError is raised.
- The TransformerLens index page and the nnsight API index were also fetched to find
  the pages above; neither contained the claims themselves.

## Installed code read (transformers 5.20.2, verified copies in the virtualenv)

- `models/gpt2/modeling_gpt2.py`: GPT2Block applies ln_1 then attention then residual
  add, ln_2 then MLP then residual add; scaling head_dim ** −0.5; `pytorch_utils.Conv1D`
  computes addmm(bias, x, weight) with weight (nx, nf) = (in, out);
  `activations.NewGELUActivation` is the tanh formula; GPT2Config: activation_function
  gelu_new, layer_norm_epsilon 1e-05, n_embd 768, n_head 12, n_layer 12, n_positions
  1024, vocab_size 50257, tie_word_embeddings true.
- `models/llama/modeling_llama.py`: LlamaRMSNorm (float32, rsqrt(mean(x²)+eps), weight,
  no bias); LlamaMLP down_proj(act_fn(gate_proj(x)) * up_proj(x)), hidden_act silu;
  rotate_half and apply_rotary_pos_emb (q*cos + rotate_half(q)*sin); repeat_kv;
  input_layernorm and post_attention_layernorm placement.
- `models/qwen3/modeling_qwen3.py`: Qwen3MLP identical in form, no biases; q_norm and
  k_norm of size head_dim applied before rotation.

## Verified by running (see verify/lab-transcript.txt)

- GPT-2 state dict: 149 entries, 148 distinct parameter tensors, 124,439,808 parameters;
  lm_head.weight shares storage with transformer.wte.weight.
- Tokenizer: 50,257 entries; merges.txt has 50,000 merge lines; ids for the running
  prompt and for the space/no-space pairs.
- TransformerLens 4.2.0: 493 cache entries for a 6-token input; the 40 block-5 hook
  names; `ln_final.hook_normalized` is pre-affine and `ln_final.hook_out` matches
  HF hidden_states[12]; no_processing matches HF to ~1e-5; default processing
  differs by a per-position logit constant and a per-vector mean; `to_tokens`
  prepends 50256.
- nnsight 0.8.1: LanguageModel is deprecated in favour of TransformersModel;
  h[i].output is a tensor, h[i].attn.output is (tensor, None); out-of-order access
  raises OutOfOrderError; a trace from stdin fails, so all runs are from files.
- transformers 5.20.2: output_attentions requires attn_implementation='eager'.

## Original material

All pencil examples (the 3-token attention head, [1,3,5,7], the SwiGLU two-vector,
the five-word BPE corpus, [2,1,0]) and all prose explanations are original. The
running prompt "The cat sat on the mat" was chosen for length; no claim is made about
its generality.
