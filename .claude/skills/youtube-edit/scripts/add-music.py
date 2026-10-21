#!/usr/bin/env python3
"""add-music.py: lay a light music bed (lo-fi / chill hip hop) under the voice of a finished video, ducked while the voice speaks.

The bed is looped to the video length, fades in/out, and is pushed down by a sidechain compressor keyed on the voice (it
breathes back up in pauses). The voice is not touched. Video is copied (no re-encode). Keep a no-music twin of the master.

Usage:
  python3 add-music.py --video master.mp4 --out master-music.mp4 [--track lofi-02 | path/to/bed.mp3]
                       [--db -14] [--lufs -14] [--fade 2.0] [--start 0]
--track: a name in assets/music (lofi-01..04, no extension) or any audio file. --db: bed level in dB relative to its own -20 LUFS
normalisation (measured on video #2: -3 with threshold 0.2 / ratio 2.5 puts the ducked bed about 10 dB under a -14 LUFS voice; the old default, -14, left it 20+ dB under, inaudible on a phone). --start: where the bed begins.
"""
import argparse, os, subprocess, json, sys
ap = argparse.ArgumentParser()
ap.add_argument("--video", required=True); ap.add_argument("--out", required=True); ap.add_argument("--track", default="lofi-02")
ap.add_argument("--db", type=float, default=-3.0)
ap.add_argument("--duck-ratio", type=float, default=2.5, help="sidechain ratio: 10 = the bed nearly disappears while the voice speaks, 3-4 = it dips about 3-4 dB")
ap.add_argument("--duck-threshold", type=float, default=0.2)
ap.add_argument("--lufs", type=float, default=-14.0, help="loudness of the delivered file (0 = leave as it is)")
ap.add_argument("--fade", type=float, default=2.0); ap.add_argument("--start", type=float, default=0.0)
a = ap.parse_args()
SK = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
tr = a.track if os.path.exists(a.track) else os.path.join(SK, "assets", "music", a.track + ".mp3")
if not os.path.exists(tr):
    sys.exit("track not found: %s (assets/music has: %s)" % (a.track, ", ".join(sorted(os.listdir(os.path.join(SK, "assets", "music"))))))
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video], capture_output=True, text=True).stdout.strip())
L = max(1.0, dur - a.start)
bed = ("[1:a]aloop=loop=-1:size=2e9,atrim=0:%.3f,asetpts=PTS-STARTPTS,%s,afade=t=in:st=0:d=%.2f,afade=t=out:st=%.3f:d=%.2f,adelay=%d|%d[bed]"
       % (L, "volume=%.1fdB" % a.db, a.fade, max(0.0, L - a.fade), a.fade, int(a.start * 1000), int(a.start * 1000)))
fc = (bed + ";[0:a]asplit=2[voice][sc];[bed][sc]sidechaincompress=threshold=%g:ratio=%g:attack=15:release=450[duck];"
      "[voice][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0%s,alimiter=limit=0.8:level=disabled[a]" % (a.duck_threshold, a.duck_ratio, ",loudnorm=I=%g:TP=-2:LRA=11,aresample=48000" % a.lufs if a.lufs else ""))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", a.video, "-i", tr, "-filter_complex", fc, "-map", "0:v:0", "-map", "[a]", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", a.out], check=True)
print("wrote %s (bed %s at %.1f dB, ducked under the voice)" % (a.out, os.path.basename(tr), a.db))
