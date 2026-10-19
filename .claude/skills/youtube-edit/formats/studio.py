"""studio.py: four "explainer" formats, built from the inspiration study of 19/10/2026 (Iman Gadzhi, Callaway, Pedro Andrade, Marshall Crew).

Why these four: in every reference the graphic IS the explanation, built piece by piece on the spoken word, with real objects,
a camera that moves through space and one visual identity. The older formats show a thing and then hold it still.

  build     (Marshall)  items appear one after another ON THEIR WORD: picture -> label -> value (swatch, "BRUSHED FLEECE", "500 GSM")
  annotate  (Marshall)  one picture (a technical flat, a garment) and callouts whose lines DRAW onto it, each on its word
  orbit     (Callaway)  a card (beside the speaker, then carried into a dark space) with satellites that fly in and connect to it
  dive      (Iman)      zoom into one spot of a screen / page, click, then zoom OUT to reveal the whole thing
  agenda    (Marshall)  a fixed list beside the speaker that gets one more line at every topic and stays

Style: every colour and the font are CSS variables (--k-*) set in css(); a storyboard can override them with "style": {"accent": "#..."}.
Usage inside compose.py: css = studio.css(S.get("style")); then for a beat b: inner, lines, hostless = studio.<type>(...).
All motion is seek-safe (tweens only, hidden start states set by fromTo).
"""
import math, html as _h

esc = lambda s: _h.escape(str(s), quote=True)

DEFAULT_STYLE = {
    "bg": "#0b0907", "bg2": "#1b140d", "text": "#f4efe6", "mute": "rgba(244,239,230,.62)",
    "accent": "#d4af5f", "accent2": "#3f9a78", "accent3": "#e9e2d2",
    "chip": "#f4efe6", "chip_text": "#15100b",
    "font": '"DM Sans", ui-sans-serif, system-ui, sans-serif',
    "hand": '"Caveat", "Segoe Print", cursive',
    "serif": '"Instrument Serif", "Georgia", serif',
}


