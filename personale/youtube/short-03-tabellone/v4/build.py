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
GLB = "D:/ClaudeCodeTest/personale/youtube/short-03-tabellone/assets/trouser10b.glb"
w = World3D("s", 0.0, DUR, fov=42, w=1080, h=1920, fade=0.4)
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
w.leak(T_D2 - 0.05, 0.9)
w.leak(X(31.7), 0.5)                                   # the camera flash on the photo set

# ---- the logo sign: not at the start (the flip was in Short #2). It drops in for the end card.
ENDS = (0.9, 0.0, 2.5)
T_SIGN = at("scrivi") - 0.9
w.prop("logosign", "totem", (ENDS[0], -6.0, ENDS[2]), (1.0, 0.31), rot_y=0.0, height=1.3, flips=[[at("scrivi") + 0.5, 1.1, 2 * PI]],
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
w.prop("ctaplate", "cta", (0.9, 0.0, 3.4), (1.2, 0.4), text="Scrivi *PANTALONE* nei commenti", t=at("scrivi") - 0.5)
w.card("cprice", (0.9, 0.7, 3.4), w=0.95, h=0.28, text="e ti dico il *prezzo finale*", rot_y=0.0, color="#B9AE98", t=at("commenti") + 0.1)

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
OMINO = "D:/ClaudeCodeTest/personale/youtube/short-03-tabellone/assets/action-figure-3d.glb"   # PS2 toy of Jacopo (Hunyuan3D shape + colours projected from the 3 approved views)
DIVE = {1: ((-2.5, 2.3, 1.25), (-2.5, 0.9, 0.2)), 2: ((0.5, 2.6, 1.9), (0.5, 0.9, 0.95)), 3: ((3.5, 1.7, 2.8), (3.5, 1.1, 0.5)),
        4: ((0.9, 2.3, 0.6), (0.9, 1.7, -2.95)), 5: ((-0.9, 1.9, 4.2), (-0.9, 1.0, 2.55))}


ZOOMS = []


def me(oid, pos, t0, t1, rot=0.0, height=0.2, k=1):
    """The narrator: appears, the camera zooms on him while he talks, then cuts at once to what he is saying about (the station's dive view). He moves with the speech: his body follows the voice loudness and leans on each word onset."""
    x, y, z = pos
    tw = talk_windows(t0, t1)
    words = [round(wd["s"], 3) for wd in WORDS if any(a_ <= wd["s"] <= b_ for a_, b_ in tw)]
    w.glb(oid, OMINO, fit=height, pos=(x, -8.0, z), rot_y=rot, talk=[list(v) for v in tw], env=[60, ENV], words=words, bob=round(height * 0.03, 4),
          move=[(t0, 0.35, pos, "out"), (t1, 0.01, (x, -8.0, z), "linear")])
    d_ = height * 2.6
    ZOOMS.append(((x + math.sin(rot) * d_, y + height * 0.72, z + math.cos(rot) * d_), (x, y + height * 0.55, z), t0, DIVE[k], t0 + 0.95))


me("me1", (-3.12, 0.9, 0.42), T_D1 + 1.15, T_MAP2 + 0.1, rot=0.35, height=0.3, k=1)
me("me2", (1.72, 0.915, 0.95), T_D2 + 1.15, T_MAP3 + 0.1, rot=-0.5, height=0.3, k=2)
me("me3", (2.72, 0.6, 1.5), T_D3 + 1.15, T_MAP4 + 0.1, rot=-0.45, height=0.3, k=3)
me("me4", (0.0, 0.915, 1.5), T_D4 + 1.15, T_MAP5 + 0.1, rot=0.15, height=0.34, k=4)
me("me5", (-0.15, 0.0, 3.15), T_D5 + 1.5, T_SIGN + 0.3, rot=0.2, height=0.55, k=5)

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
    zt = [z[2] for z in ZOOMS]
    _calls[:] = [c for c in _calls if c[0] in zt or not any(z - 0.2 <= c[0] <= z + 0.1 for z in zt)]     # the narrator zoom wins over a story cam that lands right on it
    _calls.sort(key=lambda c: c[0])
    for i, (t, d, pos, look, ease) in enumerate(_calls):
        nxt = _calls[i + 1][0] if i + 1 < len(_calls) else 1e9
        dd = min(d, nxt - t - 0.02)
        if dd < 0.25:
            print("  cam skipped %.2f (no room)" % t); continue
        if dd < d - 0.01: print("  cam trim %.2f: %.2f -> %.2f" % (t, d, dd))
        _cam(pos, look, t=t, d=dd, ease=ease)


w.cam = _camx
for _p, _l, _t, _dv, _t2 in ZOOMS:
                                                                       # narrator zoom, then cut to the topic
    w.cam(_p, _l, t=_t, d=0.35, ease="glide", raw=True)
    w.cam(_dv[0], _dv[1], t=_t2, d=0.4, ease="glide")
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
w.big(-0.3, 3.6, "Quanto costa|lanciare un *pantalone*?", top=250, size=80)
w.big(t10 - 0.2, T_MAP5 + 0.2, "*10*, poi *20*|non cento", top=250, size=88)
chunks = [c for c in chunks if not (c[0] < 3.6 or (c[0] < T_MAP5 + 0.2 and c[1] > t10 - 0.2) or c[0] >= at("scrivi") - 0.05)]
w.captions(chunks, top=1180, size=96)


def _extra(path):
    p = open(path, encoding="utf-8").read()
    css = ("<style>#cost{position:absolute;left:0;right:0;top:118px;text-align:center;opacity:0;pointer-events:none;z-index:60}"
           "#cost span{display:inline-block;padding:16px 32px;border-radius:999px;background:rgba(22,18,14,.72);color:#fbf7ee;font:600 40px/1.1 Inter,'Segoe UI',sans-serif;letter-spacing:-.01em}"
           "#cost i{font-family:'Playfair Display',Georgia,serif;font-weight:500;color:#ffb48f;font-style:italic}</style></head>")
    js = ("<div id='cost'><span>il mio costo: <i id='costv'></i></span></div>"
          "<script>(function(){var S=%s,OUT=%.3f;window.addEventListener('hf-seek',function(e){var t=e.detail.time,el=document.getElementById('cost'),v=document.getElementById('costv'),k=-1;"
          "for(var i=0;i<S.length;i++)if(t>=S[i][0])k=i;var a=k<0?0:Math.min(1,(t-S[0][0])/0.25,(OUT-t)/0.25);el.style.opacity=Math.max(0,a);"
          "if(k>=0&&v.textContent!==S[k][1]){v.textContent=S[k][1];}var p=k>=0?Math.min(1,(t-S[k][0])/0.2):1;el.style.transform='scale('+(1+0.12*Math.sin(Math.PI*p))+')';});})();</script></body>"
          ) % (json.dumps(PILL), at("scrivi") - 0.2)
    open(path, "w", encoding="utf-8").write(p.replace("</head>", css, 1).replace("</body>", js, 1))


if __name__ == "__main__":
    out = os.path.join(HERE, "comp")
    print(World3D.page(out, [w], duration=DUR)); _extra(os.path.join(out, "index.html"))
    os.makedirs(os.path.join(out, "img"), exist_ok=True); shutil.copy(os.path.join(HERE, "assets", "me.png"), os.path.join(out, "img", "me.png")); print("built")
