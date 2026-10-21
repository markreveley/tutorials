"""Lesson 08: reductions over axes, and einsum read aloud."""
import numpy as np

acts = np.arange(2 * 3 * 4, dtype=float).reshape(2, 3, 4)    # (batch, seq, d)
print("acts.sum()           ->", acts.sum(), "(a scalar: every axis reduced)")
print("acts.sum(axis=0)     ->", acts.sum(axis=0).shape, "(batch gone)")
print("acts.mean(axis=1)    ->", acts.mean(axis=1).shape, "(seq gone)")
print("acts.max(axis=-1)    ->", acts.max(axis=-1).shape, "(d gone)")
print("acts.argmax(axis=-1) ->", acts.argmax(axis=-1).shape, "indices into d")
print("acts.mean(axis=(0, 1)) ->", acts.mean(axis=(0, 1)).shape, "(one vector per feature)")
print("np.linalg.norm(acts, axis=-1) ->", np.linalg.norm(acts, axis=-1).shape)

rng = np.random.default_rng(0)
x = rng.normal(size=(5, 768))       # 5 token vectors
d = rng.normal(size=(768,))         # one direction
print("\neinsum 'sd,d->s'  :", np.einsum("sd,d->s", x, d).shape, "== x @ d:", np.allclose(np.einsum("sd,d->s", x, d), x @ d))
y = rng.normal(size=(7, 768))
print("einsum 'sd,td->st':", np.einsum("sd,td->st", x, y).shape, "== x @ y.T:", np.allclose(np.einsum("sd,td->st", x, y), x @ y.T))
q = rng.normal(size=(2, 12, 5, 64)); k = rng.normal(size=(2, 12, 5, 64))
scores = np.einsum("bhqd,bhkd->bhqk", q, k)
print("einsum 'bhqd,bhkd->bhqk':", scores.shape, "(batch, heads, query pos, key pos)")
print("einsum 'ii->i' diagonal:", np.einsum("ii->i", np.eye(3) * 5))
print("einsum 'ij->ji' transpose:", np.einsum("ij->ji", np.arange(6).reshape(2, 3)).shape)
print("einsum 'bsd->bd' sums over seq:", np.einsum("bsd->bd", acts).shape, "== acts.sum(axis=1):", np.allclose(np.einsum("bsd->bd", acts), acts.sum(axis=1)))
W = rng.normal(size=(768, 3072))
print("batched matmul 'bsd,de->bse':", np.einsum("bsd,de->bse", rng.normal(size=(2, 5, 768)), W).shape)