_TEMPLATE = """
  :root { --k-bg:@bg@; --k-bg2:@bg2@; --k-text:@text@; --k-mute:@mute@; --k-accent:@accent@; --k-accent2:@accent2@; --k-accent3:@accent3@;
          --k-chip:@chip@; --k-chip-text:@chip_text@; --k-font:@font@; --k-hand:@hand@; --k-serif:@serif@; }
  /* ---- studio formats: a calm dark wash, no grid ---- */
  .k-cut { position:absolute; inset:0; font-family:var(--k-font); color:var(--k-text); background:
      radial-gradient(1100px 700px at 50% 112%, color-mix(in srgb, var(--k-accent) 26%, transparent), transparent 70%),
      radial-gradient(900px 600px at 10% 0%, color-mix(in srgb, var(--k-accent2) 18%, transparent), transparent 70%), var(--k-bg); overflow:hidden; }
  .k-title { position:absolute; left:0; right:0; top:70px; text-align:center; font-weight:700; font-size:54px; letter-spacing:.02em; color:var(--k-text); opacity:0; }
  /* build */
  .k-row { position:absolute; left:0; right:0; top:170px; bottom:120px; display:flex; justify-content:center; align-items:center; gap:90px; }
  .k-item { display:flex; flex-direction:column; align-items:center; gap:26px; width:480px; }
  .k-img { height:430px; display:flex; align-items:flex-end; justify-content:center; opacity:0; }
  .k-img img { max-width:520px; max-height:430px; object-fit:contain; filter: drop-shadow(0 30px 40px rgba(0,0,0,.55)); }
  .k-label { position:relative; font-weight:700; font-size:52px; line-height:1; letter-spacing:.05em; text-transform:uppercase; padding:6px 6px 14px; white-space:nowrap; opacity:0;
    background:linear-gradient(90deg, var(--k-text) 8%, var(--k-accent) 100%); -webkit-background-clip:text; background-clip:text; color:transparent;
    filter: drop-shadow(0 0 16px color-mix(in srgb, var(--k-accent) 50%, transparent)) drop-shadow(0 4px 10px rgba(0,0,0,.75)); }
  .k-label::after { content:""; position:absolute; left:6%; right:6%; bottom:0; height:3px; border-radius:2px; background:linear-gradient(90deg, transparent, var(--k-accent), transparent); }
  .k-value { font-weight:700; font-size:40px; line-height:1; letter-spacing:.06em; white-space:nowrap; color:var(--k-accent); opacity:0;
    text-shadow:0 0 22px color-mix(in srgb, var(--k-accent) 55%, transparent), 0 3px 10px rgba(0,0,0,.7); }
  /* annotate */
  .k-an-wrap { position:absolute; inset:0; }
  .k-an-img { position:absolute; opacity:0; }
  .k-an-img img { width:100%; height:100%; object-fit:contain; filter: drop-shadow(0 26px 40px rgba(0,0,0,.5)); }
  .k-an-img.page { border-radius:14px; overflow:hidden; box-shadow:0 50px 120px rgba(0,0,0,.65), 0 0 0 2px rgba(255,255,255,.14); background:#0b0907; }
  .k-an-img.page img { filter:none; object-fit:fill; }
  .k-sp-stage { position:absolute; inset:0; perspective:2400px; perspective-origin:50% 42%; }
  .k-sp-rig { position:absolute; inset:0; transform-style:preserve-3d; }
  .k-an-svg { position:absolute; inset:0; width:1920px; height:1080px; overflow:visible; }
  .k-an-svg line, .k-an-svg polyline { fill:none; stroke-width:4; stroke-linecap:round; stroke-linejoin:round; }
  .k-an-dot { position:absolute; width:22px; height:22px; margin:-11px 0 0 -11px; border-radius:50%; opacity:0; border:4px solid #fff; box-sizing:border-box; }
  .k-an-lab { position:absolute; opacity:0; max-width:520px; }
  .k-an-lab .t { font-weight:700; font-size:34px; line-height:1.05; letter-spacing:.05em; text-transform:uppercase; }
  .k-an-lab .s { font-weight:500; font-size:25px; line-height:1.15; margin-top:6px; color:var(--k-mute); }
  .k-an-lab.r { text-align:left; } .k-an-lab.l { text-align:right; }
  /* orbit */
  .k-or-scrim { position:absolute; inset:0; opacity:0; background:
      radial-gradient(1200px 520px at 50% 118%, color-mix(in srgb, var(--k-accent) 40%, transparent), transparent 70%), var(--k-bg); }
  .k-or-svg { position:absolute; inset:0; width:1920px; height:1080px; overflow:visible; }
  .k-or-svg line { stroke:var(--k-accent); stroke-width:2.5; stroke-opacity:.62; stroke-linecap:round; }
  .k-or-stage { position:absolute; inset:0; perspective:2200px; perspective-origin:50% 45%; }
  .k-or-rig { position:absolute; inset:0; transform-style:preserve-3d; }
  .k-or-card { position:absolute; left:960px; top:540px; border-radius:30px; overflow:hidden; opacity:0; translate:-50% -50%;
    background:linear-gradient(160deg, color-mix(in srgb, var(--k-accent) 70%, #2a1d63), color-mix(in srgb, var(--k-accent2) 60%, #140d3a));
    box-shadow:0 50px 120px rgba(0,0,0,.6), 0 0 0 2px rgba(255,255,255,.18); display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }
  .k-or-card img { width:100%; height:100%; object-fit:contain; }
  .k-or-card .t { font-weight:700; font-size:92px; line-height:.95; letter-spacing:-.01em; color:#fff; text-transform:uppercase; padding:0 24px; }
  .k-or-card .s { font-weight:500; font-size:30px; margin-top:18px; color:rgba(255,255,255,.8); padding:0 30px; }
  .k-or-node { position:absolute; width:170px; margin:-85px 0 0 -85px; display:flex; flex-direction:column; align-items:center; gap:12px; opacity:0; }
  .k-or-disc { width:150px; height:150px; border-radius:50%; overflow:hidden; background:#fff; border:5px solid var(--k-accent); box-shadow:0 18px 50px rgba(0,0,0,.55);
    display:flex; align-items:center; justify-content:center; box-sizing:border-box; }
  .k-or-disc img { width:100%; height:100%; object-fit:cover; } .k-or-disc.logo img { width:64%; height:64%; object-fit:contain; }
  .k-or-disc .ltr { font-weight:700; font-size:30px; letter-spacing:.02em; color:var(--k-chip-text); }
  .k-or-cap { font-weight:700; font-size:26px; letter-spacing:.05em; text-transform:uppercase; color:var(--k-text); text-shadow:0 2px 10px rgba(0,0,0,.8); white-space:nowrap; }
  /* dive */
  .k-dv-wrap { position:absolute; inset:0; perspective:2400px; perspective-origin:50% 40%; }
  .k-dv-stage { position:absolute; inset:0; transform-style:preserve-3d; opacity:0; }
  .k-dv-cam { position:absolute; left:0; top:0; width:1920px; height:1080px; transform-origin:0 0; }
  .k-dv-frame { position:absolute; border-radius:18px; overflow:hidden; background:#0b0907; box-shadow:0 60px 140px rgba(0,0,0,.65), 0 0 0 2px rgba(255,255,255,.16); }
  .k-dv-frame img { width:100%; height:100%; display:block; object-fit:fill; }
  .k-cursor { position:absolute; left:0; top:0; width:70px; height:70px; margin:-6px 0 0 -6px; opacity:0; z-index:5; filter:drop-shadow(0 4px 8px rgba(0,0,0,.55)); }
  .k-ring { position:absolute; left:0; top:0; width:90px; height:90px; margin:-45px 0 0 -45px; border-radius:50%; border:5px solid var(--k-accent); opacity:0; z-index:4; }
  /* trail: a page rests, then the camera pulls back and an arrow leads to the next thing */
  .k-tr-stage { position:absolute; inset:0; perspective:2600px; perspective-origin:50% 42%; }
  .k-tr-rig { position:absolute; inset:0; transform-style:preserve-3d; transform-origin:960px 540px; }
  .k-tr-svg { position:absolute; inset:0; width:1920px; height:1080px; overflow:visible; }
  .k-tr-svg .ln { fill:none; stroke-width:5; stroke-linecap:round; } .k-tr-svg .hd { stroke:none; }
  .k-tr-node { position:absolute; translate:-50% -50%; opacity:0; }
  .k-tr-page { border-radius:14px; overflow:hidden; box-shadow:0 50px 120px rgba(0,0,0,.65), 0 0 0 2px rgba(255,255,255,.14); background:#0b0907; }
  .k-tr-page img { width:100%; height:100%; display:block; object-fit:fill; }
  .k-tr-key { font-family:var(--k-font); font-weight:700; font-size:86px; line-height:1; letter-spacing:-.01em; white-space:nowrap; color:var(--k-text);
    text-shadow:0 0 38px color-mix(in srgb, var(--k-accent) 55%, transparent), 0 6px 30px rgba(0,0,0,.7); }
  .k-tr-key .sub { display:block; font-family:var(--k-font); font-weight:500; font-size:30px; letter-spacing:.04em; color:var(--k-mute); margin-top:8px; }
  .k-tr-ul { position:absolute; left:0; right:0; bottom:-18px; width:100%; height:22px; overflow:visible; }
  .k-tr-ul path { fill:none; stroke:var(--k-accent); stroke-width:5; stroke-linecap:round; }
  .k-tr-logo { width:190px; height:190px; border-radius:50%; background:#fff; border:6px solid var(--k-accent); box-shadow:0 22px 60px rgba(0,0,0,.55); display:flex; align-items:center; justify-content:center; }
  .k-tr-logo img { width:62%; height:62%; object-fit:contain; }
  .k-tr-card { padding:26px 38px; border-radius:22px; background:rgba(14,11,8,.82); border:2px solid color-mix(in srgb, var(--k-accent) 60%, transparent); box-shadow:0 30px 80px rgba(0,0,0,.55);
    font-weight:700; font-size:44px; line-height:1.1; color:var(--k-text); text-align:center; }
  /* captions: word by word, bold sans; the key words in the italic serif */
  .k-cap { position:absolute; left:0; right:0; font-family:var(--k-font); }
  .k-cw { position:absolute; left:0; right:0; text-align:center; opacity:0; font-weight:700; font-size:78px; line-height:1.1; letter-spacing:-.01em; color:#fff;
    text-shadow:0 3px 14px rgba(0,0,0,.7), 0 8px 40px rgba(0,0,0,.55); white-space:nowrap; }
  .k-cw.em { font-family:var(--k-serif); font-style:italic; font-weight:400; font-size:104px; letter-spacing:0; color:var(--k-text);
    text-shadow:0 0 36px color-mix(in srgb, var(--k-accent) 55%, transparent), 0 4px 18px rgba(0,0,0,.65); }
  /* halo: a ring and short labels around the speaker's head */
  .k-halo-svg { position:absolute; inset:0; width:1920px; height:1080px; overflow:visible; }
  .k-halo-svg circle { fill:none; }
  .k-halo-pill { position:absolute; translate:-50% -50%; opacity:0; padding:12px 26px; border-radius:999px; background:rgba(16,12,8,.72); border:2px solid color-mix(in srgb, var(--k-accent) 70%, transparent);
    font-family:var(--k-font); font-weight:600; font-size:32px; line-height:1; color:var(--k-text); white-space:nowrap; box-shadow:0 14px 40px rgba(0,0,0,.45); }
  .k-halo-top { position:absolute; translate:-50% -50%; opacity:0; font-family:var(--k-font); font-weight:700; font-size:54px; line-height:1; color:#fff; white-space:nowrap;
    text-shadow:0 0 30px color-mix(in srgb, var(--k-accent) 50%, transparent), 0 4px 18px rgba(0,0,0,.7); }
  /* gallery: a wall of pages, one is picked and flies to the centre */
  .k-tag { position:absolute; left:50%; top:64px; translate:-50% 0; padding:12px 26px; border-radius:999px; font-family:var(--k-font); font-weight:600; font-size:30px; color:var(--k-text);
    background:rgba(255,255,255,.08); border:2px solid rgba(255,255,255,.22); opacity:0; white-space:nowrap; }
  .k-tag b { color:var(--k-accent); font-weight:700; }
  .k-gl-item { position:absolute; border-radius:10px; overflow:hidden; opacity:0; box-shadow:0 18px 50px rgba(0,0,0,.55), 0 0 0 1.5px rgba(255,255,255,.14); background:#0b0907; }
  .k-gl-item img { width:100%; height:100%; display:block; object-fit:fill; }
  /* agenda */
  .k-ag { position:absolute; display:flex; flex-direction:column; gap:16px; font-family:var(--k-font); }
  .k-ag-item { padding:14px 28px 12px; border-radius:12px; font-weight:700; font-size:50px; line-height:1; letter-spacing:.03em; text-transform:uppercase; white-space:nowrap;
    color:var(--k-accent); background:rgba(8,6,4,.66); box-shadow:0 10px 30px rgba(0,0,0,.35); opacity:0; align-self:flex-start; }
  .k-ag-item .n { color:var(--k-text); margin-right:14px; }
"""


