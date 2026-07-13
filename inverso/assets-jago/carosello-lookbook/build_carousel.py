# -*- coding: utf-8 -*-
"""
Compone il carosello Instagram "The Lookbook System" per il brand Jago.
7 slide 1080x1350 (4:5). Foto still-life Higgsfield + tipografia EB Garamond,
palette dark-luxury della style guide. Output: slide-1..7.png + contact sheet.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import random

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "slides")
os.makedirs(OUT, exist_ok=True)
FONTS = os.path.join(BASE, "fonts")

W, H = 1080, 1350
MARGIN = 96

# Palette (style guide carosello)
BLACK   = (17, 17, 16)        # #111110
AMBER   = (199, 150, 78)      # accento caldo, leggermente piu' luminoso per leggibilita'
IVORY   = (237, 232, 220)     # #EDE8DC
MUTED   = (158, 148, 132)     # testo secondario su nero
WOOD    = (58, 42, 28)        # #3A2A1C

def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

REG  = "EBGaramond-Regular.ttf"
MED  = "EBGaramond-Medium.ttf"
SEMI = "EBGaramond-SemiBold.ttf"
ITAL = "EBGaramond-Italic.ttf"

# ---------- helpers ----------

def cover_crop(path, w=W, h=H, focus=0.5):
    """Ridimensiona e ritaglia l'immagine per riempire wxh (focus verticale 0..1)."""
    img = Image.open(path).convert("RGB")
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = int((nh - h) * focus)
    return img.crop((left, top, left + w, top + h))

def vgrad_overlay(img, top_a=0, bottom_a=210, color=(8, 8, 7)):
    """Sovrappone un gradiente verticale color con alpha che va da top_a a bottom_a."""
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

def darken(img, a=70, color=(8, 8, 7)):
    layer = Image.new("RGB", (W, H), color)
    return Image.blend(img, layer, a / 255)

def add_grain(img, amount=9):
    """Grana 35mm leggera per unire foto e slide tipografiche."""
    noise = Image.effect_noise((W, H), amount).convert("L")
    noise = ImageOps.autocontrast(noise)
    gl = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(img, gl, 0.05)

def text_w(draw, s, fnt, tracking=0):
    if tracking == 0:
        return draw.textlength(s, font=fnt)
    return sum(draw.textlength(c, font=fnt) + tracking for c in s) - tracking

def draw_tracked(draw, xy, s, fnt, fill, tracking=0, anchor_center=False):
    x, y = xy
    if anchor_center:
        x = x - text_w(draw, s, fnt, tracking) / 2
    for c in s:
        draw.text((x, y), c, font=fnt, fill=fill)
        x += draw.textlength(c, font=fnt) + tracking

