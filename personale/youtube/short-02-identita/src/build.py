# Short #2 "Il nome del mio brand ha tre significati" (13/11/2026): the Inverso studio at night, three stations + a map + a diagram on the floor.
# Everything hangs on the words of the voice (words.json). Same method as Short #1 (build.py there), new world (room.py here, atelier-studio.js in the skill).
import json, math, os, re, sys
SK = "D:/ClaudeCodeTest/.claude/skills/youtube-edit"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SK + "/formats"); sys.path.insert(0, HERE)
from world3d import World3D
import room

WORDS = json.load(open(HERE + "/words.json", encoding="utf-8"))
norm = lambda s: re.sub(r"[^\w]", "", s.lower().split("'")[-1])


def at(word, n=1, after=0.0):
    k = 0
    for x in WORDS:
        if x["s"] >= after and norm(x["w"]) == norm(word):
            k += 1
            if k == n:
                return round(x["s"], 2)
    raise KeyError(word)


def end(word, n=1):
    k = 0
    for x in WORDS:
        if norm(x["w"]) == norm(word):
            k += 1
            if k == n:
                return round(x["e"], 2)
    raise KeyError(word)


VO_END = WORDS[-1]["e"]
DUR = round(VO_END + 2.6, 2)
PW, PH = 1080, 1920
RED = "#b8432a"
w = World3D("s", 0.0, DUR, fov=42, w=PW, h=PH, fade=0.4)
w.shutter(0.5)

# ------------------------------------------------------------------ the beats
T_FLIP = at("inverso") - 0.2                    # "si chiama Inverso": the totem turns upright, top to bottom
T_MAP1 = at("nasconde") - 0.25                  # up to the map: three stations
T_D1 = at("uno") - 0.5                          # dive 1: the work table (the wrong side)
T_TURN = at("rovescio", 2) - 0.3                # the panel turns over
T_300 = at("un") - 0.2                          # "Un capo da 300 euro con il rovescio sporco"
T_X = at("sbagliato") - 0.1
T_BOARD = at("per") - 0.25                      # "Per questo ti mostro il mio rovescio": the cork board
T_MAP2 = end("tessuto") + 0.12
T_D2 = at("contrario") - 0.5                    # dive 2: the rail
T_CLEAR = at("volta") - 0.7                    # "Un capo per volta": the rail empties
T_MESI = at("mesi") - 0.35
T_MAP3 = end("fatto", 2) + 0.12
T_D3 = at("alle") - 0.45                        # dive 3: the shoe boxes
T_DROP = at("avevo") + 0.05                     # "Ne avevo una": five boxes go
T_DIA = at("servono") - 0.15                    # up to the diagram on the floor
T_END = at("questo", 2) - 0.3
FLY = [[T_MAP1, T_D1 + 1.1], [T_MAP2, T_D2 + 1.1], [T_MAP3, T_D3 + 1.1], [T_DIA - 0.1, T_END + 1.2]]
w.board_cards = [dict(x=-0.4, y=-0.02, w=0.4, h=0.3, text="ore di studio", lines=True, rot=-0.05, t=at("ore") - 0.05),
                 dict(x=0.02, y=-0.42, w=0.38, h=0.44, big="v1", text="cartamodello", sub="da rifare", strike=True, rot=0.06, t=at("errori") - 0.05),
                 dict(x=0.42, y=0.04, w=0.32, h=0.24, swatch="#6f7452", rot=-0.03, t=at("costa") - 0.15),
                 dict(x=0.44, y=-0.4, w=0.3, h=0.2, big="€ / m", text="drill", rot=0.04, t=at("costa") + 0.1)]
w.clock_spin = [[T_MESI + 0.3, end("settimane") + 0.2, 6]]
room.furnish(w, hide=FLY)
w.leak(T_D1 - 0.05, 1.1)

