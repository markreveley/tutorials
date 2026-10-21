"""Hook assertions for labs/hooks.py. RED on the stubs; skips without torch."""
import unittest

try:
    import torch
    from transformers import AutoModelForCausalLM  # noqa: F401
    HAVE_TORCH = True
except ImportError:  # pragma: no cover - environment dependent
    HAVE_TORCH = False

import hooks


@unittest.skipUnless(HAVE_TORCH, "torch and transformers are needed; install them in a virtualenv (lesson 01)")
class ResidualStreamCacheTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.tokenizer, cls.model = hooks.load_gpt2()
        except Exception as exc:  # offline cache missing
            raise unittest.SkipTest(f"gpt2 weights are not available offline: {exc}")
        cls.enc = cls.tokenizer(["The capital of France is", "Hello"], return_tensors="pt", padding=True)
        cls.hook_counts = [len(b._forward_hooks) for b in cls.model.transformer.h]

    def cache(self):
        return hooks.cache_residual_stream(self.model, self.enc["input_ids"], self.enc["attention_mask"])

    def test_thirteen_entries_in_order(self):
        cache = self.cache()
        self.assertEqual(list(cache), ["embed"] + [f"block.{i}" for i in range(12)])

    def test_every_entry_is_batch_seq_768_float32_detached(self):
        cache = self.cache()
        batch, seq = self.enc["input_ids"].shape
        for name, value in cache.items():
            with self.subTest(name=name):
                self.assertEqual(tuple(value.shape), (batch, seq, 768))
                self.assertEqual(value.dtype, torch.float32)
                self.assertFalse(value.requires_grad)
                self.assertTrue(torch.isfinite(value).all())

    def test_matches_output_hidden_states_except_the_final_layernorm(self):
        cache = self.cache()
        with torch.no_grad():
            out = self.model(**self.enc, output_hidden_states=True)
        self.assertTrue(torch.equal(cache["embed"], out.hidden_states[0]))
        for i in range(11):
            with self.subTest(block=i):
                self.assertTrue(torch.equal(cache[f"block.{i}"], out.hidden_states[i + 1]))
        # hidden_states[12] has ln_f applied; the block 11 output does not.
        self.assertFalse(torch.equal(cache["block.11"], out.hidden_states[12]))
        with torch.no_grad():
            self.assertTrue(torch.allclose(self.model.transformer.ln_f(cache["block.11"]), out.hidden_states[12], atol=1e-5))

    def test_hooks_are_removed_after_the_call(self):
        self.cache()
        self.assertEqual([len(b._forward_hooks) for b in self.model.transformer.h], self.hook_counts)
        self.assertEqual(len(self.model.transformer.drop._forward_hooks), 0)

    def test_hooks_are_removed_even_when_forward_fails(self):
        bad_ids = torch.full((1, 3), 10**6)  # out of vocabulary: the embedding lookup raises
        with self.assertRaises(Exception):
            hooks.cache_residual_stream(self.model, bad_ids)
        self.assertEqual([len(b._forward_hooks) for b in self.model.transformer.h], self.hook_counts)

    def test_cached_values_are_copies(self):
        a = self.cache(); b = self.cache()
        a["block.3"].add_(1.0)
        self.assertFalse(torch.equal(a["block.3"], b["block.3"]))


@unittest.skipUnless(HAVE_TORCH, "torch is needed for assert_cache_shapes")
class AssertCacheShapesTests(unittest.TestCase):
    def good(self, batch=2, seq=5):
        names = ["embed"] + [f"block.{i}" for i in range(12)]
        return {n: torch.zeros(batch, seq, 768) for n in names}

    def test_valid_cache_is_returned_unchanged(self):
        cache = self.good()
        self.assertIs(hooks.assert_cache_shapes(cache, 2, 5), cache)

    def test_wrong_shape_wrong_dtype_wrong_keys_nan_and_grad_are_rejected(self):
        bad = []
        c = self.good(); c["block.4"] = torch.zeros(2, 6, 768); bad.append(("seq", c))
        c = self.good(); c["block.4"] = torch.zeros(2, 5, 767); bad.append(("d_model", c))
        c = self.good(); c["block.4"] = torch.zeros(2, 5, 768, dtype=torch.float16); bad.append(("dtype", c))
        c = self.good(); del c["block.11"]; bad.append(("missing key", c))
        c = self.good(); c["extra"] = torch.zeros(2, 5, 768); bad.append(("extra key", c))
        c = self.good(); c["embed"][0, 0, 0] = float("nan"); bad.append(("nan", c))
        c = self.good(); c["embed"] = torch.zeros(2, 5, 768, requires_grad=True); bad.append(("grad", c))
        c = {k: v for k, v in reversed(list(self.good().items()))}; bad.append(("order", c))
        for label, cache in bad:
            with self.subTest(label=label), self.assertRaises(AssertionError):
                hooks.assert_cache_shapes(cache, 2, 5)


if __name__ == "__main__":
    unittest.main()
