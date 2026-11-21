#!/usr/bin/env python3
"""Labeled contact sheet for comparing grades.

  python sheet.py out.jpg img1.jpg img2.jpg ... [--labels a b ...] [--height 520] [--cols 6]
"""
import argparse, sys
from pathlib import Path
import numpy as np, cv2

sys.path.insert(0, str(Path(__file__).parent))
import cg_core as cg

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("images", nargs="+")
    ap.add_argument("--labels", nargs="*")
    ap.add_argument("--height", type=int, default=520)
    ap.add_argument("--cols", type=int, default=6)
    a = ap.parse_args()
    labels = a.labels or [Path(p).stem for p in a.images]
    tiles = []
    for p, lab in zip(a.images, labels):
        im = cg.load(p)
        im = cv2.resize(im, (int(a.height * im.shape[1] / im.shape[0]), a.height), interpolation=cv2.INTER_AREA)
        t = (np.clip(im, 0, 1) * 255).astype(np.uint8)
        bar = np.zeros((30, t.shape[1], 3), np.uint8)
        cv2.putText(bar, lab[:40], (6, 21), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
        tiles.append(np.concatenate([bar, t]))
    w = max(t.shape[1] for t in tiles)
    tiles = [np.pad(t, ((0, 0), (0, w - t.shape[1]), (0, 0))) for t in tiles]
    rows = []
    for i in range(0, len(tiles), a.cols):
        r = tiles[i:i + a.cols]
        r += [np.zeros_like(tiles[0])] * (a.cols - len(r)) if len(tiles) > a.cols else []
        rows.append(np.concatenate(r, 1))
    sheet = np.concatenate(rows, 0)
    cv2.imwrite(a.out, cv2.cvtColor(sheet, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])
    print("wrote", a.out)

if __name__ == "__main__":
    main()
