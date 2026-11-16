#!/usr/bin/env python
"""review8.py: the 8 fps review of a 3D video (Jacopo, 16/11/2026: "to understand movement, look at 8 frames per second").

    python review8.py sheets VIDEO OUTDIR            # contact sheets: 24 frames (3 s) per sheet, 6x4, 200 px wide -> OUTDIR/sheet_01.jpg ...
    python review8.py still  VIDEO [--max 0.8]       # "never still" scan: lists stretches longer than --max seconds where nothing moves except captions
    python review8.py seek   VIDEO_A T_SEC STILL_PNG # seek test: frame at T_SEC of the video vs a still rendered alone (PSNR, needs > 40 dB)

Never-still rule: between two words there is always an object move or a camera move; a caption alone is not a move. The scan ignores the band where captions sit
(rows 52-72% of the height, 9:16 layout) and the top 12% (phase pill), compares consecutive frames at 8 fps and reports runs that stay below the motion threshold.
Needs ffmpeg and numpy.
"""
import os, re, subprocess, sys
import numpy as np


def run(cmd):
    return subprocess.run(cmd, capture_output=True)


def probe(video):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", video]).stdout.decode().strip().split(",")
    return int(out[0]), int(out[1])


def frames8(video, w=90):
    W, H = probe(video); h = int(round(w * H / W))
    raw = run(["ffmpeg", "-v", "error", "-i", video, "-vf", "fps=8,scale=%d:%d,format=gray" % (w, h), "-f", "rawvideo", "-"]).stdout
    n = len(raw) // (w * h)
    return np.frombuffer(raw[: n * w * h], np.uint8).reshape(n, h, w).astype(np.float32), (W, H)


def cmd_sheets(video, outdir):
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        if re.match(r"sheet_\d+\.jpg", f): os.remove(os.path.join(outdir, f))
    r = run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", "fps=8,scale=200:-2,tile=6x4", os.path.join(outdir, "sheet_%02d.jpg")])
    print(r.stderr.decode()[:300] or "ok")
    print(len([f for f in os.listdir(outdir) if f.startswith("sheet_")]), "sheets of 3 s each, read left to right, row by row")


def _runs(flags, fps=8.0):
    out = []; i = 0
    while i < len(flags):
        if flags[i]:
            j = i
            while j < len(flags) and flags[j]: j += 1
            out.append((i / fps, (j - i + 1) / fps)); i = j
        else: i += 1
    return out


def cmd_still(video, max_s=0.8, drift_s=1.2):
    """Two levels, calibrated on Short #1/#2 and the @holcdenis reel (16/11/2026): DEAD = mean change under 2.5/255 (nothing moves, longer than max_s is a failure);
    DRIFT = under 6/255 (only a slow camera push, no object acts; longer than drift_s is a warning). Mean change is global: a local action in a fixed-camera diorama is small,
    so read the warnings with the contact sheets, they are a pointer and not a verdict."""
    a, (W, H) = frames8(video)
    h = a.shape[1]
    mask = np.ones(h, bool); mask[int(h * 0.52):int(h * 0.72)] = False; mask[: int(h * 0.12)] = False
    d = np.abs(np.diff(a[:, mask, :], axis=0)).mean(axis=(1, 2))          # mean change between consecutive frames, 0-255
    dead = [(t, L) for t, L in _runs(d < 2.5) if L > max_s + 1e-6]
    drift = [(t, L) for t, L in _runs(d < 6.0) if L > drift_s + 1e-6]
    print("%s: %d frames at 8 fps, %.1f s, mean motion %.2f (0-255)" % (os.path.basename(video), len(a), len(a) / 8, float(d.mean())))
    print("DEAD (< 2.5, max %.1f s): %s" % (max_s, "PASS" if not dead else "%d stretch(es)" % len(dead)))
    for t, L in dead: print("  dead  from %5.1f s for %.2f s" % (t, L))
    print("DRIFT only (< 6, warn over %.1f s): %s" % (drift_s, "none" if not drift else "%d stretch(es)" % len(drift)))
    for t, L in drift: print("  drift from %5.1f s for %.2f s" % (t, L))
    return dead, drift


def cmd_seek(video, t, png):
    tmp = os.path.join(os.path.dirname(os.path.abspath(png)), "_seek.png")
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", video, "-frames:v", "1", tmp])
    r = run(["ffmpeg", "-i", tmp, "-i", png, "-lavfi", "psnr", "-f", "null", "-"]).stderr.decode()
    m = re.search(r"average:([0-9.inf]+)", r)
    v = m.group(1) if m else "?"
    print("seek test at %ss: PSNR %s dB (%s)" % (t, v, "PASS" if v == "inf" or (v.replace('.', '').isdigit() and float(v) > 40) else "FAIL: something is not a pure function of time"))


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == "sheets": cmd_sheets(a[1], a[2])
    elif len(a) >= 2 and a[0] == "still": cmd_still(a[1], float(a[a.index("--max") + 1]) if "--max" in a else 0.8)
    elif len(a) >= 4 and a[0] == "seek": cmd_seek(a[1], a[2], a[3])
    else: print(__doc__)
