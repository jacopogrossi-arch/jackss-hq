# Short #3 v2 "Quanto costa lanciare un pantalone" (16/11/2026): the Inverso sample room at night. No board game, no mascot: every price is a real object in a dense room.
import json, math, os, re, shutil, sys
SK = "D:/ClaudeCodeTest/.claude/skills/fashion-3d"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SK + "/engine"); sys.path.insert(0, HERE)
from world3d import World3D
import room
PI = math.pi
WORDS = json.load(open(HERE + "/words.json", encoding="utf-8"))
norm = lambda s: re.sub(r"[^\w]", "", s.lower().split("'")[-1])


def at(word, n=1, after=0.0):
    k = 0
    for x in WORDS:
        if x["s"] >= after and norm(x["w"]) == norm(word):
            k += 1
            if k == n: return round(x["s"], 2)
    raise KeyError(word)


def end(word, n=1):
    k = 0
    for x in WORDS:
        if norm(x["w"]) == norm(word):
            k += 1
            if k == n: return round(x["e"], 2)
    raise KeyError(word)


DUR = 65.0
O = [0.0, 5.0, 14.9, 26.2, 38.2, 50.2, 58.6, 65.0]            # scene starts of the first build
N = [0.0, 5.0, 16.6, 26.6, 37.0, 48.8, 58.4, 65.0]            # scene starts with the new (v4) voice


def X(t):
    for k in range(7):
        if O[k] <= t < O[k + 1]:
            return round(N[k] + (t - O[k]) * (N[k + 1] - N[k]) / (O[k + 1] - O[k]), 3)
    return t

RED, BOSCO, RUGGINE = "#b8432a", "#2F3A2E", "#8A4B2D"
GLB = "D:/ClaudeCodeTest/social/short-03-tabellone/assets/trouser10b.glb"
CLIP = [float(x) for x in os.environ["CLIP"].split(",")] if os.environ.get("CLIP") else None          # test clip: CLIP="9,17" builds only that window (video time)
_O = CLIP[0] if CLIP else 0.0                                                      # test clip: object times (move/turn/talk/env) are plate times, so they shift by the clip start
w = World3D("s", CLIP[0] if CLIP else 0.0, CLIP[1] if CLIP else DUR, fov=42, w=1080, h=1920, fade=0.4)
w.shutter(0.5)

# ---- beats (all hang on the voice)
T_FLIP = at("brand") - 0.35
T_D1 = at("prima") - 0.05; T_MAP1 = T_D1 - 1.25             # up after "gioca con me", dive on "Prima casella"
T_D2 = at("seconda") - 0.15; T_MAP2 = T_D2 - 1.25
T_D3 = at("terza") - 0.15; T_MAP3 = T_D3 - 1.25
T_D4 = at("poi") - 0.2; T_MAP4 = T_D4 - 1.25
T_D5 = at("totale") - 0.1; T_MAP5 = T_D5 - 1.25
FLY = [[T_MAP1, T_D1 + 1.1], [T_MAP2, T_D2 + 1.1], [T_MAP3, T_D3 + 1.1], [T_MAP4, T_D4 + 1.1], [T_MAP5, T_D5 + 1.1]]
room.furnish(w, hide=FLY, hide2=[[T_D2 - 0.3, X(17.4)], [X(19.8), X(22.5)]])
w.leak(T_D2 - 0.05 - (CLIP[0] if CLIP else 0.0), 0.9)
w.leak(X(31.7) - (CLIP[0] if CLIP else 0.0), 0.5)                                   # the camera flash on the photo set

# ---- the logo sign: not at the start (the flip was in Short #2). It drops in for the end card.
ENDS = (0.9, 0.0, 3.0)
T_SIGN = at("scrivi") - 0.9
w.prop("logosign", "totem", (ENDS[0], -6.0, ENDS[2]), (1.0, 0.31), rot_y=0.0, height=0.78, flips=[[at("scrivi") + 0.5, 1.1, PI]],
       move=[(T_SIGN, 0.01, (ENDS[0], 3.6, ENDS[2]), "linear"), (T_SIGN + 0.02, 0.55, ENDS, "in")])
SIGN = ENDS

