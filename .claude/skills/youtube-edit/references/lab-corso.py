# Banco delle prove del corso (04/11/2026). Ogni famiglia e' UNA composizione: le prove si susseguono, ognuna con la sua etichetta in basso a sinistra.
# python gen.py -> mov/ testi/ abb/ (public/index.html). Niente suono: qui si giudica il movimento.
import math, os, random, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.abspath(os.path.join(HERE, "../../03-brand-ai/v4/public"))
INK, IV, MINT, GOLD, BG = "#0b0907", "#f4efe6", "#5EE6A8", "#e3c47f", "#0A2B1E"
STEPS = ["Idea", "Capo", "Foto", "Sito", "Lancio"]

BASE = """
@font-face { font-family:"Inter"; src:url("fonts/Inter.ttf"); font-weight:100 900; font-display:block; }
@font-face { font-family:"Playfair"; src:url("fonts/PlayfairDisplay-Italic.ttf"); font-style:italic; font-display:block; }
* { box-sizing:border-box; }
html,body { margin:0; width:100%; height:100%; overflow:hidden; background:#000; font-family:"Inter",sans-serif; }
#stage { position:relative; width:100%; height:100%; overflow:hidden; background:#000; }
.t { position:absolute; inset:0; overflow:hidden; display:none; color:#f4efe6;
     background:radial-gradient(1100px 700px at 50% 112%, #17613F, transparent 70%), radial-gradient(900px 600px at 10% 0%, rgba(23,97,63,.7), transparent 70%), #0A2B1E; }
.tag { position:absolute; left:36px; bottom:28px; z-index:99; font-weight:600; font-size:30px; color:#f4efe6; background:rgba(0,0,0,.5); padding:8px 18px; border-radius:10px; }
.grid { position:absolute; background:linear-gradient(rgba(120,235,180,.13) 1px, transparent 1px), linear-gradient(90deg, rgba(120,235,180,.13) 1px, transparent 1px); background-size:80px 80px; }
.w { position:absolute; left:0; top:0; width:1920px; height:1080px; transform-origin:0 0; }
.pg { position:absolute; width:1920px; height:1080px; }
.ti { position:absolute; left:0; right:0; top:90px; text-align:center; font-weight:700; font-size:64px; }
.ti em, em { color:#e3c47f; font-style:normal; }
.card { position:absolute; background:#f4efe6; color:#0b0907; border-radius:22px; padding:26px; box-shadow:0 30px 60px rgba(0,0,0,.5); overflow:hidden; }
.card .n { font-weight:800; font-size:30px; color:#1f8a5b; } .card .l { margin-top:14px; font-weight:700; font-size:42px; line-height:1.1; }
.abs { position:absolute; }
"""
HEADJS = """
const BZ = function (x1, y1, x2, y2) { return function (x) { if (x <= 0) return 0; if (x >= 1) return 1; var a = 0, b = 1, t = x, k, u, X;
  for (k = 0; k < 40; k++) { t = (a + b) / 2; u = 1 - t; X = 3*u*u*t*x1 + 3*u*t*t*x2 + t*t*t; if (X < x) a = t; else b = t; }
  u = 1 - t; return 3*u*u*t*y1 + 3*u*t*t*y2 + t*t*t; }; };
const HAND = BZ(.54,0,0,1), C40 = BZ(.5,0,.3,1), CENTER = BZ(.76,0,.16,1), LATE = BZ(1,0,.74,1);
"""


class Lab:
    def __init__(self, name):
        self.name, self.t, self.html, self.js, self.n, self.index = name, 0.0, [], [], 0, []

    def seg(self, label, dur, fn):
        self.n += 1
        P = "%s%d" % (self.name[0], self.n)
        s = Seg(P, self.t)
        h = fn(s) or ""
        self.html.append('<div class="t" id="%s"><div class="tag">%s</div>%s</div>' % (P, label, h))
        self.js.append("tl.set('#%s',{display:'block'},%.3f);tl.set('#%s',{display:'none'},%.3f);" % (P, self.t, P, self.t + dur))
        self.js += s.js
        self.index.append((round(self.t, 2), label))
        self.t += dur

    def write(self, extra_css="", root_attrs=""):
        d = os.path.join(HERE, self.name, "public")
        os.makedirs(os.path.join(d, "fonts"), exist_ok=True); os.makedirs(os.path.join(d, "vendor"), exist_ok=True); os.makedirs(os.path.join(d, "img"), exist_ok=True)
        for f in ("Inter.ttf", "PlayfairDisplay-Italic.ttf"):
            shutil.copy(os.path.join(V4, "fonts", f), os.path.join(d, "fonts", f))
        shutil.copy(os.path.join(V4, "vendor", "gsap.min.js"), os.path.join(d, "vendor"))
        for f in ("ai-foto.jpg", "ai-video.jpg", "ai-royal.jpg", "ai-onlife.jpg"):
            shutil.copy(os.path.join(V4, "img", "pres", f), os.path.join(d, "img", f))
        shutil.copy(os.path.join(HERE, "tile.jpg"), os.path.join(d, "img", "tile.jpg"))
        if os.path.exists(os.path.join(HERE, "clip.mp4")):
            shutil.copy(os.path.join(HERE, "clip.mp4"), os.path.join(d, "clip.mp4"))
        page = ('<!doctype html><html lang="it"><head><meta charset="utf-8"><style>%s%s</style></head><body>'
                '<div id="stage" data-composition-id="prove" data-start="0" data-duration="%.3f" data-fps="30" data-width="1920" data-height="1080"%s>%s'
                '<script src="vendor/gsap.min.js"></script><script>(function(){%s\nconst tl = window.gsap.timeline({paused:true});\n%s\ntl.to({}, {duration:%.3f}, 0);'
                'window.__timelines=window.__timelines||{};window.__timelines["prove"]=tl;})();</script></div></body></html>'
                % (BASE, extra_css, self.t, root_attrs, "\n".join(self.html), HEADJS, "\n".join(self.js), self.t))
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page)
        with open(os.path.join(HERE, self.name, "indice.txt"), "w", encoding="utf-8") as f:
            for t, l in self.index:
                f.write("%6.2f  %s\n" % (t, l))
        print(self.name, "%.1f s" % self.t, len(self.index), "prove")


