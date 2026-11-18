"""Lesson 15: seeds, safetensors, a run manifest, memory and batching on CPU."""
import os
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error"); os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
import hashlib
import json
from pathlib import Path
import tempfile
import time
import numpy as np
import torch
from safetensors.torch import load_file, save_file
from transformers import AutoModelForCausalLM, AutoTokenizer

torch.manual_seed(0)
a = torch.randn(3)
torch.manual_seed(0)
b = torch.randn(3)
print("same seed, same draw:", torch.equal(a, b), a.tolist())
print("numpy has its own generator:", np.random.default_rng(0).normal(size=2).round(3).tolist())

tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained("gpt2").eval()
prompts = ["The capital of France is", "Hello"]
enc = tokenizer(prompts, return_tensors="pt", padding=True)
with torch.no_grad():
    t0 = time.perf_counter(); out = model(**enc, output_hidden_states=True); dt = time.perf_counter() - t0
hs = torch.stack(out.hidden_states)          # (13, batch, seq, 768)
print("stacked hidden states:", tuple(hs.shape), f"| {hs.numel() * 4 / 1e6:.2f} MB in float32")
print("a 1024-token prompt would need", f"{13 * 1024 * 768 * 4 / 1e6:.0f} MB for the same stack; a batch of 32 of them", f"{32 * 13 * 1024 * 768 * 4 / 1e9:.1f} GB")
with torch.no_grad():
    again = torch.stack(model(**enc, output_hidden_states=True).hidden_states)
print("repeat forward pass identical:", torch.equal(hs, again))

tensors = {f"block.{i}": out.hidden_states[i + 1].contiguous() for i in range(12)}
tensors["embed"] = out.hidden_states[0].contiguous()
with tempfile.TemporaryDirectory() as d:
    path = Path(d) / "resid.safetensors"
    save_file(tensors, path)
    back = load_file(path)
    print("safetensors round trip:", len(back), "tensors,", f"{path.stat().st_size / 1e6:.2f} MB,", "block.5 equal:", torch.equal(back["block.5"], tensors["block.5"]))
    manifest = {
        "model": "gpt2", "prompts": prompts, "seed": 0,
        "versions": {"torch": torch.__version__, "numpy": np.__version__},
        "tensors": {k: {"shape": list(v.shape), "dtype": str(v.dtype).replace("torch.", ""),
                        "sha256": hashlib.sha256(v.numpy().tobytes()).hexdigest()[:16] + "..."} for k, v in tensors.items()},
        "attention_mask": enc["attention_mask"].tolist(),
    }
    (Path(d) / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print("manifest keys:", sorted(manifest), "| block.5 entry:", manifest["tensors"]["block.5"])
