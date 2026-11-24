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
CY = 250                         # centro verticale del sottotitolo (sopra la testa: le inquadrature lasciano aria in alto)
MAXW = 930
BIANCO = (255, 255, 255); ACCENTO = (255, 180, 143)
K = True
WORDS = [
    ("La", 0.00, 0.18), ("tua", 0.18, 0.32), ("M", 0.32, 0.74, K), ("non", 0.74, 1.16), ("è", 1.16, 1.36), ("la", 1.36, 1.50), ("M", 1.50, 1.78, K), ("di", 1.78, 1.94), ("un", 1.94, 2.04), ("altro", 2.04, 2.24, K), ("brand", 2.24, 2.85, K),
    ("Prendi", 3.14, 3.52), ("un", 3.52, 3.62), ("pantalone", 3.62, 4.08), ("che", 4.08, 4.22), ("ti", 4.22, 4.38), ("sta", 4.38, 4.54), ("bene", 4.54, 4.92, K), ("e", 4.92, 5.28), ("stendilo", 5.28, 5.74), ("sul", 5.74, 5.90), ("tavolo", 5.90, 6.50, K),
    ("Prima", 6.70, 6.98), ("misura", 6.98, 7.92), ("la", 7.92, 8.02), ("vita", 8.02, 8.90, K), ("Da", 9.00, 9.12), ("un", 9.12, 9.24), ("lato", 9.24, 9.50), ("all'altro", 9.50, 9.92), ("del", 9.92, 10.12), ("bordo", 10.12, 10.52), ("e", 10.52, 10.98), ("moltiplichi", 10.98, 11.50), ("per", 11.50, 11.70), ("due", 11.70, 12.20, K),
    ("Seconda", 12.38, 13.42), ("l'altezza", 13.42, 13.90), ("del", 13.90, 14.10), ("cavallo", 14.10, 14.90, K), ("dall'incrocio", 15.12, 15.70), ("delle", 15.70, 15.90), ("gambe", 15.90, 16.34), ("fino", 16.34, 16.70), ("al", 16.70, 16.88), ("bordo", 16.88, 17.14), ("davanti", 17.14, 17.90, K),
    ("Terza", 18.12, 19.00), ("l'interno", 19.00, 19.48), ("gamba", 19.48, 20.20, K), ("dall'incrocio", 20.32, 21.14), ("giù", 21.14, 21.66), ("fino", 21.66, 21.90), ("all'orlo", 21.90, 22.80, K),
    ("Tre", 23.04, 23.32), ("numeri", 23.32, 24.20, K), ("Prima", 24.22, 24.42), ("di", 24.42, 24.56), ("comprare", 24.56, 25.40), ("confrontali", 25.40, 25.98), ("con", 25.98, 26.08), ("la", 26.08, 26.18), ("tabella", 26.18, 26.96, K), ("Se", 26.96, 27.14), ("non", 27.14, 27.28), ("tornano", 27.28, 28.10), ("lascia", 28.10, 28.44), ("stare", 28.44, 29.10, K),
    ("E", 29.34, 29.44), ("tu", 29.44, 29.98), ("scrivimi", 29.98, 30.46), ("nei", 30.46, 30.58), ("commenti", 30.58, 31.24, K), ("il", 31.24, 31.44), ("tuo", 31.44, 31.68), ("interno", 31.68, 32.22, K), ("gamba", 32.22, 32.75, K),
]
def inter(sz):
    f = ImageFont.truetype(FD + "Inter.ttf", sz)
    for how in (lambda: f.set_variation_by_name("ExtraBold"), lambda: f.set_variation_by_axes([800]), lambda: f.set_variation_by_axes([32, 800])):
        try: how(); break
        except Exception: continue
    return f
def playfair(sz): return ImageFont.truetype(FD + "PlayfairDisplay-Italic.ttf", sz)
def word_image(text, key):
    """RGBA 1080x1920 con la parola centrata in (540, CY): ombra morbida + testo. Il corpo si adatta alla larghezza massima."""
    size = 150 if not key else 164
    while True:
        f = playfair(size) if key else inter(size)
        l, t, r, b = ImageDraw.Draw(Image.new("RGB", (10, 10))).textbbox((0, 0), text, font=f, anchor="ls")
        if r - l <= MAXW or size < 60: break
        size -= 6
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = W / 2 - (l + r) / 2; y = CY - (t + b) / 2
    ImageDraw.Draw(sh).text((x, y + 6), text, font=f, fill=(0, 0, 0, 230), anchor="ls")
    ImageDraw.Draw(im).text((x, y), text, font=f, fill=(ACCENTO if key else BIANCO) + (255,), anchor="ls")
    return Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), im)
def veil():
    v = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(v)
    for y in range(0, 640): d.line((0, y, W, y), fill=(0, 0, 0, int(105 * (1 - y / 640) ** 1.5)))
    return v
def ease_out_back(x):
    x = max(0.0, min(1.0, x)); c1 = 1.4; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
if __name__ == "__main__":
    blank = Image.new("RGBA", (W, H), (0, 0, 0, 0)); blank.save(OUT + "blank.png")
    VEIL = veil(); cache = {}
    for f in range(1, NFR + 1):
        t = (f - 1) / FPS; w = next((w for w in WORDS if w[1] <= t < w[2]), None); path = OUT + "c%04d.png" % f
        if not w: shutil.copyfile(OUT + "blank.png", path); continue
        key = len(w) > 3; age = t - w[1]
        if (w[0], key) not in cache: cache[(w[0], key)] = word_image(w[0], key)
        img = cache[(w[0], key)]
        pop = 0.80 + 0.20 * ease_out_back(age / 0.16); alpha = min(1.0, age / 0.07)
        if pop != 1.0 or alpha < 1.0:
            sw, sh_ = int(W * pop), int(H * pop); img = img.resize((sw, sh_), Image.LANCZOS)
            canv = Image.new("RGBA", (W, H), (0, 0, 0, 0)); canv.paste(img, ((W - sw) // 2, int(CY - CY * pop)), img); img = canv
            if alpha < 1.0: img.putalpha(img.getchannel("A").point(lambda v: int(v * alpha)))
        out = Image.alpha_composite(VEIL, img); out.save(path)
    print("fatto", NFR)
