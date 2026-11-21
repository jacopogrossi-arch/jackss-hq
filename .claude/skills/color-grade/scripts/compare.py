#!/usr/bin/env python3
"""Self-check: how close is a grade to its references, measured the way a colorist reads scopes.

  python compare.py --ref r1.jpg r2.jpg --images original.jpg graded.jpg
  python compare.py --look the-matrix --images original.jpg graded.jpg

Prints black level / mid / white (L*), color cast per zone (a* = green-/red+, b* = blue-/yellow+),
saturation, and a distance to the reference (lower is closer).
"""
import argparse, json, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import cg_core as cg
from grade import load_looks, find_look

def summary(st):
    p = st["lum_pct"]
    z = st["zones"]
    return {"black": p[1], "mid": p[5], "white": p[9],
            "shadow_ab": z[0]["mean"], "mid_ab": z[1]["mean"], "high_ab": z[2]["mean"],
            "chroma": st["chroma"][0]}

def distance(a, b):
    d = abs(a["black"] - b["black"]) * 0.6 + abs(a["mid"] - b["mid"]) * 0.4 + abs(a["white"] - b["white"]) * 0.4
    for k in ("shadow_ab", "mid_ab", "high_ab"):
        d += float(np.hypot(*(np.array(a[k]) - np.array(b[k]))))
    return round(d + abs(a["chroma"] - b["chroma"]) * 0.5, 1)

def fmt(name, s, ref=None):
    ab = lambda v: f"{v[0]:+5.1f},{v[1]:+5.1f}"
    line = (f"{name[:22]:22s} black {s['black']:5.1f}  mid {s['mid']:5.1f}  white {s['white']:5.1f}  "
            f"shadows {ab(s['shadow_ab'])}  mids {ab(s['mid_ab'])}  highs {ab(s['high_ab'])}  sat {s['chroma']:5.1f}")
    return line + (f"   distance {distance(s, ref)}" if ref else "")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", nargs="+")
    ap.add_argument("--look")
    ap.add_argument("--images", nargs="+", required=True)
    a = ap.parse_args()
    if a.look:
        looks, stats = load_looks()
        ref = summary(stats[find_look(a.look, looks)])
    else:
        ref = summary(cg.analyze([cg.load(p, 1200) for p in a.ref]))
    print(fmt("REFERENCE", ref))
    for p in a.images:
        print(fmt(Path(p).name, summary(cg.analyze([cg.load(p, 1200)])), ref))

if __name__ == "__main__":
    main()
