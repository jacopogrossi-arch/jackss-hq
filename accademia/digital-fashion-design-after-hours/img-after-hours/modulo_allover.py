# Modulo all-over "Catena della notte": half-drop continuo costruito dai due elementi generati.
from PIL import Image, ImageOps, ImageDraw, ImageChops
import numpy as np

SRC = "D:/ClaudeCodeTest/accademia/img-after-hours/allover-elementi.webp"
OUT = "D:/ClaudeCodeTest/accademia/img-after-hours/"
T = 3780  # 32 cm a 300 dpi

CHOC = (59, 38, 32)
GREEN = (15, 77, 58)
IVORY = (237, 228, 211)

src = Image.open(SRC).convert("RGB")
a = np.asarray(src).astype(float)
bg = np.median(a[:40, :40].reshape(-1, 3), axis=0)
dist = np.sqrt(((a - bg) ** 2).sum(axis=2))
alpha = np.clip((dist - 25) / 60, 0, 1)
alpha_img = Image.fromarray((alpha * 255).astype("uint8"))

def main_run(profile, gap=25):
    # tratto continuo piu lungo (tollera buchi < gap): scarta i segnetti isolati
    on = np.where(profile > 0)[0]
    runs, start, prev = [], on[0], on[0]
    for v in on[1:]:
        if v - prev > gap:
            runs.append((start, prev)); start = v
        prev = v
    runs.append((start, prev))
    return max(runs, key=lambda r: r[1] - r[0])

def cut(x0, x1):
    sub = alpha[:, x0:x1] > 0.3
    cx0, cx1 = main_run(sub.sum(axis=0))
    ry0, ry1 = main_run(sub[:, cx0:cx1 + 1].sum(axis=1))
    box = (x0 + cx0 - 6, ry0 - 6, x0 + cx1 + 6, ry1 + 6)
    rgba = src.crop(box).convert("RGBA")
    m = alpha_img.crop(box)
    rgba.putalpha(m)
    return rgba

w = src.width
bit = cut(0, w // 2)
key = cut(w // 2, w)

def scaled(im, target_w):
    h = round(im.height * target_w / im.width)
    return im.resize((target_w, h), Image.LANCZOS)

bitA = scaled(bit, int(T * 0.21)).rotate(-42, expand=True, resample=Image.BICUBIC)
bitB = scaled(bit, int(T * 0.19)).rotate(-28, expand=True, resample=Image.BICUBIC)
keyA = scaled(key, int(T * 0.13)).rotate(-15, expand=True, resample=Image.BICUBIC)
keyB = scaled(key, int(T * 0.13)).rotate(15, expand=True, resample=Image.BICUBIC)

def build(elem_layer_color=None):
    layer = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    # half-drop: colonna 0 a y = 0 e T/2, colonna 1 sfalsata di T/4
    # 2 colonne x 4 righe; la colonna di destra scende di mezza cella (half-drop)
    # 4 colonne x 2 righe; le colonne dispari scendono di mezza cella (half-drop)
    cells = []
    for col in range(4):
        x = T * (0.125 + 0.25 * col)
        off = 0.25 * T if col % 2 else 0
        for row in range(2):
            y = T * (0.25 + 0.5 * row) + off
            if row == col // 2:  # i morsetti formano una catena in diagonale
                im = bitA
            else:
                im = keyA if col % 2 == 0 else keyB
            cells.append((x, y, im))
    for cx, cy, im in cells:
        for dx in (-T, 0, T):
            for dy in (-T, 0, T):
                x = int(cx + dx - im.width / 2)
                y = int(cy + dy - im.height / 2)
                layer.alpha_composite(im, (x, y)) if 0 <= x and 0 <= y and x + im.width <= T and y + im.height <= T else paste_clip(layer, im, x, y)
    return layer

def paste_clip(layer, im, x, y):
    x0, y0 = max(x, 0), max(y, 0)
    x1, y1 = min(x + im.width, T), min(y + im.height, T)
    if x0 >= x1 or y0 >= y1:
        return
    part = im.crop((x0 - x, y0 - y, x1 - x, y1 - y))
    layer.alpha_composite(part, (x0, y0))

motif = build()

# variante A: oro originale su cioccolato
A = Image.new("RGBA", (T, T), CHOC + (255,))
A.alpha_composite(motif)
A = A.convert("RGB")

# variante B: stesso disegno ricolorato avorio su smeraldo
lum = ImageOps.autocontrast(motif.convert("L"))
tinted = ImageOps.colorize(lum, black=(120, 140, 120), white=IVORY).convert("RGBA")
tinted.putalpha(motif.getchannel("A"))
B = Image.new("RGBA", (T, T), GREEN + (255,))
B.alpha_composite(tinted)
B = B.convert("RGB")

A.save(OUT + "allover-modulo-A.jpg", quality=90)
B.save(OUT + "allover-modulo-B.jpg", quality=90)

# anteprima 3x3 con il modulo evidenziato (come nell'esempio della prof)
def repeat_preview(tile, n=3, size=900):
    small = tile.resize((size // n, size // n), Image.LANCZOS)
    prev = Image.new("RGB", (size, size))
    for i in range(n):
        for j in range(n):
            prev.paste(small, (i * small.width, j * small.height))
    d = ImageDraw.Draw(prev)
    s = small.width
    d.rectangle([s, s, 2 * s, 2 * s], outline=(193, 149, 96), width=4)
    return prev

repeat_preview(A).save(OUT + "allover-ripetizione-A.jpg", quality=92)
repeat_preview(B).save(OUT + "allover-ripetizione-B.jpg", quality=92)
print("ok", bitA.size, keyA.size)




