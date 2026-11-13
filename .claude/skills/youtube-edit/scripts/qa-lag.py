#!/usr/bin/env python3
"""qa-lag.py: how long after the word that opens it does each graphic start moving? (UX principle "Doherty threshold", 13/11/2026, proposal not yet voted.)

A plate should answer its word within ~12 frames (0.40 s at 30 fps). Feed it the transcript words and the times at which the graphics start:

  python qa-lag.py --words words.json --starts starts.json [--max 0.40]

  words.json   [{"w": "disegno", "s": 20.26, "e": 20.7}, ...]      (the transcript; "s" = start of the word, seconds)
  starts.json  [18.4, {"t": 31.9, "word": "volume"}, ...]          (graphic start times; "word" is optional: the word it belongs to)

For a start without "word" the nearest word that starts at or before it is taken. Prints each lag and exits 1 if any is over --max (a graphic that starts
BEFORE its word, up to 0.25 s, is fine: plates are allowed to lead). It measures; it does not say a graphic is wrong.
"""
import argparse, json, sys

ap = argparse.ArgumentParser()
ap.add_argument("--words", required=True)
ap.add_argument("--starts", required=True)
ap.add_argument("--max", type=float, default=0.40)
a = ap.parse_args()
words = json.load(open(a.words, encoding="utf-8"))
starts = json.load(open(a.starts, encoding="utf-8"))
bad = 0
for it in starts:
    t = it["t"] if isinstance(it, dict) else float(it)
    w = None
    if isinstance(it, dict) and it.get("word"):
        same = [x for x in words if x["w"].strip(".,;:!?").lower() == it["word"].lower()]
        w = min(same, key=lambda x: abs(x["s"] - t)) if same else None          # the occurrence of that word nearest to the graphic
    if w is None:
        prior = [x for x in words if x["s"] <= t + 0.25]
        w = prior[-1] if prior else None
    if w is None:
        print("%7.2f s  no word before it" % t)
        continue
    lag = t - w["s"]
    flag = lag > a.max
    bad += flag
    print("%7.2f s  %-14s word at %6.2f  lag %+5.2f s%s" % (t, w["w"], w["s"], lag, "  TOO LATE" if flag else ""))
print("\n%d of %d graphics start more than %.2f s after their word." % (bad, len(starts), a.max))
sys.exit(1 if bad else 0)
