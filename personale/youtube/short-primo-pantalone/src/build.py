# Short 9:16 "Il mio primo pantalone sembrava una gonna", v4 (14/11/2026): the Autogrill method applied to the detailed atelier.
# One continuous 3D atelier; a MAP of the atelier seen from above (4 numbered stations + a red dotted path that grows at every visit) ties the story together;
# the camera never stops (slow drift between moves); live counters (cost of a mistake, 117 cm); every cue tied to a word of the voiceover (words.json).
import json, math, os, re, sys
SK = "D:/ClaudeCodeTest/.claude/skills/youtube-edit"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SK + "/formats"); sys.path.insert(0, HERE)
from world3d import World3D
from room import furnish

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


def wend(stem, after):                                             # end of the first word containing `stem` after time `after`
    return next(x["e"] for x in WORDS if x["s"] > after and stem in x["w"].lower())


VO_END = WORDS[-1]["e"]
DUR = round(VO_END + 2.6, 2)
PW, PH = 1080, 1920
RED = "#b8432a"                                                    # ruggine, a touch brighter: the path, the counters, the badges' rings
w = World3D("s", 0.0, DUR, fov=42, w=PW, h=PH, fade=0.4)
w.shutter(0.5)

# ------------------------------------------------------------------ the story beats (all from the voice)
T_MAP1 = at("ti") - 0.15                       # "Ti mostro come ci sono arrivato": up to the map
T_D1 = at("Tutto") - 0.55                      # dive to station 1 (the drawing)
T_MAP2 = end("niente") + 0.15                  # after "sbagliare non costa niente": the map again, path 1 -> 2
T_D2 = at("carta") - 0.35
T_COS = at("primo", 2) - 0.25                  # "il primo errore": the COS trouser and the table in one shot
T_MAP3 = end("COS") + 0.1
T_D3 = at("cuce") - 0.2
T_SK = at("più") - 0.1                         # "più che un pantalone ampio, una gonna"
T_SWAP = at("gesso") - 0.55
T_MAP4 = end("finito") + 0.12
T_D4 = at("tessuto", 2) - 0.45
T_END = at("Questo") - 0.2
furnish(w, hide=[[T_MAP1, T_D1 + 1.0], [T_MAP2, T_D2 + 1.0], [T_MAP3, T_D3 + 1.15], [T_MAP4, T_D4 + 1.15]])   # the pendants fade out while the camera flies to the map and back (they crossed the lens)
w.leak(T_D1 - 0.05, 1.1)                       # the film burn on the first dive into the atelier (Jacopo's note on proof 1)

# ------------------------------------------------------------------ the objects
HERO = (3.0, 0.55, -0.4)
w.trouser("toileA", pos=(0.9, 0.55, 0.3), rot_y=0.15, color="#e4dcc6", hang=2.2, hi=True, toile=True, noband=True, bp=0, bulge=[0.05, 0.05], turn=[(0, T_SWAP, 0.35, "smooth")],
          move=[(T_SWAP, 0.01, (0.9, -12.0, 0.3), "linear")])
w.trouser("toileB", pos=(0.9, -12.0, 0.3), rot_y=0.35, color="#e4dcc6", hang=2.2, hi=True, toile=True, noband=True, bp=0, bulge=[0.05, 0.004], chalk=True,
          move=[(T_SWAP, 0.01, (0.9, 0.55, 0.3), "linear")])
w.trouser("cos", pos=(-0.55, 0.55, 1.0), rot_y=0.55, color="#1e1b18", hang=2.2, hi=True, loops=True, cuff=False, bp=2)
w.trouser("hero", pos=HERO, rot_y=-0.4, color="#6f7452", hang=2.2, hi=True, loops=False, cuff=False, bp=1, bpbutton=False, turn=[(0, DUR, 0.25, "smooth")])
w.prop("sketchdraw", "sketch", (-2.0, 0.928, 0.5), (0.5, 0.7), rot_y=0.28, reveal=[T_D1 + 0.5, at("sbagliare") - 0.2])
w.prop("patterncut", "patt", (-2.85, 0.926, 0.6), (0.6, 0.86), rot_y=0.06, cut=[at("cartamodello") + 0.1, at("primo", 2) - 0.6])
w.prop("hoop", "hoopCos", (-0.55, 1.45, 1.0), (0.23, 0.14), t=at("misure"), rot_y=0.55)
w.prop("hoop", "hoopToile", (0.9, 1.45, 0.3), (0.30, 0.168), t=at("centodiciassette") - 0.3, rot_y=0.15, turn=[(0, T_SWAP, 0.35, "smooth")], move=[(T_SWAP, 0.01, (0.9, -12.0, 0.3), "linear")])   # turns WITH the toile (it cut into it) and leaves with it
w.prop("bolts", "stoffa", (2.35, 0.78, 0.52), (0.5, 0.4), n=4, seed=6, rot_y=0.4, palette=["#6f7452", "#5d6145", "#7b7d5a", "#e4dcc6"])
w.prop("logoplate", "end", (2.45, 30.0, 1.6), (1.0, 0.47), rot_y=0.06, sub="Drop 1", move=[(at("inverso") - 0.5, 1.4, (2.45, 2.2, 1.6), "glide")])

