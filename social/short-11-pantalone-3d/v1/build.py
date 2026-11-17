# Short #11 "Ho dato un disegno a un'AI e mi ha restituito un pantalone 3D" (17-18/11/2026): the Inverso sample room at night (same world as Short #3), one hero object (the toy trouser on a pedestal),
# four steps (scheda -> 4 viste -> 3D -> in scena) and the narrator (speech-driven performance + jaw) inside the scene.
import json, math, os, re, shutil, sys
SK = "D:/ClaudeCodeTest/.claude/skills/fashion-3d"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SK + "/engine"); sys.path.insert(0, HERE)
from world3d import World3D
import room
PI = math.pi
WORDS = json.load(open(HERE + "/words.json", encoding="utf-8"))
JAW = json.load(open(HERE + "/jaw.json"))
norm = lambda s: re.sub(r"[^\w]", "", s.lower().split("'")[-1])


def at(word, n=1, after=0.0):
    k = 0
    for x in WORDS:
        if x["s"] >= after and norm(x["w"]) == norm(word):
            k += 1
            if k == n: return round(x["s"], 2)
    raise KeyError(word)


def end(word, n=1, after=0.0):
    k = 0
    for x in WORDS:
        if x["s"] >= after and norm(x["w"]) == norm(word):
            k += 1
            if k == n: return round(x["e"], 2)
    raise KeyError(word)


DUR = 36.5
F = "D:/ClaudeCodeTest/videos/_bench/assets3d/finali/"
TROUSER = F + "pantalone.glb"
OMINO = "D:/ClaudeCodeTest/videos/_bench/short11/assets/narratore-perf.glb"
w = World3D("s", 0.0, DUR, fov=42, w=1080, h=1920, fade=0.4)
w.shutter(0.5)
GESSO, SABBIA, RUGGINE, BOSCO = "#EFE9DD", "#B9AE98", "#8A4B2D", "#2F3A2E"

# ---- beats (all hang on the voice)
T_SCHEDA = at("parti") - 0.15                                 # 4.5   step 1: the sheet (drawing desk)
T_VISTE = at("poi") - 0.15                                    # 10.3  step 2: four views (photo set)
T_3D = at("le", 1, 15.0) + 0.05                               # 15.6  step 3: the 3D model (hero pedestal)
T_SCENA = at("e", 1, 21.0) - 0.1                              # 21.3  step 4: in the scene (turn it)
T_NON = at("non", 1, 20.0)                                    # 26.0  "Non ho niente da venderti"
T_COMP = at("video")                                          # 29.8  "Il video completo..."
T_CHE = at("che", 1, 31.0)                                             # 31.9  "Che colore lo vuoi?"
room.furnish(w)

# ---- hero: the toy trouser on a turning pedestal on the green rug
HP = (1.0, 0.0, 2.6)
w.solid("ped", "cyl", (HP[0], 0.15, HP[2]), (0.7, 0.30), color=GESSO, rough=0.7)
w.solid("pedtop", "cyl", (HP[0], 0.31, HP[2]), (0.62, 0.02), color=RUGGINE, rough=0.6)
R0 = 0.25
w.glb("tr", TROUSER, fit=0.86, pos=(HP[0], 0.32, HP[2]), rot_y=R0, double=True,
      turn=[(0.0, 4.4, R0 + 1.3, "glide"), (T_3D, 1.4, R0, "glide"), (at("girare", 1, 20.0), 2.0, R0 + 2 * PI, "hand"), (at("dietro", 2) + 0.1, 1.0, R0 + 3 * PI, "hand"), (T_NON, 3.8, R0 + 4 * PI, "glide")])

# ---- step 1: the sheet on the drawing desk (pencil writes it)
S1 = (-2.5, 0.9, 0.2)
w.prop("sketchdraw", "sk", (S1[0], 0.905, S1[2]), (0.55, 0.78), rot_y=0.15, t=T_SCHEDA, reveal=[at("verde") - 0.2, end("parole") - 0.2])
w.card("cscheda", (-1.85, 1.38, 0.8), w=0.78, h=0.46, text="*La scheda*", sub="verde oliva · vita alta · pieghe doppie", rot_y=-0.3, color=GESSO, t=at("scheda") - 0.1,
       move=[(T_VISTE + 0.15, 0.01, (-1.85, -5.0, 0.8), "linear")])

