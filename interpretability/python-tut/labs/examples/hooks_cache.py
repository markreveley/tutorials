"""Lesson 13: forward hooks: register, capture, assert shapes, save to disk."""
import os
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error"); os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
from pathlib import Path
import tempfile
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2").eval()
enc = tokenizer("The capital of France is", return_tensors="pt")

captured = {}
def make_hook(name):
    def hook(module, args, output):
        out = output[0] if isinstance(output, tuple) else output
        captured[name] = out.detach().clone()
    return hook

handles = [model.transformer.h[i].register_forward_hook(make_hook(f"block.{i}")) for i in range(12)]
print("hooks registered:", len(handles), "| handle type:", type(handles[0]).__name__)
try:
    with torch.no_grad():
        out = model(**enc, output_hidden_states=True)
finally:
    for h in handles:
        h.remove()
print("captured:", list(captured)[:3], "...", list(captured)[-1])
batch, seq = enc["input_ids"].shape
for name, act in captured.items():
    assert act.shape == (batch, seq, 768), f"{name}: {tuple(act.shape)}"
    assert act.dtype == torch.float32 and not act.requires_grad and torch.isfinite(act).all(), name
print("every block output has shape", (batch, seq, 768))
print("block.5 equals hidden_states[6]:", torch.equal(captured["block.5"], out.hidden_states[6]))
print("block.11 equals hidden_states[12]:", torch.equal(captured["block.11"], out.hidden_states[12]), "(ln_f applied to [12])")

with tempfile.TemporaryDirectory() as d:
    path = Path(d) / "resid.pt"
    torch.save(captured, path)
    loaded = torch.load(path)
    print("saved and reloaded:", len(loaded), "tensors,", f"{path.stat().st_size / 1e3:.0f} kB,", "block.5 identical:", torch.equal(loaded["block.5"], captured["block.5"]))

alive = {}
h = model.transformer.h[0].register_forward_hook(lambda m, a, o: alive.__setitem__("block.0", o[0] if isinstance(o, tuple) else o))
with torch.no_grad():
    model(**enc)
print("forgot h.remove(): a second forward still fires the hook ->", "block.0" in alive)
h.remove()