# ---- station 1: the drawing desk (brand price vs mine)
S1 = (-2.5, 0.9, 0.2)
w.prop("sketchdraw", "sk", (S1[0], 0.905, S1[2]), (0.55, 0.78), rot_y=0.15, t=T_D1, reveal=[at("disegno") + 0.2, at("meno") + 0.25])
w.card("c300", (-3.15, 1.45, 0.75), w=0.5, h=0.3, text="*€300–800*", sub="modellista", rot_y=0.3, color="#EFE9DD", t=at("300") - 0.1, move=[(T_MAP2 + 0.15, 0.01, (-3.15, -5.0, 0.75), "linear")])
w.card("c30", (-1.85, 1.45, 0.75), w=0.5, h=0.3, text="*< €30*", sub="carta, matita, metro", rot_y=-0.3, color="#B9AE98", t=at("30") - 0.05, move=[(T_MAP2 + 0.15, 0.01, (-1.85, -5.0, 0.75), "linear")])

# ---- station 2: the cutting table (pattern, redone until it falls well)
S2 = (0.5, 0.9, 0.95)
w.prop("patterncut", "pc", (S2[0], 0.915, S2[2]), (0.8, 1.16), rot_y=1.57, t=T_D2, cut=[at("rifaccio") - 0.4, at("bene") + 0.6])
w.card("ctime", (0.5, 1.55, 1.75), w=0.62, h=0.3, text="*tempo*, non €", rot_y=0.0, color="#B9AE98", t=at("tempo") - 0.1, move=[(T_MAP3 + 0.15, 0.01, (0.5, -5.0, 1.75), "linear")])

# ---- station 3: the photo set (shooting price vs 3D lookbook)
S3 = (3.5, 0.0, 0.5)
w.card("c3000", (3.0, 2.5, 1.55), w=0.62, h=0.34, text="*€3.000–8.000*", sub="shooting", rot_y=-0.2, color="#EFE9DD",
       t=at("shooting") - 0.5, move=[(at("shooting") + 0.15, 0.6, (3.0, 1.45, 1.55), "in"), (T_MAP4 + 0.15, 0.01, (3.0, -5.0, 1.55), "linear")])
w.solid("lapt", "box", (2.45, 0.3, 1.35), (0.8, 0.6, 0.55), color="#7a5236", rough=0.6)
w.prop("laptop", "lap", (2.45, 0.6, 1.35), rot_y=-0.5, t=at("lookbook") - 0.4)

# ---- station 4: the twist, 100 tags on the back wall, 10 then 20 light up
t10, t20 = at("10"), at("20")
lit = [(t10 + 0.09 * i, i) for i in range(10)] + [(t20 + 0.07 * i, 10 + i) for i in range(10)]
w.prop("dotgrid", "g", (0.9, 1.7, -2.95), (1.7, 1.7), cols=10, rows=10, color="#EFE9DD", pop=[T_D4 + 0.6, 0.012], lit=lit, accent="#ffc23a")

# ---- station 5: the Blender trouser on a rail with a hanger. It is the first thing you see ("€ ?"), parks underground during the story, comes back for the arrival.
HR = (-0.9, 0.0, 2.55)
T_HIDE, T_BACK = T_MAP1 + 0.4, T_D5 - 0.35


def hero(oid, pos):
    return dict(move=[(T_HIDE, 0.01, (pos[0], -8.0, pos[2]), "linear"), (T_BACK, 0.01, pos, "linear")])


def hsolid(oid, shape, pos, size, **kw):
    w.solid(oid, shape, pos, size, color="#1E1B18", metal=0.8, rough=0.4, **hero(oid, pos), **kw)


hsolid("hbar", "box", (HR[0], 1.76, HR[2]), (1.5, 0.03, 0.03))
for _i, _sx in enumerate((-0.75, 0.75)):
    hsolid("hst%d" % _i, "cyl", (HR[0] + _sx, 0.88, HR[2]), (0.04, 1.76))
    hsolid("hft%d" % _i, "cyl", (HR[0] + _sx, 0.02, HR[2]), (0.45, 0.04))
hsolid("hhook", "cyl", (HR[0], 1.80, HR[2]), (0.014, 0.08))                         # the hanger: hook on the rail, a bar at the waistband, two clips
hsolid("hhbar", "box", (HR[0], 1.742, HR[2]), (0.42, 0.016, 0.016))
for _i, _sx in enumerate((-0.17, 0.17)):
    hsolid("hclip%d" % _i, "box", (HR[0] + _sx, 1.705, HR[2] + 0.004), (0.034, 0.07, 0.03))
w.glb("tr", GLB, fit=0.95, pos=(HR[0], 0.78, HR[2]), rot_y=0.15, double=True, fabric=True, **hero("tr", (HR[0], 0.78, HR[2])))
w.card("cq", (HR[0] + 0.62, 1.5, HR[2] + 0.1), w=0.5, h=0.3, text="*€ ?*", rot_y=-0.25, color="#EFE9DD", move=[(T_HIDE, 0.01, (HR[0] + 0.62, -8.0, HR[2] + 0.1), "linear")])
w.card("ctot", (-0.9, 2.15, 2.55), w=0.62, h=0.34, text="*€500–1.500*", sub="tessuto, primo drop", rot_y=0.0, color="#EFE9DD", t=at("500") - 0.2)

