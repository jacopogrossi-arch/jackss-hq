"""Light leak procedurali per il Reel «Le 3 misure» (24/11/2026): strisce di luce calda (arancio/rosso, nucleo giallo caldo) che attraversano il quadro e si spengono,
sui tagli. Sequenza di PNG RGB 540x960 su nero (mescolata in 'screen' sopra il video da assemble.sh) -> videos/_bench/reel-3-misure/leaks/l0001.png ...
Eventi: grande sul cambio 2 -> 1 pantaloni (3.24 s), medi sui cambi di blocco, piccoli sui tagli dentro i blocchi.
Uso: python -I leaks.py
"""
import numpy as np, os
from PIL import Image
W, H = 540, 960; FPS = 24; NFR = 787
OUT = "D:/ClaudeCodeTest/videos/_bench/reel-3-misure/leaks/"; os.makedirs(OUT, exist_ok=True)
EVENTS = [(3.24, "big"), (6.75, "big"), (12.38, "big"), (18.12, "big"), (23.15, "big"), (29.33, "big"), (9.00, "small"), (15.10, "small"), (20.30, "small"), (26.20, "small")]
# Transizione a TUTTO SCHERMO: la luce sale fino a coprire il quadro (il taglio avviene al picco, nascosto) e poi si dissolve.
KIND = {"big": dict(rise=0.42, fall=0.58, power=1.0), "small": dict(rise=0.20, fall=0.34, power=0.85)}
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); xx /= W; yy /= H
def lowfreq_noise(seed, shape=(7, 5)):
    r = np.random.default_rng(seed).random(shape).astype(np.float32)
    return np.asarray(Image.fromarray((r * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), dtype=np.float32) / 255.0
def ease_in(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def frame_for(t):
    out = np.zeros((H, W, 3), np.float32)
    for i, (tc, kind) in enumerate(EVENTS):
        k = KIND[kind]; a = t - tc
        if a < -k["rise"] or a > k["fall"]: continue
        E = ease_in((a + k["rise"]) / k["rise"]) if a < 0 else (1 - ease_in(a / k["fall"])) ** 1.3
        u = (a + k["rise"]) / (k["rise"] + k["fall"]); d = 1 if i % 2 == 0 else -1
        field = np.zeros((H, W), np.float32)
        for j in range(3):                                   # bagliori larghi che scorrono, tutto il quadro resta coperto
            cx = (-0.2 + 1.4 * u if d > 0 else 1.2 - 1.4 * u) + 0.25 * (j - 1); cy = 0.3 + 0.2 * j + 0.1 * np.sin(5 * u + j)
            field += np.exp(-(((xx - cx) / 0.55) ** 2 + ((yy - cy) / 0.75) ** 2))
        field = field / max(float(field.max()), 1e-6)
        n = lowfreq_noise(200 + i)
        I = E * k["power"] * (0.62 + 0.38 * field) * (0.82 + 0.3 * n)          # base che copre tutto + strisce piu' luminose
        r = np.clip(I * 1.28, 0, 1.0); g = np.clip(I ** 1.7 * 0.96, 0, 0.95); b = np.clip(I ** 3.4 * 0.5, 0, 0.5)
        out = np.maximum(out, np.stack([r, g, b], -1))
    return out
if __name__ == "__main__":
    blank = Image.new("RGB", (W, H), (0, 0, 0)); blank.save(OUT + "blank.png"); import shutil
    for f in range(1, NFR + 1):
        t = (f - 1) / FPS
        if not any(-KIND[e[1]]["rise"] - 0.03 <= t - e[0] <= KIND[e[1]]["fall"] + 0.03 for e in EVENTS): shutil.copyfile(OUT + "blank.png", OUT + "l%04d.png" % f); continue
        Image.fromarray((np.clip(frame_for(t), 0, 1) * 255).astype(np.uint8)).save(OUT + "l%04d.png" % f)
    print("fatto")
