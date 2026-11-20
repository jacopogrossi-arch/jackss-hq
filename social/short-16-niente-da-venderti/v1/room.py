# Short #16 «Non ho niente da venderti» (v2, 20/11/2026): a market square at dawn. One wooden stall seen FRONTALLY: dark cloth at the back (contrast for the
# narrator and the trouser), striped awning, a clothesline under the awning where the fact cards hang, two pedestals on the counter (left: the trouser, right: the notebook).
import math
PI = math.pi
INK, GESSO, RUGGINE, BOSCO, SABBIA = "#1E1B18", "#EFE9DD", "#8A4B2D", "#2F3A2E", "#B9AE98"
TOP = 0.8                                                    # counter top (y)
STALL = (0.0, -1.5)                                          # centre of the counter (x, z)
Y = TOP + 0.06                                               # surface of the counter
LINE_Y = 2.0                                                 # the clothesline under the awning
LINE_Z = STALL[1] + 0.52                                     # front posts
PED_L, PED_R = (-0.95, STALL[1] + 0.1), (0.95, STALL[1] + 0.1)
PED_H = 0.1


def furnish(w):
    w.room(bg="#d8a283", key="#ffc08a", dir=(3.0, 3.6, 8.0), key_i=2.2, aim=(0.0, 1.0, -1.5), hemi=("#ffe0c8", "#2c2630"), hemi_i=0.85, side_i=0.5,
           rim="#9db8ff", rim_i=0.9, box=(8, 6, 30), fog=("#d8a283", 12, 40), exposure=1.3)
    # ---- ground: stone slabs, darker than the stall so the stall reads
    w.solid("ground", "box", (0.0, -0.03, 2.0), (18, 0.06, 28), color="#6c635a", rough=0.95)
    for i in range(-24, 25):
        w.solid("jx%d" % i, "box", (i * 0.5, 0.004, 2.0), (0.02, 0.008, 28), color="#4a433d", rough=1.0)
    for j in range(-8, 52):
        w.solid("jz%d" % j, "box", (0.0, 0.004, -9.0 + j * 0.5), (18, 0.008, 0.02), color="#4a433d", rough=1.0)
    # ---- the square behind, still in the shade of dawn: dark plaster facades, a few lit windows, symmetric around x = 0
    for k, (bx, bw, bh, col) in enumerate(((-5.4, 5.0, 8.0, "#5b4842"), (0.0, 5.8, 9.4, "#4e4246"), (5.4, 5.0, 8.0, "#5b4842"))):
        w.solid("bld%d" % k, "box", (bx, bh / 2, -6.4), (bw, bh, 0.6), color=col, rough=0.95)
        w.solid("cor%d" % k, "box", (bx, bh - 0.1, -6.0), (bw + 0.2, 0.26, 0.5), color="#7d6a5c", rough=0.85)
        for r in range(3):
            for c in range(3):
                wx, wy = bx - bw / 2 + 0.9 + c * (bw - 1.8) / 2, 2.4 + r * 2.1
                lit = (k, r, c) in ((0, 1, 2), (1, 2, 0), (2, 0, 1), (1, 1, 2))
                w.solid("w%d_%d_%d" % (k, r, c), "box", (wx, wy, -6.07), (0.8, 1.2, 0.06), color="#ffcf8a" if lit else "#2a2326", rough=0.6)
                w.solid("ws%d_%d_%d" % (k, r, c), "box", (wx, wy - 0.7, -6.0), (1.0, 0.08, 0.2), color="#7d6a5c", rough=0.85)
    # ---- the stall
    sx, sz = STALL
    w.solid("counter", "box", (sx, TOP / 2, sz), (3.4, TOP, 1.1), color="#9a6b42", rough=0.8)
    w.solid("ctop", "box", (sx, TOP + 0.03, sz), (3.5, 0.06, 1.2), color="#c08d5a", rough=0.7)
    for i in range(-5, 6):
        w.solid("plank%d" % i, "box", (sx + i * 0.3, TOP / 2, sz + 0.56), (0.02, TOP - 0.06, 0.02), color="#6a4a2e", rough=0.9)
    for ix in (-1.7, 1.7):
        for iz in (sz - 0.52, sz + 0.52):
            w.solid("post_%d_%d" % (ix * 10, iz * 10), "box", (ix, 1.15, iz), (0.08, 2.3, 0.08), color="#5f432a", rough=0.85)
    w.solid("backcloth", "box", (sx, (TOP + 2.28) / 2, sz - 0.5), (3.32, 2.28 - TOP, 0.03), color="#25272d", rough=0.95)   # dark cloth at the back: the contrast
    w.solid("beam", "box", (sx, 2.28, sz + 0.52), (3.6, 0.09, 0.09), color="#5f432a", rough=0.85)
    for i in range(10):
        w.solid("aw%d" % i, "box", (sx - 1.62 + i * 0.36, 2.32, sz), (0.36, 0.05, 1.3), color=RUGGINE if i % 2 == 0 else GESSO, rough=0.9)
        w.solid("awf%d" % i, "box", (sx - 1.62 + i * 0.36, 2.2, sz + 0.66), (0.36, 0.22, 0.04), color=RUGGINE if i % 2 == 0 else GESSO, rough=0.9)
    w.solid("line", "box", (sx, LINE_Y, LINE_Z), (3.4, 0.012, 0.012), color="#e8dcc4", rough=0.9)                    # the clothesline for the cards
    # ---- two pedestals on the counter: left empty at first (the trouser comes), right holds the notebook (the "document")
    for k, (px, pz) in enumerate((PED_L, PED_R)):
        w.solid("ped%d" % k, "cyl", (px, Y + PED_H / 2, pz), (0.42, PED_H), color=GESSO, rough=0.7)
    nx, nz = PED_R
    w.solid("nb", "box", (nx, Y + PED_H + 0.02, nz), (0.3, 0.04, 0.22), color="#e8dfc9", rough=0.8)
    w.solid("nbspine", "box", (nx - 0.14, Y + PED_H + 0.021, nz), (0.03, 0.043, 0.22), color=RUGGINE, rough=0.8)
    w.solid("pen", "cyl", (nx + 0.02, Y + PED_H + 0.05, nz + 0.05), (0.012, 0.2), color=INK, rough=0.5, rot_y=0.4)
    # ---- props at the sides of the square (never between the camera and the stall)
    for i, (cx, cz, s) in enumerate(((-2.5, -1.3, 0.5), (-2.5, -1.3 + 0.0, 0.5), (2.5, -1.3, 0.5), (-3.2, -2.4, 0.45), (3.2, -2.4, 0.45))):
        w.solid("crate%d" % i, "box", (cx, s / 2 + (0.5 if i == 1 else 0), cz), (s, s, s), color="#a77b4c", rough=0.9, rot_y=0.15 * (i % 2))
    w.prop("plant", "plant1", (-3.0, 0.0, -3.4), (1.3,))
    w.prop("plant", "plant2", (3.0, 0.0, -3.4), (1.3,))
    return w
