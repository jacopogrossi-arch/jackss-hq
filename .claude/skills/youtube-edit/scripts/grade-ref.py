#!/usr/bin/env python3
"""grade-ref.py: start a look from frames Jacopo likes (reference matching, 27/10/2026).

The lesson of 27/10: copying a creator's before/after transform as a LUT does NOT work on Jacopo's clips (their "before" is
another camera's log: purple highlights, dark skin). What works is measuring the FINISHED reference picture and moving our
look until our clip has the same traits. This script measures, on the reference frames and on our clip graded with a base
film look, five things that do not depend on what is in the scene:

  - the tint of the highlights (brightest 15 %) and of the shadows (darkest 20 %): warm / teal split tone;
  - the black level (1st percentile): deep or lifted blacks;
  - the spread between blacks and highlights: contrast;
  - how coloured the picture is (mean chroma): saturation.

Tints are measured only on pixels that are not coloured by the scene itself (chroma under 0.15, sea and sky hues out): the
first test read the lagoon's turquoise water as "teal shadows" and pushed the shadows red. Blacks and contrast are copied only
when our clip has real darks (1st percentile under 12 %): a bright lagoon has no blacks to deepen. Saturation moves at most
+-10 %, since how coloured a picture is depends on the scene.

It moves the base look's "film" numbers part of the way (60 %) towards the reference, inside safe limits, and writes:
  look.json      the new look, ready to paste into presets/vacanze-grading/preset.json (or --save NAME does it)
  ref-sheet.png  the references on top; below, our clip with the base look, with the new look at 50 % and at 100 %.
Exposure is NOT copied: how bright a picture is depends on the scene, and the exposure step owns it.

Usage:
  python3 grade-ref.py --ref inspo.mp4@5.5 --ref still.png [...] --video clip.MP4 --scan DIR/report.json --out DIR
                       [--base pellicola-oro] [--save ref-hawaii]"""
import argparse, copy, importlib.util, json, os, sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("grade_film", os.path.join(HERE, "grade-film.py"))
gf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gf)
gs = gf.gs

PULL = 0.6                  # how far towards the reference: all the way copies its scene along with its grade
CROP = (0.13, 0.82, 0.03, 0.97)   # rows / columns kept: social videos carry logos and captions on the edges
PRESET = os.path.join(os.path.dirname(HERE), "presets", "vacanze-grading", "preset.json")


def load_ref(spec_):
    if "@" in spec_ and not os.path.exists(spec_):
        path, t = spec_.rsplit("@", 1)
        import subprocess, tempfile
        tmp = os.path.join(tempfile.mkdtemp(prefix="grade-ref-"), "f.png")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", t, "-i", path, "-frames:v", "1", "-vf", "scale=960:-2", tmp], check=True)
        spec_ = tmp
    a = np.asarray(Image.open(spec_).convert("RGB")).astype(np.float32) / 255.0
    h, w, _ = a.shape
    return a[int(h * CROP[0]):int(h * CROP[1]), int(w * CROP[2]):int(w * CROP[3])]


def traits(frames):
    x = np.concatenate([f.reshape(-1, 3) for f in frames])
    y = gs.luma(x)
    c = x.max(axis=1) - x.min(axis=1)
    calm = (c < 0.15) & (gf.gl.sea_weight(x[:, None, :])[:, 0] < 0.1)      # not coloured by the scene: walls, sand, clouds, skin in shade
    yc = y[calm] if calm.sum() > 500 else y
    xc = x[calm] if calm.sum() > 500 else x
    sh, hi = yc < np.percentile(yc, 20), yc > np.percentile(yc, 85)
    return {"hl_tint": (xc[hi].mean(0) - xc[hi].mean()).tolist(), "sh_tint": (xc[sh].mean(0) - xc[sh].mean()).tolist(),
            "calm": float(calm.mean()),
            "black": float(np.percentile(y, 1)), "spread": float(np.percentile(y, 99) - np.percentile(y, 1)),
            "chroma": float(c.mean())}


def derive(base, ref, ours):
    """The base look moved PULL of the way towards the reference's traits, inside limits."""
    look = copy.deepcopy(base)
    f = look.setdefault("film", {})
    d = dict(gf.FILM)
    d.update(f)
    warm = d["warm"] or [[0, 0, 0], [0, 0, 0]]
    hl = [float(np.clip(warm[0][i] + PULL * (ref["hl_tint"][i] - ours["hl_tint"][i]), -0.05, 0.05)) for i in range(3)]
    sh = [float(np.clip(warm[1][i] + PULL * (ref["sh_tint"][i] - ours["sh_tint"][i]), -0.03, 0.03)) for i in range(3)]
    f["warm"] = [[round(v, 4) for v in hl], [round(v, 4) for v in sh]]
    if ours["black"] < 0.12:                                          # only a clip with real darks can copy blacks and contrast
        f["contrast"] = round(float(np.clip(d["contrast"] * (ref["spread"] / max(ours["spread"], 1e-3)) ** (0.5 * PULL), d["contrast"] * 0.92, d["contrast"] * 1.08)), 3)
        lin_gap = ref["black"] ** 2.4 - ours["black"] ** 2.4           # deeper blacks in the reference -> a stronger toe
        f["black"] = round(float(np.clip(d["black"] - PULL * lin_gap * 2, 0.0, 0.02)), 4)
    k = float(np.clip((ref["chroma"] / max(ours["chroma"], 1e-3)) ** PULL, 0.9, 1.1))
    look["sat"] = round(look.get("sat", 1.0) * k, 3)
    return look