# ------------------------------------------------------------------ the map: 4 stations and the path (the Autogrill "serpentone")
ST = {1: (-2.0, 1.55, "disegno"), 2: (-2.95, 1.55, "cartamodello"), 3: (0.9, 1.2, "tela"), 4: (3.0, 0.62, "tessuto")}
pop = [at("disegno") - 0.1, at("disegno") + 0.35, at("disegno") + 0.8, at("disegno") + 1.25]   # all four on the map before the dive (3 and 4 used to pop during it)
for n, (x, z, word) in ST.items():
    w.prop("floorbadge", "st%d" % n, (x, 0.02, z), (0.78,), rot_y=math.pi / 2, n=n, word=word, ring=RED, show=pop[n - 1], out=T_END - 0.3)
SEG = {1: [(-2.0, 1.55), (-2.45, 1.82), (-2.95, 1.55)],
       2: [(-2.95, 1.55), (-3.05, 2.2), (-2.3, 2.55), (-1.2, 2.5), (-0.1, 2.3), (0.55, 1.75), (0.9, 1.2)],
       3: [(0.9, 1.2), (1.45, 1.62), (2.4, 1.62), (2.85, 1.25), (3.0, 0.62)]}
for k, (t0, t1) in {1: (T_MAP2 + 0.55, T_MAP2 + 1.35), 2: (T_MAP3 + 0.5, T_MAP3 + 1.45), 3: (T_MAP4 + 0.5, T_MAP4 + 1.35)}.items():
    w.prop("pathdots", "path%d" % k, (0, 0.035, 0), pts=[[x, 0, z] for x, z in SEG[k]], gap=0.13, r=0.045, flat=True, color=RED, span=[t0, t1])
# the COS measurements copied onto the pattern: a dotted arc from the COS waist to the paper
arc = [[-0.55 + (-2.8 + 0.55) * f, 1.45 + (0.97 - 1.45) * f + 0.55 * math.sin(math.pi * f), 1.0 + (0.62 - 1.0) * f] for f in [i / 14 for i in range(15)]]
w.prop("pathdots", "copy", (0, 0, 0), pts=arc, gap=0.09, r=0.022, color=RED, span=[at("copiate") - 0.05, end("COS") - 0.1], out=T_MAP3 + 1.6)
# "una gonna": a skirt silhouette drawn in front of the toile; then the chalk line on the hip
TX, TZ = 0.9, 0.3
w.prop("pathdots", "skirt", (TX, 0, TZ + 0.12), pts=[[-0.22, 1.47, 0], [-0.30, 0.64, 0], [0.30, 0.64, 0], [0.22, 1.47, 0]], gap=0.045, r=0.012, color=RED, span=[at("ampio") - 0.2, end("gonna", 2) - 0.1], out=T_SWAP - 0.1)
# (15/11) no floating chalk dots: toileB carries its own chalk line ON the cloth (chalk=True)

# ------------------------------------------------------------------ the camera: one move at a time, never still (slow drift between moves, as in the Autogrill)
CAMS = []


def C(t, d, pos, look, ease="hand"):
    CAMS.append((round(t, 2), d, pos, look, ease))


