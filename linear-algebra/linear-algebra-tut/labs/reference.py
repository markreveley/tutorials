"""Reference implementations of every exercise in linalg.py, plus fixture loading.

Read this file only after your own tests pass, or when a command in the course
needs a working implementation. Every function is small on purpose: the point is
that each one is a few lines of numpy, and that you can say in words what the
lines do to a vector.

Shapes are written as comments in the form (n, d): n rows (tokens), d columns
(dimensions). Vectors are one-dimensional arrays of length d.
"""
import json
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parent / 'data'


# ----------------------------------------------------------------- fixture
def load_fixture(skip_first=False):
    """Return (X, tokens, labels). X is float32 of shape (n_tokens, 768).

    skip_first=True drops position 0, whose activation is far larger than every
    other token's (see data/README.md). Labels are dropped to match.
    """
    X = np.load(DATA / 'activations.npy').astype(np.float32)
    tok = json.loads((DATA / 'tokens.json').read_text())
    labels = json.loads((DATA / 'labels.json').read_text())
    labels['position'] = tok['positions']
    tokens = tok['tokens']
    if skip_first:
        X, tokens = X[1:], tokens[1:]
        labels = {k: v[1:] for k, v in labels.items()}
    return X, tokens, {k: np.asarray(v, dtype=np.float64) for k, v in labels.items()}


def load_head():
    """Return dict of real GPT-2 weights for layer 7, head 0 as float64 arrays.

    float64 so that products such as W_Q @ W_K.T have rounding far below the
    tolerance numpy uses to count rank.
    """
    with np.load(DATA / 'weights.npz') as z:
        return {k: z[k].astype(np.float64) for k in z.files}


# ------------------------------------------------------------ 01-03 vectors
def norm(v):
    """Euclidean length: sqrt(sum of squares)."""
    v = np.asarray(v, dtype=np.float64)
    return float(np.sqrt(np.sum(v * v)))


def cosine(a, b):
    """cos(angle between a and b) = a.b / (|a| |b|). Undefined for a zero vector."""
    a, b = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    na, nb = norm(a), norm(b)
    if na == 0 or nb == 0:
        raise ValueError('cosine similarity is undefined for a zero vector')
    return float(np.dot(a, b) / (na * nb))


def project(v, d):
    """Project v onto the line through direction d.

    Returns (coefficient, projection, residual) where
      coefficient = v.d / |d|         (signed length along the unit direction)
      projection  = coefficient * d / |d|
      residual    = v - projection    (orthogonal to d).
    """
    v, d = np.asarray(v, dtype=np.float64), np.asarray(d, dtype=np.float64)
    nd = norm(d)
    if nd == 0:
        raise ValueError('cannot project onto the zero vector')
    unit = d / nd
    coef = float(np.dot(v, unit))
    proj = coef * unit
    return coef, proj, v - proj


def project_rows(X, d):
    """Coefficient of every row of X along direction d: shape (n,)."""
    X, d = np.asarray(X, dtype=np.float64), np.asarray(d, dtype=np.float64)
    nd = norm(d)
    if nd == 0:
        raise ValueError('cannot project onto the zero vector')
    return X @ (d / nd)


def mean_difference_direction(X, y):
    """Mean of rows with label 1 minus mean of rows with label 0."""
    X, y = np.asarray(X, dtype=np.float64), np.asarray(y)
    if y.sum() == 0 or (1 - y).sum() == 0:
        raise ValueError('both label classes must be present')
    return X[y == 1].mean(axis=0) - X[y == 0].mean(axis=0)


# ----------------------------------------------------- 04-07 matrices, bases
def coordinates_in_basis(v, B):
    """Coordinates c such that B @ c == v, for a basis given as the columns of B."""
    v, B = np.asarray(v, dtype=np.float64), np.asarray(B, dtype=np.float64)
    if B.shape[0] != B.shape[1]:
        raise ValueError('a basis of R^d has d columns of length d')
    c = np.linalg.solve(B, v)
    return c


def rank(A, tol=None):
    """Number of singular values above tolerance (numpy's convention when tol is None)."""
    A = np.asarray(A, dtype=np.float64)
    s = np.linalg.svd(A, compute_uv=False)
    if s.size == 0:
        return 0
    if tol is None:
        tol = s.max() * max(A.shape) * np.finfo(np.float64).eps
    return int((s > tol).sum())


# ------------------------------------------------------- 08 orthogonality
def gram_schmidt(vectors, tol=1e-10):
    """Orthonormalise a list of vectors in order; drop any that are dependent.

    Returns an array Q of shape (k, d) with orthonormal rows, where k is the
    number of independent inputs.
    """
    basis = []
    for v in vectors:
        w = np.asarray(v, dtype=np.float64).copy()
        for q in basis:
            w = w - np.dot(w, q) * q
        # a second pass removes rounding left by the first
        for q in basis:
            w = w - np.dot(w, q) * q
        n = norm(w)
        if n > tol:
            basis.append(w / n)
    return np.array(basis) if basis else np.zeros((0, len(vectors[0])))


