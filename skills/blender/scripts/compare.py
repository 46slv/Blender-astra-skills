"""Paired inspection for ALREADY registered images; Pillow + NumPy on host Python.

python compare.py reference.png model.png --out inspection.png
  [--region left top right bottom] [--alpha-masks]
Region is normalized and applied equally; no independent auto-cropping or fitting.
Alpha masks are opt-in and rejected for opaque images. IDs/edges are not semantics.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw


def compare(reference, model, out, region=(0,0,1,1), alpha_masks=False):
    a, b = Image.open(reference).convert('RGBA'), Image.open(model).convert('RGBA')
    if a.size != b.size:
        raise ValueError('Register images on the same canvas first; size mismatch is not shape error.')
    if not (0 <= region[0] < region[2] <= 1 and 0 <= region[1] < region[3] <= 1):
        raise ValueError('Region must be normalized left, top, right, bottom')
    box = tuple(round(v * a.size[i % 2]) for i, v in enumerate(region))
    a, b = a.crop(box), b.crop(box)
    bg = Image.new('RGBA', a.size, '#24282d')
    ar, br = Image.alpha_composite(bg, a).convert('RGB'), Image.alpha_composite(bg, b).convert('RGB')
    overlay = Image.blend(ar, br, .5)
    report = {'region':list(region), 'crop_pixels':list(box),
              'meaning':'Paired visual evidence; RGB differences also contain lighting/material/camera error.'}
    panels = [('Reference', ar), ('Model', br), ('50% overlay',overlay)]
    if alpha_masks:
        aa, bb = np.asarray(a)[:,:,3], np.asarray(b)[:,:,3]
        if aa.min() == 255 or bb.min() == 255:
            raise ValueError('Opaque crop has no usable alpha silhouette; supply transparent renders/masks.')
        am, bm = aa >= 128, bb >= 128
        union = np.logical_or(am,bm).sum()
        if not union:
            raise ValueError('Both masks empty')
        report['silhouette_iou'] = float(np.logical_and(am,bm).sum()/union)
        diff = np.zeros((*am.shape,3),dtype=np.uint8)
        diff[am & bm], diff[am & ~bm], diff[bm & ~am] = (180,180,180),(250,70,95),(40,190,250)
        panels.append(('Red: reference only / blue: model only',Image.fromarray(diff)))
    width, height = a.size
    # Limit panels for comfortable inspection, retaining the exact crop in report.
    scale = min(1, 540/width, 720/height)
    w, h = max(1,round(width*scale)), max(1,round(height*scale))
    canvas = Image.new('RGB',(w*len(panels),h+34),'#15191e')
    draw = ImageDraw.Draw(canvas)
    for i,(label,panel) in enumerate(panels):
        draw.text((i*w+8,10),label,fill='white')
        canvas.paste(panel.resize((w,h),Image.Resampling.LANCZOS),(i*w,34))
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)
    out.with_suffix('.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('reference')
    p.add_argument('model')
    p.add_argument('--out',required=True)
    p.add_argument('--region',nargs=4,type=float,default=(0,0,1,1))
    p.add_argument('--alpha-masks',action='store_true')
    a = p.parse_args()
    print(json.dumps(compare(a.reference,a.model,a.out,a.region,a.alpha_masks),indent=2))
