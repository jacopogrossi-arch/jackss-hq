# lab2.py: prova dei prodotti v2 e della macchina nuova (un'inquadratura al secondo), senza voce.
import os, sys, shutil, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "D:/ClaudeCodeTest/.claude/skills/youtube-edit/formats"); sys.path.insert(0, HERE)
from world3d import World3D
from store import add_store, room, REALE_CSS
SHOTS = [((-2.75, 0.75, 0.9), (-1.9, 0.45, 0.0)),        # giocattoli, altezza bambino
         ((-1.0, 1.1, -1.5), (0.1, 0.8, -1.2)),           # tipici, da vicino
         ((-0.9, 2.1, -0.2), (0.1, 1.75, 0.2)),           # salami appesi
         ((1.1, 1.0, 1.0), (2.1, 0.7, 0.6)),              # dolci da vicino
         ((1.1, 1.6, -2.6), (2.1, 0.8, -0.5)),            # dolci, corsia
         ((5.4, 1.4, 0.6), (4.25, 0.95, 1.9)),            # cassa
         ((-2.0, 1.2, 14.0), (-7.5, 0.6, 8.2)),           # auto parcheggiate
         ((-9.0, 0.9, 22.0), (-12.6, 0.6, 8.2))]
w = room(World3D("w1", 0.0, len(SHOTS) * 1.0 + 0.5, fov=40, fade=0.01), "reale")
add_store(w, "reale")
w._obj("box", "grass", (0, -0.06, 20), 0, None, None, None, size=[700, 0.1, 500], color="#ffffff", rough=1.0, tex="grass")
w._obj("road", "park", (0, 0.0, 13.5), 0, None, None, None, size=[62.4, 17], rk="parking")
for k, (x, z, c, ry) in enumerate(((-12.6, 8.2, "#e9e6df", math.pi / 2), (-7.4, 8.2, "#2f3b4a", math.pi / 2), (-10.0, 12.0, "#d2232a", 0.3))):
    w._obj("car", "pk%d" % k, (x, 0, z), ry, None, None, None, color=c)
w.cam(SHOTS[0][0], look=SHOTS[0][1])
for i, (p, l) in enumerate(SHOTS[1:], 1):
    w.cam(p, look=l, t=i * 1.0, d=0.05)
f = os.path.join(HERE, "lab-v2")
World3D.page(f, [w])
shutil.copy(os.path.join(HERE, "vendor", "world3d.js"), os.path.join(f, "vendor", "world3d.js"))
p = os.path.join(f, "index.html"); s = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write(s.replace("</head>", REALE_CSS % ("w1", "w1", "w1") + "</head>"))
print("ok", ",".join("%.1f" % (i + 0.5) for i in range(len(SHOTS))))
