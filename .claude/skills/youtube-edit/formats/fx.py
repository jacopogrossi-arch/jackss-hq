"""fx.py: transitions and overlays for the studio compositions (flash, whip, zoomblur, lightleak, burn; vignette, grain).

A transition is a beat {"type":"transition","id","kind","at","dur"?,"color"?,"sfx"?}. `at` is the instant of the cut: the effect peaks there
(the video underneath is whatever the edit does at `at`; a transition hides/dresses the cut, it does not make one). Everything is seek-safe
GSAP (tweens and sets with explicit times); the hosts sit above the graphics (z-index 60). Kinds that glow (lightleak, burn, glitch) are
blended with `screen` on the host itself, so they add light to the picture instead of painting over it.
All the kinds act on #video-wrap (the footage) except the overlays; they never touch the graphics in the studio layer.
"""
import hashlib, random

DEFAULT_DUR = {"flash": 0.34, "whip": 0.42, "zoomblur": 0.46, "lightleak": 1.1, "burn": 0.9}
BLEND = {"lightleak", "burn"}


def dur_of(b):
    return float(b.get("dur", DEFAULT_DUR.get(b.get("kind"), 0.4)))


def window(b):
    """(t_in, t_out) of the host that carries the overlay for a transition / overlay beat."""
    if b["type"] == "overlay":
        return float(b["in"]), float(b["out"])
    at, d, k = float(b["at"]), dur_of(b), b["kind"]
    pre = {"flash": 0.08, "whip": d * 0.55, "zoomblur": d * 0.55, "lightleak": d * 0.5, "burn": d * 0.5}[k]
    return max(0.0, at - pre), at + d + 0.05


def blend(b):
    return b["type"] == "transition" and b.get("kind") in BLEND


def css(style=None):
    return """
  /* fx: transitions and overlays (formats/fx.py) */
  .fx-host { z-index:60; }
  .fx-host.screen { mix-blend-mode:screen; }
  .fx-fill { position:absolute; inset:0; opacity:0; }
  .fx-streak { position:absolute; top:-10%; height:120%; width:520px; left:-700px; opacity:0; transform:skewX(-16deg);
    background:linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.55) 45%, rgba(255,255,255,.9) 50%, rgba(255,255,255,.55) 55%, rgba(255,255,255,0)); }
  .fx-burn { position:absolute; top:-10%; height:120%; width:1500px; left:0; opacity:0; filter:blur(26px); }
  .fx-blob { position:absolute; border-radius:50%; filter:blur(90px); opacity:0; }
  .fx-band { position:absolute; left:-6%; width:112%; opacity:0; }
  .fx-vig { position:absolute; inset:0; background:radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 52%, rgba(0,0,0,.55) 100%); opacity:0; }
  .fx-grain { position:absolute; inset:-120px; opacity:0; background-size:260px 260px;
    background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .9 0'/></filter><rect width='260' height='260' filter='url(%23n)'/></svg>"); }
"""


def _color(b, style, default="white"):
    c = b.get("color", default)
    st = style or {}
    return {"white": "#ffffff", "warm": "#fff1d6", "accent": st.get("accent", "#d4af5f"), "bg": st.get("bg", "#0b0907"), "black": "#000000"}.get(c, c)


