#!/usr/bin/env python3
"""mix-audio.py: rebuild the audio of a composed video WITHOUT rendering the picture again.

The render mixes the voice (from the footage) and every <audio> cue of public/index.html. A change of sound design (cue volume, music
level, a different track) used to cost a full render (20 min at 1080p, 65 min at 4K). This script does the same mix with ffmpeg in about
a minute, so the sound can be iterated and checked before the long render:

  voice (audio of --voice, level 1)  +  every <audio data-start data-duration data-volume> of --index  (x --sfx-gain dB)
  -> loudnorm to --lufs (two-pass, linear) -> optional music bed (add-music.py rules) -> muxed onto the picture of --video (copied, no re-encode)

Usage:
  python3 mix-audio.py --index public/index.html --voice public/input-video.mp4 --video render-raw.mp4 --out out.mp4
                       [--sfx-gain -3] [--music lofi-02] [--music-db -7] [--lufs -14]
"""
import argparse, json, os, re, subprocess, sys, tempfile

ap = argparse.ArgumentParser()
ap.add_argument("--index", required=True); ap.add_argument("--voice", required=True)
ap.add_argument("--video", required=True, help="a rendered picture (its own audio is ignored)"); ap.add_argument("--out", required=True)
ap.add_argument("--sfx-gain", type=float, default=0.0, help="dB added to every sound effect (negative = quieter)")
ap.add_argument("--music", default=""); ap.add_argument("--music-db", type=float, default=-7.0)
ap.add_argument("--duck-ratio", type=float, default=2.5); ap.add_argument("--duck-threshold", type=float, default=0.2)
ap.add_argument("--lufs", type=float, default=-14.0)
a = ap.parse_args()
SK = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
html = open(a.index, encoding="utf-8").read()
base = os.path.dirname(os.path.abspath(a.index))
cues = []
for m in re.finditer(r"<audio\b([^>]*)>", html):
    at = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
    src = at.get("src")
    if not src or "data-start" not in at:
        continue
    cues.append((os.path.join(base, src), float(at["data-start"]), float(at.get("data-duration", 0) or 0), float(at.get("data-volume", 1) or 1)))
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video], capture_output=True, text=True).stdout.strip())
gain = 10 ** (a.sfx_gain / 20.0)
inputs = ["-i", a.voice]
fc = ["[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=1[v0]"]
labels = ["[v0]"]
for i, (path, start, d, vol) in enumerate(cues, start=1):
    if not os.path.exists(path):
        print("WARN missing", path); continue
    inputs += ["-i", path]
    ms = int(round(start * 1000))
    fc.append("[%d:a]aresample=48000,aformat=channel_layouts=stereo,%svolume=%.4f,adelay=%d|%d[s%d]" % (i, ("atrim=0:%.3f," % d) if d else "", vol * gain, ms, ms, i))
    labels.append("[s%d]" % i)
fc.append("%samix=inputs=%d:duration=first:dropout_transition=0:normalize=0,atrim=0:%.3f[mix]" % ("".join(labels), len(labels), dur))
tmp = tempfile.mkdtemp(prefix="mixaudio-", dir=os.environ.get("TEMP") or None)
script = os.path.join(tmp, "fc.txt"); open(script, "w", encoding="utf-8").write(";\n".join(fc))
raw = os.path.join(tmp, "mix.wav")
subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex_script", script, "-map", "[mix]", "-c:a", "pcm_s16le", raw], check=True)
# loudness: measure, then apply linearly (voice + effects at the target level before the music joins)
m = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", raw, "-af", "loudnorm=I=%g:TP=-1.5:LRA=11:print_format=json" % a.lufs, "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
norm = os.path.join(tmp, "norm.wav")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", "loudnorm=I=%g:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true" % (a.lufs, j["input_i"], j["input_tp"], j["input_lra"], j["input_thresh"], j["target_offset"]), "-ar", "48000", norm], check=True)
final = norm
if a.music:
    tr = a.music if os.path.exists(a.music) else os.path.join(SK, "assets", "music", a.music + ".mp3")
    if not os.path.exists(tr):
        sys.exit("track not found: " + a.music)
    final = os.path.join(tmp, "music.wav")
    fcm = ("[1:a]loudnorm=I=-20:TP=-2:LRA=11,aloop=loop=-1:size=2e9,atrim=0:%.3f,asetpts=PTS-STARTPTS,volume=%.1fdB,afade=t=in:d=2,afade=t=out:st=%.3f:d=2[bed];"
           "[0:a]asplit=2[voice][sc];[bed][sc]sidechaincompress=threshold=%g:ratio=%g:attack=15:release=450[duck];[voice][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,alimiter=limit=0.9[a]"
           % (dur, a.music_db, max(0.0, dur - 2), a.duck_threshold, a.duck_ratio))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", norm, "-i", tr, "-filter_complex", fcm, "-map", "[a]", "-ar", "48000", final], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", a.video, "-i", final, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-t", "%.3f" % dur, "-movflags", "+faststart+write_colr", a.out], check=True)
print("wrote %s: %d sound cues (%+.1f dB), voice+fx at %g LUFS%s" % (a.out, len(cues), a.sfx_gain, a.lufs, (", music %s at %.1f dB" % (a.music, a.music_db)) if a.music else ""))
