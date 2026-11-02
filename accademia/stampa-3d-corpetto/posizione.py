"""Immagine 'dove sta il modulo sul figurino': figurino intero + zoom sul busto con un modulo evidenziato."""
import math
import sys
from PIL import Image, ImageDraw, ImageFont

SRC = "figurino-corretto.webp"
CX, CY, R = (int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (322, 600, 78)
BOX = (420, 280, 640, 700)
K = 3

im = Image.open(SRC).convert("RGB")
zoom = im.crop(BOX).resize(((BOX[2] - BOX[0]) * K, (BOX[3] - BOX[1]) * K), Image.LANCZOS)
zoom = zoom.resize((660, 1260), Image.LANCZOS)
d = ImageDraw.Draw(zoom)
pts = [(CX + R * math.cos(math.radians(a)), CY + R * math.sin(math.radians(a))) for a in range(30, 390, 60)]
d.line(pts + [pts[0]], fill=(255, 200, 0), width=6)

full = im.copy()
fd = ImageDraw.Draw(full)
fd.rectangle(BOX, outline=(255, 200, 0), width=4)

W, H = 1500, 1300
page = Image.new("RGB", (W, H), "white")
f = full.resize((int(full.width * H / full.height), H), Image.LANCZOS)
page.paste(f, (20, 0))
page.paste(zoom, (W - 700, 20))
pd = ImageDraw.Draw(page)
try:
    font = ImageFont.truetype("arial.ttf", 30)
    big = ImageFont.truetype("arialbd.ttf", 34)
except OSError:
    font = big = ImageFont.load_default()
tx, ty = W - 700 + CX + R + 14, 20 + CY - 22
pd.rectangle((tx - 8, ty - 6, tx + 140, ty + 46), fill=(20, 20, 20))
pd.text((tx, ty), "1 modulo", font=font, fill=(255, 200, 0))
pd.text((40, 1250), "Zone a moduli: centro busto e petto (vista frontale)", font=font, fill=(30, 30, 30))
page.save("04-posizione-modulo-figurino.png")
print("ok")