# ---- Jacopo in miniature: a toy-figure of him (round glasses, swept-up hair, black tee, selvage jeans, boots) on each station; his mouth moves and the right hand gestures while the voice speaks
def talk_windows(t0, t1):
    ws = []
    for x in WORDS:
        if t0 + 0.3 <= x["s"] <= t1 - 0.15:
            a_, b_ = x["s"] - 0.05, x["e"] + 0.12
            if ws and a_ - ws[-1][1] < 0.3: ws[-1][1] = b_
            else: ws.append([a_, b_])
    return [tuple(v) for v in ws]


ENV = json.load(open(HERE + "/env.json"))                                               # voice loudness at 60 fps: the narrator moves with the speech
OMINO = "D:/ClaudeCodeTest/social/short-03-tabellone/assets/action-figure-anim10.glb"   # PS2 toy of Jacopo (Hunyuan3D shape + colours projected from the 3 approved views)
DIVE = {1: ((-2.5, 2.3, 1.25), (-2.5, 0.9, 0.2)), 2: ((0.5, 2.6, 1.9), (0.5, 0.9, 0.95)), 3: ((3.5, 1.7, 2.8), (3.5, 1.1, 0.5)),
        4: ((0.9, 2.3, 0.6), (0.9, 1.7, -2.95)), 5: ((-0.9, 1.9, 4.2), (-0.9, 1.0, 2.55))}


def _merged_talk(gap=0.9):
    ws = []
    for x_ in WORDS:
        a_, b_ = x_["s"] - 0.05, x_["e"] + 0.12
        if ws and a_ - ws[-1][1] < gap: ws[-1][1] = b_
        else: ws.append([a_, b_])
    return [tuple(v) for v in ws]


TALK = _merged_talk()
WORDS_T = [round(wd["s"], 3) for wd in WORDS]


# ---- v7 (17/11/2026): the new Tripo file has 4 clips of 10 s each (played at normal speed, no slow motion, no cutting). RULE (Jacopo): in every shot the narrator plays ONE single clip from start to end of the shot,
# never half of one and half of another (that was the "glitch"). Close-up on an important sentence = the clip with the most hand movement; side shots = the still "relaxed" clip.
ACT = json.load(open(HERE + "/clip-activity.json"))            # arm activity per frame (24 fps) of each clip of the glb, measured on the exported file
# The 4 animations of the Tripo file (checked frame by frame, 17/11/2026; catalogue sheet: assets/clip-catalogo.png). Indexes = order inside action-figure-anim10.glb:
IDLE = 0        # FERMA: rilassato, braccia lungo i fianchi, quasi immobile  -> inquadrature di lato / quando non e' protagonista
E_MID = 1       # GESTI MEDI: parla guardando in camera, braccia che si aprono e si chiudono, ritmo calmo
E_MAX = 2       # GESTI AMPI: parla con energia, braccia larghe, mani sui fianchi, la piu' mossa -> parole importanti
EXPL = 3        # SPIEGA: parla spiegando, palmi aperti verso la camera, movimento medio
CLIP_FPS, CLIP_DUR = 24.0, 9.9583
HERO_CLIP = {1: E_MAX, 2: EXPL, 3: E_MID, 4: EXPL, 5: E_MAX}    # which clip each close-up uses (k = station); the final (CTA) uses FINAL_CLIP
FINAL_CLIP = E_MID
FADE = 0.35
HERO_SPEED = 1.0                                                  # playback speed of the close-up clips (1.0 = as made by Tripo)


def _off(ci, L, high=True, sp=1.0):
    """Start offset in the clip (s) for a segment of length L played at speed sp: the window with the most (or least) activity, away from the first/last 0.4 s (the ends of a clip are not loops)."""
    a = ACT[ci]["act"]; n = int(L * sp * CLIP_FPS); lo, hi = int(0.4 * CLIP_FPS), int((CLIP_DUR - 0.4) * CLIP_FPS) - n
    if hi <= lo: return 0.4
    best = max if high else min
    k = best(range(lo, hi + 1), key=lambda i: sum(a[i:i + n]))
    return round(k / CLIP_FPS, 3)


def _speed(L):
    """The 10 s clips are gentle at normal speed: close-ups play faster (up to HERO_SPEED) as long as the whole segment still fits inside ONE clip (no loop, no second clip)."""
    return round(max(1.0, min(HERO_SPEED, (CLIP_DUR - 0.9) / L)), 3)


