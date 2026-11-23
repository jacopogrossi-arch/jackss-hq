"""Plate del Reel «Le 3 misure» (24/11/2026): PNG trasparenti 1080x1920 con i font del brand (Instrument Serif + IBM Plex Sans) e la palette Inverso.
Uso: python -I plates.py   ->  videos/_bench/reel-3-misure/plates/*.png   (poi assemble.sh li sovrappone con dissolvenza)
Zona sicura Instagram: niente nel quarto basso ne' nella colonna destra dei pulsanti; i plate stanno tra il 56% e il 74% dell'altezza.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
W, H = 1080, 1920
FD = "D:/ClaudeCodeTest/.claude/skills/youtube-edit/assets/fonts/"
OUT = "D:/ClaudeCodeTest/videos/_bench/reel-3-misure/plates/"
os.makedirs(OUT, exist_ok=True)
GESSO = (0xEF, 0xE9, 0xDD); BOSCO = (0x2F, 0x3A, 0x2E); RUGGINE = (0x8A, 0x4B, 0x2D); SABBIA = (0xB9, 0xAE, 0x98); INCH = (0x1E, 0x1B, 0x18)
def serif(sz, it=False): return ImageFont.truetype(FD + ("InstrumentSerif-Italic.ttf" if it else "InstrumentSerif-Regular.ttf"), sz)
def sans(sz):
    f = ImageFont.truetype(FD + "IBMPlexSans.ttf", sz)
    try: f.set_variation_by_axes([600])
    except Exception: pass
    return f

def card(rows, y_center, pad=(56, 40), gap=18, alpha=215, radius=28, minw=0):
    """rows: lista di (testo, font, colore). Carta bosco arrotondata con le righe centrate. Ritorna l'immagine RGBA a piena pagina."""
    dm = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    sizes = [dm.textbbox((0, 0), t, font=f) for t, f, c in rows]
    tw = max(max(b[2] - b[0] for b in sizes), minw); th = sum(b[3] - b[1] for b in sizes) + gap * (len(rows) - 1)
    bw, bh = tw + 2 * pad[0], th + 2 * pad[1]
    x0, y0 = (W - bw) // 2, int(y_center - bh / 2)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + 10, x0 + bw, y0 + bh + 10), radius, fill=(0, 0, 0, 110))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(im); d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), radius, fill=BOSCO + (alpha,))
    y = y0 + pad[1]
    for (t, f, c), b in zip(rows, sizes):
        d.text((W // 2 - (b[2] - b[0]) // 2 - b[0], y - b[1]), t, font=f, fill=c); y += (b[3] - b[1]) + gap
    return im

def save(name, im): im.save(OUT + name + ".png"); print(name)

# 1 gancio: la frase intera, leggibile anche muto
save("p1_gancio", card([("La tua M", serif(118), GESSO), ("non è la M di un altro brand", serif(66, True), SABBIA)], H * 0.64))
# 2-4 etichette delle tre misure
save("p2_vita", card([("1", sans(40), SABBIA), ("Vita", serif(120), GESSO), ("da lato a lato", serif(56, True), SABBIA)], H * 0.64))
save("p3_x2", card([("× 2", serif(190), (0xE0, 0x9A, 0x6E))], H * 0.64, pad=(70, 30)))
save("p4_cavallo", card([("2", sans(40), SABBIA), ("Altezza del cavallo", serif(96), GESSO), ("dall'incrocio al bordo davanti", serif(52, True), SABBIA)], H * 0.64))
save("p5_interno", card([("3", sans(40), SABBIA), ("Interno gamba", serif(110), GESSO), ("dall'incrocio all'orlo", serif(54, True), SABBIA)], H * 0.64))
# 6 tre numeri (valori d'esempio finche' Jacopo non da' i suoi)
def numeri(n):
    rows = [("TRE NUMERI", sans(34), SABBIA)]
    data = [("Vita", "41 × 2 = 82 cm"), ("Cavallo", "27 cm"), ("Interno gamba", "80 cm")]
    for lab, val in data[:n]:
        rows.append((lab + "   " + val, serif(84), GESSO))
    rows.append(("valori d'esempio", sans(26), SABBIA))
    return card(rows, H * 0.64, gap=26, minw=720)
for n in (1, 2, 3): save("p6_numeri%d" % n, numeri(n))
# 7 domanda finale
save("p7_domanda", card([("Il tuo interno gamba?", serif(104), GESSO), ("scrivilo nei commenti", serif(60, True), SABBIA)], H * 0.64))
