"""scene.py: a toolkit to IMPROVISE a motion plate, not a format to pick from a catalogue (Jacopo, 01/11/2026: "una volta che hai capito lo stile di Joseph improvvisa: ogni volta che devi
spiegare qualcosa, bam, una motion che spiega bene, dinamica, mai ferma. Possono essere 100.000 diversi, l'importante è che mantengano questi canoni").

The canon (teardown of Joseph's video, personale/youtube/inspo-motion-plates-joseph.md): a full-frame scene on the green grid, the title top-left with ONE key word in the italic serif gold, every element lands
ON the word that names it (card / pill / disc / photo, then the dashed line that connects it), things you do not need are struck through, the camera never stands still (plates_base.wrap: slow push-in; a run of plates glides on board.py, no kicks
since 04/11/2026), a smooth swish on everything that appears, and the plate is full screen with no face PiP (since 04/11/2026, taste.md 9e).

    from scene import Scene
    s = Scene("p1", t_in=27.7, t_out=37.4, title="Carta *bianca*")
    page = s.photo(150, 330, 400, 520, "img/pres/p01.jpg", t=28.3)                  # returns an id; boxes are remembered
    cl   = s.disc(940, 520, t=28.96, logo="img/logos/claude.svg", label="Claude")
    s.link(page, cl, t=29.1)                                                         # dashed connector that draws itself, then marches until the plate ends
    mh   = s.pill(1250, 580, "Mano umana", t=35.28)
    s.strike(mh, t=36.16)                                                            # red line + dim: what you no longer need
    out = s.build()                                                                  # {"html","js"} for compose.py raw_html / raw_js

Elements: pill(x,y,label,t,w,h,logo,img,kind in card|mint|bad), disc(cx,cy,t,logo|text,label,r), photo(x,y,w,h,src,t,rot,caption), chip = small pill, text(x,y,html,t,size,color),
bigtext (a key number / word in the serif gold), link(a,b,t,mode h|v), strike(id,t), tick(id,t), glow(id,t), shift(id,t,dx,dy), tint(id,t,kind). Every tween is a fromTo with explicit values (seek-safe).
"""
from plates_base import *

CSS = """
  .sc-e { position:absolute; opacity:0; }
  .sc-p { border-radius:20px; background:rgba(244,239,230,.95); color:#0b0907; font-family:var(--k-font); font-weight:700; display:flex; align-items:center; justify-content:center; gap:16px;
          white-space:nowrap; box-shadow:0 22px 44px rgba(0,0,0,.45); box-sizing:border-box; padding:0 22px; }
  .sc-p img.lg { height:46px; width:46px; object-fit:contain; flex:none; }
  .sc-p img.th { height:100%; width:auto; border-radius:14px; margin-left:-22px; flex:none; }
  .sc-p.mint { background:rgba(11,9,7,.55); color:var(--k-text); box-shadow:0 0 0 3px var(--k-accent2), 0 0 34px rgba(94,230,168,.35); font-weight:600; }
  .sc-p.bad { color:#8a2a24; }
  .sc-p i { font-family:var(--k-serif); font-style:italic; font-weight:500; }
  .sc-d { border-radius:50%; display:flex; align-items:center; justify-content:center; box-sizing:border-box;
          background:radial-gradient(circle at 38% 32%, #ffffff, #f4efe6 70%, #e2d9c6); border:6px solid var(--k-accent); box-shadow:0 0 90px color-mix(in srgb, var(--k-accent) 45%, transparent), 0 30px 60px rgba(0,0,0,.5); }
  .sc-d img { width:62%; height:62%; object-fit:contain; }
  .sc-d b { font-family:var(--k-serif); font-style:italic; font-weight:500; color:#2a1d05; }
  .sc-dl { text-align:center; font-family:var(--k-font); font-weight:700; font-size:34px; color:var(--k-text); }
  .sc-ph { background:rgba(244,239,230,.96); border-radius:18px; padding:12px; box-shadow:0 30px 60px rgba(0,0,0,.5); box-sizing:border-box; }
  .sc-ph img { width:100%; display:block; border-radius:8px; object-fit:cover; }
  .sc-ph span { display:block; font-family:var(--k-font); font-weight:800; font-size:30px; color:#0b0907; padding:10px 6px 2px; letter-spacing:-.01em; }
  .sc-tx { font-family:var(--k-font); font-weight:800; color:var(--k-text); letter-spacing:-.02em; white-space:nowrap; }
  .sc-tx i, .sc-big i { font-family:var(--k-serif); font-style:italic; font-weight:500; color:var(--k-accent); letter-spacing:0; }
  .sc-big { font-family:var(--k-serif); font-style:italic; font-weight:500; color:var(--k-accent); line-height:1; white-space:nowrap; }
  .sc-x { height:5px; border-radius:3px; background:#e0645c; transform-origin:0 50%; box-shadow:0 0 16px rgba(224,100,92,.6); }
  .sc-lk { left:0; top:0; width:1920px; height:1080px; }
  .sc-svg { position:absolute; inset:0; width:1920px; height:1080px; overflow:visible; }
  .sc-svg path { fill:none; stroke:var(--k-accent2); stroke-width:4; stroke-linecap:round; stroke-dasharray:3 12; }
"""
BAD = "#e0645c"
CHECK = '<svg viewBox="0 0 36 36"><path d="M10 18.5 L16 24.5 L26.5 12.5" fill="none" stroke="#06140d" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


