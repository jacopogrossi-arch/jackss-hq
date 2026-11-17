# Video 3D v2 "Tre vite di un pantalone" (14/11/2026): the same voice, now a tour of an atelier with three stations (drawing, toile, fabric).
import json, os, sys
SK = "D:/ClaudeCodeTest/.claude/skills/youtube-edit"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SK + "/formats"); sys.path.insert(0, HERE)
from world3d import World3D
from room import furnish
WORDS = json.load(open(HERE + "/words.json", encoding="utf-8"))
CHUNKS = [(0.0, 9.55), (9.95, 21.95), (22.35, 36.1), (36.45, 52.7), (52.95, 59.9), (60.3, 67.4)]
GAPS = [3.0, 0.5, 0.7, 0.7, 0.6, 0.7]
ABS, t = [], GAPS[0]
for i, (a, b) in enumerate(CHUNKS):
    ABS.append(t); t += (b - a) + (GAPS[i + 1] if i + 1 < len(GAPS) else 0)
VO_END = t
DUR = round(VO_END + 4.4, 2)


def at(src):
    for (a, b), s0 in zip(CHUNKS, ABS):
        if a - 0.01 <= src <= b + 0.2:
            return round(s0 + (src - a), 2)
    raise ValueError(src)


if __name__ == "__main__" and "--times" in sys.argv:
    print("ABS", ABS, "VO_END", round(VO_END, 2), "DUR", DUR); sys.exit()

w = World3D("v", 0.0, DUR, title="Tre vite di un *pantalone*", sub="Il viaggio di un capo", title_out=8.6, fov=36, fade=0.6)
furnish(w)
w.shutter(0.8)
# --- the three trousers, one per station
w.trouser("hero", pos=(3.0, 0.55, -0.4), rot_y=-0.4, color="#6f7452", hang=2.2, turn=[(0, 55, 0.35, "smooth"), (at(60.5), 10.5, 5.883, "smooth")])
w.trouser("toile", pos=(0.9, 0.55, 0.3), rot_y=0.25, color="#e4dcc6", hang=2.2, turn=[(at(23.5), 14, -0.45, "smooth")])
w.card("end", (1.0, 2.5, 0.9), w=1.6, h=0.56, text="*Inverso*", sub="Drop 1", color="#EFE9DD", t=at(65.6), flat=True)

# --- the camera (one move at a time; every number is a word of the voice)
c = w.cam
c((4.8, 1.9, 6.2), look=(0.4, 1.1, -0.6))
c((2.6, 1.5, 3.8), look=(0.7, 1.1, 0.2), t=0.3, d=5.2, ease="glide")
c((1.6, 1.3, 2.5), look=(0.9, 1.0, 0.3), t=5.7, d=5.2, ease="glide")
c((-1.2, 1.35, 2.5), look=(-2.6, 1.0, 0.6), t=11.8, d=1.5)                              # whip to the drawing table: "il disegno"
c((-2.1, 1.5, 1.7), look=(-2.7, 0.95, 0.6), t=13.5, d=3.8, ease="glide")
c((-2.9, 1.35, 1.25), look=(-2.7, 0.93, 0.55), t=17.5, d=2.5)
c((-2.2, 1.25, 1.0), look=(-2.0, 0.95, 0.5), t=21.3, d=2.6, ease="glide")
c((1.4, 1.35, 2.1), look=(0.9, 1.25, 0.3), t=24.6, d=1.6)                                 # whip to the toile: "il volume"
c((0.3, 1.3, 1.7), look=(0.9, 1.25, 0.3), t=26.5, d=3.2, ease="glide")
c((0.5, 1.4, 1.35), look=(0.95, 1.3, 0.3), t=29.9, d=1.8, ease="glide")
c((1.25, 1.55, 1.0), look=(0.95, 1.45, 0.3), t=31.9, d=1.9)                               # "tira"
c((0.7, 1.45, -0.5), look=(0.9, 1.3, 0.3), t=33.9, d=1.2)                                # "si siede": from behind
c((1.4, 0.7, 1.2), look=(0.9, 0.65, 0.3), t=35.3, d=0.9)                                # "cade": at the hem
c((0.8, 1.5, 2.9), look=(0.9, 1.2, 0.3), t=36.4, d=1.8)
c((2.2, 1.45, 1.9), look=(3.0, 1.2, -0.4), t=38.9, d=1.5)                                # whip to the stock wall: "la materia"
c((2.6, 1.25, 0.9), look=(3.0, 1.1, -0.4), t=40.6, d=2.8, ease="glide")
c((3.4, 1.4, 0.7), look=(3.0, 1.2, -0.4), t=43.6, d=2.0, ease="glide")
c((3.0, 1.75, 0.4), look=(3.0, 1.58, -0.4), t=45.8, d=1.3)                               # the pleat
c((3.5, 1.7, 0.3), look=(3.05, 1.6, -0.4), t=49.0, d=1.4)                              # the side adjusters
c((2.4, 1.4, 1.5), look=(3.0, 1.2, -0.4), t=52.0, d=2.0, ease="glide")
c((3.6, 1.3, 1.8), look=(3.0, 1.1, -0.4), t=54.3, d=2.5, ease="glide")
c((2.2, 1.3, 1.8), look=(3.2, 1.1, -0.4), t=57.2, d=3.3, ease="glide")                   # a slow arc round the hero: "si sente"
c((3.7, 0.75, 1.5), look=(3.0, 0.8, -0.4), t=60.7, d=2.0)
c((2.2, 1.9, 6.4), look=(0.5, 1.2, -0.4), t=63.2, d=5.5, ease="glide")                   # the pull-back: three passages, one trouser
c((1.6, 1.8, 6.9), look=(0.7, 1.2, -0.4), t=68.9, d=DUR - 68.9 - 0.5, ease="linear")