def _segments(t0, t1, heroes):
    """[[t0, t1, clip, offset], ...]: calm clip until a close-up, ONE clip for the whole close-up, calm clip in between/after. Neighbours overlap by FADE (the cross-fade runs on the camera move). heroes = [(start, end, clip)]."""
    segs = []

    def calm(a, b):
        while a < b - 1e-6:
            bb = min(b, a + 9.0); segs.append([a, bb, IDLE, _off(IDLE, bb - a, False), 1.0]); a = bb - FADE
            if bb >= b: break
    cur = t0
    for hs, he, ci in heroes:
        calm(cur, hs + FADE)
        sp_ = _speed(he - hs); segs.append([hs, he, ci, _off(ci, he - hs, True, sp_), sp_]); cur = he - FADE
    if heroes[-1][1] < t1 - 0.05: calm(cur, t1)
    return segs


def me(oid, pos, t0, t1, rot=0.0, height=0.2, heroes=()):
    """The narrator INSIDE the scene: he stands on a surface of the station, in perspective and lit by the room, and the camera frames him as a character of the world. v7: one Tripo clip per shot (see above)."""
    x, y, z = pos
    sg = _segments(t0, t1, heroes)
    for q in sg: print("  %s seg %.2f-%.2f clip %d off %.2f x%.2f" % (oid, q[0], q[1], q[2], q[3], q[4]))
    w.glb(oid, OMINO, fit=height, pos=(x, -8.0, z), rot_y=rot, segs=[[a_ - _O, b_ - _O, c_, o_, v_] for a_, b_, c_, o_, v_ in sg], segFade=FADE, clipSpeed=1.0, bob=0,
          move=[(t0 - _O, 0.35, pos, "out"), (t1 - _O, 0.01, (x, -8.0, z), "linear")])


# ---- NARRATOR LAYER (v5, 17/11/2026): always present at the side (bottom left, under the captions) while the camera works on the topic; on the sentences that matter the rectangle grows to a close-up for the WHOLE sentence (riser before it), then back to the side.
def _sentences():
    out, cur = [], []
    for wd in WORDS:
        cur.append(wd)
        if wd["w"][-1] in ".?!": out.append((cur[0]["s"], cur[-1]["e"], " ".join(x["w"] for x in cur))); cur = []
    if cur: out.append((cur[0]["s"], cur[-1]["e"], " ".join(x["w"] for x in cur)))
    return out


SENT = _sentences()
_sent = lambda pre: next(x for x in SENT if x[2].lower().startswith(pre.lower()))
HEROES = [_sent(p) for p in ("Io parto", "Costa tempo", "Io il mio", "Ne faccio", "Il resto")]
FINAL = _sent("A quanto")
TAN = 0.49866                                         # 2 * tan(fov / 2) for fov 28
_dist = lambda vis_h: round(vis_h / TAN, 3)
SIDE = [-10, 0, 560, 660, 0.5, _dist(1.12), 0.45]    # x, y, w, h (px, origin bottom-left), look height (m), camera distance (m), turn toward the scene
OFF = [-700, 0, 560, 660, 0.5, _dist(1.12), 0.45]
HERO = [0, 0, 1080, 1100, 0.66, _dist(0.72), 0.0]
HEROF = [0, 0, 1080, 1100, 0.66, _dist(0.72), 0.0]
LAY = [(3.3, 0.55, SIDE, "glide")]
for s_, e_, _tx in HEROES:
    LAY += [(s_ - 0.5, 0.45, HERO, "glide"), (e_ + 0.1, 0.4, SIDE, "glide")]
LAY += [(FINAL[0] - 0.5, 0.45, HEROF, "glide")]
_ws = [round(wd["s"], 3) for wd in WORDS]

# ---- the map: five stations, badges and path only while the camera is up
ST = {1: (-2.5, 1.75, "disegno"), 2: (0.5, 2.15, "modello"), 3: (3.5, 2.2, "foto"), 4: (0.9, -1.7, "pre-order"), 5: (-0.9, 2.55, "arrivo")}
for k, (t0, t1) in enumerate([(T_MAP1, T_D1), (T_MAP2, T_D2), (T_MAP3, T_D3), (T_MAP4, T_D4), (T_MAP5, T_D5)]):
    for n, (x, z, word) in ST.items():
        w.prop("floorbadge", "b%d_%d" % (k, n), (x, 0.02, z), (0.8,), rot_y=PI / 2, n=n, word=word, ring=RED, show=t0 + 0.15 + 0.08 * n, out=t1 + 0.25)