MAP = ((3.45, 12.5, 1.45), (0.45, 0.0, 1.35))                         # the atelier from above: x runs down the screen (station 1 at the top, 4 at the bottom)
w.cam((1.05, 1.36, 3.3), look=(0.9, 1.2, 0.3))
C(0.0, at("gonna") - 0.2, (1.0, 1.3, 2.05), (0.9, 1.2, 0.3), "out")                              # already moving at frame 1, pushing in on the toile
C(at("gonna") - 0.15, 0.55, (2.15, 1.3, 1.05), (0.95, 1.18, 0.3))                                # "gonna": the bulging side
C(T_MAP1, 1.6, MAP[0], MAP[1], "glide")                                                          # up through the roof: the map
C(T_D1, 1.0, (-2.0, 1.78, 0.72), (-2.0, 0.93, 0.5), "glide")                                    # dive to station 1, the pencil draws
C(at("doppia") + 0.3, 1.6, (-1.92, 1.6, 0.9), (-2.02, 0.93, 0.45), "glide")
C(T_MAP2, 1.1, MAP[0], MAP[1], "glide")                                                          # the map: 1 -> 2
C(T_D2, 1.0, (-2.86, 1.78, 1.32), (-2.84, 0.93, 0.52), "glide")                                 # dive to the cutting mat
C(at("verso") - 0.2, 1.4, (-2.8, 1.6, 1.45), (-2.82, 0.93, 0.66), "glide")
C(T_COS, 0.9, (1.7, 1.9, 2.35), (-1.9, 0.95, 0.75))                                          # the mistake: COS trouser and the table in one frame
C(T_MAP3, 1.3, MAP[0], MAP[1], "glide")                                                          # the map: 2 -> 3
C(T_D3, 1.15, (2.3, 1.12, 1.25), (1.8, 0.9, 0.5), "glide")                                      # dive to the sewing machine
C(at("non", 1, at("tela")) - 0.45, 1.2, (1.0, 1.36, 2.35), (0.9, 1.2, 0.3))                                 # the toile, "non per sembrare belli"
C(at("cintura") - 0.3, 1.0, (0.92, 1.78, 1.15), (0.9, 1.55, 0.3))                               # the raw top edge: no waistband
C(at("provata") - 0.1, 1.3, (1.0, 1.32, 2.2), (0.9, 1.2, 0.3), "glide")
C(at("bombatura") - 0.5, 1.0, (2.05, 1.36, 0.95), (1.1, 1.36, 0.3))                              # the bulge, from the side
C(at("centodiciassette") - 0.15, 0.9, (1.72, 1.45, 0.95), (1.0, 1.42, 0.3), "glide")             # the tape on the hips
C(T_SK, 1.2, (1.0, 1.15, 2.7), (0.9, 1.1, 0.3), "glide")                                         # front: the skirt outline
C(T_SWAP - 0.2, 0.75, (1.85, 1.2, 0.85), (1.12, 1.15, 0.3))                                     # (the swap happens here, under the blur)
C(at("tolto") - 0.1, 1.5, (1.3, 1.25, 1.9), (0.95, 1.15, 0.3), "glide")
C(at("Ecco") - 0.45, 1.25, (2.1, 1.22, 1.65), (2.35, 0.95, 0.52))                                 # the cloth: what a mistake costs
C(T_MAP4, 1.3, MAP[0], MAP[1], "glide")                                                          # the map: 3 -> 4
C(T_D4, 1.15, (3.0, 1.32, 1.95), (3.0, 1.2, -0.4), "glide")                                     # dive to the finished trouser
C(at("drill") - 0.25, 0.9, (2.75, 1.12, 0.6), (3.0, 0.95, -0.4))
C(at("doppia", 2) - 0.35, 0.85, (3.0, 1.74, 0.45), (3.0, 1.6, -0.4))
C(at("regolatori", 2) - 0.35, 0.85, (3.55, 1.66, 0.3), (3.05, 1.6, -0.4))
C(at("ogni", 3) - 0.2, 1.1, (3.0, 1.35, 2.3), (3.0, 1.15, -0.4), "glide")
C(T_END, 2.2, (2.15, 2.35, 4.45), (2.35, 1.45, -0.2), "glide")                                    # the pull-back: the whole path, the logo board drops in
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
    if gap > 0.35:                             # never still: a slow dolly toward the subject + a little sideways, until the next move (Autogrill video.py)
        dx, dy, dz = look[0] - pos[0], look[1] - pos[1], look[2] - pos[2]
        dist = math.sqrt(dx * dx + dy * dy + dz * dz); hl = math.hypot(dx, dz) or 1.0
        f = min(0.07, 0.022 * gap); lx, lz = -dz / hl * dist * f * 0.6, dx / hl * dist * f * 0.6
        if pos == MAP[0]: lx, lz, f = 0.0, 0.0, min(0.05, 0.015 * gap)             # on the map: just sink a little
        p2 = (pos[0] + dx * f + lx, pos[1] + dy * f, pos[2] + dz * f + lz); l2 = (look[0] + lx, look[1], look[2] + lz)
        w.cam(p2, look=l2, t=t + d2 + 0.03, d=gap, ease="linear")

# ------------------------------------------------------------------ labels (pinned on the objects), each on its word
L = w.label
for n, (x, z, word) in ST.items():                                  # on the first map: the four stations, one by one
    L("st%d" % n, (0, 0, 0), "%d · *%s*" % (n, word), t=pop[n - 1] + 0.05, out=T_D1 - 0.1, anchor="st%d" % n, dx={1: -150, 2: 40, 3: -150, 4: 40}[n], dy={1: 90, 2: -130, 3: -130, 4: -130}[n])