class Seg:
    def __init__(self, P, T):
        self.P, self.T, self.js, self.seen = P, T, [], set()

    def i(self, x):
        return "#%s-%s" % (self.P, x)

    def ft(self, sel, a, b, at, d, ease="HAND"):
        e = ease if ease.isupper() or "(" in ease and not ease[0].islower() else "'%s'" % ease
        if sel not in self.seen:
            self.seen.add(sel)
            self.js.append("tl.set('%s',{%s},%.3f);" % (sel, a, self.T))
        self.js.append("tl.fromTo('%s',{%s},{%s,duration:%.3f,ease:%s,immediateRender:false},%.3f);" % (sel, a, b, d, e, self.T + at))

    def set(self, sel, a, at=0):
        self.seen.add(sel)
        self.js.append("tl.set('%s',{%s},%.3f);" % (sel, a, self.T + at))


def card(x, y, w, h, n, l, i="", extra=""):
    return '<div class="card" %s style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s"><div class="n">%s</div><div class="l">%s</div></div>' % ('id="%s"' % i if i else "", x, y, w, h, extra, n, l)


def pageA():
    return '<div class="ti">Uno <em>strumento</em></div>' + card(620, 330, 680, 420, "AI", "Da solo non basta: serve il metodo")


def pageB():
    return '<div class="ti">La <em>mappa</em></div>' + "".join(card(145 + k * 330, 400, 300, 270, "%02d" % (k + 1), STEPS[k]) for k in range(5))


def world(s, ox, oy, grid=True, gid="g"):
    """two pages on one board: page A at 0,0 and page B at ox,oy; grid in its own layer"""
    g = '<div class="w" id="%s-%s"><div class="grid" style="left:-2400px;top:-2400px;width:9000px;height:7000px"></div></div>' % (s.P, gid) if grid else ""
    return g + '<div class="w" id="%s-w"><div class="pg">%s</div><div class="pg" style="left:%dpx;top:%dpx">%s</div></div>' % (s.P, pageA(), ox, oy, pageB())


# ---------------------------------------------------------------- MOVIMENTO
def swipe(mode="grid", ease="HAND", d=1.3, vert=False):
    def f(s):
        ox, oy = (0, 1500) if vert else (2500, 0)
        h = world(s, ox, oy, grid=mode != "fermo")
        to = "x:%d,y:%d" % (-ox, -oy)
        s.ft(s.i("w"), "x:0,y:0", to, .7, d, ease)
        if mode != "fermo":
            k = .5 if mode == "fake3d" else 1
            s.ft(s.i("g"), "x:0,y:0", "x:%d,y:%d" % (-ox * k, -oy * k), .7, d, ease)
        return h
    return f


def zoom(ease):
    def f(s):
        h = '<div class="w" id="%s-w"><div class="grid" style="left:-2400px;top:-2400px;width:7000px;height:6000px"></div><div class="pg">%s</div></div>' % (s.P, pageB())
        s.ft(s.i("w"), "x:0,y:0,scale:1", "x:%d,y:%d,scale:1.6" % (960 - 1.6 * 790, 540 - 1.6 * 535), .6, 1.8, ease)
        return h
    return f


def rot(s):
    h = '<div class="w" id="%s-c" style="transform-origin:960px 540px"><div class="grid" style="left:-2400px;top:-2400px;width:9000px;height:7000px"></div><div class="pg">%s</div><div class="pg" style="left:2500px;top:300px">%s</div></div>' % (s.P, pageA(), pageB())
    s.ft(s.i("c"), "x:0,y:0,rotation:0", "x:-2500,y:-300,rotation:0", .7, 1.3, "HAND")
    s.js.pop()
    s.js.append("tl.fromTo('%s',{x:0,y:0,rotation:0,transformOrigin:'960px 540px'},{keyframes:[{x:-1250,y:-150,rotation:-5,duration:.55,ease:'power1.in'},{x:-2500,y:-300,rotation:0,duration:.95,ease:HAND}],immediateRender:false},%.3f);" % (s.i("c"), s.T + .7))
    return h


