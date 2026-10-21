window.NAV = [
  {
    "module": "Start here",
    "pages": [
      {
        "path": "index.html",
        "title": "Course home",
        "n": "",
        "kw": "overview prerequisites toolchain"
      }
    ]
  },
  {
    "module": "0 · The object of study",
    "pages": [
      {
        "path": "pages/00-orientation.html",
        "title": "The model is a function from token ids to logits",
        "n": "00",
        "kw": "logits residual stream shapes config overview"
      },
      {
        "path": "pages/01-tokenization.html",
        "title": "Tokenization: byte-pair encoding and the GPT-2 vocabulary",
        "n": "01",
        "kw": "tokenizer BPE merges vocabulary leading space token boundary"
      },
      {
        "path": "pages/02-embeddings-and-positions.html",
        "title": "Embeddings and positions: the first residual vector",
        "n": "02",
        "kw": "wte wpe embedding positional embedding hidden_states[0] context window"
      },
      {
        "path": "pages/03-the-residual-stream.html",
        "title": "The residual stream: a sum of writes",
        "n": "03",
        "kw": "residual stream additive writes resid_pre resid_post norms attribution"
      },
      {
        "path": "pages/04-layer-norm.html",
        "title": "Layer norm: what it does, where GPT-2 puts it, and folding it away",
        "n": "04",
        "kw": "layer norm pre-LN ln_1 ln_2 ln_f epsilon folding RMSNorm"
      }
    ]
  },
  {
    "module": "1 · Attention",
    "pages": [
      {
        "path": "pages/05-attention-one-head.html",
        "title": "Attention I: one head on three tokens",
        "n": "05",
        "kw": "attention query key value softmax causal mask scaled dot product pencil example"
      },
      {
        "path": "pages/06-attention-circuits.html",
        "title": "Attention II: heads as a QK circuit and an OV circuit",
        "n": "06",
        "kw": "multi-head attention QK circuit OV circuit low rank pattern c_attn c_proj head slicing"
      }
    ]
  },
  {
    "module": "2 · MLPs and the output",
    "pages": [
      {
        "path": "pages/07-the-mlp-block.html",
        "title": "The MLP block: two matrices, a GELU, and where a neuron lives",
        "n": "07",
        "kw": "MLP c_fc c_proj GELU gelu_new neuron hook_post d_mlp privileged basis"
      },
      {
        "path": "pages/08-gated-mlps.html",
        "title": "Gated MLPs: SwiGLU in Llama and Qwen3",
        "n": "08",
        "kw": "SwiGLU gated MLP GLU Swish SiLU gate_proj up_proj down_proj Llama Qwen3"
      },
      {
        "path": "pages/09-unembedding-and-logits.html",
        "title": "Unembedding and logits: from the stream to a distribution",
        "n": "09",
        "kw": "unembedding logits tied embeddings lm_head ln_f softmax logit lens direct logit attribution"
      }
    ]
  },
  {
    "module": "3 · The whole model",
    "pages": [
      {
        "path": "pages/10-forward-pass-from-raw-weights.html",
        "title": "The full forward pass from raw weights",
        "n": "10",
        "kw": "forward pass from scratch state_dict capstone match logits tolerance Conv1D"
      },
      {
        "path": "pages/11-shapes-and-parameter-counts.html",
        "title": "Shapes and parameter counts: deriving 124M from the config",
        "n": "11",
        "kw": "parameter count shapes state dict 124M 117M Conv1D tied lm_head"
      },
      {
        "path": "pages/12-generation-and-the-kv-cache.html",
        "title": "Generation and the KV cache",
        "n": "12",
        "kw": "generation sampling temperature greedy KV cache past_key_values"
      }
    ]
  },
  {
    "module": "4 · Tooling and variants",
    "pages": [
      {
        "path": "pages/13-naming-maps.html",
        "title": "Naming maps: the same activation in Hugging Face, TransformerLens 4, and nnsight",
        "n": "13",
        "kw": "TransformerLens TransformerBridge hook names run_with_cache nnsight trace hidden_states naming map"
      },
      {
        "path": "pages/14-architectural-variants.html",
        "title": "Architectural variants: GPT-2 versus Llama-style models",
        "n": "14",
        "kw": "Llama Qwen3 RMSNorm rotary RoPE SwiGLU grouped-query attention GQA QK-Norm variants"
      },
      {
        "path": "pages/15-readiness-review.html",
        "title": "Readiness review",
        "n": "15",
        "kw": "readiness review rubric checklist assessment"
      }
    ]
  },
  {
    "module": "Reference and practice",
    "pages": [
      {
        "path": "appendices/a-shapes-and-notation.html",
        "title": "Shapes and notation",
        "n": "A",
        "kw": "shapes notation tensor table d_model d_head d_mlp symbols"
      },
      {
        "path": "appendices/b-command-reference.html",
        "title": "Command reference",
        "n": "B",
        "kw": "commands anatomy.py reference tests"
      },
      {
        "path": "glossary.html",
        "title": "Glossary",
        "n": "",
        "kw": "definitions terms"
      },
      {
        "path": "bibliography.html",
        "title": "Annotated bibliography",
        "n": "",
        "kw": "sources provenance papers"
      }
    ]
  }
];
