"""Lesson 01: confirm the toolchain and print the shapes you will see all course."""
import os
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

print("python", sys.version.split()[0])
import numpy as np
print("numpy", np.__version__)
try:
    import torch
except ImportError:
    print("torch   missing: see the install steps above")
    sys.exit(1)
print("torch", torch.__version__, "| cuda available:", torch.cuda.is_available())
try:
    import transformers
    print("transformers", transformers.__version__)
except ImportError:
    print("transformers missing")
    sys.exit(1)

x = torch.zeros(2, 5, 768)
print("a batch of 2 prompts, 5 tokens each, 768 numbers per token:", tuple(x.shape))
print("x.shape[0] is the batch:", x.shape[0], "| x.shape[-1] is d_model:", x.shape[-1])
