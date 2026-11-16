"""sfx.py (v2): il sound design sotto la voce. Più fitto della v1, pensato per Instagram:
- apertura: whoosh sul primo fotogramma + riser che sale fino alla battuta "è colpa del pavimento", con un impatto lì;
- pop sulle etichette che spuntano, swish sulle scritte, whoosh sulle mosse di camera grandi;
- ticchettio sotto il contatore dei prodotti, campanello alla cassa, auto che sfrecciano in autostrada, il tetto che si alza.
Legge voce/voce-only.wav e scrive voce/voce-pause.wav (finish.sh usa quest'ultimo)."""
import os, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE); sys.path.insert(0, HERE)
import video as v  # noqa: E402

SK = v.SK + "/assets/sfx/"
SR = 48000
_cache = {}


def load(f, dur=None, peak_db=-24, fade=0.08):
    k = (f, dur, peak_db)
    if k in _cache:
        return _cache[k]
    cmd = ["ffmpeg", "-v", "error", "-i", SK + f] + (["-t", str(dur)] if dur else []) + ["-ar", str(SR), "-ac", "2", "-f", "f32le", "-"]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()
    n = len(a); fd = min(int(fade * SR), n // 3)
    if fd:
        a[-fd:] *= np.linspace(1, 0, fd)[:, None]
    a *= 10 ** (peak_db / 20) / (np.abs(a).max() + 1e-9)
    _cache[k] = a
    return a


def peak_time(a):
    """Dove il suono è più forte (per allineare il culmine di un riser o di un whoosh a un istante)."""
    env = np.convolve(np.abs(a).mean(1), np.ones(2400) / 2400, "same")
    return int(np.argmax(env))


src = os.path.join(HERE, "voce", "voce-only.wav")
with wave.open(src, "rb") as r:
    params = r.getparams(); voice = np.frombuffer(r.readframes(r.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
mix = np.zeros_like(voice)
placed = []


def put(a, t, align="start", name=""):
    off = peak_time(a) if align == "peak" else 0
    s = int(round(t * SR)) - off
    a2 = a[max(0, -s):]; s = max(0, s); e = min(s + len(a2), len(mix))
    if e > s:
        mix[s:e] += a2[: e - s]; placed.append((round(t, 2), name))


at = v.at
w, overlays = v.build_world()
punch = at("colpa", 2)
# ---- apertura
put(load("licensed/cc-zoom-whoosh.mp3", peak_db=-20), 0.0, name="whoosh d'apertura")
put(load("core/impact-bass-1.mp3", 1.2, -24, 0.5), 0.02, name="colpo d'apertura")
put(load("licensed/cc-riser-lungo.mp3", peak_db=-22, fade=0.02), punch, "peak", "riser")
put(load("licensed/cc-impact.mp3", peak_db=-17), punch, name="impatto: colpa del pavimento")
# ---- eventi del racconto
put(load("licensed/es-swoosh-wide.mp3", peak_db=-25), at("E", 1, 16) + 0.25, "peak", "auto che sfreccia")
put(load("licensed/es-swoosh-wide.mp3", peak_db=-27), at("fretta") - 0.1, "peak", "auto che sfreccia 2")
put(load("core/whoosh-cinematic.mp3", 2.6, -23), at("guarda") - 0.2, name="il tetto si alza")
put(load("licensed/es-number-counter.mp3", peak_db=-31), at("Più") + 0.45, name="contatore")
put(load("licensed/es-number-counter.mp3", peak_db=-32), at("Più") + 4.1, name="contatore 2")
put(load("core/chime.mp3", 1.4, -25, 0.4), at("cassa"), name="campanello cassa")
put(load("licensed/cc-impact.mp3", peak_db=-21), at("percorso", 1, 68), name="impatto: percorso obbligato")
put(load("licensed/es-reverse-glass.mp3", peak_db=-26), at("Il", 1, 77) - 0.1, "peak", "si riparte")
fixed = [t for t, _ in placed]

# ---- pop sulle etichette, swish sulle scritte, whoosh sulle mosse grandi (mai due suoni a meno di 0.35 s, mai sopra gli eventi fissi)
pops = [load("pack2/pop1.mp3", peak_db=-24), load("pack2/pop2.mp3", peak_db=-24), load("core/pop.mp3", 0.4, -27)]
swish = [load("licensed/es-whoosh-soft-resonant.mp3", 0.57, -27), load("licensed/es-whoosh-generic-air.mp3", 0.55, -27), load("licensed/es-swish-classic-filter.mp3", 0.67, -28)]
big = load("licensed/es-whoosh-soft-airy.mp3", 0.9, -25)
ev = [(L["at"], "pop") for L in w.labels] + [(o[4], "swish") for o in overlays if o[4] > 0.3]
ev += [(c["t"], "big") for c in w.cams[1:] if c.get("d", 0) >= 0.8 and c.get("ease") != "linear"]
ev.sort()
last, k = -9, 0
for t, kind in ev:
    if t - last < 0.35 or any(abs(t - f) < 0.4 for f in fixed):
        continue
    if kind == "pop":
        put(pops[k % 3], t, name="pop")
    elif kind == "swish":
        put(swish[k % 3], t - 0.3, name="swish")
    else:
        put(big, t, "peak" if False else "start", "whoosh camera")
    k += 1; last = t

out = np.clip(voice + mix * 10 ** (5 / 20), -1, 1)       # v2.1: effetti +5 dB (nella v2 erano troppo bassi)
with wave.open(os.path.join(HERE, "voce", "voce-pause.wav"), "wb") as o:
    o.setparams(params); o.writeframes((out * 32767).astype(np.int16).tobytes())
print("suoni piazzati:", len(placed), "| eventi fissi:", ", ".join("%s@%.1f" % (n, t) for t, n in placed[:12]))