def css(style=None):
    """The studio formats' CSS with the style tokens filled in. If the style carries a "lines" dict, the older lower-line format
    (and the chip) follow the same palette and font; without it they keep the original look (nothing changes for old storyboards).
    "lines": {"size": 64, "weight": 600, "spacing": "0.02em", "upper": false, "bottom": 84, "italic": false}"""
    st = dict(DEFAULT_STYLE); st.update({k: v for k, v in (style or {}).items() if k != "lines"})
    out = _TEMPLATE
    for k, v in st.items():
        out = out.replace("@%s@" % k, str(v))
    for ff in (style or {}).get("font_faces", []):   # {"family": "Inter", "file": "Inter.ttf", "weight": "100 900"} (the file lives in the skill's assets/fonts)
        out += '\n  @font-face { font-family:"%s"; src:url("fonts/%s"); font-weight:%s; font-display:block; }' % (ff["family"], ff["file"], ff.get("weight", "400"))
    ln = (style or {}).get("lines")
    if ln:
        size = int(ln.get("size", 64)); weight = int(ln.get("weight", 600)); sp = ln.get("spacing", "0.01em")
        out += """
  /* the lower line and the chip follow the studio style (opt-in: storyboard "style": {"lines": {...}}) */
  .lower { font-family:var(--k-font); letter-spacing:%s; bottom:%dpx; }
  .lower .w, .lower .sp { font-size:%dpx; font-weight:%d; %s%s }
  .lower .w { color:var(--k-text); } .lower .w.em { color:var(--k-accent); } .lower.amber .w.em { color:var(--k-accent2); }
  .lower .w.em { text-shadow:0 0 30px color-mix(in srgb, var(--k-accent) 55%%, transparent), 0 3px 8px rgba(0,0,0,.85); }
  .chip .inner { font-family:var(--k-font); } .chip .inner .em { color:var(--k-accent); }
  %s
""" % (sp, int(ln.get("bottom", 84)), size, weight, "text-transform:uppercase;" if ln.get("upper") else "", "font-style:italic;" if ln.get("italic") else "",
                  (".lower .w.em { font-family:var(--k-hand); font-weight:700; font-size:%dpx; letter-spacing:0; }" % int(size * 1.22)) if ln.get("hand_em") else "")
    return out


# ---- helpers ------------------------------------------------------------------------------------------------------------
def _attrs(at, anchor):
    s = ' data-at="%.3f"' % float(at)
    if anchor == "-":
        return s + ' data-unanchored="1"'
    return s + (' data-anchor="%s"' % esc(anchor) if anchor else "")


def _rise(js, sel, t, dy=24, dur=0.45, scale=0.95):
    js("tl.fromTo('%s', { opacity: 0, y: %d, scale: %.2f }, { opacity: 1, y: 0, scale: 1, duration: %.2f, ease: 'power2.out' }, %.3f);" % (sel, dy, scale, dur, t))


def _fit(w, h, maxw, maxh):
    s = min(maxw / float(w), maxh / float(h))
    return w * s, h * s


# ---- build ----------------------------------------------------------------------------------------------------------------
def build(b, bid, t_in, t_out, js):
    """items: [{"img": "img/x.png", "label": "BRUSHED FLEECE", "value": "500 GSM", "at": t, "label_at": t, "value_at": t,
                "anchor": "...", "label_anchor": "...", "value_anchor": "..."}]   (any of img/label/value may be missing)"""
    items = b["items"][:4]; n = len(items)
    title = ('<div class="k-title" id="%s-title">%s</div>' % (bid, esc(b["title"]))) if b.get("title") else ""
    cells = ""
    for i, it in enumerate(items):
        at = float(it["at"]); la = float(it.get("label_at", at + 0.5)); va = float(it.get("value_at", la + 0.5))
        cell = ""
        if it.get("img"):
            cell += '<div class="k-img" id="%s-im%d"%s><img src="%s" alt="" /></div>' % (bid, i, _attrs(at, it.get("anchor")), it["img"])
            _rise(js, "#%s-im%d" % (bid, i), at, dy=34, dur=0.5, scale=0.9)
        if it.get("label"):
            cell += '<div class="k-label" id="%s-l%d"%s>%s</div>' % (bid, i, _attrs(la, it.get("label_anchor", it["label"])), esc(it["label"]))
            _rise(js, "#%s-l%d" % (bid, i), la, dy=18, dur=0.36)
        if it.get("value"):
            cell += '<div class="k-value" id="%s-v%d"%s>%s</div>' % (bid, i, _attrs(va, it.get("value_anchor", it["value"])), esc(it["value"]))
            _rise(js, "#%s-v%d" % (bid, i), va, dy=18, dur=0.36)
        cells += '<div class="k-item">%s</div>' % cell
    if title:
        js("tl.fromTo('#%s-title', { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.4, ease: 'power2.out' }, %.3f);" % (bid, t_in + 0.05))
    return '<div class="k-cut">%s<div class="k-row">%s</div></div>' % (title, cells)