def transition(b, bid, js, style=None):
    k, at, d = b["kind"], float(b["at"]), dur_of(b)
    W = "#video-wrap"
    seed = int(hashlib.md5(bid.encode()).hexdigest()[:6], 16)
    rnd = random.Random(seed)
    if k == "flash":
        col = _color(b, style, "white")
        js("tl.fromTo('#%s-f', { opacity: 0 }, { opacity: %.2f, duration: 0.05, ease: 'power2.out' }, %.3f);" % (bid, float(b.get("strength", 0.95)), at - 0.05))
        js("tl.to('#%s-f', { opacity: 0, duration: %.3f, ease: 'power2.in' }, %.3f);" % (bid, d, at))
        js("tl.fromTo('%s', { scale: 1.0 }, { scale: 1.05, duration: 0.05, ease: 'power2.out', immediateRender: false }, %.3f);" % (W, at - 0.05))
        js("tl.to('%s', { scale: 1.0, duration: %.3f, ease: 'power2.out' }, %.3f);" % (W, d, at))
        return '<div class="fx-fill" id="%s-f" style="background:%s"></div>' % (bid, col)
    if k == "whip":
        h = d / 2
        sg = -1 if b.get("dir", "left") == "left" else 1
        js("tl.fromTo('%s', { x: 0, scale: 1.0, filter: 'blur(0px)' }, { x: %d, scale: 1.14, filter: 'blur(20px)', duration: %.3f, ease: 'power3.in' }, %.3f);" % (W, sg * 340, h, at - h))
        js("tl.fromTo('%s', { x: %d, scale: 1.14, filter: 'blur(20px)' }, { x: 0, scale: 1.0, filter: 'blur(0px)', duration: %.3f, ease: 'power3.out', immediateRender: false }, %.3f);" % (W, -sg * 340, h, at))
        js("tl.fromTo('#%s-s', { x: %d, opacity: 0.9 }, { x: %d, opacity: 0.9, duration: %.3f, ease: 'power2.inOut' }, %.3f);" % (bid, 2700 if sg < 0 else 0, 0 if sg < 0 else 2700, d, at - h))
        js("tl.set('#%s-s', { opacity: 0 }, %.3f);" % (bid, at + h + 0.02))
        return '<div class="fx-streak" id="%s-s" ></div>' % bid
    if k == "zoomblur":
        h = d / 2
        js("tl.fromTo('%s', { scale: 1.0, filter: 'blur(0px)' }, { scale: 1.32, filter: 'blur(16px)', duration: %.3f, ease: 'power3.in' }, %.3f);" % (W, h, at - h))
        js("tl.fromTo('%s', { scale: 1.32, filter: 'blur(16px)' }, { scale: 1.0, filter: 'blur(0px)', duration: %.3f, ease: 'power3.out', immediateRender: false }, %.3f);" % (W, h, at))
        js("tl.fromTo('#%s-f', { opacity: 0 }, { opacity: %.2f, duration: 0.06, ease: 'power2.out' }, %.3f);" % (bid, float(b.get("strength", 0.4)), at - 0.03))
        js("tl.to('#%s-f', { opacity: 0, duration: %.3f, ease: 'power2.in' }, %.3f);" % (bid, h, at + 0.03))
        return '<div class="fx-fill" id="%s-f" style="background:%s"></div>' % (bid, _color(b, style, "white"))
    if k == "lightleak":
        # light that leaks in from ONE edge (like film), in the palette's warm tones, peaking on the cut; the footage itself lifts a little.
        pk = at; h = d / 2; side = b.get("side", "left" if rnd.random() < 0.5 else "right"); st = style or {}
        warm = [st.get("accent", "#d4af5f"), "#f0a548", st.get("accent3", "#fff1d6")]
        x0 = -420 if side == "left" else 1920 - 900
        blobs = [(warm[1], 900, 1500, x0, -200, 0.80, -18), (warm[0], 700, 1300, x0 + (260 if side == "left" else -160), 120, 0.85, 12), (warm[2], 380, 900, x0 + (180 if side == "left" else 40), 260, 0.60, -8)]
        html = ""
        sgn = 1 if side == "left" else -1
        # the cut hides under a FULL-FRAME wash: at the peak the whole picture is warm light (a leak that covers only half the frame shows the cut)
        html += '<div class="fx-fill" id="%s-w" style="background:linear-gradient(%ddeg, %s 0%%, %s 55%%, %s 100%%)"></div>' % (bid, 90 if side == "left" else 270, warm[1], warm[0], warm[2])
        js("tl.fromTo('#%s-w', { opacity: 0 }, { opacity: %.2f, duration: %.3f, ease: 'power2.in' }, %.3f);" % (bid, float(b.get("flood", 0.95)), h * 0.75, pk - h * 0.75 - 0.02))
        js("tl.to('#%s-w', { opacity: 0, duration: %.3f, ease: 'power2.out' }, %.3f);" % (bid, h * 1.1, pk + 0.1))
        for i, (c, w, hh, x, y, op, rot) in enumerate(blobs):
            html += '<div class="fx-blob" id="%s-l%d" style="background:%s;width:%dpx;height:%dpx;left:%dpx;top:%dpx;transform:rotate(%ddeg);filter:blur(80px)"></div>' % (bid, i, c, w, hh, x, y, rot)
            t_up = pk - h * 0.9 + 0.05 * i
            js("tl.fromTo('#%s-l%d', { opacity: 0, x: %d }, { opacity: %.2f, x: %d, duration: %.3f, ease: 'power2.out' }, %.3f);" % (bid, i, -sgn * 90, op, sgn * 40, h * 0.9, t_up))
            for q in range(3):   # a little flicker while it burns in
                js("tl.set('#%s-l%d', { opacity: %.2f }, %.3f);" % (bid, i, op * (0.82 + 0.18 * rnd.random()), t_up + h * 0.9 + 0.05 * q))
            js("tl.to('#%s-l%d', { opacity: 0, x: %d, duration: %.3f, ease: 'sine.inOut' }, %.3f);" % (bid, i, sgn * 170, h * 1.2, pk + 0.15 + 0.05 * i))
        js("tl.fromTo('%s', { filter: 'brightness(1) saturate(1)' }, { filter: 'brightness(1.22) saturate(1.12)', duration: %.3f, ease: 'power2.out', immediateRender: false }, %.3f);" % (W, h * 0.9, pk - h * 0.9))
        js("tl.to('%s', { filter: 'brightness(1) saturate(1)', duration: %.3f, ease: 'sine.inOut' }, %.3f);" % (W, h * 1.2, pk + 0.1))
        return html
    if k == "burn":
        # film burn: the footage over-exposes (warm, then washed) as a hot band sweeps across and a flicker runs; peak on the cut
        pk = at; h = d / 2; sg = 1 if b.get("dir", "right") == "right" else -1
        js("tl.fromTo('%s', { filter: 'brightness(1) sepia(0) saturate(1)' }, { filter: 'brightness(2.2) sepia(0.55) saturate(1.5)', duration: %.3f, ease: 'power2.in', immediateRender: false }, %.3f);" % (W, h, pk - h))
        for q in range(4):   # flicker of the overexposure
            js("tl.set('%s', { filter: 'brightness(%.2f) sepia(0.55) saturate(1.5)' }, %.3f);" % (W, 1.7 + 0.6 * rnd.random(), pk - h * 0.8 + h * 0.2 * q))
        js("tl.to('%s', { filter: 'brightness(1) sepia(0) saturate(1)', duration: %.3f, ease: 'power2.out' }, %.3f);" % (W, h * 1.1, pk))
        x_from, x_to = (-1900, 2000) if sg > 0 else (2000, -1900)
        js("tl.fromTo('#%s-b', { x: %d, opacity: 1 }, { x: %d, opacity: 1, duration: %.3f, ease: 'power2.inOut' }, %.3f);" % (bid, x_from, x_to, d, pk - h))
        js("tl.set('#%s-b', { opacity: 0 }, %.3f);" % (bid, pk + h + 0.02))
        js("tl.fromTo('#%s-w', { opacity: 0 }, { opacity: %.2f, duration: %.3f, ease: 'power2.in' }, %.3f);" % (bid, float(b.get("flood", 0.95)), h * 0.7, pk - h * 0.7 - 0.02))
        js("tl.to('#%s-w', { opacity: 0, duration: %.3f, ease: 'power2.out' }, %.3f);" % (bid, h * 1.1, pk + 0.1))
        return '<div class="fx-fill" id="%s-w" style="background:radial-gradient(circle at 60%% 50%%, #fff 0%%, #ffe3b0 45%%, #ff9a3c 100%%)"></div><div class="fx-burn" id="%s-b" style="background:linear-gradient(%ddeg, rgba(150,30,0,0) 0%%, rgba(255,110,25,.85) 34%%, rgba(255,226,170,1) 58%%, #fff 74%%, rgba(255,255,255,0) 100%%)"></div>' % (bid, bid, 90 if sg > 0 else 270)
    raise SystemExit("unknown transition kind %r (flash, whip, zoomblur, lightleak, burn)" % k)


