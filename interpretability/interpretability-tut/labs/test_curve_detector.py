"""Curve-detector replication, model-free parts (lessons 06 and 07)."""
import unittest

import numpy as np

from _impl import load

C = load('curve_detector')
ANGLES = list(range(0, 360, 10))


def bump(pref, width=2, peak=5.0, opposite=0.0):
    """A synthetic tuning curve peaked at `pref` degrees."""
    c = np.zeros(len(ANGLES))
    for k in range(-width, width + 1):
        c[(pref // 10 + k) % 36] = peak * (1 - abs(k) / (width + 1))
    c[(pref // 10 + 18) % 36] += opposite
    return c


class StimulusChecks(unittest.TestCase):
    def test_arc_shape_range_and_ink(self):
        img = C.render_arc(90, 40)
        self.assertEqual(img.shape, (3, 224, 224)); self.assertEqual(img.dtype, np.float32)
        self.assertGreaterEqual(img.min(), 0.0); self.assertLessEqual(img.max(), 1.0)
        self.assertAlmostEqual(float(img[0, 111, 111]), 0.1, places=1)  # passes through the centre
        self.assertAlmostEqual(float(img[0, 5, 5]), 0.5, places=5)      # background untouched
        dark = (img[0] < 0.3).sum()
        self.assertGreater(dark, 150); self.assertLess(dark, 1500)

    def test_arc_rotates_with_orientation(self):
        a, b = C.render_arc(0, 40)[0], C.render_arc(180, 40)[0]
        # theta + 180 is the arc bent the other way: the 180-degree rotation of the image.
        self.assertLess(np.abs(np.rot90(a, 2) - b).max(), 0.02)
        self.assertGreater(np.abs(a - b).max(), 0.3)
        # theta + 90 is the image rotated by 90 degrees.
        c = C.render_arc(90, 40)[0]
        self.assertLess(np.abs(np.rot90(a, -1) - c).max(), 0.05)

    def test_line_is_symmetric_under_180(self):
        a, b = C.render_line(30)[0], C.render_line(210)[0]
        self.assertLess(np.abs(a - b).max(), 1e-6)
        self.assertAlmostEqual(float(a[111, 111]), 0.1, places=1)
        self.assertGreater(np.abs(C.render_line(30)[0] - C.render_line(120)[0]).max(), 0.3)

    def test_orientation_selectivity(self):
        self.assertAlmostEqual(C.orientation_selectivity(bump(90, width=0), ANGLES), 1.0)
        self.assertAlmostEqual(C.orientation_selectivity(np.ones(36), ANGLES), 0.0)
        self.assertEqual(C.orientation_selectivity(np.zeros(36), ANGLES), 0.0)
        self.assertEqual(C.orientation_selectivity(-np.ones(36), ANGLES), 0.0)
        wide = C.orientation_selectivity(bump(90, width=6), ANGLES)
        self.assertGreater(wide, 0.5); self.assertLess(wide, 1.0)


class EvaluationChecks(unittest.TestCase):
    def test_angular_difference_wraps(self):
        self.assertEqual(C.angular_difference(350, 10), 20)
        self.assertEqual(C.angular_difference(10, 350), 20)
        self.assertEqual(C.angular_difference(90, 270), 180)

    def test_summarise_tuning(self):
        s = C.summarise_tuning(bump(120, peak=4.0, opposite=1.0))
        self.assertEqual(s['pref'], 120); self.assertAlmostEqual(s['peak'], 4.0)
        self.assertAlmostEqual(s['opp_ratio'], 0.25)

    def test_select_candidates_prefers_strong_selective_channels(self):
        rng = np.random.default_rng(0)
        curves = rng.normal(0, 0.1, size=(20, 36))
        curves[3] = bump(40, peak=6.0); curves[7] = bump(200, peak=5.0)
        curves[11] = np.full(36, 6.0)  # strong but flat
        self.assertEqual(C.select_candidates(curves, 2), [3, 7])

    def test_curve_detector_passes_and_line_detector_fails(self):
        screen, held, inv = bump(40), bump(50, peak=6.0), bump(40, peak=4.0)
        line = np.full(36, 0.5)
        r = C.evaluate_candidate(screen, held, inv, line)
        self.assertTrue(all(r[h] for h in ('H1', 'H2', 'H3', 'H4')))
        # A line detector responds equally at theta and theta+180 and as much to lines.
        line_like = bump(40, peak=6.0, opposite=6.0)
        r = C.evaluate_candidate(line_like, line_like, line_like, np.full(36, 6.0))
        self.assertTrue(r['H1']); self.assertFalse(r['H2']); self.assertFalse(r['H4'])
        # A unit that changes its preference on held-out stimuli fails H1.
        r = C.evaluate_candidate(bump(40), bump(130), bump(40), line)
        self.assertFalse(r['H1'])
        # A unit silent under inverted contrast fails H3.
        r = C.evaluate_candidate(bump(40), bump(40), np.zeros(36), line)
        self.assertFalse(r['H3'])

    def test_largest_gap(self):
        self.assertEqual(C.largest_gap([10, 100, 190, 280]), 90)
        self.assertEqual(C.largest_gap([0, 90, 180]), 180)
        self.assertEqual(C.largest_gap([270, 270, 10]), 260)


class ModelSmokeTest(unittest.TestCase):
    def test_inception3b_output_shape(self):
        try:
            import torch
            from torchvision.models import GoogLeNet_Weights, googlenet
            model = googlenet(weights=GoogLeNet_Weights.IMAGENET1K_V1).eval()
        except Exception as exc:  # pragma: no cover - environment without the cached weights
            self.skipTest(f'torchvision GoogLeNet unavailable: {exc}')
        store = {}
        h = model.inception3b.register_forward_hook(lambda m, i, o: store.__setitem__('o', o))
        with torch.no_grad():
            model(torch.from_numpy(C.render_arc(90, 40))[None])
        h.remove()
        self.assertEqual(tuple(store['o'].shape), (1, 480, 28, 28))
        self.assertGreaterEqual(float(store['o'].min()), 0.0)


if __name__ == '__main__':
    unittest.main()
