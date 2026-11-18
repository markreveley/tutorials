"""Tests for the exercises in linalg.py, with independently known values.

Hand-computed 2-D and 3-D cases come first; invariants (orthonormality,
reconstruction, Pythagoras) follow; the real fixture is used last. A function
that still raises NotImplementedError makes its tests skip, naming the function.

Set LINALG_MODULE=reference to run the same tests against reference.py.
"""
import importlib
import os
import unittest

import numpy as np

import reference as R  # fixture loading only


class Base(unittest.TestCase):
    """Subclasses in test_reference.py rebind M to reference.py."""
    M = importlib.import_module(os.environ.get('LINALG_MODULE', 'linalg'))


def implemented(fn):
    def wrapper(self):
        try:
            return fn(self)
        except NotImplementedError as e:
            self.skipTest(f'implement {e} in labs/linalg.py')
    return wrapper


class Vectors(Base):
    @implemented
    def test_norm_known_values(self):
        self.assertAlmostEqual(self.M.norm([3, 4]), 5.0)
        self.assertAlmostEqual(self.M.norm([1, 2, 2]), 3.0)
        self.assertAlmostEqual(self.M.norm([0, 0, 0]), 0.0)
        self.assertAlmostEqual(self.M.norm(np.ones(16)), 4.0)

    @implemented
    def test_cosine_known_angles(self):
        self.assertAlmostEqual(self.M.cosine([1, 0], [0, 1]), 0.0)
        self.assertAlmostEqual(self.M.cosine([1, 0], [1, 1]), 1 / np.sqrt(2))
        self.assertAlmostEqual(self.M.cosine([2, 0], [-3, 0]), -1.0)
        self.assertAlmostEqual(self.M.cosine([1, 2, 3], [10, 20, 30]), 1.0)  # scale invariant
        with self.assertRaises(ValueError):
            self.M.cosine([0, 0], [1, 2])

    @implemented
    def test_project_hand_computed(self):
        # v = (3, 4) onto d = (1, 0): coefficient 3, projection (3, 0), residual (0, 4)
        c, p, r = self.M.project([3, 4], [1, 0])
        self.assertAlmostEqual(c, 3.0)
        np.testing.assert_allclose(p, [3, 0]); np.testing.assert_allclose(r, [0, 4])
        # v = (3, 4) onto d = (1, 1): coefficient 7/sqrt(2), projection (3.5, 3.5), residual (-0.5, 0.5)
        c, p, r = self.M.project([3, 4], [1, 1])
        self.assertAlmostEqual(c, 7 / np.sqrt(2))
        np.testing.assert_allclose(p, [3.5, 3.5]); np.testing.assert_allclose(r, [-0.5, 0.5])
        # direction length must not matter
        c2, p2, r2 = self.M.project([3, 4], [10, 10])
        self.assertAlmostEqual(c, c2); np.testing.assert_allclose(p, p2)
        with self.assertRaises(ValueError):
            self.M.project([1, 1], [0, 0])

    @implemented
    def test_project_pythagoras_on_real_activations(self):
        X, _, labels = R.load_fixture(skip_first=True)
        X = X.astype(np.float64)
        d = X[5] - X[9]
        for i in (0, 17, 300):
            c, p, r = self.M.project(X[i], d)
            self.assertAlmostEqual(np.dot(r, d), 0.0, places=6)
            self.assertAlmostEqual(np.dot(p, p) + np.dot(r, r), np.dot(X[i], X[i]), places=3)
            np.testing.assert_allclose(p + r, X[i], atol=1e-9)
        coefs = self.M.project_rows(X, d)
        self.assertEqual(coefs.shape, (301,))
        self.assertAlmostEqual(coefs[17], self.M.project(X[17], d)[0])

    @implemented
    def test_mean_difference_direction(self):
        X = np.array([[1.0, 0], [3, 0], [0, 2], [0, 4]])
        y = np.array([1, 1, 0, 0])
        np.testing.assert_allclose(self.M.mean_difference_direction(X, y), [2, -3])
        with self.assertRaises(ValueError):
            self.M.mean_difference_direction(X, np.zeros(4))


