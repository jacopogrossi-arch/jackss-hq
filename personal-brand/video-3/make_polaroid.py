# Genera versioni polaroid dei 10 shot lookbook Video #3:
# bordo bianco (più alto in basso, stile polaroid), leggera rotazione
# casuale ±2-4°, ombra morbida, sfondo trasparente per il nero in CapCut.
import glob
import os
import random

from PIL import Image, ImageFilter

SRC = r"C:\Users\Jacopo Grossi\Downloads"
OUT = os.path.join(SRC, "video3-polaroid")
os.makedirs(OUT, exist_ok=True)

random.seed(3)  # rotazioni riproducibili

files = sorted(glob.glob(os.path.join(SRC, "video3-shot*.png")))
for i, path in enumerate(files):
    img = Image.open(path).convert("RGB")
    w, h = img.size

    side = round(w * 0.05)          # bordo laterale e superiore
    bottom = round(w * 0.16)        # bordo inferiore più spesso
    card = Image.new("RGB", (w + side * 2, h + side + bottom), "white")
    card.paste(img, (side, side))

    # rotazione alternata: pari a destra, dispari a sinistra
    angle = random.uniform(2, 4) * (1 if i % 2 == 0 else -1)
    card = card.convert("RGBA").rotate(angle, expand=True, resample=Image.BICUBIC)

    # ombra morbida sotto la card per staccarla dal fondo nero
    shadow = Image.new("RGBA", card.size, (0, 0, 0, 0))
    alpha = card.split()[3].point(lambda a: min(a, 110))
    shadow.putalpha(alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(round(w * 0.015)))

    pad = round(w * 0.05)
    canvas = Image.new("RGBA", (card.width + pad * 2, card.height + pad * 2), (0, 0, 0, 0))
    off = round(w * 0.012)
    canvas.alpha_composite(shadow, (pad + off, pad + off))
    canvas.alpha_composite(card, (pad, pad))

    name = os.path.splitext(os.path.basename(path))[0] + "-polaroid.png"
    canvas.save(os.path.join(OUT, name))
    print(f"{name}  ({angle:+.1f} deg)")

print(f"\n{len(files)} polaroid salvate in {OUT}")
