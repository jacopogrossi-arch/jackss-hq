# -*- coding: utf-8 -*-
"""
Copertina Instagram/YouTube per il Video #5 "SCIROCCO" (Jago).
1080x1920 (9:16). Foto reale shot1 (full body, lava rock) + tipografia EB Garamond,
palette locked nel brief SCIROCCO (off-white / sand-ocra / basalto nero / blu mare).
Output: variante-1.png, variante-2.png, variante-3.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(BASE, "..", "..", "assets", "carosello-lookbook", "fonts")
SHOT1 = "C:/Users/Jacopo Grossi/Downloads/video 5/hf_20260627_192921_7b3031dc-8a0f-491c-b6da-a066663f25ab.png"

W, H = 1080, 1920
MARGIN = 90

# Palette — locked nel brief SCIROCCO (video-5-brief-scirocco.md)
OFFWHITE = (237, 231, 216)
SAND     = (196, 156, 96)
BASALT   = (16, 14, 12)
DEEPBLUE = (40, 72, 96)
MUTED    = (170, 161, 145)

def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

REG  = "EBGaramond-Regular.ttf"
MED  = "EBGaramond-Medium.ttf"
SEMI = "EBGaramond-SemiBold.ttf"
ITAL = "EBGaramond-Italic.ttf"

def cover_crop(path, w=W, h=H, focus=0.42):
    img = Image.open(path).convert("RGB")
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = int((nh - h) * focus)
    return img.crop((left, top, left + w, top + h))

def vgrad_overlay(img, top_a=0, bottom_a=215, color=BASALT):
    grad = Image.new("L", (1, H))
    for y in range(H):
        t = y / (H - 1)
        grad.putpixel((0, y), int(top_a + (bottom_a - top_a) * t))
    grad = grad.resize((W, H))
    layer = Image.new("RGB", (W, H), color)
    return Image.composite(layer, img, grad)

def top_grad_overlay(img, top_a=140, bottom_a=0, color=BASALT):
    grad = Image.new("L", (1, H))
    for y in range(H):
        t = y / (H - 1)
        grad.putpixel((0, y), int(top_a + (bottom_a - top_a) * t))
    grad = grad.resize((W, H))
    layer = Image.new("RGB", (W, H), color)
    return Image.composite(layer, img, grad)

def add_grain(img, amount=8):
    noise = Image.effect_noise((W, H), amount).convert("L")
    noise = ImageOps.autocontrast(noise)
    gl = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(img, gl, 0.045)

def text_w(draw, s, fnt, tracking=0):
    if tracking == 0:
        return draw.textlength(s, font=fnt)
    return sum(draw.textlength(c, font=fnt) + tracking for c in s) - tracking

def draw_tracked(draw, xy, s, fnt, fill, tracking=0, center_x=None):
    x, y = xy
    if center_x is not None:
        x = center_x - text_w(draw, s, fnt, tracking) / 2
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

def draw_block(draw, x, y, s, fnt, fill, maxw, leading=1.15, center=False):
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

def rule(draw, x, y, w=70, color=SAND, h=2):
    draw.rectangle([x, y, x + w, y + h], fill=color)

def pill(draw, text, cx, y, fnt, fg=BASALT, bg=SAND, pad_x=28, pad_y=14):
    tw = draw.textlength(text, font=fnt)
    asc, desc = fnt.getmetrics()
    th = asc + desc
    x0 = cx - tw / 2 - pad_x
    x1 = cx + tw / 2 + pad_x
    y0, y1 = y, y + th + pad_y * 2
    draw.rounded_rectangle([x0, y0, x1, y1], radius=(y1 - y0) / 2, fill=bg)
    draw.text((cx - tw / 2, y0 + pad_y - 2), text, font=fnt, fill=fg)
    return y1

def finish(img, name):
    img = add_grain(img)
    path = os.path.join(BASE, name)
    img.save(path, "PNG")
    print("saved", name)

# ============== VARIANTE 1 — title card, tagline brand ==============
def variante1():
    img = cover_crop(SHOT1, focus=0.40)
    img = vgrad_overlay(img, top_a=10, bottom_a=225)
    d = ImageDraw.Draw(img)
    draw_tracked(d, (MARGIN, MARGIN), "JAGO · VIDEO N°5", font(MED, 28), SAND, 4)

    y = H - 560
    draw_tracked(d, (MARGIN, y), "A SICILIAN RESORT LABEL", font(MED, 26), SAND, 5)
    y += 56
    f_title = font(SEMI, 128)
    d.text((MARGIN, y), "SCIROCCO", font=f_title, fill=OFFWHITE)
    y += 150
    f_tag = font(ITAL, 42)
    y = draw_block(d, MARGIN, y, "Sun-bleached linen, in Mediterranean heat.",
                    f_tag, SAND, W - 2 * MARGIN, leading=1.2)
    y += 22
    rule(d, MARGIN, y, 70)
    y += 30
    f_sub = font(REG, 32)
    draw_block(d, MARGIN, y, "Built with AI. Five looks, one world, 47 minutes.",
               f_sub, MUTED, W - 2 * MARGIN, leading=1.3)
    finish(img, "variante-1.png")

# ============== VARIANTE 2 — hook numerico (47 minuti) ==============
def variante2():
    img = cover_crop(SHOT1, focus=0.38)
    img = vgrad_overlay(img, top_a=20, bottom_a=232)
    img = top_grad_overlay(img, top_a=130, bottom_a=0)
    d = ImageDraw.Draw(img)
    draw_tracked(d, (MARGIN, MARGIN), "JAGO · VIDEO N°5", font(MED, 28), OFFWHITE, 4)

    cx = W // 2
    y = H - 700
    draw_tracked(d, (0, y), "A FULL FASHION CAMPAIGN, BUILT IN", font(MED, 26), SAND, 4, center_x=cx)
    y += 60
    f_num = font(SEMI, 250)
    num = "47"
    nw = d.textlength(num, font=f_num)
    d.text((cx - nw / 2, y), num, font=f_num, fill=OFFWHITE)
    y += 250
    draw_tracked(d, (0, y), "MINUTES", font(SEMI, 54), SAND, 14, center_x=cx)
    y += 110
    rule(d, cx - 35, y, 70)
    y += 36
    f_sub = font(ITAL, 36)
    y = draw_block(d, cx, y, "No photographer. No Sicily. Just a brief.",
                    f_sub, MUTED, W - 2 * MARGIN, leading=1.3, center=True)
    y += 30
    pill(d, "COMMENT “LOOKBOOK”", cx, y, font(MED, 28), fg=BASALT, bg=SAND)
    finish(img, "variante-2.png")

# ============== VARIANTE 3 — editorial/magazine, registro alto ==============
def variante3():
    img = cover_crop(SHOT1, focus=0.42)
    img = vgrad_overlay(img, top_a=0, bottom_a=195)
    d = ImageDraw.Draw(img)
    draw_tracked(d, (MARGIN, MARGIN), "JAGO", font(ITAL, 40), OFFWHITE, 0)
    draw_tracked(d, (MARGIN, MARGIN + 56), "VIDEO N°5 · SICILY", font(MED, 24), SAND, 4)

    # colonna verticale a destra, registro editoriale
    f_v = font(MED, 24)
    vtext = "VOLCANIC LUXURY"
    vimg = Image.new("RGBA", (400, 40), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vimg)
    draw_tracked(vd, (0, 0), vtext, f_v, SAND, 6)
    vimg = vimg.rotate(90, expand=True)
    img.paste(vimg, (W - MARGIN - vimg.width, H // 2 - vimg.height // 2), vimg)

    y = H - 470
    f_title = font(SEMI, 108)
    d.text((MARGIN, y), "SCIROCCO", font=f_title, fill=OFFWHITE)
    y += 128
    rule(d, MARGIN, y, 70)
    y += 28
    f_sub = font(REG, 33)
    draw_block(d, MARGIN, y, "I built a professional lookbook in 47 minutes.",
               f_sub, MUTED, W - 2 * MARGIN - 40, leading=1.3)
    finish(img, "variante-3.png")

if __name__ == "__main__":
    variante1(); variante2(); variante3()
    print("DONE")
