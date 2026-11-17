"""Colonna sonora della scena Capitoli v3, generata in codice (48 kHz, stereo)."""
import numpy as np, wave, sys

SR = 48000
DUR = 11.0
CUT = 10.85
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(3)
L = np.zeros(N); R = np.zeros(N)

def db(x): return 10 ** (x / 20)

def lp(x, fc):
    """passa-basso a un polo; fc può variare nel tempo (array)."""
    fc = np.broadcast_to(fc, x.shape)
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s
        y[i] = s
    return y

def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR); j = min(N, i + len(sig))
    if i >= N: return
    L[i:j] += sig[:j - i] * gain * (1 - pan) ** 0.5 * 1.0
    R[i:j] += sig[:j - i] * gain * (1 + pan) ** 0.5 * 1.0

def env(n, a, d):
    """attacco a, decadimento d (secondi), forma esponenziale."""
    tt = np.arange(n) / SR
    return np.minimum(1, tt / max(a, 1e-4)) * np.exp(-np.maximum(0, tt - a) / d)

# --- tappeto: Re minore, caldo, lento ---
drone = np.zeros(N)
for f, g in [(73.42, 1), (110.0, .55), (146.83, .35), (174.61, .18), (220.0, .12)]:
    drone += g * np.sin(2 * np.pi * f * t + 0.4 * np.sin(2 * np.pi * 0.11 * t * g))
    drone += g * 0.5 * np.sin(2 * np.pi * f * 1.003 * t)
drone = lp(drone, 900)
shape = np.clip(t / 1.4, 0, 1) ** 1.5 * (1 + 0.35 * np.clip((t - 7.4) / 0.8, 0, 1) - 0.2 * np.clip((t - 9.3) / 1, 0, 1))
drone *= shape / np.max(np.abs(drone)) * db(-21)
L += drone; R += drone

# --- whoosh: rumore con filtro che sale e scende ---
def whoosh(dur=0.55, top=6000, seed=0):
    n = int(dur * SR); x = np.random.default_rng(seed).normal(0, 1, n)
    k = np.linspace(0, 1, n); bell = np.sin(np.pi * k) ** 2
    fc = 200 + top * bell
    y = lp(x, fc) - lp(x, fc * 0.25)
    return y * bell / (np.max(np.abs(y)) + 1e-9)

for i, c in enumerate([1.4, 3.6, 5.8, 8.0]):
    w = whoosh(seed=10 + i); add(w, c - 0.3, db(-13), pan=-0.4)
    add(whoosh(seed=20 + i), c - 0.27, db(-15), pan=0.4)

# --- colpi bassi sui numeri ---
def hit(f0=58, dur=0.9):
    n = int(dur * SR); tt = np.arange(n) / SR
    f = f0 * (1 + 1.6 * np.exp(-tt / 0.03))
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-tt / 0.28)
    click = lp(rng.normal(0, 1, n), 3000) * np.exp(-tt / 0.008) * 0.6
    y = body + click
    return y / np.max(np.abs(y))

for c in [1.55, 3.75, 5.95, 8.15]:
    add(hit(), c, db(-12))
add(hit(48, 1.2), 0.15, db(-17))   # "quattro", più morbido

# --- tick: le 27 idee che cadono ---
def tick(f=3200):
    n = int(0.05 * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.006)

for k in range(12):
    add(tick(2400 + rng.random() * 2400), 2.55 + rng.random() * 0.7, db(-26), pan=rng.uniform(-.7, .7))

# --- campanella calda: le 3 scelte si accendono ---
def bell(f=587.33, dur=1.6):
    n = int(dur * SR); tt = np.arange(n) / SR
    y = sum(g * np.sin(2 * np.pi * f * m * tt) * np.exp(-tt / (0.6 / m)) for m, g in [(1, 1), (2.01, .4), (3.02, .2)])
    return y / np.max(np.abs(y))

add(bell(), 3.0, db(-20), pan=-0.2)
add(bell(880.0), 3.08, db(-24), pan=0.2)

# --- scatti dei pezzi della tavola ---
def snap():
    n = int(0.12 * SR); tt = np.arange(n) / SR
    y = lp(rng.normal(0, 1, n), 2500) * np.exp(-tt / 0.012) + 0.7 * np.sin(2 * np.pi * 140 * tt) * np.exp(-tt / 0.04)
    return y / np.max(np.abs(y))

for b in [3.95, 4.2, 4.45, 4.65, 4.8, 4.95, 5.1, 5.3]:
    add(snap(), b + 0.12, db(-17), pan=rng.uniform(-.4, .4))

# --- penna che disegna + colore che riempie ---
n = int(1.1 * SR); x = rng.normal(0, 1, n); tt = np.arange(n) / SR
scr = (lp(x, 5000) - lp(x, 1800)) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * tt) ** 2)
scr *= np.minimum(1, tt / 0.1) * np.minimum(1, (1.1 - tt) / 0.2)
add(scr / np.max(np.abs(scr)), 5.95, db(-28))
add(whoosh(0.8, 3000, seed=40), 7.0, db(-19))

# --- riser verso il capitolo 4 ---
n = int(0.85 * SR); tt = np.arange(n) / SR; k = tt / tt[-1]
rs = np.sin(2 * np.pi * np.cumsum(300 + 900 * k ** 2) / SR) * 0.4 + lp(rng.normal(0, 1, n), 800 + 6000 * k) * 0.8
rs *= k ** 2.2
add(rs / np.max(np.abs(rs)), 7.15, db(-18))

# --- luce che attraversa il figurino ---
n = int(0.8 * SR); tt = np.arange(n) / SR; x = rng.normal(0, 1, n)
sh = (lp(x, 9000) - lp(x, 5000)) * np.sin(np.pi * tt / tt[-1]) ** 2
add(sh / np.max(np.abs(sh)), 8.45, db(-24))

# --- la camera si allontana + numeri finali ---
add(whoosh(0.8, 2500, seed=50)[::-1], 9.3, db(-17))
for i in range(4):
    add(tick(1800 + i * 300), 10.2 + i * 0.1, db(-20), pan=-0.6 + i * 0.4)

# --- riverbero leggero (stanza scura) ---
ir_n = int(0.9 * SR); ir = rng.normal(0, 1, ir_n) * np.exp(-np.arange(ir_n) / SR / 0.25); ir /= np.sqrt(np.sum(ir ** 2))
def verb(x):
    m = len(x) + ir_n
    return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[:len(x)]
L = L + 0.22 * verb(L); R = R + 0.22 * verb(R)

# --- taglio netto al nero ---
c = int(CUT * SR); L[c:] = 0; R[c:] = 0
fade = int(0.004 * SR); L[c - fade:c] *= np.linspace(1, 0, fade); R[c - fade:c] *= np.linspace(1, 0, fade)

peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
g = db(-3) / peak if peak > db(-3) else 1.0
st = (np.stack([L, R], 1) * g * 32767).astype(np.int16)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print('peak dBFS', round(20 * np.log10(peak * g), 1))
