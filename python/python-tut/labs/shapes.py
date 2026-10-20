"""Shape labs: implement each function so that labs/test_shapes.py passes.

These stubs use NumPy only. Every test is a shape assertion first and a value
check second, because shape is the thing you must be able to predict before
running anything. Run from the course directory:

    python3 -m unittest discover -s labs -p 'test_shapes.py' -v

Read labs/ASSESSMENTS.md for the specification and the reasoning each
function should let you explain.
"""
import numpy as np


def broadcast_shape(a_shape, b_shape):
    """Return the broadcast result shape of two shapes, or raise ValueError.

    Pure Python, no NumPy call that does the work for you. Implement the rule
    from lesson 07: align the shapes at the right, treat a missing dimension
    as 1, and at each position the sizes must be equal or one of them 1.
    The result size at that position is the larger of the two.
    """
    raise NotImplementedError("Implement broadcast_shape from the rule in lesson 07")


def row_normalize(x):
    """Divide each row of a (n, d) array by its Euclidean norm.

    Output shape equals input shape. Rows with norm zero stay zero; do not
    divide by zero. Use keepdims so the broadcast is explicit.
    """
    raise NotImplementedError("Implement row_normalize with a keepdims reduction")


def center_last_axis(x):
    """Subtract the mean over the last axis from an array of any rank.

    Output shape equals input shape, and the mean over the last axis of the
    result is zero. This is what TransformerLens's compatibility mode does to
    residual-stream activations (lesson 14).
    """
    raise NotImplementedError("Implement center_last_axis for any rank")


def pairwise_dot(a, b):
    """Dot product of every row of a (n, d) with every row of b (m, d).

    Return shape (n, m). Write it with np.einsum and read the subscript
    string aloud in your explanation.
    """
    raise NotImplementedError("Implement pairwise_dot with einsum")


def causal_attention_pattern(q, k):
    """Scaled, causally masked softmax attention pattern.

    q and k have shape (batch, heads, seq, d_head). Return shape
    (batch, heads, seq, seq) where entry [b, h, i, j] is how much query
    position i attends to key position j. Positions j > i are masked to
    exactly zero, and every row sums to one. Scale scores by 1/sqrt(d_head)
    before the softmax. Compute the softmax in a numerically stable way.
    """
    raise NotImplementedError("Implement causal_attention_pattern with einsum and a mask")


def masked_mean_pool(x, mask):
    """Average positions of x (batch, seq, d) where mask (batch, seq) is nonzero.

    Return shape (batch, d). A row whose mask is all zero returns zeros rather
    than NaN. Padded positions must not contribute to the average.
    """
    raise NotImplementedError("Implement masked_mean_pool with a broadcast mask")
