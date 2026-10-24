#!/usr/bin/env python3
"""grade-looks.py: show every look of the preset on the SAME frame, so a look is chosen with the eyes.

A look is the creative step that comes after the technical ones (LUT, exposure, white balance): how much contrast, how
saturated, which colours lean warm or cold in the shadows and in the highlights. Each look is a short list of numbers in
presets/vacanze-grading/preset.json ("grade" -> "looks"); this script applies them to one frame of a clip and draws a
contact sheet, every tile labelled, plus the original on top for comparison.

A look is a pure colour function (a pixel's new colour depends only on its own colour), so it can later be baked into a 3D LUT
and applied in the same pass as the rest. Hue windows (the sea, the skin) are colour functions too: that is how "a mask" works
here, without drawing anything on the picture.

Usage:
  python3 grade-looks.py --video clip.MP4 --scan DIR/report.json --out sheet.png [--t SECONDS] [--looks a,b,c] [--cols 3] [--tile 640]"""
import argparse, importlib.util, json, os, sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("grade_scan", os.path.join(HERE, "grade-scan.py"))
gs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gs)


def hue_sat(rgb):
    """HSV hue (0-1) and saturation (0-1) of every pixel."""
    mx, mn = rgb.max(axis=-1), rgb.min(axis=-1)
    d = mx - mn
    h = np.zeros_like(mx)
    nz = d > 1e-6
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    h = np.where(nz & (mx == r), ((g - b) / np.maximum(d, 1e-6)) % 6, h)
    h = np.where(nz & (mx == g), (b - r) / np.maximum(d, 1e-6) + 2, h)
    h = np.where(nz & (mx == b), (r - g) / np.maximum(d, 1e-6) + 4, h)
    return (h / 6.0) % 1.0, d / np.maximum(mx, 1e-6)


def window(h, centre, width):
    """1 at `centre`, falling smoothly to 0 at `width` away (circular hue, 0-1)."""
    dist = np.abs((h - centre + 0.5) % 1.0 - 0.5)
    t = np.clip(1 - dist / width, 0, 1)
    return t * t * (3 - 2 * t)


# hue windows (HSV hue, 0-1): orange skin 0.02-0.12, water and sky from green-cyan to blue 0.35-0.65
SEA = (0.50, 0.15)
SKIN = (0.065, 0.075)      # wide and soft: a narrow window turns colour noise into visible blotches on skin


def skin_weight(rgb):
    h, s = hue_sat(rgb)
    y = gs.luma(rgb)
    gate = np.clip((s - 0.06) / 0.22, 0, 1) * np.clip((0.85 - s) / 0.25, 0, 1) * np.clip((y - 0.05) / 0.25, 0, 1)   # smooth ramps, no hard thresholds
    return window(h, *SKIN) * gate


def sea_weight(rgb):
    h, s = hue_sat(rgb)
    y = gs.luma(rgb)
    return window(h, *SEA) * np.clip((s - 0.04) / 0.08, 0, 1) * np.clip((y - 0.10) / 0.10, 0, 1)   # turquoise water is pale: it is only a little coloured