# ---- annotate -------------------------------------------------------------------------------------------------------------
def annotate(b, bid, t_in, t_out, js, size):
    """src: the picture; callouts: [{"label": "SLEEVE LENGTH", "sub": "shoulder to cuff", "x": .62, "y": .30, "to": [x2, y2] (optional: a measured segment),
    "side": "r"|"l", "dy": 0, "at": t, "anchor": "..."}]   x/y are fractions of the picture.
    space: true -> the picture is a window in 3D space (frame, entry turn, slow camera drift), the lines and labels are part of that space, so the
    camera keeps moving while the notes connect (a page never just appears and sits still). frame: true/false forces the window frame."""
    iw, ih = size
    space = bool(b.get("space"))
    framed = b.get("frame", space)
    pw, ph = _fit(iw, ih, b.get("max_w", 1120 if space else 1000), b.get("max_h", 760 if space else 840))
    left = (1920 - pw) / 2.0 + b.get("shift_x", -120 if space else 0); top = (1080 - ph) / 2.0 + b.get("shift_y", 10 if space else 0)
    cols = ["var(--k-accent)", "var(--k-accent2)", "var(--k-accent3)", "#e07a5f"]
    svg, dots, labs = "", "", ""
    pans = []
    for i, c in enumerate(b["callouts"]):
        col = cols[i % len(cols)]
        tx, ty = left + c["x"] * pw, top + c["y"] * ph
        side = c.get("side", "r" if c["x"] >= 0.5 else "l")
        lx = (left + pw + 70) if side == "r" else (left - 70)
        ly = ty + c.get("dy", 0)
        at = float(c["at"])
        pans.append((at, tx, ty, lx, ly, side))
        seg = ""
        if c.get("to"):
            ex, ey = left + c["to"][0] * pw, top + c["to"][1] * ph
            seg = '<line id="%s-m%d" x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="%s"/>' % (bid, i, tx, ty, ex, ey, col)
            tx, ty = (tx + ex) / 2.0, (ty + ey) / 2.0
        elbow = (lx - 40) if side == "r" else (lx + 40)
        svg += seg + '<polyline id="%s-k%d" points="%.0f,%.0f %.0f,%.0f %.0f,%.0f" stroke="%s"/>' % (bid, i, tx, ty, elbow, ly, lx, ly, col)
        dots += '<div class="k-an-dot" id="%s-d%d" style="left:%.0fpx;top:%.0fpx;background:%s"></div>' % (bid, i, tx, ty, col)
        sub = ('<div class="s">%s</div>' % esc(c["sub"])) if c.get("sub") else ""
        pos = ("left:%.0fpx;" % (lx + 14)) if side == "r" else ("right:%.0fpx;" % (1920 - lx + 14))
        labs += ('<div class="k-an-lab %s" id="%s-t%d" style="%stop:%.0fpx;translate:0 -50%%;"%s><div class="t" style="color:%s">%s</div>%s</div>'
                 % (side, bid, i, pos, ly, _attrs(at, c.get("anchor", c["label"])), col, esc(c["label"]), sub))
        if c.get("to"):
            js("(function(){ var l = document.getElementById('%s-m%d'); var L = Math.hypot(l.x2.baseVal.value - l.x1.baseVal.value, l.y2.baseVal.value - l.y1.baseVal.value);"
               " l.style.strokeDasharray = L; l.style.strokeDashoffset = L; tl.to(l, { strokeDashoffset: 0, duration: 0.45, ease: 'power2.out' }, %.3f); })();" % (bid, i, at - 0.1))
        js("(function(){ var l = document.getElementById('%s-k%d'); var L = l.getTotalLength(); l.style.strokeDasharray = L; l.style.strokeDashoffset = L;"
           " tl.to(l, { strokeDashoffset: 0, duration: 0.42, ease: 'power2.out' }, %.3f); })();" % (bid, i, at + (0.25 if c.get("to") else 0.0)))
        js("tl.fromTo('#%s-d%d', { opacity: 0, scale: 0.2 }, { opacity: 1, scale: 1, duration: 0.3, ease: 'power2.out' }, %.3f);" % (bid, i, at - 0.05))
        zz = float(b.get("label_z", 90)) if space else 0
        js("tl.fromTo('#%s-t%d', { opacity: 0, x: %d }, { opacity: 1, x: 0, z: %.0f, duration: 0.38, ease: 'power2.out' }, %.3f);" % (bid, i, 18 if side == "r" else -18, zz, at + 0.32 + (0.25 if c.get("to") else 0.0)))
    base_at = float(b.get("img_at", t_in + 0.05))
    js("tl.fromTo('#%s-img', { opacity: 0, y: 30, scale: 0.96 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: 'power2.out' }, %.3f);" % (bid, base_at))
    if space:   # entry: the window turns into place, then the camera keeps drifting for the rest of the scene
        d0, d1 = float(b.get("turn", [24, 9])[0]), float(b.get("turn", [24, 9])[1])
        js("tl.fromTo('#%s-rig', { rotationY: %.1f, rotationX: 5 }, { rotationY: %.1f, rotationX: 2, duration: 0.9, ease: 'power3.out' }, %.3f);" % (bid, d0, d1, t_in))
        js("tl.to('#%s-rig', { rotationY: %.1f, rotationX: -2, duration: %.3f, ease: 'sine.inOut' }, %.3f);" % (bid, float(b.get("drift_to", -9)), max(1.0, t_out - t_in - 0.9), t_in + 0.9))
        if b.get("follow"):   # the camera swings fast toward each arrow and its label, then returns to the picture (which stays centred)
            f = b["follow"] if isinstance(b["follow"], dict) else {}
            zoom, wgt, d_in, hold, d_out = float(f.get("zoom", 1.3)), float(f.get("pan", 0.62)), float(f.get("dur", 0.42)), float(f.get("hold", 0.85)), float(f.get("back", 0.5))
            dl = b.get("dolly") or [1.0, 1.0]
            total = max(1.0, t_out - t_in)
            base = lambda tt: float(dl[0]) + (float(dl[1]) - float(dl[0])) * min(1.0, max(0.0, (tt - t_in) / total))
            js("tl.set('#%s-rig', { x: 0, y: 0, scale: %.3f }, %.3f);" % (bid, base(t_in), t_in))
            prev = t_in
            for (at_, tx_, ty_, lx_, ly_, sd_) in pans:
                px = (1 - wgt) * tx_ + wgt * (lx_ + (190 if sd_ == "r" else -190)); py = (1 - wgt) * ty_ + wgt * ly_
                t0 = at_ - 0.12
                if t0 > prev + 0.05:
                    js("tl.to('#%s-rig', { x: 0, y: 0, scale: %.3f, duration: %.3f, ease: 'sine.inOut' }, %.3f);" % (bid, base(t0), t0 - prev, prev))
                js("tl.to('#%s-rig', { x: %.1f, y: %.1f, scale: %.3f, duration: %.2f, ease: 'power3.out' }, %.3f);" % (bid, -zoom * (px - 960), -zoom * (py - 540), zoom, d_in, t0))
                t1 = t0 + d_in + hold
                js("tl.to('#%s-rig', { x: 0, y: 0, scale: %.3f, duration: %.2f, ease: 'power2.inOut' }, %.3f);" % (bid, base(t1 + d_out), d_out, t1))
                prev = t1 + d_out
            if t_out - prev > 0.1:
                js("tl.to('#%s-rig', { x: 0, y: 0, scale: %.3f, duration: %.3f, ease: 'sine.inOut' }, %.3f);" % (bid, base(t_out), t_out - prev, prev))
        elif b.get("dolly"):   # the camera pulls away from the picture (or closes in) for the whole scene; the picture stays centred
            d0, d1 = float(b["dolly"][0]), float(b["dolly"][1])
            js("tl.fromTo('#%s-rig', { scale: %.3f }, { scale: %.3f, duration: %.3f, ease: 'sine.inOut' }, %.3f);" % (bid, d0, d1, max(1.0, t_out - t_in), t_in))
    title = ('<div class="k-title" id="%s-title">%s</div>' % (bid, esc(b["title"]))) if b.get("title") else ""
    if title:
        js("tl.fromTo('#%s-title', { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.4, ease: 'power2.out' }, %.3f);" % (bid, t_in + 0.05))
    body = ('<div class="k-an-img%s" id="%s-img" style="left:%.0fpx;top:%.0fpx;width:%.0fpx;height:%.0fpx"><img src="%s" alt="" /></div>'
            '<svg class="k-an-svg" viewBox="0 0 1920 1080">%s</svg>%s%s' % (" page" if framed else "", bid, left, top, pw, ph, b["src"], svg, dots, labs))
    if space:
        body = '<div class="k-sp-stage"><div class="k-sp-rig" id="%s-rig">%s</div></div>' % (bid, body)
    return '<div class="k-cut">%s%s</div>' % (title, body)


