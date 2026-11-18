"""Tests for labs/gpt2_from_scratch.py: match transformers, then TransformerLens 4 and nnsight."""
import os
import unittest

from _impl import have, load

os.environ.setdefault('HF_HUB_OFFLINE', '1')
os.environ.setdefault('HF_HUB_DISABLE_PROGRESS_BARS', '1')
if have('torch'):
    import torch
impl = load('gpt2_from_scratch')
PROMPT = 'The cat sat on the mat'
LOGIT_TOL = 1e-3      # float32 accumulation order differs; observed max difference is about 1e-4
RESID_TOL = 1e-3


@unittest.skipUnless(have('torch'), 'torch is not installed; GPT-2 tests skipped')
class Components(unittest.TestCase):
    def test_layer_norm_pencil_example(self):
        x = torch.tensor([1.0, 3.0, 5.0, 7.0])
        got = impl.layer_norm(x, torch.ones(4), torch.zeros(4), eps=0.0)
        self.assertTrue(torch.allclose(got, torch.tensor([-3.0, -1.0, 1.0, 3.0]) / 5 ** 0.5, atol=1e-6))
        w, b = torch.tensor([2.0, 1.0, 0.5, 1.0]), torch.tensor([0.0, 1.0, 0.0, -1.0])
        ref = torch.nn.functional.layer_norm(x, (4,), w, b, eps=1e-5)
        self.assertTrue(torch.allclose(impl.layer_norm(x, w, b, eps=1e-5), ref, atol=1e-6))

    def test_gelu_new_matches_tanh_formula(self):
        x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])
        ref = torch.nn.functional.gelu(x, approximate='tanh')
        self.assertTrue(torch.allclose(impl.gelu_new(x), ref, atol=1e-6))
        self.assertAlmostEqual(impl.gelu_new(torch.tensor(1.0)).item(), 0.8412, places=4)

    def test_causal_attention_shapes_and_rows(self):
        torch.manual_seed(0)
        d, n_head, seq = 8, 2, 5
        bp = dict(c_attn_w=torch.randn(d, 3 * d) * 0.3, c_attn_b=torch.zeros(3 * d), c_proj_w=torch.randn(d, d) * 0.3, c_proj_b=torch.zeros(d))
        out, pattern = impl.causal_attention(torch.randn(1, seq, d), bp, n_head)
        self.assertEqual(tuple(out.shape), (1, seq, d))
        self.assertEqual(tuple(pattern.shape), (1, n_head, seq, seq))
        self.assertTrue(torch.allclose(pattern.sum(-1), torch.ones(1, n_head, seq)))
        self.assertTrue(torch.all(pattern.triu(1) == 0), 'future positions must get zero weight')


