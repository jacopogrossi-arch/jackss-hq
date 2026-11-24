"""Light leak procedurali per il Reel «Le 3 misure» (24/11/2026): strisce di luce calda (arancio/rosso, nucleo giallo caldo) che attraversano il quadro e si spengono,
sui tagli. Sequenza di PNG RGB 540x960 su nero (mescolata in 'screen' sopra il video da assemble.sh) -> videos/_bench/reel-3-misure/leaks/l0001.png ...
Eventi: grande sul cambio 2 -> 1 pantaloni (3.24 s), medi sui cambi di blocco, piccoli sui tagli dentro i blocchi.
Uso: python -I leaks.py
"""
import numpy as np, os
from PIL import Image
W, H = 540, 960; FPS = 24; NFR = 787
OUT = "D:/ClaudeCodeTest/videos/_bench/reel-3-misure/leaks/"; os.makedirs(OUT, exist_ok=True)
EVENTS = [(3.24, "big"), (6.75, "mid"), (12.38, "mid"), (18.12, "mid"), (23.15, "mid"), (29.33, "mid"), (9.00, "small"), (15.10, "small"), (20.30, "small"), (26.20, "small")]
KIND = {"big": dict(dur=0.95, peak=0.62, rise=0.08, sig=0.42), "mid": dict(dur=0.70, peak=0.44, rise=0.07, sig=0.34), "small": dict(dur=0.38, peak=0.28, rise=0.05, sig=0.28)}
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); xx /= W; yy /= H
rng = np.random.default_rng(7)
def lowfreq_noise(seed):
    r = np.random.default_rng(seed).random((6, 4)).astype(np.float32)
    return np.asarray(Image.fromarray((r * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), dtype=np.float32) / 255.0
def frame_for(t):
    out = np.zeros((H, W, 3), np.float32)
    for i, (tc, kind) in enumerate(EVENTS):
        k = KIND[kind]; a = t - (tc - 0.03)             # il leak parte un soffio prima del taglio
        if a < 0 or a > k["dur"]: continue
        env = a / k["rise"] if a < k["rise"] else (1 - (a - k["rise"]) / (k["dur"] - k["rise"])) ** 1.7
        u = a / k["dur"]; d = 1 if i % 2 == 0 else -1
        field = np.zeros((H, W), np.float32)
        for j in range(3):                                 # tre bagliori che scorrono in diagonale
            cx = (-0.15 + 1.3 * u if d > 0 else 1.15 - 1.3 * u) + 0.12 * j; cy = 0.25 + 0.25 * j + 0.1 * np.sin(6 * u + j)
            field += np.exp(-(((xx - cx) / (k["sig"] * 0.55)) ** 2 + ((yy - cy) / (k["sig"] * 1.1)) ** 2))
        field *= 0.55 + 0.9 * lowfreq_noise(100 + i)       # macchie irregolari
        field = np.clip(field * env * k["peak"], 0, 1.2)
        # colore: bordo rosso/arancio, nucleo giallo caldo
        r = np.clip(field * 1.1, 0, 0.95); g = np.clip(field ** 2.0 * 0.62, 0, 0.7); b = np.clip(field ** 3.8 * 0.30, 0, 0.4)
        out = np.maximum(out, np.stack([r, g, b], -1))
    return out
if __name__ == "__main__":
    blank = Image.new("RGB", (W, H), (0, 0, 0)); blank.save(OUT + "blank.png"); import shutil
    for f in range(1, NFR + 1):
        t = (f - 1) / FPS
        if not any(-0.04 <= t - e[0] <= KIND[e[1]]["dur"] + 0.02 for e in EVENTS): shutil.copyfile(OUT + "blank.png", OUT + "l%04d.png" % f); continue
        Image.fromarray((np.clip(frame_for(t), 0, 1) * 255).astype(np.uint8)).save(OUT + "l%04d.png" % f)
    print("fatto")
