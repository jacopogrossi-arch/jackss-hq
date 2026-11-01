"""diagram.py: the metaphor diagram (format 50). One centre node, things that go in on the left, things that come out on the right, dashed
connectors that draw themselves, and what you no longer need struck through. From the teardown of Joseph's video (01/11/2026): "think of Claude
as a brain" is a pink brain with the inputs entering on the left ("reference", "text", "video") and a prompt pill, each on the word that names it;
"it needs arms" is the old tools crossed out and the new one connected. A diagram stays small: three to five objects per side.

Usage (compose.py "raw_html"/"raw_js", or a build script):
    import sys; sys.path.insert(0, "<SK>/formats"); from diagram import diagram
    out = diagram(center={"label": "Claude", "t": 60.6, "anchor": "cervello"},
                  inputs=[{"label": "Reference", "t": 63.0, "anchor": "informazioni"}, {"label": "Le tue indicazioni", "t": 64.5, "anchor": "indicazioni"},
                          {"label": "Premiere", "t": 66.0, "anchor": "premiere", "strike_t": 67.2}],
                  outputs=[{"label": "Lavoro finito", "t": 69.0, "anchor": "lavoro"}], title="Claude come un *cervello*", t_in=59.0, t_out=75.0)
center: label (shown under the node), t, anchor, logo (optional image path), initial (letter shown when there is no logo).
inputs: 1 to 4, outputs: 1 to 3, {label, t, anchor, kind ("prompt" = ringed pill), strike_t (the pill is crossed out and dims at that time)}.
Layout: centre at (940, 490); inputs left (x 100..560), outputs right (x 1360..1820, y <= 560), all above the face PiP corner (checked).
Alive between words: the connector dashes march along the lines (into the node / out of it) for the plate's whole life, the node breathes.
Seek-safe: connectors reveal with a clip-path tween, strikes with scaleX; every tween is a fromTo.
"""
from plates_base import *

CX, CY = 940, 490
PILL_W, PILL_H = 460, 76
XL, XR = 100, 1360
BAD = "#e0645c"


def _ys(n):
    return [CY + (i - (n - 1) / 2) * 108 for i in range(n)]