def apply_look(rgb, p):
    x = np.clip(rgb.astype(np.float32), 0, 1)
    if not p:
        return x
    if p.get("gamma", 1.0) != 1.0:
        x = x ** p["gamma"]
    if p.get("crush", 0):
        x = np.clip((x - p["crush"]) / (1 - p["crush"]), 0, 1)
    if p.get("lift", 0):
        x = p["lift"] + x * (1 - p["lift"])
    if p.get("gain", 1.0) != 1.0:
        x = np.clip(x * p["gain"], 0, 1)
    if p.get("temp", 0):
        x = x * np.array([1 + p["temp"], 1, 1 - p["temp"]], np.float32)
    k = p.get("contrast", 0)
    if k:
        x = x * (1 - k) + (x * x * (3 - 2 * x)) * k              # an S curve: darker darks, brighter lights, round shoulders
    y = gs.luma(x)[..., None]
    sat = p.get("sat", 1.0)
    if p.get("vibrance", 0):                                      # push the dull colours more than the strong ones
        c = np.clip(np.abs(x - y).max(axis=-1, keepdims=True) * 2.2, 0, 1)
        sat = sat * (1 + p["vibrance"] * (1 - c))
    x = y + (x - y) * sat
    if p.get("shadows") or p.get("highlights"):
        y = np.clip(gs.luma(x), 0, 1)[..., None]
        if p.get("shadows"):
            x = x + ((1 - y) ** 2) * np.array(p["shadows"], np.float32)
        if p.get("highlights"):
            x = x + (y ** 2) * np.array(p["highlights"], np.float32)
    x = np.clip(x, 0, 1)
    if p.get("sea_sat") or p.get("sea_luma"):                     # a hue window on the blues: deeper, richer water, skin untouched
        w = sea_weight(x)[..., None]
        yy = gs.luma(x)[..., None]
        s2 = 1 + (p.get("sea_sat", 1.0) - 1) * w
        x = yy + (x - yy) * s2
        x = x * (1 + (p.get("sea_luma", 1.0) - 1) * w)
    if p.get("skin_luma") or p.get("skin_sat"):                   # a hue window on skin: lift and warm only the skin
        w = skin_weight(x)[..., None]
        yy = gs.luma(x)[..., None]
        s2 = 1 + (p.get("skin_sat", 1.0) - 1) * w
        x = yy + (x - yy) * s2
        x = x * (1 + (p.get("skin_luma", 1.0) - 1) * w)
    return np.clip(x, 0, 1)


def tile(img, w, label, sub=""):
    h = int(w * img.shape[0] / img.shape[1])
    t = Image.fromarray(gs.to_u8(img)).resize((w, h))
    out = Image.new("RGB", (w, h + 22), (18, 18, 18))
    out.paste(t, (0, 22))
    dr = ImageDraw.Draw(out)
    dr.text((6, 5), label, fill=(255, 255, 255))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--scan", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--t", type=float, help="seconds into the clip (default: the scan's middle sample)")
    ap.add_argument("--looks", help="comma-separated names (default: all)")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--tile", type=int, default=640)
    args = ap.parse_args()
    rep = json.load(open(args.scan, encoding="utf8"))
    prof = rep["profile"]
    looks = gs.CFG.get("looks", {})
    names = args.looks.split(",") if args.looks else list(looks)
    t = args.t if args.t is not None else rep["samples"][len(rep["samples"]) // 2]["t"]
    meta = rep["meta"]
    w = 960
    h = int(round(w * meta["h"] / meta["w"] / 2) * 2)
    f = gs.grab(args.video, t, w, h)
    base = gs.apply_lut(f, gs.load_cube(os.path.join(gs.LUTS, prof["lut"])))
    stops = rep["proposal"]["exposure_stops"]
    base = np.clip(base * (2.0 ** (stops / 2.4)), 0, 1)
    tiles = [tile(f, args.tile, "0 · LOG come girato (piatto: e' normale)")]
    for i, n in enumerate(names, 1):
        if n not in looks:
            print("unknown look", n, "(have: %s)" % ", ".join(looks))
            return 1
        tiles.append(tile(apply_look(base, looks[n]["p"]), args.tile, "%d · %s" % (i, looks[n]["title"])))
    cols = args.cols
    rows = (len(tiles) + cols - 1) // cols
    tw, th = tiles[0].size
    sheet = Image.new("RGB", (tw * cols + 8 * (cols - 1), th * rows + 8 * (rows - 1)), (10, 10, 10))
    for i, tl in enumerate(tiles):
        sheet.paste(tl, ((i % cols) * (tw + 8), (i // cols) * (th + 8)))
    sheet.save(args.out)
    print("%s: %d looks on t=%.1fs (%s, exposure %+.2f stops) -> %s" % (os.path.basename(args.video), len(names), t, prof["label"], stops, args.out))
    for i, n in enumerate(names, 1):
        print("%2d  %-24s %s" % (i, looks[n]["title"], looks[n]["desc"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