class Scene:
    def __init__(self, cid, t_in, t_out, title=None, title_t=None, sub=None, track=3, track_audio=20, fade_in=0.3, fade_out=0.3, bg=True, sound=True):
        self.cid, self.t_in, self.t_out = cid, t_in, t_out
        self.track, self.track_audio, self.fade_in, self.fade_out, self.bg, self.sound = track, track_audio, fade_in, fade_out, bg, sound
        self.html, self.js, self.events, self.box, self.when, self.n = [], [], [], {}, {}, 0
        self.pre_title = ""
        if title:
            self.html.append('<div class="sc-e sc-tx" id="%s-T" style="left:110px;top:100px;font-size:96px;line-height:1.05">%s</div>' % (cid, keyword(title).replace("pl-key", "pl-key")))
            tt = t_in + 0.15 if title_t is None else title_t
            self.js.append("tl.set('#%s-T', { opacity:0, y:14 }, 0);" % cid)
            self.js.append(fromto("#%s-T" % cid, "{opacity:0,y:14}", "{opacity:1,y:0}", tt, 0.45))
        if sub:
            self.html.append('<div class="sc-e pl-sub" id="%s-S" style="left:112px;top:226px;font-size:34px">%s</div>' % (cid, keyword(sub)))
            self.js.append("tl.set('#%s-S', { opacity:0, y:10 }, 0);" % cid)
            self.js.append(fromto("#%s-S" % cid, "{opacity:0,y:10}", "{opacity:1,y:0}", t_in + 0.35, 0.45))

    # ---- helpers
    def _id(self, k):
        self.n += 1
        return "%s-%s%d" % (self.cid, k, self.n)

    def _appear(self, i, t, dx=0, dy=36, blur=8, d=0.5, rest=1.0, ease=EASE):
        self.js.append("tl.set('#%s', { opacity:0, x:%d, y:%d, filter:'blur(%dpx)' }, 0);" % (i, dx, dy, blur))
        self.js.append(fromto("#" + i, "{opacity:0,x:%d,y:%d,filter:'blur(%dpx)'}" % (dx, dy, blur), "{opacity:%s,x:0,y:0,filter:'blur(0px)'}" % rest, t - 0.05, d, ease))
        self.events.append(t)

    def _box(self, i, x, y, w, h, what, t=None):
        check_pip(x, y, w, h, what)
        self.box[i] = (x, y, w, h)
        if t is not None:
            self.when[i] = t

    # ---- elements
    def pill(self, x, y, label, t, anchor="", w=None, h=76, kind="card", logo=None, img=None, size=32, dx=0, dy=36):
        """label may contain *word* for the serif gold key (or the serif ink on ivory)."""
        w = w or int(len(label.replace("*", "")) * size * 0.56 + 90 + (60 if logo else 0) + (h - 14 if img else 0))
        i = self._id("p")
        inner = ('<img class="lg" src="%s" alt="">' % esc(logo) if logo else "") + ('<img class="th" src="%s" alt="">' % esc(img) if img else "") + keyword(label).replace('class="pl-key"', "")
        self.html.append('<div class="sc-e sc-p %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;font-size:%dpx"%s>%s</div>' % (kind if kind != "card" else "", i, x, y, w, h, size, at_attrs(t, anchor), inner))
        self._box(i, x, y, w, h, "pill " + label, t)
        self._appear(i, t, dx, dy)
        return i

    def disc(self, cx, cy, t, anchor="", logo=None, text=None, label=None, r=100, size=None):
        i = self._id("d")
        face = '<img src="%s" alt="">' % esc(logo) if logo else '<b style="font-size:%dpx">%s</b>' % (size or int(r * 0.95), esc(text or ""))
        self.html.append('<div class="sc-e sc-d" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"%s>%s</div>' % (i, cx - r, cy - r, 2 * r, 2 * r, at_attrs(t, anchor), face))
        self._box(i, cx - r, cy - r, 2 * r, 2 * r, "disc", t)
        self.js.append("tl.set('#%s', { opacity:0, scale:0.7 }, 0);" % i)
        self.js.append(fromto("#" + i, "{opacity:0,scale:0.7}", "{opacity:1,scale:1}", t - 0.1, 0.6, "power2.out"))
        self.js.append("tl.fromTo('#%s', { y:0 }, { y:-8, duration:%.3f, ease:'sine.inOut', immediateRender:false }, %.3f);" % (i, max(self.t_out - t - 0.6, 1.0), t + 0.6))   # alive: a slow breath
        self.events.append(t)
        if label:
            li = i + "l"
            self.html.append('<div class="sc-e sc-dl" id="%s" style="left:%dpx;top:%dpx;width:%dpx">%s</div>' % (li, cx - 150, cy + r + 12, 300, esc(label)))
            self.js.append("tl.set('#%s', { opacity:0, y:10 }, 0);" % li)
            self.js.append(fromto("#" + li, "{opacity:0,y:10}", "{opacity:1,y:0}", t + 0.1, 0.45))
        return i

    def photo(self, x, y, w, h, src, t, anchor="", rot=0, caption=None, dx=0, dy=40):
        """A real image on an ivory card; h is the whole card (the caption sits under the image). The image is cropped to fit (object-fit: cover)."""
        i = self._id("f")
        ih = h - 24 - (62 if caption else 0)
        cap = "<span>%s</span>" % esc(caption) if caption else ""
        self.html.append('<div class="sc-e sc-ph" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;transform:rotate(%sdeg)"%s><img src="%s" style="height:%dpx" alt="">%s</div>' % (i, x, y, w, h, rot, at_attrs(t, anchor), esc(src), ih, cap))
        self._box(i, x, y, w, h, "photo", t)
        self._appear(i, t, dx, dy)
        return i

    def text(self, x, y, html, t, anchor="", size=60, color=None, dy=14):
        i = self._id("t")
        st = "left:%dpx;top:%dpx;font-size:%dpx" % (x, y, size) + (";color:%s" % color if color else "")
        self.html.append('<div class="sc-e sc-tx" id="%s" style="%s"%s>%s</div>' % (i, st, at_attrs(t, anchor), keyword(html).replace('class="pl-key"', "")))
        self._appear(i, t, 0, dy, 4, 0.45)
        return i

    def big(self, x, y, html, t, anchor="", size=260):
        i = self._id("b")
        self.html.append('<div class="sc-e sc-big" id="%s" style="left:%dpx;top:%dpx;font-size:%dpx"%s>%s</div>' % (i, x, y, size, at_attrs(t, anchor), esc(html)))
        self.js.append("tl.set('#%s', { opacity:0, scale:0.6, transformOrigin:'0 100%%' }, 0);" % i)
        self.js.append(fromto("#" + i, "{opacity:0,scale:0.6}", "{opacity:1,scale:1}", t - 0.05, 0.7, "back.out(1.6)"))
        self.events.append(t)
        return i

    def link(self, a, b, t, mode="h", d=0.55):
        """A dashed connector from element a to element b (their facing edges), drawn left to right / top to bottom, then marching until the plate ends."""
        ax, ay, aw, ah = self.box[a]
        bx, by, bw, bh = self.box[b]
        if mode == "h":
            x1, y1, x2, y2 = (ax + aw, ay + ah / 2, bx, by + bh / 2) if bx >= ax + aw else (ax, ay + ah / 2, bx + bw, by + bh / 2)
            c = abs(x2 - x1) * 0.45 * (1 if x2 >= x1 else -1)
            p = "M%d %d C %d %d, %d %d, %d %d" % (x1, y1, x1 + c, y1, x2 - c, y2, x2, y2)
        else:
            x1, y1, x2, y2 = (ax + aw / 2, ay + ah, bx + bw / 2, by) if by >= ay + ah else (ax + aw / 2, ay, bx + bw / 2, by + bh)
            c = abs(y2 - y1) * 0.45 * (1 if y2 >= y1 else -1)
            p = "M%d %d C %d %d, %d %d, %d %d" % (x1, y1, x1, y1 + c, x2, y2 - c, x2, y2)
        t = max(t, (self.when.get(a) or 0) + 0.05, (self.when.get(b) or 0) + 0.05)   # RULE (Jacopo, 01/11/2026): a dashed line never shows before the two things it joins; 04/11: it draws WITH the card that lands, not after it
        i = self._id("l")
        self.html.append('<div class="sc-e sc-lk" id="%s"><svg class="sc-svg"><path d="%s"/></svg></div>' % (i, p))
        # the reveal runs over the line's own span, not the whole 1920 frame (04/11: over the frame the line stayed hidden, then popped in late)
        if mode == "h":
            clip0, clip1 = (("inset(-20px %dpx -20px 0px)" % (1920 - x1), "inset(-20px %dpx -20px 0px)" % (1920 - x2)) if x2 >= x1 else ("inset(-20px 0px -20px %dpx)" % x1, "inset(-20px 0px -20px %dpx)" % x2))
        else:
            clip0, clip1 = (("inset(0px -20px %dpx -20px)" % (1080 - y1), "inset(0px -20px %dpx -20px)" % (1080 - y2)) if y2 >= y1 else ("inset(%dpx -20px 0px -20px)" % y1, "inset(%dpx -20px 0px -20px)" % y2))
        self.js.append("tl.set('#%s', { opacity:0, clipPath:'%s' }, 0);" % (i, clip0))
        self.js.append("tl.set('#%s', { opacity:1 }, %.3f);" % (i, t))
        self.js.append(fromto("#" + i, "{clipPath:'%s'}" % clip0, "{clipPath:'%s'}" % clip1, t, d, "sine.inOut"))
        run = t + d + 0.1
        self.js.append("tl.set('#%s path', { strokeDashoffset:0 }, 0);" % i)
        self.js.append("tl.fromTo('#%s path', { strokeDashoffset:0 }, { strokeDashoffset:%d, duration:%.3f, ease:'none', immediateRender:false }, %.3f);" % (i, -int(45 * max(self.t_out - run, 1.0)), max(self.t_out - run, 1.0), run))
        return i

    def strike(self, i, t):
        x, y, w, h = self.box[i]
        k = self._id("x")
        self.html.append('<div class="sc-e sc-x" id="%s" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (k, x + 14, y + h // 2 - 2, w - 28))
        self.js.append("tl.set('#%s', { opacity:1, scaleX:0 }, 0);" % k)
        self.js.append(fromto("#" + k, "{scaleX:0}", "{scaleX:1}", t, 0.35, "power2.inOut"))
        self.js.append(fromto("#" + i, "{opacity:1}", "{opacity:0.4}", t + 0.2, 0.4, "power2.inOut"))
        self.events.append(t)

    def tick(self, i, t):
        x, y, w, h = self.box[i]
        k = self._id("k")
        self.html.append('<span class="sc-e pl-ck" id="%s" style="left:%dpx;top:%dpx">%s</span>' % (k, x + w - 22, y - 16, CHECK))
        self.js.append("tl.set('#%s', { opacity:0, scale:0.5 }, 0);" % k)
        self.js.append(fromto("#" + k, "{opacity:0,scale:0.5}", "{opacity:1,scale:1}", t, 0.3, "power2.out"))
        self.events.append(t)

    def glow(self, i, t, color="94,230,168"):
        self.js.append(fromto("#" + i, "{boxShadow:'0 22px 44px rgba(0,0,0,.45)'}", "{boxShadow:'0 0 0 4px rgba(%s,1), 0 0 44px rgba(%s,.55), 0 36px 70px rgba(0,0,0,.55)'}" % (color, color), t, 0.45))
        self.events.append(t)

    def shift(self, i, t, dx=0, dy=0, d=0.6, frm=(0, 0)):
        """Move an element from offset frm to (dx, dy) (absolute offsets from its place), e.g. two titles swapping."""
        self.js.append(fromto("#" + i, "{x:%d,y:%d}" % frm, "{x:%d,y:%d}" % (dx, dy), t, d, "power2.inOut"))
        self.events.append(t)

    def parts(self):
        """For board.py: the plate's raw content, with no host, camera or sound of its own."""
        return "\n".join(self.html), list(self.js)

    def build(self):
        inner = "\n".join(self.html)
        h, pre, post = wrap(self.cid, self.t_in, self.t_out, CSS + BASE_CSS, inner, bg=self.bg, track=self.track, fade_in=self.fade_in, fade_out=self.fade_out,
                            kicks=self.events, sound=self.sound, track_audio=self.track_audio)
        return {"html": h, "js": "\n        ".join(pre + self.js + post)}