# ---- orbit ----------------------------------------------------------------------------------------------------------------
_ANG = {1: [0], 2: [200, -20], 3: [205, -25, 90], 4: [210, 330, 150, 30], 5: [215, 325, 160, 20, 270], 6: [215, 325, 160, 20, 90, 270], 7: [200, 330, 150, 20, 90, 270, 0],
        8: [200, 340, 150, 30, 90, 270, 10, 170]}


def orbit(b, bid, t_in, t_out, js):
    """center: {"src": "img/card.png"} or {"text": "PLAYBOOK", "sub": "for building personal brands"}; card: [w, h] (default 460x600)
    pre: {"go_at": t}  -> the card first sits beside the speaker (left), then is carried into the dark space at go_at (no pre: starts in space)
    nodes: [{"src": "img/logo.svg", "logo": true, "text": "Canva", "caption": "Canva", "at": t, "anchor": "..."}]"""
    cw, ch = b.get("card", [460, 600]); cen = b["center"]
    nodes = b["nodes"][:8]; n = len(nodes)
    angs = _ANG.get(n, [])
    cx, cy, RX, RY = 960, 560, b.get("rx", 650), b.get("ry", 330)
    pre = b.get("pre"); go = float(pre["go_at"]) if pre else t_in + 0.05
    # the card
    if cen.get("src"):
        content = '<img src="%s" alt="" />' % cen["src"]
    else:
        content = '<div class="t">%s</div>%s' % (esc(cen["text"]), ('<div class="s">%s</div>' % esc(cen["sub"])) if cen.get("sub") else "")
    card = '<div class="k-or-card" id="%s-card" style="width:%dpx;height:%dpx">%s</div>' % (bid, cw, ch, content)
    svg, ns = "", ""
    for i, (nd, ang) in enumerate(zip(nodes, angs)):
        a = math.radians(ang); px, py = cx + RX * math.cos(a), cy + RY * math.sin(a)
        # the line runs from the card's edge to the node
        ex, ey = cx + (cw / 2.0 + 10) * (1 if math.cos(a) > 0.3 else (-1 if math.cos(a) < -0.3 else 0)), cy + (ch / 2.0 + 10) * (1 if math.sin(a) > 0.6 else (-1 if math.sin(a) < -0.6 else 0))
        svg += '<line id="%s-ln%d" x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f"/>' % (bid, i, ex, ey, px, py)
        if nd.get("src"):
            disc = '<div class="k-or-disc%s"><img src="%s" alt="" /></div>' % (" logo" if nd.get("logo") else "", nd["src"])
        else:
            disc = '<div class="k-or-disc"><span class="ltr">%s</span></div>' % esc((nd.get("text") or "?").upper())
        cap = ('<div class="k-or-cap">%s</div>' % esc(nd["caption"])) if nd.get("caption") else ""
        at = float(nd["at"])
        ns += '<div class="k-or-node" id="%s-n%d" style="left:%.0fpx;top:%.0fpx"%s>%s%s</div>' % (bid, i, px, py, _attrs(at, nd.get("anchor", nd.get("caption") or nd.get("text") or "")), disc, cap)
        ox, oy = (px - cx) * 0.55, (py - cy) * 0.55
        js("tl.fromTo('#%s-n%d', { opacity: 0, x: %.0f, y: %.0f, scale: 0.7 }, { opacity: 1, x: 0, y: 0, scale: 1, duration: 0.7, ease: 'power3.out' }, %.3f);" % (bid, i, ox, oy, at))
        js("(function(){ var l = document.getElementById('%s-ln%d'); var L = Math.hypot(l.x2.baseVal.value - l.x1.baseVal.value, l.y2.baseVal.value - l.y1.baseVal.value);"
           " l.style.strokeDasharray = L; l.style.strokeDashoffset = L; tl.to(l, { strokeDashoffset: 0, duration: 0.5, ease: 'power2.out' }, %.3f); })();" % (bid, i, at + 0.2))
    # card motion + scrim
    if pre:
        js("tl.fromTo('#%s-card', { opacity: 0, x: -760, scale: 0.7 }, { opacity: 1, x: -500, scale: 0.72, duration: 0.6, ease: 'power3.out' }, %.3f);" % (bid, t_in + 0.05))
        js("tl.to('#%s-card', { x: 0, scale: 1, duration: 0.95, ease: 'power2.inOut' }, %.3f);" % (bid, go))
        js("tl.fromTo('#%s-scrim', { opacity: 0 }, { opacity: 1, duration: 0.8, ease: 'power2.inOut' }, %.3f);" % (bid, go))
    else:
        js("tl.fromTo('#%s-scrim', { opacity: 0 }, { opacity: 1, duration: 0.5, ease: 'power2.out' }, %.3f);" % (bid, t_in))
        js("tl.fromTo('#%s-card', { opacity: 0, y: 40, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: 'power2.out' }, %.3f);" % (bid, t_in + 0.15))
    js("tl.fromTo('#%s-rig', { rotationY: -5 }, { rotationY: 5, duration: %.3f, ease: 'none' }, %.3f);" % (bid, max(1.0, t_out - go), go))
    return ('<div class="k-orbit"><div class="k-or-scrim" id="%s-scrim"></div><div class="k-or-stage"><div class="k-or-rig" id="%s-rig">'
            '<svg class="k-or-svg" id="%s-svg" viewBox="0 0 1920 1080">%s</svg>%s<div id="%s-nodes">%s</div></div></div></div>' % (bid, bid, bid, svg, card, bid, ns))


