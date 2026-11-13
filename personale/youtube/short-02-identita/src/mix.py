# Audio of Short #2 (13/11/2026; copied from Short #1 v4), on the autogrill method (references/explainer-3d-sop.md §7):
#  1. voice + sound effects (numpy): fixed story events, an opening whoosh + hit + a riser whose PEAK lands on "gonna";
#     automatic pops on labels, swishes on big statements, whooshes on camera moves; never two sounds within 0.35 s, never on top of a fixed event.
#  2. music: a bed BED dB under the voice MEASURED in LUFS, ducked under speech (sidechain), then one FIXED gain to TARGET LUFS + limiter (no single-pass loudnorm).
# Writes renders/mix.wav (the full soundtrack). Needs vo.mp3.
import os, subprocess, sys, wave
import numpy as np
sys.argv = [sys.argv[0]]
import build as B
SK = "D:/ClaudeCodeTest/.claude/skills/youtube-edit/assets/"
MUSIC = SK + "music/licensed/es-auxjack-locomotivate.mp3"
BED, TARGET, SFX_GAIN = 13.0, -16.0, 5.0
SR = 48000
at, end, DUR = B.at, B.end, B.DUR
OUT = os.path.join(B.HERE, "renders"); os.makedirs(OUT, exist_ok=True)


