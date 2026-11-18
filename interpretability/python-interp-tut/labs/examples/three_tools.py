"""Lesson 14: the same residual-stream activation in transformers, TransformerLens 4, and nnsight."""
import os
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error"); os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
import warnings
warnings.filterwarnings("ignore")
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

prompt = "The capital of France is"
LAYER = 5

# 1. transformers + a forward hook
tokenizer = AutoTokenizer.from_pretrained("gpt2")
hf = AutoModelForCausalLM.from_pretrained("gpt2").eval()
enc = tokenizer(prompt, return_tensors="pt")
got = {}
h = hf.transformer.h[LAYER].register_forward_hook(lambda m, a, o: got.__setitem__("hf", (o[0] if isinstance(o, tuple) else o).detach()))
with torch.no_grad():
    hf_logits = hf(**enc).logits
h.remove()
print("transformers hook  blocks[5] output:", tuple(got["hf"].shape))

# 2. TransformerLens 4: TransformerBridge, with and without compatibility mode
from transformer_lens.model_bridge import TransformerBridge
raw_bridge = TransformerBridge.boot_transformers("gpt2")
tl_logits_raw, raw_cache = raw_bridge.run_with_cache(prompt, prepend_bos=False)
print("TransformerLens      blocks.5.hook_resid_post:", tuple(raw_cache[f"blocks.{LAYER}.hook_resid_post"].shape), "| cache entries:", len(raw_cache))
print("  without compatibility mode, max |diff| vs transformers:", f"{(raw_cache[f'blocks.{LAYER}.hook_resid_post'] - got['hf']).abs().max().item():.1e}")
bridge = TransformerBridge.boot_transformers("gpt2")
bridge.enable_compatibility_mode()
tl_logits, cache = bridge.run_with_cache(prompt, prepend_bos=False)
resid = cache[f"blocks.{LAYER}.hook_resid_post"]
print("  with compatibility mode,    max |diff| vs transformers:", f"{(resid - got['hf']).abs().max().item():.2f}")
centered = got["hf"] - got["hf"].mean(-1, keepdim=True)
print("  ... but vs transformers centered over d_model:  ", f"{(resid - centered).abs().max().item():.1e}")
print("  logits argmax agrees:", tl_logits[0, -1].argmax().item() == hf_logits[0, -1].argmax().item(),
      "| logits equal:", torch.allclose(tl_logits, hf_logits, atol=1e-3), "(unembed is centered too)")
print("  prepend_bos default adds a token: shape with default is", tuple(bridge.run_with_cache(prompt)[1][f"blocks.{LAYER}.hook_resid_post"].shape))

# 3. nnsight
from nnsight import LanguageModel
nn_model = LanguageModel("gpt2", device_map="cpu", dispatch=True)
with nn_model.trace(prompt):
    nn_resid = nn_model.transformer.h[LAYER].output.save()
    nn_logits = nn_model.output.logits.save()
print("nnsight            transformer.h[5].output:", tuple(nn_resid.shape),
      "| max |diff| vs transformers:", f"{(nn_resid - got['hf']).abs().max().item():.1e}",
      "| logits equal:", torch.equal(nn_logits, hf_logits))
