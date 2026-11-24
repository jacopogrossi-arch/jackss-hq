"""Sottotitoli del Reel «Le 3 misure» (24/11/2026) nello stile degli altri Reel / della skill youtube-edit (formato `captions`):
UNA PAROLA ALLA VOLTA, grassetto Inter bianco, le parole chiave in Playfair Display corsivo (accento #ffb48f), piccolo pop all'ingresso, ombra morbida.
Tempi = parole della voce (Whisper sulla voce montata, corretti a mano). Uscita: sequenza di PNG trasparenti 1080x1920, uno per fotogramma a 24 fps
-> videos/_bench/reel-3-misure/caps/c0001.png ... (assemble.sh li sovrappone). Uso: python -I captions.py
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, shutil
W, H = 1080, 1920; FPS = 24; NFR = 787
FD = "D:/ClaudeCodeTest/.claude/skills/youtube-edit/assets/fonts/"
OUT = "D:/ClaudeCodeTest/videos/_bench/reel-3-misure/caps/"
os.makedirs(OUT, exist_ok=True)
CY = 1190                         # centro verticale: un po' sotto il centro dello schermo (richiesta di Jacopo)
MAXW = 860
SIZE = 74                         # piu' piccoli (richiesta di Jacopo)
CREMA = (255, 226, 200)
BIANCO = (255, 255, 255); ACCENTO = (255, 180, 143)
K = True
# gruppi di parole (testo con *parola chiave* in corsivo), inizio, fine: come i sottotitoli dello Short #16 (2-4 parole per riga, non una parola sola)
CHUNKS = [
    ("La tua *M*", 0.00, 0.74), ("non è la *M*", 0.74, 1.78), ("di un *altro brand*", 1.78, 2.85),
    ("Prendi un pantalone", 3.14, 4.08), ("che ti sta *bene*", 4.08, 4.92), ("e stendilo", 4.92, 5.74), ("sul *tavolo*", 5.74, 6.50),
    ("Prima misura:", 6.70, 7.92), ("la *vita*", 7.92, 8.90), ("Da un lato", 9.00, 9.50), ("all'altro del bordo", 9.50, 10.52), ("e moltiplichi", 10.52, 11.50), ("per *due*", 11.50, 12.20),
    ("Seconda:", 12.38, 13.42), ("l'altezza del *cavallo*", 13.42, 14.90), ("dall'incrocio", 15.12, 15.70), ("delle gambe", 15.70, 16.34), ("fino al bordo", 16.34, 17.14), ("davanti", 17.14, 17.90),
    ("Terza:", 18.12, 19.00), ("l'*interno* gamba", 19.00, 20.20), ("dall'incrocio", 20.32, 21.14), ("giù fino", 21.14, 21.90), ("all'*orlo*", 21.90, 22.80),
    ("Tre *numeri*", 23.04, 24.20), ("Prima di comprare", 24.22, 25.40), ("confrontali", 25.40, 25.98), ("con la *tabella*", 25.98, 26.96), ("Se non tornano", 26.96, 28.10), ("lascia *stare*", 28.10, 29.10),
    ("E tu,", 29.34, 29.98), ("scrivimi", 29.98, 30.46), ("nei *commenti*", 30.46, 31.24), ("il tuo *interno gamba*", 31.24, 32.75),
]
def inter(sz):
    f = ImageFont.truetype(FD + "Inter.ttf", sz)
    for how in (lambda: f.set_variation_by_name("ExtraBold"), lambda: f.set_variation_by_axes([800]), lambda: f.set_variation_by_axes([32, 800])):
        try: how(); break
        except Exception: continue
    return f
def playfair(sz): return ImageFont.truetype(FD + "PlayfairDisplay-Italic.ttf", sz)
def chunk_image(text):
    """RGBA 1080x1920 con il gruppo centrato in (540, CY): Inter ExtraBold bianco, parole *chiave* in Playfair corsivo (crema), ombra morbida."""
    segs = []
    for i, part in enumerate(text.split("*")): 
        if part: segs.append((part, i % 2 == 1))
    size = SIZE
    dm = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    while True:
        parts = [(p, k, (playfair(int(size * 1.12)) if k else inter(size))) for p, k in segs]
        total = sum(dm.textlength(p, font=f) for p, k, f in parts)
        if total <= MAXW or size < 40: break
        size -= 4
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); x = (W - total) / 2
    for p, k, f in parts:
        ImageDraw.Draw(sh).text((x, CY + 4), p, font=f, fill=(0, 0, 0, 215), anchor="ls"); ImageDraw.Draw(im).text((x, CY), p, font=f, fill=(CREMA if k else BIANCO) + (255,), anchor="ls"); x += dm.textlength(p, font=f)
    return Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)), im)
def veil():
    v = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(v)
    for y in range(0, 640): d.line((0, y, W, y), fill=(0, 0, 0, int(105 * (1 - y / 640) ** 1.5)))
    return v
def ease_out_back(x):
    x = max(0.0, min(1.0, x)); c1 = 1.4; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
if __name__ == "__main__":
    blank = Image.new("RGBA", (W, H), (0, 0, 0, 0)); blank.save(OUT + "blank.png"); cache = {}
    for f in range(1, NFR + 1):
        tt = (f - 1) / FPS; c = next((c for c in CHUNKS if c[1] <= tt < c[2]), None); path = OUT + "c%04d.png" % f
        if not c: shutil.copyfile(OUT + "blank.png", path); continue
        if c[0] not in cache: cache[c[0]] = chunk_image(c[0])
        age = tt - c[1]; img = cache[c[0]]; al = min(1.0, age / 0.10); rise = int(14 * (1 - min(1.0, age / 0.14)) ** 2)     # entra con una breve dissolvenza e una piccola salita
        if al < 1.0 or rise:
            canv = Image.new("RGBA", (W, H), (0, 0, 0, 0)); canv.paste(img, (0, rise), img); img = canv
            if al < 1.0: img.putalpha(img.getchannel("A").point(lambda v: int(v * al)))
        img.save(path)
    print("fatto", NFR)
