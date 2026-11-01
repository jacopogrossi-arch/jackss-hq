"""tracker.py: the recurring step map (format 47). A row of numbered cards, the finished ones ticked, the current one lifted and ringed.
From the teardown of Joseph's video (01/11/2026): his "7 step" row comes back eight times in 12 minutes, and each time the state is different, so
the viewer always knows where they are without a word. In our long videos it is the same plate shown again at every chapter change (~3 s).

Usage (compose.py "raw_html"/"raw_js", or a build script):
    import sys; sys.path.insert(0, "<SK>/formats"); from tracker import tracker
    out = tracker(steps=["Reference", "Audio", "Piano", "Storyboard", "Montaggio", "Revisioni", "Suoni"], active=3,
                  title="*7* step", t_in=96.0, t_out=100.5, at=97.6, anchor="storyboard")
steps: 3 to 7 labels. active: index of the current step (the finished ones are the steps before it unless done=[...] says otherwise).
title: "*word*" puts the starred word in the italic serif key colour. at/anchor: the moment (and spoken word) the active card lifts.
Layout: the row sits at y 330 to 600, clear of the face PiP corner (checked). Colours/fonts/grid from the preset tokens (--k-*).
Seek-safe: every tween is a fromTo with explicit values.
"""
from plates_base import *

CHECK = '<svg viewBox="0 0 36 36"><path d="M10 18.5 L16 24.5 L26.5 12.5" fill="none" stroke="#06140d" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def tracker(steps, active, title, t_in, t_out, at=None, anchor="", done=None, sub=None, bg=True, cid="tk", sound=True):
    n = len(steps)
    assert 3 <= n <= 7 and 0 <= active < n, "three to seven steps, active inside them"
    done = list(range(active)) if done is None else list(done)
    gap = 34
    cw = min(250, (1700 - gap * (n - 1)) // n); ch = 270
    total = n * cw + (n - 1) * gap; x0 = (1920 - total) // 2; y0 = 330
    check_pip(x0, y0 - 40, total, ch + 80, "tracker")
    t_act = at if at is not None else t_in + 1.2
    css = BASE_CSS + """
  .tk-c { position:absolute; width:%dpx; height:%dpx; top:%dpx; padding:22px 22px 0; transform-origin:50%% 60%%; }
  .tk-n { font-family:var(--k-font); font-weight:800; font-size:26px; color:var(--k-accent2); filter:brightness(.62) saturate(1.4); }
  .tk-l { margin-top:14px; font-family:var(--k-font); font-weight:700; font-size:31px; line-height:1.12; letter-spacing:-.01em; }
  .tk-bar { position:absolute; left:22px; right:22px; bottom:22px; height:8px; border-radius:4px; background:rgba(11,9,7,.12); overflow:hidden; }
  .tk-bar i { display:block; height:100%%; width:100%%; background:var(--k-accent2); transform-origin:0 50%%; filter:brightness(.8); }
""" % (cw, ch, y0)
    inner = '<div class="pl-t" id="tkT" style="left:110px;top:130px;font-size:108px;line-height:1.05">%s</div>\n' % keyword(title)
    if sub:
        inner += '<div class="pl-sub" id="tkS" style="left:112px;top:262px;font-size:34px">%s</div>\n' % keyword(sub)
    for i, name in enumerate(steps):
        x = x0 + i * (cw + gap)
        ck = '<span class="pl-ck" id="tkk%d" style="right:18px;top:18px">%s</span>' % (i, CHECK) if i in done else ""
        bar = '<div class="tk-bar"><i id="tkb%d"></i></div>' % i if i in done else ""
        inner += ('<div class="pl-card tk-c" id="tkc%d" style="left:%dpx"%s><div class="tk-n">%02d</div><div class="tk-l">%s</div>%s%s</div>\n'
                  % (i, x, at_attrs(t_act, anchor) if i == active else "", i + 1, esc(name), ck, bar))
    html, pre, post = wrap(cid, t_in, t_out, css, inner, bg=bg, kicks=[t_in + 0.4, t_act], sfx_events=[t_in + 0.5, t_act], sound=sound)
    js = list(pre)
    js.append("tl.set('#tkT', { opacity:0, y:14 }, 0);")
    js.append(fromto("#tkT", "{opacity:0,y:14}", "{opacity:1,y:0}", t_in + 0.15, 0.45))
    if sub:
        js.append("tl.set('#tkS', { opacity:0, y:10 }, 0);")
        js.append(fromto("#tkS", "{opacity:0,y:10}", "{opacity:1,y:0}", t_in + 0.35, 0.45))
    for i in range(n):
        t0 = t_in + 0.35 + 0.07 * i
        rest = 1.0 if (i in done or i == active) else 0.6
        js.append("tl.set('#tkc%d', { opacity:0, y:40, filter:'blur(8px)' }, 0);" % i)
        js.append(fromto("#tkc%d" % i, "{opacity:0,y:40,filter:'blur(8px)'}", "{opacity:%s,y:0,filter:'blur(0px)'}" % rest, t0, 0.5))
        if i in done:
            js.append("tl.set('#tkk%d', { opacity:0, scale:0.5 }, 0); tl.set('#tkb%d', { scaleX:0 }, 0);" % (i, i))
            js.append(fromto("#tkk%d" % i, "{opacity:0,scale:0.5}", "{opacity:1,scale:1}", t0 + 0.45, 0.3, "power2.out"))
            js.append(fromto("#tkb%d" % i, "{scaleX:0}", "{scaleX:1}", t0 + 0.4, 0.5))
    # the current step lifts and takes a ring; the pending ones stay dim
    js.append(fromto("#tkc%d" % active, "{y:0,scale:1,boxShadow:'0 30px 60px rgba(0,0,0,.5)'}",
                     "{y:-26,scale:1.07,boxShadow:'0 0 0 4px var(--k-accent2), 0 0 44px rgba(94,230,168,.55), 0 36px 70px rgba(0,0,0,.55)'}", t_act, 0.45))
    js.extend(post)
    return {"html": html, "js": "\n        ".join(js)}
