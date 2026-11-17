# Pannello dietro della vestaglia (look 2) con la stampa piazzata Room Key posizionata.
# Scala: S px = 1 cm. Origine: centro scollo dietro (x=0, y=0), y verso il basso.
from PIL import Image, ImageDraw, ImageFont

MOTIF = r"D:\ClaudeCodeTest\accademia\img-after-hours\stampa-room-key-A-FINALE.webp"
OUT = r"D:\ClaudeCodeTest\accademia\img-after-hours\cartamodello-dietro-stampa.png"

S = 12
GOLD = (193, 152, 99, 255)
GREEN = (2, 79, 56, 255)
MX, MY = 260, 170  # margini
X0 = MX + 36 * S   # x del centro dietro
W = X0 * 2
H = MY + int(121 * S) + 190

def P(x, y):
    return (X0 + x * S, MY + (y + 2.5) * S)

def bez(p0, p1, p2, p3, n=30):
    out = []
    for i in range(n + 1):
        t = i / n
        a = (1 - t) ** 3; b = 3 * (1 - t) ** 2 * t; c = 3 * (1 - t) * t ** 2; d = t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
                    a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out

# metà destra del pannello, in cm
right = []
right += bez((0, 0), (4, 0), (8, -1.5), (9, -2.5))            # scollo dietro
right += [(23, 2.5)]                                         # spalla
right += bez((23, 2.5), (21.5, 12), (23, 22), (29, 26))      # giromanica
right += [(29, 50), (36, 118)]                               # fianco, svasato verso l'orlo
right += bez((36, 118), (24, 119.2), (10, 119.5), (0, 119.5))  # orlo
left = [(-x, y) for x, y in reversed(right)]
outline = [P(x, y) for x, y in right + left]

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.polygon(outline, fill=GREEN)
d.line(outline + [outline[0]], fill=GOLD, width=4, joint="curve")

# motivo: ritaglio stretto sull'emblema, 20 cm di larghezza, 12 cm sotto lo scollo
m = Image.open(MOTIF).convert("RGB")
px = m.load()
xs, ys = [], []
for yy in range(0, m.height, 2):
    for xx in range(0, m.width, 2):
        r, g, b = px[xx, yy]
        if r > 120 and g > 100:
            xs.append(xx); ys.append(yy)
box = (min(xs) - 4, min(ys) - 4, max(xs) + 4, max(ys) + 4)
m = m.crop(box)
mw = 20 * S
mh = round(m.height * mw / m.width)
m = m.resize((mw, mh), Image.LANCZOS)
motif_h_cm = mh / S
mx0, my0 = P(-10, 12)
mask = m.convert("L").point(lambda v: 0 if v < 70 else min(255, (v - 70) * 3))
img.paste(m, (int(mx0), int(my0)), mask)

try:
    f = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 30)
    fs = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 24)
    fi = ImageFont.truetype(r"C:\Windows\Fonts\georgiai.ttf", 26)
except OSError:
    f = fs = fi = ImageFont.load_default()

# centro dietro (linea punto-tratto) e quote
cx = X0
y = P(0, 0)[1] - 30
skip = (my0 - 10, my0 + mh + 10)
while y < P(0, 119.5)[1] + 30:
    if skip[0] < y < skip[1]:
        y += 48; continue
    d.line([(cx, y), (cx, y + 22)], fill=GOLD, width=2); y += 34
    d.line([(cx, y), (cx, y + 4)], fill=GOLD, width=2); y += 14
d.text((cx + 12, P(0, 119.5)[1] + 22), "centro dietro", font=fi, fill=GOLD)

def tick_v(x, ya, yb, label, side=1):
    d.line([(x, ya), (x, yb)], fill=GOLD, width=2)
    for yy in (ya, yb):
        d.line([(x - 10, yy), (x + 10, yy)], fill=GOLD, width=2)
    tw = d.textlength(label, font=f)
    tx = x + 18 if side > 0 else x - 18 - tw
    d.text((tx, (ya + yb) / 2 - 18), label, font=f, fill=GOLD)

def tick_h(xa, xb, y, label):
    d.line([(xa, y), (xb, y)], fill=GOLD, width=2)
    for xx in (xa, xb):
        d.line([(xx, y - 10), (xx, y + 10)], fill=GOLD, width=2)
    tw = d.textlength(label, font=f)
    d.text(((xa + xb) / 2 - tw / 2, y - 44), label, font=f, fill=GOLD)

tick_v(P(-14, 0)[0], P(0, 0)[1], P(0, 12)[1], "12 cm", side=-1)
tick_h(P(-10, 0)[0], P(10, 0)[0], P(0, 12 + motif_h_cm + 4)[1], "")
d.text((P(0, 0)[0] - d.textlength("20 cm", font=f) / 2, P(0, 12 + motif_h_cm + 5)[1]), "20 cm", font=f, fill=GOLD)
tick_v(P(13, 0)[0], P(0, 12)[1], P(0, 12 + motif_h_cm)[1], f"{motif_h_cm:.0f} cm", side=1)

# drittofilo
gx = P(-19, 0)[0]
ya, yb = P(0, 66)[1], P(0, 100)[1]
d.line([(gx, ya), (gx, yb)], fill=GOLD, width=3)
for yy, s in ((ya, 1), (yb, -1)):
    d.polygon([(gx, yy), (gx - 10, yy + 22 * s), (gx + 10, yy + 22 * s)], fill=GOLD)
d.text((gx + 16, (ya + yb) / 2 - 14), "drittofilo", font=fi, fill=GOLD)

# etichetta del pezzo
lab = ["DIETRO", "vestaglia · look 2", "velluto smeraldo · taglia 1", "stampa a lamina oro"]
ly = P(0, 70)[1]
for i, t in enumerate(lab):
    font = f if i == 0 else fs
    d.text((P(8, 0)[0], ly + i * 38), t, font=font, fill=GOLD)

img.save(OUT)
print(OUT, img.size, f"motivo {motif_h_cm:.1f} cm di altezza")

