"""Scena di esempio: narratore + i 7 oggetti 3D in stile giocattolo (17/11/2026), con la luce notturna dello Short #3.
Si copia, si cambia la lista OBJ (nome, file, altezza in metri) e si usa nel build.py di uno Short al posto di `w.glb(...)`.
Render di prova (2 s): python -I scena-oggetti.py  ->  npx hyperframes@0.9.35 render comp --quality draft --fps 24 --workers 2 -o prova.mp4
I GLB stanno in D:/ClaudeCodeTest/videos/_bench/assets3d/finali/ (locale, fuori da git: pesano ~12 MB l'uno)."""
import os, sys
sys.path.insert(0, "D:/ClaudeCodeTest/.claude/skills/fashion-3d/engine")
from world3d import World3D
F = "D:/ClaudeCodeTest/videos/_bench/assets3d/finali/"
NARRATORE = "D:/ClaudeCodeTest/social/short-03-tabellone/assets/action-figure-perf.glb"
# nome, file, altezza in metri (a occhio nella prova: le scale vere si fissano per scena), rot_y
OBJ = [("laptop", "laptop.glb", 0.35), ("fotocamera", "fotocamera.glb", 0.5), ("macchina", "macchina-da-cucire.glb", 0.42), ("pantalone", "pantalone.glb", 0.75),
       ("rotoli", "rotoli-tessuto.glb", 0.32), ("forbici", "forbici.glb", 0.04), ("manichino", "manichino.glb", 0.7)]   # forbici: piatte, si scalano per altezza minuscola e si vedono dall'alto
w = World3D("s", 0.0, 2.0, fov=34, w=1920, h=1080, fade=0.1)
w.room(bg="#07090c", key="#9fb4ff", dir=(-3.0, 3.4, -9.0), key_i=1.35, aim=(0.4, 0.4, 0.2), hemi=("#ffd9a8", "#151210"), hemi_i=0.8, side_i=0.8,
       rim="#7f9be0", rim_i=0.5, box=(10, 7, 40), fog=("#07090c", 16, 42), exposure=1.6)                          # stessa luce di short-03-tabellone/v8/room.py
w.glb("me", NARRATORE, fit=0.6, pos=(-2.0, 0.0, 0.3), rot_y=0.3, recv=False, segs=[[0.0, 2.0, 1, 1.0, 1.0]], segFade=0.1, clipSpeed=1.0, bob=0)   # recv=False: niente "pixel" sul viso
for k, (n, f, h) in enumerate(OBJ):
    w.glb(n, F + f, fit=h, pos=(-1.2 + k * 0.62, 0.0, 0.0), rot_y=-0.35, double=True)
w.cam((0.3, 0.6, 4.6), (0.3, 0.3, 0.0))
print(World3D.page(os.path.join(os.path.dirname(os.path.abspath(__file__)), "comp"), [w], duration=2.0))
