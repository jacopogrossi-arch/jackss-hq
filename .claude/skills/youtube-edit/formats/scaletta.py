"""scaletta.py: the outline rail (format 44), a list read out as a script outline: a dotted rail on the free side of the
face, one coloured dot per item, its name, a "×N" in italic serif and N thin bars drawing under it. Built on the bench A/B
of 23/10/2026 (`videos/_bench/ab/lista-timeline/`), after the @realskytan reel (his Introduction / Struggle / Rise outline):
it beat the glass list (3a) on the `lista` window; the creator: "perfect".

Usage (any build script, or compose.py's "raw_html"/"raw_js"):
    import sys; sys.path.insert(0, "<SK>/formats"); from scaletta import scaletta
    out = scaletta(items=[("Outfit", 7.26, "tre outfit", 3), ...], title="Cosa doveva uscire", t_in=6.2, t_out=11.5)
    storyboard["raw_html"] = out["html"]; storyboard["raw_js"] = out["js"]
items: (name, time the item's word lands, anchor phrase, count shown as "×N" and drawn as N bars, 1 to 5; 0 = no count),
two to five items. The rail sits left of the face (x 110 to ~640). No card behind it: a soft linear wash from the left edge
fades in with the first item. Colours from the elegante-portfolio preset: gold, emerald and their light mixes. No sound.
Spec and numbers: references/formats.md, 44. Seek-safe: every tween is a fromTo with explicit values.
"""

COLS = ["#d4af5f", "#4aa585", "#e3c47f", "#89c4b0", "#d4af5f"]
BARW = [300, 240, 270, 220, 260]
EASE = "power3.out"