# ---- step 2: four views, standing in a row in front of the photo set
S3 = (3.5, 0.0, 0.5)
VIEWS = [("fronte", "davanti", at("quattro") - 0.05), ("retro", "dietro", at("quattro") + 0.15), ("left", "sinistra", at("quattro") + 0.35), ("right", "destra", at("quattro") + 0.55)]     # the four cards pop right after "Quattro viste"
for i, (f_, lab_, t_) in enumerate(VIEWS):                       # a 2 x 2 grid: portrait frame, so the four cards stand in a block, not in a row
    x_ = S3[0] + (-0.23 if i % 2 == 0 else 0.23); y_ = 1.85 if i < 2 else 1.0
    w.card("view%d" % i, (x_, y_, S3[2] + 0.75), w=0.40, h=0.74, img="img/pantalone-%s.png" % f_, text="*%s*" % lab_, rot_y=0.0, color=GESSO, t=t_,
           move=[(T_3D, 0.01, (x_, -5.0, S3[2] + 0.75), "linear")])

# ---- the logo sign for the end card (drops in with "esce", flips = INVERSO)
ENDS = (-0.25, 0.0, 3.0)
T_SIGN = at("esce") - 0.5
w.prop("logosign", "totem", (ENDS[0], -6.0, ENDS[2]), (1.0, 0.31), rot_y=0.25, height=0.78, flips=[[end("commenti") + 0.35, 1.1, PI]],
       move=[(T_SIGN, 0.01, (ENDS[0], 3.6, ENDS[2]), "linear"), (T_SIGN + 0.02, 0.55, ENDS, "in")])
w.leak(T_3D - 0.1, 0.9)

# ---- NARRATOR: the speech-driven performance (one long clip) + the jaw, standing inside the scene
TAN = 0.49866
_dist = lambda vis_h: round(vis_h / TAN, 3)


def me(oid, pos, t0, t1, rot=0.0, height=0.2):
    x, y, z = pos
    w.glb(oid, OMINO, fit=height, pos=(x, -8.0, z), rot_y=rot, segs=[[0.0, DUR + 1.0, 0, 0.0, 1.0]], segFade=0.35, clipSpeed=1.0, bob=0, jaw=[60, JAW], jawGain=1.0, recv=False,
          move=[(t0, 0.35, pos, "out"), (t1, 0.01, (x, -8.0, z), "linear")])


_calls = []


def C(t, d, pos, look, ease="hand", hero=False):
    _calls.append([t, d, pos, look, ease] + (["hero"] if hero else []))


def _flush():
    _calls.sort(key=lambda c: c[0])
    first = True
    for i, c in enumerate(_calls):
        t, d, pos, look, ease = c[:5]
        nxt = _calls[i + 1][0] if i + 1 < len(_calls) else 1e9
        dd = min(d, nxt - t - 0.02)
        if dd < 0.25:
            print("  cam skipped %.2f (no room)" % t); continue
        if dd < d - 0.01: print("  cam trim %.2f: %.2f -> %.2f" % (t, d, dd))
        w.cam(pos, look, t=t, d=dd, ease=ease)