PATH = [(-2.5, 1.75), (-1.2, 2.3), (0.5, 2.15), (2.0, 2.4), (3.5, 2.2), (4.2, 0.0), (3.2, -1.4), (0.9, -1.7), (0.9, 0.2), (-0.9, 2.55)]
w.prop("pathdots", "path", (0, 0.035, 0), pts=[[x, 0, z] for x, z in PATH], gap=0.14, r=0.045, flat=True, color=RED, span=[T_MAP1 + 0.4, T_MAP1 + 1.3], out=T_D1 + 0.25)

# ---- the camera: a cut or a move every 2-3 s
_cam, _end = w.cam, [0.0]


K = 1.75
def _far(p, l):
    return tuple(l[i] + (p[i] - l[i]) * K for i in range(3)) if p[1] < 10 else p


_calls = []


def _camx(pos, look, t=None, d=1.3, ease="hand", raw=False):
    pos = pos if raw else _far(pos, look)
    if t is None:
        return _cam(pos, look)
    _calls.append([t, d, pos, look, ease])


def _flush():
    """Emit the camera moves in order; a move never runs into the next one (its duration is trimmed), so every start time stays on its word."""
    _calls[:] = [c for c in _calls if len(c) > 5 or not any(a_ <= c[0] <= b_ for a_, b_ in HERO_INT)]     # inside a close-up the camera belongs to the close-up
    _calls.sort(key=lambda c: c[0])
    for i, _c in enumerate(_calls):
        t, d, pos, look, ease = _c[:5]
        nxt = _calls[i + 1][0] if i + 1 < len(_calls) else 1e9
        dd = min(d, nxt - t - 0.02)
        if dd < 0.25:
            print("  cam skipped %.2f (no room)" % t); continue
        if dd < d - 0.01: print("  cam trim %.2f: %.2f -> %.2f" % (t, d, dd))
        _cam(pos, look, t=t, d=dd, ease=ease)


