#!/usr/bin/env python3
"""check-frames.py: look at a render the way a viewer watches it: 10 frames a second, with a clear gap between tiles.

Why: one frame a second misses what a viewer sees at once (an animation that plays twice, a flash, text that lands too
late). Tiles that touch make two neighbouring frames look like one flashing image (fake glitches), so every tile has a
white gap. Never call something a defect on a tile: look at ONE full-size frame with --frame.

Writes <out>/sheet_01.jpg, sheet_02.jpg ... (each time-labelled, --cols x --rows tiles) and <out>/check-report.md.
The report holds only what a computer can catch (a word said twice in a row, a card on screen too briefly to read);
the six viewer checks below are for the eyes:
  1 an animation plays twice | 2 a graphic flashes (under 0.5 s) or the picture pops | 3 text lands too late to read
  4 a graphic covers the face | 5 a word is said twice | 6 lips drift out of sync with the voice
Say what you saw by time ("graphic at 8.2 s covers the chin"); never just "looks good".

Usage:
  python3 check-frames.py --video render.mp4 --out check/ [--fps 10] [--cols 6] [--rows 5] [--start T --end T]
                          [--transcript transcript.json] [--index public/index.html]
  python3 check-frames.py --video render.mp4 --out check/ --frame 8.2        one full-size frame, then stop
Exit code 0 always: this reports, it does not gate (qa-motion.py and verify-render.py gate).
"""
import argparse, glob, json, os, re, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("--video", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--fps", type=int, default=10); ap.add_argument("--cols", type=int, default=6); ap.add_argument("--rows", type=int, default=5)
ap.add_argument("--start", type=float, default=0.0); ap.add_argument("--end", type=float, default=0.0, help="0 = to the end")
ap.add_argument("--frame", type=float, help="write one full-size frame at this second and stop")
ap.add_argument("--transcript", help="Parakeet transcript.json of the render: finds a word said twice in a row")
ap.add_argument("--index", help="public/index.html: finds cards on screen too briefly to read")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)


def ff(*args):
    return subprocess.run(["ffmpeg", "-y", "-v", "error", *args], capture_output=True, text=True)


if a.frame is not None:
    path = os.path.join(a.out, "frame_%g.png" % a.frame)
    ff("-ss", str(a.frame), "-i", a.video, "-frames:v", "1", path)
    print(path)
    sys.exit(0)

for old in glob.glob(os.path.join(a.out, "sheet_*.jpg")):
    os.remove(old)
dims = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", a.video],
                      capture_output=True, text=True).stdout.strip().split("x")
tw = 320
th = int(tw * int(dims[1]) / int(dims[0])) // 2 * 2
window = (["-ss", str(a.start)] if a.start else []) + (["-to", str(a.end)] if a.end else [])
label = ""
# the time label is written when drawtext works; fonts can be missing (then ffmpeg fails), so retry without it
if "Unknown filter" not in subprocess.run(["ffmpeg", "-hide_banner", "-h", "filter=drawtext"], capture_output=True, text=True).stdout:
    label = r",drawtext=text='%{pts\:hms}':x=4:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6"
sheet_out = os.path.join(a.out, "sheet_%02d.jpg")
tile = lambda lab: "fps=%d,scale=%d:%d%s,tile=%dx%d:padding=10:color=white" % (a.fps, tw, th, lab, a.cols, a.rows)
r = ff(*window, "-i", a.video, "-vf", tile(label), "-q:v", "3", sheet_out)
if label and not glob.glob(os.path.join(a.out, "sheet_*.jpg")):
    label = ""
    r = ff(*window, "-i", a.video, "-vf", tile(label), "-q:v", "3", sheet_out)
sheets = sorted(glob.glob(os.path.join(a.out, "sheet_*.jpg")))

per = a.cols * a.rows
lines = ["# check-frames: %s" % os.path.basename(a.video), "",
         "%d sheets in %s (each = %d frames = %.1f s of video, from %.1f s)" % (len(sheets), a.out, per, per / a.fps, a.start), ""]
if not sheets:
    lines.append("FAIL: no sheet written. ffmpeg said: " + r.stderr.strip()[:300])
if not label:
    lines.append("note: this ffmpeg has no drawtext, so the tiles carry no time. Tile k of sheet n is at %.1f s + (n-1) x %.1f s + k/%d." % (a.start, per / a.fps, a.fps))

lines.append("AUTO CHECKS (a computer catches only some of the six):")
if a.transcript:
    d = json.load(open(a.transcript))
    words = d["words"] if isinstance(d, dict) and "words" in d else d
    norm = lambda t: re.sub(r"[^a-z0-9']", "", t.lower())
    twice = ['%.1f s "%s"' % (float(x["start"]), x["text"]) for x, y in zip(words, words[1:])
             if norm(x["text"]) == norm(y["text"]) and len(norm(x["text"])) > 2]
    lines.append("- word said twice in a row: " + (", ".join(twice) if twice else "none found"))
if a.index:
    html = open(a.index, encoding="utf-8").read()
    short = []
    for m in re.finditer(r'<div[^>]*class="[^"]*card-host[^"]*"[^>]*>', html):
        tag = m.group(0)
        get = lambda k: (re.search(r'%s="([^"]*)"' % k, tag) or [None, None])[1]
        s, dur, anc = get("data-start"), get("data-duration"), get("data-anchor") or ""
        if not s or not dur:
            continue
        s, dur = float(s), float(dur)
        n = 0 if anc == "-" else len(anc.split())
        if dur < 0.5:
            short.append("card at %.1f s shows only %.2f s: a flash" % (s, dur))
        elif n and dur < 0.5 + 0.35 * n:
            short.append("card at %.1f s: %d words in %.2f s, may be too fast to read" % (s, n, dur))
    lines += ["- " + x for x in short] or ["- cards on screen long enough to read: none flagged"]
if not a.transcript and not a.index:
    lines.append("- (none run: pass --transcript and/or --index)")
lines += ["", "YOU LOOK AT EVERY SHEET, in order, for: animation plays twice | flash under 0.5 s or a pop | text too late to read | "
          "graphic covers the face | word said twice | lips out of sync (pick 5 moments and compare mouth and word).",
          "Before calling a defect, look at one full-size frame: check-frames.py --video ... --frame T."]
text = "\n".join(lines)
open(os.path.join(a.out, "check-report.md"), "w", encoding="utf-8").write(text + "\n")
print(text)
