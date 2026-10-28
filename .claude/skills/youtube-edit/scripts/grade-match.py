#!/usr/bin/env python3
"""grade-match.py: make the clips of ONE video look shot in the same world, before the look (shot matching, 27/10/2026).

Each clip is graded on its own by grade-scan + grade-apply; cut together they can still jump: one face brighter, one beach
bluer. A colourist balances the shots against each other first, then puts the look on top. This script does that step:

  - it reads the scan report of every clip, grabs 6 frames each and applies the DJI LUT and the scan's exposure;
  - EXPOSURE: the anchor is the skin when at least two clips show skin (else the median). Every clip is moved so its anchor
    moves half-way towards the set's median anchor, never more than +-0.3 stop away from its own proposal and never outside the band
    of the preset: a night clip stays darker than a beach clip, it just stops jumping;
  - COLOUR: the cast of each clip is measured on its near-neutral mid-tones (walls, clouds, shirts: chroma under 0.03, the
    sea and sky hues excluded: pale turquoise water is not a cast) and the clip moves half-way towards the set's median
    cast, at most +-3 % per channel. Towards the set, not towards neutral:
    a warm trip stays warm. A clip with too few near-neutral pixels (under 2 %) is left alone and the report says so;
  - it writes match.json (per clip: stops, white-balance gains, why) and match-sheet.png: every clip before / after, with
    the look, side by side. grade-apply.py --match match.json then uses these numbers.

Usage:
  python3 grade-match.py --clip clipA.MP4=scanA/report.json --clip clipB.MP4=scanB/report.json [...] --out DIR [--look pellicola-oro]"""
import argparse, importlib.util, json, os, sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("grade_film", os.path.join(HERE, "grade-film.py"))
gf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gf)
gs, gl = gf.gs, gf.gl

MAX_MOVE = 0.3          # stops away from the clip's own proposal
MAX_CAST = 0.03         # white-balance gain, per channel
DAMP = 0.5              # cover half the gap: balance the shots, do not flatten them (first test: full matching dulled the lagoon, greyed a warm wall)
NEUTRAL_CHROMA = 0.03
MIN_NEUTRAL = 0.02
N_FRAMES = 6


def cast(rgb):
    """Mean (Cb, Cr) of the near-neutral mid-tones, and the fraction of the picture they cover."""
    y = gs.luma(rgb)
    cb = (rgb[..., 2] - y) / 1.8556
    cr = (rgb[..., 0] - y) / 1.5748
    m = (y > 0.3) & (y < 0.88) & (np.hypot(cb, cr) < NEUTRAL_CHROMA) & (gl.sea_weight(rgb) < 0.1)
    if m.mean() < MIN_NEUTRAL:
        return None, float(m.mean()), None
    return (float(cb[m].mean()), float(cr[m].mean())), float(m.mean()), float(y[m].mean())


def grade(rgb, stops, wb, look, white):
    if gf.is_film(look):
        return gf.apply(rgb, look, stops, wb, white)
    g = 2.0 ** (stops / 2.4)
    out = np.clip(rgb * np.array([g * (wb[0] if wb else 1), g, g * (wb[1] if wb else 1)], np.float32), 0, 1)
    return gl.apply_look(out, look) if look else out


def measure(video, scan):
    rep = json.load(open(scan, encoding="utf8"))
    meta = rep["meta"]
    w = gs.W_STATS
    h = int(round(w * meta["h"] / meta["w"] / 2) * 2)
    lut = gs.load_cube(os.path.join(gs.LUTS, rep["profile"]["lut"]))
    s = rep["samples"]
    pick = [s[int(round(i * (len(s) - 1) / (N_FRAMES - 1)))]["t"] for i in range(N_FRAMES)] if len(s) >= N_FRAMES else [x["t"] for x in s]
    frames = [gs.apply_lut(gs.grab(video, t, w, h), lut) for t in pick]
    stops = rep["proposal"]["exposure_stops"]
    g = 2.0 ** (stops / 2.4)
    exposed = [np.clip(f * g, 0, 1) for f in frames]
    st = [gs.frame_stats(f) for f in exposed]
    skin = [x["skin_luma"] for x in st if x["skin_luma"] is not None and x["skin_frac"] >= 0.01]
    casts = [cast(f) for f in exposed]
    good = [c for c in casts if c[0] is not None]
    return {"video": video, "scan": scan, "name": os.path.basename(video), "stops": stops, "frames": frames,
            "skin": float(np.median(skin)) if skin else None, "median": float(np.median([x["median"] for x in st])),
            "cast": (float(np.mean([c[0][0] for c in good])), float(np.mean([c[0][1] for c in good]))) if good else None,
            "neutral_y": float(np.mean([c[2] for c in good])) if good else None,
            "neutral_frac": float(np.mean([c[1] for c in casts])), "white": gf.measure_white(frames)}


