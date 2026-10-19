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
        pk = at; h = d / 2
        blobs = [("#ff7a1a", 1100, 900, -200, 250, 0.9), ("#ffd48a", 800, 700, 600, -150, 0.8), ("#ff2a55", 900, 800, 1300, 450, 0.65)]
        html = ""
        for i, (c, w, hh, x, y, op) in enumerate(blobs):
            html += '<div class="fx-blob" id="%s-l%d" style="background:%s;width:%dpx;height:%dpx;left:%dpx;top:%dpx"></div>' % (bid, i, c, w, hh, x, y)
            js("tl.fromTo('#%s-l%d', { opacity: 0, x: -140 }, { opacity: %.2f, x: 40, duration: %.3f, ease: 'sine.inOut' }, %.3f);" % (bid, i, op, h, pk - h + 0.06 * i))
            js("tl.to('#%s-l%d', { opacity: 0, x: 220, duration: %.3f, ease: 'sine.inOut' }, %.3f);" % (bid, i, h, pk + 0.06 * i))
        return html
    if k == "burn":
        pk = at; h = d / 2
        grad = "radial-gradient(circle at %d%% %d%%, #fff 0%%, #ffe3a8 16%%, #ff8a1f 38%%, #c01d00 60%%, rgba(120,0,0,0) 80%%)" % (b.get("x", 70), b.get("y", 60))
        js("tl.fromTo('#%s-f', { opacity: 0, scale: 0.35 }, { opacity: 1, scale: 2.6, duration: %.3f, ease: 'power2.in' }, %.3f);" % (bid, h, pk - h))
        for s in range(5):   # film flicker while it burns
            js("tl.set('#%s-f', { opacity: %.2f }, %.3f);" % (bid, 0.7 + 0.3 * rnd.random(), pk - h + h * (s + 1) / 6))
        js("tl.fromTo('#%s-f', { opacity: 1 }, { opacity: 0, scale: 2.9, duration: %.3f, ease: 'power2.out', immediateRender: false }, %.3f);" % (bid, h, pk))
        return '<div class="fx-fill" id="%s-f" style="background:%s;transform-origin:%d%% %d%%"></div>' % (bid, grad, b.get("x", 70), b.get("y", 60))
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
