"""Two-stage, pre-registered test for curve detectors in torchvision GoogLeNet's
inception3b (the layer the Distill "Curve Detectors" article calls mixed3b).

Stage 1 (screening, "train" stimuli): show thin dark arcs at 36 orientations and
two radii; rank the 480 channels by (peak response x orientation selectivity);
keep the top K as candidates. Looking at this stage is allowed; it chooses the
hypothesis.

Stage 2 (held-out stimuli): BEFORE rendering them, we commit to the predictions
below for the candidates on stimuli the screening never saw: new radii and
thickness, inverted contrast (light arc on dark field), and straight lines.

Run:  python labs/reference/curve_tuning.py [--top 12] [--random 100]
      python labs/reference/curve_tuning.py --units 379,406,385,343,342,388,324,340,330,349
      (the second form tests the Distill unit numbers directly; see lesson 06 for why
      they are not expected to transfer to torchvision's weights)
"""
import argparse

import numpy as np
import torch

from sol_curve_detector import (angular_difference, evaluate_candidate, largest_gap,
                                select_candidates, summarise_tuning)
from vision_common import (CURVE_UNITS, centre_response, layer_output, load_model,
                           orientation_selectivity, render_arc, render_line)

ANGLES = list(range(0, 360, 10))
SCREEN = dict(radii=[25, 45], thickness=3.0, extent=120.0, ink=0.1, background=0.5)
HELDOUT = dict(radii=[35, 60], thickness=5.0, extent=150.0, ink=0.1, background=0.5)
INVERTED = dict(radii=[35, 60], thickness=5.0, extent=150.0, ink=0.9, background=0.5)

PREREGISTRATION = {
    'claim': 'inception3b of torchvision GoogLeNet contains a family of orientation-selective '
             'curve detectors: channels that respond to a curve of one orientation, are nearly '
             'silent at the opposite orientation, keep their preference under cosmetic changes, '
             'and prefer a curve to a straight line of the same tangent.',
    'selection': 'top K channels by peak x selectivity on the screening stimuli (K fixed before running)',
    'H1 (held-out radius/thickness)': 'preferred orientation on held-out arcs within 20 degrees of the '
             'screening preference, for at least 80% of candidates',
    'H2 (opposite orientation)': 'held-out response at preferred+180 degrees < 0.25 x peak, for at least '
             '80% of candidates',
    'H3 (contrast inversion)': 'on light-on-dark arcs the preferred orientation stays within 20 degrees '
             'and the peak is at least 0.3 x the dark-arc peak, for at least 60% of candidates',
    'H4 (curve, not line)': 'held-out arc peak > 1.5 x the peak response to a straight line of the same '
             'tangent orientation and thickness, for at least 80% of candidates',
    'H5 (family spans orientations)': 'the candidates\' preferred orientations leave no gap larger than '
             '90 degrees around the circle',
    'controls': '100 random non-candidate channels run through the same held-out tests; their pass rates '
             'are reported beside the candidates\'. The blank-field response is subtracted everywhere.',
    'what_failure_means': 'a hypothesis that fails is reported as failed; the candidates are then '
             'orientation-selective arc responders, not demonstrated curve detectors.',
}


def responses(model, stims, base):
    """[n_stimuli, 480] baseline-subtracted centre responses."""
    out = []
    for i in range(0, len(stims), 12):
        batch = torch.from_numpy(np.stack(stims[i:i + 12]))
        out.append((centre_response(layer_output(model, batch)) - base).numpy())
    return np.concatenate(out)


def arc_curves(model, base, spec):
    """Tuning curves [480, 36]: max over radii of the response to arcs."""
    stims = [render_arc(a, r, thickness=spec['thickness'], extent_deg=spec['extent'],
                        ink=spec['ink'], background=spec['background'])
             for a in ANGLES for r in spec['radii']]
    resp = responses(model, stims, base).reshape(len(ANGLES), len(spec['radii']), 480)
    return resp.max(axis=1).T


