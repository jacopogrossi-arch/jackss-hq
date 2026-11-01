"""versus.py: the side-by-side comparison (format 49). Two cards, one on each side, each landing on the word that names it, then a verdict.
From the teardown of Joseph's video (01/11/2026): when he says "put the two products one on the right and one on the left so you can see them
together", the plate is exactly that, never one after the other. Our rule: a comparison is always side by side.

Usage (compose.py "raw_html"/"raw_js", or a build script):
    import sys; sys.path.insert(0, "<SK>/formats"); from versus import versus
    out = versus(left={"label": "ElevenLabs", "sub": "la voce più nota", "t": 4.0, "anchor": "elevenlabs"},
                 right={"label": "Fish Audio", "sub": "il clone che uso", "t": 5.4, "anchor": "fish audio"},
                 title="Chi suona *meglio*?", t_in=3.0, t_out=12.0, win="right", win_at=9.0, win_anchor="questo")
left/right: label (str, *word* markup allowed), sub (optional), t, anchor, logo (optional image path, shown above the label).
win: "left" | "right" | None; at win_at the winner takes the ring and the other card dims to .55. vs=True puts a small "vs" between the cards
when both are in. The cards stop at y 640, clear of the face PiP corner (checked). Seek-safe: every tween is a fromTo.
"""
from plates_base import *


def versus(left, right, title, t_in, t_out, win=None, win_at=None, win_anchor="", vs=True, sub=None, bg=True, cid="vs"):
    cw, ch, y0 = 700, 400, 250
    xl, xr = 130, 1090
    check_pip(xl, y0 - 20, xr + cw - xl, ch + 40, "versus cards")
    css = BASE_CSS + """
  .vs-c { position:absolute; width:%dpx; height:%dpx; top:%dpx; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:30px; }
  .vs-c img { height:120px; margin-bottom:22px; }
  .vs-l { font-family:var(--k-font); font-weight:800; font-size:78px; line-height:1.05; letter-spacing:-.025em; }
  .vs-l .pl-key { color:#0b0907; filter:brightness(.7) saturate(1.6); }
  .vs-s { margin-top:16px; font-family:var(--k-font); font-weight:600; font-size:34px; color:rgba(11,9,7,.62); }
  .vs-v { position:absolute; left:910px; top:%dpx; width:100px; height:100px; margin:0; border-radius:50%%; background:var(--k-accent2); color:#06140d; opacity:0;
          font-family:var(--k-serif); font-style:italic; font-weight:500; font-size:50px; line-height:100px; text-align:center; box-shadow:0 0 36px rgba(94,230,168,.5); }
""" % (cw, ch, y0, y0 + ch // 2 - 50)
    def card(side, x, d, k):
        lg = '<img src="%s" alt="">' % esc(d["logo"]) if d.get("logo") else ""
        s = '<div class="vs-s">%s</div>' % keyword(d["sub"]) if d.get("sub") else ""
        return ('<div class="pl-card vs-c" id="vsc%s" style="left:%dpx"%s>%s<div class="vs-l">%s</div>%s</div>\n'
                % (k, x, at_attrs(d["t"], d.get("anchor", "")), lg, keyword(d["label"]), s))
    inner = '<div class="pl-t" id="vsT" style="left:110px;top:100px;font-size:96px;line-height:1.05">%s</div>\n' % keyword(title)
    inner += card("l", xl, left, "l") + card("r", xr, right, "r")
    if vs:
        inner += '<div class="vs-v" id="vsV">vs</div>\n'
    html, pre, post = wrap(cid, t_in, t_out, css, inner, bg=bg)
    js = list(pre)
    js.append("tl.set('#vsT', { opacity:0, y:14 }, 0);")
    js.append(fromto("#vsT", "{opacity:0,y:14}", "{opacity:1,y:0}", t_in + 0.15, 0.45))
    for k, d, dx in (("l", left, -70), ("r", right, 70)):
        js.append("tl.set('#vsc%s', { opacity:0, x:%d, filter:'blur(8px)' }, 0);" % (k, dx))
        js.append(fromto("#vsc%s" % k, "{opacity:0,x:%d,filter:'blur(8px)'}" % dx, "{opacity:1,x:0,filter:'blur(0px)'}", d["t"] - 0.05, 0.55))
    if vs:
        both = max(left["t"], right["t"]) + 0.35
        js.append("tl.set('#vsV', { opacity:0, scale:0.6 }, 0);")
        js.append(fromto("#vsV", "{opacity:0,scale:0.6}", "{opacity:1,scale:1}", both, 0.4, "power2.out"))
    if win in ("left", "right"):
        w, o = ("l", "r") if win == "left" else ("r", "l")
        tw = win_at if win_at is not None else max(left["t"], right["t"]) + 2.0
        js.append(fromto("#vsc%s" % w, "{scale:1,boxShadow:'0 30px 60px rgba(0,0,0,.5)'}",
                         "{scale:1.04,boxShadow:'0 0 0 5px var(--k-accent2), 0 0 56px rgba(94,230,168,.55), 0 36px 70px rgba(0,0,0,.55)'}", tw, 0.5))
        js.append(fromto("#vsc%s" % o, "{opacity:1}", "{opacity:0.55}", tw, 0.5, "power2.inOut"))
    js.extend(post)
    return {"html": html, "js": "\n        ".join(js)}
