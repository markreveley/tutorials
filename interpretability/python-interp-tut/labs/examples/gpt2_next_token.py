"""Lesson 12: tokenizer, input ids, logits, next-token prediction, hidden states."""
import os
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error"); os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2").eval()

prompt = "The capital of France is"
enc = tokenizer(prompt, return_tensors="pt")
ids = enc["input_ids"]
print("input_ids:", ids.tolist(), "shape", tuple(ids.shape))
print("tokens:   ", tokenizer.convert_ids_to_tokens(ids[0]))
print("note the leading space is part of the token (Ġ shows it)")

with torch.no_grad():
    out = model(**enc, output_hidden_states=True)
print("logits:", tuple(out.logits.shape), "= (batch, seq, vocab)")
last = out.logits[0, -1]                     # scores for the token after the last position
top = torch.topk(last.softmax(-1), 5)
for p, i in zip(top.values, top.indices):
    print(f"  {p.item():.3f}  {tokenizer.decode(i)!r}")
print("hidden_states:", len(out.hidden_states), "tensors, each", tuple(out.hidden_states[0].shape))
print("hidden_states[0] is the embedding output; [12] has the final LayerNorm applied")
print("hidden_states[6] is the residual stream after block 5 (zero-indexed)")
norms = torch.stack([h[0, -1].norm() for h in out.hidden_states])
print("norm of the last position across layers:", [round(n, 1) for n in norms.tolist()])

print("tokenizer.pad_token before:", tokenizer.pad_token)
tokenizer.pad_token = tokenizer.eos_token
batch = tokenizer(["The capital of France is", "Hello"], return_tensors="pt", padding=True)
print("batched input_ids:\n", batch["input_ids"])
print("attention_mask:\n", batch["attention_mask"])
with torch.no_grad():
    out2 = model(**batch, output_hidden_states=True)
print("batched hidden_states[6]:", tuple(out2.hidden_states[6].shape))
print("prompt 0 unchanged by batching:", torch.allclose(out2.hidden_states[6][0], out.hidden_states[6][0], atol=1e-4))