# ------------------------------------------------------------------ the objects
TOT = (0.4, 0.0, 1.4)
w.prop("wordblocks", "totem", TOT, (0.3,), rot_y=0.0, text="INVERSO", flips=[[T_FLIP, 0.09, 0.62, math.pi], [at("inverso", 3) - 0.25, 0.07, 0.8, 2 * math.pi]])
PANEL, DIRTY = (-2.28, 0.9, 0.48), (-1.66, 0.9, 0.5)
w.prop("seampanel", "panel", PANEL, (0.5, 0.62), rot_y=0.08, color="#6f7452", flip=[T_TURN, T_TURN + 0.95])
w.prop("seampanel", "dirty", DIRTY, (0.5, 0.62), rot_y=-0.1, color="#6f7452", dirty=True, flipped=True)
w.prop("crossmark", "xmark", (DIRTY[0] + 0.03, 0.912, DIRTY[2] + 0.05), (0.2,), rot_y=-0.1, show=T_X, out=T_BOARD + 0.6)
RAIL = (2.9, 0.0, -1.0)
w.prop("fastrail", "rail", RAIL, (4.4, 1.75), span=[T_D2 + 0.15, T_CLEAR], clear=T_CLEAR, speed=3.4)
HERO_Y = 0.6
w.trouser("hero", pos=(2.9, 30.0, -1.0), rot_y=-0.25, color="#6f7452", hang=0.004, hi=True, loops=False, cuff=False, bp=1, bpbutton=False,
          move=[(T_CLEAR - 0.6, 0.01, (1.35, HERO_Y, -1.0), "linear"), (T_CLEAR + 0.35, 1.25, (2.9, HERO_Y, -1.0), "glide")], turn=[(T_CLEAR + 1.6, 6.0, 0.2, "smooth")])
BOX = (3.45, 0.55, 1.35)
w.prop("shoeboxes", "boxes", BOX, show=[at("scarpa") - 0.15, 0.11], drop=T_DROP, keep=1, price="150 €")
w.prop("sneaker", "shoe", (BOX[0], BOX[1] + 0.134, BOX[2] - 0.01), rot_y=-0.35, t=T_DROP + 0.55)
AX = (-1.3, 0.02, 3.4)
w.solid("rugdia", "box", (AX[0], 0.006, AX[2]), (4.3, 0.012, 1.45), color="#34402f", rough=0.95)
w.prop("axisline", "axis", AX, (2.6,), draw=[T_DIA + 0.55, T_DIA + 1.35], lt=at("ostentazione") - 0.05, rt=at("flexing") - 0.1,
       puck=[[at("ostentazione") + 0.25, 0.4, 0.1], [at("flexing") + 0.05, 0.85, 0.9], [at("inverso", 2) + 0.1, 0.95, 0.5]], tspin=math.pi / 2, pspin=math.pi)

# ------------------------------------------------------------------ the map: three stations and the path
ST = {1: (-2.05, 1.35, "rovescio"), 2: (2.9, 0.1, "fretta"), 3: (3.45, 2.2, "")}
pop = [at("tre") - 0.05, at("tre") + 0.3, at("tre") + 0.65]
BADGES = {"st": (pop, T_D1 + 0.25), "m2st": ([T_MAP2 + 0.15, T_MAP2 + 0.25, T_MAP2 + 0.35], T_D2 + 0.25), "m3st": ([T_MAP3 + 0.15, T_MAP3 + 0.25, T_MAP3 + 0.35], T_D3 + 0.25)}
for pre, (shows, out) in BADGES.items():
    for n, (x, z, word) in ST.items():
        w.prop("floorbadge", pre + "%d" % n, (x, 0.02, z), (0.78,), rot_y=math.pi / 2, n=n, word=word, ring=RED, show=shows[n - 1], out=out)
SEG = {1: [(-2.05, 1.35), (-1.3, 2.05), (0.0, 2.25), (1.35, 1.95), (2.1, 1.1), (2.6, 0.45), (2.9, 0.1)],
       2: [(2.9, 0.1), (2.3, 0.75), (2.25, 1.85), (2.75, 2.25), (3.45, 2.2)]}
for nm, k, t0, t1, out in [("path1", 1, T_MAP2 + 0.5, T_MAP2 + 1.3, T_D2 + 0.25), ("path1b", 1, T_MAP3 + 0.1, T_MAP3 + 0.3, T_D3 + 0.25), ("path2", 2, T_MAP3 + 0.5, T_MAP3 + 1.2, T_D3 + 0.25)]:
    w.prop("pathdots", nm, (0, 0.035, 0), pts=[[x, 0, z] for x, z in SEG[k]], gap=0.13, r=0.045, flat=True, color=RED, span=[t0, t1], out=out)

