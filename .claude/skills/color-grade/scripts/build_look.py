#!/usr/bin/env python3
"""Save a new reusable look from a set of stills.

  python build_look.py "Blade Runner 2049" still1.jpg still2.jpg ... [--slug blade-runner-2049] [--look "orange haze"]

Only color statistics are stored (no images), so the look can be shared.
Recipe ops and params can be added to looks/looks.json afterwards.
"""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cg_core as cg

ROOT = Path(__file__).resolve().parent.parent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("images", nargs="+")
    ap.add_argument("--slug")
    ap.add_argument("--look", default="")
    ap.add_argument("--weights", nargs="*", type=float, help="optional weight per image")
    a = ap.parse_args()
    slug = a.slug or a.name.lower().replace(" ", "-").replace("'", "").replace(":", "")
    imgs = [cg.load(p, 1600) for p in a.images]
    if a.weights:
        st = cg.merge_stats([cg.analyze([im]) for im in imgs], a.weights)
    else:
        st = cg.analyze(imgs)
    sp, lp = ROOT / "looks" / "stats.json", ROOT / "looks" / "looks.json"
    stats = json.loads(sp.read_text()) if sp.exists() else {}
    looks = json.loads(lp.read_text()) if lp.exists() else {}
    stats[slug] = st
    looks.setdefault(slug, {"name": a.name, "look": a.look, "aliases": [], "params": {}, "ops": []})
    sp.write_text(json.dumps(stats, separators=(",", ":")))
    lp.write_text(json.dumps(looks, indent=1, ensure_ascii=False))
    print(f"saved look '{slug}' from {len(imgs)} stills")

if __name__ == "__main__":
    main()
