# Audio of Short #3 (tabellone): voice + fixed sfx tied to the board events + music bed 13 dB under the voice (LUFS), sidechain, fixed gain to -16 LUFS + limiter.
import os, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SK = "D:/ClaudeCodeTest/.claude/skills/youtube-edit/assets/"
MUSIC = SK + "music/licensed/es-pixel-ghost.mp3"
BED, TARGET, SFX_GAIN, SR, DUR = 13.0, -16.0, 5.0, 48000, 65.0
OUT = os.path.join(HERE, "renders"); os.makedirs(OUT, exist_ok=True)


def load(f, dur=None, peak_db=-24, fade=0.08):
    cmd = ["ffmpeg", "-v", "error", "-i", SK + "sfx/" + f] + (["-t", str(dur)] if dur else []) + ["-ar", str(SR), "-ac", "2", "-f", "f32le", "-"]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()
    fd = min(int(fade * SR), len(a) // 3)
    if fd: a[-fd:] *= np.linspace(1, 0, fd)[:, None]
    return a * (10 ** (peak_db / 20) / (np.abs(a).max() + 1e-9))


def peak_time(a): return int(np.argmax(np.convolve(np.abs(a).mean(1), np.ones(2400) / 2400, "same")))


voice = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(HERE, "vo", "vo-placed.mp3"), "-ar", str(SR), "-ac", "2", "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
n = int(DUR * SR); vtrack = np.zeros((n, 2), np.float32); vtrack[:min(n, len(voice))] = voice[:n]
fx = np.zeros_like(vtrack); placed = []


def put(a, t, align="start", name=""):
    s = int(round(t * SR)) - (peak_time(a) if align == "peak" else 0)
    a2 = a[max(0, -s):]; s = max(0, s); e = min(s + len(a2), n)
    if e > s: fx[s:e] += a2[: e - s]; placed.append((round(t, 2), name))


L = "licensed/"
# opening
put(load(L + "cc-zoom-whoosh.mp3", peak_db=-20), 0.0, name="opening whoosh")
put(load("core/impact-bass-1.mp3", 1.2, -24, 0.5), 0.02, name="opening hit")
# Jacopino walks to each square
for i, t in enumerate([1.5, 14.0, 26.0, 38.6, 50.0]):
    put(load(L + ("es-whoosh-soft-clean.mp3" if i % 2 else "es-whoosh-soft-airy.mp3"), 0.9, -25), t - 0.1, name="walk %d" % (i + 1))
# price cards pop in (brand price, then mine)
put(load(L + "es-pops6.mp3", peak_db=-24), 6.2, name="card 300-800")
put(load(L + "es-pops6.mp3", peak_db=-24), 9.8, name="card <30")
put(load(L + "es-scissors-cut-paper.mp3", peak_db=-19), 18.2, name="scissors")
put(load(L + "es-scissors-cut-paper.mp3", peak_db=-21), 21.0, name="scissors 2")
put(load(L + "es-pops6.mp3", peak_db=-25), 20.5, name="card tempo")
# photos: camera click, the 3000-8000 tag falls
put(load(L + "cc-camera.mp3", peak_db=-22), 33.0, name="camera")
put(load(L + "cc-impact.mp3", peak_db=-20), 35.2, name="tag lands")
# the twist: riser into 100 dots, ten then twenty light up
put(load(L + "cc-riser-corto.mp3", peak_db=-24, fade=0.02), 43.0, "peak", "riser -> grid")
put(load(L + "es-whoosh-medium-transition.mp3", peak_db=-22), 39.7, "peak", "grid rises")
put(load(L + "es-number-counter.mp3", 1.2, -27), 43.05, name="count 10")
put(load(L + "es-number-counter.mp3", 1.0, -28), 46.5, name="count 20")
put(load(L + "cc-impact.mp3", peak_db=-18), 46.6, name="impact: 10 poi 20")
# total, arrival, ask, logo
put(load(L + "es-pops6.mp3", peak_db=-24), 54.0, name="card total")
put(load(L + "cc-impact.mp3", peak_db=-21), 54.1, name="impact: total")
put(load(L + "es-whoosh-soft-resonant.mp3", 0.6, -25), 58.2, name="cta rises")
put(load(L + "al-logo-incoming.mp3", peak_db=-20), 61.5, name="logo")
vo_fx = np.clip(vtrack + fx * 10 ** (SFX_GAIN / 20), -1, 1)
VF = os.path.join(OUT, "voice-fx.wav")
with wave.open(VF, "wb") as o:
    o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((vo_fx * 32767).astype(np.int16).tobytes())


def lufs(args):
    o = subprocess.run(["ffmpeg", "-v", "info"] + args + ["-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float([l for l in o.splitlines() if "I:" in l][-1].split("I:")[1].split()[0])


v = lufs(["-i", os.path.join(HERE, "vo", "vo-placed.mp3")]); m = lufs(["-i", MUSIC]); gain = (v - BED) - m
fc = ("[1:a]aloop=loop=-1:size=2e9,asetpts=PTS-STARTPTS,volume=%.2fdB,atrim=0:%.3f,afade=t=in:st=0:d=1.0,afade=t=out:st=%.3f:d=2.5[bed];"
      "[0:a]asplit=2[vo][sc];[bed][sc]sidechaincompress=threshold=0.05:ratio=3:attack=20:release=500[duck];"
      "[vo][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]") % (gain, DUR, DUR - 2.5)
pre = os.path.join(OUT, "mix-pre.wav")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", VF, "-i", MUSIC, "-filter_complex", fc, "-map", "[a]", "-ar", "48000", pre], check=True)
g = TARGET - lufs(["-i", pre])
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", pre, "-af", "volume=%.2fdB,alimiter=limit=0.85:level=disabled" % g, "-ar", "48000", os.path.join(OUT, "mix.wav")], check=True)
print("sounds: %d | voice %.1f LUFS, music %.1f -> %+.1f dB, final gain %+.1f dB" % (len(placed), v, m, gain, g))
