"""Lesson 11: nn.Module, parameters, state_dict, and reading GPT-2's module tree."""
import os
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error"); os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
import torch
from torch import nn


class TinyMLP(nn.Module):
    def __init__(self, d_model=8, d_hidden=32):
        super().__init__()
        self.up = nn.Linear(d_model, d_hidden)
        self.act = nn.GELU()
        self.down = nn.Linear(d_hidden, d_model)

    def forward(self, x):                       # x: (batch, seq, d_model)
        return self.down(self.act(self.up(x)))


mlp = TinyMLP()
print(mlp)
for name, p in mlp.named_parameters():
    print(f"  {name:12s} {tuple(p.shape)}  requires_grad={p.requires_grad}")
print("state_dict keys:", list(mlp.state_dict()))
print("parameter count:", sum(p.numel() for p in mlp.parameters()))
out = mlp(torch.zeros(2, 5, 8))
print("TinyMLP keeps the shape:", tuple(out.shape))
print("nn.Linear(8, 32).weight is stored as (out, in):", tuple(mlp.up.weight.shape))

from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained("gpt2").eval()
print("\ntop-level children:", [n for n, _ in model.named_children()])
print("transformer children:", [n for n, _ in model.transformer.named_children()])
print("one block:", [n for n, _ in model.transformer.h[0].named_children()])
print("blocks:", len(model.transformer.h), "| parameters:", sum(p.numel() for p in model.parameters()))
for name, p in list(model.named_parameters())[:6]:
    print(f"  {name:36s} {tuple(p.shape)}")
print("lm_head.weight is wte.weight (tied):", model.lm_head.weight.data_ptr() == model.transformer.wte.weight.data_ptr())
print("state_dict entries:", len(model.state_dict()), "| model.training:", model.training)
print("get_submodule('transformer.h.5.mlp'):", type(model.get_submodule("transformer.h.5.mlp")).__name__)
