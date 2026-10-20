"""Reference solution for labs/curve_detector.py: stimuli, tuning-curve summaries,
candidate selection, and the held-out hypothesis checks."""
import numpy as np

try:
    from .vision_common import orientation_selectivity, render_arc, render_line  # noqa: F401
except ImportError:  # run as a script from labs/reference
    from vision_common import orientation_selectivity, render_arc, render_line  # noqa: F401

ANGLES = list(range(0, 360, 10))


def angular_difference(a, b):
    return abs((a - b + 180) % 360 - 180)


def summarise_tuning(curve, angles=ANGLES):
    curve = np.asarray(curve, dtype=np.float64)
    pi = int(np.argmax(curve)); peak = float(curve[pi])
    opp = float(curve[(pi + len(angles) // 2) % len(angles)])
    return dict(pref=angles[pi], peak=peak, opp=opp,
                opp_ratio=(opp / peak) if peak > 0 else float('nan'),
                sel=orientation_selectivity(curve, angles))


def select_candidates(screen_curves, k, angles=ANGLES):
    """Top-k channels by (clipped peak x selectivity) on the screening tuning curves."""
    screen_curves = np.asarray(screen_curves, dtype=np.float64)
    peak = np.clip(screen_curves.max(axis=1), 0, None)
    sel = np.array([orientation_selectivity(c, angles) for c in screen_curves])
    return [int(c) for c in np.argsort(-(peak * sel))[:k]]


def evaluate_candidate(screen_curve, held_curve, inverted_curve, line_curve, angles=ANGLES):
    """The four pre-registered held-out hypotheses for one channel."""
    s, h, v = summarise_tuning(screen_curve, angles), summarise_tuning(held_curve, angles), summarise_tuning(inverted_curve, angles)
    line_peak = float(np.max(line_curve))
    return dict(s_pref=s['pref'], s_peak=s['peak'], h_pref=h['pref'], h_peak=h['peak'], h_opp=h['opp_ratio'],
                v_pref=v['pref'], v_peak=v['peak'], line_peak=line_peak,
                H1=angular_difference(s['pref'], h['pref']) <= 20,
                H2=(h['peak'] > 0) and (h['opp_ratio'] < 0.25),
                H3=angular_difference(s['pref'], v['pref']) <= 20 and h['peak'] > 0 and v['peak'] >= 0.3 * h['peak'],
                H4=h['peak'] > 0 and h['peak'] > 1.5 * max(line_peak, 0.0))


def largest_gap(preferred_angles):
    """Largest angular gap between neighbouring preferred orientations on the circle."""
    p = sorted(int(a) % 360 for a in preferred_angles)
    if len(p) < 2:
        return 360
    gaps = [p[i + 1] - p[i] for i in range(len(p) - 1)] + [p[0] + 360 - p[-1]]
    return int(max(gaps))
