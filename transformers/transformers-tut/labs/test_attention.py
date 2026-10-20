"""Tests for labs/attention.py."""
import math
import unittest

from _impl import have, load

if have('torch'):
    import torch
attention = load('attention')

# The pencil example from lesson 05: 3 tokens, d_head = 4, so the scale is 1/2.
Q = [[0.0, 2.0, 0.0, 0.0], [2.0, 0.0, 0.0, 0.0], [2.0, 2.0, 0.0, 0.0]]
K = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [1.0, 1.0, 0.0, 0.0]]
V = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
E = math.e


@unittest.skipUnless(have('torch'), 'torch is not installed; attention tests skipped')
class HandExample(unittest.TestCase):
    def setUp(self):
        self.q, self.k, self.v = (torch.tensor(t) for t in (Q, K, V))

    def test_softmax_rows_sum_to_one_and_match_formula(self):
        p = attention.softmax(torch.tensor([[1.0, 1.0, 2.0]]))
        self.assertTrue(torch.allclose(p.sum(-1), torch.ones(1)))
        expected = torch.tensor([[1 / (2 + E), 1 / (2 + E), E / (2 + E)]])
        self.assertTrue(torch.allclose(p, expected, atol=1e-6))
        big = attention.softmax(torch.tensor([1000.0, 1000.0]))
        self.assertTrue(torch.allclose(big, torch.tensor([0.5, 0.5])))  # no overflow

    def test_causal_mask_is_lower_triangular(self):
        m = attention.causal_mask(3)
        self.assertEqual(m.dtype, torch.bool)
        self.assertEqual(m.tolist(), [[True, False, False], [True, True, False], [True, True, True]])

    def test_pattern_matches_pencil_values(self):
        out, pattern = attention.attention(self.q, self.k, self.v, causal=True)
        expected = torch.tensor([
            [1.0, 0.0, 0.0],
            [E / (E + 1), 1 / (E + 1), 0.0],
            [1 / (2 + E), 1 / (2 + E), E / (2 + E)],
        ])
        self.assertTrue(torch.allclose(pattern, expected, atol=1e-6), pattern)
        self.assertTrue(torch.allclose(out[2], torch.tensor([1 / (2 + E), 1 / (2 + E), E / (2 + E), 0.0]), atol=1e-6))
        self.assertTrue(torch.allclose(out[0], torch.tensor([1.0, 0.0, 0.0, 0.0])))

    def test_non_causal_lets_token_0_see_the_future(self):
        _, pattern = attention.attention(self.q, self.k, self.v, causal=False)
        self.assertGreater(pattern[0, 1].item(), 0.0)
        self.assertTrue(torch.allclose(pattern.sum(-1), torch.ones(3)))


@unittest.skipUnless(have('torch'), 'torch is not installed; attention tests skipped')
class AgainstTorch(unittest.TestCase):
    def test_matches_scaled_dot_product_attention(self):
        torch.manual_seed(0)
        q, k, v = (torch.randn(2, 4, 7, 16) for _ in range(3))  # batch, head, seq, d_head
        for causal in (True, False):
            out, pattern = attention.attention(q, k, v, causal=causal)
            ref = torch.nn.functional.scaled_dot_product_attention(q, k, v, is_causal=causal)
            self.assertEqual(tuple(pattern.shape), (2, 4, 7, 7))
            self.assertTrue(torch.allclose(out, ref, atol=1e-5), f'causal={causal}')
            if causal:
                self.assertTrue(torch.all(pattern.triu(1) == 0))

    def test_split_and_merge_heads_round_trip(self):
        x = torch.arange(2 * 3 * 8, dtype=torch.float32).reshape(2, 3, 8)
        h = attention.split_heads(x, 4)
        self.assertEqual(tuple(h.shape), (2, 4, 3, 2))
        self.assertTrue(torch.equal(h[0, 1, 0], x[0, 0, 2:4]))  # head 1 owns columns 2-3
        self.assertTrue(torch.equal(attention.merge_heads(h), x))

    def test_circuits_have_rank_at_most_d_head(self):
        torch.manual_seed(1)
        d_model, d_head = 12, 3
        W_Q, W_K, W_V, W_O = torch.randn(d_model, d_head), torch.randn(d_model, d_head), torch.randn(d_model, d_head), torch.randn(d_head, d_model)
        qk, ov = attention.qk_circuit(W_Q, W_K), attention.ov_circuit(W_V, W_O)
        self.assertEqual(tuple(qk.shape), (d_model, d_model))
        self.assertEqual(tuple(ov.shape), (d_model, d_model))
        self.assertLessEqual(torch.linalg.matrix_rank(qk).item(), d_head)
        self.assertLessEqual(torch.linalg.matrix_rank(ov).item(), d_head)
        x_q, x_k = torch.randn(d_model), torch.randn(d_model)
        self.assertTrue(torch.allclose(x_q @ qk @ x_k, (x_q @ W_Q) @ (x_k @ W_K), atol=1e-5))


if __name__ == '__main__':
    unittest.main()
