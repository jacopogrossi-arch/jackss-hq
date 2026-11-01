"""pip.py: the face in a square window (picture-in-picture) while a full-frame plate is on screen (Jacopo, 28/10/2026: "la 1 però quadrata"; "non far mai andare le grafiche sotto alla testa").
Until 01/11/2026 this lived only in the bench builder `videos/_bench/ab/plate-pip/build.py`; this module is that builder, for any storyboard.

The PiP is NOT a second video: it is the base video's wrapper (`#video-wrap`), which rises above the plate (z-index 20) and is scaled into the corner with a clip-path, so the lips stay in sync and there is one audio. A mint ring
(plates-verde; the older presets used cyan) fades in as the face lands and out as it leaves. The corner and size are `plates_base.PIP` (320 x 320 at left 1552 / top 712): the plate formats keep clear of it (`check_pip`).

Usage (a storyboard's raw_html / raw_js, next to the plate it goes with):
    import sys; sys.path.insert(0, "<SK>/formats"); from pip import pip
    p = pip(t_in=66.8, t_out=71.4, crop=(630, 250, 700), cid="pip1")
    storyboard["raw_html"] += p["html"]; storyboard["raw_js"] += "\\n" + p["js"]
crop = (x, y, side) of a square on the face in 1920 x 1080 coordinates (measure it on a frame: the head and a bit of shoulders). The plate's first element should enter only after the face has landed
(t_in + MOVE - 0.1): the plate formats start their first element at t_in + 0.35 or later, so give pip() the same t_in as the plate.
Several PiPs in one storyboard need different `cid`s. Seek-safe: every tween is a fromTo with explicit values.
"""
from plates_base import PIP

MOVE = 0.55


def pip(t_in, t_out, crop=(570, 250, 700), cid="pip", ring="#5EE6A8", radius=28, move=MOVE):
    cx, cy, side = crop
    tx, ty, size = PIP[0], PIP[1], PIP[2]
    s = size / side
    x, y = tx - cx * s, ty - cy * s
    r_el = radius / s                                   # the radius in the video's own coordinates, before the scale
    full = "inset(0px 0px 0px 0px round 0px)"
    small = "inset(%dpx %dpx %dpx %dpx round %.1fpx)" % (cy, 1920 - cx - side, 1080 - cy - side, cx, r_el)
    rgb = ",".join(str(int(ring.lstrip("#")[i:i + 2], 16)) for i in (0, 2, 4))
    html = ('<div class="card-host clip" id="host-%(c)s" data-card-id="%(c)s" data-unanchored="1" data-start="%(a).3f" data-duration="%(d).3f" data-track-index="5"'
            ' style="left:0;top:0;width:1920px;height:1080px;visibility:hidden;opacity:1;"><div id="%(c)s-ring" style="position:absolute;left:%(l)dpx;top:%(t)dpx;width:%(w)dpx;height:%(w)dpx;'
            'border-radius:%(r)dpx;border:3px solid %(ring)s;box-shadow:0 0 28px rgba(%(rgb)s,.45), 0 18px 50px rgba(0,0,0,.55);box-sizing:border-box;opacity:0;"></div></div>\n'
            % dict(c=cid, a=t_in, d=t_out - t_in, l=tx - 3, t=ty - 3, w=size + 6, r=radius + 3, ring=ring, rgb=rgb))
    js = [
        "tl.set('#video-wrap', { transformOrigin:'0px 0px' }, 0);",
        "tl.set('#video-wrap', { zIndex:20 }, %.3f);" % t_in,
        "tl.fromTo('#video-wrap', { x:0, y:0, scale:1, clipPath:'%s' }, { x:%.1f, y:%.1f, scale:%.4f, clipPath:'%s', duration:%.3f, ease:'power3.inOut', immediateRender:false }, %.3f);" % (full, x, y, s, small, move, t_in),
        "tl.set('#%s-ring', { opacity:0 }, 0);" % cid,
        "tl.fromTo('#%s-ring', { opacity:0 }, { opacity:1, duration:0.3, ease:'power2.out', immediateRender:false }, %.3f);" % (cid, t_in + move - 0.15),
        "tl.fromTo('#%s-ring', { opacity:1 }, { opacity:0, duration:0.15, ease:'power2.in', immediateRender:false }, %.3f);" % (cid, t_out - move),
        "tl.fromTo('#video-wrap', { x:%.1f, y:%.1f, scale:%.4f, clipPath:'%s' }, { x:0, y:0, scale:1, clipPath:'%s', duration:%.3f, ease:'power3.inOut', immediateRender:false }, %.3f);" % (x, y, s, small, full, move, t_out - move),
        "tl.set('#video-wrap', { zIndex:1 }, %.3f);" % t_out,
    ]
    return {"html": html, "js": "\n        ".join(js)}
