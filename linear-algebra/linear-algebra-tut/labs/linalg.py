"""Linear Algebra for Interpretability: the exercises. Implement every function.

Run the tests from the course directory:

  python3 -m unittest discover -s labs -p 'test_*.py' -v

Tests for functions that still raise NotImplementedError are reported as
skipped, with the function name. Make them pass one at a time, in file order,
as the lessons introduce each idea. Use numpy only; np.linalg.svd, lstsq, solve
and eigh are allowed where the docstring says so. reference.py holds a working
version; read it after your own passes, not before.

Convention: a vector is a 1-D array of length d; a matrix of activations has
shape (n, d) with one token per row.
"""
import numpy as np


def norm(v):
    """Lesson 02. Euclidean length of v: the square root of the sum of squares."""
    raise NotImplementedError('norm')


def cosine(a, b):
    """Lesson 02. a.b / (|a| |b|). Raise ValueError if either vector is zero."""
    raise NotImplementedError('cosine')


def project(v, d):
    """Lesson 03. Return (coefficient, projection, residual) of v onto direction d.

    coefficient = v.d / |d|; projection = coefficient * d/|d|; residual = v - projection.
    Raise ValueError if d is the zero vector.
    """
    raise NotImplementedError('project')


def project_rows(X, d):
    """Lesson 03. Coefficient of every row of X along d, as an array of shape (n,)."""
    raise NotImplementedError('project_rows')


def mean_difference_direction(X, y):
    """Lesson 03. Mean of rows where y == 1 minus mean of rows where y == 0.

    Raise ValueError unless both classes are present.
    """
    raise NotImplementedError('mean_difference_direction')


def coordinates_in_basis(v, B):
    """Lesson 06. Coordinates c with B @ c == v, where the basis vectors are the columns of B.

    np.linalg.solve is allowed. Raise ValueError if B is not square.
    """
    raise NotImplementedError('coordinates_in_basis')


def rank(A, tol=None):
    """Lesson 07. Count singular values above tol; np.linalg.svd(A, compute_uv=False) is allowed.

    When tol is None use numpy's convention: max singular value * max(A.shape) * float64 eps.
    """
    raise NotImplementedError('rank')


def gram_schmidt(vectors, tol=1e-10):
    """Lesson 08. Orthonormalise in order, dropping dependent inputs. Return rows (k, d)."""
    raise NotImplementedError('gram_schmidt')


def remove_direction(X, d):
    """Lesson 08. Subtract from every row of X its component along d."""
    raise NotImplementedError('remove_direction')


def least_squares(X, y, ridge=0.0):
    """Lesson 09. Fit y ~ X @ w + b. Return (w, b).

    Centre X and y, solve for w (np.linalg.lstsq when ridge == 0, otherwise the
    ridge normal equations with np.linalg.solve), then set b so the fit passes
    through the means.
    """
    raise NotImplementedError('least_squares')


def covariance(X):
    """Lesson 10. Sample covariance (d, d) of the rows of X, dividing by n - 1."""
    raise NotImplementedError('covariance')


def pca(X, k):
    """Lesson 11. Return (components (k, d), explained (k,), scores (n, k)) using the SVD of centred X."""
    raise NotImplementedError('pca')


def low_rank(A, k):
    """Lesson 12. Best rank-k approximation of A from its SVD."""
    raise NotImplementedError('low_rank')


def grad_dot(v, d):
    """Lesson 13. Gradient of v.d with respect to v."""
    raise NotImplementedError('grad_dot')


def grad_norm(v):
    """Lesson 13. Gradient of |v| with respect to v. Raise ValueError at the zero vector."""
    raise NotImplementedError('grad_norm')


def correlation(a, b):
    """Lesson 14. Pearson correlation. Raise ValueError if either sequence is constant."""
    raise NotImplementedError('correlation')