def phrase(s):
    words = [("Un brand", 300, 430), ("si costruisce", 760, 430), ("un passo", 300, 560), ("alla volta", 760, 560)]
    h = '<div class="w" id="%s-w"><div class="grid" style="left:-2400px;top:-2400px;width:7000px;height:6000px"></div>' % s.P
    for k, (t, x, y) in enumerate(words):
        h += '<div class="abs" id="%s-p%d" style="left:%dpx;top:%dpx;font-weight:800;font-size:92px;white-space:nowrap">%s</div>' % (s.P, k, x, y, t)
    h += "</div>"
    scale, cx, cy = [1.9, 1.55, 1.3, 1.0], [520, 760, 820, 960], [480, 490, 540, 540]
    for k in range(4):
        at = .4 + k * 1.3
        s.ft(s.i("p%d" % k), "opacity:0,y:30,color:'#e3c47f'", "opacity:1,y:0,color:'#e3c47f'", at, .5, "power3.out")
        s.ft(s.i("p%d" % k), "color:'#e3c47f'", "color:'#f4efe6'", at + 1.1, .5, "none")
        tf = "x:%.1f,y:%.1f,scale:%.3f" % (960 - scale[k] * cx[k], 540 - scale[k] * cy[k], scale[k])
        if k == 0:
            s.set(s.i("w"), tf)
        else:
            p = "x:%.1f,y:%.1f,scale:%.3f" % (960 - scale[k-1] * cx[k-1], 540 - scale[k-1] * cy[k-1], scale[k-1])
            s.ft(s.i("w"), p, tf, at - .1, 1.15, "HAND")
    return h


def plate3(s, ids=True):
    return '<div class="ti">Tre <em>prove</em></div>' + "".join(card(240 + k * 500, 360, 440, 380, "%02d" % (k + 1), ["Tela", "Prova", "Taglio"][k], s.i("c%d" % k)[1:]) for k in range(3))


def appear3(s, stagger=.8, dy=40):
    for k in range(3):
        s.ft(s.i("c%d" % k), "opacity:0,y:%d" % dy, "opacity:1,y:0", .4 + k * stagger, .7, "HAND")


def slow(keep):
    def f(s):
        h = '<div class="w" id="%s-w" style="transform-origin:960px 540px"><div class="grid" style="left:-2400px;top:-2400px;width:7000px;height:6000px"></div><div class="pg">%s</div></div>' % (s.P, plate3(s))
        appear3(s)
        s.ft(s.i("w"), "scale:1", "scale:1.07", 0, 6 if keep else 2.6, "none" if keep else "power2.out")
        return h
    return f


def wiggle(on):
    def f(s):
        h = '<div class="grid" style="inset:0"></div><div class="pg">%s</div>' % plate3(s)
        appear3(s)
        if on:
            for k in range(3):
                # sum of two sines, fixed seed by card: the same on every render
                sel = "#%s-q%d" % (s.P, k)
                h = h.replace('id="%s-c%d"' % (s.P, k), 'id="%s-c%d" data-q="%d"' % (s.P, k, k))
                pts = [(math.sin(t * 1.3 + k * 2) * 2.2 + math.sin(t * 2.1 + k) * 1.1, math.cos(t * 1.1 + k) * 2.2 + math.sin(t * 1.9 + k * 3) * 1.1, math.sin(t * .9 + k) * .25) for t in [i * .4 for i in range(16)]]
                for i in range(15):
                    a, b = pts[i], pts[i + 1]
                    s.js.append("tl.fromTo('%s .n,%s .l',{x:%.2f,y:%.2f,rotation:%.3f},{x:%.2f,y:%.2f,rotation:%.3f,duration:.4,ease:'sine.inOut',immediateRender:false},%.3f);" % (s.i("c%d" % k), s.i("c%d" % k), a[0], a[1], a[2], b[0], b[1], b[2], s.T + i * .4))
        return h
    return f


def master(on):
    def f(s):
        h = '<div class="grid" style="inset:0"></div><div class="pg" id="%s-m">%s</div>' % (s.P, plate3(s))
        if on:
            s.ft(s.i("m"), "x:220", "x:0", .3, 2.0, "HAND")
            for k in range(3):
                s.ft(s.i("c%d" % k), "opacity:0,x:%d" % (160 + 80 * k), "opacity:1,x:0", .3 + k * .12, 1.5, "HAND")
        else:
            appear3(s, stagger=.5)
        return h
    return f


def focus(s):
    h = '<div class="ti">Il <em>fuoco</em> sulla parola</div>'
    pos = [(250, 340, 1.0), (760, 400, .85), (1230, 310, 1.15)]
    for k, (x, y, sc) in enumerate(pos):
        h += '<div class="card" id="%s-c%d" style="left:%dpx;top:%dpx;width:420px;height:380px;transform:scale(%s)"><div class="n">%02d</div><div class="l">%s</div></div>' % (s.P, k, x, y, sc, k + 1, ["Tessuto", "Fit", "Prezzo"][k])
    cur = [0, 0, 0]
    for step, on in enumerate((0, 1, 2)):
        at = .4 + step * 1.6
        for k in range(3):
            b = 0 if k == on else (5 + abs(k - on) * 3)
            s.ft(s.i("c%d" % k), "filter:'blur(%dpx)',opacity:%.2f" % (cur[k], 1 if cur[k] == 0 else .75), "filter:'blur(%dpx)',opacity:%.2f" % (b, 1 if b == 0 else .75), at, .8, "HAND")
            cur[k] = b
    return '<div class="grid" style="inset:0"></div>' + h


