import sys, math, json, os
sys.path.insert(0, "D:/ClaudeCodeTest/.claude/skills/fashion-3d/engine")
from world3d import World3D
GLB = "D:/ClaudeCodeTest/social/short-03-tabellone/assets/trouser10b.glb"
PI = math.pi
SOFT = "--soft" in sys.argv
Y = 0.04                                   # board top
SQ = {"P": (-1.2, 0.6), "1": (-0.4, 0.6), "2": (0.4, 0.6), "3": (1.2, 0.6), "4": (1.2, -0.3), "5": (0.25, -0.45)}
def at(k, dy=0.0): x, z = SQ[k]; return (x, Y + dy, z)

w = World3D("w1", 0.0, 65.0, fov=44, w=1080, h=1920)
w.room(bg="#120f0c", key="#ffd9a8", dir=(-2.5, 4, 2.2), key_i=2.6, hemi=("#ffe6c8", "#3a2a1c"), hemi_i=0.55, rim="#8fa9d8", rim_i=0.6, aim=(0, 0.3, 0)).photo()
if SOFT: w.soft(n=10, area=0.12, sky=0.35)
w.prop("woodfloor", "fl", (0, 0, 0), (10, 10))
w.prop("wall", "wl", (0, 0, -1.6), (8, 4, 0.1), hole=[0.4, 1.25, 1.3, 1.1])
w.prop("window", "win", (0.4, 1.25, -1.54), (1.3, 1.1), view="night", dist=3)
# the board: ivory slab with a forest border
w.solid("brd0", "box", (0, Y / 2 - 0.004, 0.05), (3.4, Y - 0.008, 2.0), color="#2F3A2E", rough=0.7, radius=0.02)
w.solid("brd", "box", (0, Y / 2, 0.05), (3.28, Y, 1.88), color="#EFE9DD", rough=0.85, radius=0.01)
w.prop("logoplate", "logo", (-0.45, Y + 0.016, -0.3), (0.95, 0.48), rot_x=-PI / 2)
for k, word in [("P", "via"), ("1", "disegno"), ("2", "modello"), ("3", "foto"), ("4", "pre-order"), ("5", "arrivo")]:
    w.prop("floorbadge", "sq" + k, at(k), (0.46,), n=("★" if k == "P" else "✓" if k == "5" else k), word=word, ring="#8A4B2D" if k in "P5" else "#2F3A2E", show=0.0 if k == "P" else None)
# the path, drawn as the token walks
w.prop("pathdots", "path", (0, Y + 0.01, 0), pts=[[-1.2, 0, 0.6], [1.2, 0, 0.6], [1.2, 0, -0.3], [0.25, 0, -0.45]], gap=0.09, r=0.016, color="#B9AE98", glow=0.1, flat=True, span=[0.0, 52.0])
# Jacopino, the token
J = dict(height=0.34, glasses=True, vest=True)
w.mascot("j", pos=at("P"), rot_y=0.3, hop=[0.5, 57.0], wave=[(57.4, 59.0)],
         walk=[(1.5, 3.7), (14.0, 16.4), (26.0, 28.4), (38.6, 41.2), (50.0, 53.0)],
         turn=[(1.2, 0.4, PI / 2, "glide"), (4.0, 0.5, 0.25, "glide"), (13.6, 0.4, PI / 2, "glide"), (16.6, 0.5, 0.25, "glide"), (25.6, 0.4, PI / 2, "glide"), (28.6, 0.5, 0.0, "glide"),
               (38.2, 0.4, PI, "glide"), (41.4, 0.4, -PI / 2 - 0.2 + 2 * PI, "glide"), (53.2, 0.5, 2 * PI + 0.3, "glide")],
         move=[(1.5, 2.2, at("1"), "glide"), (14.0, 2.4, at("2"), "glide"), (26.0, 2.4, at("3"), "glide"), (38.6, 2.6, at("4"), "glide"), (50.0, 3.0, (0.55, Y, -0.38), "glide")], **J)
# square 1: the drawing — the brand price vs mine
w.card("t1a", (-0.6, Y + 0.2, 0.62), w=0.19, h=0.115, text="*€300–800*", sub="modellista", t=6.2, color="#8A4B2D", move=[(17.0, 0.5, (-0.62, -0.4, 0.35), "in")])
w.card("t1b", (-0.2, Y + 0.2, 0.62), w=0.19, h=0.115, text="*< €30*", sub="carta, matita, metro", t=9.8, color="#2F3A2E", move=[(17.0, 0.5, (-0.18, -0.4, 0.35), "in")])
w.prop("sketchdraw", "sk", (-0.4, Y + 0.002, 0.95), (0.3, 0.42), rot_x=0, t=9.8, reveal=[10.0, 13.0])
# square 2: the pattern
w.prop("patterncut", "pc", (0.4, Y + 0.003, 0.15), (0.4, 0.58), rot_y=1.57, t=17.0, cut=[18.0, 24.0])
w.card("t2", (0.55, Y + 0.12, 0.12), w=0.5, h=0.26, text="*tempo*, non €", t=20.5, color="#2F3A2E", move=[(29.0, 0.5, (0.62, -0.4, 0.35), "in")])
# square 3: photos — the shooting tag falls
w.card("t3a", (0.98, Y + 0.2, 0.62), w=0.21, h=0.12, text="*€3.000–8.000*", sub="shooting", t=30.0, color="#8A4B2D",
       move=[(34.6, 0.7, (1.0, Y + 0.02, 0.45), "in")], turn=[(34.6, 0.7, 0.0, "in")])