def mix(base, new, a):
    """A look a of the way from base to new (numbers only), for the 50 % tile."""
    out = copy.deepcopy(new)
    bf, nf = gf.film_params(base), gf.film_params(new)
    for key in ("contrast", "black"):
        out["film"][key] = bf[key] + (nf[key] - bf[key]) * a
    bw, nw = np.array(bf["warm"] or [[0] * 3, [0] * 3]), np.array(nf["warm"])
    out["film"]["warm"] = (bw + (nw - bw) * a).tolist()
    out["sat"] = base.get("sat", 1.0) + (new.get("sat", 1.0) - base.get("sat", 1.0)) * a
    return out


def tile(img, w, label):
    h = int(w * img.shape[0] / img.shape[1])
    t = Image.new("RGB", (w, h + 22), (16, 16, 16))
    t.paste(Image.fromarray(gs.to_u8(img)).resize((w, h)), (0, 22))
    ImageDraw.Draw(t).text((6, 5), label, fill=(255, 255, 255))
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", action="append", required=True, help="a reference: an image, or VIDEO@SECONDS; several are averaged")
    ap.add_argument("--video", required=True)
    ap.add_argument("--scan", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--base", default="pellicola-oro", help="the film look to start from")
    ap.add_argument("--save", help="also add the new look to the preset under this name")
    args = ap.parse_args()
    looks = gs.CFG["looks"]
    base = looks[args.base]["p"]
    if not gf.is_film(base):
        print("--base must be a film look (one with a 'film' key), e.g. pellicola-oro")
        return 1
    refs = [load_ref(r) for r in args.ref]
    rep = json.load(open(args.scan, encoding="utf8"))
    meta = rep["meta"]
    w = gs.W_STATS
    h = int(round(w * meta["h"] / meta["w"] / 2) * 2)
    lut = gs.load_cube(os.path.join(gs.LUTS, rep["profile"]["lut"]))
    stops = rep["proposal"]["exposure_stops"]
    s = rep["samples"]
    frames = [gs.apply_lut(gs.grab(args.video, s[int(round(i * (len(s) - 1) / 3))]["t"], w, h), lut) for i in range(4)]
    white = gf.measure_white(frames)
    ours_frames = [gf.apply(f, base, stops, None, white) for f in frames]
    rt, ot = traits(refs), traits(ours_frames)
    new = derive(base, rt, ot)
    half = mix(base, new, 0.5)
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "look.json"), "w", encoding="utf8") as fh:
        json.dump({"title": "Da riferimento", "desc": "Ricavato da grade-ref.py: " + ", ".join(os.path.basename(r) for r in args.ref), "p": new}, fh, indent=2, ensure_ascii=False)
    tw = 480
    top = [tile(r, tw, "RIFERIMENTO %d" % (i + 1)) for i, r in enumerate(refs[:4])]
    mid = frames[len(frames) // 2]
    bottom = [tile(gf.finish_image(gf.apply(mid, lk, stops, None, white), lk), tw, lab)
              for lk, lab in ((base, "TUA CLIP: %s" % args.base), (half, "nuovo look al 50 %"), (new, "nuovo look al 100 %"))]
    th = max(t.height for t in top + bottom)
    cols = max(len(top), len(bottom))
    sheet = Image.new("RGB", (cols * (tw + 8), th * 2 + 8), (0, 0, 0))
    for i, t in enumerate(top):
        sheet.paste(t, (i * (tw + 8), 0))
    for i, t in enumerate(bottom):
        sheet.paste(t, (i * (tw + 8), th + 8))
    sheet.save(os.path.join(args.out, "ref-sheet.png"))

    def fmt(t):
        return "luci %s | ombre %s | nero %.0f | spread %.0f | colore %.0f" % (
            "/".join("%+.0f" % (v * 255) for v in t["hl_tint"]), "/".join("%+.0f" % (v * 255) for v in t["sh_tint"]), t["black"] * 255, t["spread"] * 255, t["chroma"] * 255)
    print("riferimento: " + fmt(rt))
    print("tua clip    : " + fmt(ot))
    print("nuovo look  : film %s, sat %.3f" % (json.dumps({k: new["film"][k] for k in ("contrast", "black", "warm")}), new.get("sat", 1.0)))
    if args.save:
        preset = json.load(open(PRESET, encoding="utf8"))
        preset["grade"]["looks"][args.save] = {"title": "Da riferimento: %s" % args.save, "desc": "Ricavato da grade-ref.py il giorno del salvataggio, base %s, riferimenti: %s." % (args.base, ", ".join(os.path.basename(r) for r in args.ref)), "p": new}
        with open(PRESET, "w", encoding="utf8") as fh:
            json.dump(preset, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        print("saved as look %r in the preset" % args.save)
    print("-> %s, %s" % (os.path.join(args.out, "look.json"), os.path.join(args.out, "ref-sheet.png")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
