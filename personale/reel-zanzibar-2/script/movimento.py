"""Movimento di camera di ogni clip (dai proxy LRF): velocita' media e tremolio, per trovare le clip con un movimento fluido.
velocita' = spostamento medio dell'immagine (pixel per fotogramma su 320 px di larghezza)
tremolio  = quanto il movimento si discosta dalla sua media mobile (0,5 s): alto = mosso a mano / scatti
uso: python -I movimento.py   -> work/movimento.csv"""
import csv, os
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
Z = os.path.join(HERE, "..")
out = os.path.join(HERE, "work", "movimento.csv")
rows = []
for cam, folder in (("p", "pocket"), ("n", "nano")):
    d = os.path.join(Z, folder, "lrf")
    for f in sorted(os.listdir(d)):
        cap = cv2.VideoCapture(os.path.join(d, f))
        prev, v = None, []
        while True:
            ok, fr = cap.read()
            if not ok:
                break
            g = cv2.cvtColor(cv2.resize(fr, (320, 180)), cv2.COLOR_BGR2GRAY).astype(np.float32)
            if prev is not None:
                (dx, dy), _ = cv2.phaseCorrelate(prev, g)
                v.append((dx, dy))
            prev = g
        if len(v) < 15:
            continue
        v = np.array(v)
        k = np.ones(13) / 13
        sm = np.stack([np.convolve(v[:, i], k, mode="same") for i in (0, 1)], 1)
        speed = float(np.linalg.norm(sm, axis=1)[6:-6].mean())
        jitter = float(np.linalg.norm(v - sm, axis=1)[6:-6].mean())
        kind = "fermo" if speed < 0.15 and jitter < 0.25 else ("fluido" if jitter < 0.35 + 0.15 * speed else "mosso")
        n = f.split("_")[2]
        rows.append([cam + n, round(speed, 2), round(jitter, 2), kind, round(len(v) / 25, 1)])
        print(rows[-1], flush=True)
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["clip", "velocita", "tremolio", "tipo", "durata"])
    w.writerows(rows)
