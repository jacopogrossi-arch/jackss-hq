"""Impara il look di Jacopo dalle coppie del Pocket D-Log: colore dopo la LUT DJI -> colore del suo export di Mimo.
Modello: polinomio di 3o grado sui tre canali (liscio, generalizza bene), stimato con i minimi quadrati e un po' di
regolarizzazione. Verifica su fotogrammi diversi da quelli usati per imparare. Scrive look-jacopo.cube (33 punti, Rec.709).
uso: python -I impara.py"""
import itertools, json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
pairs = list(json.load(open(os.path.join(HERE, "coppie.json"))).values())
d = np.load(os.path.join(HERE, "work", "pixel.npz"))
per = len(d["src"]) // len(pairs)
pocket = [i for i, p in enumerate(pairs) if p["clip"][0] == "p"]


def feats(x):
    cols = [np.ones(len(x))]
    for deg in (1, 2, 3):
        for c in itertools.combinations_with_replacement(range(3), deg):
            cols.append(np.prod(x[:, list(c)], axis=1))
    return np.stack(cols, 1)


def fit(src, dst, lam=1e-3):
    F = feats(src)
    return np.linalg.solve(F.T @ F + lam * len(F) * np.eye(F.shape[1]), F.T @ dst)


S = np.concatenate([d["src"][i * per:(i + 1) * per] for i in pocket])
D = np.concatenate([d["dst"][i * per:(i + 1) * per] for i in pocket])
# verifica: impara su 3 fotogrammi su 4 di ogni clip, misura sul quarto (fotogrammi diversi, momenti diversi della clip)
fr = per // 4
test = np.zeros(len(S), bool)
for k in range(len(pocket)):
    test[k * per + 3 * fr:(k + 1) * per] = True
W = fit(S[~test], D[~test])
err = lambda a, b: float(np.abs(a - b).mean() * 255)
print("errore medio (su 255) su fotogrammi mai visti: solo LUT DJI %.1f  ->  look imparato %.1f" %
      (err(S[test], D[test]), err(np.clip(feats(S[test]) @ W, 0, 1), D[test])))
W = fit(S, D)
n = 33
g = np.linspace(0, 1, n)
b, gg, r = np.meshgrid(g, g, g, indexing="ij")  # .cube: il rosso varia piu' in fretta
grid = np.stack([r.ravel(), gg.ravel(), b.ravel()], 1)
out = np.clip(feats(grid) @ W, 0, 1)
with open(os.path.join(HERE, "look-jacopo.cube"), "w") as f:
    f.write('TITLE "look Jacopo (Mimo), imparato il 29/10/2026 da 3 coppie Pocket D-Log"\nLUT_3D_SIZE %d\n' % n)
    f.writelines("%.6f %.6f %.6f\n" % tuple(v) for v in out)
print("ok look-jacopo.cube")
