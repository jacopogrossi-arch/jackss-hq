# Short 9:16 "Il mio primo pantalone sembrava una gonna" (14/11/2026): one continuous 3D atelier, every cue tied to a word of the voiceover (words.json).
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


VO_END = WORDS[-1]["e"]
DUR = round(VO_END + 2.6, 2)
if __name__ == "__main__" and "--times" in sys.argv:
    print("VO ends", VO_END, "DUR", DUR); sys.exit()

PW, PH = 1080, 1920
w = World3D("s", 0.0, DUR, fov=42, w=PW, h=PH, fade=0.4)
furnish(w)
w.shutter(0.5)

# ------------------------------------------------------------------ the objects
HERO = (3.0, 0.55, -0.4)
w.trouser("toileA", pos=(0.9, 0.55, 0.3), rot_y=0.15, color="#e4dcc6", hang=2.2, hi=True, toile=True, noband=True, bp=0, bulge=[0.05, 0.05], turn=[(0, DUR, 0.45, "smooth")],
          move=[(at("gesso") - 0.55, 0.01, (0.9, -12.0, 0.3), "linear")])
w.trouser("toileB", pos=(0.9, -12.0, 0.3), rot_y=0.15, color="#e4dcc6", hang=2.2, hi=True, toile=True, noband=True, bp=0, bulge=[0.05, 0.004], chalk=True,
          move=[(at("gesso") - 0.55, 0.01, (0.9, 0.55, 0.3), "linear")], turn=[(at("gesso") - 0.54, 12, 0.5, "smooth")])
w.trouser("cos", pos=(-0.55, 0.55, 1.0), rot_y=0.55, color="#1e1b18", hang=2.2, hi=True, loops=True, cuff=False, bp=2)
w.trouser("hero", pos=HERO, rot_y=-0.4, color="#6f7452", hang=2.2, hi=True, loops=False, cuff=False, bp=1, bpbutton=False, turn=[(0, DUR, 0.25, "smooth")])
# drawing and cutting
t_draw0, t_draw1 = at("parte") - 0.1, at("sbagliare") - 0.2
w.prop("sketchdraw", "sketch", (-2.0, 0.928, 0.5), (0.5, 0.7), rot_y=0.28, reveal=[t_draw0, t_draw1])
w.prop("shears", "shears", (-3.45, 0.928, 0.78), rot_y=0.15, move=[(at("cartamodello") - 0.2, 1.8, (-2.75, 0.928, 0.78), "glide"), (at("verso"), 1.3, (-2.35, 0.928, 0.62), "glide")])
w.prop("hoop", "hoopCos", (-0.55, 1.45, 1.0), (0.23, 0.14), t=at("misure"), rot_y=0.55)
w.prop("hoop", "hoopToile", (0.9, 1.45, 0.3), (0.245, 0.14), t=at("centodiciassette") - 0.3, rot_y=0.15)
w.prop("bolts", "stoffa", (2.35, 0.78, 0.52), (0.5, 0.4), n=4, seed=6, rot_y=0.4)
w.card("end", (1.25, 2.55, 1.2), w=1.25, h=0.46, text="*Inverso*", sub="Drop 1", color="#EFE9DD", t=at("inverso"), flat=True)

# ------------------------------------------------------------------ the camera (one move at a time; every moment is a word)
CAMS = []


def C(t, d, pos, look, ease="hand"):
    CAMS.append((round(t, 2), d, pos, look, ease))


w.cam((0.95, 1.38, 3.5), look=(0.9, 1.2, 0.3))
C(0.25, at("disegno") - 1.5, (0.95, 1.3, 1.95), (0.9, 1.22, 0.3), "glide")                                        # hook: the toile, pushing in
C(at("disegno") - 0.85, 0.95, (-1.95, 1.62, 1.1), (-2.0, 0.93, 0.5))                                                  # whip to the drawing table
C(t_draw0, t_draw1 - t_draw0 + 0.3, (-2.0, 1.78, 0.72), (-2.0, 0.93, 0.5), "glide")                                   # the pencil draws, the camera sinks
C(at("carta") - 0.7, 0.9, (-2.9, 1.3, 1.55), (-2.9, 0.93, 0.62))                                                      # whip to the cutting mat
C(at("cartamodello"), at("errore", 2) - at("cartamodello") - 1.0, (-2.5, 1.2, 1.35), (-2.75, 0.93, 0.62), "glide")
C(at("errore", 2) - 0.6, 0.9, (-0.2, 1.42, 2.35), (-0.55, 1.2, 1.0))                                                  # whip to the COS trouser
C(at("cuce") - 0.75, 0.95, (1.0, 1.36, 2.35), (0.9, 1.2, 0.3))                                                        # whip to the toile
C(at("cintura") - 0.3, 1.0, (0.92, 1.78, 1.15), (0.9, 1.55, 0.3))                                                     # the raw top edge: no waistband
C(at("provata") - 0.1, 1.3, (1.0, 1.32, 2.2), (0.9, 1.2, 0.3), "glide")
C(at("bombatura") - 0.5, 1.0, (2.05, 1.36, 0.95), (1.1, 1.36, 0.3))                                                   # the bulge, from the side
C(at("gonna", 2) - 0.6, 1.4, (1.1, 1.25, 3.0), (0.9, 1.15, 0.3), "glide")
C(at("gesso") - 0.75, 0.75, (1.85, 1.2, 0.85), (1.12, 1.15, 0.3))                                                     # (the swap happens here, under the blur)
C(at("tolto") - 0.1, 1.5, (1.05, 1.28, 2.5), (0.9, 1.15, 0.3), "glide")
C(at("stoffa") - 0.7, 0.9, (2.1, 1.22, 1.65), (2.35, 0.95, 0.52))                                                     # whip to the cloth
C(at("finito") - 0.8, 0.9, (3.0, 1.32, 1.95), (3.0, 1.2, -0.4))                                                       # whip to the finished trouser
C(at("tessuto") - 0.1, 1.2, (2.75, 1.12, 0.6), (3.0, 0.95, -0.4), "glide")
C(at("doppia", 2) - 0.45, 1.0, (3.0, 1.74, 0.45), (3.0, 1.6, -0.4))
C(at("regolatori", 2) - 0.45, 1.0, (3.55, 1.66, 0.3), (3.05, 1.6, -0.4))
C(at("scelta") - 0.3, 1.2, (3.0, 1.35, 2.3), (3.0, 1.15, -0.4), "glide")
C(at("Questo") - 0.1, DUR - at("Questo") - 0.4, (2.2, 1.85, 5.3), (0.9, 1.3, -0.4), "glide")                        # the pull-back, the card
CAMS.sort()
for k, (t, d, pos, look, ease) in enumerate(CAMS):
    nxt = CAMS[k + 1][0] if k + 1 < len(CAMS) else DUR
    d2 = min(d, nxt - t - 0.03)
    if d2 < 0.35:
        print("  SKIPPED move at %.2f (no room: %.2f)" % (t, d2)); continue
    if d2 < d - 0.01:
        print("  move at %.2f shortened %.2f -> %.2f" % (t, d, d2))
    w.cam(pos, look=look, t=t, d=d2, ease=ease)

