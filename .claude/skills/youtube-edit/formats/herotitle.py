"""herotitle.py: the hero phrase on a living gradient (format 46). A full-screen cut: a radial mask blooms from the
centre onto a dark ground, four blurred colour blobs open like a curtain and then drift slowly, film grain on top, a
slow push 1.00 -> 1.05; the words come out of a blur one by one, a glass logo tile slides in and pushes the first
word, the first line can turn to a gold gradient, the second line is Playfair Italic with a gold gradient and a soft
duplicate glow. Won the blind A/B of 26/10/2026 against the lower line (2) on the strumenti bench window.

Usage (any build script, or compose.py's "raw_html"/"raw_js"):
    import sys; sys.path.insert(0, "<SK>/formats"); from herotitle import herotitle
    out = herotitle(lines=[[("Claude", 1.11)], [("come", 3.99), ("strumento", 4.55)]], t_in=1.11, t_out=5.8,
                    logo="<path>/claude.svg", logo_at=1.59, gold_at=3.11)       # -> {"html", "js"}
    storyboard["raw_html"] = out["html"]; storyboard["raw_js"] = out["js"]
    # the caller copies the logo file to <project>/public/img/<same file name>
lines: 1 or 2 lines, each a list of (word, time the word lands). Line 1 is Inter 700 120 px ivory, line 2 Playfair
Display Italic 110 px, gold->ivory gradient. At most 2 lines and 6 words in all; t_out - t_in between 2 and 7 s.
logo: path of the logo, enters at logo_at to the left of the first word of line 1 and pushes it (the only movement
allowed); gold_at: when line 1 cross-fades to the gold gradient over 0.4 s (None = never). No sound.
Numbers: mask radius 0 -> 1320 px in 0.45 s (soft edge 200 px) and back in 0.4 s ending at t_out; blobs blur 120 px,
curtain 1.2 s then drift 4 s; grain opacity .06; words in 0.5 s with y 20 -> 0 and blur 14 -> 0; tile slot 0 -> 150 px.
Every line is laid out from the first frame at its final position (only opacity is animated, never display, x or
left), so a word appearing never moves the others. Seek-safe: every tween is a fromTo with explicit values.
"""
import os

GRAIN = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'>"
         "<feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1.4 -.2'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>")
CLOSE = 0.4
# (id, colour, size, final centre, opacity, drift (dx, dy))
BLOBS = [("b1", "#d4af5f", 900, (700, 1020), 1.0, (120, -60)),
         ("b2", "#8a5a1c", 1100, (1320, 1090), 1.0, (-140, -80)),
         ("b3", "#4aa585", 700, (260, 230), 0.6, (90, 110)),
         ("b4", "#f4efe6", 400, (1600, 300), 0.25, (-80, 90))]