w.cam = _camx
MAP = ((0.6, 15.0, 1.0), (0.6, 0.0, 0.8))
_cam((-0.25, 1.15, 5.6), (-0.9, 1.15, 2.55))                                                           # frame 1: the hanging trouser and "€ ?"
w.cam((-1.9, 1.3, 5.0), (-0.9, 1.1, 2.55), t=0.05, d=2.3, ease="glide", raw=True)
w.cam((0.2, 1.7, 4.3), (0.6, 1.0, 0.8), t=2.4, d=1.1, ease="glide")
w.cam(MAP[0], MAP[1], t=T_MAP1, d=1.2, ease="glide")
w.cam((-2.5, 2.3, 1.25), (-2.5, 0.9, 0.2), t=T_D1, d=1.1, ease="glide")                           # dive 1: the desk
w.cam((-2.55, 1.2, 1.15), (-3.12, 1.04, 0.42), t=X(5.9), d=1.5, raw=True)                                       # sketch paper, low
w.cam((-2.5, 1.55, 2.1), (-2.5, 1.2, 0.3), t=X(7.7), d=1.1, ease="glide")                             # wide: the 300-800 card lands
w.cam((-3.1, 1.5, 1.4), (-3.1, 1.45, 0.75), t=X(9.0), d=0.9)                                          # push on the rust card
w.cam((-2.15, 1.3, 1.2), (-2.4, 0.95, 0.2), t=X(10.4), d=1.3, ease="glide")                           # the hand drawing: pencil
w.cam((-2.45, 1.7, 0.7), (-2.5, 0.9, 0.2), t=X(12.1), d=0.85)                                          # top-down on the drawing
w.cam((-1.85, 1.5, 1.5), (-1.85, 1.45, 0.75), t=X(13.0), d=0.45, ease="glide")                        # the <30 card
w.cam(MAP[0], MAP[1], t=T_MAP2, d=1.2, ease="glide")
w.cam((0.5, 2.6, 1.9), (0.5, 0.9, 0.95), t=T_D2, d=1.1, ease="glide")                              # dive 2: the cutting table
w.cam((1.25, 1.2, 1.75), (1.72, 1.05, 0.95), t=X(16.4), d=1.5, raw=True)
w.cam((1.7, 1.3, 1.9), (1.2, 0.85, 1.2), t=X(18.0), d=1.6, ease="glide")                             # the shears cut: from the side
w.cam((0.5, 2.2, 1.3), (0.5, 0.9, 0.95), t=X(20.0), d=1.5)                                            # top-down on the pattern
w.cam((0.3, 1.55, 3.4), (0.5, 1.4, 1.75), t=X(21.9), d=1.1, ease="glide")                             # the time card
w.cam((1.2, 1.5, 3.1), (0.8, 1.0, 1.0), t=X(23.4), d=1.1)
w.cam(MAP[0], MAP[1], t=T_MAP3, d=1.2, ease="glide")
w.cam((3.5, 1.7, 2.8), (3.5, 1.1, 0.5), t=T_D3, d=1.1, ease="glide")                               # dive 3: the photo set
w.cam((2.5, 1.2, 3.1), (3.5, 1.25, 0.3), t=X(27.7), d=1.4)                                            # set wide
w.cam((3.0, 1.6, 2.2), (3.0, 1.45, 1.55), t=X(29.4), d=1.0, ease="glide")                             # the 3000-8000 card lands
w.cam((2.2, 1.35, 3.4), (3.4, 1.2, 0.9), t=X(31.0), d=1.5, raw=True)                                             # the camera on its tripod
w.cam((1.2, 1.2, 3.6), (2.45, 0.8, 1.35), t=X(33.0), d=1.5, ease="glide", raw=True)                              # the laptop: my lookbook, in 3D
w.cam((2.7, 1.0, 2.2), (2.45, 0.8, 1.35), t=X(35.2), d=1.5)
w.cam(MAP[0], MAP[1], t=T_MAP4, d=1.2, ease="glide")
w.cam((0.9, 2.3, 0.6), (0.9, 1.7, -2.95), t=T_D4, d=1.1, ease="glide")                             # dive 4: the wall
w.cam((0.8, 1.6, 2.2), (0.9, 1.6, -2.9), t=X(39.4), d=1.6)                                            # the 100 tags appear
w.cam((-0.4, 1.7, 1.6), (1.0, 1.7, -2.9), t=X(41.6), d=1.7, ease="glide")                              # orbit
w.cam((0.3, 1.3, 2.7), (0.0, 1.35, 1.2), t=X(43.5), d=2.0, raw=True)
w.cam((1.0, 1.7, 0.6), (0.9, 1.7, -2.9), t=X(46.2), d=1.2, ease="glide")                             # push: ten, then twenty light up
w.cam((0.9, 1.7, 2.4), (0.9, 1.7, -2.9), t=X(47.8), d=0.9)
w.cam(MAP[0], MAP[1], t=T_MAP5, d=1.2, ease="glide")
w.cam((-0.9, 1.9, 4.2), (-0.9, 1.0, 2.55), t=T_D5, d=1.1, ease="glide")                            # dive 5: the trouser
w.cam((-1.7, 1.2, 3.8), (-0.9, 1.1, 2.55), t=X(51.7), d=1.8)
w.cam((-0.5, 2.3, 3.7), (-0.9, 1.8, 2.55), t=X(53.5), d=1.3, ease="glide")                            # the 500-1500 card
w.cam((-1.1, 0.7, 3.4), (-0.9, 0.8, 2.55), t=X(55.2), d=1.7)                                          # low on the hem
w.cam((-0.3, 1.4, 6.4), (0.2, 1.0, 2.6), t=X(57.0), d=1.8, ease="glide", raw=True)                  # widen: rail, CTA and sign in one frame
w.cam((0.9, 1.0, 6.0), (0.9, 0.9, 3.0), t=X(58.9), d=2.1, raw=True)                                  # slow push on the ask
w.cam((0.9, 1.35, 5.0), (0.9, 1.25, 2.5), t=X(61.0), d=2.0, ease="glide", raw=True)                   # the logo sign, centred
w.cam((0.9, 1.3, 4.7), (0.9, 1.2, 2.5), t=X(63.0), d=2.0, raw=True)                                   # a last drift in, no dead frames
# ---- narrator placement + close-up cameras (v5b)
HERO_INT = [(s_ - 0.5, e_ + 0.05) for s_, e_, _x in HEROES] + [(FINAL[0] - 0.5, DUR + 1.0)]
V4 = {1: ((-3.12, 0.9, 0.42), 0.30), 2: ((1.72, 0.915, 0.95), 0.30), 3: ((2.72, 0.6, 1.5), 0.30), 4: ((0.0, 0.915, 1.5), 0.34), 5: ((0.9, 0.0, 3.55), 0.55)}
WIN = {1: (T_D1, T_MAP2), 2: (T_D2, T_MAP3), 3: (T_D3, T_MAP4), 4: (T_D4, T_MAP5), 5: (T_D5, DUR)}


