"""Effetti + tappeto per la clip Impaginazione, a tempo con la trascrizione (48 kHz stereo)."""
import numpy as np, wave, sys

SR = 48000; DUR = 13.0; N = int(SR * DUR); t = np.arange(N) / SR
rng = np.random.default_rng(5)
L = np.zeros(N); R = np.zeros(N)
db = lambda x: 10 ** (x / 20)
T = dict(imp=2.42, claude=5.44, mcp=7.24, canva=8.52, coll=9.46, giu=10.86)

def lp(x, fc):
    fc = np.broadcast_to(fc, x.shape); a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y

def add(sig, start, gain, pan=0.0):
    i = int(start * SR); j = min(N, i + len(sig))
    if i < 0: sig = sig[-i:]; i = 0
    L[i:j] += sig[:j - i] * gain * (1 - pan) ** .5; R[i:j] += sig[:j - i] * gain * (1 + pan) ** .5

def norm(y): return y / (np.max(np.abs(y)) + 1e-9)

def whoosh(dur=.5, top=6000, seed=0):
    n = int(dur * SR); x = np.random.default_rng(seed).normal(0, 1, n); k = np.linspace(0, 1, n)
    bell = np.sin(np.pi * k) ** 2; fc = 200 + top * bell
    return norm((lp(x, fc) - lp(x, fc * .25)) * bell)

def hit(f0=58, dur=.9):
    n = int(dur * SR); tt = np.arange(n) / SR; f = f0 * (1 + 1.6 * np.exp(-tt / .03))
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .28) + lp(rng.normal(0, 1, n), 3000) * np.exp(-tt / .008) * .6)

def tick(f=3000):
    n = int(.05 * SR); tt = np.arange(n) / SR; return np.sin(2 * np.pi * f * tt) * np.exp(-tt / .006)

def snap():
    n = int(.12 * SR); tt = np.arange(n) / SR
    return norm(lp(rng.normal(0, 1, n), 2500) * np.exp(-tt / .012) + .7 * np.sin(2 * np.pi * 140 * tt) * np.exp(-tt / .04))

# tappeto basso, sale sull'inserto e cala quando torni a camera
drone = sum(g * np.sin(2 * np.pi * f * t) + g * .5 * np.sin(2 * np.pi * f * 1.003 * t) for f, g in [(73.42, 1), (110, .55), (146.83, .3), (220, .1)])
drone = lp(drone, 800)
shape = .45 * np.clip((t - 1.8) / 1, 0, 1) + .55 * np.clip((t - T['claude'] + .2) / .6, 0, 1) - .7 * np.clip((t - T['giu']) / 1.6, 0, 1)
drone = norm(drone) * np.clip(shape, 0, 1) * db(-30)
L += drone; R += drone

add(hit(), T['imp'] - .02, db(-16))                                    # "impaginazione"
add(whoosh(.45, 6500, 1), T['claude'] - .4, db(-15), -.4); add(whoosh(.45, 6500, 2), T['claude'] - .37, db(-17), .4)
add(hit(52, 1.1), T['claude'] + .02, db(-17))                          # logo Claude
add(tick(2600), T['mcp'] + .02, db(-22))                               # MCP
add(snap(), T['canva'] + .04, db(-15)); add(hit(70, .5), T['canva'] + .04, db(-22))
add(whoosh(.7, 4000, 3), T['coll'] - .25, db(-20))                     # impulso sulla linea
for i in range(5): add(tick(2000 + i * 350), T['coll'] + .55 + i * .09, db(-27), -.5 + i * .25)
add(snap(), T['coll'] + .62, db(-17))
add(whoosh(.55, 3000, 4)[::-1], T['giu'] - .15, db(-16))               # lo schermo scende

out = np.stack([L, R], 1)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
print('sfx ok')