# ---- dive -----------------------------------------------------------------------------------------------------------------
def dive(b, bid, t_in, t_out, js, size):
    """src: the screen/page; focus: {"x","y","w","h"} fractions of the picture to start zoomed on; reveal_at: when the camera pulls back to the whole picture;
    click: {"x","y","at"} (fractions, optional): a cursor glides to that spot and clicks before the pull-back; tilt: true (a gentle 3D settle after the reveal)."""
    iw, ih = size
    dw, dh = _fit(iw, ih, b.get("max_w", 1500), b.get("max_h", 860))
    left, top = (1920 - dw) / 2.0, (1080 - dh) / 2.0
    f = b["focus"]; fcx, fcy = left + (f["x"] + f["w"] / 2.0) * dw, top + (f["y"] + f["h"] / 2.0) * dh
    s0 = min(1700.0 / (f["w"] * dw), 880.0 / (f["h"] * dh), b.get("max_zoom", 3.4))
    x0, y0 = 960 - s0 * fcx, 540 - s0 * fcy
    rev = float(b["reveal_at"])
    js("tl.fromTo('#%s-stage', { opacity: 0, y: 620 }, { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }, %.3f);" % (bid, t_in))
    js("tl.set('#%s-cam', { x: %.2f, y: %.2f, scale: %.4f }, %.3f);" % (bid, x0, y0, s0, t_in))
    js("tl.to('#%s-cam', { x: 0, y: 0, scale: 1, duration: %.2f, ease: 'power2.inOut' }, %.3f);" % (bid, b.get("reveal_dur", 1.25), rev))
    cur = ""
    ck = b.get("click")
    if ck:
        sx, sy = x0 + s0 * (left + ck["x"] * dw), y0 + s0 * (top + ck["y"] * dh)
        cat = float(ck["at"])
        cur = ('<div class="k-ring" id="%s-ring" style="left:%.0fpx;top:%.0fpx"></div><svg class="k-cursor" id="%s-cur" viewBox="0 0 24 24"><path d="M3 2 L3 19 L8 14.5 L11.5 22 L14.5 20.6 L11.2 13.2 L18 13 Z" fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>'
               % (bid, sx, sy, bid))
        js("tl.fromTo('#%s-cur', { opacity: 0, x: %.0f, y: %.0f }, { opacity: 1, x: %.0f, y: %.0f, duration: 0.8, ease: 'power2.inOut' }, %.3f);" % (bid, sx + 300, sy + 260, sx, sy, cat - 0.8))
        js("tl.fromTo('#%s-cur', { scale: 1 }, { scale: 0.86, duration: 0.1, ease: 'power2.in' }, %.3f);" % (bid, cat))
        js("tl.to('#%s-cur', { scale: 1, duration: 0.14, ease: 'power2.out' }, %.3f);" % (bid, cat + 0.1))
        js("tl.fromTo('#%s-ring', { opacity: 0.95, scale: 0.4 }, { opacity: 0, scale: 1.7, duration: 0.55, ease: 'power2.out' }, %.3f);" % (bid, cat))
        js("tl.to('#%s-cur', { opacity: 0, duration: 0.3 }, %.3f);" % (bid, rev + 0.2))
    if b.get("tilt"):
        js("tl.to('#%s-stage', { rotationY: -7, rotationX: 3, duration: %.3f, ease: 'power1.inOut' }, %.3f);" % (bid, max(1.2, t_out - rev - 1.0), rev + 1.0))
    return ('<div class="k-cut"><div class="k-dv-wrap"><div class="k-dv-stage" id="%s-stage"><div class="k-dv-cam" id="%s-cam"><div class="k-dv-frame" style="left:%.0fpx;top:%.0fpx;width:%.0fpx;height:%.0fpx">'
            '<img src="%s" alt="" /></div></div></div></div>%s</div>' % (bid, bid, left, top, dw, dh, b["src"], cur))


# ---- agenda ---------------------------------------------------------------------------------------------------------------
AG_POS = {"tl": "left:70px; top:96px;", "tr": "right:70px; top:96px;", "ml": "left:70px; top:300px;", "bl": "left:70px; bottom:110px;"}


def agenda(b, bid, t_in, t_out, js):
    """items: [["Impaginazione", t, "anchor (optional)"], ...] -> '#1 IMPAGINAZIONE', '#2 ...': each line enters on its word and the list stays until `out`."""
    rows = ""
    for i, it in enumerate(b["items"]):
        at = float(it[1])
        rows += '<div class="k-ag-item" id="%s-a%d"%s><span class="n">#%d</span>%s</div>' % (bid, i, _attrs(at, it[2] if len(it) > 2 else it[0]), i + 1, esc(it[0]))
        js("tl.fromTo('#%s-a%d', { opacity: 0, x: -34 }, { opacity: 1, x: 0, duration: 0.42, ease: 'power2.out' }, %.3f);" % (bid, i, at))
    js("tl.to('#%s-list', { opacity: 0, duration: 0.3, ease: 'power2.in' }, %.3f);" % (bid, t_out - 0.34))
    return '<div class="k-ag" id="%s-list" style="%s">%s</div>' % (bid, AG_POS.get(b.get("pos", "ml"), AG_POS["ml"]), rows)


# ---- trail ----------------------------------------------------------------------------------------------------------------
import math as _m


def _edge(cx, cy, w, h, tx, ty, pad=16):
    """the point where the line from the centre (cx,cy) toward (tx,ty) leaves a w x h box, pushed out by pad"""
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    k = min((w / 2.0 + pad) / abs(dx) if dx else 1e9, (h / 2.0 + pad) / abs(dy) if dy else 1e9)
    return cx + dx * k, cy + dy * k


