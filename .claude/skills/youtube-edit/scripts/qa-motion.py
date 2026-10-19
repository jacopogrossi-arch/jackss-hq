#!/usr/bin/env python3
"""qa-motion.py: numbers about the MOTION and LOUDNESS of a render, before anyone looks at it (see references/taste.md).

Reports (and writes <out>/qa-motion.md + <out>/sheet.jpg):
  - frozen stretches (ffmpeg freezedetect): every stretch longer than --max-hold seconds (default 0.6) and the total frozen time;
    a stretch that touches the end of the video is the "end hold" (should be <= --end-hold 1.4 s);
  - black/empty runs (blackdetect) longer than 3 frames;
  - integrated loudness and true peak (ebur128) of the delivered file;
  - a contact sheet (one frame every --every seconds, default 2) to look at.
Exit code 1 if a gate fails: a frozen stretch over --max-hold that is not the end hold, the end hold over --end-hold,
a black run, or a true peak above -1.0 dBTP. It measures; it never says a video is good.

Usage: python3 qa-motion.py --video render.mp4 --out qa/ [--max-hold 0.6] [--end-hold 1.4] [--every 2] [--noise -50]
"""
import argparse, os, re, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("--video", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--max-hold", type=float, default=0.6); ap.add_argument("--end-hold", type=float, default=1.4)
ap.add_argument("--every", type=float, default=2.0); ap.add_argument("--noise", type=float, default=-50.0,
                help="freezedetect noise floor in dB (lower = stricter)")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)


def ff(*args):
    return subprocess.run(["ffmpeg", "-nostats", "-hide_banner", *args], capture_output=True, text=True).stderr


dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video],
                           capture_output=True, text=True).stdout.strip())

# frozen stretches
log = ff("-i", a.video, "-vf", "freezedetect=n=%ddB:d=0.3" % int(a.noise), "-an", "-f", "null", "-")
starts = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"freeze_end: ([\d.]+)", log)]
freezes = []
for i, s in enumerate(starts):
    e = ends[i] if i < len(ends) else dur            # a freeze that runs to the end has no freeze_end
    freezes.append((s, e))
total_frozen = sum(e - s for s, e in freezes)

# black runs
blog = ff("-i", a.video, "-vf", "blackdetect=d=0.1:pic_th=0.98", "-an", "-f", "null", "-")
blacks = [(float(s), float(e)) for s, e in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", blog)]

# loudness
llog = ff("-i", a.video, "-af", "ebur128=peak=true", "-vn", "-f", "null", "-")
mi = re.findall(r"I:\s+(-?[\d.]+) LUFS", llog); mp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", llog)
lufs = float(mi[-1]) if mi else None; peak = float(mp[-1]) if mp else None

fails, notes = [], []
for s, e in freezes:
    d = e - s
    at_end = e >= dur - 0.15
    if at_end:
        (fails if d > a.end_hold else notes).append("end hold %.2f s (%.2f-%.2f)%s" % (d, s, e, " > %.1f s" % a.end_hold if d > a.end_hold else ""))
    elif d > a.max_hold:
        fails.append("frozen %.2f s at %.2f-%.2f (> %.1f s)" % (d, s, e, a.max_hold))
for s, e in blacks:
    if e - s > 0.1:
        fails.append("black/empty %.2f s at %.2f-%.2f" % (e - s, s, e))
if peak is not None and peak > -1.0:
    fails.append("true peak %.1f dBFS (> -1.0)" % peak)

ff("-y", "-i", a.video, "-vf", "fps=1/%g,scale=320:-1,tile=6x6" % a.every, "-frames:v", "1", os.path.join(a.out, "sheet.jpg"))

lines = ["# qa-motion: %s" % os.path.basename(a.video), "",
         "duration %.1f s | frozen total %.1f s (%.0f%%) | loudness %s | peak %s" % (
             dur, total_frozen, 100 * total_frozen / dur if dur else 0,
             "%.1f LUFS" % lufs if lufs is not None else "n/a", "%.1f dBFS" % peak if peak is not None else "n/a"), ""]
lines += ["FAIL: " + f for f in fails] or ["no gate failed"]
lines += ["note: " + n for n in notes]
lines += ["", "These are measurements, not a verdict: look at sheet.jpg and the transitions, and say what nobody listened to."]
text = "\n".join(lines)
open(os.path.join(a.out, "qa-motion.md"), "w", encoding="utf-8").write(text + "\n")
print(text)
sys.exit(1 if fails else 0)
