"""Lesson 14: check the name map between TransformerLens 4 keys and nnsight module paths."""
import os
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error"); os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
import warnings
warnings.filterwarnings("ignore")
import torch
from nnsight import LanguageModel
from transformer_lens.model_bridge import TransformerBridge

prompt = "The capital of France is"
nn_model = LanguageModel("gpt2", device_map="cpu", dispatch=True)
with nn_model.trace(prompt):                      # access modules in forward order
    drop = nn_model.transformer.drop.output.save()
    attn = nn_model.transformer.h[5].attn.output.save()
    mid = nn_model.transformer.h[5].ln_2.input.save()
    mlp = nn_model.transformer.h[5].mlp.output.save()
    ln_f = nn_model.transformer.ln_f.output.save()
print("nnsight attn.output is a", type(attn).__name__, "of", [type(x).__name__ for x in attn], "; [0] has shape", tuple(attn[0].shape))

bridge = TransformerBridge.boot_transformers("gpt2")     # raw weights: no compatibility mode
_, cache = bridge.run_with_cache(prompt, prepend_bos=False)
pairs = [("transformer.drop.output", drop, "blocks.0.hook_resid_pre"),
         ("transformer.h[5].attn.output[0]", attn[0], "blocks.5.hook_attn_out"),
         ("transformer.h[5].ln_2.input", mid, "blocks.5.hook_resid_mid"),
         ("transformer.h[5].mlp.output", mlp, "blocks.5.hook_mlp_out"),
         ("transformer.ln_f.output", ln_f, "ln_final.hook_normalized")]
for nn_name, value, tl_key in pairs:
    diff = (value - cache[tl_key]).abs().max().item()
    print(f"{nn_name:34s} vs {tl_key:28s} shape {tuple(value.shape)}  max |diff| {diff:.1e}")
print("blocks.5.attn.hook_pattern shape:", tuple(cache["blocks.5.attn.hook_pattern"].shape), "(batch, heads, query, key)")