def peakcut(s):
    h = '<div class="grid" style="inset:0" id="%s-g"></div><div class="w" id="%s-a"><div class="pg">%s</div></div><div class="w" id="%s-b"><div class="pg">%s</div></div>' % (s.P, s.P, pageA(), s.P, pageB())
    s.ft(s.i("a"), "x:0,opacity:1", "x:-1500,opacity:1", .8, 1.2, "CENTER")
    s.ft(s.i("b"), "x:1500,opacity:1", "x:0,opacity:1", .8, 1.2, "CENTER")
    s.set(s.i("a"), "display:'block'", 0); s.set(s.i("a"), "display:'none'", .8 + .56)
    s.set(s.i("b"), "display:'none'", 0); s.set(s.i("b"), "display:'block'", .8 + .56)
    return h


mov = Lab("mov")
mov.seg("1 · Curva D, griglia che segue (oggi)", 3.6, swipe("grid"))
mov.seg("2 · Profondità: la griglia va a metà", 3.6, swipe("fake3d"))
mov.seg("3 · Sfondo fermo, senza griglia", 3.6, swipe("fermo"))
mov.seg("4 · Swipe con curva D", 3.6, swipe("grid"))
mov.seg("5 · Swipe a cupola (stessa durata)", 3.6, swipe("grid", "sine.inOut"))
mov.seg("6 · Dal lato corto: verticale", 3.6, swipe("grid", vert=True))
mov.seg("7 · Un gesto con rotazione", 3.8, rot)
mov.seg("8 · Zoom di oggi (power2.inOut)", 3.6, zoom("power2.inOut"))
mov.seg("9 · Zoom con picco al 40% (a occhio)", 3.6, zoom("C40"))
mov.seg("10 · Frase che si accumula", 6.4, phrase)
mov.seg("11 · Scala che si ferma", 6, slow(False))
mov.seg("12 · Scala lenta unica, mai ferma", 6, slow(True))
mov.seg("13 · Senza tremolio", 5, wiggle(False))
mov.seg("14 · Tremolio leggero", 5, wiggle(True))
mov.seg("15 · Elementi per conto loro", 4, master(False))
mov.seg("16 · Un maestro, partenze sfalsate", 4, master(True))
mov.seg("17 · Il fuoco segue la parola", 6, focus)
mov.seg("18 · Cambio di plate nel picco", 3.6, peakcut)
mov.write()


# ---------------------------------------------------------------- TESTI
def edge(s):
    h = '<div class="grid" style="inset:0"></div><div class="abs" style="left:0;right:0;top:380px;height:190px;overflow:hidden;text-align:center"><div id="%s-a" style="font-weight:800;font-size:150px">Il laboratorio</div></div>' % s.P
    h += '<div class="abs" style="left:0;right:0;top:575px;height:90px;overflow:hidden;text-align:center"><div id="%s-b" style="font-weight:500;font-size:60px;color:#e3c47f">prima del brand</div></div>' % s.P
    s.ft(s.i("a"), "y:200", "y:0", .4, 1.3); s.ft(s.i("b"), "y:-100", "y:0", .7, 1.3)
    s.ft(s.i("a"), "y:0", "y:-200", 3.3, .9, "power2.in"); s.ft(s.i("b"), "y:0", "y:-100", 3.3, .9, "power2.in")
    return h


def letters(s):
    h = ('<video id="%s-v" src="clip.mp4" muted playsinline data-start="%.3f" data-duration="5.5" data-track-index="2" style="position:absolute;inset:0;width:1920px;height:1080px;object-fit:cover"></video>'
         '<div class="abs" id="%s-m" style="inset:0;background:#000;mix-blend-mode:multiply;display:flex;align-items:center;justify-content:center"><div id="%s-x" style="font-weight:900;font-size:430px;letter-spacing:-.03em;color:#fff">MARE</div></div>') % (s.P, s.T, s.P, s.P)
    s.ft(s.i("x"), "scale:.82", "scale:1", .1, 5.2, "none")
    s.ft(s.i("m"), "opacity:1", "opacity:0", 4.2, 1.1, "HAND")
    return h


def bignum(s):
    h = '<div class="grid" style="inset:0"></div><div class="abs" id="%s-n" style="left:0;right:0;top:50px;text-align:center;font-weight:900;font-size:880px;line-height:1;color:rgba(94,230,168,.17)">3</div>' % s.P
    h += '<div class="abs" id="%s-w" style="left:0;right:0;top:450px;text-align:center;font-weight:800;font-size:130px">La comunicazione</div>' % s.P
    s.ft(s.i("n"), "opacity:0,scale:1.25", "opacity:1,scale:1", .3, 1.6); s.ft(s.i("w"), "opacity:0,y:50", "opacity:1,y:0", .8, 1.2)
    s.ft(s.i("n"), "scale:1", "scale:1.05", 1.9, 2.3, "none")
    return h


def mosaic(s):
    h = '<div class="grid" style="inset:0"></div><div class="ti">Cinque <em>passi</em></div>'
    rnd = random.Random(4)
    for r, (t, at) in enumerate((("01  L'idea", .9), ("02  Il capo", 2.2), ("03  La campagna", 3.5))):
        y = 300 + r * 190
        h += '<div class="abs" style="left:420px;top:%dpx;width:1080px;height:160px;border-radius:16px;overflow:hidden;background:#f4efe6"><div style="color:#0b0907;font-weight:800;font-size:76px;padding:36px 44px">%s</div>' % (y, t)
        for c in range(12):
            for q in range(2):
                i = "%s-m%d-%d-%d" % (s.P, r, c, q)
                h += '<div class="abs" id="%s" style="left:%dpx;top:%dpx;width:91px;height:81px;background:%s"></div>' % (i, c * 90, q * 80, rnd.choice(["#17613F", "#124E33", "#1f7a50"]))
                s.ft("#" + i, "opacity:1,scale:1", "opacity:0,scale:.4", at + rnd.random() * .45, .35, "power2.in")
        h += "</div>"
    return h


