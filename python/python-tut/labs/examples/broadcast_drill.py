"""Lesson 07: predict the result shape before reading the answer."""
import numpy as np

pairs = [((4, 3), (3,)), ((4, 3), (4, 1)), ((4, 3), (4,)), ((2, 1, 5), (3, 1)),
         ((8, 1, 6, 1), (7, 1, 5)), ((5, 768), (768,)), ((2, 5, 768), (2, 1, 768)),
         ((2, 5, 768), (5,)), ((12, 5, 5), (5, 5)), ((1,), (3, 4))]
for a, b in pairs:
    try:
        shape = (np.zeros(a) + np.zeros(b)).shape
        print(f"{str(a):>16} + {str(b):<12} -> {shape}")
    except ValueError as exc:
        print(f"{str(a):>16} + {str(b):<12} -> ValueError: {str(exc).split(' with ')[0]}")

acts = np.arange(2 * 3 * 4, dtype=float).reshape(2, 3, 4)   # (batch, seq, d)
mean = acts.mean(axis=-1)
print("\nmean over d without keepdims:", mean.shape)
try:
    acts - mean
except ValueError as exc:
    print("acts - mean fails:", str(exc).split(' with ')[0])
mean_k = acts.mean(axis=-1, keepdims=True)
print("with keepdims:", mean_k.shape, "-> (acts - mean_k).shape =", (acts - mean_k).shape)
print("explicit alternative mean[..., None]:", mean[..., None].shape)
