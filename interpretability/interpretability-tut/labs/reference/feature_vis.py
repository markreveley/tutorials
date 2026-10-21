"""Feature visualisation by gradient ascent in plain torch (no Lucent).

Run:  python labs/reference/feature_vis.py --unit 177 --out assets/img/fv-3b-177.png
"""
import argparse
import math

import numpy as np
import torch
import torch.nn.functional as F

from vision_common import LAYER, MEAN, STD, load_model


def visualise(model, unit, steps=150, size=128, lr=0.1, seed=0, layer=LAYER, tv_weight=0.02):
    torch.manual_seed(seed)
    module = dict(model.named_modules())[layer]
    store = {}
    handle = module.register_forward_hook(lambda m, i, o: store.__setitem__('out', o))
    # Parameterise in [-inf, inf] and squash with sigmoid so pixels stay in [0, 1].
    param = torch.randn(1, 3, size, size) * 0.5
    param.requires_grad_(True)
    opt = torch.optim.Adam([param], lr=lr)
    history = []
    try:
        for step in range(steps):
            img = torch.sigmoid(param)
            # Transformation robustness: random jitter and small rotation-free scale.
            dx, dy = np.random.randint(-8, 9, size=2)
            jittered = torch.roll(img, shifts=(int(dx), int(dy)), dims=(2, 3))
            up = F.interpolate(jittered, size=(224, 224), mode='bilinear', align_corners=False)
            model((up - MEAN) / STD)
            acts = store['out'][0, unit]
            h, w = acts.shape
            objective = acts[h // 2 - 2:h // 2 + 2, w // 2 - 2:w // 2 + 2].mean()
            # Total-variation penalty keeps high-frequency noise down.
            tv = (img[:, :, 1:, :] - img[:, :, :-1, :]).abs().mean() + (img[:, :, :, 1:] - img[:, :, :, :-1]).abs().mean()
            loss = -objective + tv_weight * tv
            opt.zero_grad(); loss.backward(); opt.step()
            history.append(float(objective.detach()))
    finally:
        handle.remove()
    return torch.sigmoid(param).detach()[0], history


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', type=int, default=177)
    ap.add_argument('--steps', type=int, default=150)
    ap.add_argument('--out', default='')
    args = ap.parse_args()
    np.random.seed(0)
    model = load_model()
    img, hist = visualise(model, args.unit, steps=args.steps)
    print(f'unit {LAYER}:{args.unit}: centre objective step 0 = {hist[0]:.2f}, '
          f'step {len(hist)//2} = {hist[len(hist)//2]:.2f}, final = {hist[-1]:.2f}')
    if args.out:
        from PIL import Image
        arr = (img.permute(1, 2, 0).numpy() * 255).round().astype(np.uint8)
        Image.fromarray(arr).save(args.out)
        print(f'wrote {args.out} ({arr.shape[1]}x{arr.shape[0]})')


if __name__ == '__main__':
    main()