def trail(b, bid, t_in, t_out, js, sizes):
    """A page (or any picture) rests on screen, then the camera pulls back through 3D space, the window shrinks and an arrow leads to the next thing.
    nodes: [{"id": "p", "kind": "page", "src": "img/page.png", "w": 1100, "x": 0, "y": 0, "z": 0, "rot": -6, "at": t_in, "anchor": ".."},
            {"id": "k", "kind": "key", "text": "Palette colori", "sub": "optional", "x": 1250, "y": -60, "z": 120, "at": t, "anchor": ".."},
            {"id": "c", "kind": "logo", "src": "img/logos/claude.svg", "x": .., "y": .., "at": t}, {"id": "m", "kind": "card", "text": "..", "w": 420, "h": 130, ...}]
    links: [{"from": "p", "to": "k", "at": t}]  (the arrow draws from the edge of one node to the edge of the other)
    cam: [[t_in, cx, cy, zoom, rotY, rotX], [t, cx, cy, zoom, rotY, rotX, dur], ...]  the first is the starting pose, every other one a move (default 1.3 s)
    All positions are canvas px from the stage centre; zoom 1 shows 1920 x 1080 of canvas."""
    geo, html = {}, ""
    for i, nd in enumerate(b["nodes"]):
        kind = nd.get("kind", "page"); x, y, z = float(nd.get("x", 0)), float(nd.get("y", 0)), float(nd.get("z", 0))
        at = float(nd.get("at", t_in)); nid = "%s-n%d" % (bid, i)
        if kind == "page":
            iw, ih = sizes[nd["src"]]; w = float(nd.get("w", 1100)); h = w * ih / float(iw)
            inner = '<div class="k-tr-page" style="width:%.0fpx;height:%.0fpx"><img src="%s" alt="" /></div>' % (w, h, nd["src"]); rot = float(nd.get("rot", -6))
        elif kind == "key":
            txt = nd["text"]; w = float(nd.get("w", len(txt) * 50 + 60)); h = float(nd.get("h", 150 if nd.get("sub") else 120)); rot = float(nd.get("rot", 0))
            sub = ('<span class="sub">%s</span>' % esc(nd["sub"])) if nd.get("sub") else ""
            ul = '<svg class="k-tr-ul" viewBox="0 0 300 22" preserveAspectRatio="none"><path id="%s-ul" d="M2 11 L298 11"/></svg>' % nid
            inner = '<div class="k-tr-key" style="position:relative">%s%s%s</div>' % (esc(txt), ul, sub)
        elif kind == "logo":
            w = h = float(nd.get("w", 190)); rot = float(nd.get("rot", 0))
            inner = '<div class="k-tr-logo"><img src="%s" alt="" /></div>' % nd["src"]
        else:   # card
            w = float(nd.get("w", 420)); h = float(nd.get("h", 130)); rot = float(nd.get("rot", 0))
            inner = '<div class="k-tr-card" style="width:%.0fpx">%s</div>' % (w, esc(nd["text"]))
        geo[nd["id"]] = (960 + x, 540 + y, w, h)
        html += '<div class="k-tr-node" id="%s" style="left:%.0fpx;top:%.0fpx"%s>%s</div>' % (nid, 960 + x, 540 + y, _attrs(at, nd.get("anchor", "-")), inner)
        if kind == "page" and nd.get("enter") is False:   # already in place (it continues from the scene before, e.g. a gallery's picked page)
            js("tl.set('#%s', { opacity: 1, rotationY: %.1f, z: %.0f }, %.3f);" % (nid, rot, z, at))
        elif kind == "page":
            js("tl.fromTo('#%s', { opacity: 0, y: 140, rotationY: %.1f }, { opacity: 1, y: 0, rotationY: %.1f, z: %.0f, duration: 0.85, ease: 'power3.out' }, %.3f);" % (nid, rot + 22, rot, z, at))
        else:
            js("tl.fromTo('#%s', { opacity: 0, y: 36, scale: 0.86, rotationY: %.1f }, { opacity: 1, y: 0, scale: 1, z: %.0f, duration: 0.6, ease: 'power2.out' }, %.3f);" % (nid, rot, z, at))
        if kind == "key":
            js("(function(){ var u = document.getElementById('%s-ul'); var L = u.getTotalLength(); u.style.strokeDasharray = L; u.style.strokeDashoffset = L; tl.to(u, { strokeDashoffset: 0, duration: 0.5, ease: 'power2.out' }, %.3f); })();" % (nid, at + 0.35))
    svg = ""
    cols = ["var(--k-accent)", "var(--k-accent2)", "var(--k-accent3)"]
    for j, lk in enumerate(b.get("links", [])):
        a, c = geo[lk["from"]], geo[lk["to"]]
        x1, y1 = _edge(a[0], a[1], a[2], a[3], c[0], c[1]); x2, y2 = _edge(c[0], c[1], c[2], c[3], a[0], a[1], pad=22)
        ang = _m.atan2(y2 - y1, x2 - x1); col = cols[j % len(cols)]
        hx = [(x2, y2), (x2 - 34 * _m.cos(ang - 0.42), y2 - 34 * _m.sin(ang - 0.42)), (x2 - 34 * _m.cos(ang + 0.42), y2 - 34 * _m.sin(ang + 0.42))]
        svg += ('<line class="ln" id="%s-l%d" x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="%s"/><polygon class="hd" id="%s-h%d" points="%s" fill="%s" opacity="0"/>'
                % (bid, j, x1, y1, x2, y2, col, bid, j, " ".join("%.0f,%.0f" % pt for pt in hx), col))
        ta = float(lk.get("at", t_in + 3.0))
        js("(function(){ var l = document.getElementById('%s-l%d'); var L = Math.hypot(l.x2.baseVal.value - l.x1.baseVal.value, l.y2.baseVal.value - l.y1.baseVal.value);"
           " l.style.strokeDasharray = L; l.style.strokeDashoffset = L; tl.to(l, { strokeDashoffset: 0, duration: 0.6, ease: 'power2.out' }, %.3f); })();" % (bid, j, ta))
        js("tl.to('#%s-h%d', { opacity: 1, duration: 0.18 }, %.3f);" % (bid, j, ta + 0.5))
    cam = b["cam"]

    def pose(c):
        cx, cy, zm = float(c[1]), float(c[2]), float(c[3]); ry = float(c[4]) if len(c) > 4 else 0.0; rx = float(c[5]) if len(c) > 5 else 0.0
        return "x: %.1f, y: %.1f, scale: %.4f, rotationY: %.1f, rotationX: %.1f" % (-zm * cx, -zm * cy, zm, ry, rx)
    js("tl.set('#%s-rig', { %s }, %.3f);" % (bid, pose(cam[0]), t_in))
    for c in cam[1:]:
        dur = float(c[6]) if len(c) > 6 else 1.3
        js("tl.to('#%s-rig', { %s, duration: %.2f, ease: 'power2.inOut' }, %.3f);" % (bid, pose(c), dur, float(c[0])))
    # the camera never stops: after the last move it keeps drifting (a little closer, turning toward the front) until the scene ends
    last = cam[-1]; t_last = float(last[0]) + (float(last[6]) if len(last) > 6 else 1.3) if len(cam) > 1 else t_in + 0.9
    if b.get("drift", True) and t_last < t_out - 0.5:
        cx, cy, zm = float(last[1]), float(last[2]), float(last[3]) * 1.06
        ry = (float(last[4]) if len(last) > 4 else 0.0) * 0.45
        js("tl.to('#%s-rig', { x: %.1f, y: %.1f, scale: %.4f, rotationY: %.1f, duration: %.3f, ease: 'sine.inOut' }, %.3f);" % (bid, -zm * cx, -zm * cy, zm, ry, t_out - t_last, t_last))
    return ('<div class="k-cut"><div class="k-tr-stage"><div class="k-tr-rig" id="%s-rig"><svg class="k-tr-svg" viewBox="0 0 1920 1080">%s</svg>%s</div></div></div>' % (bid, svg, html))


# ---- captions ---------------------------------------------------------------------------------------------------------------
def captions(b, bid, t_in, t_out, js):
    """Word-by-word captions in the middle of the frame: bold sans, one word at a time; "em" words in the italic serif (optionally coloured).
    words: [{"text": "tecnicismi", "at": t, "end": t2 (optional), "em": true, "color": "#e14a4a" (optional)}]   top: pixel row of the caption (default 650)"""
    ws = b["words"]; top = int(b.get("top", 650)); html = ""
    for i, w in enumerate(ws):
        at = float(w["at"]); nxt = float(ws[i + 1]["at"]) if i + 1 < len(ws) else float(w.get("end", at + 0.5)) + 0.25
        end = float(w.get("end_show", nxt))
        st = ' style="color:%s"' % w["color"] if w.get("color") else ""
        anc = _attrs(at, w.get("anchor", w["text"])) if (i == 0 or w.get("anchor")) else ""
        html += '<span class="k-cw%s" id="%s-w%d"%s%s>%s</span>' % (" em" if w.get("em") else "", bid, i, st, anc, esc(w["text"]))
        js("tl.fromTo('#%s-w%d', { opacity: 0, scale: 0.88, y: 10 }, { opacity: 1, scale: 1, y: 0, duration: 0.11, ease: 'power2.out' }, %.3f);" % (bid, i, at - 0.02))
        js("tl.to('#%s-w%d', { opacity: 0, duration: 0.07, ease: 'power1.in' }, %.3f);" % (bid, i, max(at + 0.12, end - 0.05)))
    return '<div class="k-cap" style="top:%dpx">%s</div>' % (top, html)


