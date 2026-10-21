"""Environment check: this file passes as shipped; it tests your setup, not you.

    python3 -m unittest discover -s labs -p 'test_environment.py' -v
"""
import os
import sys
import unittest

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")


class PythonAndNumpyTests(unittest.TestCase):
    def test_python_is_recent_enough(self):
        self.assertGreaterEqual(sys.version_info[:2], (3, 10), "use Python 3.10 or newer")

    def test_numpy_broadcasts_a_row_against_a_matrix(self):
        import numpy as np
        self.assertEqual((np.ones((4, 3)) + np.arange(3)).shape, (4, 3))


class TorchTests(unittest.TestCase):
    def setUp(self):
        try:
            import torch
        except ImportError:
            self.skipTest("torch is not installed; see lesson 01 for the CPU-only install")
        self.torch = torch

    def test_matmul_shape_and_no_grad(self):
        torch = self.torch
        a = torch.ones(2, 3); b = torch.ones(3, 5)
        with torch.no_grad():
            c = a @ b
        self.assertEqual(tuple(c.shape), (2, 5))
        self.assertFalse(c.requires_grad)


class GPT2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError:
            raise unittest.SkipTest("torch and transformers are needed for the GPT-2 checks")
        try:
            cls.tokenizer = AutoTokenizer.from_pretrained("gpt2")
            cls.model = AutoModelForCausalLM.from_pretrained("gpt2").eval()
        except Exception as exc:
            raise unittest.SkipTest(f"gpt2 is not in the local cache (run once online to download it): {exc}")
        cls.torch = torch

    def test_thirteen_hidden_states_of_batch_seq_768(self):
        enc = self.tokenizer("The capital of France is", return_tensors="pt")
        with self.torch.no_grad():
            out = self.model(**enc, output_hidden_states=True)
        self.assertEqual(len(out.hidden_states), 13)
        self.assertEqual(tuple(out.hidden_states[0].shape), (1, 5, 768))
        self.assertEqual(tuple(out.logits.shape), (1, 5, 50257))

    def test_config_matches_gpt2_small(self):
        c = self.model.config
        self.assertEqual((c.n_layer, c.n_embd, c.n_head), (12, 768, 12))


if __name__ == "__main__":
    unittest.main()