# ------------------------------------------------------------------ labels (pinned on the objects), each on its word
L = w.label
L("sketch", (0.10, 0.0, -0.29), "Vita *alta*", t=at("vita"), out=at("vita") + 1.2, anchor="vita", dx=-30, dy=-190)
L("sketch", (0.115, 0.0, 0.07), "Gamba *dritta*", t=at("gamba"), out=at("gamba") + 1.2, anchor="gamba", dx=-190, dy=-130)
L("sketch", (0.045, 0.0, -0.21), "Doppia *piega*", t=at("piega"), out=at("piega") + 1.5, anchor="piega", dx=-250, dy=-80)
L("cos", (0.0, 1.0, 0.13), "Pantalone *COS*", t=at("COS"), out=at("COS") + 1.8, anchor="cos", dx=-340, dy=-120)
L("toileA", (0.1, 0.98, 0.14), "Tela *grezza*", t=at("grezza"), out=at("grezza") + 1.6, anchor="grezza", dx=-330, dy=-120)
L("toileA", (0.19, 0.94, 0.04), "*117* cm ai fianchi", t=at("centodiciassette"), out=at("centodiciassette") + 3.0, anchor="117", dx=-420, dy=-160)
L("toileB", (0.21, 0.75, 0.0), "Linea col *gesso*", t=at("gesso"), out=at("gesso") + 1.6, anchor="gesso", dx=-380, dy=-100)
L("toileB", (0.21, 0.55, 0.05), "*Molto* meglio", t=at("meglio"), out=at("meglio") + 1.6, anchor="meglio", dx=-390, dy=-120)
L("stoffa", (0.0, 0.2, 0.0), "un pezzo di *stoffa*", t=at("stoffa"), out=at("stoffa") + 1.6, anchor="stoffa", dx=-390, dy=-130)
L("hero", (0.0, 0.98, 0.13), "un capo *finito*", t=at("finito"), out=at("finito") + 1.5, anchor="finito", dx=-340, dy=-150)
L("hero", (0.113, 0.5, 0.108), "Cotone *drill*", t=at("drill"), out=at("drill") + 1.8, anchor="drill", sub="verde oliva", dx=-360, dy=-120)
L("hero", (0.01, 0.98, 0.135), "Doppia *piega*", t=at("doppia", 2), out=at("doppia", 2) + 2.0, anchor="piega2", dx=-340, dy=-120)
L("hero", (0.19, 1.05, 0.03), "Regolatori *laterali*", t=at("regolatori", 2), out=at("regolatori", 2) + 2.0, anchor="regolatori", dx=-440, dy=-130)

# ------------------------------------------------------------------ captions (big, word groups, upper-middle zone: Shorts' own buttons sit at the bottom)
KEY = {"gonna", "disegno", "errore", "carta", "cartamodello", "corpo", "tela", "grezza", "bombatura", "centodiciassette", "gesso", "meglio", "stoffa", "finito", "drill", "oliva", "scelta", "inverso", "studente", "seguimi", "errori", "venderti", "primo"}
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
        chunks.append((cur[0]["s"], min(nxt - 0.02, cur[-1]["e"] + 0.45), txt.rstrip(".,:").replace("...", "…")))
        cur = []
w.captions(chunks, top=1180, size=96)

def _style(path):
    p = open(path, encoding="utf-8").read()
    css = "<style>.w3-lab{font-size:44px !important;padding:20px 32px !important;border-radius:24px !important}.w3-lab small{font-size:34px !important}</style></head>"
    open(path, "w", encoding="utf-8").write(p.replace("</head>", css, 1))


if __name__ == "__main__":
    out = os.path.join(HERE, "comp")
    print(World3D.page(out, [w], duration=DUR)); _style(os.path.join(out, "index.html"))
    print("DUR", DUR, "captions", len(chunks))
