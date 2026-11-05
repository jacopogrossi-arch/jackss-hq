#!/usr/bin/env python3
"""grade-1090.py: fixed check after any grade (course, Jacopo's yes 05/11/2026). How much of the image sits below 10% and above 90% of luma.

    python grade-1090.py clip.mp4 [--fps 1]

A measure, not a verdict: reports the mean and the peak frame. Dreamy reels live with a lot under 10; a face under 10 for most of the frame is too dark.
"""
import argparse
import subprocess

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("--fps", type=float, default=1)
a = ap.parse_args()
W, H = 480, 270
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf", "fps=%g,scale=%d:%d,format=gray" % (a.fps, W, H), "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
f = np.frombuffer(raw, np.uint8).reshape(-1, H * W).astype(np.float32)
f = (f - 16) / 219          # limited range luma to 0-1
lo, hi = (f < .1).mean(1) * 100, (f > .9).mean(1) * 100
print("%d frame | sotto il 10: media %.1f%%, punta %.1f%% | sopra il 90: media %.1f%%, punta %.1f%%" % (len(f), lo.mean(), lo.max(), hi.mean(), hi.max()))