def line_curves(model, base, spec):
    stims = [render_line(a, thickness=spec['thickness'], ink=spec['ink'], background=spec['background'])
             for a in ANGLES]
    return responses(model, stims, base).T


def evaluate(ch, screen, held, inv, lines):
    return dict(ch=ch, **evaluate_candidate(screen[ch], held[ch], inv[ch], lines[ch]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--top', type=int, default=12)
    ap.add_argument('--random', type=int, default=100)
    ap.add_argument('--units', default='', help='comma-separated channels to test instead of screening')
    args = ap.parse_args()
    print('PRE-REGISTRATION (fixed before the held-out stimuli were rendered):')
    for k, v in PREREGISTRATION.items():
        print(f'  {k}: {v}')
    model = load_model()
    base = centre_response(layer_output(model, torch.full((1, 3, 224, 224), 0.5)))[0]
    screen = arc_curves(model, base, SCREEN)
    peak = screen.max(axis=1)
    sel = np.array([orientation_selectivity(c, ANGLES) for c in screen])
    if args.units:
        cands = [int(u) for u in args.units.split(',')]
        print(f'\nSTAGE 1 skipped: testing the named units {cands}')
    else:
        cands = select_candidates(screen, args.top)
        print(f'\nSTAGE 1 (screening on {len(ANGLES)}x{len(SCREEN["radii"])} dark arcs): '
              f'median channel peak {np.median(peak):.2f}, selectivity median {np.median(sel):.2f}')
        print(f'  top {args.top} channels by peak x selectivity: {cands}')
    rng = np.random.default_rng(0)
    pool = [c for c in range(480) if c not in cands]
    randoms = sorted(rng.choice(pool, size=args.random, replace=False).tolist())
    held = arc_curves(model, base, HELDOUT)
    inv = arc_curves(model, base, INVERTED)
    lines = line_curves(model, base, HELDOUT)
    print('\nSTAGE 2 (held-out stimuli):')
    print(f'{"ch":>4} {"scr":>4} {"held":>4} {"peak":>6} {"opp":>5} {"inv":>4} {"ipk":>6} {"line":>6}  H1 H2 H3 H4')
    rows = [evaluate(c, screen, held, inv, lines) for c in cands]
    for r in rows:
        print(f'{r["ch"]:>4} {r["s_pref"]:>4} {r["h_pref"]:>4} {r["h_peak"]:>6.2f} {r["h_opp"]:>5.2f} '
              f'{r["v_pref"]:>4} {r["v_peak"]:>6.2f} {r["line_peak"]:>6.2f}  '
              + ' '.join(' y' if r[h] else ' -' for h in ('H1', 'H2', 'H3', 'H4')))
    ctrl = [evaluate(c, screen, held, inv, lines) for c in randoms]
    print()
    for h, need in (('H1', .8), ('H2', .8), ('H3', .6), ('H4', .8)):
        rate = np.mean([r[h] for r in rows]); crate = np.mean([r[h] for r in ctrl])
        print(f'{h}: candidates {rate:.0%} (need >= {need:.0%}) -> {"pass" if rate >= need else "FAIL"}; '
              f'random-channel control {crate:.0%}')
    all4 = np.mean([all(r[h] for h in ('H1', 'H2', 'H3', 'H4')) for r in rows])
    call4 = np.mean([all(r[h] for h in ('H1', 'H2', 'H3', 'H4')) for r in ctrl])
    print(f'H1-H4 jointly: candidates {all4:.0%}; random-channel control {call4:.0%}')
    prefs = sorted(r['h_pref'] for r in rows)
    gap = largest_gap(prefs)
    print(f'H5: held-out preferred orientations {prefs}; largest gap {gap} degrees -> '
          f'{"pass" if gap <= 90 else "FAIL"}')


if __name__ == '__main__':
    main()
