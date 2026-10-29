"""Misura cosa fa Jacopo in Mimo: per ogni coppia (originale con la LUT DJI ufficiale / suo export) confronta 12 fotogrammi
alla stessa ora: luce (percentili), saturazione per zona (mare-cielo, verde, pelle), colore dei bianchi, nitidezza.
Salva anche le coppie di pixel (per imparare la LUT) in work/pixel.npz.
uso: python -I misura.py"""
import csv, json, os, subprocess
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
Z = os.path.join(HERE, "..", "zanzibar")
LUTS = os.path.join(HERE, "..", "..", ".claude", "skills", "youtube-edit", "assets", "luts")
SM = os.path.join(HERE, "..", "..", "personale", "reel-zanzibar", "smistamento")
LUT = {"D-Log": "DJI-Pocket4P-DLog-to-Rec709-V2.0-size33.cube", "D-Log2": "DJI-Pocket4P-DLog2-to-Rec709-size65.cube",
       "D-Log M": "DJI-OsmoNano-DLogM-to-Rec709-V1.cube"}
inv = {c: {r["id"].split("_")[2]: r for r in csv.DictReader(open(os.path.join(SM, f), encoding="utf-8"))}
       for c, f in (("p", "inventario-pocket.csv"), ("n", "inventario-nano.csv"))}
pairs = json.load(open(os.path.join(HERE, "coppie.json")))
os.makedirs(os.path.join(HERE, "work"), exist_ok=True)


def grab(path, t, vf=""):
    vf = (vf + "," if vf else "") + "scale=960:540:flags=area"
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", "%.3f" % t, "-i", path, "-frames:v", "1", "-vf", vf, "-f", "rawvideo",
                        "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(p, np.uint8).reshape(540, 960, 3).astype(np.float32) / 255


def sharp(path, t, vf=""):  # nitidezza a piena risoluzione su un ritaglio centrale 1280x720
    vf = (vf + "," if vf else "") + "crop=1280:720"
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", "%.3f" % t, "-i", path, "-frames:v", "1", "-vf", vf + ",format=gray",
                        "-f", "rawvideo", "-"], capture_output=True).stdout
    return cv2.Laplacian(np.frombuffer(p, np.uint8).reshape(720, 1280).astype(np.float32), cv2.CV_32F).var()


def zones(rgb):
    hsv = cv2.cvtColor((rgb * 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    h, s, v = hsv[..., 0] * 2, hsv[..., 1] / 255, hsv[..., 2] / 255
    ok = (s > 0.15) & (v > 0.15)
    return {"mare-cielo": ok & (h >= 170) & (h < 250), "verde": ok & (h >= 70) & (h < 170), "pelle-caldi": ok & ((h < 45) | (h >= 330))}, s


rows, P_src, P_dst = [], [], []
for e, m in pairs.items():
    cam, n = m["clip"][0], m["clip"][1:]
    row = inv[cam][n]
    prof = row["gamma"] if cam == "p" else (None if row["giorno"] == "23/10" else "D-Log M")
    d = os.path.join(Z, "pocket" if cam == "p" else "nano", "mp4")
    src = os.path.join(d, next(x for x in sorted(os.listdir(d)) if "_%s_" % n in x))
    exp = os.path.join(HERE, "export", e)
    vf = ("lut3d=file='%s'" % os.path.join(LUTS, LUT[prof]).replace("\\", "/").replace(":", "\\:")) if prof else ""
    dur = float(row["dur"])
    st = {"src": [], "dst": []}
    for k in range(12):
        t = dur * (k + 0.5) / 12
        a, b = grab(src, t + m["offset"], vf), grab(exp, t)
        st["src"].append(a)
        st["dst"].append(b)
        if k % 3 == 0:
            idx = np.random.default_rng(k).choice(960 * 540, 6000, replace=False)
            P_src.append(a.reshape(-1, 3)[idx]); P_dst.append(b.reshape(-1, 3)[idx])
    A, B = np.stack(st["src"]), np.stack(st["dst"])
    ya, yb = A @ [0.2126, 0.7152, 0.0722], B @ [0.2126, 0.7152, 0.0722]
    q = [1, 5, 25, 50, 75, 95, 99]
    r = {"export": e[11:26], "clip": m["clip"], "profilo": prof or "normale",
         "luce_src": np.percentile(ya, q).round(3).tolist(), "luce_suo": np.percentile(yb, q).round(3).tolist()}
    za, sa = zones(A.reshape(-1, 960, 3)); zb, sb = zones(B.reshape(-1, 960, 3))
    r["sat_tot"] = round(float(sb.mean() / sa.mean()), 2)
    for z in za:
        mask = za[z] | zb[z]
        if mask.mean() > 0.02:
            r["sat_" + z] = round(float(sb[mask].mean() / max(sa[mask].mean(), 1e-3)), 2)
    wa, wb = A.reshape(-1, 3)[ya.ravel() > np.percentile(ya, 97)], B.reshape(-1, 3)[yb.ravel() > np.percentile(yb, 97)]
    r["bianchi_src_RGB"] = (wa.mean(0) / wa.mean()).round(3).tolist()
    r["bianchi_suo_RGB"] = (wb.mean(0) / wb.mean()).round(3).tolist()
    r["nitidezza_suo/src"] = round(float(sharp(exp, dur / 2) / sharp(src, dur / 2 + m["offset"], vf)), 2)
    rows.append(r)
    print(json.dumps(r, ensure_ascii=False), flush=True)
json.dump(rows, open(os.path.join(HERE, "misure.json"), "w"), indent=1, ensure_ascii=False)
np.savez_compressed(os.path.join(HERE, "work", "pixel.npz"), src=np.concatenate(P_src), dst=np.concatenate(P_dst))
