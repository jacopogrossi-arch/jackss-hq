# Short #16 «Non ho niente da venderti» (20/11/2026): a market square at dawn, NEW world. One empty wooden stall (striped awning), a sign «IN VENDITA» that turns into «IN CORSO».
import math
PI = math.pi
INK, GESSO, RUGGINE, BOSCO, SABBIA = "#1E1B18", "#EFE9DD", "#8A4B2D", "#2F3A2E", "#B9AE98"
TOP = 0.8                                                    # counter top (y)
STALL = (0.0, -1.5)                                          # centre of the counter (x, z)


def furnish(w, trouser=None):
    w.room(bg="#e9b896", key="#ffb27a", dir=(5.0, 3.2, 7.0), key_i=2.1, aim=(0.0, 0.6, -1.5), hemi=("#ffe3cc", "#4a3a44"), hemi_i=1.05, side_i=0.7,
           rim="#9db8ff", rim_i=0.6, box=(12, 8, 40), fog=("#efc3a2", 14, 44), exposure=1.35)
    # ---- ground: pale stone slabs with joints
    w.solid("ground", "box", (0.0, -0.03, 2.0), (18, 0.06, 28), color="#9b8f80", rough=0.95)
    for i in range(-24, 25):
        w.solid("jx%d" % i, "box", (i * 0.5, 0.004, 2.0), (0.02, 0.008, 28), color="#6f6559", rough=1.0)
    for j in range(-8, 52):
        w.solid("jz%d" % j, "box", (0.0, 0.004, -9.0 + j * 0.5), (18, 0.008, 0.02), color="#6f6559", rough=1.0)
    # ---- the buildings closing the square: three plaster facades, windows, a cornice
    for k, (bx, bw, bh, col) in enumerate(((-5.2, 5.4, 8.0, "#c98d5c"), (0.2, 5.6, 9.2, "#d9b48a"), (5.6, 5.4, 7.4, "#b97550"))):
        w.solid("bld%d" % k, "box", (bx, bh / 2, -6.2), (bw, bh, 0.6), color=col, rough=0.95)
        w.solid("cor%d" % k, "box", (bx, bh - 0.1, -5.8), (bw + 0.2, 0.26, 0.5), color="#e3cfa8", rough=0.85)
        for r in range(3):
            for c in range(3):
                wx, wy = bx - bw / 2 + 0.9 + c * (bw - 1.8) / 2, 2.2 + r * 2.1
                w.solid("w%d_%d_%d" % (k, r, c), "box", (wx, wy, -5.87), (0.8, 1.2, 0.06), color="#7a5638" if (r + c + k) % 3 else "#ffd9a0", rough=0.6)
                w.solid("ws%d_%d_%d" % (k, r, c), "box", (wx, wy - 0.7, -5.8), (1.0, 0.08, 0.2), color="#e3cfa8", rough=0.85)
    # ---- the stall: counter, front planks, four posts, striped awning
    sx, sz = STALL
    w.solid("counter", "box", (sx, TOP / 2, sz), (3.4, TOP, 1.1), color="#8a6240", rough=0.8)
    w.solid("ctop", "box", (sx, TOP + 0.03, sz), (3.5, 0.06, 1.2), color="#b58557", rough=0.7)
    for i in range(-5, 6):
        w.solid("plank%d" % i, "box", (sx + i * 0.3, TOP / 2, sz + 0.56), (0.02, TOP - 0.06, 0.02), color="#5f432a", rough=0.9)
    for ix in (-1.7, 1.7):
        for iz in (sz - 0.52, sz + 0.52):
            w.solid("post_%s_%s" % (ix, iz), "box", (ix, 1.15, iz), (0.08, 2.3, 0.08), color="#5f432a", rough=0.85)
    w.solid("beam", "box", (sx, 2.28, sz + 0.52), (3.6, 0.09, 0.09), color="#5f432a", rough=0.85)
    for i in range(10):
        w.solid("aw%d" % i, "box", (sx - 1.62 + i * 0.36, 2.3, sz), (0.36, 0.05, 1.3), color=RUGGINE if i % 2 == 0 else GESSO, rough=0.9)
    for i in range(10):
        w.solid("awf%d" % i, "box", (sx - 1.62 + i * 0.36, 2.18, sz + 0.66), (0.36, 0.22, 0.04), color=RUGGINE if i % 2 == 0 else GESSO, rough=0.9)
    # ---- around the stall: crates, a barrel, plants
    for i, (cx, cz, s) in enumerate(((-2.6, -1.2, 0.5), (-2.55, -0.6, 0.42), (2.7, -1.0, 0.55), (-3.4, -2.2, 0.5))):
        w.solid("crate%d" % i, "box", (cx, s / 2, cz), (s, s, s), color="#a77b4c", rough=0.9, rot_y=0.3 * i)
    w.solid("barrel", "cyl", (3.1, 0.35, -1.9), (0.6, 0.7), color="#6b4a30", rough=0.85)
    w.prop("plant", "plant1", (-2.2, 0.0, 0.2), (1.3,))
    w.prop("plant", "plant2", (2.6, 0.0, 0.3), (1.1,))
    return w