L("st2", (0, 0, 0), "2 · *cartamodello*", t=T_MAP2 + 1.2, out=T_D2 - 0.05, anchor="st2b", dx=-150, dy=-130)
L("st3", (0, 0, 0), "3 · *tela*", t=T_MAP3 + 1.3, out=T_D3 - 0.05, anchor="st3b", dx=-150, dy=-130)
L("st4", (0, 0, 0), "4 · *tessuto*", t=T_MAP4 + 1.2, out=T_D4 - 0.05, anchor="st4b", dx=-150, dy=-130)
L("sketch", (0.10, 0.0, -0.29), "Vita *alta*", t=at("vita"), out=at("vita") + 1.2, anchor="vita", dx=-30, dy=130)
L("sketch", (0.115, 0.0, 0.07), "Gamba *dritta*", t=at("gamba"), out=at("gamba") + 1.2, anchor="gamba", dx=-360, dy=-260)
L("sketch", (0.045, 0.0, -0.21), "Doppia *piega*", t=at("piega"), out=at("piega") + 1.5, anchor="piega", dx=-250, dy=60)
L("patt", (0.0, 0.003, 0.0), "*Drittofilo*", t=at("verso"), out=at("verso") + 0.95, anchor="verso", dx=-300, dy=-140)
L("patt", (0.098, 0.003, 0.017), "*Tacca* di montaggio", t=at("tacca"), out=at("tacca") + 1.7, anchor="tacca", dx=-420, dy=-160)
L("cos", (0.0, 1.0, 0.13), "Pantalone *COS*", t=at("pantalone", 2), out=end("COS") + 0.3, anchor="cos", dx=-60, dy=-260)
L("toileA", (0.1, 0.98, 0.14), "Tela *grezza*", t=at("grezza"), out=at("grezza") + 1.6, anchor="grezza", dx=-330, dy=-120)
L("toileB", (0.21, 0.75, 0.0), "Linea col *gesso*", t=at("linea"), out=at("linea") + 1.4, anchor="gesso", dx=-380, dy=-100)
L("toileB", (0.21, 0.55, 0.05), "*Molto* meglio", t=at("meglio"), out=at("meglio") + 1.4, anchor="meglio", dx=-390, dy=-120)
L("hero", (0.113, 0.5, 0.108), "Cotone *drill*", t=at("drill"), out=at("drill") + 1.5, anchor="drill", sub="verde oliva", dx=-360, dy=-120)
L("hero", (0.01, 0.98, 0.135), "Doppia *piega*", t=at("doppia", 2), out=at("doppia", 2) + 1.0, anchor="piega2", dx=-60, dy=-470)
L("hero", (0.19, 1.05, 0.03), "Regolatori *laterali*", t=at("regolatori", 2), out=at("regolatori", 2) + 2.0, anchor="regolatori", dx=-440, dy=-130)

# ------------------------------------------------------------------ captions + big statements: text on screen for the WHOLE video, max two lines
KEY = {"gonna", "disegno", "errore", "carta", "cartamodello", "corpo", "tela", "grezza", "bombatura", "centodiciassette", "gesso", "meglio", "stoffa", "finito", "drill", "oliva", "scelta", "inverso", "studente", "seguimi", "errori", "venderti", "primo", "arrivato"}
chunks, cur = [], []
for i, x in enumerate(WORDS):
    cur.append(x)
    brk = x["w"].endswith((".", ":", "?", "!", ",", "...")) or len(cur) >= 3 or sum(len(c["w"]) for c in cur) > 17
    if brk or i == len(WORDS) - 1:
        nxt = WORDS[i + 1]["s"] if i + 1 < len(WORDS) else cur[-1]["e"] + 1.0
        txt = " ".join(c["w"] for c in cur)
        for c in cur:
            if norm(c["w"]) in KEY:
                txt = txt.replace(c["w"], "*" + c["w"].rstrip(".,:!?") + "*" + c["w"][len(c["w"].rstrip(".,:!?")):], 1); break
        txt = txt.replace("*centodiciassette* centimetri", "*117* cm").replace("centodiciassette centimetri", "117 cm")
        chunks.append((cur[0]["s"], min(nxt - 0.02, cur[-1]["e"] + 0.45), txt.rstrip(".,:").replace("...", "…")))
        cur = []
