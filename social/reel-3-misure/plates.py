"""Sottotitoli del Reel «Le 3 misure» (24/11/2026), nello stile degli altri Reel (Short #16): IN ALTO, bianco grassetto (IBM Plex Sans) con UNA parola chiave in Instrument Serif corsivo,
ombra morbida, nessun riquadro. La parola chiave ha il colore della sua misura (vita arancio, cavallo azzurro, interno magenta), come le linee sul pantalone.
Uso: python -I plates.py  ->  videos/_bench/reel-3-misure/plates/*.png (1080x1920, trasparenti), poi assemble.sh li sovrappone con dissolvenza.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
W, H = 1080, 1920
FD = "D:/ClaudeCodeTest/.claude/skills/youtube-edit/assets/fonts/"
OUT = "D:/ClaudeCodeTest/videos/_bench/reel-3-misure/plates/"
os.makedirs(OUT, exist_ok=True)
BIANCO = (255, 255, 255); SABBIA = (0xD8, 0xCF, 0xBA)
C_VITA = (255, 122, 84); C_CAV = (96, 176, 255); C_INT = (240, 98, 176); C_NEUTRO = (0xF6, 0xDF, 0xB0)

def sans(sz, w=700):
    f = ImageFont.truetype(FD + "IBMPlexSans.ttf", sz)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def serif(sz): return ImageFont.truetype(FD + "InstrumentSerif-Italic.ttf", int(sz * 1.14))

def caption(lines, size=88, y0=170, lead=1.16):
    """lines: lista di righe; riga = lista di segmenti (testo, 'sans'|'serif'|'small', colore). Centrate, in alto, con ombra e un velo scuro leggero sotto il testo."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # velo: leggerissimo gradiente scuro in alto, solo per garantire la leggibilita'
    veil = Image.new("RGBA", (W, H), (0, 0, 0, 0)); vd = ImageDraw.Draw(veil)
    for y in range(0, 560):
        vd.line((0, y, W, y), fill=(0, 0, 0, int(110 * (1 - y / 560) ** 1.6)))
    im = Image.alpha_composite(im, veil)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(shadow); txt = Image.new("RGBA", (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(txt)
    y = y0; dm = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    for line in lines:
        parts = []
        for t, kind, col in line:
            f = sans(size) if kind == "sans" else (serif(size) if kind == "serif" else sans(int(size * 0.55), 500))
            b = dm.textbbox((0, 0), t, font=f, anchor="ls"); parts.append((t, f, col, dm.textlength(t, font=f), b))
        tw = sum(p[3] for p in parts); x = (W - tw) / 2; base = y + size
        for t, f, col, adv, b in parts:
            sd.text((x, base + 5), t, font=f, fill=(0, 0, 0, 215), anchor="ls"); td.text((x, base), t, font=f, fill=col + (255,), anchor="ls"); x += adv
        y += int(size * lead)
    im = Image.alpha_composite(im, shadow.filter(ImageFilter.GaussianBlur(9)))
    return Image.alpha_composite(im, txt)
def save(name, im): im.save(OUT + name + ".png"); print(name)
S = "sans"; R = "serif"; P = "small"

save("p1_gancio", caption([[("La tua M non è", S, BIANCO)], [("la M di un ", S, BIANCO), ("altro brand", R, C_NEUTRO)]]))
save("p2_vita", caption([[("1 · La ", S, BIANCO), ("vita", R, C_VITA)], [("da lato a lato", P, SABBIA)]]))
save("p3_x2", caption([[("× ", S, BIANCO), ("2", R, C_VITA)]], size=170, y0=150))
save("p4_cavallo", caption([[("2 · L'altezza", S, BIANCO)], [("del ", S, BIANCO), ("cavallo", R, C_CAV)]]))
save("p5_interno", caption([[("3 · L'", S, BIANCO), ("interno", R, C_INT), (" gamba", S, BIANCO)]], size=84))
def numeri(n):
    rows = [[("Vita ", S, BIANCO), ("41 × 2 = 82", R, C_VITA)]]
    if n >= 2: rows.append([("Cavallo ", S, BIANCO), ("27", R, C_CAV)])
    if n >= 3: rows.append([("Interno ", S, BIANCO), ("80", R, C_INT)])
    rows.append([("(valori d'esempio)", P, SABBIA)])
    return caption(rows, size=84)
for n in (1, 2, 3): save("p6_numeri%d" % n, numeri(n))
save("p7_domanda", caption([[("Il tuo ", S, BIANCO), ("interno gamba", R, C_NEUTRO), ("?", S, BIANCO)], [("scrivilo nei commenti", P, SABBIA)]]))