def wrap(draw, s, fnt, maxw):
    words = s.split()
    lines, cur = [], ""
    for wd in words:
        test = (cur + " " + wd).strip()
        if draw.textlength(test, font=fnt) <= maxw:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def draw_block(draw, x, y, s, fnt, fill, maxw, leading=1.22, center=False):
    lines = wrap(draw, s, fnt, maxw)
    asc, desc = fnt.getmetrics()
    lh = int((asc + desc) * leading)
    for ln in lines:
        if center:
            lw = draw.textlength(ln, font=fnt)
            draw.text((x - lw / 2, y), ln, font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def eyebrow(draw, text, x, y, color=AMBER, size=25, tracking=6, center=False):
    f = font(MED, size)
    s = text.upper()
    if center:
        draw_tracked(draw, (x, y), s, f, color, tracking, anchor_center=True)
    else:
        draw_tracked(draw, (x, y), s, f, color, tracking)

def wordmark(draw, corner="bl", handle=None):
    f = font(ITAL, 40)
    s = "Jago"
    if corner == "bl":
        draw.text((MARGIN, H - MARGIN - 44), s, font=f, fill=IVORY)
    elif corner == "tl":
        draw.text((MARGIN, MARGIN - 6), s, font=f, fill=IVORY)
    if handle:
        fh = font(REG, 26)
        draw.text((MARGIN + draw.textlength(s, font=f) + 18, H - MARGIN - 30),
                  handle, font=fh, fill=MUTED)

def number(draw, n, x, y, color=MUTED):
    f = font(MED, 27)
    draw_tracked(draw, (x, y), f"{n} —", f, color, 3)

def amber_rule(draw, x, y, w=64, color=AMBER, h=2):
    draw.rectangle([x, y, x + w, y + h], fill=color)

def finish(img, name):
    img = add_grain(img)
    path = os.path.join(OUT, name)
    img.save(path, "PNG")
    print("saved", name)
    return path

# ================= SLIDE 1 — COVER =================
def slide1():
    img = cover_crop(os.path.join(BASE, "cover-A.png"), focus=0.45)
    img = vgrad_overlay(img, top_a=60, bottom_a=235)
    img = top_grad_overlay(img, top_a=120, bottom_a=0)
    d = ImageDraw.Draw(img)
    wordmark(d, "tl")
    # blocco titolo in basso, flusso dinamico per evitare collisioni
    eyebrow(d, "The Lookbook System", MARGIN, H - 524, AMBER, 25, 6)
    f_title = font(SEMI, 76)
    y = H - 476
    y = draw_block(d, MARGIN, y, "I built a fashion lookbook with AI.",
                   f_title, IVORY, W - 2 * MARGIN, leading=1.08)
    f_it = font(ITAL, 76)
    d.text((MARGIN, y + 6), "In one afternoon.", font=f_it, fill=AMBER)
    ia, idsc = f_it.getmetrics()
    y = y + 6 + ia + idsc
    f_sub = font(REG, 32)
    draw_tracked(d, (MARGIN, y + 22), "THE SYSTEM  —  SWIPE »", f_sub, MUTED, 3)
    finish(img, "slide-1.png")

# ================= SLIDE 2 — PRINCIPLE =================
def slide2():
    img = Image.new("RGB", (W, H), BLACK)
    # leggerissima texture in alto da detail per calore
    tx = cover_crop(os.path.join(BASE, "detail-A.png"), focus=0.3)
    tx = darken(tx, a=205)
    mask = Image.new("L", (1, H))
    for yy in range(H):
        mask.putpixel((0, yy), max(0, 70 - int(70 * yy / (H * 0.5))))
    mask = mask.resize((W, H))
    img = Image.composite(tx, img, mask)
    d = ImageDraw.Draw(img)
    number(d, "01", MARGIN, MARGIN + 4)
    cx = W // 2
    f_big = font(REG, 60)
    y = 470
    y = draw_block(d, cx, y, "The AI is not the creative director.",
                   f_big, IVORY, W - 2 * MARGIN, leading=1.18, center=True)
    y += 26
    f_punch = font(SEMI, 132)
    pw = d.textlength("You are.", font=f_punch)
    d.text((cx - pw / 2, y), "You are.", font=f_punch, fill=AMBER)
    y += 168
    amber_rule(d, cx - 32, y, 64)
    y += 34
    f_sub = font(ITAL, 35)
    draw_block(d, cx, y, "The tools only execute decisions you have already made.",
               f_sub, MUTED, W - 2 * MARGIN - 80, leading=1.3, center=True)
    wordmark(d, "bl")
    finish(img, "slide-2.png")

# ================= SLIDE 3 — THE BRIEF =================
def slide3():
    img = cover_crop(os.path.join(BASE, "desk-A.png"), focus=0.55)
    img = top_grad_overlay(img, top_a=232, bottom_a=10)
    img = vgrad_overlay(img, top_a=0, bottom_a=120)
    d = ImageDraw.Draw(img)
    number(d, "02", MARGIN, MARGIN + 4)
    eyebrow(d, "Step 1 · the brief", MARGIN, MARGIN + 52, AMBER, 24, 5)
    f_title = font(SEMI, 62)
    y = MARGIN + 96
    y = draw_block(d, MARGIN, y, "60% of the work happens before you open a tool.",
                   f_title, IVORY, W - 2 * MARGIN, leading=1.1)
    y += 18
    f_sub = font(REG, 34)
    y = draw_block(d, MARGIN, y, "Lock six pillars in writing:",
                   f_sub, MUTED, W - 2 * MARGIN, leading=1.3)
    # sei pilastri in due colonne
    pillars = ["Hero piece", "World", "Light", "Palette", "Model", "Mood"]
    f_p = font(MED, 37)
    y += 16
    col_x = [MARGIN + 10, W // 2 + 10]
    for i, p in enumerate(pillars):
        cx = col_x[i % 2]
        ry = y + (i // 2) * 62
        d.text((cx, ry), "·", font=f_p, fill=AMBER)
        d.text((cx + 26, ry), p, font=f_p, fill=IVORY)
    wordmark(d, "bl")
    finish(img, "slide-3.png")

# ================= SLIDE 4 — ONE WORLD =================
def slide4():
    img = cover_crop(os.path.join(BASE, "cover-B.png"), focus=0.5)
    img = vgrad_overlay(img, top_a=70, bottom_a=238)
    d = ImageDraw.Draw(img)
    number(d, "03", MARGIN, MARGIN + 4)
    eyebrow(d, "the golden rule", MARGIN, H - 452, AMBER, 24, 5)
    f_title = font(SEMI, 70)
    y = H - 408
    y = draw_block(d, MARGIN, y, "Real campaigns never change worlds.",
                   f_title, IVORY, W - 2 * MARGIN, leading=1.08)
    y += 16
    f_sub = font(REG, 33)
    draw_block(d, MARGIN, y,
               "Five shots inside one world: full body, three-quarter, close-up, wide, and one detail with no face.",
               f_sub, MUTED, W - 2 * MARGIN, leading=1.32)
    finish(img, "slide-4.png")

# ================= SLIDE 5 — THE MISTAKES =================
def slide5():
    img = Image.new("RGB", (W, H), BLACK)
    tx = cover_crop(os.path.join(BASE, "detail-B.png"), focus=0.5)
    tx = darken(tx, a=210)
    mask = Image.new("L", (1, H))
    for yy in range(H):
        t = yy / (H - 1)
        mask.putpixel((0, yy), max(0, int(60 * (t - 0.6) / 0.4)) if t > 0.6 else 0)
    mask = mask.resize((W, H))
    img = Image.composite(tx, img, mask)
    d = ImageDraw.Draw(img)
    number(d, "04", MARGIN, MARGIN + 4)
    eyebrow(d, "the tells", MARGIN, MARGIN + 52, AMBER, 24, 5)
    f_title = font(SEMI, 64)
    y = MARGIN + 96
    y = draw_block(d, MARGIN, y, "What screams “AI”:", f_title, IVORY, W - 2 * MARGIN, leading=1.1)
    y += 40
    items = [
        "Different light in every shot",
        "Changing the world between shots",
        "Over-polished skin and poses",
    ]
    f_i = font(REG, 41)
    f_x = font(MED, 44)
    for it in items:
        d.text((MARGIN, y - 2), "×", font=f_x, fill=AMBER)
        d.text((MARGIN + 52, y), it, font=f_i, fill=IVORY)
        y += 78
    y += 26
    amber_rule(d, MARGIN, y, 64)
    y += 30
    f_sub = font(ITAL, 37)
    draw_block(d, MARGIN, y, "Real campaigns have wind, weight, gravity.",
               f_sub, MUTED, W - 2 * MARGIN, leading=1.3)
    wordmark(d, "bl")
    finish(img, "slide-5.png")

# ================= SLIDE 6 — THE VALUE =================
def slide6():
    img = cover_crop(os.path.join(BASE, "detail-A.png"), focus=0.5)
    img = vgrad_overlay(img, top_a=30, bottom_a=232)
    d = ImageDraw.Draw(img)
    number(d, "05", MARGIN, MARGIN + 4)
    f_title = font(SEMI, 66)
    y = H - 400
    y = draw_block(d, MARGIN, y, "Wrong light kills a lookbook faster than a wrong face.",
                   f_title, IVORY, W - 2 * MARGIN, leading=1.1)
    y += 18
    f_sub = font(ITAL, 36)
    draw_block(d, MARGIN, y, "Five strong images beat fifteen average ones.",
               f_sub, AMBER, W - 2 * MARGIN, leading=1.3)
    wordmark(d, "bl")
    finish(img, "slide-6.png")

# ================= SLIDE 7 — CTA =================
def slide7():
    img = cover_crop(os.path.join(BASE, "jago-cta.png"), focus=0.4)
    img = vgrad_overlay(img, top_a=40, bottom_a=243)
    img = top_grad_overlay(img, top_a=120, bottom_a=0)
    d = ImageDraw.Draw(img)
    f_wm = font(ITAL, 46)
    d.text((MARGIN, MARGIN - 10), "Jago", font=f_wm, fill=IVORY)
    eyebrow(d, "Built with AI · directed by a human", MARGIN, H - 430, AMBER, 24, 4)
    f_title = font(SEMI, 62)
    y = H - 384
    y = draw_block(d, MARGIN, y, "Want the full three-step system?",
                   f_title, IVORY, W - 2 * MARGIN, leading=1.12)
    y += 14
    f_sub = font(REG, 36)
    y = draw_block(d, MARGIN, y, "Comment LOOKBOOK and I’ll send you the PDF.",
                   f_sub, IVORY, W - 2 * MARGIN, leading=1.28)
    y += 22
    f_h = font(MED, 30)
    draw_tracked(d, (MARGIN, y), "@JAGOWORKS  ·  BYJAGO.BEEHIIV.COM", f_h, MUTED, 2)
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
    random.seed(7)
    slide1(); slide2(); slide3(); slide4(); slide5(); slide6(); slide7()
    contact_sheet()
    print("DONE")