# --- labels, each on its word
w.label("sketch", (0.14, 0.0, -0.27), "Vita *naturale*", t=at(19.3), out=at(19.3) + 1.7, anchor="vita", dx=150, dy=-140)
w.label("sketch", (0.11, 0.0, 0.12), "Gamba *dritta*", t=at(20.4), out=at(20.4) + 1.6, anchor="gamba", dx=170, dy=-60)
w.label("sketch", (-0.045, 0.0, -0.2), "La *piega*", t=at(21.5), out=at(21.5) + 1.2, anchor="piega", dx=-380, dy=40)
w.label("toile", (0.12, 0.6, 0.12), "Tela *di prova*", t=at(24.8), out=at(24.8) + 2.4, anchor="tela", sub="grigia e nuda", dx=170, dy=-110)
w.label("toile", (0.20, 0.95, 0.10), "Dove *tira*", t=at(30.6), out=at(30.6) + 1.3, anchor="tira", dx=150, dy=-100)
w.label("toile", (0.0, 0.88, -0.14), "Dove si *siede*", t=at(31.6), out=at(31.6) + 1.2, anchor="siede", dx=-380, dy=-60)
w.label("toile", (0.12, 0.08, 0.12), "Dove *cade*", t=at(32.5), out=at(32.5) + 1.3, anchor="cade", dx=170, dy=-110)
w.label("hero", (0.12, 0.5, 0.12), "Cotone *drill*", t=at(38.5), out=at(38.5) + 2.3, anchor="drill", sub="pesante", dx=170, dy=-110)
w.label("hero", (0.075, 1.0, 0.112), "Doppia piega *all'italiana*", t=at(42.9), out=at(42.9) + 3.3, anchor="piega2", dx=-640, dy=30)
w.label("hero", (0.2, 1.06, 0.03), "Regolatori *laterali*", t=at(46.6), out=at(46.6) + 2.3, anchor="regolatori", sub="al posto della cintura", dx=170, dy=-130)

# --- depth of field on the close shots
w.dof(17.4, 3.0, 0.02)
w.dof(at(38.2) - 0.4, 3.0, 0.025)
w.dof(at(42.5) - 0.3, 3.4, 0.02)
w.dof(at(46.5) + 0.2, 2.4, 0.02)

def _style(path):
    p = open(path, encoding="utf-8").read()
    css = "<style>.w3-title{color:#1e1b18 !important;text-shadow:0 2px 18px rgba(255,244,222,.7) !important}.w3-title i{color:#8a4b2d !important}.w3-sub{color:#3a2c20 !important;text-shadow:0 1px 12px rgba(255,244,222,.8) !important}</style></head>"
    open(path, "w", encoding="utf-8").write(p.replace("</head>", css, 1))


if __name__ == "__main__":
    out = os.path.join(HERE, "comp")
    print(World3D.page(out, [w], duration=DUR)); _style(os.path.join(out, "index.html"))
    print("ABS", ABS, "VO_END", round(VO_END, 2), "DUR", DUR)
