"""Per ogni clip trova la finestra di N secondi col movimento di camera piu' pulito (dai proxy LRF).
Misura per fotogramma lo spostamento dell'immagine; "sporco" = tremolio + cambi di velocita'/direzione (gli assestamenti
dell'inquadratura). Stampa il profilo secondo per secondo e la finestra migliore.
uso: python -I finestre.py DURATA p0128 p0075 n0196 ...   (DURATA in secondi)"""
import os, sys
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
Z = os.path.join(HERE, "..")
dur = float(sys.argv[1])
for tag in sys.argv[2:]:
    cam, n = tag[0], tag[1:]
    d = os.path.join(Z, "pocket" if cam == "p" else "nano", "lrf")
    f = os.path.join(d, next(x for x in sorted(os.listdir(d)) if "_%s_" % n in x))
    cap = cv2.VideoCapture(f)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    prev, v = None, []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(cv2.resize(fr, (320, 180)), cv2.COLOR_BGR2GRAY).astype(np.float32)
        if prev is not None:
            v.append(cv2.phaseCorrelate(prev, g)[0])
        prev = g
    v = np.array(v)
    k = np.ones(13) / 13
    sm = np.stack([np.convolve(v[:, i], k, mode="same") for i in (0, 1)], 1)
    jit = np.linalg.norm(v - sm, axis=1)
    acc = np.r_[0, np.linalg.norm(np.diff(sm, axis=0), axis=1)] * 10
    dirt = jit + acc
    sec = int(len(v) / fps)
    prof = " ".join("%d:%.1f" % (s, dirt[int(s * fps):int((s + 1) * fps)].mean()) for s in range(sec))
    w = int(dur * fps)
    best = min(range(0, max(1, len(v) - w)), key=lambda i: dirt[i:i + w].mean())
    speed = np.linalg.norm(sm[best:best + w], axis=1).mean()
    print("%s  migliore %.1f-%.1f s  sporco %.2f  velocita %.2f\n   %s" % (tag, best / fps, (best + w) / fps, dirt[best:best + w].mean(), speed, prof), flush=True)