def spacing(s):
    word = "Il metodo"
    h = '<div class="grid" style="inset:0"></div><div class="abs" style="left:0;right:0;top:440px;text-align:center;font-weight:800;font-size:140px;white-space:pre">'
    for k, c in enumerate(word):
        h += '<span id="%s-c%d" style="display:inline-block">%s</span>' % (s.P, k, c)
        s.ft(s.i("c%d" % k), "x:%d,opacity:0" % ((k - (len(word) - 1) / 2) * 90), "x:0,opacity:1", .3, 1.9)
    return h + "</div>"


def ring(s):
    R = 230; C = 2 * math.pi * R
    h = ('<div class="grid" style="inset:0"></div><svg class="abs" style="left:660px;top:240px;width:600px;height:600px" viewBox="0 0 600 600"><circle cx="300" cy="300" r="%d" fill="none" stroke="rgba(244,239,230,.14)" stroke-width="26"/>'
         '<circle id="%s-r" cx="300" cy="300" r="%d" fill="none" stroke="#5EE6A8" stroke-width="26" stroke-linecap="round" stroke-dasharray="%.1f" stroke-dashoffset="%.1f" transform="rotate(-90 300 300)"/></svg>' % (R, s.P, R, C, C))
    h += '<div class="abs" style="left:660px;top:240px;width:600px;height:600px;font-weight:800;font-size:150px;text-align:center;line-height:600px">'
    def bez(x, x1=.54, x2=0):
        a, b = 0, 1
        for _ in range(40):
            t = (a + b) / 2; u = 1 - t
            X = 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3
            a, b = (t, b) if X < x else (a, t)
        u = 1 - t
        return 3 * u * t * t + t ** 3
    s.ft(s.i("r"), "strokeDashoffset:%.1f" % C, "strokeDashoffset:%.1f" % (C * .28), .5, 2.2)
    # the number follows the same curve as the ring: one span per value, shown by a set (seek-safe)
    first = {}
    for f in range(0, 67):
        first.setdefault(round(72 * bez(f / 66)), f)
    ks = sorted(first)
    for n, v in enumerate(ks):
        h += '<div class="abs" id="%s-n%d" style="inset:0;opacity:0">%d<span style="font-size:80px">%%</span></div>' % (s.P, v, v)
        s.set(s.i("n%d" % v), "opacity:0", 0)
        s.set(s.i("n%d" % v), "opacity:1", .5 + first[v] / 30 if n else 0)
        if n + 1 < len(ks):
            s.set(s.i("n%d" % v), "opacity:0", .5 + first[ks[n + 1]] / 30)
    h += "</div>"
    return h


def online(s):
    h = ('<div class="grid" style="inset:0"></div><svg class="abs" style="inset:0;width:1920px;height:1080px" viewBox="0 0 1920 1080">'
         '<path id="%s-p" d="M300 640 C 700 280, 1150 860, 1620 430" fill="none" stroke="#5EE6A8" stroke-width="6" stroke-linecap="round" pathLength="1000" stroke-dasharray="1000 1200" stroke-dashoffset="1100"/>'
         '<path id="%s-q" d="M300 620 C 700 260, 1150 840, 1620 410" fill="none"/>'
         '<text font-family="Inter" font-weight="800" font-size="62" fill="#e3c47f"><textPath id="%s-t" href="#%s-q" startOffset="0%%">metodo</textPath></text></svg>' % (s.P, s.P, s.P, s.P))
    h += card(110, 560, 280, 170, "", "Idea") + card(1520, 300, 300, 170, "", "Capo")
    s.ft(s.i("p"), "strokeDashoffset:1100", "strokeDashoffset:0", .5, 1.4, "HAND")
    s.ft(s.i("t"), "attr:{startOffset:'0%'}", "attr:{startOffset:'70%'}", 1.0, 2.2, "HAND")
    return h


def text3d(s):
    N = 26
    layers = "".join('<div class="abs" style="inset:0;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:300px;letter-spacing:-.02em;transform:translateZ(%dpx);color:%s">VIDEO 3</div>' % (-i * 3, "#e3c47f" if i == 0 else "#7a5f2a" if i < N - 1 else "#3a2c12") for i in range(N))
    h = '<div class="abs" style="inset:0;background:#070605;perspective:1500px"><div class="abs" id="%s-c" style="inset:0;transform-style:preserve-3d">%s</div></div>' % (s.P, layers)
    s.ft(s.i("c"), "rotationY:-48,rotationX:14,scale:.8", "rotationY:-12,rotationX:5,scale:1", .2, 3.6, "HAND")
    return h


te = Lab("testi")
te.seg("1 · Testo da un bordo invisibile", 4.6, edge)
te.seg("2 · Video dentro le lettere", 5.5, letters)
te.seg("3 · Numero enorme dietro, parola davanti", 4.4, bignum)
te.seg("4 · Testo nascosto col mosaico", 5.2, mosaic)
te.seg("5 · Spaziatura che si stringe", 3.6, spacing)
te.seg("6 · Numero dentro un anello", 4, ring)
te.seg("7 · Parola che viaggia su una linea", 4.2, online)
te.seg("8 · Scritta 3D con spessore", 4.4, text3d)
te.write()


