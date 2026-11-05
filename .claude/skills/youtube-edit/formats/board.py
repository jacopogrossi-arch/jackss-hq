"""board.py: the digital whiteboard (Jacopo, 04/11/2026). A run of plates is ONE big board: the pages sit side by side on a single grid, and all the movement is a fluid camera on it.

"La dinamicità non si dà col rimbalzo, si dà con movimenti di camera fluidi", "come se fosse una grande lavagna digitale e ti spostassi in una parte vuota". So there are no zoom kicks and no fades:
    - face -> board: the board pushes the face out of frame in one eased swipe; board -> face is the same swipe going on;
    - page -> page: the camera swipes across the board to an empty part, the old page stays where it was;
    - inside a page the camera glides to what is being named (auto from the Scene's boxes and times, or `cam=` by hand), then pulls back to show the whole page.

    b = Board("a", track=10, track_audio=300)
    b.page(scene1, at=(0, 0), a=77.3, b=88.2)                         # a Scene written as usual; its own wrap() is not used
    b.page(scene2, at=(1, 0), a=88.2, b=92.9)
    b.page(None, at=(1, 0), a=98.6, b=101.5, cam=[(99.75, 300, 460, 1.7, 1.0)])   # back to a page already on the board
    out = b.build()                                                    # {"html","js"}; the run lasts from the first page's a to the last page's b
cam: [(t, x, y, scale, duration)] in page coordinates. Every tween is a fromTo with explicit values (seek-safe).
"""
from plates_base import SOUNDS, POOL, plan_sfx, BASE_CSS
from scene import CSS as SCENE_CSS

PITCH = (2500, 1500)         # distance between pages on the board: the camera always crosses empty grid
PUSH = 0.9                   # face <-> board swipe, seconds
SWIPE = 1.3                  # page -> page swipe, seconds: the course curve at 1.3 s (curve D, chosen by Jacopo 04/11; 1.6 s was too slow, and at 1.0 s it jumps at 30 fps)
SWIPE_EASE = "window.__hand" # cubic-bezier(.54,0,0,1), a JS function: fast early, long soft landing
SWIPE_PEAK = 0.3             # where the curve is fastest, as a share of the swipe: the sound sits there
SWIPE_LEAD = 0.05 + SWIPE_PEAK * SWIPE   # the peak falls 0.05 s before the page's time, where the old swipe had it
PUSH_EASE = "power3.inOut"   # face <-> board: slow start, fast middle, soft landing
GLIDE_EASE = "window.__c40"  # camera glides inside a page: cubic-bezier(.5,0,.3,1), speed peak near 40% (course L8, Jacopo's yes 05/11; the 40% was read by eye, not measured)
HAND_JS = ("window.__hand = window.__hand || function (x) { if (x <= 0) return 0; if (x >= 1) return 1; var a = 0, b = 1, t = x, k, u, X;"
           " for (k = 0; k < 40; k++) { t = (a + b) / 2; u = 1 - t; X = 3 * u * u * t * .54 + 3 * u * t * t * 0 + t * t * t; if (X < x) a = t; else b = t; }"
           " u = 1 - t; return 3 * u * t * t + t * t * t; };"   # cubic-bezier(.54,0,0,1): y1 is 0 and y2 is 1, solved by bisection so every frame gives the same value
           " window.__c40 = window.__c40 || function (x) { if (x <= 0) return 0; if (x >= 1) return 1; var a = 0, b = 1, t = x, k, u, X;"
           " for (k = 0; k < 40; k++) { t = (a + b) / 2; u = 1 - t; X = 3 * u * u * t * .5 + 3 * u * t * t * .3 + t * t * t; if (X < x) a = t; else b = t; }"
           " u = 1 - t; return 3 * u * t * t + t * t * t; };")
GRID_DEPTH = 0.5             # the grid sits behind the pages and travels half as far as they do (course fake 3D, Jacopo's yes 05/11: "un dettaglio che conta"); 1 = glued to the pages
FINISH = ('<div class="bd-fin" style="position:absolute;inset:0;z-index:50;pointer-events:none;background:radial-gradient(900px 500px at 50% 42%,rgba(255,240,200,.13),transparent 70%),'
          'radial-gradient(closest-side at 50% 50%,transparent 62%,rgba(0,0,0,.4) 120%)"></div>')   # glow and vignette over the plate (course, Jacopo's yes 05/11); it stays still while the camera moves