class Matrices(Base):
    @implemented
    def test_coordinates_in_basis_hand_computed(self):
        B = np.array([[1.0, 1.0], [0.0, 1.0]])  # columns (1,0) and (1,1)
        np.testing.assert_allclose(self.M.coordinates_in_basis([3, 2], B), [1, 2])
        Q = np.array([[1, 1], [1, -1]]) / np.sqrt(2)  # orthonormal: coordinates are dot products
        v = np.array([2.0, 0.0])
        np.testing.assert_allclose(self.M.coordinates_in_basis(v, Q), Q.T @ v)
        with self.assertRaises(ValueError):
            self.M.coordinates_in_basis([1, 2, 3], np.ones((3, 2)))

    @implemented
    def test_rank_known_cases(self):
        self.assertEqual(self.M.rank(np.eye(4)), 4)
        self.assertEqual(self.M.rank(np.array([[1, 2], [2, 4]])), 1)
        self.assertEqual(self.M.rank(np.zeros((3, 3))), 0)
        self.assertEqual(self.M.rank(np.outer([1, 2, 3], [4, 5]) + np.outer([1, 0, 1], [1, 1])), 2)
        W = R.load_head()
        self.assertEqual(self.M.rank(W['W_Q'] @ W['W_K'].T), 64)


class Orthogonality(Base):
    @implemented
    def test_gram_schmidt_hand_computed(self):
        Q = self.M.gram_schmidt([[1, 1, 0], [1, 0, 0]])
        np.testing.assert_allclose(Q[0], [1, 1, 0] / np.sqrt(2))
        np.testing.assert_allclose(Q[1], [1, -1, 0] / np.sqrt(2), atol=1e-12)
        self.assertEqual(self.M.gram_schmidt([[1, 0], [2, 0], [0, 3]]).shape, (2, 2))
        rng = np.random.default_rng(1)
        V = rng.standard_normal((5, 20))
        Q = self.M.gram_schmidt(V)
        np.testing.assert_allclose(Q @ Q.T, np.eye(5), atol=1e-10)
        # the span is unchanged: every input is reproduced by its projections on Q
        np.testing.assert_allclose((V @ Q.T) @ Q, V, atol=1e-10)

    @implemented
    def test_remove_direction(self):
        X = np.array([[3.0, 4.0], [1.0, 0.0], [0.0, 2.0]])
        np.testing.assert_allclose(self.M.remove_direction(X, [1, 0]), [[0, 4], [0, 0], [0, 2]], atol=1e-12)
        np.testing.assert_allclose(self.M.remove_direction(X, [1, 1]), [[-0.5, 0.5], [0.5, -0.5], [-1, 1]], atol=1e-12)
        Xa, _, _ = R.load_fixture(skip_first=True)
        d = Xa[3]
        Xr = self.M.remove_direction(Xa, d)
        self.assertLess(np.abs(Xr @ d).max() / np.dot(d, d), 1e-9)
        np.testing.assert_allclose(self.M.remove_direction(Xr, d), Xr, atol=1e-6)  # idempotent


class LeastSquares(Base):
    @implemented
    def test_exact_line(self):
        X = np.array([[0.0], [1.0], [2.0], [3.0]])
        y = 2 * X[:, 0] + 1
        w, b = self.M.least_squares(X, y)
        self.assertAlmostEqual(w[0], 2.0); self.assertAlmostEqual(b, 1.0)

    @implemented
    def test_hand_computed_fit(self):
        # Points (0,-1), (1,0.2), (2,0.9), (3,2.1): slope = cov/var = 5.0/5 = 1.0, intercept = mean(y) - mean(x) = 0.55 - 1.5 = -0.95
        X = np.array([[0.0], [1.0], [2.0], [3.0]]); y = np.array([-1.0, 0.2, 0.9, 2.1])
        w, b = self.M.least_squares(X, y)
        self.assertAlmostEqual(w[0], 1.0); self.assertAlmostEqual(b, -0.95)
        # residual orthogonal to the centred column (normal equations)
        resid = y - (X @ w + b)
        self.assertAlmostEqual(float((X[:, 0] - X[:, 0].mean()) @ resid), 0.0)
        self.assertAlmostEqual(float(resid.sum()), 0.0)

    @implemented
    def test_ridge_shrinks_and_fixture_probe(self):
        X, _, labels = R.load_fixture(skip_first=True)
        y = labels['is_digit']
        tr, te = R.split(len(y), 0.7, seed=0)
        w0, b0 = self.M.least_squares(X[tr], y[tr])
        w1, b1 = self.M.least_squares(X[tr], y[tr], ridge=100.0)
        self.assertLess(np.linalg.norm(w1), np.linalg.norm(w0))
        pred = X[te] @ w1 + b1
        self.assertGreater(np.corrcoef(pred, y[te])[0, 1], 0.9)


