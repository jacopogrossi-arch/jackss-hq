# -*- coding: utf-8 -*-
"""
Compone il carosello Instagram "What a EUR20,000 lookbook costs" per il brand Jago.
7 slide 1080x1350 (4:5). Foto Higgsfield Nano Banana Pro (stile VESPRO/Capri) +
tipografia Apple Garamond, palette dark-luxury della style guide.
Output: slide-1..7.png + contact sheet.

Font: Apple Garamond Bold Italic come font protagonista (titoli e righe editoriali).
Apple Garamond dritto (Bold/Regular) per eyebrow maiuscoli e numeri/prezzi.
Nota: Apple Garamond non contiene il glifo euro, quindi il simbolo (euro) viene
disegnato in EB Garamond (stessa famiglia serif) inline coi numeri Apple Garamond.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "slides")
os.makedirs(OUT, exist_ok=True)
FONTS = os.path.join(BASE, "fonts")

EURO = "€"  # simbolo euro

W, H = 1080, 1350
MARGIN = 96

# Palette (style guide carosello) - INVARIATA
BLACK = (17, 17, 16)        # #111110
AMBER = (199, 150, 78)      # #C7964E accento caldo
IVORY = (237, 232, 220)     # #EDE8DC
MUTED = (158, 148, 132)     # #9E9484 testo secondario

# Font roles - Apple Garamond
DISP = "AppleGaramond-BoldItalic.ttf"   # titoli + righe editoriali (protagonista)
BOLD = "AppleGaramond-Bold.ttf"         # eyebrow uppercase, prezzi upright
REG  = "AppleGaramond.ttf"              # corpo
# Font euro (EB Garamond, solo per il glifo euro)
EURO_IT = "EBGaramond-Italic.ttf"       # da abbinare al display bold-italic
EURO_UP = "EBGaramond-SemiBold.ttf"     # da abbinare al bold upright

def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

# ---------- helpers immagine ----------

def cover_crop(path, w=W, h=H, focus=0.5):
    img = Image.open(path).convert("RGB")
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = int((nh - h) * focus)
    return img.crop((left, top, left + w, top + h))

def vgrad_overlay(img, top_a=0, bottom_a=210, color=(8, 8, 7)):
    grad = Image.new("L", (1, H))
    for y in range(H):
        t = y / (H - 1)
        grad.putpixel((0, y), int(top_a + (bottom_a - top_a) * t))
    grad = grad.resize((W, H))
    layer = Image.new("RGB", (W, H), color)
    return Image.composite(layer, img, grad)

def top_grad_overlay(img, top_a=205, bottom_a=0, color=(8, 8, 7)):
    grad = Image.new("L", (1, H))
    for y in range(H):
        t = y / (H - 1)
        grad.putpixel((0, y), int(top_a + (bottom_a - top_a) * t))
    grad = grad.resize((W, H))
    layer = Image.new("RGB", (W, H), color)
    return Image.composite(layer, img, grad)

def band(img, y0, y1, a=200, color=(8, 8, 7)):
    """Banda scura sfumata per far leggere il testo su foto chiare."""
    grad = Image.new("L", (1, H), 0)
    feather = 140
    for y in range(H):
        if y0 - feather <= y < y0:
            v = int(a * (y - (y0 - feather)) / feather)
        elif y0 <= y <= y1:
            v = a
        elif y1 < y <= y1 + feather:
            v = int(a * (1 - (y - y1) / feather))
        else:
            v = 0
        grad.putpixel((0, y), max(0, min(255, v)))
    grad = grad.resize((W, H))
    layer = Image.new("RGB", (W, H), color)
    return Image.composite(layer, img, grad)

def darken(img, a=70, color=(8, 8, 7)):
    layer = Image.new("RGB", (W, H), color)
    return Image.blend(img, layer, a / 255)

def add_grain(img, amount=9):
    noise = Image.effect_noise((W, H), amount).convert("L")
    noise = ImageOps.autocontrast(noise)
    gl = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(img, gl, 0.05)

# ---------- helpers testo (euro-aware) ----------

def _fnt_for(c, main_fnt, euro_fnt):
    return euro_fnt if (c == EURO and euro_fnt is not None) else main_fnt

def text_w(draw, s, main_fnt, euro_fnt=None, tracking=0):
    if not s:
        return 0
    w = 0
    for c in s:
        w += draw.textlength(c, font=_fnt_for(c, main_fnt, euro_fnt)) + tracking
    return w - tracking

def draw_line(draw, xy, s, main_fnt, fill, euro_fnt=None, tracking=0, anchor="left"):
    x, y = xy
    total = text_w(draw, s, main_fnt, euro_fnt, tracking)
    if anchor == "center":
        x -= total / 2
    elif anchor == "right":
        x -= total
    for c in s:
        f = _fnt_for(c, main_fnt, euro_fnt)
        draw.text((x, y), c, font=f, fill=fill)
        x += draw.textlength(c, font=f) + tracking

def wrap(draw, s, main_fnt, maxw, euro_fnt=None):
    words = s.split()
    lines, cur = [], ""
    for wd in words:
        test = (cur + " " + wd).strip()
        if text_w(draw, test, main_fnt, euro_fnt) <= maxw:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def draw_block(draw, x, y, s, main_fnt, fill, maxw, euro_fnt=None, leading=1.22, center=False):
    lines = wrap(draw, s, main_fnt, maxw, euro_fnt)
    asc, desc = main_fnt.getmetrics()
    lh = int((asc + desc) * leading)
    for ln in lines:
        draw_line(draw, (x, y), ln, main_fnt, fill, euro_fnt,
                  anchor="center" if center else "left")
        y += lh
    return y

def eyebrow(draw, text, x, y, color=AMBER, size=27, tracking=6, center=False):
    f = font(BOLD, size)
    draw_line(draw, (x, y), text.upper(), f, color, tracking=tracking,
              anchor="center" if center else "left")

def amber_rule(draw, x, y, w=64, color=AMBER, h=2):
    draw.rectangle([x, y, x + w, y + h], fill=color)

def wordmark(draw, corner="tl"):
    f = font(DISP, 46)
    s = "Jago"
    if corner == "tl":
        draw.text((MARGIN, MARGIN - 12), s, font=f, fill=IVORY)
    elif corner == "bl":
        draw.text((MARGIN, H - MARGIN - 48), s, font=f, fill=IVORY)

def finish(img, name):
    img = add_grain(img)
    path = os.path.join(OUT, name)
    img.save(path, "PNG")
    print("saved", name)
    return path

# ================= SLIDE 1 - COVER =================
def slide1():
    img = cover_crop(os.path.join(BASE, "IMG-1-cover.png"), focus=0.5)
    img = band(img, H - 470, H, a=226)
    d = ImageDraw.Draw(img)
    y = H - 470
    eyebrow(d, "Jago", MARGIN, y, AMBER, 27, 6)
    y += 56
    f_title = font(DISP, 62)
    eu_it = font(EURO_IT, 58)
    y = draw_block(d, MARGIN, y, "A lookbook like a major fashion brand's costs " + EURO + "20,000.",
                   f_title, IVORY, W - 2 * MARGIN, euro_fnt=eu_it, leading=1.06)
    y += 6
    draw_line(d, (MARGIN, y), "Mine costs " + EURO + "400.", f_title, AMBER, euro_fnt=eu_it)
    ia, idsc = f_title.getmetrics()
    y += int((ia + idsc) * 1.05)
    draw_line(d, (MARGIN, y + 18), "HERE'S THE MATH  -  SWIPE " + "»",
              font(BOLD, 28), MUTED, tracking=4)
    finish(img, "slide-1.png")

# ================= SLIDE 2 - WHAT BRANDS PAY =================
def slide2():
    img = Image.new("RGB", (W, H), BLACK)
    tx = cover_crop(os.path.join(BASE, "IMG-2-tessuto.png"), focus=0.28)
    tx = darken(tx, a=214)
    mask = Image.new("L", (1, H))
    for yy in range(H):
        mask.putpixel((0, yy), max(0, 58 - int(58 * yy / (H * 0.5))))
    mask = mask.resize((W, H))
    img = Image.composite(tx, img, mask)
    d = ImageDraw.Draw(img)
    eyebrow(d, "What brands actually pay for", MARGIN, MARGIN + 8, AMBER, 26, 4)
    rows = [
        ("Creative director", "3,000"),
        ("Photographer", "2,500"),
        ("Studio rental", "800"),
        ("Models", "2,400"),
        ("Retouching", "2,250"),
        ("Art direction", "2,000"),
    ]
    f_role = font(DISP, 50)
    f_price = font(BOLD, 50)
    eu_up = font(EURO_UP, 44)
    y = MARGIN + 96
    rx = W - MARGIN
    for role, price in rows:
        d.text((MARGIN, y), role, font=f_role, fill=IVORY)
        s = EURO + price
        pw = text_w(d, s, f_price, eu_up)
        draw_line(d, (rx - pw, y + 2), s, f_price, MUTED, euro_fnt=eu_up)
        y += 96
        d.line([(MARGIN, y - 20), (rx, y - 20)], fill=(48, 46, 42), width=1)
    y += 30
    amber_rule(d, MARGIN, y, 64)
    y += 36
    draw_line(d, (MARGIN, y), "TOTAL", font(BOLD, 30), MUTED, tracking=5)
    y += 52
    f_tot = font(DISP, 90)
    eu_tot = font(EURO_IT, 84)
    s1 = EURO + "15,000"
    draw_line(d, (MARGIN, y), s1, f_tot, AMBER, euro_fnt=eu_tot)
    w1 = text_w(d, s1, f_tot, eu_tot)
    f_tot2 = font(DISP, 56)
    eu_tot2 = font(EURO_IT, 52)
    draw_line(d, (MARGIN + w1 + 16, y + 30), "- " + EURO + "25,000", f_tot2, IVORY, euro_fnt=eu_tot2)
    finish(img, "slide-2.png")

# ================= SLIDE 3 - RESPIRO (tessuto, no testo) =================
def slide3():
    img = cover_crop(os.path.join(BASE, "IMG-2-tessuto.png"), focus=0.5)
    finish(img, "slide-3.png")

# ================= SLIDE 4 - WHAT CHANGES WITH AI =================
def slide4():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    cx = W // 2
    eyebrow(d, "What changes with AI", cx, MARGIN + 40, AMBER, 26, 4, center=True)
    f_big = font(DISP, 58)
    y = 460
    y = draw_block(d, cx, y,
                   "The vision is still yours. The taste is still yours. The creative decisions are still yours.",
                   f_big, IVORY, W - 2 * MARGIN - 30, leading=1.2, center=True)
    y += 46
    amber_rule(d, cx - 32, y, 64)
    y += 44
    draw_block(d, cx, y, "Only the execution changes.", font(DISP, 50), AMBER,
               W - 2 * MARGIN, leading=1.2, center=True)
    finish(img, "slide-4.png")

# ================= SLIDE 5 - TERRAZZA (deliverable) =================
def slide5():
    img = cover_crop(os.path.join(BASE, "IMG-3-terrazza.png"), focus=0.5)
    img = band(img, H - 195, H, a=212)
    d = ImageDraw.Draw(img)
    draw_line(d, (MARGIN, H - 150), "10-15 IMAGES   " + "·" + "   48 HOURS",
              font(BOLD, 34), IVORY, tracking=4)
    finish(img, "slide-5.png")

# ================= SLIDE 6 - THE OFFER =================
def slide6():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    cx = W // 2
    eyebrow(d, "The offer", cx, 360, AMBER, 27, 5, center=True)
    f_punch = font(DISP, 188)
    eu_punch = font(EURO_IT, 168)
    s = EURO + "400"
    pw = text_w(d, s, f_punch, eu_punch)
    draw_line(d, (cx, 430), s, f_punch, AMBER, euro_fnt=eu_punch, anchor="center")
    f_flat = font(DISP, 60)
    draw_line(d, (cx, 668), "flat.", f_flat, IVORY, anchor="center")
    y = 800
    amber_rule(d, cx - 32, y, 64)
    y += 42
    y = draw_block(d, cx, y, "Campaign-quality lookbook in 48-72 hours.",
                   font(DISP, 44), IVORY, W - 2 * MARGIN, leading=1.24, center=True)
    y += 20
    draw_block(d, cx, y,
               "First 3 brands get the pilot price - in exchange for a case study.",
               font(REG, 38), MUTED, W - 2 * MARGIN - 40, leading=1.32, center=True)
    finish(img, "slide-6.png")

# ================= SLIDE 7 - CTA =================
def slide7():
    img = cover_crop(os.path.join(BASE, "IMG-4-cta.png"), focus=0.42)
    img = band(img, H - 430, H, a=234)
    img = top_grad_overlay(img, top_a=120, bottom_a=0)
    d = ImageDraw.Draw(img)
    wordmark(d, "tl")
    y = H - 400
    y = draw_block(d, MARGIN, y, "If you're launching a collection, you know where to find me.",
                   font(DISP, 56), IVORY, W - 2 * MARGIN, leading=1.12)
    y += 28
    draw_line(d, (MARGIN, y), "COMMENT  LOOKBOOK", font(BOLD, 40), AMBER, tracking=3)
    y += 66
    draw_line(d, (MARGIN, y), "@JAGOWORKS   " + "·" + "   BYJAGO.BEEHIIV.COM",
              font(BOLD, 27), MUTED, tracking=2)
    finish(img, "slide-7.png")

def contact_sheet():
    cols, rows = 4, 2
    pad = 20
    tw = (W // 4)
    th = (H // 4)
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * pad, rows * th + (rows + 1) * pad), (24, 24, 22))
    for i in range(1, 8):
        im = Image.open(os.path.join(OUT, f"slide-{i}.png")).resize((tw, th), Image.LANCZOS)
        idx = i - 1
        r, c = idx // cols, idx % cols
        x = pad + c * (tw + pad)
        y = pad + r * (th + pad)
        sheet.paste(im, (x, y))
    sheet.save(os.path.join(OUT, "contact-sheet.png"))
    print("saved contact-sheet.png")

if __name__ == "__main__":
    slide1(); slide2(); slide3(); slide4(); slide5(); slide6(); slide7()
    contact_sheet()
    print("DONE")