# ---- halo -----------------------------------------------------------------------------------------------------------------
def halo(b, bid, t_in, t_out, js):
    """A ring around the speaker's head with short labels that land on their words, and a line of text above the head.
    cx, cy, r: the ring (px; the head's centre and about 1.4 x its height); pills: [{"text": "Immagini", "at": t, "angle": 200, "anchor": ".."}]; top: {"text": "ASSET", "at": t}"""
    cx, cy, r = float(b.get("cx", 900)), float(b.get("cy", 430)), float(b.get("r", 330))
    ring_at = float(b.get("ring_at", t_in + 0.05))
    svg = ('<svg class="k-halo-svg" viewBox="0 0 1920 1080"><g id="%s-ring">'
           '<circle id="%s-r1" cx="%.0f" cy="%.0f" r="%.0f" stroke="rgba(255,255,255,.75)" stroke-width="2.5" stroke-dasharray="5 11"/></g>'
           '<circle id="%s-r2" cx="%.0f" cy="%.0f" r="%.0f" stroke="color-mix(in srgb, var(--k-accent) 55%%, transparent)" stroke-width="2"/></svg>'
           % (bid, bid, cx, cy, r, bid, cx, cy, r + 38))
    pills = ""
    for i, pl in enumerate(b.get("pills", [])):
        a = math.radians(float(pl.get("angle", 200 + 50 * i))); px, py = cx + r * math.cos(a), cy + r * math.sin(a); at = float(pl["at"])
        pills += '<div class="k-halo-pill" id="%s-p%d" style="left:%.0fpx;top:%.0fpx"%s>%s</div>' % (bid, i, px, py, _attrs(at, pl.get("anchor", pl["text"])), esc(pl["text"]))
        js("tl.fromTo('#%s-p%d', { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.38, ease: 'power2.out' }, %.3f);" % (bid, i, at))
    top = ""
    if b.get("top"):
        tp = b["top"]; at = float(tp["at"])
        top = '<div class="k-halo-top" id="%s-top" style="left:%.0fpx;top:%.0fpx"%s>%s</div>' % (bid, cx, cy - r - 88, _attrs(at, tp.get("anchor", tp["text"])), esc(tp["text"]))
        js("tl.fromTo('#%s-top', { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.4, ease: 'power2.out' }, %.3f);" % (bid, at))
    js("tl.fromTo('#%s-ring, #%s-r2', { opacity: 0, scale: 0.82, svgOrigin: '%.0f %.0f' }, { opacity: 1, scale: 1, duration: 0.7, ease: 'power2.out', svgOrigin: '%.0f %.0f' }, %.3f);" % (bid, bid, cx, cy, cx, cy, ring_at))
    js("tl.to('#%s-r1', { rotation: 70, duration: %.3f, ease: 'none', svgOrigin: '%.0f %.0f' }, %.3f);" % (bid, max(1.0, t_out - t_in), cx, cy, t_in))
    js("tl.to('#host-%s .k-halo-pill, #host-%s .k-halo-top, #%s-ring, #%s-r2', { opacity: 0, duration: 0.3, ease: 'power2.in' }, %.3f);" % (bid, bid, bid, bid, t_out - 0.34))
    return svg + pills + top


# ---- gallery --------------------------------------------------------------------------------------------------------------
def gallery(b, bid, t_in, t_out, js):
    """A wall of pages (or any pictures) that fill in one by one under a small tag; then one is picked, the rest dim and it flies to the centre at the
    size the next scene starts from. images: [src, ...]; cols; tag: "Portfolio" / tag_em: "17 tavole"; select: {"index": 0, "at": t, "w": 1100}; ratio: height/width of a thumb"""
    imgs = b["images"]; cols = int(b.get("cols", 6)); rows = (len(imgs) + cols - 1) // cols
    tw = float(b.get("thumb_w", 270)); th = tw * float(b.get("ratio", 1685 / 2381.0)); gap = float(b.get("gap", 22))
    left0 = (1920 - (cols * tw + (cols - 1) * gap)) / 2.0; top0 = (1080 - (rows * th + (rows - 1) * gap)) / 2.0 + 36
    items = ""
    for i, src in enumerate(imgs):
        r, c = divmod(i, cols); x, y = left0 + c * (tw + gap), top0 + r * (th + gap)
        items += '<div class="k-gl-item" id="%s-g%d" style="left:%.0fpx;top:%.0fpx;width:%.0fpx;height:%.0fpx"><img src="%s" alt="" /></div>' % (bid, i, x, y, tw, th, src)
        js("tl.fromTo('#%s-g%d', { opacity: 0, y: 34, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.42, ease: 'power2.out' }, %.3f);" % (bid, i, t_in + 0.12 + 0.05 * i))
    tag = ""
    if b.get("tag"):
        tag = '<div class="k-tag" id="%s-tag">%s%s</div>' % (bid, esc(b["tag"]), (" <b>%s</b>" % esc(b["tag_em"])) if b.get("tag_em") else "")
        js("tl.fromTo('#%s-tag', { opacity: 0, y: -14 }, { opacity: 1, y: 0, duration: 0.4, ease: 'power2.out' }, %.3f);" % (bid, t_in + 0.05))
    sel = b.get("select")
    if sel:
        k = int(sel["index"]); r, c = divmod(k, cols); cxk, cyk = left0 + c * (tw + gap) + tw / 2.0, top0 + r * (th + gap) + th / 2.0
        at = float(sel["at"]); S = float(sel.get("w", 1100)) / tw
        others = ", ".join("#%s-g%d" % (bid, i) for i in range(len(imgs)) if i != k)
        js("tl.to('%s', { opacity: 0.2, duration: 0.4, ease: 'power2.out' }, %.3f);" % (others, at))
        js("tl.set('#%s-g%d', { zIndex: 10 }, %.3f);" % (bid, k, at))
        js("tl.to('#%s-g%d', { x: %.1f, y: %.1f, scale: %.3f, duration: %.2f, ease: 'power2.inOut' }, %.3f);" % (bid, k, 960 - cxk, 540 - cyk, S, float(sel.get("dur", 0.85)), at + 0.1))
        if tag:
            js("tl.to('#%s-tag', { opacity: 0, duration: 0.3 }, %.3f);" % (bid, at))
    return '<div class="k-cut">%s%s</div>' % (tag, items)
