#!/usr/bin/env python3
"""sound-report.py: the numbers of a sound mix, because Claude cannot listen (idea from Jacopo's sound-design guide, 24/10/2026).

Reads the stems mix-audio.py writes with --stems (voice.wav, fx.wav, music.wav at the mix's own levels), the <audio> cues of
public/index.html and the delivered file, and writes SOUND-REPORT.md:
  - voice, effects and music: loudness (LUFS, gated, so silences do not count) and how many dB each sits under the voice;
  - every effect: time, file, its level in its own window against the voice, and whether the voice is speaking under it;
  - the master: integrated LUFS and true peak.
It WARNS (never fails) when a number is outside the house targets, so the human ear decides:
  effects about 7 dB under the voice (warn above -3 dB or below -16 dB), music 13-15 dB under the voice (Jacopo's ear on video #2:
  ~10 dB under was too loud; warn under 11 or over 18), master -14 LUFS (+-1) and true peak at most -1.0 dBTP.

Usage: python3 sound-report.py --stems W/stems --index W/public/index.html --final W/final.mp4 --out W/SOUND-REPORT.md
Exit code 0 always; the WARN lines are the to-do list.
"""
import argparse, os, re, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("--stems", required=True); ap.add_argument("--index", required=True)
ap.add_argument("--final", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--fx-target", type=float, default=-7.0, help="dB of an effect against the voice")
ap.add_argument("--music-under", default="13,15", help="dB range the music sits under the voice")
a = ap.parse_args()
MU = [float(x) for x in a.music_under.split(",")]


def ff(*args):
    return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *args], capture_output=True, text=True).stderr


def lufs(path, ss=None, t=None):
    """integrated loudness (gated) and true peak of a file or a window of it; None when there is no signal"""
    win = (["-ss", "%.3f" % ss] if ss is not None else []) + (["-t", "%.3f" % t] if t is not None else [])
    o = ff(*win, "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-")
    i = re.findall(r"I:\s+(-?[\d.]+|-inf) LUFS", o); p = re.findall(r"Peak:\s+(-?[\d.]+|-inf) dBFS", o)
    li = float(i[-1]) if i and i[-1] != "-inf" else None
    return (li if li is not None and li > -69 else None), (float(p[-1]) if p and p[-1] != "-inf" else None)


def rms(path, ss, t):
    o = ff("-ss", "%.3f" % ss, "-t", "%.3f" % t, "-i", path, "-af", "astats=measure_perchannel=none:measure_overall=RMS_level", "-f", "null", "-")
    v = re.findall(r"RMS level dB:\s*(\S+)", o)
    return float(v[-1]) if v and v[-1] not in ("-inf", "nan") else -200.0


st = {n: os.path.join(a.stems, n + ".wav") for n in ("voice", "fx", "music")}
voice_l, _ = lufs(st["voice"])
fx_l, _ = lufs(st["fx"]) if os.path.exists(st["fx"]) else (None, None)
mus_l, _ = lufs(st["music"]) if os.path.exists(st["music"]) else (None, None)
master_l, master_tp = lufs(a.final)
# the voice level a cue is compared with: the voice's RMS over its speaking parts (the whole stem's RMS counts its pauses)
v_rms_all = rms(st["voice"], 0, 1e6)

html = open(a.index, encoding="utf-8").read()
cues = []
for m in re.finditer(r"<audio\b([^>]*)>", html):
    at = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
    if at.get("src") and "data-start" in at:
        cues.append((float(at["data-start"]), float(at.get("data-duration") or 0.5), at["src"], at.get("id", "")))
cues.sort()

warn, rows = [], []
ref = voice_l if voice_l is not None else v_rms_all
for t0, d, src, cid in cues:
    d = min(max(d, 0.1), 3.0)
    lv = rms(st["fx"], t0, d)
    vv = rms(st["voice"], t0, d)
    speaking = vv > v_rms_all - 10
    rel = lv - (v_rms_all + 3.0)          # RMS of speech runs ~3 dB under its gated loudness; compare like with like
    rows.append("| %.2f | `%s` | %+.1f dB | %s |" % (t0, os.path.basename(src), rel, "yes" if speaking else "no"))
    if lv < -150:
        warn.append("effect at %.2f s (%s) is SILENT in the fx stem: missing file or zero volume" % (t0, os.path.basename(src)))
    elif rel > a.fx_target + 4:
        warn.append("effect at %.2f s (%s) is %+.1f dB against the voice: too loud (target about %+.0f)" % (t0, os.path.basename(src), rel, a.fx_target))
    elif rel < a.fx_target - 9:
        warn.append("effect at %.2f s (%s) is %+.1f dB against the voice: probably inaudible on a phone" % (t0, os.path.basename(src), rel))
mus_under = (voice_l - mus_l) if (voice_l is not None and mus_l is not None) else None
if mus_under is not None and not (MU[0] - 2 <= mus_under <= MU[1] + 3):
    warn.append("music sits %.1f dB under the voice (house range %g-%g)" % (mus_under, MU[0], MU[1]))
if master_l is not None and abs(master_l + 14) > 1.0:
    warn.append("master at %.1f LUFS (target -14 +-1)" % master_l)
if master_tp is not None and master_tp > -1.0:
    warn.append("master true peak %.1f dBTP (max -1.0)" % master_tp)

fmt = lambda x: "n/a" if x is None else "%.1f LUFS" % x
L = ["# Sound report", "", "Measured, not heard: these numbers say where a sound sits, the ear says whether it is good.", "",
     "| Track | Loudness | Under the voice |", "|---|---|---|",
     "| Voice | %s | - |" % fmt(voice_l),
     "| Effects (all) | %s | %s |" % (fmt(fx_l), "n/a" if fx_l is None or voice_l is None else "%.1f dB" % (voice_l - fx_l)),
     "| Music (after ducking) | %s | %s |" % (fmt(mus_l), "n/a" if mus_under is None else "%.1f dB" % mus_under),
     "| **Master** | %s, true peak %s | |" % (fmt(master_l), "n/a" if master_tp is None else "%.1f dBTP" % master_tp), "",
     "## Effects (%d)" % len(cues), "", "| Time (s) | File | Level vs voice | Voice speaking |", "|---|---|---|---|"] + (rows or ["| - | none | - | - |"])
L += ["", "## Warnings (%d)" % len(warn), ""] + (["- " + w for w in warn] or ["- none: every number is inside the house targets"])
open(a.out, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
