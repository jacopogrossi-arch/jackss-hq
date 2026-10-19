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
}


_TEMPLATE = """
  :root { --k-bg:@bg@; --k-bg2:@bg2@; --k-text:@text@; --k-mute:@mute@; --k-accent:@accent@; --k-accent2:@accent2@; --k-accent3:@accent3@;
          --k-chip:@chip@; --k-chip-text:@chip_text@; --k-font:@font@; }
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
  .k-label { font-weight:700; font-size:44px; line-height:1; letter-spacing:.03em; text-transform:uppercase; padding:14px 26px 12px; border-radius:10px;
    background:var(--k-chip); color:var(--k-chip-text); opacity:0; white-space:nowrap; }
  .k-value { font-weight:700; font-size:38px; line-height:1; letter-spacing:.04em; padding:11px 22px 9px; border-radius:10px; border:3px solid var(--k-accent);
    color:var(--k-accent); background:rgba(0,0,0,.35); opacity:0; white-space:nowrap; }
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
  /* agenda */
  .k-ag { position:absolute; display:flex; flex-direction:column; gap:16px; font-family:var(--k-font); }
  .k-ag-item { padding:14px 28px 12px; border-radius:12px; font-weight:700; font-size:50px; line-height:1; letter-spacing:.03em; text-transform:uppercase; white-space:nowrap;
    color:var(--k-accent); background:rgba(8,6,4,.66); box-shadow:0 10px 30px rgba(0,0,0,.35); opacity:0; align-self:flex-start; }
  .k-ag-item .n { color:var(--k-text); margin-right:14px; }
"""


def css(style=None):
    st = dict(DEFAULT_STYLE); st.update(style or {})
    out = _TEMPLATE
    for k, v in st.items():
        out = out.replace("@%s@" % k, v)
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
    for i, c in enumerate(b["callouts"]):
        col = cols[i % len(cols)]
        tx, ty = left + c["x"] * pw, top + c["y"] * ph
        side = c.get("side", "r" if c["x"] >= 0.5 else "l")
        lx = (left + pw + 70) if side == "r" else (left - 70)
        ly = ty + c.get("dy", 0)
        at = float(c["at"])
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
        js("tl.fromTo('#%s-t%d', { opacity: 0, x: %d }, { opacity: 1, x: 0, duration: 0.38, ease: 'power2.out' }, %.3f);" % (bid, i, 18 if side == "r" else -18, at + 0.32 + (0.25 if c.get("to") else 0.0)))
    base_at = float(b.get("img_at", t_in + 0.05))
    js("tl.fromTo('#%s-img', { opacity: 0, y: 30, scale: 0.96 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: 'power2.out' }, %.3f);" % (bid, base_at))
    if space:   # entry: the window turns into place, then the camera keeps drifting for the rest of the scene
        d0, d1 = float(b.get("turn", [24, 9])[0]), float(b.get("turn", [24, 9])[1])
        js("tl.fromTo('#%s-rig', { rotationY: %.1f, rotationX: 5 }, { rotationY: %.1f, rotationX: 2, duration: 0.9, ease: 'power3.out' }, %.3f);" % (bid, d0, d1, t_in))
        js("tl.to('#%s-rig', { rotationY: %.1f, rotationX: -2, duration: %.3f, ease: 'sine.inOut' }, %.3f);" % (bid, float(b.get("drift_to", -9)), max(1.0, t_out - t_in - 0.9), t_in + 0.9))
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
