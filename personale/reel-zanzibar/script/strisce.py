"""Una striscia di 8 fotogrammi per clip, con il secondo scritto sopra. uso: python -I strisce.py CARTELLA_CLIP OUT.jpg NNNN [NNNN ...]"""
import os, subprocess, sys, json
from PIL import Image, ImageDraw, ImageFont

src, out, ids = sys.argv[1], sys.argv[2], sys.argv[3:]
font = ImageFont.load_default(size=18)
rows = []
for n in ids:
    f = next(os.path.join(src, x) for x in sorted(os.listdir(src)) if "_%s_" % n in x)
    d = float(json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", f],
                                        capture_output=True, text=True).stdout)["format"]["duration"])
    row = Image.new("RGB", (8 * 240, 135))
    dr = ImageDraw.Draw(row)
    for k in range(8):
        t = d * (k + 0.5) / 8
        p = subprocess.run(["ffmpeg", "-v", "error", "-ss", "%.2f" % t, "-i", f, "-frames:v", "1", "-vf", "scale=240:135",
                            "-f", "image2pipe", "-vcodec", "ppm", "-"], capture_output=True).stdout
        if p:
            import io
            row.paste(Image.open(io.BytesIO(p)), (k * 240, 0))
        dr.text((k * 240 + 4, 4), "%s  %.1fs" % (n, t), fill=(255, 255, 0), font=font)
    rows.append(row)
sheet = Image.new("RGB", (8 * 240, 135 * len(rows)))
for i, r in enumerate(rows):
    sheet.paste(r, (0, i * 135))
sheet.save(out, quality=82)
