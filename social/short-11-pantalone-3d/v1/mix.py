# Audio of Short #11 (pantalone 3D): voice + fixed sfx tied to the board events + music bed 13 dB under the voice (LUFS), sidechain, fixed gain to -16 LUFS + limiter.
import os, subprocess, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SK = "D:/ClaudeCodeTest/.claude/skills/youtube-edit/assets/"
MUSIC = SK + "music/licensed/es-skyline.mp3"
BED, TARGET, SFX_GAIN, SR, DUR = 13.0, -16.0, 5.0, 48000, 36.5
VO = "D:/ClaudeCodeTest/videos/_bench/short11/vo/vo.mp3"
OUT = "D:/ClaudeCodeTest/videos/_bench/short11/renders"; os.makedirs(OUT, exist_ok=True)


def load(f, dur=None, peak_db=-24, fade=0.08):
    cmd = ["ffmpeg", "-v", "error", "-i", SK + "sfx/" + f] + (["-t", str(dur)] if dur else []) + ["-ar", str(SR), "-ac", "2", "-f", "f32le", "-"]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()
    fd = min(int(fade * SR), len(a) // 3)
    if fd: a[-fd:] *= np.linspace(1, 0, fd)[:, None]
    return a * (10 ** (peak_db / 20) / (np.abs(a).max() + 1e-9))


def peak_time(a): return int(np.argmax(np.convolve(np.abs(a).mean(1), np.ones(2400) / 2400, "same")))


voice = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", VO, "-ar", str(SR), "-ac", "2", "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
n = int(DUR * SR); vtrack = np.zeros((n, 2), np.float32); vtrack[:min(n, len(voice))] = voice[:n]
fx = np.zeros_like(vtrack); placed = []


def put(a, t, align="start", name=""):
    s = int(round(t * SR)) - (peak_time(a) if align == "peak" else 0)
    a2 = a[max(0, -s):]; s = max(0, s); e = min(s + len(a2), n)
    if e > s: fx[s:e] += a2[: e - s]; placed.append((round(t, 2), name))


L = "licensed/"
sys.argv = [sys.argv[0]]
import build as B
at = B.at
put(load(L + "cc-zoom-whoosh.mp3", peak_db=-20), 0.0, name="opening whoosh")
put(load("core/impact-bass-1.mp3", 1.2, -24, 0.5), 0.02, name="opening hit")
SW = [("es-swish-classic-filter.mp3", 0.67, -26), ("es-whoosh-soft-resonant.mp3", 0.57, -26), ("es-whoosh-generic-air.mp3", 0.55, -26)]
_k = [0]


def swish(t, name, extra=0.0):
    f, d, p = SW[_k[0] % 3]; _k[0] += 1
    put(load(L + f, d, p + extra), t, name=name)


for t, nm in [(B.T_SCHEDA, "dive desk"), (B.T_VISTE, "dive photo set"), (B.T_3D, "dive hero")]:
    put(load(L + "es-whoosh-soft-clean.mp3", 0.9, -22), t, name=nm)
for t, nm in [(at("scheda") - 0.1, "card scheda"), (B.VIEWS[0][2], "view 1"), (B.VIEWS[1][2], "view 2"), (B.VIEWS[2][2], "view 3"), (B.VIEWS[3][2], "view 4")]:
    swish(t, nm)
put(load(L + "cc-riser-corto.mp3", peak_db=-23, fade=0.02), B.T_3D, "peak", "riser -> 3D")
put(load(L + "cc-impact.mp3", peak_db=-20), B.T_3D, name="impact 3D")
put(load(L + "es-whoosh-generic-air.mp3", 1.6, -24), at("girare", 1, 20.0), name="spin")
put(load(L + "es-whoosh-soft-airy.mp3", 0.9, -25), at("dietro", 2), name="turn back")
put(load(L + "cc-riser-corto-b.mp3", peak_db=-23, fade=0.02), B.T_NON - 0.06, "peak", "riser close-up")
put(load(L + "cc-impact.mp3", peak_db=-18), B.T_SIGN + 0.55, name="sign lands")
put(load(L + "al-logo-incoming.mp3", peak_db=-20), B.end("commenti") + 0.35, name="logo flip")
put(load(L + "cc-riser-corto.mp3", peak_db=-22, fade=0.02), B.T_CHE - 0.06, "peak", "riser final")
vo_fx = np.clip(vtrack + fx * 10 ** (SFX_GAIN / 20), -1, 1)
VF = os.path.join(OUT, "voice-fx.wav")
with wave.open(VF, "wb") as o:
    o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((vo_fx * 32767).astype(np.int16).tobytes())


def lufs(args):
    o = subprocess.run(["ffmpeg", "-v", "info"] + args + ["-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float([l for l in o.splitlines() if "I:" in l][-1].split("I:")[1].split()[0])


v = lufs(["-i", VO]); m = lufs(["-i", MUSIC]); gain = (v - BED) - m
fc = ("[1:a]aloop=loop=-1:size=2e9,asetpts=PTS-STARTPTS,volume=%.2fdB,atrim=0:%.3f,afade=t=in:st=0:d=1.0,afade=t=out:st=%.3f:d=2.5[bed];"
      "[0:a]asplit=2[vo][sc];[bed][sc]sidechaincompress=threshold=0.05:ratio=3:attack=20:release=500[duck];"
      "[vo][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]") % (gain, DUR, DUR - 2.5)
pre = os.path.join(OUT, "mix-pre.wav")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", VF, "-i", MUSIC, "-filter_complex", fc, "-map", "[a]", "-ar", "48000", pre], check=True)
g = TARGET - lufs(["-i", pre])
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", pre, "-af", "volume=%.2fdB,alimiter=limit=0.85:level=disabled" % g, "-ar", "48000", os.path.join(OUT, "mix.wav")], check=True)
print("sounds: %d | voice %.1f LUFS, music %.1f -> %+.1f dB, final gain %+.1f dB" % (len(placed), v, m, gain, g))
