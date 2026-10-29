"""Trova, per ogni export di Mimo, la clip originale e il punto d'inizio: confronta i contorni (non i colori, che Jacopo ha
cambiato) di 3 fotogrammi dell'export con i proxy LRF delle clip candidate, campionati a 5 fps.
uso: python -I coppie.py   -> coppie.json"""
import json, os, subprocess
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
Z = os.path.join(HERE, "..", "zanzibar")
# export -> candidati (cam, da, a), dal giorno dell'export
CAND = {"dji_export_20261023_133842": [("n", 187, 209)], "dji_export_20261023_133928": [("n", 187, 209)],
        "dji_export_20261024_155142": [("p", 77, 91), ("n", 210, 219)], "dji_export_20261027_113736": [("n", 239, 250)],
        "dji_export_20261029_150928": [("p", 153, 153)], "dji_export_20261029_151246": [("p", 7, 11)]}


def sig(img):
    g = cv2.cvtColor(cv2.resize(img, (96, 54), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
    e = np.hypot(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1))
    e -= e.mean()
    return e / (np.linalg.norm(e) + 1e-6)


def frames(path, fps):
    cap, out, i = cv2.VideoCapture(path), [], 0
    src = cap.get(cv2.CAP_PROP_FPS) or 25
    step = max(1, round(src / fps))
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        if i % step == 0:
            out.append((i / src, sig(fr)))
        i += 1
    return out


res = {}
for e in sorted(os.listdir(os.path.join(HERE, "export"))):
    key = e[:26]
    if key not in CAND:
        continue
    ef = frames(os.path.join(HERE, "export", e), 5)
    probe = [ef[len(ef) // 5], ef[len(ef) // 2], ef[4 * len(ef) // 5]]
    best = (-1, None, None)
    for cam, a, b in CAND[key]:
        d = os.path.join(Z, "pocket" if cam == "p" else "nano", "lrf")
        for f in sorted(os.listdir(d)):
            n = int(f.split("_")[2])
            if not a <= n <= b:
                continue
            sf = frames(os.path.join(d, f), 5)
            st = np.array([t for t, _ in sf])
            ss = np.stack([s for _, s in sf]).reshape(len(sf), -1)
            # offset = tempo sorgente - tempo export; ogni sonda vota, si tiene l'offset col punteggio medio piu' alto
            for te, s in probe:
                c = ss @ s.ravel()
                j = int(c.argmax())
                off = st[j] - te
                score = np.mean([(ss[np.abs(st - (tp + off)).argmin()] @ sp.ravel()) for tp, sp in probe])
                if score > best[0]:
                    best = (float(score), "%s%04d" % (cam, n), float(off))
    res[e] = {"clip": best[1], "offset": round(best[2], 2), "score": round(best[0], 3)}
    print(e, res[e], flush=True)
json.dump(res, open(os.path.join(HERE, "coppie.json"), "w"), indent=1)
