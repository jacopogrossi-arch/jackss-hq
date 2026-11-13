# Proof of the UX principles on plates (13/11/2026): four "Prima | Dopo" demos, 26 s, GSAP only. Principles: arcs, follow-through (no bounce), frequency of use, word -> effect delay.
import os, shutil, sys
SK = "D:/ClaudeCodeTest/.claude/skills/youtube-edit"
sys.path.insert(0, SK + "/formats")
import board
from plates_base import repeat_factor

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "public")
os.makedirs(OUT + "/fonts", exist_ok=True)
os.makedirs(OUT + "/vendor", exist_ok=True)
for f in ("Inter.ttf", "PlayfairDisplay-Italic.ttf"):
    shutil.copy(SK + "/assets/fonts/" + f, OUT + "/fonts/" + f)
shutil.copy(SK + "/assets/vendor/gsap.min.js", OUT + "/vendor/gsap.min.js")

GESSO, INK, RUG, BOSCO, SAB = "#EFE9DD", "#1E1B18", "#8A4B2D", "#2F3A2E", "#B9AE98"
SEG = 6.5
SEGS = [
    ("Archi, non <i>rette</i>", "Una swipe diagonale curva del 8%: stessa velocità, percorso più naturale."),
    ("Follow-through, <i>senza rimbalzo</i>", "L'elemento secondario arriva 3 fotogrammi dopo e si posa in ease-out."),
    ("Frequenza <i>d'uso</i>", "Più un elemento ritorna, meno deve animare: 100 %, 70 %, 50 %, 35 %."),
    ("Ritardo <i>parola → effetto</i>", "Il grafico risponde entro 12 fotogrammi (0,40 s) dalla parola che lo apre."),
]
DUR = SEG * len(SEGS)
PX = {"L": 90, "R": 990}      # panel left edges
PY, PW, PH = 300, 840, 600
css = """
@font-face { font-family:"Inter"; src:url("fonts/Inter.ttf"); font-weight:100 900; font-display:block; }
@font-face { font-family:"Playfair"; src:url("fonts/PlayfairDisplay-Italic.ttf"); font-style:italic; font-display:block; }
* { box-sizing:border-box; }
html,body { margin:0; width:100%%; height:100%%; overflow:hidden; background:%(G)s; font-family:"Inter",sans-serif; }
#stage { position:relative; width:1920px; height:1080px; overflow:hidden; background:%(G)s; color:%(I)s; }
.seg { position:absolute; inset:0; display:none; }
h1 { position:absolute; left:90px; top:70px; margin:0; font-size:78px; font-weight:800; letter-spacing:-1px; }
h1 i { font-family:"Playfair",Georgia,serif; font-weight:500; color:%(R)s; }
.sub { position:absolute; left:94px; top:178px; font-size:32px; font-weight:500; color:rgba(30,27,24,.66); }
.panel { position:absolute; top:%(PY)dpx; width:%(PW)dpx; height:%(PH)dpx; border-radius:26px; background:#E5DECF; overflow:hidden; box-shadow:inset 0 0 0 2px rgba(30,27,24,.10); }
.tag { position:absolute; left:26px; top:20px; font:700 26px/1 "Inter",sans-serif; letter-spacing:.12em; color:rgba(30,27,24,.55); }
.tag.good { color:%(B)s; }
.mono { font-family:"Consolas","IBM Plex Mono",monospace; }
.dot { position:absolute; width:120px; height:80px; border-radius:16px; background:%(R)s; box-shadow:0 18px 30px rgba(30,27,24,.22); }
.card { position:absolute; width:380px; height:230px; border-radius:22px; background:%(G)s; box-shadow:0 26px 50px rgba(30,27,24,.25); font-weight:800; font-size:46px; display:flex; align-items:center; justify-content:center; }
.chip { position:absolute; padding:12px 24px; border-radius:16px; background:%(B)s; color:%(G)s; font-weight:700; font-size:32px; box-shadow:0 14px 26px rgba(30,27,24,.25); }
.chap { position:absolute; left:50%%; top:200px; transform:translateX(-50%%); padding:20px 40px; border-radius:20px; background:%(I)s; color:%(G)s; font-weight:700; font-size:44px; letter-spacing:.08em; white-space:nowrap; }
.nth { position:absolute; left:0; right:0; bottom:40px; text-align:center; font-size:30px; font-weight:600; color:rgba(30,27,24,.6); }
.word { position:absolute; top:110px; padding:12px 22px; border-radius:14px; background:#F6F1E6; font-size:34px; font-weight:600; box-shadow:0 8px 16px rgba(30,27,24,.15); }
.head { position:absolute; top:70px; width:4px; height:150px; background:%(R)s; }
.lag { position:absolute; left:0; right:0; bottom:44px; text-align:center; font-size:34px; font-weight:700; }
.foot { position:absolute; left:90px; bottom:36px; font-size:24px; font-weight:500; color:rgba(30,27,24,.5); }
svg { position:absolute; left:0; top:0; width:%(PW)dpx; height:%(PH)dpx; }
""" % dict(G=GESSO, I=INK, R=RUG, B=BOSCO, PY=PY, PW=PW, PH=PH)