w.prop("laptop", "lap", (1.5, Y, 0.42), (0.34,), rot_y=-0.5, t=33.0)
# square 4: the twist — 10 then 20 of 100 light up
lit = [(43.0 + 0.12 * i, i) for i in range(10)] + [(46.5 + 0.08 * i, 10 + i) for i in range(10)]
w.prop("dotgrid", "g", (1.25, Y + 0.48, -0.78), (0.8, 0.8), cols=10, rows=10, pop=[39.8, 0.008], lit=lit, accent="#ffc23a")
# arrival: the Blender trouser
w.glb("tr", GLB, fit=0.7, pos=(0.05, Y, -0.6), rot_y=-0.25, double=True, fabric=True, t=48.5)
# the counter on the board edge (cards swap)
w.card("c0", (-1.45, Y + 0.12, -0.55), w=0.32, h=0.18, text="totale *€0*", rot_y=0.4, move=[(10.2, 0.4, (-1.45, -0.4, -0.55), "in")])
w.card("c1", (-1.45, Y + 0.12, -0.55), w=0.32, h=0.18, text="totale *< €30*", rot_y=0.4, t=10.4, move=[(53.6, 0.4, (-1.45, -0.4, -0.55), "in")])
w.card("c2", (0.1, Y + 0.3, -0.1), rot_y=0.15, w=0.36, h=0.18, text="*€500–1.500*", sub="tessuto, primo drop", t=54.0, move=[(58.0, 0.4, (0.1, -0.4, -0.1), "in")])
# the ask, inside the world, then the logo
w.prop("ctaplate", "cta", (0.3, Y, 0.2), (0.7, 0.24), text="Scrivi *PANTALONE*", t=58.2)
w.prop("logoplate", "logo2", (0.3, 0.62, -0.25), (0.8, 0.4), t=61.6)

C = [((-1.55, 0.36, 1.45), (-1.2, 0.14, 0.6)),
     (1.4, 2.4, (-0.62, 0.3, 1.38), (-0.4, 0.14, 0.6)),
     (5.0, 4.0, (-0.28, 0.3, 1.5), (-0.4, 0.17, 0.5)),
     (9.2, 4.4, (-0.5, 0.32, 1.5), (-0.4, 0.17, 0.5)),
     (13.8, 3.0, (0.4, 2.2, 1.45), (0.4, 0.0, 0.4)),
     (17.0, 8.6, (0.62, 1.7, 1.05), (0.4, 0.0, 0.45)),
     (25.8, 3.0, (0.95, 0.36, 1.45), (1.2, 0.14, 0.6)),
     (29.0, 5.4, (1.3, 0.3, 1.5), (1.12, 0.16, 0.5)),
     (34.6, 3.6, (1.4, 0.32, 1.55), (1.15, 0.15, 0.5)),
     (38.4, 3.2, (2.15, 0.7, 0.55), (1.15, 0.42, -0.65)),
     (41.8, 7.2, (0.45, 0.72, 0.55), (1.2, 0.46, -0.78)),
     (49.2, 3.8, (0.75, 0.62, 0.95), (0.1, 0.42, -0.55)),
     (53.2, 4.4, (0.32, 0.5, 0.78), (0.15, 0.42, -0.55)),
     (57.8, 3.2, (0.32, 0.36, 1.25), (0.3, 0.18, 0.2)),
     (61.2, 3.4, (0.3, 0.66, 1.15), (0.3, 0.62, -0.25))]
K = 1.6
far = lambda p, l: tuple(l[i] + (p[i] - l[i]) * K for i in range(3))
w.cam(far(*C[0]), C[0][1])
for t, d, p, l in C[1:]: w.cam(far(p, l), l, t=t, d=d)
w.dof(0.0, 65.0, aperture=0.012)

# ---- captions (word by word) + two big statements; text on screen the whole video
WORDS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "words.json"), encoding="utf-8"))
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
w.big(-0.3, 3.6, "Quanto costa|lanciare un *pantalone*?", top=240, size=80)
w.big(46.5, 50.0, "*10*, poi *20*|non cento", top=240, size=88)
chunks = [c for c in chunks if not (c[0] < 3.6 or (c[0] < 50.0 and c[1] > 46.5) or c[0] >= 58.4)]
w.captions(chunks, top=1180, size=96)
World3D.page("D:/ClaudeCodeTest/videos/_bench/short3/prev", [w], duration=65.0)
print("built")
