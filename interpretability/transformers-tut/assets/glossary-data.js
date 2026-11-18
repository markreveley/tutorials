window.GLOSSARY = {
  "token": {
    "name": "Token",
    "short": "The unit the model reads: an integer id standing for a string piece chosen by the tokenizer.",
    "def": "The unit the model reads: an integer id standing for a string piece chosen by the tokenizer. GPT-2 has 50,257 of them."
  },
  "tokenizer": {
    "name": "Tokenizer",
    "short": "The fixed procedure that turns text into token ids and back.",
    "def": "The fixed procedure that turns text into token ids and back. It is not part of the neural network and is not learned with it."
  },
  "byte-pair-encoding": {
    "name": "Byte-pair encoding",
    "short": "A tokenizer-building procedure that repeatedly merges the most frequent adjacent pair of symbols in a corpus; the merge list is then applied in order to new text..",
    "def": "A tokenizer-building procedure that repeatedly merges the most frequent adjacent pair of symbols in a corpus; the merge list is then applied in order to new text."
  },
  "vocabulary": {
    "name": "Vocabulary",
    "short": "The set of all token strings, indexed by id.",
    "def": "The set of all token strings, indexed by id. Its size is the last dimension of the logits."
  },
  "token-boundary": {
    "name": "Token boundary",
    "short": "The place where one token ends and the next begins.",
    "def": "The place where one token ends and the next begins. A claim about \"the word cat\" is really a claim about whichever tokens cover it."
  },
  "embedding": {
    "name": "Embedding",
    "short": "The lookup that maps a token id to a d_model-dimensional vector: row id of the matrix wte..",
    "def": "The lookup that maps a token id to a d_model-dimensional vector: row id of the matrix wte."
  },
  "positional-embedding": {
    "name": "Positional embedding",
    "short": "A learned vector added to each position's token embedding so the model can tell positions apart.",
    "def": "A learned vector added to each position's token embedding so the model can tell positions apart. GPT-2 learns one per position (wpe); Llama-style models use rotations instead."
  },
  "residual-stream": {
    "name": "Residual stream",
    "short": "The running (seq, d_model) vector per token that every block reads from and adds to.",
    "def": "The running (seq, d_model) vector per token that every block reads from and adds to. The final stream is the embedding plus every attention and MLP output."
  },
  "d-model": {
    "name": "d_model",
    "short": "The width of the residual stream, 768 in GPT-2 small.",
    "def": "The width of the residual stream, 768 in GPT-2 small. Also called hidden size or n_embd."
  },
  "block": {
    "name": "Block",
    "short": "One attention layer followed by one MLP layer, each wrapped in a layer norm and a residual addition.",
    "def": "One attention layer followed by one MLP layer, each wrapped in a layer norm and a residual addition. GPT-2 small has 12."
  },
  "layer-norm": {
    "name": "Layer norm",
    "short": "Normalise a vector to mean 0 and variance 1 across d_model, then scale by a learned weight and shift by a learned bias..",
    "def": "Normalise a vector to mean 0 and variance 1 across d_model, then scale by a learned weight and shift by a learned bias."
  },
  "rmsnorm": {
    "name": "RMSNorm",
    "short": "Layer norm without the mean subtraction and without the bias: divide by the root mean square, then scale..",
    "def": "Layer norm without the mean subtraction and without the bias: divide by the root mean square, then scale."
  },
  "pre-ln": {
    "name": "Pre-LN",
    "short": "Placing the layer norm on the input of each sub-block, before attention and before the MLP, so the residual stream itself is never normalised until ln_f..",
    "def": "Placing the layer norm on the input of each sub-block, before attention and before the MLP, so the residual stream itself is never normalised until ln_f."
  },
  "ln-folding": {
    "name": "Layer-norm folding",
    "short": "Multiplying the layer norm's weight and bias into the next linear layer so the normalisation step has no learned parameters.",
    "def": "Multiplying the layer norm's weight and bias into the next linear layer so the normalisation step has no learned parameters. The function is unchanged."
  },
  "attention-head": {
    "name": "Attention head",
    "short": "One unit of attention: its own query, key, value, and output maps of width d_head.",
    "def": "One unit of attention: its own query, key, value, and output maps of width d_head. GPT-2 small has 12 per layer."
  },
  "query": {
    "name": "Query",
    "short": "The vector a position uses to ask what to attend to; q = x W_Q..",
    "def": "The vector a position uses to ask what to attend to; q = x W_Q."
  },
  "key": {
    "name": "Key",
    "short": "The vector a position offers to be matched against queries; k = x W_K..",
    "def": "The vector a position offers to be matched against queries; k = x W_K."
  },
  "value": {
    "name": "Value",
    "short": "The vector a position contributes when attended to; v = x W_V..",
    "def": "The vector a position contributes when attended to; v = x W_V."
  },
  "attention-score": {
    "name": "Attention score",
    "short": "The scaled dot product q·k / sqrt(d_head) before the softmax..",
    "def": "The scaled dot product q·k / sqrt(d_head) before the softmax."
  },
  "attention-pattern": {
    "name": "Attention pattern",
    "short": "The (query position, key position) matrix of softmax weights; each row sums to 1.",
    "def": "The (query position, key position) matrix of softmax weights; each row sums to 1. It says where a head reads, not what it does with what it reads."
  },
  "causal-mask": {
    "name": "Causal mask",
    "short": "Setting scores for key positions after the query position to minus infinity, so a token cannot attend to the future..",
    "def": "Setting scores for key positions after the query position to minus infinity, so a token cannot attend to the future."
  },
  "softmax": {
    "name": "Softmax",
    "short": "Exponentiate every entry and divide by their sum, giving positive weights that add to 1.",
    "def": "Exponentiate every entry and divide by their sum, giving positive weights that add to 1. Invariant to adding a constant to all entries."
  },
  "d-head": {
    "name": "d_head",
    "short": "The width of one head's query, key, and value vectors: d_model / n_head = 64 in GPT-2 small..",
    "def": "The width of one head's query, key, and value vectors: d_model / n_head = 64 in GPT-2 small."
  },
  "multi-head-attention": {
    "name": "Multi-head attention",
    "short": "Several heads run in parallel on the same input; their outputs are summed (equivalently, concatenated and multiplied by one output matrix)..",
    "def": "Several heads run in parallel on the same input; their outputs are summed (equivalently, concatenated and multiplied by one output matrix)."
  },
  "qk-circuit": {
    "name": "QK circuit",
    "short": "The matrix W_Q W_K^T (d_model by d_model, rank at most d_head) that scores a query residual against a key residual.",
    "def": "The matrix W_Q W_K^T (d_model by d_model, rank at most d_head) that scores a query residual against a key residual. It determines the attention pattern."
  },
  "ov-circuit": {
    "name": "OV circuit",
    "short": "The matrix W_V W_O (d_model by d_model, rank at most d_head) that maps an attended residual vector to what the head writes.",
    "def": "The matrix W_V W_O (d_model by d_model, rank at most d_head) that maps an attended residual vector to what the head writes. It determines what attention moves."
  },
  "mlp": {
    "name": "MLP",
    "short": "The block's position-wise two-layer network: up-project to d_mlp, apply a nonlinearity, down-project to d_model..",
    "def": "The block's position-wise two-layer network: up-project to d_mlp, apply a nonlinearity, down-project to d_model."
  },
  "d-mlp": {
    "name": "d_mlp",
    "short": "The hidden width of the MLP, 3072 = 4 × d_model in GPT-2 small.",
    "def": "The hidden width of the MLP, 3072 = 4 × d_model in GPT-2 small. Hugging Face calls it n_inner or intermediate_size."
  },
  "neuron": {
    "name": "Neuron",
    "short": "One hidden unit of an MLP: a column of the up-projection (its input direction), a scalar activation, and a row of the down-projection (its output direction)..",
    "def": "One hidden unit of an MLP: a column of the up-projection (its input direction), a scalar activation, and a row of the down-projection (its output direction)."
  },
  "gelu": {
    "name": "GELU",
    "short": "The activation x·Φ(x), with Φ the standard normal CDF.",
    "def": "The activation x·Φ(x), with Φ the standard normal CDF. GPT-2 uses the tanh approximation called gelu_new."
  },
  "swiglu": {
    "name": "SwiGLU",
    "short": "A gated MLP: (Swish(xW) ⊙ xV) W_2, with three matrices instead of two.",
    "def": "A gated MLP: (Swish(xW) ⊙ xV) W_2, with three matrices instead of two. Used by Llama and Qwen3."
  },
  "gating": {
    "name": "Gating",
    "short": "Multiplying one branch of a computation elementwise by another, so one branch decides how much of the other passes..",
    "def": "Multiplying one branch of a computation elementwise by another, so one branch decides how much of the other passes."
  },
  "unembedding": {
    "name": "Unembedding",
    "short": "The final linear map from the residual stream to one logit per vocabulary entry.",
    "def": "The final linear map from the residual stream to one logit per vocabulary entry. In GPT-2 it is the transpose of the embedding matrix."
  },
  "tied-embeddings": {
    "name": "Tied embeddings",
    "short": "Using the same matrix for embedding and unembedding.",
    "def": "Using the same matrix for embedding and unembedding. GPT-2's lm_head.weight is literally transformer.wte.weight."
  },
  "logits": {
    "name": "Logits",
    "short": "The unnormalised scores over the vocabulary at each position, shape (batch, seq, d_vocab).",
    "def": "The unnormalised scores over the vocabulary at each position, shape (batch, seq, d_vocab). Softmax turns a row into next-token probabilities."
  },
  "logit-lens": {
    "name": "Logit lens",
    "short": "Applying ln_f and the unembedding to the residual stream after an earlier block, to see what the model would predict if it stopped there..",
    "def": "Applying ln_f and the unembedding to the residual stream after an earlier block, to see what the model would predict if it stopped there."
  },
  "temperature": {
    "name": "Temperature",
    "short": "A divisor applied to logits before sampling.",
    "def": "A divisor applied to logits before sampling. Below 1 sharpens the distribution; above 1 flattens it; greedy decoding is the limit of 0."
  },
  "kv-cache": {
    "name": "KV cache",
    "short": "The keys and values of every earlier position, stored so generating the next token recomputes only the new position..",
    "def": "The keys and values of every earlier position, stored so generating the next token recomputes only the new position."
  },
  "forward-pass": {
    "name": "Forward pass",
    "short": "Running the model once from token ids to logits with no gradient computation..",
    "def": "Running the model once from token ids to logits with no gradient computation."
  },
  "state-dict": {
    "name": "State dict",
    "short": "PyTorch's mapping from parameter names to tensors; the raw weights the capstone loads..",
    "def": "PyTorch's mapping from parameter names to tensors; the raw weights the capstone loads."
  },
  "hook": {
    "name": "Hook",
    "short": "A function attached to a point in the forward pass that sees (and may replace) the activation there..",
    "def": "A function attached to a point in the forward pass that sees (and may replace) the activation there."
  },
  "activation-cache": {
    "name": "Activation cache",
    "short": "A dictionary of named activations captured during one forward pass; TransformerLens's run_with_cache returns one..",
    "def": "A dictionary of named activations captured during one forward pass; TransformerLens's run_with_cache returns one."
  },
  "hidden-states": {
    "name": "hidden_states",
    "short": "Hugging Face's tuple of residual-stream snapshots: entry 0 after embedding, entry i after block i−1, and the last entry after the final layer norm..",
    "def": "Hugging Face's tuple of residual-stream snapshots: entry 0 after embedding, entry i after block i−1, and the last entry after the final layer norm."
  },
  "rotary-embedding": {
    "name": "Rotary embedding",
    "short": "RoPE: rotating pairs of query and key dimensions by an angle proportional to position, so dot products depend on relative position.",
    "def": "RoPE: rotating pairs of query and key dimensions by an angle proportional to position, so dot products depend on relative position. No position vector is added to the stream."
  },
  "grouped-query-attention": {
    "name": "Grouped-query attention",
    "short": "Several query heads share one key/value head, shrinking the KV cache.",
    "def": "Several query heads share one key/value head, shrinking the KV cache. Qwen3-0.6B has 16 query heads and 8 key/value heads."
  },
  "privileged-basis": {
    "name": "Privileged basis",
    "short": "A coordinate system that the computation singles out.",
    "def": "A coordinate system that the computation singles out. The residual stream has none (any rotation works if all weights rotate too); MLP neurons do, because the nonlinearity acts per coordinate."
  },
  "virtual-weights": {
    "name": "Virtual weights",
    "short": "The product of one layer's output weights with a later layer's input weights: the effective linear map between them through the residual stream..",
    "def": "The product of one layer's output weights with a later layer's input weights: the effective linear map between them through the residual stream."
  },
  "context-window": {
    "name": "Context window",
    "short": "The maximum sequence length the model was built for: 1024 positions in GPT-2, fixed by the size of wpe..",
    "def": "The maximum sequence length the model was built for: 1024 positions in GPT-2, fixed by the size of wpe."
  },
  "end-of-text": {
    "name": "End-of-text token",
    "short": "GPT-2's token 50256, <|endoftext|>.",
    "def": "GPT-2's token 50256, <|endoftext|>. TransformerLens prepends it as a beginning-of-sequence token by default; Hugging Face and nnsight do not."
  },
  "sequence-position": {
    "name": "Sequence position",
    "short": "The index of a token within the input, the middle axis of a (batch, seq, d_model) tensor..",
    "def": "The index of a token within the input, the middle axis of a (batch, seq, d_model) tensor."
  },
  "parameter-count": {
    "name": "Parameter count",
    "short": "The number of learned scalars; 124,439,808 for GPT-2 small, derived from the config in lesson 11..",
    "def": "The number of learned scalars; 124,439,808 for GPT-2 small, derived from the config in lesson 11."
  }
};