w.cam((1.0, 0.95, 4.5), (1.0, 0.75, 2.6))                                                   # frame 1: the trouser, close, already turning
C(0.05, 2.3, (2.1, 1.0, 4.0), (1.0, 0.75, 2.6), "glide")                                    # orbit while "ho dato un disegno a un'AI"
C(at("pantalone"), 1.4, (1.2, 0.8, 3.7), (1.0, 0.78, 2.6), "hand")                          # push in on "pantalone"
C(at("3d"), 0.5, (0.2, 1.25, 4.4), (1.0, 0.8, 2.6), "hand")
C(T_SCHEDA, 1.1, (-2.1, 1.75, 2.7), (-2.3, 1.1, 0.4), "glide")                              # dive to the desk: paper + the sheet card
C(at("verde") - 0.4, 1.4, (-2.35, 1.55, 1.0), (-2.5, 0.92, 0.25), "glide")                  # top view: the pencil writes
C(at("alta") - 0.3, 1.3, (-3.0, 1.15, 0.9), (-2.5, 0.95, 0.2), "hand")                       # low and side
C(at("scrivi") - 0.2, 1.1, (-2.1, 1.6, 2.8), (-2.3, 1.1, 0.4), "glide")                      # wide again: paper, card, narrator
C(T_VISTE, 1.1, (4.2, 1.5, 4.2), (3.5, 1.35, 1.2), "glide")                                  # the photo set
C(at("immagine") - 0.4, 1.0, (3.0, 1.4, 3.9), (3.5, 1.3, 1.25), "hand")
C(at("quattro") - 0.3, 1.4, (3.5, 1.35, 4.1), (3.5, 1.3, 1.25), "hand")
C(at("dietro") - 0.6, 1.9, (3.55, 1.3, 3.5), (3.5, 1.3, 1.25), "hand")
C(T_3D, 1.2, (1.0, 1.15, 4.8), (1.0, 0.8, 2.6), "glide")                                    # back to the hero: it becomes 3D
C(at("modello") - 0.3, 1.5, (1.9, 0.95, 3.8), (1.0, 0.7, 2.6), "hand")
C(at("pieghe", 1, 19.0) - 0.5, 1.6, (1.15, 1.0, 3.4), (1.0, 0.9, 2.6), "hand")               # close on the waist: the pleats
C(at("sistemare") + 0.2, 0.8, (1.0, 1.1, 4.7), (1.0, 0.8, 2.6), "glide")
C(at("girare", 1, 20.0) - 0.15, 1.9, (2.3, 1.1, 3.9), (1.0, 0.8, 2.6), "glide")                      # orbit during the 360
C(at("dietro", 2) - 0.25, 1.4, (1.1, 0.9, 4.0), (1.0, 0.8, 2.6), "hand")                    # "da dietro": push on the back
# narrator placement: automatic, the best spot visible from the side of the shots of each station
V4 = {1: ((0.3, 0.0, 2.95), 0.50), 2: ((-3.12, 0.9, 0.42), 0.30), 3: ((2.7, 0.0, 2.2), 0.50), 4: ((0.3, 0.0, 2.95), 0.55)}
WIN = {1: (0.0, T_SCHEDA), 2: (T_SCHEDA, T_VISTE), 3: (T_VISTE, T_3D), 4: (T_3D, DUR)}


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
for k_ in (2, 3, 4):
    (bx, by, bz), hh = V4[k_]; best = None
    for dx_ in [i * 0.15 for i in range(-5, 6)]:
        for dz_ in [i * 0.15 for i in range(-4, 5)]:
            P = (bx + dx_, by + hh * 0.5, bz + dz_); sc_ = _score(P, k_)
            if best is None or sc_ > best[0]: best = (sc_, (bx + dx_, by, bz + dz_))
    PLACE[k_] = best[1]; print("  narrator %d at (%.2f, %.2f, %.2f) score %.1f" % (k_, *best[1], best[0]))
for k_ in range(2, 5):
    P = PLACE[k_]; hh = V4[k_][1]; cams_ = [c for c in _calls if len(c) <= 5 and WIN[k_][0] <= c[0] <= WIN[k_][1]]
    mx_, mz_ = (sum(c[2][0] for c in cams_) / len(cams_), sum(c[2][2] for c in cams_) / len(cams_)) if cams_ else (P[0], P[2] + 3)
    rot_ = math.atan2(mx_ - P[0], mz_ - P[2]) * 0.9
    if k_ == 3: P = (3.15, 0.0, 2.65)                      # fixed: bottom-left of the four cards
    if k_ == 4: P, rot_ = (0.7, 0.0, 3.4), 0.2              # in front of the pedestal, a little to the left: the trouser stays behind him in the close-ups
    PLACE[k_] = (P, rot_)
    me("nar%d" % k_, P, (WIN[k_][0] + 0.9) if k_ < 4 else T_NON - 0.75, (WIN[k_][1] + 0.1) if k_ < 4 else DUR + 1.0, rot=rot_, height=hh)