# ------------------------------------------------------------------ the camera
CAMS = []


def C(t, d, pos, look, ease="hand"):
    CAMS.append((round(t, 2), d, pos, look, ease))


MAP = ((3.45, 12.5, 1.15), (0.45, 0.0, 1.05))
DIA = ((AX[0] + 1.0, 6.0, AX[2]), (AX[0] - 0.2, 0.0, AX[2]))
w.cam((1.45, 0.95, 4.55), look=(0.4, 1.28, 1.4))                                              # frame 1: the totem reads upside down
C(0.05, T_FLIP + 0.9, (1.15, 1.15, 4.1), (0.4, 1.3, 1.4), "out")                                 # push while the cubes turn
C(at("nome") - 0.1, at("nasconde") - at("nome") - 0.25, (-0.45, 1.55, 3.85), (0.4, 1.25, 1.4), "glide")   # orbit to the other side
C(T_MAP1, 1.6, MAP[0], MAP[1], "glide")                                                         # up: the map, three stations
C(T_D1, 1.05, (-2.27, 1.52, 1.32), (-2.28, 0.9, 0.46), "glide")                                 # dive 1: the right side of the panel
C(at("dritto") - 0.25, 1.1, (-2.33, 1.2, 0.72), (-2.3, 0.9, 0.36))                               # macro: the welt pocket
C(T_TURN - 0.05, 1.2, (-2.2, 1.62, 1.2), (-2.28, 0.9, 0.46), "glide")                           # back up while it turns over
C(at("cuciture") - 0.25, 1.0, (-2.37, 1.16, 0.8), (-2.36, 0.9, 0.45))                           # macro: the pressed-open seams, overlocked
C(at("nessuno") - 0.3, 1.0, (-2.24, 1.12, 0.52), (-2.27, 0.9, 0.2))                             # the woven label in the waistband
C(T_300, 1.0, (-1.62, 1.5, 1.32), (-1.66, 0.9, 0.5), "glide")                                   # the dirty one
C(T_X - 0.15, 0.8, (-1.64, 1.36, 1.1), (-1.66, 0.9, 0.48))
C(T_BOARD, 1.25, (-1.33, 1.58, -0.95), (-1.35, 1.48, -3.0), "glide")                               # the cork board: hours, mistakes, cost
C(at("errori") - 0.2, 1.8, (-1.29, 1.52, -1.4), (-1.33, 1.47, -3.0), "glide")
C(T_MAP2, 1.25, MAP[0], MAP[1], "glide")                                                        # the map: 1 -> 2
C(T_D2, 1.1, (2.62, 1.38, 1.05), (2.9, 1.28, -1.0), "glide")                                    # dive 2: the fast rail
C(T_CLEAR + 0.3, 1.3, (2.82, 1.32, 0.75), (2.9, 1.2, -1.0), "glide")                            # one garment
C(T_MESI, 1.1, (3.05, 1.3, 1.2), (2.42, 1.5, -2.0))                                         # the clock races behind it
C(at("quando") - 0.25, 1.0, (3.0, 1.66, -0.25), (2.9, 1.55, -1.0))                              # macro: the waist
C(at("sono") - 0.2, 1.6, (2.15, 1.55, 3.2), (2.9, 1.15, -1.0), "glide")                          # wide: an empty rail, one trouser
C(T_MAP3, 1.25, MAP[0], MAP[1], "glide")                                                        # the map: 2 -> 3
C(T_D3, 1.1, (2.8, 1.18, 2.25), (3.45, 0.64, 1.3), "glide")                                   # dive 3: the shoe boxes
C(T_DROP - 0.1, 1.0, (3.45, 0.95, 2.35), (3.45, 0.78, 1.35))                                   # one
C(at("imparato") - 0.6, 1.1, (3.88, 0.86, 1.88), (3.45, 0.74, 1.33), "glide")                    # macro: the sneaker
C(at("scelgono") - 0.3, 2.0, (2.98, 0.95, 1.98), (3.45, 0.74, 1.33), "glide")                    # round it
C(T_DIA, 1.5, DIA[0], DIA[1], "glide")                                                          # up: the diagram
C(at("inverso", 2) + 0.45, 1.0, (AX[0] + 0.85, 3.0, AX[2]), (AX[0] + 0.35, 0.0, AX[2]), "glide")        # push in on the puck: Inverso, in the middle
C(T_END, 1.5, (1.5, 1.3, 4.55), (0.4, 1.28, 1.4), "glide")                                      # back to the totem
C(at("studente") - 0.2, 2.6, (-0.55, 1.5, 4.1), (0.4, 1.25, 1.4), "glide")
C(at("documentando") - 0.2, 3.2, (1.2, 2.6, 6.2), (0.6, 1.0, -0.4), "glide")                     # pull back: the whole studio
CAMS.sort()
for k, (t, d, pos, look, ease) in enumerate(CAMS):
    nxt = CAMS[k + 1][0] if k + 1 < len(CAMS) else DUR
    d2 = min(d, nxt - t - 0.03)
    if d2 < 0.35:
        print("  SKIPPED move at %.2f (no room: %.2f)" % (t, d2)); continue
    if d2 < d - 0.01:
        print("  move at %.2f shortened %.2f -> %.2f" % (t, d, d2))
    w.cam(pos, look=look, t=t, d=d2, ease=ease)
    gap = nxt - (t + d2) - 0.06
    if gap > 0.35:                                     # never still: a slow drift toward the subject until the next move
        dx, dy, dz = look[0] - pos[0], look[1] - pos[1], look[2] - pos[2]
        dist = math.sqrt(dx * dx + dy * dy + dz * dz); hl = math.hypot(dx, dz) or 1.0
        f = min(0.07, 0.022 * gap); lx, lz = -dz / hl * dist * f * 0.6, dx / hl * dist * f * 0.6
        if pos in (MAP[0], DIA[0]): lx, lz, f = 0.0, 0.0, min(0.05, 0.015 * gap)
        p2 = (pos[0] + dx * f + lx, pos[1] + dy * f, pos[2] + dz * f + lz); l2 = (look[0] + lx, look[1], look[2] + lz)
        w.cam(p2, look=l2, t=t + d2 + 0.03, d=gap, ease="linear")

