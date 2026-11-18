"""Hook labs: capture GPT-2 small's residual stream with forward hooks.

Implement the two stubs so that labs/test_hooks.py passes. The tests need
torch and transformers and the cached `gpt2` weights; they skip with a message
otherwise. Run from the course directory:

    HF_HUB_OFFLINE=1 python3 -m unittest discover -s labs -p 'test_hooks.py' -v

`load_gpt2` is provided: it is the same loader the lessons use.
"""
import os

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

D_MODEL = 768
N_LAYERS = 12


def load_gpt2():
    """Return (tokenizer, model) for GPT-2 small in eval mode on the CPU."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained("gpt2", dtype=torch.float32)
    model.eval()
    return tokenizer, model


def cache_residual_stream(model, input_ids, attention_mask=None):
    """Run one forward pass and return the residual stream after every layer.

    Return a dict with 13 entries in this order: "embed" (the output of
    model.transformer.drop, the token plus position embeddings) and
    "block.0" ... "block.11" (the output of each GPT2Block, that is the
    residual stream after that block). Every value is a detached float32
    tensor of shape (batch, seq, 768) and is NOT the same object the model
    computed (clone it). Register forward hooks, run the model under
    torch.no_grad(), and remove every hook you added before returning, even
    if the forward pass raises. Do not call the model with
    output_hidden_states=True: the point is to do it with hooks.
    """
    raise NotImplementedError("Implement cache_residual_stream with register_forward_hook")


def assert_cache_shapes(cache, batch, seq):
    """Raise AssertionError with a readable message unless the cache is right.

    Required: exactly the 13 keys above in order; every value has shape
    (batch, seq, 768), dtype float32, no NaN or inf, and requires_grad False.
    Return the cache unchanged so the call can be chained.
    """
    raise NotImplementedError("Implement assert_cache_shapes; every shape is a test")