# ---------------------------------------------------------------- ABBELLIMENTI
def lightreveal(s):
    h = '<div class="abs" id="%s-a" style="left:0;right:0;top:400px;text-align:center;font-weight:800;font-size:170px;white-space:nowrap">Il laboratorio</div>' % s.P
    h += '<div class="abs" id="%s-l" style="left:-140px;top:150px;width:140px;height:780px;background:linear-gradient(90deg,transparent,rgba(255,244,214,.95),transparent);filter:blur(16px)"></div>' % s.P
    s.ft(s.i("a"), "clipPath:'inset(0% 100% 0% 0%)'", "clipPath:'inset(0% 0% 0% 0%)'", .3, 1.5, "power2.inOut")
    s.ft(s.i("l"), "x:0,opacity:1", "x:2060,opacity:1", .3, 1.5, "power2.inOut")
    s.ft(s.i("a"), "clipPath:'inset(0% 0% 0% 0%)'", "clipPath:'inset(0% 0% 0% 100%)'", 2.9, 1.3, "power2.inOut")
    s.ft(s.i("l"), "x:0,opacity:1", "x:2060,opacity:1", 2.9, 1.3, "power2.inOut")
    return h


def inside(s):
    h = '<div class="grid" style="inset:0"></div><div class="abs" id="%s-a" style="left:0;top:0;width:1920px;height:1080px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:280px;color:#f4efe6;transform-origin:912px 560px">BRAND</div>' % s.P
    s.ft(s.i("a"), "scale:46", "scale:1", .5, 2.2, "HAND")
    return h


def cgrid(on):
    def f(s):
        if on:
            g = ('<div class="abs" style="inset:0;perspective:1100px"><div class="grid" id="%s-g" style="left:-1040px;top:-1000px;width:4000px;height:3000px;transform:rotateX(62deg);background-image:linear-gradient(rgba(120,235,180,.42) 2px, transparent 2px),linear-gradient(90deg,rgba(120,235,180,.42) 2px, transparent 2px);background-size:120px 120px;'
                 '-webkit-mask-image:radial-gradient(closest-side,#000 25%%,transparent 100%%);mask-image:radial-gradient(closest-side,#000 25%%,transparent 100%%)"></div></div>' % s.P)
            s.ft(s.i("g"), "rotationX:62,rotation:0", "rotationX:62,rotation:9", 0, 4.4, "none")
        else:
            g = '<div class="grid" style="inset:0"></div>'
        return g + '<div class="ti" style="top:420px;font-size:110px">Il <em>metodo</em></div>'
    return f


def lens(s):
    src = "img/ai-royal.jpg"
    h = '<img class="abs" src="%s" style="inset:0;width:1920px;height:1080px;object-fit:cover;filter:grayscale(1) brightness(.32)">' % src
    h += '<img class="abs" id="%s-i" src="%s" style="inset:0;width:1920px;height:1080px;object-fit:cover">' % (s.P, src)
    h += '<div class="abs" id="%s-r" style="left:0;top:0;width:520px;height:520px;margin:-260px 0 0 -260px;border-radius:50%%;border:4px solid #5EE6A8;box-shadow:0 0 40px rgba(94,230,168,.5)"></div>' % s.P
    pts = [(420, 400), (1000, 620), (1500, 420)]
    for k in range(2):
        a, b = pts[k], pts[k + 1]
        s.ft(s.i("i"), "clipPath:'circle(260px at %dpx %dpx)'" % a, "clipPath:'circle(260px at %dpx %dpx)'" % b, .6 + k * 2, 1.5)
        s.ft(s.i("r"), "x:%d,y:%d" % a, "x:%d,y:%d" % b, .6 + k * 2, 1.5)
    return h


def sweep(s):
    h = '<div class="grid" style="inset:0"></div><div class="card" style="left:560px;top:320px;width:800px;height:440px;background:#0d3626;color:#f4efe6;border:2px solid rgba(94,230,168,.35)"><div class="n" style="color:#5EE6A8">Pre-order</div><div class="l" style="font-size:64px">Il primo capo</div>'
    h += '<div class="abs" style="left:26px;bottom:30px;padding:18px 40px;border-radius:999px;background:#17613F;color:#f4efe6;font-weight:700;font-size:36px">Prenota</div>'
    h += '<div class="abs" id="%s-l" style="left:-400px;top:-120px;width:220px;height:700px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.55),transparent);transform:rotate(20deg)"></div></div>' % s.P
    s.ft(s.i("l"), "x:0,rotation:20", "x:1500,rotation:20", .7, 1.6, "power2.inOut")
    return h