def tile(img, w, label):
    h = int(w * img.shape[0] / img.shape[1])
    t = Image.new("RGB", (w, h + 22), (16, 16, 16))
    t.paste(Image.fromarray(gs.to_u8(img)).resize((w, h)), (0, 22))
    ImageDraw.Draw(t).text((6, 5), label, fill=(255, 255, 255))
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", action="append", required=True, help="VIDEO=SCAN_REPORT, once per clip (at least two)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--look", default=gs.CFG.get("default_look"), help="look for the sheet (the match itself does not depend on it)")
    args = ap.parse_args()
    if len(args.clip) < 2:
        print("Matching needs at least two clips.")
        return 1
    look = gs.CFG["looks"][args.look]["p"] if args.look else None
    clips = []
    for c in args.clip:
        video, scan = c.split("=", 1)
        clips.append(measure(video, scan))
        print("measured %s" % clips[-1]["name"])

    with_skin = [c for c in clips if c["skin"] is not None]
    anchor = "skin" if len(with_skin) >= 2 else "median"
    lo, hi = gs.CFG["skin_band"] if anchor == "skin" else gs.CFG["median_band"]
    target = float(np.clip(np.median([c[anchor] for c in clips if c[anchor] is not None]), lo, hi))
    casts = [c["cast"] for c in clips if c["cast"] is not None]
    cast_t = (float(np.median([x[0] for x in casts])), float(np.median([x[1] for x in casts]))) if len(casts) >= 2 else None

    # clips with the same file name (e.g. every shot cut to its own folder as log.mov) are keyed by their full path:
    # keyed by name they overwrote each other and every clip got the last clip's exposure (Zanzibar reel, 28/10/2026)
    names = [c["name"] for c in clips]
    key = lambda c: os.path.abspath(c["video"]) if names.count(c["name"]) > 1 else c["name"]
    out, rows = {}, []
    for c in clips:
        why = []
        val = c[anchor]
        if val is None:
            stops = c["stops"]
            why.append("no %s in this clip: exposure left at the scan's proposal" % anchor)
        else:
            move = round(float(np.clip(DAMP * 2.4 * np.log2(target / max(val, 1e-4)), -MAX_MOVE, MAX_MOVE)), 2)
            stops = round(c["stops"] + move, 2)
            why.append("%s %.0f IRE -> set target %.0f IRE: %+.2f stops on top of the proposal (%+.2f)" % (anchor, val * 100, target * 100, move, c["stops"]))
        wb = None
        if cast_t and c["cast"] is not None:
            dcb, dcr = DAMP * (cast_t[0] - c["cast"][0]), DAMP * (cast_t[1] - c["cast"][1])
            yn = max(c["neutral_y"], 0.2)
            gr = float(np.clip(1 + dcr * 1.5748 / yn, 1 - MAX_CAST, 1 + MAX_CAST))
            gb = float(np.clip(1 + dcb * 1.8556 / yn, 1 - MAX_CAST, 1 + MAX_CAST))
            if max(abs(gr - 1), abs(gb - 1)) >= 0.005:
                wb = [round(gr, 3), round(gb, 3)]
                why.append("colour moved towards the set: R x%.3f, B x%.3f (neutral areas %.0f %% of the picture)" % (gr, gb, c["neutral_frac"] * 100))
            else:
                why.append("colour already in line with the set")
        else:
            why.append("colour left alone: too few near-neutral areas (%.1f %%)" % (c["neutral_frac"] * 100) if c["cast"] is None else "colour left alone: only one clip to compare")
        out[key(c)] = {"video": c["video"], "scan": c["scan"], "stops": stops, "wb_gains": wb, "why": why}
        mid = c["frames"][len(c["frames"]) // 2]
        rows.append([tile(grade(mid, c["stops"], None, look, c["white"]), 480, "%s  PRIMA" % c["name"][:34]),
                     tile(grade(mid, stops, wb, look, c["white"]), 480, "%s  DOPO il match" % c["name"][:30])])
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "match.json"), "w", encoding="utf8") as fh:
        json.dump({"anchor": anchor, "target": target, "cast_target": cast_t, "look_for_sheet": args.look, "clips": out}, fh, indent=1, ensure_ascii=False)
    tw, th = rows[0][0].size
    sheet = Image.new("RGB", (tw * 2 + 8, (th + 8) * len(rows)), (0, 0, 0))
    for r, (a, b) in enumerate(rows):
        sheet.paste(a, (0, r * (th + 8)))
        sheet.paste(b, (tw + 8, r * (th + 8)))
    sheet.save(os.path.join(args.out, "match-sheet.png"))
    print("anchor: %s, target %.0f IRE%s" % (anchor, target * 100, (", colour target Cb %.3f Cr %.3f" % cast_t) if cast_t else ""))
    for n, v in out.items():
        print("- %s: %+.2f stops, WB %s\n    %s" % (n, v["stops"], v["wb_gains"] or "untouched", "\n    ".join(v["why"])))
    print("-> %s and match-sheet.png. Then: grade-apply.py ... --match %s" % (os.path.join(args.out, "match.json"), os.path.join(args.out, "match.json")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
