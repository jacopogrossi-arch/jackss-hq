# Video 3D "Tre vite di un pantalone" (13/11/2026): one continuous world3d scene of 90 s, wipes/labels/dof tied to the voiceover words.
import json, os, sys
SK = "D:/ClaudeCodeTest/.claude/skills/youtube-edit"
sys.path.insert(0, SK + "/formats")
from world3d import World3D

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = json.load(open(HERE + "/words.json", encoding="utf-8"))
DUR = float(os.environ.get("W3_DUR", 90.0))

# the voiceover chunks (source start, source end) and where each one starts in the video; gaps are the breaths between chapters
CHUNKS = [(0.0, 9.55), (9.95, 21.95), (22.35, 36.1), (36.45, 52.7), (52.95, 59.9), (60.3, 67.4)]
GAPS = [8.0, 1.2, 1.4, 1.4, 1.2, 1.5]          # video time where chunk 0 starts, then the pause before each next chunk
ABS = []
t = GAPS[0]
for i, (a, b) in enumerate(CHUNKS):
    ABS.append(t)
    t += (b - a) + (GAPS[i + 1] if i + 1 < len(GAPS) else 0)
VO_END = t


def at(src):
    """Video time of a moment of the voiceover file (seconds in the file)."""
    for (a, b), s0 in zip(CHUNKS, ABS):
        if a - 0.01 <= src <= b + 0.2:
            return round(s0 + (src - a), 2)
    raise ValueError(src)


def word(src_s):
    return at(src_s)


if __name__ == "__main__" and "--times" in sys.argv:
    print("chunks start at", ABS, "VO ends", round(VO_END, 2))
    for x in WORDS:
        print(x["w"], at(x["s"]))
    sys.exit()

w = World3D("v", 0.0, DUR, title="Tre vite di un *pantalone*", sub="Il viaggio di un capo", title_out=15.0, fov=34, fade=0.8)
w.look(floor="#3a281b", wall="#4d3827")
w.shutter(0.8)

# ---- the objects
w.trouser("main", pos=(0, 0, 0), rot_y=-0.5, color="#6f7452",
          turn=[(0, 16, -0.15, "smooth"), (26, 6, 0.1, "smooth"), (33, 10, 0.9, "smooth"), (47, 12, 0.25, "smooth"), (62.0, 10.5, 6.4332, "smooth")],
          move=[(72.2, 1.6, (1.0, 0, 0), "glide")])
w.card("sheet", (-1.6, 0.45, -0.75), w=0.62, h=0.86, text="*Scheda*", sub="tecnica · Drop 1", rot_y=0.5)
w.solid("roll1", "cyl", (0.72, 0.21, -0.2), (0.22, 0.42), fabric=True, color="#7b7d5a", rot_y=0.3)
w.solid("roll2", "cyl", (1.0, 0.21, -0.5), (0.22, 0.42), fabric=True, color="#8a4b2d", rot_y=0.1)
w.solid("roll3", "cyl", (0.5, 0.21, -0.65), (0.22, 0.42), fabric=True, color="#b9ae98", rot_y=0.5)
# the finale: three lives side by side (ink, clay, final), plus the end card
w.trouser("inkT", pos=(-1.0, 0, 0), rot_y=-0.1, color="#6f7452", look="ink", t=at(60.5), turn=[(73.4, 9, 0.5, "smooth")])
w.trouser("clayT", pos=(0.0, 0, 0), rot_y=0.1, color="#6f7452", look="clay", t=at(61.32), turn=[(74.2, 9, -0.4, "smooth")])
w.card("end", (0.0, 1.55, -0.25), w=2.1, h=0.74, text="*Inverso*", sub="Drop 1", color="#EFE9DD", t=at(65.5), flat=True)

# ---- the passes: final (the hook), ink (chapter 1), clay (chapter 2), final (chapter 3)
w.wipe("ink", at(10.0) - 0.4, 0.9)
w.wipe("clay", at(23.0) - 0.9, 0.9)
w.wipe("final", at(37.06) - 0.9, 0.9)

