# Audio of Short #3 (tabellone): voice + fixed sfx tied to the board events + music bed 13 dB under the voice (LUFS), sidechain, fixed gain to -16 LUFS + limiter.
import os, subprocess, sys, wave
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
sys.argv = [sys.argv[0]]
import build as B
at = B.at
t10, t20 = at("10"), at("20")
put(load(L + "cc-zoom-whoosh.mp3", peak_db=-20), 0.0, name="opening whoosh")
put(load("core/impact-bass-1.mp3", 1.2, -24, 0.5), 0.02, name="opening hit")
put(load(L + "es-whoosh-medium-transition.mp3", peak_db=-21), B.T_FLIP, "peak", "logo flips")
put(load(L + "cc-impact.mp3", peak_db=-19), B.T_FLIP + 0.9, name="impact: brand")
for k, (tm, td) in enumerate([(B.T_MAP1, B.T_D1), (B.T_MAP2, B.T_D2), (B.T_MAP3, B.T_D3), (B.T_MAP4, B.T_D4), (B.T_MAP5, B.T_D5)]):
    put(load(L + "es-whoosh-classic-airy.mp3", peak_db=-21), tm, name="map up %d" % (k + 1))
    put(load(L + "cc-tick.mp3", peak_db=-27), tm + 0.6, name="path tick")
    put(load(L + "es-whoosh-soft-clean.mp3", 0.9, -22), td, name="dive %d" % (k + 1))
for t, nm in [(at("300") - 0.1, "card 300"), (at("meno") - 0.05, "card 30"), (at("tempo") - 0.1, "card tempo"), (at("lookbook") - 0.4, "laptop"), (at("500") - 0.2, "card total")]:
    put(load(L + "es-pops6.mp3", peak_db=-24), t, name=nm)
put(load(L + "es-scissors-cut-paper.mp3", peak_db=-19), at("rifaccio") - 0.1, name="scissors")
put(load(L + "es-scissors-cut-paper.mp3", peak_db=-21), at("rifaccio") + 2.6, name="scissors 2")
put(load(L + "es-whoosh-soft-airy.mp3", 0.7, -25), at("shooting") - 0.5, name="card falls")
put(load(L + "cc-impact.mp3", peak_db=-21), at("shooting") + 0.75, name="card lands")
put(load(L + "cc-camera.mp3", peak_db=-20), 31.7, name="camera shutter")
put(load(L + "es-whoosh-medium-transition.mp3", peak_db=-22), B.T_D4 + 0.6, "peak", "tags rise")
put(load(L + "cc-riser-corto.mp3", peak_db=-24, fade=0.02), t10, "peak", "riser -> ten")
put(load(L + "cc-impact.mp3", peak_db=-18), t10, name="impact: ten")
put(load(L + "es-number-counter.mp3", 1.2, -27), t10 + 0.05, name="count 10")
put(load(L + "es-number-counter.mp3", 1.0, -28), t20 + 0.05, name="count 20")
put(load(L + "cc-impact.mp3", peak_db=-21), at("totale") + 0.05, name="impact: total")
put(load(L + "es-whoosh-soft-resonant.mp3", 0.6, -25), at("vuoi") - 0.3, name="cta rises")
put(load(L + "cc-impact.mp3", peak_db=-18), 59.45, name="sign lands")
put(load("licensed/al-logo-incoming.mp3", peak_db=-20), at("scrivi") + 0.5, name="logo")
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