def remove_direction(X, d):
    """Return X with the component along d removed from every row."""
    X, d = np.asarray(X, dtype=np.float64), np.asarray(d, dtype=np.float64)
    nd = norm(d)
    if nd == 0:
        raise ValueError('cannot remove the zero direction')
    unit = d / nd
    return X - np.outer(X @ unit, unit)


# --------------------------------------------------------- 09 least squares
def least_squares(X, y, ridge=0.0):
    """Fit y ~ X @ w + b by least squares. Returns (w, b).

    With ridge > 0 the normal equations become (XcᵀXc + ridge·I) w = Xcᵀ yc,
    where Xc and yc are centred. The intercept b makes the fit pass through
    the means. With ridge == 0 and more columns than rows, the minimum-norm
    solution is returned (as numpy.linalg.lstsq does).
    """
    X, y = np.asarray(X, dtype=np.float64), np.asarray(y, dtype=np.float64)
    xm, ym = X.mean(axis=0), y.mean()
    Xc, yc = X - xm, y - ym
    if ridge > 0:
        G = Xc.T @ Xc + ridge * np.eye(X.shape[1])
        w = np.linalg.solve(G, Xc.T @ yc)
    else:
        w = np.linalg.lstsq(Xc, yc, rcond=None)[0]
    b = ym - xm @ w
    return w, float(b)


def predict(X, w, b):
    return np.asarray(X, dtype=np.float64) @ w + b


# ------------------------------------------------- 10-12 covariance, PCA, SVD
def covariance(X):
    """Sample covariance (d, d): centred Xᵀ X divided by n − 1."""
    X = np.asarray(X, dtype=np.float64)
    Xc = X - X.mean(axis=0)
    return Xc.T @ Xc / (X.shape[0] - 1)


def pca(X, k):
    """Top-k principal components of X via SVD of the centred matrix.

    Returns (components, explained, scores):
      components  (k, d): unit-length directions, orthonormal rows
      explained   (k,):   fraction of total variance along each component
      scores      (n, k): coordinates of each centred row along the components
    """
    X = np.asarray(X, dtype=np.float64)
    Xc = X - X.mean(axis=0)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    total = float(np.sum(S ** 2))
    comps = Vt[:k]
    explained = (S[:k] ** 2) / total
    scores = Xc @ comps.T
    return comps, explained, scores


def low_rank(A, k):
    """Best rank-k approximation of A (Eckart–Young): keep the top k singular triples."""
    A = np.asarray(A, dtype=np.float64)
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    return (U[:, :k] * S[:k]) @ Vt[:k]


# ------------------------------------------------------------- 13 gradients
def grad_dot(v, d):
    """Gradient of f(v) = v.d with respect to v: the constant vector d."""
    return np.asarray(d, dtype=np.float64).copy()


def grad_norm(v):
    """Gradient of f(v) = |v| with respect to v: the unit vector v/|v|."""
    v = np.asarray(v, dtype=np.float64)
    n = norm(v)
    if n == 0:
        raise ValueError('the norm is not differentiable at the zero vector')
    return v / n


def numeric_gradient(f, v, h=1e-5):
    """Central finite differences, one coordinate at a time. Slow; for checking."""
    v = np.asarray(v, dtype=np.float64)
    g = np.zeros_like(v)
    for i in range(v.size):
        e = np.zeros_like(v); e[i] = h
        g[i] = (f(v + e) - f(v - e)) / (2 * h)
    return g


# ------------------------------------------------------------ 14 correlation
def correlation(a, b):
    """Pearson correlation between two equal-length sequences."""
    a, b = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    ac, bc = a - a.mean(), b - b.mean()
    den = norm(ac) * norm(bc)
    if den == 0:
        raise ValueError('correlation is undefined when a sequence is constant')
    return float(np.dot(ac, bc) / den)


def split(n, train_fraction=0.7, seed=0):
    """Deterministic shuffled train/held-out index split."""
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n)
    cut = int(round(n * train_fraction))
    return np.sort(idx[:cut]), np.sort(idx[cut:])


def permutation_null(values, y, n_perm=500, seed=0):
    """Correlations between values and shuffled copies of y: the 'no relation' baseline."""
    rng = np.random.default_rng(seed)
    y = np.asarray(y, dtype=np.float64)
    return np.array([correlation(values, rng.permutation(y)) for _ in range(n_perm)])