def _ndc(cp, cl, p, fov=42.0, asp=1080 / 1920):
    f = [cl[i] - cp[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in f)); f = [v / n for v in f]
    r = [f[2], 0.0, -f[0]]; rn = math.sqrt(r[0] ** 2 + r[2] ** 2) or 1.0; r = [r[0] / rn, 0.0, r[2] / rn]
    u = [f[1] * r[2] - f[2] * r[1], f[2] * r[0] - f[0] * r[2], f[0] * r[1] - f[1] * r[0]]
    v = [p[i] - cp[i] for i in range(3)]; zc = sum(v[i] * f[i] for i in range(3))
    if zc < 0.2: return None
    th = math.tan(math.radians(fov / 2)); return sum(v[i] * r[i] for i in range(3)) / (zc * th * asp), sum(v[i] * u[i] for i in range(3)) / (zc * th), zc


def _score(P, k):
    s = 0.0
    for c in _calls:
        if len(c) > 5 or not (WIN[k][0] <= c[0] <= WIN[k][1]): continue
        q = _ndc(c[2], c[3], P)
        if q is None: continue
        x_, y_, z_ = q
        if 0.30 < abs(x_) < 0.86 and -0.8 < y_ < 0.55 and 0.35 < z_ < 5.0: s += 1.0 + (0.3 if x_ < 0 else 0.0)
        elif abs(x_) < 0.22 and -0.6 < y_ < 0.3: s -= 0.7
    return s


PLACE = {}
for k_ in (1, 2, 3, 4):
    (bx, by, bz), hh = V4[k_]; best = None
    for dx_ in [i * 0.15 for i in range(-5, 6)]:
        for dz_ in [i * 0.15 for i in range(-4, 5)]:
            P = (bx + dx_, by + hh * 0.5, bz + dz_); sc_ = _score(P, k_)
            if best is None or sc_ > best[0]: best = (sc_, (bx + dx_, by, bz + dz_))
    PLACE[k_] = best[1]; print("  narrator station %d at (%.2f, %.2f, %.2f) score %.1f" % (k_, *best[1], best[0]))
PLACE[5] = V4[5][0]
for k_ in range(1, 6):
    P = PLACE[k_]; hh = V4[k_][1]; cams_ = [c for c in _calls if len(c) <= 5 and WIN[k_][0] <= c[0] <= WIN[k_][1]]
    mx_, mz_ = (sum(c[2][0] for c in cams_) / len(cams_), sum(c[2][2] for c in cams_) / len(cams_)) if cams_ else (P[0], P[2] + 3)
    rot_ = math.atan2(mx_ - P[0], mz_ - P[2]) * 0.9
    t0_ = WIN[k_][0] + 0.9; t1_ = (WIN[k_][1] + 0.1) if k_ < 5 else DUR + 1.0
    s_, e_, _x = HEROES[k_ - 1]; d_ = 1.55 * hh      # v7: wider close-up so the hands are in frame
    HL = [(s_ - 0.55, e_ + 0.05, HERO_CLIP[k_])] if k_ < 5 else [(s_ - 0.55, e_ + 0.05, HERO_CLIP[5]), (FINAL[0] - 0.55, t1_, FINAL_CLIP)]
    me("nar%d" % k_, P, t0_, t1_, rot=rot_, height=hh, heroes=HL)
    pos0 = (P[0] + math.sin(rot_) * d_, P[1] + 0.60 * hh, P[2] + math.cos(rot_) * d_); look0 = (P[0], P[1] + 0.60 * hh, P[2])
    _calls.append([s_ - 0.5, 0.45, pos0, look0, "glide", "hero"])
    if e_ - s_ > 2.2:
        d1 = d_ * 0.9; _calls.append([s_ + 0.9, e_ - s_ - 1.1, (P[0] + math.sin(rot_) * d1, P[1] + 0.60 * hh, P[2] + math.cos(rot_) * d1), look0, "glide", "hero"])
    if k_ == 5:                                                                  # final: same spot, the camera pulls back to show him with the sign behind
        dF = 2.3 * hh; _calls.append([FINAL[0] - 0.5, 0.5, (P[0], P[1] + 0.5 * hh, P[2] + dF), (P[0], P[1] + 0.78 * hh, P[2]), "glide", "hero"])
        dF2 = 2.7 * hh; _calls.append([FINAL[0] + 1.5, 4.0, (P[0], P[1] + 0.5 * hh, P[2] + dF2), (P[0], P[1] + 0.85 * hh, P[2]), "glide", "hero"])
_flush()
w.dof(0.0, DUR, aperture=0.003)