# ------------------------------------------------------------------ labels (pinned on the objects)
L = w.label
names = {1: "il *rovescio*", 2: "la *fretta*", 3: "il più *personale*"}
for n in ST:
    L("st%d" % n, (0, 0, 0), "%d · %s" % (n, names[n]) if n < 3 else "3 · *?*", t=pop[n - 1] + 0.05, out=T_D1 - 0.1, anchor="st%d" % n, dx={1: -170, 2: -170, 3: 40}[n], dy={1: 90, 2: -140, 3: -140}[n])
L("st3", (0, 0, 0), "3 · il più *personale*", t=at("personale") - 0.1, out=T_D1 - 0.1, anchor="st3p", dx=-120, dy=60)
L("m2st2", (0, 0, 0), "2 · la *fretta*", t=T_MAP2 + 1.25, out=T_D2 - 0.05, anchor="st2b", dx=-170, dy=-140)
L("m3st3", (0, 0, 0), "3 · la scarpa", t=T_MAP3 + 1.2, out=T_D3 - 0.05, anchor="st3b", dx=-150, dy=-140)
L("panel", (-0.04, 0.012, -0.14), "Tasca *a filo*", t=at("dritto") + 0.75, out=T_TURN - 0.1, anchor="tasca", sub="bottone in corno", dx=-330, dy=-300)
L("panel", (-0.09, 0.006, 0.05), "*Sorfilate*", t=at("cuciture") + 0.85, out=at("nessuno") - 0.35, anchor="sorf", sub="e stirate aperte", dx=-300, dy=-330)
L("panel", (0.0, 0.006, -0.28), "L'etichetta *Inverso*", t=at("nessuno") + 0.55, out=T_300 + 0.1, anchor="etichetta", dx=-310, dy=-380)
L("dirty", (0.09, 0.006, 0.0), "Fili *liberi*", t=at("rovescio", 3) + 0.25, out=T_X + 0.05, anchor="fili", sub="margini non rifiniti", dx=-380, dy=-330)
L("hero", (0.01, 0.98, 0.135), "Drop 1 · *il pantalone*", t=T_CLEAR + 1.3, out=T_MESI - 0.05, anchor="drop1", sub="cotone drill verde oliva", dx=-330, dy=-430)
L("shoe", (0.0, 0.1, 0.0), "*Una* scarpa", t=at("imparato") + 0.1, out=at("scelgono") - 0.2, anchor="unascarpa", sub="portata fino in fondo", dx=-200, dy=-360) if False else None
L("axis", (-1.6, 0.0, 0.0), "chi *ha*", t=at("ostentazione") + 0.6, out=T_END - 0.1, anchor="chiha", dx=150, dy=-30)
L("axis", (1.6, 0.0, 0.0), "chi *non ha*", t=at("flexing") + 0.6, out=T_END - 0.1, anchor="chinonha", dx=150, dy=-30)

