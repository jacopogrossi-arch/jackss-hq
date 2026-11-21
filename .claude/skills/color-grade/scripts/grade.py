#!/usr/bin/env python3
"""Grade an image from reference images and/or a named movie look.

  python grade.py IMAGE --ref ref1.jpg ref2.jpg            # match references
  python grade.py IMAGE --look the-matrix                  # built-in look
  python grade.py IMAGE --look drive --ref still.jpg       # built-in look + extra references
  python grade.py IMAGE --ref r.jpg --set tone=0.8 --set skin=0.7 --add-op '{"op":"grain","amount":0.03}'
  python grade.py IMAGE --look her --lut her.cube          # also export the per-pixel grade as a LUT
  python grade.py --list                                   # list built-in looks
"""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cg_core as cg

ROOT = Path(__file__).resolve().parent.parent
LOOKS = ROOT / "looks" / "looks.json"
STATS = ROOT / "looks" / "stats.json"

def load_looks():
    looks = json.loads(LOOKS.read_text())
    stats = json.loads(STATS.read_text()) if STATS.exists() else {}
    return looks, stats

def find_look(name, looks):
    key = name.lower().strip().replace(" ", "-").replace("'", "")
    if key in looks:
        return key
    for k, v in looks.items():
        if key in [a.lower().replace(" ", "-").replace("'", "") for a in v.get("aliases", [])] or key == v["name"].lower().replace(" ", "-"):
            return k
    raise SystemExit(f"unknown look '{name}'. Run with --list.")

def parse_value(v):
    try:
        return json.loads(v)
    except json.JSONDecodeError:
        return v

def build(args, src_for_fit):
    """Returns a cg.Grade. src_for_fit is an rgb image or a Lab sample."""
    looks, all_stats = load_looks()
    params, ops, stats = {}, [], None
    if args.look:
        key = find_look(args.look, looks)
        lk = looks[key]
        params, ops = dict(lk.get("params", {})), list(lk.get("ops", []))
        stats = all_stats[key]
    if args.ref:
        rs = cg.analyze([cg.load(r, 1600) for r in args.ref])
        if stats is None:
            stats = rs
        else:
            w = args.ref_weight
            stats = cg.merge_stats([stats, rs], [1.0 - w, w])
    if stats is None:
        raise SystemExit("give --ref images and/or --look")
    if args.no_ops:
        ops = []
    for s in args.set or []:
        k, v = s.split("=", 1)
        params[k] = parse_value(v)
    for o in args.add_op or []:
        o = json.loads(o)
        ops = [x for x in ops if x["op"] != o["op"]] + [o] if o.pop("replace", True) else ops + [o]
    for d in args.drop_op or []:
        ops = [x for x in ops if x["op"] != d]
    return cg.Grade(src_for_fit, stats, params, ops)

def add_common(ap):
    ap.add_argument("--ref", nargs="+", help="reference images (any number, same movie or look)")
    ap.add_argument("--look", help="built-in look name, e.g. the-matrix")
    ap.add_argument("--ref-weight", type=float, default=0.5, help="weight of --ref when combined with --look")
    ap.add_argument("--set", action="append", help="override a parameter, e.g. tone=0.8")
    ap.add_argument("--add-op", action="append", help="add or replace a recipe op (JSON)")
    ap.add_argument("--drop-op", action="append", help="remove a recipe op by name")
    ap.add_argument("--no-ops", action="store_true", help="ignore the look's recipe ops")
    ap.add_argument("--lut", help="also write the per-pixel grade as a .cube LUT")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image", nargs="?")
    ap.add_argument("--out", help="output path (default: IMAGE-graded.jpg)")
    ap.add_argument("--max-side", type=int, default=0, help="downscale for fast previews")
    ap.add_argument("--list", action="store_true")
    add_common(ap)
    args = ap.parse_args()
    if args.list:
        looks, _ = load_looks()
        for k, v in looks.items():
            print(f"{k:28s} {v['name']}: {v.get('look', '')}")
        return
    if not args.image:
        ap.error("IMAGE is required")
    img = cg.load(args.image, args.max_side or None)
    g = build(args, img)
    out = args.out or str(Path(args.image).with_name(Path(args.image).stem + "-graded.jpg"))
    cg.save(out, g.render(img))
    print("wrote", out)
    if args.lut:
        g.cube(args.lut, title=args.look or "reference match")
        print("wrote", args.lut)

if __name__ == "__main__":
    main()