@unittest.skipUnless(have('torch') and have('transformers'), 'torch/transformers not installed; GPT-2 tests skipped')
class AgainstTransformers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from transformers import AutoTokenizer, GPT2LMHeadModel
        cls.tok = AutoTokenizer.from_pretrained('gpt2')
        cls.hf = GPT2LMHeadModel.from_pretrained('gpt2', attn_implementation='eager').eval()
        cls.params = impl.load_params()
        cls.ids = torch.tensor([cls.tok.encode(PROMPT)])
        with torch.no_grad():
            cls.ref = cls.hf(cls.ids, output_hidden_states=True, output_attentions=True)
            cls.logits, cls.cache = impl.forward_with_cache(cls.ids, cls.params)

    def test_param_keys_and_shapes(self):
        self.assertEqual(tuple(self.params['wte.weight'].shape), (50257, 768))
        self.assertEqual(tuple(self.params['wpe.weight'].shape), (1024, 768))
        self.assertEqual(tuple(self.params['h.0.attn.c_attn.weight'].shape), (768, 2304))
        self.assertEqual(tuple(self.params['h.11.mlp.c_proj.weight'].shape), (3072, 768))
        self.assertNotIn('lm_head.weight', self.params)
        self.assertEqual(len(self.params), 148)

    def test_logits_match_reference(self):
        self.assertEqual(tuple(self.logits.shape), (1, 6, 50257))
        diff = (self.logits - self.ref.logits).abs().max().item()
        self.assertLess(diff, LOGIT_TOL, f'max logit difference {diff}')
        self.assertTrue(torch.equal(self.logits.argmax(-1), self.ref.logits.argmax(-1)))

    def test_every_residual_checkpoint_matches(self):
        for i in range(12):
            diff = (self.cache[f'resid_post.{i}'] - self.ref.hidden_states[i + 1]).abs().max().item() if i < 11 else 0.0
            self.assertLess(diff, RESID_TOL, f'resid_post.{i}')
            self.assertTrue(torch.allclose(self.cache[f'pattern.{i}'], self.ref.attentions[i], atol=1e-4), f'pattern.{i}')
            self.assertEqual(tuple(self.cache[f'mlp_post.{i}'].shape), (1, 6, 3072))
        self.assertTrue(torch.allclose(self.cache['embed'] + self.cache['pos_embed'], self.ref.hidden_states[0], atol=1e-6))
        self.assertLess((self.cache['ln_final'] - self.ref.hidden_states[12]).abs().max().item(), RESID_TOL)

    def test_stream_is_the_sum_of_its_writes(self):
        total = self.cache['embed'] + self.cache['pos_embed']
        for i in range(12):
            self.assertTrue(torch.allclose(self.cache[f'resid_mid.{i}'], self.cache[f'resid_pre.{i}'] + self.cache[f'attn_out.{i}'], atol=1e-5))
            total = total + self.cache[f'attn_out.{i}'] + self.cache[f'mlp_out.{i}']
        self.assertTrue(torch.allclose(total, self.cache['resid_post.11'], atol=1e-3))

    @unittest.skipUnless(have('transformer_lens'), 'transformer_lens not installed')
    def test_matches_transformerlens_without_weight_processing(self):
        from transformer_lens import TransformerBridge
        bridge = TransformerBridge.boot_transformers('gpt2')
        bridge.enable_compatibility_mode(no_processing=True, disable_warnings=True)
        tl_logits, tl_cache = bridge.run_with_cache(self.ids)
        self.assertLess((tl_logits - self.logits).abs().max().item(), LOGIT_TOL)
        for i in (0, 5, 11):
            self.assertLess((tl_cache[f'blocks.{i}.hook_resid_post'] - self.cache[f'resid_post.{i}']).abs().max().item(), RESID_TOL)
            self.assertTrue(torch.allclose(tl_cache[f'blocks.{i}.attn.hook_pattern'], self.cache[f'pattern.{i}'], atol=1e-4))
            self.assertLess((tl_cache[f'blocks.{i}.mlp.hook_post'] - self.cache[f'mlp_post.{i}']).abs().max().item(), RESID_TOL)

    @unittest.skipUnless(have('nnsight'), 'nnsight not installed')
    def test_matches_nnsight(self):
        from nnsight import TransformersModel
        nn = TransformersModel('gpt2', task='text-generation', device_map='cpu', dispatch=True)
        with nn.trace(self.ids):
            mlp5 = nn.transformer.h[5].mlp.output.save()   # request modules in the order they run
            h5 = nn.transformer.h[5].output.save()
            h11 = nn.transformer.h[11].output.save()
            logits = nn.lm_head.output.save()
        self.assertLess((h5 - self.cache['resid_post.5']).abs().max().item(), RESID_TOL)
        self.assertLess((mlp5 - self.cache['mlp_out.5']).abs().max().item(), RESID_TOL)
        self.assertLess((h11 - self.cache['resid_post.11']).abs().max().item(), RESID_TOL)
        self.assertLess((logits - self.logits).abs().max().item(), LOGIT_TOL)


if __name__ == '__main__':
    unittest.main()
