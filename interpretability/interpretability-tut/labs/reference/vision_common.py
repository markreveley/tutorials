"""Shared helpers for the InceptionV1 (torchvision GoogLeNet) experiments.

Reference implementation used to produce the verified transcript. Learners
implement the same ideas in labs/curve_detector.py.
"""
import math

import numpy as np
import torch
from torchvision.models import GoogLeNet_Weights, googlenet

MEAN = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
STD = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)
# The ten mixed3b curve detectors named in Cammarata et al. (2020), "Curve
# Detectors", Distill; torchvision calls the layer inception3b.
CURVE_UNITS = [379, 406, 385, 343, 342, 388, 324, 340, 330, 349]
LAYER = 'inception3b'


def load_model():
    torch.manual_seed(0)
    model = googlenet(weights=GoogLeNet_Weights.IMAGENET1K_V1).eval()
    for p in model.parameters():
        p.requires_grad_(False)
    return model


def layer_output(model, images, layer=LAYER):
    """Return the post-ReLU output of a named layer for a batch of [0,1] images."""
    store = {}
    module = dict(model.named_modules())[layer]
    handle = module.register_forward_hook(lambda m, i, o: store.__setitem__('out', o))
    try:
        model((images - MEAN) / STD)
    finally:
        handle.remove()
    return store['out']


def render_arc(orientation_deg, radius, size=224, thickness=3.0, extent_deg=120.0,
               background=0.5, ink=0.1):
    """Draw a dark arc on a grey field. The arc's midpoint lies in direction
    `orientation_deg` from the image centre; the arc bulges away from the centre
    so that its tangent at the midpoint is perpendicular to that direction.
    Returns a float32 array [3, size, size] in [0, 1]."""
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    cx = cy = (size - 1) / 2.0
    theta = math.radians(orientation_deg)
    # Arc centre sits on the opposite side so the arc passes through the image centre.
    acx = cx - radius * math.cos(theta)
    acy = cy - radius * math.sin(theta)
    dist = np.sqrt((xx - acx) ** 2 + (yy - acy) ** 2)
    ang = np.degrees(np.arctan2(yy - acy, xx - acx))
    diff = (ang - orientation_deg + 180.0) % 360.0 - 180.0
    on_arc = (np.abs(dist - radius) <= thickness / 2.0) & (np.abs(diff) <= extent_deg / 2.0)
    soft = np.clip(1.0 - (np.abs(dist - radius) - thickness / 2.0), 0.0, 1.0)
    mask = np.where(np.abs(diff) <= extent_deg / 2.0, soft, 0.0)
    mask = np.maximum(mask, on_arc.astype(np.float32))
    img = background + (ink - background) * mask
    return np.repeat(img[None].astype(np.float32), 3, axis=0)


def centre_response(acts, k=2):
    """Average activation over the central k x k block of a [B, C, H, W] map."""
    h, w = acts.shape[-2:]
    r0, c0 = h // 2 - k // 2, w // 2 - k // 2
    return acts[..., r0:r0 + k, c0:c0 + k].mean(dim=(-1, -2))


def orientation_selectivity(responses, angles_deg):
    """Vector-strength selectivity on a 360-degree tuning curve: 1 means all
    response at one angle, 0 means flat. Responses are clipped at zero."""
    r = np.clip(np.asarray(responses, dtype=np.float64), 0, None)
    if r.sum() <= 0:
        return 0.0
    ang = np.radians(np.asarray(angles_deg, dtype=np.float64))
    return float(abs((r * np.exp(1j * ang)).sum()) / r.sum())


def render_line(orientation_deg, size=224, thickness=3.0, background=0.5, ink=0.1):
    """A straight dark line through the centre whose tangent matches the tangent
    of `render_arc(orientation_deg, ...)` at the arc midpoint (perpendicular to the
    orientation direction). A line is the same stimulus at theta and theta+180."""
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    c = (size - 1) / 2.0
    theta = math.radians(orientation_deg)
    # signed distance from the line with normal (cos theta, sin theta) through the centre
    dist = np.abs((xx - c) * math.cos(theta) + (yy - c) * math.sin(theta))
    mask = np.clip(1.0 - (dist - thickness / 2.0), 0.0, 1.0)
    img = background + (ink - background) * mask
    return np.repeat(img[None].astype(np.float32), 3, axis=0)
