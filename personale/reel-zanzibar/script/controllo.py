"""Controllo clip per clip del reel: per ogni inquadratura 3 fotogrammi (inizio, meta', fine del pezzo usato) col colore
nuovo (graded.mp4 + contrasto + ritocchi), misure (luce, luci bruciate, neri chiusi, nitidezza, rumore) e due fogli:
  scelta/controllo-dettaglio.jpg  3 fotogrammi per clip (per guardare i difetti)
  scelta/prima-dopo-1.jpg / -2.jpg  il render approvato vs il colore nuovo, a meta' di ogni clip
uso: python -I controllo.py"""
import io, json, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf-8"))
GRADE = "curves=all='0/0 0.25/0.21 0.5/0.5 0.75/0.79 1/1',eq=saturation=1.12"
OLD = os.path.join(HERE, "zanzibar-reel_4k.mp4")
F = ImageFont.load_default(size=26)


def frame(path, t, vf):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", "%.3f" % t, "-i", path, "-frames:v", "1", "-vf", vf,
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    return Image.open(io.BytesIO(p)).convert("RGB")


def measure(img):
    a = np.asarray(img.resize((960, 540))).astype(np.float32) / 255
    y = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    g = np.asarray(img.convert("L").resize((960, 540)), np.float32)
    lap = np.abs(g[1:-1, 1:-1] * 4 - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:])
    flat = np.abs(np.asarray(img.convert("L").resize((960, 540)).filter(ImageFilter.GaussianBlur(2)), np.float32) - g)
    return {"luce": float(np.median(y)), "p99": float(np.percentile(y, 99.5)), "bruciato": float((a.max(-1) > 0.985).mean()),
            "chiuso": float((y < 0.02).mean()), "nitidezza": float(lap.mean()), "rumore": float(np.median(flat))}


def label(img, txt, w):
    img = img.resize((w, w * 9 // 16))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 14 + F.getlength(txt), 36), fill=(0, 0, 0))
    d.text((7, 4), txt, font=F, fill=(255, 220, 0))
    return img


rows, pairs, report = [], [], []
for i, s in enumerate(cfg["shots"]):
    a, b = cfg["cuts"][i], cfg["cuts"][i + 1]
    graded = os.path.join(HERE, "work", "shots", "%02d-%s" % (i + 1, s["id"]), "grade", "graded.mp4")
    vf = "scale=1920:1080," + GRADE + ("," + s["extra"] if s.get("extra") else "")
    times = [0.15, (b - a) / 2, (b - a) - 0.15]
    imgs = [frame(graded, t, vf) for t in times]
    m = [measure(x) for x in imgs]
    avg = {k: round(float(np.mean([x[k] for x in m])), 3) for k in m[0]}
    avg["bruciato_max"] = round(max(x["bruciato"] for x in m), 4)
    report.append({"n": i + 1, "id": s["id"], "cosa": s["cosa"], **avg})
    rows.append([label(x, "%d · %s  %s" % (i + 1, s["id"], ("inizio", "meta'", "fine")[k]), 640) for k, x in enumerate(imgs)])
    old = frame(OLD, a + (b - a) / 2, "scale=1920:1080")
    pairs.append((label(old, "%d · %s  PRIMA" % (i + 1, s["id"]), 640), label(imgs[1], "%d · %s  DOPO" % (i + 1, s["id"]), 640)))

det = Image.new("RGB", (640 * 3, 360 * len(rows)))
for r, row in enumerate(rows):
    for k, x in enumerate(row):
        det.paste(x, (k * 640, r * 360))
det.save(os.path.join(HERE, "scelta", "controllo-dettaglio.jpg"), quality=80)
half = (len(pairs) + 1) // 2
for part, chunk in enumerate((pairs[:half], pairs[half:]), 1):
    sh = Image.new("RGB", (1280, 360 * len(chunk)))
    for r, (o, n) in enumerate(chunk):
        sh.paste(o, (0, r * 360))
        sh.paste(n, (640, r * 360))
    sh.save(os.path.join(HERE, "scelta", "prima-dopo-%d.jpg" % part), quality=78)
json.dump(report, open(os.path.join(HERE, "work", "controllo.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("%-3s %-5s %6s %6s %9s %7s %9s %7s" % ("n", "clip", "luce", "p99.5", "bruciato%", "chiuso%", "nitidezza", "rumore"))
for r in report:
    print("%-3d %-5s %6.2f %6.2f %9.2f %7.2f %9.1f %7.2f" % (r["n"], r["id"], r["luce"], r["p99"], 100 * r["bruciato_max"],
                                                          100 * r["chiuso"], r["nitidezza"], r["rumore"]))