# ---- the camera (one move at a time)
w.cam((1.9, 0.42, 4.2), look=(0.3, 0.35, 0))
w.cam((1.15, 0.95, 2.5), look=(0, 0.72, 0), t=0.3, d=7.6, ease="glide")
w.cam((0.25, 1.05, 1.7), look=(0, 0.8, 0), t=15.4, d=2.2)
w.cam((-0.95, 1.05, 2.0), look=(0, 0.72, 0), t=18.6, d=4.0, ease="glide")
w.cam((-0.2, 0.75, 2.3), look=(0, 0.6, 0), t=22.8, d=4.4, ease="glide")
w.cam((0.28, 1.2, 0.95), look=(0.05, 1.02, 0.05), t=at(19.2) - 0.7, d=1.0)
w.cam((0.45, 0.55, 1.25), look=(0.1, 0.45, 0), t=at(20.3) - 0.5, d=0.9)
w.cam((0.15, 1.08, 0.9), look=(0.075, 0.98, 0.1), t=at(21.4) - 0.6, d=1.0)
w.cam((-1.3, 0.85, 2.1), look=(0, 0.7, 0), t=at(22.4) + 0.8, d=1.6)
w.cam((1.5, 0.9, 1.4), look=(0, 0.7, 0), t=at(26.4) - 0.6, d=2.4, ease="glide")
w.cam((0.9, 1.0, 0.8), look=(0.2, 0.95, 0.05), t=at(29.0) - 0.7, d=0.7)
w.cam((0.5, 0.95, -1.2), look=(0, 0.88, -0.1), t=at(30.9) - 0.9, d=1.0)
w.cam((0.7, 0.3, 0.9), look=(0.12, 0.2, 0.1), t=at(32.1) - 0.6, d=0.8)
w.cam((0.3, 0.9, 2.4), look=(0, 0.7, 0), t=at(33.4) - 0.4, d=2.4)
w.cam((-0.5, 0.35, 1.8), look=(0.1, 0.5, 0), t=at(36.5) + 0.2, d=1.2)
w.cam((0.3, 0.7, 1.1), look=(0.1, 0.6, 0.05), t=at(38.0), d=1.6)
w.cam((-0.1, 0.9, 2.2), look=(0, 0.75, 0), t=at(39.9) - 0.2, d=1.7)
w.cam((0.18, 1.1, 0.85), look=(0.075, 1.0, 0.11), t=at(42.1) - 0.2, d=1.4)
w.cam((0.55, 1.12, 0.8), look=(0.19, 1.06, 0.03), t=at(46.4) - 0.4, d=1.4)
w.cam((0.3, 0.95, 2.0), look=(0, 0.75, 0), t=at(49.2), d=2.4)
w.cam((-1.15, 0.65, 1.9), look=(0, 0.72, 0), t=at(52.95) - 0.3, d=3.0, ease="glide")
w.cam((0.15, 0.95, 1.5), look=(0, 0.8, 0), t=at(55.9) - 0.1, d=2.0, ease="glide")
w.cam((1.15, 0.38, 1.7), look=(0.0, 0.5, 0), t=at(58.6) - 0.79, d=2.6, ease="glide")
w.cam((0.0, 1.0, 3.6), look=(0, 0.8, 0), t=at(60.4) - 0.8, d=2.2)
w.cam((-0.4, 0.95, 3.4), look=(0.0, 0.8, 0), t=at(63.3), d=1.6, ease="glide")
w.cam((0.15, 1.0, 5.2), look=(0.0, 0.88, -0.1), t=at(65.0), d=DUR - at(65.0) - 1.0, ease="glide")

# ---- labels (ivory tags pinned on the garment), each on its word
w.label("main", (0.18, 1.06, 0.03), "Vita *naturale*", t=at(19.3), out=at(19.3) + 2.2, anchor="vita", dx=150, dy=-150)
w.label("main", (0.115, 0.34, 0.112), "Gamba *dritta*", t=at(20.4), out=at(20.4) + 2.0, anchor="gamba", dx=190, dy=-60)
w.label("main", (0.075, 1.0, 0.112), "La *piega*", t=at(21.5), out=at(21.5) + 2.4, anchor="piega", dx=-420, dy=40)
w.label("main", (0.12, 0.6, 0.12), "Tela *di prova*", t=at(25.0), out=at(25.0) + 3.0, anchor="tela", sub="grigia e nuda", dx=170, dy=-110)
w.label("main", (0.20, 0.95, 0.10), "Dove *tira*", t=at(29.5), out=at(29.5) + 1.6, anchor="tira", dx=150, dy=-100)
w.label("main", (0.0, 0.88, -0.14), "Dove si *siede*", t=at(31.4), out=at(31.4) + 1.4, anchor="siede", dx=-380, dy=-60)
w.label("main", (0.12, 0.08, 0.12), "Dove *cade*", t=at(32.4), out=at(32.4) + 1.4, anchor="cade", dx=170, dy=-110)
w.label("main", (0.12, 0.5, 0.12), "Cotone *drill*", t=at(38.5), out=at(38.5) + 2.6, anchor="drill", sub="pesante", dx=170, dy=-110)
w.label("main", (0.075, 1.0, 0.112), "Doppia piega *all'italiana*", t=at(42.9), out=at(42.9) + 3.6, anchor="piega2", dx=-640, dy=30)
w.label("main", (0.2, 1.06, 0.03), "Regolatori *laterali*", t=at(46.6), out=at(46.6) + 2.4, anchor="regolatori", sub="al posto della cintura", dx=170, dy=-130)

# ---- depth of field on the detail shots
w.dof(at(38.0) - 0.2, 3.0, 0.025)
w.dof(at(42.0), 4.0, 0.02)
w.dof(at(46.3), 3.0, 0.02)
w.dof(at(63.0), 3.0, 0.03)       # the pull-back on the final line

if __name__ == "__main__":
    out = os.path.join(HERE, "comp")
    print(World3D.page(out, [w], duration=DUR))
    print("VO", [ (round(s,2)) for s in ABS ], "end", round(VO_END, 2))
