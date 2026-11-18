"""Lesson 10: what a gradient is operationally, and a tiny gradient-descent fit."""
import torch

torch.manual_seed(0)
x = torch.linspace(0, 1, 50)
y_true = 3.0 * x + 1.0 + 0.05 * torch.randn(50)       # a line with noise

w = torch.tensor(0.0, requires_grad=True)
b = torch.tensor(0.0, requires_grad=True)

loss = ((w * x + b - y_true) ** 2).mean()
loss.backward()
print(f"at w=0, b=0: loss {loss.item():.3f}, dloss/dw {w.grad.item():.3f}, dloss/db {b.grad.item():.3f}")
print("negative gradient says: increase w and b")

# finite-difference check of what the gradient means
eps = 1e-3
with torch.no_grad():
    bumped = (((w + eps) * x + b - y_true) ** 2).mean()
print(f"(loss(w+eps) - loss(w)) / eps = {((bumped - loss) / eps).item():.3f}  (close to dloss/dw)")

lr = 0.5
for step in range(201):
    w.grad = None; b.grad = None                      # gradients accumulate unless cleared
    loss = ((w * x + b - y_true) ** 2).mean()
    loss.backward()
    with torch.no_grad():                            # the update must not be recorded
        w -= lr * w.grad
        b -= lr * b.grad
    if step % 50 == 0:
        print(f"step {step:3d}  loss {loss.item():.4f}  w {w.item():.3f}  b {b.item():.3f}")
print(f"fit: y = {w.item():.2f} x + {b.item():.2f}   (true 3.00 x + 1.00)")

g = torch.ones(3, requires_grad=True)
(g * 2).sum().backward(); (g * 2).sum().backward()
print("two backward() calls without clearing: grad =", g.grad, "(accumulated, not replaced)")
