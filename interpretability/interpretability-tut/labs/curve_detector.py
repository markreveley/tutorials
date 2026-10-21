"""Lab: curve-detector replication, the model-free parts.

Render arc and line stimuli, summarise tuning curves, select candidates on the
screening stimuli, and evaluate the four held-out hypotheses.
Spec and tests: test_curve_detector.py (lessons 06 and 07).
"""

import numpy as np

import math

ANGLES = list(range(0, 360, 10))


def angular_difference(a, b):
    raise NotImplementedError('implement after reading the tests')


def summarise_tuning(curve, angles=ANGLES):
    raise NotImplementedError('implement after reading the tests')


def select_candidates(screen_curves, k, angles=ANGLES):
    """Top-k channels by (clipped peak x selectivity) on the screening tuning curves."""
    raise NotImplementedError('implement after reading the tests')


def evaluate_candidate(screen_curve, held_curve, inverted_curve, line_curve, angles=ANGLES):
    """The four pre-registered held-out hypotheses for one channel."""
    raise NotImplementedError('implement after reading the tests')


def largest_gap(preferred_angles):
    """Largest angular gap between neighbouring preferred orientations on the circle."""
    raise NotImplementedError('implement after reading the tests')


def render_arc(orientation_deg, radius, size=224, thickness=3.0, extent_deg=120.0,
               background=0.5, ink=0.1):
    """Draw a dark arc on a grey field as a float32 array [3, size, size] in [0, 1].
    The arc passes through the image centre; its midpoint tangent is perpendicular
    to the direction `orientation_deg`, and it bulges towards that direction, so
    that orientation theta and theta+180 are the same curve bent the other way."""
    raise NotImplementedError('implement after reading the tests')


def render_line(orientation_deg, size=224, thickness=3.0, background=0.5, ink=0.1):
    """A straight dark line through the centre with the same tangent as the arc's
    midpoint. A line at theta and at theta+180 must be the same image."""
    raise NotImplementedError('implement after reading the tests')


def orientation_selectivity(responses, angles_deg):
    """Vector strength of a 360-degree tuning curve with responses clipped at zero:
    1 when all response sits at one angle, 0 when flat or all zero."""
    raise NotImplementedError('implement after reading the tests')
