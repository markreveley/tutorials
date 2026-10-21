"""Lesson 06: NumPy arrays: shape, dtype, indexing, slicing, views."""
import numpy as np

a = np.arange(12).reshape(3, 4)
print(a)
print("shape", a.shape, "| ndim", a.ndim, "| dtype", a.dtype, "| size", a.size)
print("a[1, 2] =", a[1, 2], "| a[1] row:", a[1], "shape", a[1].shape)
print("a[:, 2] column:", a[:, 2], "shape", a[:, 2].shape)
print("a[1:, ::2] shape", a[1:, ::2].shape)
print("a[-1, -1] =", a[-1, -1])

row = a[0]                 # a view, not a copy
row[0] = 99
print("writing through the view changed a[0, 0]:", a[0, 0])
copy = a[0].copy(); copy[0] = -1
print("writing to a copy did not touch a; a[0, 0] is still", a[0, 0])

print("float division of ints gives float64:", (a / 2).dtype)
x = np.array([1, 2, 3], dtype=np.float32)
print("float32 stays float32 under +1.0:", (x + 1.0).dtype, "| promotes with float64 array:", (x + np.array([1.0])).dtype)
print("integer overflow is silent in int8:", np.array([120], dtype=np.int8) + np.int8(10))

mask = a > 5
print("boolean mask shape", mask.shape, "| selected values:", a[mask])
print("a[[0, 2]] picks rows 0 and 2 -> shape", a[[0, 2]].shape)
print("a[None].shape (new leading axis):", a[None].shape, "| a[:, None].shape:", a[:, None].shape)
print("a.reshape(-1).shape:", a.reshape(-1).shape, "| a.T.shape:", a.T.shape, "| contiguous?", a.T.flags["C_CONTIGUOUS"])