def herotitle(lines, t_in, t_out, logo=None, logo_at=None, gold_at=None):
    assert 1 <= len(lines) <= 2, "one or two lines"
    assert sum(len(l) for l in lines) <= 6 and all(len(l) >= 1 for l in lines), "a hero phrase: at most 6 words"
    assert 2 <= t_out - t_in <= 7, "between 2 and 7 s on screen"
    assert (logo is None) == (logo_at is None), "logo and logo_at go together"
    for l in lines:
        for _, t in l:
            assert t_in <= t < t_out - CLOSE, "each word lands inside the scene"
    two = len(lines) == 2
    y1, y2 = (470, 610) if two else (540, 540)

    css = """
      #tm { position:absolute; inset:0; overflow:hidden; background:#0b0907; -webkit-mask-image:radial-gradient(circle at 50% 50%, #000 0px, transparent 1px); mask-image:radial-gradient(circle at 50% 50%, #000 0px, transparent 1px); }
      #tcam { position:absolute; inset:0; transform-origin:50% 50%; }
      .bl { position:absolute; border-radius:50%; filter:blur(120px); will-change:transform; }
      #grain { position:absolute; inset:0; opacity:.06; mix-blend-mode:screen; background-image:url("GRAINURL"); }
      .tl-row { position:absolute; left:0; width:1920px; display:flex; justify-content:center; align-items:center; }
      #r1 { top:Y1px; height:150px; margin-top:-75px; gap:36px; }
      #r2 { top:Y2px; height:140px; margin-top:-70px; gap:30px; }
      #tw { position:relative; width:0px; height:120px; flex:none; }
      #tile { position:absolute; left:0; top:0; width:120px; height:120px; border-radius:30px; box-sizing:border-box; border:2px solid rgba(244,239,230,.4);
        background:rgba(244,239,230,.10); backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px); display:flex; align-items:center; justify-content:center; opacity:0; }
      #tile img { width:70px; height:70px; object-fit:contain; display:block; }
      .wd { position:relative; display:grid; opacity:0; }
      .wd > span { grid-area:1/1; white-space:nowrap; line-height:1.1; }
      .w1 span { font-family:"Inter","Segoe UI",sans-serif; font-weight:700; font-size:120px; letter-spacing:-.02em; padding:0 .04em; }
      .w1 .ga { color:#f4efe6; }
      .w1 .gb { background:linear-gradient(100deg,#d4af5f 0%,#f4efe6 100%); -webkit-background-clip:text; background-clip:text; color:transparent; -webkit-text-fill-color:transparent; opacity:0; }
      .w2 span { font-family:"Playfair Display",Georgia,serif; font-style:italic; font-weight:400; font-size:110px; padding:0 .06em; }
      .w2 .gl { color:#d4af5f; filter:blur(18px); opacity:.45; }
      .w2 .mn { background:linear-gradient(100deg,#d4af5f 0%,#f4efe6 100%); -webkit-background-clip:text; background-clip:text; color:transparent; -webkit-text-fill-color:transparent; }
    """.replace("GRAINURL", GRAIN).replace("Y1", str(y1)).replace("Y2", str(y2))

    blobs = ""
    for i, c, s, (cx, cy), op, dr in BLOBS:
        blobs += '<div class="bl" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;opacity:%s"></div>' % (i, cx - s // 2, cy - s // 2, s, s, c, op)
    tile = ""
    if logo:
        tile = '<div id="tw"><div id="tile"><img src="img/%s" alt=""/></div></div>' % os.path.basename(logo)
    r1 = "".join('<div class="wd w1" id="w1_%d"><span class="ga">%s</span><span class="gb">%s</span></div>' % (k, w, w) for k, (w, _) in enumerate(lines[0]))
    r2 = ""
    if two:
        r2 = '<div class="tl-row" id="r2">' + "".join(
            '<div class="wd w2" id="w2_%d"><span class="gl">%s</span><span class="mn">%s</span></div>' % (k, w, w) for k, (w, _) in enumerate(lines[1])) + '</div>'
    inner = ('<div id="tm"><div id="tcam">' + blobs + '<div id="grain"></div><div class="tl-row" id="r1">' + tile + r1 + '</div>' + r2 + '</div></div>')
    html = ('<style>%s</style>\n<div class="card-host clip" id="host-tt" data-card-id="tt" data-unanchored="1" data-start="%.3f" data-duration="%.3f" data-track-index="3"'
            ' style="left:0;top:0;width:1920px;height:1080px;visibility:hidden;opacity:1;"><div class="card">%s</div></div>\n' % (css, t_in, t_out - t_in, inner))

    ent = "{ opacity:1, y:0, filter:'blur(0px)', duration:0.5, ease:'power3.out', immediateRender:false }"
    st = "{ opacity:0, y:20, filter:'blur(14px)' }"
    js = []
    js.append("""(function(){ var m=document.getElementById('tm'); var o={r:0};
          function ap(){ var r=o.r, a=Math.max(0,r-200); var g='radial-gradient(circle at 50%% 50%%, #000 '+a.toFixed(1)+'px, transparent '+Math.max(r,1).toFixed(1)+'px)'; m.style.webkitMaskImage=g; m.style.maskImage=g; }
          ap();
          tl.fromTo(o,{r:0},{r:1320,duration:0.45,ease:'power3.out',immediateRender:false,onUpdate:ap},%.3f);
          tl.fromTo(o,{r:1320},{r:0,duration:%.3f,ease:'power3.in',immediateRender:false,onUpdate:ap},%.3f);
        })();""" % (t_in, CLOSE, t_out - CLOSE))
    js.append("tl.fromTo('#tcam', { scale:1 }, { scale:1.05, duration:%.3f, ease:'none', immediateRender:false }, %.3f);" % (t_out - t_in, t_in))
    for i, c, s, (cx, cy), op, (dx, dy) in BLOBS:
        js.append("tl.fromTo('#%s', { x:%d, scaleX:0.3, scaleY:1.15 }, { x:0, scaleX:1, scaleY:1, duration:1.2, ease:'power2.inOut', immediateRender:false }, %.3f);" % (i, 960 - cx, t_in))
        js.append("tl.fromTo('#%s', { x:0, y:0 }, { x:%d, y:%d, duration:4, ease:'sine.inOut', immediateRender:false }, %.3f);" % (i, dx, dy, t_in + 1.2))
    for k, (w, t) in enumerate(lines[0]):
        js.append("tl.fromTo('#w1_%d', %s, %s, %.3f);" % (k, st, ent, t))
    if logo:
        js.append("tl.fromTo('#tw', { width:0 }, { width:150, duration:0.5, ease:'power3.inOut', immediateRender:false }, %.3f);" % logo_at)
        js.append("tl.fromTo('#tile', { opacity:0, scale:0.6, filter:'blur(10px)' }, { opacity:1, scale:1, filter:'blur(0px)', duration:0.5, ease:'power3.out', immediateRender:false }, %.3f);" % logo_at)
    if gold_at is not None:
        for k in range(len(lines[0])):
            js.append("tl.fromTo('#w1_%d .gb', { opacity:0 }, { opacity:1, duration:0.4, ease:'sine.inOut', immediateRender:false }, %.3f);" % (k, gold_at))
    if two:
        for k, (w, t) in enumerate(lines[1]):
            js.append("tl.fromTo('#w2_%d', %s, %s, %.3f);" % (k, st, ent, t))
    return {"html": html, "js": "\n        ".join(js)}