def prox(s):
    pos = [(130 + 290 * k, 300 if k % 2 == 0 else 560) for k in range(6)]
    h = '<div class="grid" style="inset:0"></div><div class="ti">Da un concetto <em>all\'altro</em></div>'
    for k, (x, y) in enumerate(pos):
        h += card(x, y, 250, 200, "%02d" % (k + 1), ["Idea", "Capo", "Foto", "Sito", "Lancio", "Vendita"][k], s.i("c%d" % k)[1:])
    h += '<div class="abs" id="%s-d" style="left:0;top:0;width:34px;height:34px;margin:-17px;border-radius:50%%;background:#5EE6A8;box-shadow:0 0 34px #5EE6A8"></div>' % s.P
    D, step = 5.0, .1
    px = lambda t: 60 + (1860 - 60) * (t / D)
    py = lambda t: 540 + 40 * math.sin(t * 1.3)
    s.ft(s.i("d"), "x:60,y:540", "x:1860,y:540", 0, D, "none")
    for k, (x, y) in enumerate(pos):
        cx, cy = x + 125, y + 100
        def off(t):
            dx, dy = cx - px(t), cy - 540
            d = math.hypot(dx, dy)
            f = 46 * math.exp(-(d / 300) ** 2)
            return dx / max(d, 1) * f, dy / max(d, 1) * f
        for i in range(int(D / step)):
            a, b = off(i * step), off((i + 1) * step)
            if abs(a[0] - b[0]) + abs(a[1] - b[1]) < .05:
                continue
            s.js.append("tl.fromTo('%s',{x:%.2f,y:%.2f},{x:%.2f,y:%.2f,duration:%.2f,ease:'none',immediateRender:false},%.3f);" % (s.i("c%d" % k), a[0], a[1], b[0], b[1], step, s.T + i * step))
    return h


def border(s):
    h = '<div class="grid" style="inset:0"></div>'
    pos = [(200, 360), (760, 360), (1320, 360)]
    for k, (x, y) in enumerate(pos):
        h += ('<div class="abs" id="%s-b%d" style="left:%dpx;top:%dpx;width:400px;height:320px;border-radius:24px;padding:4px;background:radial-gradient(420px circle at var(--x) var(--y),#b9ffe0,#5EE6A8 30%%,rgba(94,230,168,.14) 100%%);box-shadow:0 20px 50px rgba(0,0,0,.4)">'
              '<div style="width:100%%;height:100%%;border-radius:21px;background:#0d3626;padding:26px;font-weight:700;font-size:46px">%s</div></div>') % (s.P, k, x, y, ["Tessuto", "Fit", "Prezzo"][k])
        s.ft(s.i("b%d" % k), "'--x':'%dpx','--y':'120px'" % (60 - x), "'--x':'%dpx','--y':'120px'" % (1860 - x), .2, 4.4, "none")
    h += '<div class="abs" id="%s-d" style="left:0;top:0;width:30px;height:30px;margin:-15px;border-radius:50%%;background:#f4efe6;box-shadow:0 0 40px 10px #5EE6A8"></div>' % s.P
    s.ft(s.i("d"), "x:60,y:480", "x:1860,y:480", .2, 4.4, "none")
    return h


FINISH = '<div class="abs" style="inset:0;z-index:50;background:radial-gradient(900px 500px at 50% 42%,rgba(255,240,200,.13),transparent 70%),radial-gradient(closest-side at 50% 50%,transparent 62%,rgba(0,0,0,.4) 120%);"></div>'


def finish(on):
    def f(s):
        return '<div class="grid" style="inset:0"></div><div class="pg">%s</div>%s' % (pageB(), FINISH if on else "")
    return f


def pieces(ease, glow=None):
    def f(s):
        rnd = random.Random(7)
        cols, rows, W, H = 8, 5, 130, 130
        x0, y0 = 960 - cols * W / 2, 540 - rows * H / 2
        inner = ""
        sc = "x:0,y:0,z:0,rotationX:0,rotationY:0,opacity:1"
        for r in range(rows):
            for c in range(cols):
                i = "%s-k%d-%d" % (s.P, r, c)
                inner += ('<div class="abs" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:url(img/tile.jpg) %dpx %dpx / %dpx %dpx"></div>' % (i, x0 + c * W, y0 + r * H, W + 1, H + 1, -c * W, -r * H, cols * W, rows * H))
                a = "x:%d,y:%d,z:%d,rotationX:%d,rotationY:%d,opacity:0" % (rnd.uniform(-900, 900), rnd.uniform(-600, 600), rnd.uniform(-900, 300), rnd.uniform(-160, 160), rnd.uniform(-160, 160))
                s.ft("#" + i, a, sc, .3 + rnd.random() * .5, 2.0, ease)
        h = '<div class="grid" style="inset:0"></div>'
        if glow:
            h += '<div class="abs" id="%s-g" style="inset:0;background:radial-gradient(760px 560px at 50% 50%%,rgba(227,196,127,.75),transparent 72%%)"></div>'.replace("50% 50%%", "50%% 50%%") % s.P
            if glow == "evento":
                s.ft(s.i("g"), "opacity:0,scale:.8", "opacity:1,scale:1.12", 2.5, .55, "power2.out")
                s.ft(s.i("g"), "opacity:1,scale:1.12", "opacity:.3,scale:1.05", 3.05, 1.2, "power2.inOut")
            else:
                s.set(s.i("g"), "opacity:.5")
        return h + '<div class="abs" style="inset:0;perspective:1400px"><div class="abs" style="inset:0;transform-style:preserve-3d">%s</div></div>' % inner
    return f