def load(f, dur=None, peak_db=-24, fade=0.08):
    cmd = ["ffmpeg", "-v", "error", "-i", SK + "sfx/" + f] + (["-t", str(dur)] if dur else []) + ["-ar", str(SR), "-ac", "2", "-f", "f32le", "-"]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()
    fd = min(int(fade * SR), len(a) // 3)
    if fd: a[-fd:] *= np.linspace(1, 0, fd)[:, None]
    return a * (10 ** (peak_db / 20) / (np.abs(a).max() + 1e-9))


def peak_time(a):
    return int(np.argmax(np.convolve(np.abs(a).mean(1), np.ones(2400) / 2400, "same")))


voice = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(B.HERE, "vo.mp3"), "-ar", str(SR), "-ac", "2", "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
n = int(DUR * SR); vtrack = np.zeros((n, 2), np.float32); vtrack[:min(n, len(voice))] = voice[:n]
fx = np.zeros_like(vtrack); placed = []


def put(a, t, align="start", name=""):
    s = int(round(t * SR)) - (peak_time(a) if align == "peak" else 0)
    a2 = a[max(0, -s):]; s = max(0, s); e = min(s + len(a2), n)
    if e > s: fx[s:e] += a2[: e - s]; placed.append((round(t, 2), name))


L = "licensed/"
# ---- the opening: the totem turns over on "Inverso"
put(load(L + "cc-zoom-whoosh.mp3", peak_db=-20), 0.0, name="opening whoosh")
put(load("core/impact-bass-1.mp3", 1.2, -24, 0.5), 0.02, name="opening hit")
put(load(L + "cc-riser-corto.mp3", peak_db=-24, fade=0.02), B.T_FLIP + 0.35, "peak", "riser -> flip")
put(load(L + "al-flash-impact.mp3", peak_db=-19), B.T_FLIP + 0.4, name="impact: INVERSO reads")
put(load(L + "cc-impact.mp3", peak_db=-21), at("terzo"), name="impact: il terzo")
lk = B.T_D1 - 0.2
put(load(L + "es-whoosh-medium-transition.mp3", peak_db=-20), lk, "peak", "film burn (leak)")
# ---- the map: up = airy whoosh, the path draws with soft ticks, down = clean whoosh
for i, (tm, td) in enumerate([(B.T_MAP1, B.T_D1), (B.T_MAP2, B.T_D2), (B.T_MAP3, B.T_D3)]):
    put(load(L + "es-whoosh-classic-airy.mp3", peak_db=-21), tm, name="map up %d" % (i + 1))
    if i: put(load(L + "cc-tick.mp3", peak_db=-27), tm + 0.55, name="path draws"); put(load(L + "cc-tick.mp3", peak_db=-28), tm + 1.0, name="path draws")
    if i: put(load(L + "es-whoosh-soft-clean.mp3", 0.9, -22), td, name="dive %d" % (i + 1))
# ---- 1: the reverse side
put(load(L + "cloth-feed.mp3", peak_db=-22), B.T_TURN + 0.1, name="panel turns over")
put(load(L + "cc-impact.mp3", peak_db=-18), B.T_X, name="impact: X on the dirty one")
for _t in (at("ore") - 0.05, at("errori") - 0.05, at("costa") - 0.15):
    put(load(L + "es-pops6.mp3", peak_db=-25), _t, name="card pinned")
# ---- 2: the rail races, empties, one trouser
put(load(L + "al-swoosh-intense.mp3", peak_db=-24), B.T_D2 + 0.4, name="rail races")
put(load(L + "al-whoosh-scrapy.mp3", peak_db=-24), B.T_CLEAR - 0.2, name="rail empties")
put(load(L + "al-clock-tick.mp3", 2.5, -24), B.T_MESI + 0.3, name="clock races")
put(load(L + "cc-impact.mp3", peak_db=-21), at("fatto", 2), name="impact: è un fatto")
# ---- 3: the boxes
put(load(L + "es-number-counter.mp3", 0.9, -28), at("scarpa") - 0.1, name="boxes stack")
put(load(L + "al-reverse-charge.mp3", peak_db=-24), B.T_DROP, name="five boxes go")
put(load(L + "cc-impact.mp3", peak_db=-16), at("sei"), name="impact: Non sei")
put(load(L + "es-swoosh-wide.mp3", peak_db=-24), B.T_DIA + 0.6, name="axis draws")
put(load(L + "cc-knock.mp3", peak_db=-22), at("ostentazione") + 0.25, name="puck lands")
put(load(L + "cc-knock.mp3", peak_db=-22), at("flexing") + 0.05, name="puck slides")
put(load(L + "al-logo-incoming.mp3", peak_db=-20), at("inverso", 2) + 0.1, name="puck to the middle")
put(load(L + "al-charge-riser.mp3", peak_db=-25, fade=0.02), at("inverso", 3) - 0.25, "peak", "riser -> last turn")
put(load(L + "cc-impact.mp3", peak_db=-17), at("inverso", 3), name="impact: Questo è Inverso")
fixed = [t for t, _ in placed]
# ---- automatic: pops on labels, swishes on big statements, whooshes on camera moves
pops = [load("pack2/pop1.mp3", peak_db=-24), load("pack2/pop2.mp3", peak_db=-24), load("core/pop.mp3", 0.4, -27)]
swish = [load(L + "es-whoosh-soft-resonant.mp3", 0.57, -26), load(L + "es-whoosh-generic-air.mp3", 0.55, -26), load(L + "es-swish-classic-filter.mp3", 0.67, -27)]
whoosh = [load(L + "es-whoosh-soft-airy.mp3", 0.9, -24), load(L + "es-swoosh-wide.mp3", 0.9, -26), load(L + "es-whoosh-soft-clean.mp3", 0.9, -25)]
ev = [(l["at"], "pop") for l in B.w.labels] + [(b[0], "swish") for b in B.w.bigs if b[0] > 0.3]
ev += [(c[0], "whoosh") for c in B.CAMS if 0.8 <= c[1] <= 1.4 and c[0] > 0.5]
last, k = -9, 0
for t, kind in sorted(ev):
    if t - last < 0.35 or any(abs(t - f) < 0.4 for f in fixed): continue
    if kind == "pop": put(pops[k % 3], t, name="pop")
    elif kind == "swish": put(swish[k % 3], t - 0.3, name="swish")
    else: put(whoosh[k % 3], t - 0.12, name="whoosh")
    k += 1; last = t
vo_fx = np.clip(vtrack + fx * 10 ** (SFX_GAIN / 20), -1, 1)
VF = os.path.join(OUT, "voice-fx.wav")
with wave.open(VF, "wb") as o:
    o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((vo_fx * 32767).astype(np.int16).tobytes())


def lufs(args):
    o = subprocess.run(["ffmpeg", "-v", "info"] + args + ["-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float([l for l in o.splitlines() if "I:" in l][-1].split("I:")[1].split()[0])


v = lufs(["-i", os.path.join(B.HERE, "vo.mp3")]); m = lufs(["-i", MUSIC]); gain = (v - BED) - m
fc = ("[1:a]aloop=loop=-1:size=2e9,asetpts=PTS-STARTPTS,volume=%.2fdB,atrim=0:%.3f,afade=t=in:st=0:d=1.0,afade=t=out:st=%.3f:d=2.5[bed];"
      "[0:a]asplit=2[vo][sc];[bed][sc]sidechaincompress=threshold=0.05:ratio=3:attack=20:release=500[duck];"
      "[vo][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]") % (gain, DUR, DUR - 2.5)
pre = os.path.join(OUT, "mix-pre.wav")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", VF, "-i", MUSIC, "-filter_complex", fc, "-map", "[a]", "-ar", "48000", pre], check=True)
g = TARGET - lufs(["-i", pre])
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", pre, "-af", "volume=%.2fdB,alimiter=limit=0.85:level=disabled" % g, "-ar", "48000", os.path.join(OUT, "mix.wav")], check=True)
print("sounds placed: %d | voice %.1f LUFS, music %.1f -> %+.1f dB (%.0f dB under), final gain %+.1f dB" % (len(placed), v, m, gain, BED, g))
for t, nm in sorted(placed): print("  %6.2f %s" % (t, nm))