# close-ups on the sentences that matter: "Non ho niente da venderti, sono uno studente..." and the final question
P4, R4 = PLACE[4]; hh = V4[4][1]; d_ = 1.55 * hh
s_, e_ = T_NON, end("tutto")
look0 = (P4[0], P4[1] + 0.60 * hh, P4[2])
C(s_ - 0.55, 0.45, (P4[0] + math.sin(R4) * d_, P4[1] + 0.60 * hh, P4[2] + math.cos(R4) * d_), look0, "glide", hero=True)
d1 = d_ * 0.9
C(s_ + 0.9, e_ - s_ - 1.1, (P4[0] + math.sin(R4) * d1, P4[1] + 0.60 * hh, P4[2] + math.cos(R4) * d1), look0, "glide", hero=True)
C(T_COMP - 0.15, 1.2, (0.2, 1.45, 8.5), (0.2, 0.85, 2.8), "glide")                          # widen: the sign drops with the pedestal behind him
C(T_CHE - 0.5, 0.6, (P4[0], P4[1] + 0.5 * hh, P4[2] + 3.2 * hh), (P4[0], P4[1] + 0.95 * hh, P4[2]), "glide", hero=True)
C(T_CHE + 1.5, 4.0, (P4[0], P4[1] + 0.5 * hh, P4[2] + 3.6 * hh), (P4[0], P4[1] + 1.0 * hh, P4[2]), "glide", hero=True)
T_ENDW = end("commenti") + 0.1
C(T_ENDW, 1.9, (0.2, 1.25, 8.5), (0.2, 0.8, 2.9), "glide")                                   # the end card: everything in one frame, the INVERSO sign turns the right way round
C(T_ENDW + 2.0, 2.0, (0.2, 1.1, 8.0), (0.2, 0.8, 2.9), "hand")
_flush()
w.dof(0.0, DUR, aperture=0.003)

# ---- the step counter (a pill that follows the PHASE) + text on screen the whole video
PILL = [(T_SCHEDA, "1/4 · la scheda"), (T_VISTE, "2/4 · l'immagine"), (T_3D, "3/4 · il 3D"), (T_SCENA, "4/4 · in scena")]
nm = lambda t: t.lower().strip(".,:?!")
KEY = {"disegno", "pantalone", "scheda", "immagine", "quattro", "3d", "perfetto", "girare", "dietro", "cliente", "venderti", "studente", "documento", "dicembre", "colore", "commenti", "un'ai"}
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
T_HOOK_END = at("parti") - 0.1
w.big(-0.3, T_HOOK_END, "Un *disegno*|diventa un|*pantalone* 3D", top=250, size=88)
w.big(T_CHE - 0.2, DUR, "Che *colore* lo vuoi?|*oliva* · *ruggine* · *gesso*", top=215, size=72)
chunks = [c for c in chunks if not (c[0] < T_HOOK_END or c[0] >= T_CHE - 0.05)]
w.captions(chunks, top=340, size=96)


def _extra(path):
    p = open(path, encoding="utf-8").read()
    css = ("<style>#cost{position:absolute;left:0;right:0;top:118px;text-align:center;opacity:0;pointer-events:none;z-index:60}"
           "#cost span{display:inline-block;padding:16px 32px;border-radius:999px;background:rgba(22,18,14,.72);color:#fbf7ee;font:600 40px/1.1 Inter,'Segoe UI',sans-serif;letter-spacing:-.01em}"
           "#cost i{font-family:'Playfair Display',Georgia,serif;font-weight:500;color:#ffb48f;font-style:italic}</style></head>")
    js = ("<div id='cost'><span>passaggi: <i id='costv'></i></span></div>"
          "<script>(function(){var S=%s,OUT=%.3f;window.addEventListener('hf-seek',function(e){var t=e.detail.time,el=document.getElementById('cost'),v=document.getElementById('costv'),k=-1;"
          "for(var i=0;i<S.length;i++)if(t>=S[i][0])k=i;var a=k<0?0:Math.min(1,(t-S[0][0])/0.25,(OUT-t)/0.25);el.style.opacity=Math.max(0,a);"
          "if(k>=0&&v.textContent!==S[k][1]){v.textContent=S[k][1];}var p=k>=0?Math.min(1,(t-S[k][0])/0.2):1;el.style.transform='scale('+(1+0.12*Math.sin(Math.PI*p))+')';});})();</script></body>"
          ) % (json.dumps(PILL), T_NON - 0.2)
    open(path, "w", encoding="utf-8").write(p.replace("</head>", css, 1).replace("</body>", js, 1))


if __name__ == "__main__":
    out = os.path.join(HERE, "comp")
    print(World3D.page(out, [w], duration=DUR)); _extra(os.path.join(out, "index.html"))
    os.makedirs(os.path.join(out, "img"), exist_ok=True)
    G = "D:/ClaudeCodeTest/social/assets-3d/gemini/"
    for f_, src_ in (("fronte", "01-pantalone-d-fronte.png"), ("retro", "01-pantalone-d-retro.png"), ("left", "01-pantalone-d-left.png"), ("right", "01-pantalone-d-right.png")):
        shutil.copy(G + src_, os.path.join(out, "img", "pantalone-%s.png" % f_))
    print("built")
