# Short "sconosciuti" (18/11/2026): a street in Rome at night, NEW world (the Inverso shop window lit in the middle, two lamp posts that hold the comment cards).
# Same light language as the sample room (blue moon key, warm ambient), different place: cobbles, ochre palazzo, shutters, a lit shop window with the toy trouser inside.
import math
PI = math.pi
INK, GESSO, RUGGINE, BOSCO, SABBIA = "#1E1B18", "#EFE9DD", "#8A4B2D", "#2F3A2E", "#B9AE98"
OCRA, SHUTTER = "#8a6948", "#3e5a3b"
POLES = ((-1.9, -1.5), (2.5, -1.5))                          # lamp posts (x, z)


def furnish(w, trouser=None):
    w.room(bg="#07090c", key="#9fb4ff", dir=(-3.0, 3.4, -9.0), key_i=1.35, aim=(0.4, 0.4, -1.0), hemi=("#ffd9a8", "#151210"), hemi_i=0.8, side_i=0.8,
           rim="#7f9be0", rim_i=0.5, box=(12, 8, 40), fog=("#07090c", 16, 42), exposure=1.6)
    # ---- ground: dark cobbles (a slab + a grid of paving joints) and a raised pavement along the palazzo
    w.solid("ground", "box", (0.5, -0.03, 3.5), (16, 0.06, 24), color="#3d3732", rough=0.96)
    for i in range(-18, 22):
        w.solid("jx%d" % i, "box", (0.5 + i * 0.36, 0.004, 3.5), (0.02, 0.008, 24), color="#26221f", rough=1.0)
    for j in range(-6, 56):
        w.solid("jz%d" % j, "box", (0.5, 0.004, -8.0 + j * 0.36), (16, 0.008, 0.02), color="#26221f", rough=1.0)
    w.solid("pave", "box", (0.5, 0.06, -2.6), (14, 0.12, 2.6), color="#6b6357", rough=0.9)
    w.solid("kerb", "box", (0.5, 0.06, -1.27), (14, 0.12, 0.08), color="#8a8174", rough=0.8)
    # ---- the palazzo: ochre wall with the big shop-window opening (centre), cornice, lit and shuttered upper windows
    w.prop("wall", "facade", (0.5, 0, -3.9), (14, 6.2, 0.3), color=OCRA, base="#6d4d30", rail=False, hole=[0.0, 1.35, 3.4, 2.3])
    w.solid("cornice", "box", (0.5, 6.1, -3.7), (14, 0.22, 0.5), color="#a8875f", rough=0.85)
    w.solid("shopband", "box", (0.5, 2.75, -3.72), (3.9, 0.55, 0.12), color="#16120f", rough=0.5)          # the fascia over the shop window (the sign goes here)
    for k, x in enumerate((-5.2, -3.0, -0.9, 1.9, 4.0, 6.0)):                                              # upper windows: dark glass or warm light, green shutters
        lit = k in (1, 4)
        w.solid("uw%d" % k, "box", (x, 4.55, -3.72), (0.95, 1.5, 0.08), color="#ffcf8a" if lit else "#141a2c", rough=0.6)
        for s in (-1, 1):
            w.solid("sh%d_%d" % (k, s), "box", (x + s * 0.62, 4.55, -3.7), (0.38, 1.55, 0.06), color=SHUTTER, rough=0.8)
        w.solid("ws%d" % k, "box", (x, 3.78, -3.62), (1.15, 0.06, 0.25), color="#7a6b58", rough=0.8)
    # ---- inside the shop: warm back wall, a lit floor, the toy trouser on a pedestal
    w.solid("shopback", "box", (0.5, 1.6, -5.2), (3.6, 3.2, 0.1), color="#3a2a20", rough=0.9)
    w.solid("shopfloor", "box", (0.5, 0.02, -4.55), (3.6, 0.04, 1.8), color="#2b2018", rough=0.7)
    w.solid("shopped", "cyl", (0.5, 0.2, -4.6), (0.7, 0.4), color=GESSO, rough=0.7)
    w.prop("pendant", "shoplight", (0.5, 2.5, -4.3), (1.0,), color=RUGGINE, light=7, glow=1.1)
    if trouser: w.glb("shoptr", trouser, fit=0.95, pos=(0.5, 0.4, -4.6), rot_y=0.15, double=True)
    # ---- two lamp posts: a pole, an arm, a hanging lamp that really lights the street
    for i, (px, pz) in enumerate(POLES):
        w.solid("pole%d" % i, "cyl", (px, 1.6, pz), (0.09, 3.2), color=INK, metal=0.7, rough=0.5)
        w.solid("polefoot%d" % i, "cyl", (px, 0.15, pz), (0.2, 0.3), color=INK, metal=0.6, rough=0.5)
        w.solid("arm%d" % i, "box", (px + (0.35 if px < 0 else -0.35), 3.12, pz), (0.7, 0.05, 0.05), color=INK, metal=0.7, rough=0.5)
        w.prop("pendant", "lamp%d" % i, (px + (0.7 if px < 0 else -0.7), 3.0, pz), (0.3,), color=INK, light=6, glow=1.0)
    w.solid("bench", "box", (-4.2, 0.28, -1.6), (1.4, 0.06, 0.45), color="#5a4330", rough=0.8)
    w.prop("plant", "plant1", (4.8, 0.12, -2.6), (1.3,))
    w.prop("plant", "plant2", (-3.1, 0.12, -2.8), (1.1,))
    return w