DRIFT = 0.006                # between two moves the camera keeps pushing in, per second
GROUP = 0.8                  # elements landing closer than this share one framing
CSS = """
  .bd-bg { position:absolute; inset:0; background:
      radial-gradient(1100px 700px at 50% 112%, color-mix(in srgb, var(--k-glow) var(--k-glow-a), transparent), transparent 70%),
      radial-gradient(900px 600px at 10% 0%, color-mix(in srgb, var(--k-glow2) var(--k-glow2-a), transparent), transparent 70%), var(--k-bg); }
  .bd-grid { position:absolute; background:
      linear-gradient(rgba(var(--k-grid-rgb), var(--k-grid-a)) 1px, transparent 1px),
      linear-gradient(90deg, rgba(var(--k-grid-rgb), var(--k-grid-a)) 1px, transparent 1px);
      background-size:var(--k-grid-size) var(--k-grid-size); }
  .bd-w { position:absolute; left:0; top:0; width:1920px; height:1080px; transform-origin:0 0; }
  .bd-p { position:absolute; width:1920px; height:1080px; font-family:var(--k-font); color:var(--k-text); }
"""


def _focus(box):
    x, y, w, h = box
    s = max(1.12, min(1.5, 1250.0 / max(w, 1), 700.0 / max(h, 1)))
    cy = 540 + (y + h / 2 - 540) * 0.75
    top = cy - 540 / s
    if 90 < top < 225:      # the frame's top edge would slice the page title: frame it clear of the title
        cy += 225 - top
    return (960 + (x + w / 2 - 960) * 0.75, cy, s)


def _groups(scene):
    items = sorted(((t, scene.box[i]) for i, t in scene.when.items() if t is not None and i in scene.box), key=lambda e: e[0])
    out = []
    for t, b in items:
        if out and t - out[-1][0] < GROUP:
            x, y, w, h = out[-1][1]
            X, Y = min(x, b[0]), min(y, b[1])
            out[-1] = (out[-1][0], (X, Y, max(x + w, b[0] + b[2]) - X, max(y + h, b[1] + b[3]) - Y))
        else:
            out.append((t, b))
    return out


