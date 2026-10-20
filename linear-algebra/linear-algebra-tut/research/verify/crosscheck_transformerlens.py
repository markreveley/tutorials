"""One-off cross-check: TransformerLens blocks.6.hook_resid_post equals the fixture."""
import json, numpy as np, torch
from transformer_lens import TransformerBridge
import transformer_lens, importlib.metadata as m
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'labs'))
from make_data import PASSAGE, LAYER
acts = np.load(Path(__file__).resolve().parents[2] / 'labs/data/activations.npy').astype(np.float32)
bridge = TransformerBridge.boot_transformers('gpt2')
bridge.enable_compatibility_mode()
_, cache = bridge.run_with_cache(PASSAGE, prepend_bos=False)
key = f'blocks.{LAYER}.hook_resid_post'
tl = cache[key][0].detach().numpy()
print('transformer_lens', m.version('transformer_lens'), 'torch', torch.__version__)
print(key, 'shape', tl.shape, 'fixture shape', acts.shape)
print('max |TL - fixture(float16)|', float(np.abs(tl - acts).max()))
print('max |TL| overall', float(np.abs(tl).max()))
print('relative error', float(np.abs(tl - acts).max() / np.abs(tl).max()))
