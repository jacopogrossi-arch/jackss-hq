"""Il look di Jacopo come ricetta a manopole (come in Mimo), regolate in automatico sui suoi export del Pocket D-Log.
Manopole: curva della luce (uscita a 0,05 0,25 0,5 0,75 0,95 dell'ingresso, uguale sui tre canali), saturazione generale,
saturazione in piu' per blu/turchese, verde, caldi (finestre di tinta morbide). Lavora sul colore dopo la LUT DJI.
Verifica "lascia fuori una clip", poi scrive look-jacopo-ricetta.cube (33 punti) e ricetta.json.
uso: python -I ricetta.py"""
import json, os
import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
pairs = list(json.load(open(os.path.join(HERE, "coppie.json"))).values())
d = np.load(os.path.join(HERE, "work", "pixel.npz"))
per = len(d["src"]) // len(pairs)
pocket = [i for i, p in enumerate(pairs) if p["clip"][0] == "p"]
XS = np.array([0, 0.05, 0.25, 0.5, 0.75, 0.95, 1.0])
KR, KB = 0.2126, 0.0722


def win(h, c, w):  # finestra di tinta morbida (gradi), 1 al centro, 0 oltre w
    dd = np.abs((h - c + 180) % 360 - 180)
    return np.clip(1 - dd / w, 0, 1) ** 2


def apply(x, p):
    ys = np.r_[0, np.clip(p[:5], 0, 1), 1]
    x = np.interp(x, XS, ys)
    y = x @ [KR, 1 - KR - KB, KB]
    cb, cr = (x[:, 2] - y) / (2 * (1 - KB)), (x[:, 0] - y) / (2 * (1 - KR))
    h = np.degrees(np.arctan2(cr, cb)) % 360
    # tinte nel piano Cb/Cr: blu-turchese ~ 340-30 (Cb alto), verde ~ 225, caldi/pelle ~ 110
    k = p[5] * (1 + p[6] * np.maximum(win(h, 355, 70), 0) + p[7] * win(h, 225, 55) + p[8] * win(h, 110, 50))
    cb, cr = cb * k, cr * k
    r = y + 2 * (1 - KR) * cr
    b = y + 2 * (1 - KB) * cb
    g = (y - KR * r - KB * b) / (1 - KR - KB)
    return np.clip(np.stack([r, g, b], 1), 0, 1)


P0 = np.r_[0.05, 0.25, 0.5, 0.75, 0.95, 1.0, 0, 0, 0]


def fit(S, D):
    rng = np.random.default_rng(0)
    i = rng.choice(len(S), min(30000, len(S)), replace=False)
    f = lambda p: np.abs(apply(S[i], p) - D[i]).mean() + 0.02 * np.abs(np.diff(np.r_[0, p[:5], 1]) < 0).sum()
    return minimize(f, P0, method="Powell", options={"maxiter": 4000, "xtol": 1e-3, "ftol": 1e-5}).x


clip = lambda k: (d["src"][k * per:(k + 1) * per], d["dst"][k * per:(k + 1) * per])
for k in pocket:
    tr = [i for i in pocket if i != k]
    p = fit(np.concatenate([clip(i)[0] for i in tr]), np.concatenate([clip(i)[1] for i in tr]))
    s, t = clip(k)
    print("%s mai vista: solo LUT %.1f -> ricetta %.1f" % (pairs[k]["clip"], np.abs(s - t).mean() * 255, np.abs(apply(s, p) - t).mean() * 255), flush=True)
p = fit(np.concatenate([clip(i)[0] for i in pocket]), np.concatenate([clip(i)[1] for i in pocket]))
names = ["curva 0,05", "curva 0,25", "curva 0,50", "curva 0,75", "curva 0,95", "saturazione", "blu-turchese", "verde", "caldi-pelle"]
rec = {n: round(float(v), 3) for n, v in zip(names, p)}
print(json.dumps(rec, ensure_ascii=False))
json.dump(rec, open(os.path.join(HERE, "ricetta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n = 33
g = np.linspace(0, 1, n)
b, gg, r = np.meshgrid(g, g, g, indexing="ij")
out = apply(np.stack([r.ravel(), gg.ravel(), b.ravel()], 1), p)
with open(os.path.join(HERE, "look-jacopo-ricetta.cube"), "w") as f:
    f.write('TITLE "look Jacopo (Mimo), ricetta a manopole, 29/10/2026"\nLUT_3D_SIZE %d\n' % n)
    f.writelines("%.6f %.6f %.6f\n" % tuple(v) for v in out)
print("ok look-jacopo-ricetta.cube")
