"""Shape assertions for labs/shapes.py. RED on the stubs; no solution here."""
import unittest

import numpy as np

import shapes


class BroadcastShapeTests(unittest.TestCase):
    def test_equal_shapes_are_unchanged(self):
        self.assertEqual(shapes.broadcast_shape((2, 3), (2, 3)), (2, 3))

    def test_missing_leading_dimensions_are_treated_as_one(self):
        self.assertEqual(shapes.broadcast_shape((4, 3), (3,)), (4, 3))
        self.assertEqual(shapes.broadcast_shape((3,), (4, 3)), (4, 3))
        self.assertEqual(shapes.broadcast_shape((), (2, 5)), (2, 5))

    def test_ones_stretch_to_the_other_size(self):
        self.assertEqual(shapes.broadcast_shape((4, 1), (1, 3)), (4, 3))
        self.assertEqual(shapes.broadcast_shape((8, 1, 6, 1), (7, 1, 5)), (8, 7, 6, 5))

    def test_mismatch_raises_value_error(self):
        for a, b in [((4, 3), (4,)), ((2, 3), (3, 2)), ((5,), (6,))]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                shapes.broadcast_shape(a, b)

    def test_agrees_with_numpy_on_random_shapes(self):
        rng = np.random.default_rng(7)
        for _ in range(50):
            a = tuple(int(rng.choice([1, 2, 3])) for _ in range(int(rng.integers(0, 4))))
            b = tuple(int(rng.choice([1, 2, 3])) for _ in range(int(rng.integers(0, 4))))
            try:
                expected = np.broadcast_shapes(a, b)
            except ValueError:
                with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                    shapes.broadcast_shape(a, b)
            else:
                with self.subTest(a=a, b=b):
                    self.assertEqual(shapes.broadcast_shape(a, b), expected)


class RowNormalizeTests(unittest.TestCase):
    def test_shape_is_preserved_and_rows_have_unit_norm(self):
        x = np.random.default_rng(0).normal(size=(5, 768))
        y = shapes.row_normalize(x)
        self.assertEqual(y.shape, (5, 768))
        np.testing.assert_allclose(np.linalg.norm(y, axis=1), np.ones(5), rtol=1e-6)

    def test_zero_rows_stay_zero_without_nan(self):
        x = np.array([[3.0, 4.0], [0.0, 0.0]])
        y = shapes.row_normalize(x)
        np.testing.assert_allclose(y, [[0.6, 0.8], [0.0, 0.0]])

    def test_input_is_not_mutated(self):
        x = np.array([[3.0, 4.0]])
        before = x.copy()
        shapes.row_normalize(x)
        np.testing.assert_array_equal(x, before)


class CenterLastAxisTests(unittest.TestCase):
    def test_works_for_rank_one_two_and_three(self):
        rng = np.random.default_rng(1)
        for shape in [(768,), (5, 768), (2, 5, 768)]:
            x = rng.normal(size=shape) + 3.0
            y = shapes.center_last_axis(x)
            with self.subTest(shape=shape):
                self.assertEqual(y.shape, shape)
                np.testing.assert_allclose(y.mean(axis=-1), np.zeros(shape[:-1]), atol=1e-9)
                np.testing.assert_allclose(y, x - x.mean(axis=-1, keepdims=True))


class PairwiseDotTests(unittest.TestCase):
    def test_shape_is_n_by_m(self):
        a = np.ones((4, 768))
        b = np.ones((7, 768))
        self.assertEqual(shapes.pairwise_dot(a, b).shape, (4, 7))

    def test_values_match_matrix_product_with_transpose(self):
        rng = np.random.default_rng(2)
        a, b = rng.normal(size=(3, 8)), rng.normal(size=(5, 8))
        np.testing.assert_allclose(shapes.pairwise_dot(a, b), a @ b.T)

    def test_mismatched_inner_dimension_fails(self):
        with self.assertRaises(ValueError):
            shapes.pairwise_dot(np.ones((3, 8)), np.ones((5, 9)))


class CausalAttentionPatternTests(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(3)
        self.q = rng.normal(size=(2, 12, 5, 64))
        self.k = rng.normal(size=(2, 12, 5, 64))

    def test_shape_is_batch_heads_seq_seq(self):
        self.assertEqual(shapes.causal_attention_pattern(self.q, self.k).shape, (2, 12, 5, 5))

    def test_rows_sum_to_one_and_future_is_masked(self):
        p = shapes.causal_attention_pattern(self.q, self.k)
        np.testing.assert_allclose(p.sum(axis=-1), np.ones((2, 12, 5)), rtol=1e-6)
        upper = np.triu(np.ones((5, 5), dtype=bool), k=1)
        self.assertTrue(np.all(p[..., upper] == 0.0))
        self.assertTrue(np.all(p >= 0.0))

    def test_first_position_attends_only_to_itself(self):
        p = shapes.causal_attention_pattern(self.q, self.k)
        np.testing.assert_allclose(p[..., 0, 0], np.ones((2, 12)))

    def test_scaling_uses_sqrt_d_head(self):
        q = np.zeros((1, 1, 2, 64)); k = np.zeros((1, 1, 2, 64))
        q[0, 0, 1, 0] = 8.0; k[0, 0, 0, 0] = 1.0
        p = shapes.causal_attention_pattern(q, k)
        score = 8.0 / np.sqrt(64)   # key 0 scores 1.0 after scaling, key 1 scores 0
        expected = np.exp(score) / (np.exp(score) + 1.0)
        self.assertAlmostEqual(p[0, 0, 1, 0], expected, places=6)

    def test_large_scores_do_not_overflow(self):
        p = shapes.causal_attention_pattern(self.q * 1e4, self.k * 1e4)
        self.assertFalse(np.isnan(p).any())


class MaskedMeanPoolTests(unittest.TestCase):
    def test_shape_is_batch_by_d(self):
        x = np.ones((3, 5, 768)); mask = np.ones((3, 5))
        self.assertEqual(shapes.masked_mean_pool(x, mask).shape, (3, 768))

    def test_padding_positions_are_excluded(self):
        x = np.zeros((1, 3, 2)); x[0, 0] = [2.0, 4.0]; x[0, 1] = [4.0, 8.0]; x[0, 2] = [100.0, 100.0]
        mask = np.array([[1, 1, 0]])
        np.testing.assert_allclose(shapes.masked_mean_pool(x, mask), [[3.0, 6.0]])

    def test_all_masked_row_returns_zeros_not_nan(self):
        x = np.ones((2, 4, 3)); mask = np.array([[1, 1, 1, 1], [0, 0, 0, 0]])
        out = shapes.masked_mean_pool(x, mask)
        np.testing.assert_allclose(out[0], np.ones(3))
        np.testing.assert_allclose(out[1], np.zeros(3))
        self.assertFalse(np.isnan(out).any())


if __name__ == "__main__":
    unittest.main()