class Board:
    def __init__(self, cid, track=10, track_audio=300, enter=True, leave=True, depth=GRID_DEPTH, finish=True):
        self.cid, self.track, self.ta, self.enter, self.leave, self.pages, self.holes, self.depth, self.finish = cid, track, track_audio, enter, leave, [], [], depth, finish

    def away(self, t0, t1):
        """The face comes back between t0 and t1 (a long stretch with nothing new on the board): the same swipe out and in."""
        self.holes.append((t0, t1))

    def page(self, scene, at, a, b, cam=None, overview=True):
        self.pages.append(dict(scene=scene, ox=at[0] * PITCH[0], oy=at[1] * PITCH[1], a=a, b=b, cam=cam, overview=overview))

    def _moves(self):
        moves = []   # (start, duration, (board x, board y, scale), ease)
        for n, p in enumerate(self.pages):
            ox, oy = p["ox"], p["oy"]
            end = p["b"] - (SWIPE_LEAD + 0.06 if n + 1 < len(self.pages) else 0.45 * PUSH)
            if n:
                moves.append((p["a"] - SWIPE_LEAD, SWIPE, (ox + 960, oy + 540, 1.0), SWIPE_EASE))
            free = moves[-1][0] + moves[-1][1] if moves else p["a"] + 0.45 * PUSH
            if p["cam"]:
                todo = [(t - 0.45, (x, y, s), d) for t, x, y, s, d in p["cam"]]
            else:
                gs = _groups(p["scene"]) if p["scene"] else []
                todo = []
                for k, (t, b) in enumerate(gs):
                    nxt = gs[k + 1][0] if k + 1 < len(gs) else end
                    f = _focus(b)
                    todo.append((t - 0.45, f, max(0.7, min(1.4, nxt - t))))
                    if nxt - t > 2.8:   # a long wait between two elements: the camera eases slowly back instead of standing still
                        todo.append((t + 1.0, (f[0] + (960 - f[0]) * 0.5, f[1] + (540 - f[1]) * 0.5, max(1.0, f[2] * 0.86)), nxt - t - 1.6))
            for t0, (x, y, s), d in todo:
                t0 = max(t0, free)
                d = min(d, end - t0)
                if d < 0.5:
                    continue
                moves.append((t0, d, (ox + x, oy + y, s), GLIDE_EASE))
                free = t0 + d
            if p["overview"] and not p["cam"] and end - free >= 1.2:   # the page pulls back and shows itself whole
                t0 = max(free, end - 1.5)
                moves.append((t0, end - t0, (ox + 960, oy + 540, 1.0), GLIDE_EASE))
        return moves

    def build(self):
        cid, P = self.cid, self.pages
        t_in, t_out = P[0]["a"], P[-1]["b"]
        h0, h1 = t_in - 0.5 * PUSH, t_out + 0.5 * PUSH
        W, G, R = "#%s-w" % cid, "#%s-g" % cid, "#%s-root" % cid
        tf = lambda c: "x:%.1f,y:%.1f,scale:%.4f" % (960 - c[2] * c[0], 540 - c[2] * c[1], c[2])
        c0 = (P[0]["ox"] + 960, P[0]["oy"] + 540)
        tg = lambda c: tf((c0[0] + self.depth * (c[0] - c0[0]), c0[1] + self.depth * (c[1] - c0[1]), c[2]))   # the grid layer: same zoom, a share of the travel
        js, inner, snd = [HAND_JS], [], []
        xs, ys = [p["ox"] for p in P], [p["oy"] for p in P]
        grid = '<div class="bd-grid" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>' % (min(xs) - 2400, min(ys) - 2400, max(xs) - min(xs) + 6720, max(ys) - min(ys) + 5840)
        n_snd = 0
        for p in P:
            if p["scene"] is None:
                continue
            h, j = p["scene"].parts()
            inner.append('<div class="bd-p" style="left:%dpx;top:%dpx">%s</div>' % (p["ox"], p["oy"], h))
            js += j
            for t in plan_sfx(p["scene"].events, p["a"] - 0.45, p["b"] + 0.4):
                nm = POOL[n_snd % len(POOL)]
                snd.append('<audio id="sfx-%s-e%d" src="sfx/%s.mp3" data-start="%.3f" data-duration="%.2f" data-track-index="%d" data-volume="1"></audio>'
                           % (cid, n_snd, nm, max(t - SOUNDS[nm][3], 0), SOUNDS[nm][2], self.ta + 10 + n_snd % len(POOL)))
                n_snd += 1
        # the camera: every gap between two moves is a slow push-in, so it never stands still
        cur = (P[0]["ox"] + 960, P[0]["oy"] + 540, 1.0)
        js.append("tl.set('%s', { %s }, 0);" % (W, tf(cur)))
        js.append("tl.set('%s', { %s }, 0);" % (G, tg(cur)))
        t = h0
        li, di = SOUNDS["plate-in"][3], SOUNDS["plate-in"][2]
        lo, do = SOUNDS["plate-out"][3], SOUNDS["plate-out"][2]
        for t0, d, to, ease in self._moves() + [(h1, 0, None, None)]:
            if t0 > t:
                dr = (cur[0], cur[1], cur[2] * (1 + DRIFT * (t0 - t)))
                js.append("tl.fromTo('%s', { %s }, { %s, duration:%.3f, ease:'none', immediateRender:false }, %.3f);" % (W, tf(cur), tf(dr), t0 - t, t))
                js.append("tl.fromTo('%s', { %s }, { %s, duration:%.3f, ease:'none', immediateRender:false }, %.3f);" % (G, tg(cur), tg(dr), t0 - t, t))
                cur = dr
            if to is None:
                break
            e = ease if ease.startswith("window.") else "'%s'" % ease
            js.append("tl.fromTo('%s', { %s }, { %s, duration:%.3f, ease:%s, immediateRender:false }, %.3f);" % (W, tf(cur), tf(to), d, e, t0))
            js.append("tl.fromTo('%s', { %s }, { %s, duration:%.3f, ease:%s, immediateRender:false }, %.3f);" % (G, tg(cur), tg(to), d, e, t0))
            cur, t = to, t0 + d
            if ease == SWIPE_EASE:
                snd.append('<audio id="sfx-%s-s%d" src="sfx/plate-in.mp3" data-start="%.3f" data-duration="%.2f" data-track-index="%d" data-volume="1"></audio>' % (cid, len(snd), t0 + SWIPE_PEAK * d - li, di, self.ta + 1))
        # face <-> board: one continuous swipe, the face goes out as the board comes in
        js.append("tl.set('%s', { x:%d }, 0);" % (R, 1920 if self.enter else 0))
        if self.enter:
            js.append("tl.fromTo('%s', { x:1920 }, { x:0, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (R, PUSH, PUSH_EASE, h0))
            js.append("tl.fromTo('#video-wrap', { x:0 }, { x:-1920, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (PUSH, PUSH_EASE, h0))
            snd.append('<audio id="sfx-%s-in" src="sfx/plate-in.mp3" data-start="%.3f" data-duration="%.2f" data-track-index="%d" data-volume="1"></audio>' % (cid, max(h0 + 0.5 * PUSH - li, 0), di, self.ta))
        if self.leave:
            js.append("tl.fromTo('%s', { x:0 }, { x:-1920, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (R, PUSH, PUSH_EASE, h1 - PUSH))
            js.append("tl.fromTo('#video-wrap', { x:1920 }, { x:0, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (PUSH, PUSH_EASE, h1 - PUSH))
            snd.append('<audio id="sfx-%s-out" src="sfx/plate-out.mp3" data-start="%.3f" data-duration="%.2f" data-track-index="%d" data-volume="1"></audio>' % (cid, h1 - 0.5 * PUSH - lo, do, self.ta))
        for k, (a, b) in enumerate(self.holes):
            js.append("tl.fromTo('%s', { x:0 }, { x:-1920, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (R, PUSH, PUSH_EASE, a - 0.5 * PUSH))
            js.append("tl.fromTo('#video-wrap', { x:1920 }, { x:0, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (PUSH, PUSH_EASE, a - 0.5 * PUSH))
            js.append("tl.fromTo('%s', { x:1920 }, { x:0, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (R, PUSH, PUSH_EASE, b - 0.5 * PUSH))
            js.append("tl.fromTo('#video-wrap', { x:0 }, { x:-1920, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (PUSH, PUSH_EASE, b - 0.5 * PUSH))
            snd.append('<audio id="sfx-%s-ho%d" src="sfx/plate-out.mp3" data-start="%.3f" data-duration="%.2f" data-track-index="%d" data-volume="1"></audio>' % (cid, k, a - lo, do, self.ta + 2))
            snd.append('<audio id="sfx-%s-hi%d" src="sfx/plate-in.mp3" data-start="%.3f" data-duration="%.2f" data-track-index="%d" data-volume="1"></audio>' % (cid, k, b - li, di, self.ta + 3))
        html = ('<style>%s</style>\n<div class="card-host clip" id="host-%s" data-card-id="%s" data-unanchored="1" data-start="%.3f" data-duration="%.3f" data-track-index="%d"'
                ' style="left:0;top:0;width:1920px;height:1080px;visibility:hidden;opacity:1;">\n<div id="%s-root" style="position:absolute;inset:0;overflow:hidden"><div class="bd-bg"></div>'
                '<div class="bd-w" id="%s-g">%s</div><div class="bd-w" id="%s-w">%s</div>%s</div></div>\n%s'
                % (SCENE_CSS + BASE_CSS + CSS, cid, cid, h0, h1 - h0, self.track, cid, cid, grid, cid, "\n".join(inner), FINISH if self.finish else "", "\n".join(snd)))
        return {"html": html, "js": "\n        ".join(js)}