# ---- the cost pill (a live counter that follows the PHASE) + text on screen the whole video
PILL = [(T_D1, "meno di 30 €"), (T_D2, "meno di 30 € + tempo"), (T_D3, "meno di 30 € + tempo"), (T_D4, "10–20 pezzi, non 100"), (T_D5, "500–1.500 €")]
nm = lambda t: t.lower().strip(".,:?!")
KEY = {"brand", "gioca", "disegno", "trenta", "30", "cartamodello", "tempo", "soldi", "shooting", "3d", "colpo", "prenotato", "numerati", "totale", "fiducia", "pantalone", "commenti"}
chunks, cur = [], []
for i, x in enumerate(WORDS):
    cur.append(x)
    brk = x["w"].endswith((".", ":", "?", "!", ",")) or len(cur) >= 3 or sum(len(c["w"]) for c in cur) > 17
    if brk or i == len(WORDS) - 1:
        nxt = WORDS[i + 1]["s"] if i + 1 < len(WORDS) else cur[-1]["e"] + 1.0
        txt = " ".join(c["w"] for c in cur)
        for c in cur:
            if nm(c["w"]) in KEY:
                b = c["w"].rstrip(".,:!?"); txt = txt.replace(c["w"], "*" + b + "*" + c["w"][len(b):], 1); break
        chunks.append((cur[0]["s"], min(nxt - 0.02, cur[-1]["e"] + 0.45), txt.rstrip(".,:")))
        cur = []
w.big(-0.3 - _O, 3.6 - _O, "Quanto costa|lanciare un *pantalone*?", top=250, size=80)
w.big(t10 - 0.2 - _O, T_MAP5 + 0.2 - _O, "*10*, poi *20*|non cento", top=250, size=88)
chunks = [c for c in chunks if not (c[0] < 3.6 or (c[0] < T_MAP5 + 0.2 and c[1] > t10 - 0.2) or c[0] >= at("scrivi") - 0.05)]
w.big(at("scrivi") - 0.2 - _O, DUR - _O, "Scrivi *PANTALONE*|nei commenti|e ti dico il *prezzo finale*", top=215, size=74)     # the CTA as big text above the narrator (the floor plate was hidden behind him)
w.captions([(a_ - _O, b_ - _O, tx_) for a_, b_, tx_ in chunks], top=340, size=96)                                                                      # captions up: the close-up of the narrator takes the lower half


def _extra(path):
    p = open(path, encoding="utf-8").read()
    css = ("<style>#cost{position:absolute;left:0;right:0;top:118px;text-align:center;opacity:0;pointer-events:none;z-index:60}"
           "#cost span{display:inline-block;padding:16px 32px;border-radius:999px;background:rgba(22,18,14,.72);color:#fbf7ee;font:600 40px/1.1 Inter,'Segoe UI',sans-serif;letter-spacing:-.01em}"
           "#cost i{font-family:'Playfair Display',Georgia,serif;font-weight:500;color:#ffb48f;font-style:italic}</style></head>")
    js = ("<div id='cost'><span>il mio costo: <i id='costv'></i></span></div>"
          "<script>(function(){var S=%s,OUT=%.3f;window.addEventListener('hf-seek',function(e){var t=e.detail.time+%s,el=document.getElementById('cost'),v=document.getElementById('costv'),k=-1;"
          "for(var i=0;i<S.length;i++)if(t>=S[i][0])k=i;var a=k<0?0:Math.min(1,(t-S[0][0])/0.25,(OUT-t)/0.25);el.style.opacity=Math.max(0,a);"
          "if(k>=0&&v.textContent!==S[k][1]){v.textContent=S[k][1];}var p=k>=0?Math.min(1,(t-S[k][0])/0.2):1;el.style.transform='scale('+(1+0.12*Math.sin(Math.PI*p))+')';});})();</script></body>"
          ) % (json.dumps(PILL), at("scrivi") - 0.2, "%.3f" % (CLIP[0] if CLIP else 0.0))
    open(path, "w", encoding="utf-8").write(p.replace("</head>", css, 1).replace("</body>", js, 1))


if __name__ == "__main__":
    out = os.path.join(HERE, "comp")
    print(World3D.page(out, [w], duration=(CLIP[1] - CLIP[0]) if CLIP else DUR)); _extra(os.path.join(out, "index.html"))
    if CLIP:                                                                   # the plate time already starts at the clip start: the host must start at 0
        ix = os.path.join(out, "index.html"); h_ = open(ix, encoding="utf-8").read()
        h_ = re.sub(r'data-start="[0-9.]+"', 'data-start="0"', h_); open(ix, "w", encoding="utf-8").write(h_)
    os.makedirs(os.path.join(out, "img"), exist_ok=True); shutil.copy(os.path.join(HERE, "assets", "me.png"), os.path.join(out, "img", "me.png")); print("built")