class Spectra(Base):
    @implemented
    def test_covariance_hand_computed(self):
        X = np.array([[1.0, 2.0], [3.0, 6.0], [5.0, 10.0]])  # second column is twice the first
        C = self.M.covariance(X)
        np.testing.assert_allclose(C, [[4, 8], [8, 16]])
        np.testing.assert_allclose(C, np.cov(X, rowvar=False))

    @implemented
    def test_pca_two_dimensional(self):
        rng = np.random.default_rng(0)
        t = rng.standard_normal(500)
        X = np.stack([3 * t, t], axis=1) + rng.standard_normal((500, 2)) * 0.01  # along (3, 1)
        comps, explained, scores = self.M.pca(X, 2)
        self.assertAlmostEqual(abs(np.dot(comps[0], [3, 1] / np.sqrt(10))), 1.0, places=4)
        self.assertGreater(explained[0], 0.999)
        self.assertAlmostEqual(explained.sum(), 1.0)
        np.testing.assert_allclose(comps @ comps.T, np.eye(2), atol=1e-12)
        np.testing.assert_allclose(scores, (X - X.mean(0)) @ comps.T)

    @implemented
    def test_pca_fixture_invariants(self):
        X, _, _ = R.load_fixture(skip_first=True)
        X = X.astype(np.float64)
        comps, explained, scores = self.M.pca(X, 5)
        self.assertEqual(comps.shape, (5, 768)); self.assertEqual(scores.shape, (301, 5))
        np.testing.assert_allclose(comps @ comps.T, np.eye(5), atol=1e-10)
        self.assertTrue(np.all(np.diff(explained) <= 1e-12))
        # variance along component i equals explained[i] times total variance
        total = np.var(X, axis=0, ddof=0).sum()
        for i in range(5):
            self.assertAlmostEqual(np.var(scores[:, i], ddof=0) / total, explained[i], places=8)
        # eigenvalues of the covariance agree with singular values squared / (n - 1)
        vals = np.linalg.eigvalsh(np.cov(X, rowvar=False))[::-1][:5]
        S = np.linalg.svd(X - X.mean(0), compute_uv=False)[:5]
        np.testing.assert_allclose(vals, S ** 2 / 300, rtol=1e-8)

    @implemented
    def test_low_rank_known_and_eckart_young(self):
        A = np.diag([5.0, 3.0, 1.0])
        np.testing.assert_allclose(self.M.low_rank(A, 2), np.diag([5.0, 3.0, 0.0]), atol=1e-12)
        self.assertAlmostEqual(np.linalg.norm(A - self.M.low_rank(A, 1)), np.sqrt(10))  # sqrt(3^2 + 1^2)
        W = R.load_head()
        W_QK = W['W_Q'] @ W['W_K'].T
        np.testing.assert_allclose(self.M.low_rank(W_QK, 64), W_QK, atol=1e-9)
        self.assertLess(np.linalg.norm(W_QK - self.M.low_rank(W_QK, 32)), np.linalg.norm(W_QK - self.M.low_rank(W_QK, 8)))


class Gradients(Base):
    @implemented
    def test_gradients_match_finite_differences(self):
        d = np.array([1.0, -2.0, 0.5]); v = np.array([0.3, 0.7, -1.1])
        np.testing.assert_allclose(self.M.grad_dot(v, d), d)
        np.testing.assert_allclose(self.M.grad_norm(np.array([3.0, 4.0])), [0.6, 0.8])
        np.testing.assert_allclose(self.M.grad_norm(v), R.numeric_gradient(R.norm, v), atol=1e-7)
        with self.assertRaises(ValueError):
            self.M.grad_norm(np.zeros(3))


class Correlation(Base):
    @implemented
    def test_correlation_known_values(self):
        self.assertAlmostEqual(self.M.correlation([1, 2, 3], [2, 4, 6]), 1.0)
        self.assertAlmostEqual(self.M.correlation([1, 2, 3], [3, 2, 1]), -1.0)
        self.assertAlmostEqual(self.M.correlation([1, 2, 3, 4], [1, 3, 2, 4]), 0.8)  # hand: cov 1.25, sds 1.118 each -> 0.8
        self.assertAlmostEqual(self.M.correlation([1, 0, 1, 0], [5, 5, 5, 6]), -1 / np.sqrt(3))
        with self.assertRaises(ValueError):
            self.M.correlation([1, 1, 1], [1, 2, 3])


if __name__ == '__main__':
    unittest.main()