def scaletta(items, title, t_in, t_out):
    n = len(items)
    assert 2 <= n <= 5, "two to five items"
    T = [it[1] for it in items]
    HY = [330 + 118 * k for k in range(n)]; YC = [y + 23 for y in HY]
    RAIL_Y = [(322, YC[0])] + [(YC[k - 1], YC[k]) for k in range(1, n)]
    css = """
  .tlp { position:absolute; left:0; top:0; width:1920px; height:1080px; }
  .tl-wash { position:absolute; left:0; top:0; width:760px; height:1080px; opacity:0;
    background: linear-gradient(90deg, rgba(9,7,5,.62) 0%, rgba(9,7,5,.4) 45%, rgba(9,7,5,0) 100%); }
  .tl-title { position:absolute; left:110px; top:250px; font-family:"Playfair Display", Georgia, serif; font-style:italic; font-weight:500;
    font-size:40px; line-height:48px; color:#f4efe6; white-space:nowrap; opacity:0; text-shadow:0 2px 14px rgba(0,0,0,.55); }
  .tl-seg { position:absolute; left:139px; width:2px;
    background: repeating-linear-gradient(to bottom, rgba(255,255,255,.35) 0 6px, rgba(255,255,255,0) 6px 12px); clip-path: inset(0 0 100% 0); }
  .tl-e { position:absolute; left:0; top:0; width:1920px; height:1080px; }
  .tl-dot { position:absolute; left:132px; width:16px; height:16px; border-radius:50%; opacity:0; }
  .tl-h { position:absolute; left:190px; height:46px; line-height:46px; white-space:nowrap; opacity:0; text-shadow:0 1px 3px rgba(0,0,0,.6), 0 2px 14px rgba(0,0,0,.55); }
  .tl-h .n { font-family:"Inter", "Segoe UI", system-ui, sans-serif; font-weight:600; font-size:38px; }
  .tl-h .x { font-family:"Playfair Display", Georgia, serif; font-style:italic; font-weight:500; font-size:40px; margin-left:18px; }
  .tl-bar { position:absolute; left:190px; height:8px; border-radius:4px; opacity:.8; transform-origin:0 50%; }
"""
    inner = '<div class="tlp" id="tlp"><div class="tl-wash" id="tlw"></div><div class="tl-title" id="tlt">%s</div>\n' % title
    for k in range(n):
        a, b = RAIL_Y[k]
        inner += '<div class="tl-seg" id="tls%d" style="top:%dpx;height:%dpx"></div>\n' % (k, a, b - a)
    for k, (name, t, anchor, count) in enumerate(items):
        c = COLS[k]
        x = '<span class="x">×%d</span>' % count if count else ""
        inner += ('<div class="tl-e" id="tle%d" data-at="%.3f" data-anchor="%s">'
                  '<div class="tl-dot" id="tld%d" style="top:%dpx;background:%s;box-shadow:0 0 14px %s88"></div>'
                  '<div class="tl-h" id="tlh%d" style="top:%dpx;color:%s"><span class="n">%s</span>%s</div>'
                  % (k, t - 0.15, anchor, k, YC[k] - 8, c, c, k, HY[k], c, name, x))
        for j in range(count):
            inner += '<div class="tl-bar" id="tlb%d_%d" style="top:%dpx;width:%dpx;background:%s"></div>' % (k, j, HY[k] + 58 + 16 * j, BARW[j], c)
        inner += '</div>\n'
    inner += '</div>'
    host_in, host_out = t_in - 0.1, t_out + 0.1
    html = ('<style>%s</style>\n<div class="card-host clip" id="host-tl" data-card-id="tl" data-unanchored="1" data-start="%.3f" data-duration="%.3f" data-track-index="3"'
            ' style="left:0;top:0;width:1920px;height:1080px;visibility:hidden;opacity:1;">%s</div>\n' % (css, host_in, host_out - host_in, inner))

    js = []
    def fT(sel, a, b, t, d, ease=EASE):
        js.append("tl.fromTo('%s', %s, Object.assign({}, %s, { duration:%.3f, ease:'%s', immediateRender:false }), %.3f);" % (sel, a, b, d, ease, t))
    js.append("tl.set('#tlp', { x:0, opacity:1 }, 0);")
    js.append("tl.set('#tlw', { opacity:0 }, 0); tl.set('#tlt', { opacity:0, y:12 }, 0);")
    fT('#tlw', "{opacity:0}", "{opacity:1}", round(T[0] - 0.16, 3), 0.4)   # the wash comes in with the first item, not before
    fT('#tlt', "{opacity:0,y:12}", "{opacity:1,y:0}", t_in, 0.4)
    for k, (_, t, _, count) in enumerate(items):
        js.append("tl.set('#tls" + str(k) + "', { clipPath:'inset(0% 0% 100% 0%)' }, 0);")
        js.append("tl.set('#tld%d', { opacity:0, scale:0.6 }, 0); tl.set('#tlh%d', { opacity:0, y:12 }, 0);" % (k, k))
        js.append("tl.set('#tle%d', { opacity:1 }, 0);" % k)
        for j in range(count): js.append("tl.set('#tlb%d_%d', { scaleX:0 }, 0);" % (k, j))
        fT('#tls%d' % k, "{clipPath:'inset(0% 0% 100% 0%)'}", "{clipPath:'inset(0% 0% 0% 0%)'}", t - 0.15, 0.35)
        fT('#tld%d' % k, "{opacity:0,scale:0.6}", "{opacity:1,scale:1}", t - 0.05, 0.35)
        fT('#tlh%d' % k, "{opacity:0,y:12}", "{opacity:1,y:0}", t, 0.4)
        for j in range(count): fT('#tlb%d_%d' % (k, j), "{scaleX:0}", "{scaleX:1}", t + 0.1 + 0.08 * j, 0.5)
        if k < n - 1:
            fT('#tle%d' % k, "{opacity:1}", "{opacity:0.65}", T[k + 1] - 0.1, 0.4, "power2.inOut")
    fT('#tlp', "{opacity:1,x:0}", "{opacity:0,x:-30}", t_out - 0.4, 0.4, "power2.in")
    return {"html": html, "js": "\n        ".join(js)}