html, js = [], []


def T(n, x):
    return round(n * SEG + x, 3)


def fromto(sel, a, b, at, d, ease="power3.out"):
    e = ease if ease.startswith("window.") else "'%s'" % ease
    js.append("tl.fromTo('%s',{%s},{%s,duration:%.3f,ease:%s,immediateRender:false},%.3f);" % (sel, a, b, d, e, at))


def panel(side, n, inner, good):
    return ('<div class="panel" id="s%d%s" style="left:%dpx"><div class="tag%s">%s</div>%s</div>'
            % (n, side, PX[side], " good" if good else "", "DOPO" if good else "PRIMA", inner))


for n, (title, sub) in enumerate(SEGS):
    html_inner = ['<h1>%s</h1><div class="sub">%s</div>' % (title, sub), '<div class="foot">Proposte non ancora votate · test A/B</div>']
    if n == 0:        # ---- arcs
        A, B = (150, 470), (620, 120)                     # panel-local card origin (top-left) start and end
        for side in "LR":
            good = side == "R"
            pts = board.arc_path((A[0], A[1], 1.0), (B[0], B[1], 1.0), "window.__hand", 0.08) if good else [(A[0], A[1], 1.0), (B[0], B[1], 1.0)]
            poly = " ".join("%.1f,%.1f" % (p[0] + 60, p[1] + 40) for p in pts)
            svg = '<svg viewBox="0 0 %d %d"><polyline points="%s" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="3 10" stroke-linecap="round" opacity=".55"/></svg>' % (PW, PH, poly, INK)
            html_inner.append(panel(side, n, svg + '<div class="dot" id="d%s"></div>' % side, good))
            for k, t0 in enumerate((0.9, 3.7)):
                a, b = (A, B) if k == 0 else (B, A)
                at = T(n, t0)
                if not good:
                    fromto("#d%s" % side, "x:%.1f,y:%.1f" % a, "x:%.1f,y:%.1f" % b, at, 1.3, "window.__hand")
                else:
                    wp = board.arc_path((a[0], a[1], 1.0), (b[0], b[1], 1.0), "window.__hand", 0.08)
                    dt = 1.3 / (len(wp) - 1)
                    for j in range(len(wp) - 1):
                        fromto("#d%s" % side, "x:%.1f,y:%.1f" % wp[j][:2], "x:%.1f,y:%.1f" % wp[j + 1][:2], at + j * dt, dt, "none")
            js.append("tl.set('#d%s',{x:%d,y:%d},%.3f);" % (side, A[0], A[1], T(n, 0)))
    elif n == 1:      # ---- follow-through
        for side in "LR":
            good = side == "R"
            inner = '<div class="card" id="c%s">Cotone drill</div><div class="chip" id="l%s">pesante</div>' % (side, side)
            html_inner.append(panel(side, n, inner, good))
            cx, cy = 230, 170
            for k, t0 in enumerate((0.8, 3.7)):
                at = T(n, t0)
                js.append("tl.set('#c%s',{x:-420,y:%d},%.3f);tl.set('#l%s',{x:-420,y:%d,opacity:1},%.3f);" % (side, cy, at - 0.01, side, cy + 250, at - 0.01))
                fromto("#c%s" % side, "x:-420,y:%d" % cy, "x:%d,y:%d" % (cx, cy), at, 0.7, "power3.out")
                if good:
                    fromto("#l%s" % side, "x:-120,y:%d" % (cy + 250), "x:%d,y:%d" % (cx + 20, cy + 250), at + 0.10, 0.7, "power3.out")      # 3 frames later, from a little farther behind
                else:
                    fromto("#l%s" % side, "x:-420,y:%d" % (cy + 250), "x:%d,y:%d" % (cx + 20, cy + 250), at, 0.7, "power3.out")             # welded to the card
                at_out = at + 2.1
                fromto("#c%s" % side, "x:%d" % cx, "x:%d" % (PW + 60), at_out, 0.45, "power2.in")
                fromto("#l%s" % side, "x:%d" % (cx + 20), "x:%d" % (PW + 80), at_out, 0.45, "power2.in")
    elif n == 2:      # ---- frequency of use
        for side in "LR":
            good = side == "R"
            spans = "".join('<span id="n%s%d" style="position:absolute;left:0;right:0;opacity:0">%dª volta · %d%% della durata</span>' % (side, k, k + 1, round((repeat_factor(k + 1) if good else 1.0) * 100)) for k in range(4))
            html_inner.append(panel(side, n, '<div class="chap" id="h%s">CAPITOLO</div><div class="nth">%s</div>' % (side, spans), good))
            for k in range(4):
                at = T(n, 0.5 + 1.5 * k)
                f = repeat_factor(k + 1) if good else 1.0
                d, slide = 0.6 * f, 70 * f
                js.append("tl.set('#h%s',{opacity:0,y:%.1f},%.3f);" % (side, slide, at - 0.01))
                fromto("#h%s" % side, "opacity:0,y:%.1f" % slide, "opacity:%.2f,y:0" % (1.0 if not good else (1.0 if k == 0 else 0.55 + 0.45 * f)), at, d, "power3.out")
                fromto("#h%s" % side, "opacity:1", "opacity:0", at + 1.0, 0.25, "power2.in")
                js.append("tl.set('#n%s%d',{opacity:1},%.3f);tl.set('#n%s%d',{opacity:0},%.3f);" % (side, k, at, side, k, at + 1.3))
    else:             # ---- word -> effect delay
        words = ["Il", "pantalone", "ha", "tre", "vite"]
        xs = [40, 110, 410, 520, 650]
        for side in "LR":
            good = side == "R"
            chips = "".join('<div class="word" style="left:%dpx">%s</div>' % (x, w) for x, w in zip(xs, words))
            inner = chips + '<div class="head" id="p%s"></div><div class="card" id="g%s" style="left:230px;top:300px;opacity:0">3 vite</div><div class="lag mono" id="z%s" style="opacity:0;color:%s">ritardo %.2f s (%d fotogrammi)</div>' % (side, side, side, BOSCO if good else RUG, 0.10 if good else 0.90, 3 if good else 27)
            html_inner.append(panel(side, n, inner, good))
            t_word = T(n, 3.0)                      # the word "vite" starts here
            js.append("tl.set('#g%s',{opacity:0,scale:.9,y:30},%.3f);" % (side, T(n, 0)))
            fromto("#p%s" % side, "x:30", "x:%d" % (xs[4] + 20), T(n, 0.4), 2.6, "none")
            lag = 0.10 if good else 0.90
            fromto("#g%s" % side, "opacity:0,scale:.9,y:30", "opacity:1,scale:1,y:0", t_word + lag, 0.45, "power3.out")
            js.append("tl.set('#z%s',{opacity:1},%.3f);tl.set('#z%s',{opacity:0},%.3f);" % (side, t_word + lag, side, T(n, SEG)))
    html.append('<div class="seg" id="seg%d">%s</div>' % (n, "".join(html_inner)))
    js.append("tl.set('#seg%d',{display:'block'},%.3f);tl.set('#seg%d',{display:'none'},%.3f);" % (n, T(n, 0), n, T(n, SEG)))

page = ('<!doctype html><html lang="it"><head><meta charset="utf-8"><style>%s</style></head><body>'
        '<div id="stage" data-composition-id="ux" data-start="0" data-duration="%.3f" data-fps="30" data-width="1920" data-height="1080">%s'
        '<script src="vendor/gsap.min.js"></script><script>(function(){%s\nconst tl = window.gsap.timeline({paused:true});\n%s\ntl.to({}, {duration:%.3f}, 0);'
        'window.__timelines=window.__timelines||{};window.__timelines["ux"]=tl;})();</script></div></body></html>'
        % (css, DUR, "".join(html), board.HAND_JS, "\n".join(js), DUR))
open(OUT + "/index.html", "w", encoding="utf-8").write(page)
print("ok", DUR, "s", len(js), "tweens")
