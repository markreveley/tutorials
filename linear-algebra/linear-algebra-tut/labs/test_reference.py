"""Runs the exercise tests against reference.py, and checks the fixture and the CLI."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

import numpy as np

import reference as R
import test_linalg as T

HERE = Path(__file__).resolve().parent


class ReferenceVectors(T.Vectors): M = R
class ReferenceMatrices(T.Matrices): M = R
class ReferenceOrthogonality(T.Orthogonality): M = R
class ReferenceLeastSquares(T.LeastSquares): M = R
class ReferenceSpectra(T.Spectra): M = R
class ReferenceGradients(T.Gradients): M = R
class ReferenceCorrelation(T.Correlation): M = R


class Fixture(unittest.TestCase):
    def test_shapes_and_sizes(self):
        X, tokens, labels = R.load_fixture()
        self.assertEqual(X.shape, (302, 768)); self.assertEqual(X.dtype, np.float32)
        self.assertEqual(len(tokens), 302)
        for k in ('is_digit', 'after_period', 'starts_with_space', 'capitalised', 'position'):
            self.assertEqual(labels[k].shape, (302,))
        self.assertTrue(np.isfinite(X).all())
        raw = np.load(HERE / 'data/activations.npy')
        self.assertEqual(raw.dtype, np.float16)
        total = sum(p.stat().st_size for p in (HERE / 'data').iterdir())
        self.assertLess(total, 2_000_000)

    def test_labels_agree_with_tokens(self):
        X, tokens, labels = R.load_fixture()
        self.assertEqual(int(labels['is_digit'].sum()), sum(t.strip().isdigit() for t in tokens))
        self.assertEqual(labels['after_period'][0], 0)
        self.assertEqual(int(labels['after_period'].sum()), sum(tokens[i - 1].strip() in {'.', '?', '!'} for i in range(1, len(tokens))))

    def test_first_token_is_the_outlier(self):
        X, tokens, _ = R.load_fixture()
        norms = np.linalg.norm(X, axis=1)
        self.assertGreater(norms[0], 20 * np.median(norms))
        self.assertLess(norms[1:].max(), 2 * np.median(norms))

    def test_head_weights(self):
        W = R.load_head()
        self.assertEqual(W['W_Q'].shape, (768, 64)); self.assertEqual(W['W_O'].shape, (64, 768))
        meta = json.loads((HERE / 'data/meta.json').read_text())
        self.assertEqual(meta['layer'], 6); self.assertEqual(meta['head']['layer'], 7)

    def test_split_is_a_partition(self):
        tr, te = R.split(301, 0.7, seed=0)
        self.assertEqual(len(tr) + len(te), 301)
        self.assertEqual(len(set(tr) | set(te)), 301)


class CommandLine(unittest.TestCase):
    def run_lab(self, *args):
        r = subprocess.run([sys.executable, str(HERE / 'linalg_lab.py'), *args], capture_output=True, text=True, timeout=120)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def test_help_lists_every_lesson_command(self):
        out = self.run_lab('--help')
        for c in ('inspect', 'project', 'probe', 'pca', 'svd', 'gradient', 'correlation', 'review'):
            self.assertIn(c, out)

    def test_project_output_is_consistent(self):
        out = self.run_lab('project', '--label', 'is_digit', '--token', '12')
        self.assertIn('coefficient 19.71', out)
        self.assertIn('resid.d', out)

    def test_bad_label_rejected(self):
        r = subprocess.run([sys.executable, str(HERE / 'linalg_lab.py'), 'project', '--label', 'nonsense'], capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)


if __name__ == '__main__':
    unittest.main()