B = w.big
B(-0.3, end("gonna") + 0.2, "Il mio primo pantalone|sembrava una *gonna*", top=240, size=76)
B(at("centodiciassette"), end("fianchi") + 0.15, "*<b id='c117'>117</b> cm* ai fianchi", top=260, size=96)
B(at("più"), end("gonna", 2) + 0.3, "più che un pantalone|ampio, una *gonna*", top=260, size=78)
B(at("errore", 3), wend("stoffa", at("errore", 3)) + 0.25, "l'errore costa|*un pezzo di stoffa*", top=250, size=78)
B(at("Questo"), end("capo") + 0.2, "Questo è *Inverso*,|il mio primo capo", top=1160, size=80)
B(at("vuoi"), wend("tela", at("vuoi")) + 0.25, "Vuoi vedere|la prossima tela?", top=1140, size=80)
B(wend("tela", at("vuoi")) + 0.26, DUR, "*Seguimi*", top=1140, size=96)
SP = w.spans()
chunks = [c for c in chunks if not any(c[0] < b - 0.02 and c[1] > a + 0.02 for a, b in SP)]
starts = sorted([c[0] for c in chunks] + [a for a, b in SP])
chunks = [(a, max(b, min([s for s in starts if s > a + 0.01] + [b + 1.0]) - 0.01), t) for a, b, t in chunks]
for bg in w.bigs:
    nx = [s for s in starts if s > bg[0] + 0.01]
    if nx and nx[0] - bg[1] < 1.0: bg[1] = round(max(bg[1], nx[0] - 0.01), 3)
w.captions(chunks, top=1180, size=96)

# ------------------------------------------------------------------ the live counters (DOM, pure functions of time: hf-seek)
COST = [(at("sbagliare"), "niente"), (at("copiate"), "un foglio di carta"), (at("pezzo", 2), "un pezzo di stoffa")]
COST_OUT = T_MAP4 + 0.2
C117 = (at("centodiciassette"), at("centodiciassette") + 1.0)


def _extra(path):
    p = open(path, encoding="utf-8").read()
    css = ("<style>.w3-lab{font-size:56px !important;padding:24px 38px !important;border-radius:28px !important}.w3-lab small{font-size:40px !important}"
           "#cost{position:absolute;left:0;right:0;top:118px;text-align:center;opacity:0;pointer-events:none;z-index:60}"
           "#cost span{display:inline-block;padding:16px 32px;border-radius:999px;background:rgba(22,18,14,.72);color:#fbf7ee;font:600 42px/1.1 Inter,'Segoe UI',sans-serif;letter-spacing:-.01em}"
           "#cost i{font-family:'Playfair Display',Georgia,serif;font-weight:500;color:#ffb48f;font-style:italic}</style></head>")
    js = ("<div id='cost'><span>costo di un errore: <i id='costv'></i></span></div>"
          "<script>(function(){var S=%s,OUT=%.3f,C0=%.3f,C1=%.3f;window.addEventListener('hf-seek',function(e){var t=e.detail.time,el=document.getElementById('cost'),v=document.getElementById('costv'),k=-1;"
          "for(var i=0;i<S.length;i++)if(t>=S[i][0])k=i;var a=k<0?0:Math.min(1,(t-S[0][0])/0.25,(OUT-t)/0.25);el.style.opacity=Math.max(0,a);"
          "if(k>=0&&v.textContent!==S[k][1]){v.textContent=S[k][1];}var p=k>=0?Math.min(1,(t-S[k][0])/0.2):1;el.style.transform='scale('+(1+0.12*Math.sin(Math.PI*p))+')';"
          "var c=document.getElementById('c117');if(c){var q=Math.max(0,Math.min(1,(t-C0)/(C1-C0)));q=1-Math.pow(1-q,3);c.textContent=Math.round(117*q);}});})();</script></body>"
          ) % (json.dumps(COST), COST_OUT, C117[0], C117[1])
    p = p.replace("</head>", css, 1).replace("</body>", js, 1)
    open(path, "w", encoding="utf-8").write(p)


if __name__ == "__main__":
    out = os.path.join(HERE, "comp")
    print(World3D.page(out, [w], duration=DUR)); _extra(os.path.join(out, "index.html"))
    print("DUR", DUR, "captions", len(chunks), "cams", len(CAMS))
    print("beats: map1 %.2f d1 %.2f map2 %.2f d2 %.2f cos %.2f map3 %.2f d3 %.2f swap %.2f map4 %.2f d4 %.2f end %.2f" % (T_MAP1, T_D1, T_MAP2, T_D2, T_COS, T_MAP3, T_D3, T_SWAP, T_MAP4, T_D4, T_END))