# ------------------------------------------------------------------ captions + big statements
KEY = {"inverso", "brand", "significati", "personale", "rovescio", "dritto", "cuciture", "margini", "sporco", "sbagliato", "studio", "errori", "tessuto", "fretta", "volta",
       "mesi", "pronto", "io", "strategia", "fatto", "scarpa", "una", "sei", "scelgono", "buone", "niente", "ostentazione", "flexing", "studente", "tutto", "seguimi", "capo"}
chunks, cur = [], []
lower_next = False
for i, x in enumerate(WORDS):
    x = dict(x)
    if lower_next and x["w"][:1].isupper() and x["w"] not in ("Inverso", "Inverso."): x["w"] = x["w"][0].lower() + x["w"][1:]
    lower_next = x["w"].endswith(":")
    cur.append(x)
    brk = x["w"].endswith((".", ":", "?", "!", ",", "...")) or len(cur) >= 3 or sum(len(c["w"]) for c in cur) > 17
    if brk or i == len(WORDS) - 1:
        nxt = WORDS[i + 1]["s"] if i + 1 < len(WORDS) else cur[-1]["e"] + 1.0
        txt = " ".join(c["w"] for c in cur)
        for c in cur:
            if norm(c["w"]) in KEY:
                core = c["w"].rstrip(".,:!?"); txt = txt.replace(c["w"], "*" + core + "*" + c["w"][len(core):], 1); break
        txt = txt.replace("300 euro", "300 €").replace("*300* euro", "*300 €*").replace("150 euro", "150 €").replace("*150* euro", "*150 €*")
        chunks.append((cur[0]["s"], min(nxt - 0.02, cur[-1]["e"] + 0.45), txt.rstrip(".,:").replace("...", "…")))
        cur = []
B = w.big
B(-0.3, end("inverso") + 0.3, "Il mio brand|si chiama *Inverso*", top=230, size=84)
B(at("nasconde"), end("significati") + 0.2, "nasconde|*tre* significati", top=240, size=88)
B(at("un"), end("sporco") + 0.2, "un capo da *300 €*|con il rovescio sporco…", top=250, size=74)
B(at("è", 4) if False else at("sbagliato") - 0.6, end("sbagliato") + 0.35, "…è un capo *sbagliato*", top=250, size=82)
B(at("mesi") - 0.15, end("settimane") + 0.3, "in *mesi*,|non in settimane", top=250, size=88)
B(at("non", 3), end("fatto", 2) + 0.3, "non è una strategia:|*è un fatto*", top=250, size=78)
B(at("scarpa") - 0.25, end("euro", 2) + 0.15, "la scarpa|da *150 €*", top=250, size=88)
B(at("ne"), end("una", 2) + 0.15, "Ne avevo *una*.", top=250, size=96)
B(at("sei") - 0.18, end("sei") + 0.75, "*Non sei.*", top=250, size=110)
B(at("inverso", 2), end("due") + 0.3, "l'*inverso*|di tutti e due", top=230, size=88)
B(at("questo", 2), end("inverso", 3) + 0.25, "Questo è *Inverso*", top=1160, size=86)
B(at("vuoi"), at("seguimi") - 0.02, "Se vuoi vedere nascere|il primo capo…", top=1140, size=70)
B(at("seguimi"), DUR, "*Seguimi*", top=1140, size=104)
SP = w.spans()
chunks = [c for c in chunks if not any(c[0] < b - 0.02 and c[1] > a + 0.02 for a, b in SP)]
starts = sorted([c[0] for c in chunks] + [a for a, b in SP])
chunks = [(a, max(b, min([s for s in starts if s > a + 0.01] + [b + 1.0]) - 0.01), t) for a, b, t in chunks]
for bg in w.bigs:
    nx = [s for s in starts if s > bg[0] + 0.01]
    if nx and nx[0] - bg[1] < 1.0: bg[1] = round(max(bg[1], nx[0] - 0.01), 3)