def overlay(b, bid, js, style=None):
    """Looks that stay on a stretch of the video: vignette (darker corners), grain (film noise)."""
    k = b["kind"]; t0, t1 = float(b["in"]), float(b["out"]); op = float(b.get("opacity", 0.5 if k == "vignette" else 0.10))
    if k == "vignette":
        js("tl.fromTo('#%s-o', { opacity: 0 }, { opacity: %.2f, duration: 0.6, ease: 'sine.inOut' }, %.3f);" % (bid, op, t0))
        js("tl.to('#%s-o', { opacity: 0, duration: 0.6, ease: 'sine.inOut' }, %.3f);" % (bid, max(t0 + 0.6, t1 - 0.6)))
        return '<div class="fx-vig" id="%s-o"></div>' % bid
    if k == "grain":
        js("tl.set('#%s-o', { opacity: %.2f }, %.3f);" % (bid, op, t0))
        rnd = random.Random(7); t = t0; step = 0.1
        while t < t1:
            js("tl.set('#%s-o', { x: %d, y: %d }, %.3f);" % (bid, rnd.randint(-110, 110), rnd.randint(-110, 110), t))
            t += step
        js("tl.set('#%s-o', { opacity: 0 }, %.3f);" % (bid, t1))
        return '<div class="fx-grain" id="%s-o"></div>' % bid
    raise SystemExit("unknown overlay kind %r (vignette, grain)" % k)
