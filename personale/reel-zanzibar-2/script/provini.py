"""Foglio provini: per ogni clip 6 fotogrammi dall'originale 4K, gia' con la LUT giusta (D-Log, D-Log2, D-Log M o nessuna).
Le clip usate nel primo reel sono segnate in rosso "R1".
uso: python -I provini.py OUT.jpg "Titolo capitolo" p0075 p0079 n0191 ...   (p = Pocket, n = Nano)"""
import csv, io, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
Z = os.path.join(HERE, "..")
LUTS = os.path.join(HERE, "..", "..", "..", ".claude", "skills", "youtube-edit", "assets", "luts")
SM = os.path.join(HERE, "..", "..", "..", "personale", "reel-zanzibar", "smistamento")
LUT = {"D-Log": "DJI-Pocket4P-DLog-to-Rec709-V2.0-size33.cube", "D-Log2": "DJI-Pocket4P-DLog2-to-Rec709-size65.cube",
       "D-Log M": "DJI-OsmoNano-DLogM-to-Rec709-V1.cube"}
R1 = {"0008", "0017", "0042", "0041", "0070", "0052", "0083", "0108", "0112", "0116", "0124", "0117", "0158", "0085", "0072", "0138", "0129"}
W, H, K = 320, 180, 6


def inventory(name):
    return {r["id"].split("_")[2]: r for r in csv.DictReader(open(os.path.join(SM, name), encoding="utf-8"))}


inv = {"p": inventory("inventario-pocket.csv"), "n": inventory("inventario-nano.csv")}


def profile(cam, n, row):
    if cam == "p":
        return row["gamma"]
    return None if row["giorno"] == "23/10" else "D-Log M"  # Nano: il 23/10 colori normali, dal 24/10 D-Log M


out, title, ids = sys.argv[1], sys.argv[2], sys.argv[3:]
font, big = ImageFont.load_default(size=17), ImageFont.load_default(size=26)
rows = []
for tag in ids:
    cam, n = tag[0], tag[1:]
    row = inv[cam][n]
    d = os.path.join(Z, "pocket" if cam == "p" else "nano", "mp4")
    f = os.path.join(d, next(x for x in sorted(os.listdir(d)) if "_%s_" % n in x))
    prof = profile(cam, n, row)
    lut = LUT.get(prof)
    dur = float(row["dur"])
    vf = "scale=%d:%d" % (W, H)
    if lut:
        vf = "lut3d='%s',%s" % (os.path.join(LUTS, lut).replace("\\", "/").replace(":", "\\:"), vf)
    strip = Image.new("RGB", (K * W, H))
    dr = ImageDraw.Draw(strip)
    for k in range(K):
        t = dur * (k + 0.5) / K
        p = subprocess.run(["ffmpeg", "-v", "error", "-ss", "%.2f" % t, "-i", f, "-frames:v", "1", "-vf", vf,
                            "-f", "image2pipe", "-vcodec", "ppm", "-"], capture_output=True).stdout
        if p:
            strip.paste(Image.open(io.BytesIO(p)).convert("RGB"), (k * W, 0))
        dr.text((k * W + 5, H - 22), "%.1fs" % t, fill=(255, 255, 0), font=font)
    label = "%s %s  %s  %.0fs  %sfps" % ("POCKET" if cam == "p" else "NANO", n, prof or "normale", dur, row["fps"])
    dr.rectangle((0, 0, 9 * len(label) + 10, 24), fill=(0, 0, 0))
    dr.text((5, 3), label, fill=(255, 255, 255), font=font)
    if n in R1 and cam == "p":
        dr.rectangle((K * W - 50, 0, K * W, 28), fill=(200, 0, 0))
        dr.text((K * W - 42, 2), "R1", fill=(255, 255, 255), font=big)
    rows.append(strip)
    print(tag, prof, flush=True)
sheet = Image.new("RGB", (K * W, 44 + H * len(rows)), (20, 20, 20))
ImageDraw.Draw(sheet).text((10, 8), title, fill=(255, 255, 255), font=big)
for i, r in enumerate(rows):
    sheet.paste(r, (0, 44 + i * H))
sheet.save(out, quality=85)