w.captions(chunks, top=1180, size=96)

# ------------------------------------------------------------------ the counter pill: which meaning we are on (moves with the PHASE)
PHASE = [(T_D1 - 0.1, "1/3", "il rovescio"), (T_D2 - 0.1, "2/3", "la fretta"), (T_D3 - 0.1, "3/3", "il più personale")]
PHASE_OUT = T_END - 0.1


def _extra(path):
    p = open(path, encoding="utf-8").read()
    css = ("<style>.w3-lab{font-size:54px !important;padding:22px 36px !important;border-radius:28px !important}.w3-lab small{font-size:38px !important}"
           ".w3-lab i{font-family:'Instrument Serif','Playfair Display',Georgia,serif !important;font-weight:400 !important;color:#8A4B2D !important;font-size:1.12em}"
           "#pill{position:absolute;left:0;right:0;top:118px;text-align:center;opacity:0;pointer-events:none;z-index:60}"
           "#pill span{display:inline-block;padding:16px 34px;border-radius:999px;background:rgba(14,16,14,.74);color:#fbf7ee;font:600 42px/1.1 'IBM Plex Sans',Inter,sans-serif;letter-spacing:-.005em;border:2px solid rgba(184,67,42,.85)}"
           "#pill b{font-weight:700;color:#ff9f7a;margin-right:14px}#pill i{font-family:'Instrument Serif','Playfair Display',Georgia,serif;font-weight:400;font-size:1.18em;color:#fbf7ee;font-style:italic}</style></head>")
    js = ("<div id='pill'><span><b id='pn'></b><i id='pw'></i></span></div>"
          "<script>(function(){var S=%s,OUT=%.3f;window.addEventListener('hf-seek',function(e){var t=e.detail.time,el=document.getElementById('pill'),k=-1;"
          "for(var i=0;i<S.length;i++)if(t>=S[i][0])k=i;var a=k<0?0:Math.min(1,(t-S[0][0])/0.25,(OUT-t)/0.25);el.style.opacity=Math.max(0,a);"
          "if(k>=0){document.getElementById('pn').textContent='significato '+S[k][1];document.getElementById('pw').textContent=S[k][2];}"
          "var p=k>=0?Math.min(1,(t-S[k][0])/0.22):1;el.style.transform='scale('+(1+0.12*Math.sin(Math.PI*p))+')';});})();</script></body>") % (json.dumps(PHASE), PHASE_OUT)
    p = p.replace("</head>", css, 1).replace("</body>", js, 1)
    open(path, "w", encoding="utf-8").write(p)


if __name__ == "__main__":
    out = os.path.join(HERE, "comp")
    print(World3D.page(out, [w], duration=DUR)); _extra(os.path.join(out, "index.html"))
    print("DUR", DUR, "captions", len(chunks), "cams", len(CAMS))
    print("beats: flip %.2f map1 %.2f d1 %.2f turn %.2f 300 %.2f board %.2f map2 %.2f d2 %.2f clear %.2f map3 %.2f d3 %.2f drop %.2f dia %.2f end %.2f" % (
        T_FLIP, T_MAP1, T_D1, T_TURN, T_300, T_BOARD, T_MAP2, T_D2, T_CLEAR, T_MAP3, T_D3, T_DROP, T_DIA, T_END))
