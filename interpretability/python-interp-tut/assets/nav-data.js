window.NAV = [
  {
    "module": "Start here",
    "pages": [
      {
        "path": "index.html",
        "title": "Course home",
        "n": "",
        "kw": "overview prerequisites setup"
      }
    ]
  },
  {
    "module": "0 · Orientation and setup",
    "pages": [
      {
        "path": "pages/00-orientation.html",
        "title": "What this course makes you able to do",
        "n": "00",
        "kw": "overview goals shapes readiness"
      },
      {
        "path": "pages/01-lab-setup.html",
        "title": "Lab setup: a CPU-only toolchain you can trust",
        "n": "01",
        "kw": "install virtualenv pip torch cpu colab cache offline"
      }
    ]
  },
  {
    "module": "1 · Python for someone coming from Elixir and Rust",
    "pages": [
      {
        "path": "pages/02-names-and-objects.html",
        "title": "Names bind to objects; mutation is visible through every name",
        "n": "02",
        "kw": "identity aliasing mutation copy deepcopy is equals default argument"
      },
      {
        "path": "pages/03-records-and-errors.html",
        "title": "Dicts, lists, JSON and JSONL, and exceptions as the error channel",
        "n": "03",
        "kw": "dict list json jsonl exceptions try except raise ValueError FileNotFoundError"
      },
      {
        "path": "pages/04-spec-first-testing.html",
        "title": "Spec-first testing with unittest: the three eval-pipeline labs",
        "n": "04",
        "kw": "unittest discover assertRaises subTest score_ticket load_cases summarize_run spec"
      },
      {
        "path": "pages/05-functions-generators-dataclasses.html",
        "title": "Functions, generators, dataclasses, and type hints as documentation",
        "n": "05",
        "kw": "functions kwargs closures generators yield dataclass frozen type hints context manager"
      }
    ]
  },
  {
    "module": "2 · Arrays and tensors",
    "pages": [
      {
        "path": "pages/06-arrays-and-shapes.html",
        "title": "NumPy arrays: shape, dtype, indexing, slicing, views",
        "n": "06",
        "kw": "numpy ndarray shape dtype index slice view copy ellipsis None axis"
      },
      {
        "path": "pages/07-broadcasting.html",
        "title": "Broadcasting rules, with a shape-prediction drill",
        "n": "07",
        "kw": "broadcast rule keepdims None axis ValueError shape prediction drill"
      },
      {
        "path": "pages/08-reductions-and-einsum.html",
        "title": "Reductions, axes, and einsum read aloud",
        "n": "08",
        "kw": "sum mean axis argmax norm einsum subscripts contraction attention"
      },
      {
        "path": "pages/09-torch-tensors.html",
        "title": "torch tensors: dtype, device, views versus copies, in-place ops, no_grad",
        "n": "09",
        "kw": "tensor dtype device view reshape contiguous in-place no_grad detach numpy item"
      },
      {
        "path": "pages/10-autograd.html",
        "title": "Autograd: what a gradient is operationally, backward(), and a tiny fit",
        "n": "10",
        "kw": "gradient backward requires_grad leaf grad accumulate optimizer finite difference attribution"
      }
    ]
  },
  {
    "module": "3 · Models as objects",
    "pages": [
      {
        "path": "pages/11-modules-and-state.html",
        "title": "nn.Module, parameters, state_dict, and reading a module tree",
        "n": "11",
        "kw": "nn.Module parameters state_dict named_parameters module tree GPT2 config eval"
      },
      {
        "path": "pages/12-gpt2-forward.html",
        "title": "Loading GPT-2 small: tokenizer, input ids, logits, next token, hidden states",
        "n": "12",
        "kw": "tokenizer input_ids logits softmax topk hidden_states output_hidden_states pad attention_mask"
      },
      {
        "path": "pages/13-forward-hooks.html",
        "title": "Forward hooks: registering, capturing, and caching activations with shapes asserted",
        "n": "13",
        "kw": "register_forward_hook handle remove closure detach clone cache torch.save finally"
      },
      {
        "path": "pages/14-three-toolkits.html",
        "title": "The same activation in transformers, TransformerLens 4, and nnsight",
        "n": "14",
        "kw": "TransformerLens TransformerBridge boot_transformers compatibility mode run_with_cache nnsight trace save prepend_bos"
      },
      {
        "path": "pages/15-reproducibility-and-artifacts.html",
        "title": "Reproducibility and artifacts: seeds, safetensors, a run manifest, memory and batching on CPU",
        "n": "15",
        "kw": "seed manual_seed determinism safetensors save_file manifest sha256 memory batching padding float16"
      }
    ]
  },
  {
    "module": "4 · Readiness",
    "pages": [
      {
        "path": "pages/16-readiness-review.html",
        "title": "Readiness review: cache the residual stream and prove it",
        "n": "16",
        "kw": "readiness rubric cache residual stream manifest safetensors tests green"
      }
    ]
  },
  {
    "module": "Reference and practice",
    "pages": [
      {
        "path": "appendices/a-shapes.html",
        "title": "Shape reference",
        "n": "A",
        "kw": "shape cheat sheet broadcasting einsum GPT-2 dimensions axis"
      },
      {
        "path": "appendices/b-commands.html",
        "title": "Command and lab reference",
        "n": "B",
        "kw": "commands scripts tests labs unittest verify"
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
        "kw": "sources provenance attribution"
      }
    ]
  }
];