def diagram(center, inputs, outputs, title, t_in, t_out, sub=None, bg=True, cid="dg", sound=True):
    assert 1 <= len(inputs) <= 4 and 1 <= len(outputs) <= 3, "one to four inputs, one to three outputs (a fourth output would enter the face PiP corner)"
    yi, yo = _ys(len(inputs)), _ys(len(outputs))
    for y in yi:
        check_pip(XL, y - PILL_H / 2, PILL_W, PILL_H, "diagram input")
    for y in yo:
        check_pip(XR, y - PILL_H / 2, PILL_W, PILL_H, "diagram output")
    css = BASE_CSS + """
  .dg-n { position:absolute; left:%dpx; top:%dpx; width:200px; height:200px; border-radius:50%%; opacity:0;
          background:radial-gradient(circle at 38%% 32%%, #fff6e0, var(--k-accent) 60%%, color-mix(in srgb, var(--k-accent) 55%%, #3a2a08)); box-shadow:0 0 90px color-mix(in srgb, var(--k-accent) 55%%, transparent), 0 30px 60px rgba(0,0,0,.5);
          display:flex; align-items:center; justify-content:center; }
  .dg-n img { width:62%%; height:62%%; object-fit:contain; } .dg-n b { font-family:var(--k-serif); font-style:italic; font-weight:500; font-size:96px; color:#2a1d05; }
  .dg-nl { position:absolute; left:%dpx; top:%dpx; width:300px; text-align:center; font-family:var(--k-font); font-weight:700; font-size:34px; color:var(--k-text); opacity:0; }
  .dg-p { position:absolute; width:%dpx; height:%dpx; border-radius:20px; background:rgba(244,239,230,.95); color:#0b0907; opacity:0;
          font-family:var(--k-font); font-weight:700; font-size:32px; line-height:%dpx; text-align:center; box-shadow:0 22px 44px rgba(0,0,0,.45); white-space:nowrap; }
  .dg-p.prompt { background:rgba(11,9,7,.55); color:var(--k-text); box-shadow:0 0 0 3px var(--k-accent2), 0 0 34px rgba(94,230,168,.35); font-weight:600; }
  .dg-x { position:absolute; height:5px; border-radius:3px; background:%s; transform-origin:0 50%%; box-shadow:0 0 16px rgba(224,100,92,.6); }
  .dg-svg { position:absolute; inset:0; width:1920px; height:1080px; overflow:visible; }
  .dg-svg path { fill:none; stroke:var(--k-accent2); stroke-width:4; stroke-linecap:round; stroke-dasharray:3 12; }
""" % (CX - 100, CY - 100, CX - 150, CY + 112, PILL_W, PILL_H, PILL_H, BAD)
    inner = '<div class="pl-t" id="dgT" style="left:110px;top:100px;font-size:96px;line-height:1.05">%s</div>\n' % keyword(title)
    if sub:
        inner += '<div class="pl-sub" id="dgS" style="left:112px;top:226px;font-size:34px">%s</div>\n' % keyword(sub)
    svg = ""
    for i, d in enumerate(inputs):   # input pill right edge -> node left edge
        x1, y1, x2, y2 = XL + PILL_W, yi[i], CX - 100, CY + (i - (len(inputs) - 1) / 2) * 24
        svg += '<svg class="dg-svg" id="dgi%d"><path d="M%d %d C %d %d, %d %d, %d %d"/></svg>' % (i, x1, y1, x1 + 140, y1, x2 - 140, y2, x2, y2)
    for i, d in enumerate(outputs):
        x1, y1, x2, y2 = CX + 100, CY + (i - (len(outputs) - 1) / 2) * 24, XR, yo[i]
        svg += '<svg class="dg-svg" id="dgo%d"><path d="M%d %d C %d %d, %d %d, %d %d"/></svg>' % (i, x1, y1, x1 + 140, y1, x2 - 140, y2, x2, y2)
    inner += svg + "\n"
    c = center
    face = '<img src="%s" alt="">' % esc(c["logo"]) if c.get("logo") else "<b>%s</b>" % esc(c.get("initial", c["label"][:1]))
    inner += '<div class="dg-n" id="dgN"%s>%s</div><div class="dg-nl" id="dgNl">%s</div>\n' % (at_attrs(c["t"], c.get("anchor", "")), face, esc(c["label"]))
    for side, items, ys, x in (("i", inputs, yi, XL), ("o", outputs, yo, XR)):
        for k, d in enumerate(items):
            cls = "dg-p prompt" if d.get("kind") == "prompt" else "dg-p"
            inner += '<div class="%s" id="dgp%s%d" style="left:%dpx;top:%dpx"%s>%s</div>\n' % (cls, side, k, x, ys[k] - PILL_H / 2, at_attrs(d["t"], d.get("anchor", "")), esc(d["label"]))
            if d.get("strike_t") is not None:
                inner += '<div class="dg-x" id="dgx%s%d" style="left:%dpx;top:%dpx;width:%dpx"></div>\n' % (side, k, x + 16, ys[k] - 2, PILL_W - 32)
    html, pre, post = wrap(cid, t_in, t_out, css, inner, bg=bg, sound=sound,
                           kicks=[center["t"]] + [d["t"] for d in inputs + outputs] + [d["strike_t"] for d in inputs + outputs if d.get("strike_t") is not None])
    js = list(pre)
    js.append("tl.set('#dgT', { opacity:0, y:14 }, 0);")
    js.append(fromto("#dgT", "{opacity:0,y:14}", "{opacity:1,y:0}", t_in + 0.15, 0.45))
    if sub:
        js.append("tl.set('#dgS', { opacity:0, y:10 }, 0);")
        js.append(fromto("#dgS", "{opacity:0,y:10}", "{opacity:1,y:0}", t_in + 0.35, 0.45))
    js.append("tl.set('#dgN', { opacity:0, scale:0.7 }, 0); tl.set('#dgNl', { opacity:0, y:10 }, 0);")
    js.append(fromto("#dgN", "{opacity:0,scale:0.7}", "{opacity:1,scale:1}", c["t"] - 0.1, 0.6, "power2.out"))
    js.append(fromto("#dgNl", "{opacity:0,y:10}", "{opacity:1,y:0}", c["t"] + 0.1, 0.45))
    js.append("tl.fromTo('#dgN', { y:0 }, { y:-8, duration:%.3f, ease:'sine.inOut', immediateRender:false }, %.3f);" % (max(t_out - c["t"] - 0.6, 1.0), c["t"] + 0.6))   # alive: a slow breath
    for side, items in (("i", inputs), ("o", outputs)):
        for k, d in enumerate(items):
            p, cn = "#dgp%s%d" % (side, k), "#dg%s%d" % (side, k)
            dx = -60 if side == "i" else 60
            js.append("tl.set('%s', { opacity:0, x:%d, filter:'blur(8px)' }, 0); tl.set('%s', { clipPath:'inset(0 100%% 0 0)' }, 0);" % (p, dx, cn))
            js.append(fromto(p, "{opacity:0,x:%d,filter:'blur(8px)'}" % dx, "{opacity:1,x:0,filter:'blur(0px)'}", d["t"] - 0.05, 0.5))
            js.append(fromto(cn, "{clipPath:'inset(0 100% 0 0)'}", "{clipPath:'inset(0 0% 0 0)'}", d["t"] + 0.1, 0.7, "power2.inOut"))
            run_from = d["t"] + 0.8   # alive: the dashes march along the connector (into the node, or out of it) until the plate ends; ~45 px/s
            js.append("tl.set('%s path', { strokeDashoffset:0 }, 0);" % cn)
            js.append("tl.fromTo('%s path', { strokeDashoffset:0 }, { strokeDashoffset:%d, duration:%.3f, ease:'none', immediateRender:false }, %.3f);"
                      % (cn, -int(45 * max(t_out - run_from, 1.0)), max(t_out - run_from, 1.0), run_from))
            if d.get("strike_t") is not None:   # crossed out, then dimmed: what you no longer need
                s = "#dgx%s%d" % (side, k)
                js.append("tl.set('%s', { scaleX:0 }, 0);" % s)
                js.append(fromto(s, "{scaleX:0}", "{scaleX:1}", d["strike_t"], 0.35, "power2.inOut"))
                js.append(fromto(p, "{opacity:1}", "{opacity:0.4}", d["strike_t"] + 0.2, 0.4, "power2.inOut"))
                js.append(fromto(cn, "{opacity:1}", "{opacity:0.25}", d["strike_t"] + 0.2, 0.4, "power2.inOut"))
    js.extend(post)
    return {"html": html, "js": "\n        ".join(js)}
