"""counter.py: numbers that are said out loud, made visible (format 48). Cards whose value counts up on the word, and a split bar for
"this part is mine, the whole thing is that big". From the teardown of Joseph's video (01/11/2026): his "quanto tempo serve" plate puts a time
chip under each of seven cards in the instant he says it, then a bar splits "30 min mine" from "1h40 in all".

Usage (compose.py "raw_html"/"raw_js", or a build script):
    import sys; sys.path.insert(0, "<SK>/formats"); from counter import counter
    out = counter(items=[("Studio", "≈10 ore", 98.0, "dieci ore"), ("Piano", "≈15 min", 101.2, "un quarto d'ora"), ("Storyboard", "≈30 min", 104.0, "mezz'oretta")],
                  title="Quanto *tempo* serve", t_in=96.0, t_out=114.0,
                  bar=(0.34, "≈30 min miei, dentro *1h40* in tutto", 109.0, "mezz'ora"))
items: 2 to 5 of (label, value, time the value lands, anchor phrase). The first integer in the value counts up (0.6 s); "≈", "h", "min" stay.
bar: (fraction 0..1, line under the bar with *key* markup, time, anchor), optional. Bar and cards sit left of the face PiP (checked).
Seek-safe: counting uses the same put()/onUpdate pattern as compose.py; every tween is a fromTo.
"""
import json, re
from plates_base import *


def counter(items, title, t_in, t_out, bar=None, sub=None, bg=True, cid="ct", sound=True):
    n = len(items)
    assert 2 <= n <= 5, "two to five cards"
    gap = 30; cw = min(340, (1700 - gap * (n - 1)) // n); ch = 330; barw = min(n * cw + (n - 1) * gap, 1380)
    total = n * cw + (n - 1) * gap; x0 = 110; y0 = 320
    check_pip(x0, y0, total, ch, "counter cards")
    if bar:
        check_pip(110, 690, barw, 100, "counter bar")
    css = BASE_CSS + """
  .ct-c { position:absolute; width:%dpx; height:%dpx; top:%dpx; padding:24px 24px 0; }
  .ct-n { font-family:var(--k-font); font-weight:800; font-size:26px; color:var(--k-accent2); filter:brightness(.62) saturate(1.4); }
  .ct-l { margin-top:12px; font-family:var(--k-font); font-weight:700; font-size:32px; line-height:1.12; letter-spacing:-.01em; }
  .ct-v { position:absolute; left:24px; bottom:22px; font-family:var(--k-font); font-weight:800; font-size:66px; letter-spacing:-.03em; white-space:nowrap; opacity:0;
          font-variant-numeric:tabular-nums; }
  .ct-bar { position:absolute; left:110px; top:690px; width:%dpx; height:26px; border-radius:13px; background:rgba(244,239,230,.14); opacity:0; overflow:hidden; }
  .ct-bar i { display:block; height:100%%; width:100%%; border-radius:13px; background:var(--k-accent2); box-shadow:0 0 30px rgba(94,230,168,.55); transform-origin:0 50%%; }
""" % (cw, ch, y0, barw)
    inner = '<div class="pl-t" id="ctT" style="left:110px;top:130px;font-size:108px;line-height:1.05">%s</div>\n' % keyword(title)
    if sub:
        inner += '<div class="pl-sub" id="ctS" style="left:112px;top:262px;font-size:34px">%s</div>\n' % keyword(sub)
    parts = []
    for i, (label, value, t, anchor) in enumerate(items):
        m = re.search(r"\d+", value)
        parts.append((value[:m.start()], int(m.group()), value[m.end():]) if m else (value, None, ""))
        inner += ('<div class="pl-card ct-c" id="ctc%d" style="left:%dpx"><div class="ct-n">%02d</div><div class="ct-l">%s</div>'
                  '<div class="ct-v" id="ctv%d"%s>%s</div></div>\n' % (i, x0 + i * (cw + gap), i + 1, esc(label), i, at_attrs(t, anchor), esc(value)))
    if bar:
        frac, line, tb, ab = bar
        inner += '<div class="ct-bar" id="ctB"%s><i id="ctBi"></i></div>\n<div class="pl-sub" id="ctBl" style="left:112px;top:734px;font-size:34px">%s</div>\n' % (at_attrs(tb, ab), keyword(line))
    html, pre, post = wrap(cid, t_in, t_out, css, inner, bg=bg, kicks=[it[2] for it in items] + ([bar[2]] if bar else []), sound=sound)
    js = list(pre)
    js.append("tl.set('#ctT', { opacity:0, y:14 }, 0);")
    js.append(fromto("#ctT", "{opacity:0,y:14}", "{opacity:1,y:0}", t_in + 0.15, 0.45))
    if sub:
        js.append("tl.set('#ctS', { opacity:0, y:10 }, 0);")
        js.append(fromto("#ctS", "{opacity:0,y:10}", "{opacity:1,y:0}", t_in + 0.35, 0.45))
    for i, (label, value, t, anchor) in enumerate(items):
        js.append("tl.set('#ctc%d', { opacity:0, y:40, filter:'blur(8px)' }, 0); tl.set('#ctv%d', { opacity:0, y:12 }, 0);" % (i, i))
        js.append(fromto("#ctc%d" % i, "{opacity:0,y:40,filter:'blur(8px)'}", "{opacity:1,y:0,filter:'blur(0px)'}", t_in + 0.35 + 0.07 * i, 0.5))
        js.append(fromto("#ctv%d" % i, "{opacity:0,y:12}", "{opacity:1,y:0}", t - 0.05, 0.35))
        pre_s, num, suf = parts[i]
        if num is not None:   # the first integer counts up while the chip lands
            js.append("(function(){ var el = document.getElementById('ctv%d'), o = { v: 0 }, A = %s, B = %s, put = function () { el.textContent = A + Math.round(o.v) + B; };"
                      " put(); tl.fromTo(o, { v: 0 }, { v: %d, duration: 0.6, ease: 'power2.out', immediateRender: false, onUpdate: put }, %.3f); })();"
                      % (i, json.dumps(pre_s), json.dumps(suf), num, t - 0.05))
    if bar:
        frac, line, tb, ab = bar
        js.append("tl.set('#ctB', { opacity:0 }, 0); tl.set('#ctBi', { scaleX:0 }, 0); tl.set('#ctBl', { opacity:0, y:10 }, 0);")
        js.append(fromto("#ctB", "{opacity:0}", "{opacity:1}", tb - 0.2, 0.3))
        js.append(fromto("#ctBi", "{scaleX:0}", "{scaleX:%.3f}" % frac, tb, 0.8, "power2.out"))
        js.append(fromto("#ctBl", "{opacity:0,y:10}", "{opacity:1,y:0}", tb + 0.15, 0.45))
    js.extend(post)
    return {"html": html, "js": "\n        ".join(js)}