def cyl(s):
    h = '<div class="grid" style="inset:0"></div><div class="ti">Forme <em>finte 3D</em></div>'
    h += '<div class="abs" style="left:300px;top:880px;width:1320px;height:60px;border-radius:50%;background:radial-gradient(closest-side,rgba(0,0,0,.55),transparent)"></div>'
    for k, (x, hh, col, top) in enumerate(((430, 280, "#17613F,#2fb37a 45%,#0e3f29", "#5EE6A8"), (800, 430, "#8a6a2c,#e3c47f 45%,#5d4518", "#f1dfae"), (1170, 590, "#b8b0a0,#f4efe6 45%,#8f8878", "#fffaf0"))):
        h += ('<div class="abs" id="%s-c%d" style="left:%dpx;top:900px;width:320px;height:0;transform-origin:50%% 100%%"><div class="abs" style="left:0;bottom:-40px;width:320px;height:%dpx;background:linear-gradient(90deg,%s);border-radius:160px/40px"></div>'
              '<div class="abs" style="left:0;bottom:%dpx;width:320px;height:80px;border-radius:50%%;background:%s"></div></div>') % (s.P, k, x, hh + 40, col, hh - 40, top)
        s.ft(s.i("c%d" % k), "scaleY:0,opacity:0", "scaleY:1,opacity:1", .4 + k * .3, 1.5)
    return h


def shapetr(s):
    h = '<div class="grid" style="inset:0"></div>'
    pgs = [pageA(), pageB(), pageA()]
    for k in range(3):
        h += '<div class="pg" id="%s-p%d">%s</div>' % (s.P, k, pgs[k])
    h += '<div class="abs" id="%s-s" style="left:960px;top:540px;width:200px;height:200px;margin:-100px;background:#5EE6A8;border-radius:50%%"></div>' % s.P
    s.set(s.i("p1"), "opacity:0"); s.set(s.i("p2"), "opacity:0")
    for k, at in enumerate((1.0, 3.2)):
        s.ft(s.i("s"), "scale:0", "scale:13", at, .55, "power3.in")
        s.ft(s.i("s"), "scale:13,opacity:1", "scale:13,opacity:0", at + .55, .5, "power2.out")
        s.set(s.i("p%d" % k), "opacity:0", at + .55); s.set(s.i("p%d" % (k + 1)), "opacity:1", at + .55)
        s.set(s.i("s"), "scale:0,opacity:1", at + 1.1)
    return h


def turb(s):
    h = ('<svg class="abs" width="0" height="0"><filter id="%s-f" x="-10%%" y="-10%%" width="120%%" height="120%%"><feTurbulence type="fractalNoise" baseFrequency=".006 .014" numOctaves="2" seed="4"/>'
         '<feDisplacementMap id="%s-m" in="SourceGraphic" scale="0" xChannelSelector="R" yChannelSelector="G"/></filter></svg>') % (s.P, s.P)
    h += '<div class="abs" style="inset:0;filter:url(#%s-f)"><div class="grid" style="inset:0"></div><div class="pg" id="%s-a">%s</div><div class="pg" id="%s-b">%s</div></div>' % (s.P, s.P, pageA(), s.P, pageB())
    s.set(s.i("b"), "opacity:0")
    s.ft(s.i("m"), "attr:{scale:0}", "attr:{scale:420}", .8, .6, "power2.in")
    s.ft(s.i("m"), "attr:{scale:420}", "attr:{scale:0}", 1.4, .8, "power2.out")
    s.ft(s.i("a"), "opacity:1", "opacity:0", 1.25, .3, "none"); s.ft(s.i("b"), "opacity:0", "opacity:1", 1.25, .3, "none")
    return h


ab = Lab("abb")
ab.seg("1 · La luce scopre il titolo e lo porta via", 4.4, lightreveal)
ab.seg("2 · Camera dentro la scritta che arretra", 3.6, inside)
ab.seg("3 · Griglia intera (oggi)", 3, cgrid(False))
ab.seg("4 · Griglia circolare inclinata", 4.4, cgrid(True))
ab.seg("5 · Maschera a lente", 4.6, lens)
ab.seg("6 · Light sweep su una card", 3, sweep)
ab.seg("7 · Prossimità: un punto attraversa la plate", 5, prox)
ab.seg("8 · Il bordo segue la luce", 4.8, border)
ab.seg("9 · Plate senza strato finale", 2.5, finish(False))
ab.seg("10 · Bagliore e vignettatura sopra", 2.5, finish(True))
ab.seg("11 · Pezzi che si compongono (curva D)", 4.2, pieces("HAND"))
ab.seg("12 · Stessi pezzi, picco in ritardo", 4.2, pieces("LATE"))
ab.seg("13 · Bagliore fisso", 4.2, pieces("LATE", "fisso"))
ab.seg("14 · La luce arriva con i pezzi", 4.4, pieces("LATE", "evento"))
ab.seg("15 · Forme finte 3D", 3.6, cyl)
ab.seg("16 · Transizione con una forma ripetuta", 5, shapetr)
ab.seg("17 · Onda di turbolenza", 3.4, turb)
ab.write()


# ---------------------------------------------------------------- 30 / 60 fps e sfocatura di movimento: la stessa mossa, due volte
for nm, attrs, lab in (("sw", "", "30 fps"), ("swmb", ' data-motion-blur="on" data-motion-blur-shutter="180"', "Sfocatura di movimento")):
    L = Lab(nm)
    L.seg("Swipe curva D · " + lab, 3.6, swipe("grid"))
    L.seg("Stesso swipe, più lento da vicino · " + lab, 3.6, swipe("grid", d=1.3, vert=True))
    L.write(root_attrs=attrs)
