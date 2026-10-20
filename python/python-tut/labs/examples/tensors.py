"""Lesson 09: torch tensors: dtype, device, views, in-place ops, no_grad."""
import numpy as np
import torch

t = torch.arange(12).reshape(3, 4)
print(t.shape, t.dtype, t.device, "| torch.Size is a tuple subclass:", isinstance(t.shape, tuple))
f = torch.tensor([1.0, 2.0])
print("default float dtype:", f.dtype, "| float16 after .half():", f.half().dtype, "| .to(torch.float64):", f.to(torch.float64).dtype)
try:
    torch.tensor([1.0]) @ torch.tensor([1.0], dtype=torch.float64)
except RuntimeError as exc:
    print("dtype mismatch is an error, not a promotion:", str(exc)[:84])

a = torch.zeros(2, 3)
v = a.view(6)              # same storage
v[0] = 7.0
print("view shares storage; a[0, 0] is now", a[0, 0].item(), "| same storage:", v.data_ptr() == a.data_ptr())
tt = a.t()
print("transpose is a view; contiguous?", tt.is_contiguous())
try:
    tt.view(6)
except RuntimeError:
    print(".view on a non-contiguous tensor fails; use .reshape or .contiguous()", tt.reshape(6).shape)

b = torch.ones(3)
b.add_(1)                  # trailing underscore: in place
print("in-place add_ changed b:", b)
c = b
c.mul_(2)
print("through an alias too:", b)

n = np.ones(3)
shared = torch.from_numpy(n)   # shares memory with the NumPy array
shared[0] = 5
print("torch.from_numpy shares memory: n[0] =", n[0], "| .numpy() back:", shared.numpy().dtype)

w = torch.ones(3, requires_grad=True)
y = (w * 2).sum()
print("y.requires_grad:", y.requires_grad, "| grad_fn:", type(y.grad_fn).__name__)
with torch.no_grad():
    z = (w * 2).sum()
print("under no_grad:", z.requires_grad, "| grad_fn:", z.grad_fn)
d = w.detach()
print("detach() shares data but leaves the graph:", d.requires_grad, d.data_ptr() == w.data_ptr())
try:
    w.numpy()
except RuntimeError as exc:
    print("w.numpy() with requires_grad fails:", str(exc)[:58])
print("w.detach().numpy() works:", w.detach().numpy())
print("one element to Python:", torch.tensor([3.5]).item(), "| tolist:", torch.arange(3).tolist())
