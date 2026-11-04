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
SWIPE = 1.0                  # page -> page swipe, seconds
SWIPE_EASE = "power3.inOut"  # slow start, fast middle, soft landing
GLIDE_EASE = "power2.inOut"
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
    def __init__(self, cid, track=10, track_audio=300, enter=True, leave=True):
        self.cid, self.track, self.ta, self.enter, self.leave, self.pages = cid, track, track_audio, enter, leave, []

    def page(self, scene, at, a, b, cam=None, overview=True):
        self.pages.append(dict(scene=scene, ox=at[0] * PITCH[0], oy=at[1] * PITCH[1], a=a, b=b, cam=cam, overview=overview))

    def _moves(self):
        moves = []   # (start, duration, (board x, board y, scale), ease)
        for n, p in enumerate(self.pages):
            ox, oy = p["ox"], p["oy"]
            end = p["b"] - (0.5 * SWIPE if n + 1 < len(self.pages) else 0.45 * PUSH)
            if n:
                moves.append((p["a"] - 0.55 * SWIPE, SWIPE, (ox + 960, oy + 540, 1.0), SWIPE_EASE))
            free = moves[-1][0] + moves[-1][1] if moves else p["a"] + 0.45 * PUSH
            if p["cam"]:
                todo = [(t - 0.45, (x, y, s), d) for t, x, y, s, d in p["cam"]]
            else:
                gs = _groups(p["scene"]) if p["scene"] else []
                todo = []
                for k, (t, b) in enumerate(gs):
                    nxt = gs[k + 1][0] if k + 1 < len(gs) else end
                    todo.append((t - 0.45, _focus(b), max(0.7, min(1.4, nxt - t))))
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
        W, R = "#%s-w" % cid, "#%s-root" % cid
        tf = lambda c: "x:%.1f,y:%.1f,scale:%.4f" % (960 - c[2] * c[0], 540 - c[2] * c[1], c[2])
        js, inner, snd = [], [], []
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
        t = h0
        li, di = SOUNDS["plate-in"][3], SOUNDS["plate-in"][2]
        lo, do = SOUNDS["plate-out"][3], SOUNDS["plate-out"][2]
        for t0, d, to, ease in self._moves() + [(h1, 0, None, None)]:
            if t0 > t:
                dr = (cur[0], cur[1], cur[2] * (1 + DRIFT * (t0 - t)))
                js.append("tl.fromTo('%s', { %s }, { %s, duration:%.3f, ease:'none', immediateRender:false }, %.3f);" % (W, tf(cur), tf(dr), t0 - t, t))
                cur = dr
            if to is None:
                break
            js.append("tl.fromTo('%s', { %s }, { %s, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (W, tf(cur), tf(to), d, ease, t0))
            cur, t = to, t0 + d
            if ease == SWIPE_EASE:
                snd.append('<audio id="sfx-%s-s%d" src="sfx/plate-in.mp3" data-start="%.3f" data-duration="%.2f" data-track-index="%d" data-volume="1"></audio>' % (cid, len(snd), t0 + 0.5 * d - li, di, self.ta + 1))
        # face <-> board: one continuous swipe, the face goes out as the board comes in
        js.append("tl.set('%s', { x:%d }, 0);" % (R, 1920 if self.enter else 0))
        if self.enter:
            js.append("tl.fromTo('%s', { x:1920 }, { x:0, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (R, PUSH, SWIPE_EASE, h0))
            js.append("tl.fromTo('#video-wrap', { x:0 }, { x:-1920, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (PUSH, SWIPE_EASE, h0))
            snd.append('<audio id="sfx-%s-in" src="sfx/plate-in.mp3" data-start="%.3f" data-duration="%.2f" data-track-index="%d" data-volume="1"></audio>' % (cid, max(h0 + 0.5 * PUSH - li, 0), di, self.ta))
        if self.leave:
            js.append("tl.fromTo('%s', { x:0 }, { x:-1920, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (R, PUSH, SWIPE_EASE, h1 - PUSH))
            js.append("tl.fromTo('#video-wrap', { x:1920 }, { x:0, duration:%.3f, ease:'%s', immediateRender:false }, %.3f);" % (PUSH, SWIPE_EASE, h1 - PUSH))
            snd.append('<audio id="sfx-%s-out" src="sfx/plate-out.mp3" data-start="%.3f" data-duration="%.2f" data-track-index="%d" data-volume="1"></audio>' % (cid, h1 - 0.5 * PUSH - lo, do, self.ta))
        html = ('<style>%s</style>\n<div class="card-host clip" id="host-%s" data-card-id="%s" data-unanchored="1" data-start="%.3f" data-duration="%.3f" data-track-index="%d"'
                ' style="left:0;top:0;width:1920px;height:1080px;visibility:hidden;opacity:1;">\n<div id="%s-root" style="position:absolute;inset:0;overflow:hidden"><div class="bd-bg"></div>'
                '<div class="bd-w" id="%s-w">%s\n%s</div></div></div>\n%s'
                % (SCENE_CSS + BASE_CSS + CSS, cid, cid, h0, h1 - h0, self.track, cid, cid, grid, "\n".join(inner), "\n".join(snd)))
        return {"html": html, "js": "\n        ".join(js)}
