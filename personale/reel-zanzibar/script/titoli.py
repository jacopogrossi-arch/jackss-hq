"""20 proposte di titolo 'The beauty of Zanzibar' sul fotogramma dell'arco (fermo immagine; dove serve, a meta' animazione).
uso: python -I titoli.py  ->  01.jpg ... 20.jpg + foglio-1.jpg, foglio-2.jpg (per il telefono)"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
WF = "C:/Windows/Fonts/"
UF = os.path.expandvars("%LOCALAPPDATA%/Microsoft/Windows/Fonts/")
INTER = ROOT + "/.claude/skills/youtube-edit/assets/fonts/Inter.ttf"
PLAYFAIR = ROOT + "/.claude/skills/youtube-edit/assets/fonts/PlayfairDisplay-Italic.ttf"
EBG, EBGI = ROOT + "/personale/youtube/motion/fonts/r400.ttf", ROOT + "/personale/youtube/motion/fonts/it400.ttf"
AG = ROOT + "/inverso/assets-jago/carosello-pricing/fonts/"
BG = Image.open(os.path.join(HERE, "sfondo.png")).convert("RGB")
W, H = BG.size
IVORY, GOLD, CREAM = (246, 241, 230), (214, 178, 106), (243, 230, 204)


def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight:
        f.set_variation_by_axes([32, weight])
    return f


def width(text, f, track=0):
    return sum(f.getlength(c) for c in text) + track * (len(text) - 1)


def layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def put(lay, text, f, x, y, fill=IVORY, track=0, anchor="l", alpha=255):
    """Writes text letter by letter (tracking); anchor l/c/r on x, y = baseline."""
    d = ImageDraw.Draw(lay)
    if anchor == "c":
        x -= width(text, f, track) / 2
    elif anchor == "r":
        x -= width(text, f, track)
    for c in text:
        d.text((x, y), c, font=f, fill=fill[:3] + (alpha,), anchor="ls")
        x += f.getlength(c) + track
    return x


def gradient_fill(mask_lay, c1, c2, vertical=True):
    """Colours the opaque pixels of mask_lay with a gradient c1 -> c2."""
    g = Image.new("RGBA", (W, H))
    box = mask_lay.getbbox() or (0, 0, W, H)
    a0, a1 = (box[1], box[3]) if vertical else (box[0], box[2])
    for i in range(H if vertical else W):
        t = min(max((i - a0) / max(a1 - a0, 1), 0), 1)
        col = tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3)) + (255,)
        if vertical:
            g.paste(col, (0, i, W, i + 1))
        else:
            g.paste(col, (i, 0, i + 1, H))
    g.putalpha(mask_lay.getchannel("A"))
    return g


def glow(lay, radius, colour, strength=1.0):
    a = lay.getchannel("A").filter(ImageFilter.GaussianBlur(radius))
    a = a.point(lambda v: min(255, int(v * strength)))
    g = Image.new("RGBA", (W, H), colour + (0,))
    g.putalpha(a)
    return g


def shadow(lay, radius=8, opacity=0.55):
    return glow(lay, radius, (0, 0, 0), opacity)


def veil(img, side="bottom", strength=0.55, start=0.45):
    """Dark gradient (left / bottom / center) to make text legible."""
    v = Image.new("L", (W, H))
    for i in range(W if side == "left" else H):
        t = i / (W if side == "left" else H)
        if side == "left":
            a = max(0, (0.55 - t) / 0.55)
            v.paste(int(255 * strength * a), (i, 0, i + 1, H))
        elif side == "bottom":
            a = max(0, (t - start) / (1 - start))
            v.paste(int(255 * strength * a), (0, i, W, i + 1))
        else:
            a = 1 - abs(t - 0.5) * 2
            v.paste(int(255 * strength * a ** 2), (0, i, W, i + 1))
    black = Image.new("RGB", (W, H))
    return Image.composite(black, img, v)


def label(img, n, txt):
    d = ImageDraw.Draw(img)
    f = font(INTER, 30, 600)
    t = "%02d  %s" % (n, txt)
    d.rounded_rectangle((24, 22, 48 + f.getlength(t), 70), 10, fill=(0, 0, 0))
    d.text((36, 58), t, font=f, fill=(255, 220, 0), anchor="ls")
    return img


def comp(base, *lays):
    out = base.convert("RGBA")
    for l in lays:
        out = Image.alpha_composite(out, l)
    return out.convert("RGB")


designs = []


def design(desc):
    def deco(fn):
        designs.append((desc, fn))
        return fn
    return deco


@design("Come Krabi: Segoe Light spaziato + Garamond light minuscolo")
def d1():
    l = layer()
    f1, f2 = font(WF + "segoeuil.ttf", 62), font(AG + "AppleGaramond-Light.ttf", 150)
    for w, x in (("The", 330), ("beauty", 610), ("of", 900)):
        put(l, w, f1, x, 520)
    put(l, "zanzibar", f2, 590, 720)
    return comp(BG, shadow(l, 10, .6), l)


@design("Preset YouTube: Inter 700 avorio + Playfair Italic oro con glow")
def d2():
    l1, l2 = layer(), layer()
    put(l1, "The beauty of", font(INTER, 96, 700), W / 2, 470, IVORY, anchor="c")
    put(l2, "Zanzibar", font(PLAYFAIR, 190), W / 2, 680, anchor="c")
    g = gradient_fill(l2, GOLD, IVORY)
    return comp(veil(BG, "center", .35), shadow(l1, 12, .5), glow(l2, 18, GOLD, 1.6), l1, g)


@design("Typewriter (a meta'): Courier, lettera per lettera col cursore")
def d3():
    l = layer()
    f = font(WF + "cour.ttf", 84)
    x = put(l, "the beauty of zanz", f, 300, 560, IVORY)
    ImageDraw.Draw(l).rectangle((x + 6, 492, x + 14, 572), fill=IVORY + (255,))
    return comp(veil(BG, "center", .35), shadow(l, 8, .7), l)


@design("ZANZIBAR maiuscolo Garamond, lettere larghe + riga sottile")
def d4():
    l = layer()
    put(l, "THE BEAUTY OF", font(UF + "HelveticaNeueLight.otf", 40), W / 2, 450, IVORY, track=18, anchor="c")
    put(l, "ZANZIBAR", font(AG + "AppleGaramond.ttf", 170), W / 2, 640, IVORY, track=34, anchor="c")
    ImageDraw.Draw(l).line((W / 2 - 60, 700, W / 2 + 60, 700), fill=IVORY + (255,), width=2)
    return comp(veil(BG, "center", .4), shadow(l, 12, .6), l)


@design("Playfair Italic enorme color crema, 'the beauty of' piccolo sopra")
def d5():
    l = layer()
    put(l, "the beauty of", font(INTER, 44, 400), W / 2, 420, CREAM, track=6, anchor="c")
    put(l, "Zanzibar", font(PLAYFAIR, 280), W / 2, 680, CREAM, anchor="c")
    return comp(veil(BG, "center", .35), shadow(l, 16, .55), l)


@design("EB Garamond Italic con sfumatura oro (dall'alto al basso)")
def d6():
    l = layer()
    put(l, "The beauty of Zanzibar", font(EBGI, 130), W / 2, 600, anchor="c")
    return comp(veil(BG, "center", .4), shadow(l, 12, .6), gradient_fill(l, (250, 226, 170), (190, 140, 70)))


@design("Lettera per lettera in dissolvenza (a meta')")
def d7():
    l = layer()
    f = font(AG + "AppleGaramond-Light.ttf", 170)
    text, x = "Zanzibar", W / 2 - width("Zanzibar", f, 6) / 2
    put(l, "the beauty of", font(WF + "segoeuil.ttf", 50), W / 2, 440, IVORY, track=10, anchor="c")
    for i, c in enumerate(text):
        a = max(0, min(255, int(255 * (1.6 - i * 0.28))))
        put(l, c, f, x, 640, IVORY, alpha=a)
        x += f.getlength(c) + 6
    return comp(veil(BG, "center", .35), shadow(l, 10, .5), l)


@design("Blur-in: il titolo arriva dallo sfocato (a meta')")
def d8():
    l = layer()
    put(l, "the beauty of", font(INTER, 54, 300), W / 2, 450, IVORY, track=8, anchor="c")
    put(l, "Zanzibar", font(EBG, 200), W / 2, 660, IVORY, anchor="c")
    r = l.crop((W // 2, 0, W, H)).filter(ImageFilter.GaussianBlur(9))
    l.paste(r, (W // 2, 0))
    return comp(veil(BG, "center", .35), shadow(l, 10, .5), l)


@design("Maschera dal basso: le lettere salgono da una linea (a meta')")
def d9():
    l = layer()
    put(l, "ZANZIBAR", font(UF + "HelveticaNeueBold.otf", 200), W / 2, 700, IVORY, track=10, anchor="c")
    l.paste((0, 0, 0, 0), (0, 640, W, H))
    l2 = layer()
    put(l2, "the beauty of", font(UF + "HelveticaNeueLight.otf", 48), W / 2, 440, IVORY, track=10, anchor="c")
    ImageDraw.Draw(l2).line((560, 642, W - 560, 642), fill=IVORY + (200,), width=2)
    return comp(veil(BG, "center", .4), shadow(l, 10, .5), l, l2)


@design("Editoriale in basso a sinistra + coordinate")
def d10():
    l = layer()
    put(l, "The beauty of", font(UF + "HelveticaNeueLight.otf", 46), 120, 800, IVORY, track=4)
    put(l, "Zanzibar", font(UF + "HelveticaNeueBold.otf", 150), 112, 940, IVORY)
    put(l, "6.1659° S   39.2026° E", font(INTER, 30, 400), 122, 1000, IVORY, track=6)
    ImageDraw.Draw(l).line((122, 820, 122, 820), fill=IVORY)
    return comp(veil(BG, "bottom", .7, .4), l)


@design("Impilato al centro con righe e anno")
def d11():
    l = layer()
    d = ImageDraw.Draw(l)
    put(l, "THE BEAUTY OF", font(INTER, 40, 500), W / 2, 430, IVORY, track=16, anchor="c")
    put(l, "Zanzibar", font(EBGI, 190), W / 2, 620, IVORY, anchor="c")
    put(l, "OTTOBRE 2026", font(INTER, 32, 400), W / 2, 712, IVORY, track=14, anchor="c")
    for y in (455, 680):
        d.line((W / 2 - 110, y, W / 2 + 110, y), fill=IVORY + (220,), width=2)
    return comp(veil(BG, "center", .4), shadow(l, 12, .55), l)


@design("Solo contorno: ZANZIBAR vuoto, Helvetica Black")
def d12():
    l = layer()
    f = font(UF + "HelveticaNeueBlack.otf", 250)
    ImageDraw.Draw(l).text((W / 2, 680), "ZANZIBAR", font=f, anchor="ms", fill=(0, 0, 0, 0), stroke_width=4, stroke_fill=IVORY + (255,))
    put(l, "the beauty of", font(INTER, 50, 500), W / 2, 420, IVORY, track=8, anchor="c")
    return comp(veil(BG, "center", .3), shadow(l, 8, .5), l)


@design("Lettere-finestra: l'immagine dentro ZANZIBAR, fuori velo scuro")
def d13():
    m = layer()
    ImageDraw.Draw(m).text((W / 2, 700), "ZANZIBAR", font=font(UF + "HelveticaNeueBlack.otf", 240), anchor="ms", fill=(255, 255, 255, 255))
    dark = Image.blend(BG, Image.new("RGB", (W, H)), .72)
    out = Image.composite(BG, dark, m.getchannel("A"))
    l = layer()
    put(l, "the beauty of", font(INTER, 52, 300), W / 2, 420, IVORY, track=12, anchor="c")
    return comp(out, l)


@design("Sfumatura tramonto (arancio -> rosa) su Georgia Italic")
def d14():
    l = layer()
    put(l, "the beauty of", font(WF + "georgiai.ttf", 64), W / 2, 450, anchor="c")
    put(l, "Zanzibar", font(WF + "georgiai.ttf", 210), W / 2, 670, anchor="c")
    return comp(veil(BG, "center", .4), shadow(l, 12, .6), gradient_fill(l, (255, 190, 90), (240, 110, 130), vertical=False))


@design("'Zanzibar' color turchese dell'acqua, resto bianco")
def d15():
    l1, l2 = layer(), layer()
    put(l1, "The beauty of", font(INTER, 70, 300), W / 2, 450, IVORY, track=4, anchor="c")
    put(l2, "Zanzibar", font(INTER, 220, 800), W / 2, 670, (110, 232, 214), anchor="c")
    return comp(veil(BG, "center", .45), shadow(l1, 10, .5), shadow(l2, 14, .6), l1, l2)


@design("Sottotitolo da film: corsivo piccolo in basso al centro")
def d16():
    l = layer()
    put(l, "the beauty of zanzibar", font(WF + "timesi.ttf", 58), W / 2, 980, (255, 244, 200), anchor="c")
    return comp(veil(BG, "bottom", .5, .6), shadow(l, 6, .8), l)


@design("Diviso: in alto a sinistra / in basso a destra, Inter Light")
def d17():
    l = layer()
    put(l, "The beauty of", font(INTER, 64, 200), 120, 180, IVORY, track=4)
    put(l, "Zanzibar", font(INTER, 170, 200), W - 120, 960, IVORY, anchor="r")
    return comp(veil(BG, "center", .25), shadow(l, 12, .6), l)


@design("Maiuscolo oro molto spaziato, Dubai Light")
def d18():
    l = layer()
    put(l, "THE BEAUTY OF", font(WF + "DUBAI-LIGHT.TTF", 46), W / 2, 470, GOLD, track=24, anchor="c")
    put(l, "ZANZIBAR", font(WF + "DUBAI-LIGHT.TTF", 150), W / 2, 650, GOLD, track=52, anchor="c")
    return comp(veil(BG, "center", .5), glow(l, 14, (0, 0, 0), .6), l)


@design("Parola per parola dal basso (a meta': 'of' sta salendo)")
def d19():
    l = layer()
    f = font(EBG, 110)
    x = W / 2 - width("The beauty of", f, 0) / 2
    for w, dy, a in (("The ", 0, 255), ("beauty ", 0, 255), ("of", 34, 120)):
        put(l, w, f, x, 520 + dy, IVORY, alpha=a)
        x += width(w, f)
    put(l, "Zanzibar", font(EBGI, 200), W / 2, 730, IVORY, alpha=0, anchor="c")
    return comp(veil(BG, "center", .4), shadow(l, 10, .55), l)


@design("Stretch/scatto: ZANZIBAR allungato con mosso orizzontale (a meta')")
def d20():
    l = layer()
    put(l, "ZANZIBAR", font(INTER, 230, 900), W / 2, 680, IVORY, anchor="c")
    box = l.getbbox()
    part = l.crop(box)
    part = part.resize((int(part.width * 1.25), part.height))
    l = layer()
    l.paste(part, (W // 2 - part.width // 2, box[1]))
    blur = l.filter(ImageFilter.BoxBlur(0))
    streak = l.resize((W // 40, H)).resize((W, H))
    streak.putalpha(streak.getchannel("A").point(lambda v: v // 3))
    l2 = layer()
    put(l2, "the beauty of", font(INTER, 50, 400), W / 2, 430, IVORY, track=10, anchor="c")
    return comp(veil(BG, "center", .4), streak, blur, l2)


thumbs = []
for i, (desc, fn) in enumerate(designs, 1):
    img = label(fn(), i, desc)
    img.save(os.path.join(HERE, "%02d.jpg" % i), quality=90)
    thumbs.append(img.resize((640, 360)))
for k in range(2):
    sheet = Image.new("RGB", (1280, 360 * 5))
    for j, t in enumerate(thumbs[k * 10:(k + 1) * 10]):
        sheet.paste(t, ((j % 2) * 640, (j // 2) * 360))
    sheet.save(os.path.join(HERE, "foglio-%d.jpg" % (k + 1)), quality=78)
print(len(designs), "titoli")
