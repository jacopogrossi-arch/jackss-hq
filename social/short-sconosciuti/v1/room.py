# Short "sconosciuti" (18/11/2026): a street in Rome at night, NEW world (the Inverso shop window lit in the middle, two lamp posts that hold the comment cards).
# Same light language as the sample room (blue moon key, warm ambient), different place: cobbles, ochre palazzo, shutters, a lit shop window with the toy trouser inside.
import math
PI = math.pi
INK, GESSO, RUGGINE, BOSCO, SABBIA = "#1E1B18", "#EFE9DD", "#8A4B2D", "#2F3A2E", "#B9AE98"
OCRA, SHUTTER = "#8a6948", "#3e5a3b"
POLES = ((-1.9, -1.5), (2.5, -1.5))                          # lamp posts (x, z)


def furnish(w, trouser=None, flash_l=None, flash_r=None):
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
    # ---- the palazzo (19/11: more Roman): ochre plaster, a travertine rusticated base, string course, window frames with slatted green shutters, balconies, a deep cornice with brackets, terracotta eaves
    H = 8.8
    w.prop("wall", "facade", (0.5, 0, -3.9), (14, H, 0.3), color=OCRA, base="#6d4d30", rail=False, hole=[0.0, 1.35, 3.4, 2.3])
    for i, (px_, py_, pw_, ph_, pc_) in enumerate([(-4.6, 3.3, 1.6, 1.1, "#94683f"), (5.0, 5.9, 1.8, 1.3, "#7d5a36"), (-2.3, 6.3, 1.2, 0.8, "#9a6d42"), (3.2, 3.1, 1.1, 0.9, "#96693f"),
                                                    (-6.0, 7.3, 1.5, 1.0, "#835d38"), (6.4, 4.3, 1.2, 1.2, "#9b6e44")]):                 # weathered plaster patches
        w.solid("patch%d" % i, "box", (px_, py_, -3.745), (pw_, ph_, 0.01), color=pc_, rough=1.0)
    for bi, (bx, bw) in enumerate(((-3.85, 5.3), (4.85, 5.3))):                                                                     # base, left and right of the shop opening only
        w.solid("base%d" % bi, "box", (bx, 0.45, -3.74), (bw, 0.9, 0.1), color="#8d7c63", rough=0.9)                                           # travertine base with block joints
    for i in range(-9, 10):
        if abs(0.5 + i * 0.72 - 0.5) > 1.7:
            w.solid("bj%d" % i, "box", (0.5 + i * 0.72, 0.45, -3.685), (0.02, 0.9, 0.02), color="#4a3f31", rough=1.0)
    for bi, (bx, bw) in enumerate(((-3.85, 5.3), (4.85, 5.3))):
        w.solid("bj_h%d" % bi, "box", (bx, 0.45, -3.685), (bw, 0.02, 0.02), color="#4a3f31", rough=1.0)
        w.solid("bbase%d" % bi, "box", (bx, 0.92, -3.7), (bw, 0.05, 0.14), color="#a8996f", rough=0.8)
    w.solid("string", "box", (0.5, 3.5, -3.72), (14, 0.14, 0.14), color="#b9a77f", rough=0.85)                                         # string course
    w.solid("string2", "box", (0.5, 6.0, -3.72), (14, 0.12, 0.12), color="#b9a77f", rough=0.85)
    w.solid("cornice", "box", (0.5, H - 0.1, -3.62), (14, 0.28, 0.7), color="#b79a6b", rough=0.85)                                    # deep cornice + brackets (modillions)
    w.solid("cornice2", "box", (0.5, H - 0.32, -3.7), (14, 0.16, 0.5), color="#a8875f", rough=0.85)
    for i in range(-19, 20):
        w.solid("mod%d" % i, "box", (0.5 + i * 0.36, H - 0.5, -3.7), (0.16, 0.2, 0.3), color="#a8875f", rough=0.85)
    w.solid("eaves", "box", (0.5, H + 0.12, -3.5), (14.2, 0.22, 0.95), color="#9a4a2c", rough=0.9)                                    # terracotta eaves
    w.solid("eaves2", "box", (0.5, H + 0.36, -3.3), (14.2, 0.2, 0.6), color="#8a3f25", rough=0.9)
    w.solid("shopband", "box", (0.5, 2.75, -3.72), (3.9, 0.55, 0.12), color="#000000", rough=0.5)                                      # the fascia over the shop window
    w.card("fascia", (0.5, 2.75, -3.655), w=3.9, h=0.55, img="img/fascia.png", flat=True, color="#000000")
    w.solid("fframe", "box", (0.5, 2.43, -3.7), (3.9, 0.06, 0.1), color="#b9a77f", rough=0.8)
    for sx in (-1, 1):                                                                                                                    # pilasters either side of the shop window
        w.solid("pil%d" % sx, "box", (0.5 + sx * 1.95, 1.4, -3.68), (0.22, 2.8, 0.14), color="#9c8d68", rough=0.85)

    def win(k, x, y, lit, balcony, hh=1.5):
        w.solid("uw%d" % k, "box", (x, y, -3.72), (0.95, hh, 0.08), color="#ffcf8a" if lit else "#101626", rough=0.5)
        w.solid("mv%d" % k, "box", (x, y, -3.67), (0.03, hh, 0.03), color="#2a2018", rough=0.6)                                          # muntins
        w.solid("mh%d" % k, "box", (x, y + hh * 0.12, -3.67), (0.95, 0.03, 0.03), color="#2a2018", rough=0.6)
        for s_ in (-1, 1):                                                                                                                # stone jambs, slatted green shutters (open)
            w.solid("jb%d_%d" % (k, s_), "box", (x + s_ * 0.54, y, -3.68), (0.13, hh + 0.2, 0.12), color="#c9b896", rough=0.8)
            w.solid("sh%d_%d" % (k, s_), "box", (x + s_ * 0.82, y, -3.68), (0.4, hh + 0.05, 0.05), color=SHUTTER, rough=0.8)
            for j in range(6):
                w.solid("sl%d_%d_%d" % (k, s_, j), "box", (x + s_ * 0.82, y - hh / 2 + 0.2 + j * (hh - 0.3) / 5, -3.645), (0.34, 0.06, 0.03), color="#2f4a2d", rough=0.8)
        w.solid("lt%d" % k, "box", (x, y + hh / 2 + 0.12, -3.68), (1.2, 0.14, 0.14), color="#c9b896", rough=0.8)                          # lintel + cap
        w.solid("lc%d" % k, "box", (x, y + hh / 2 + 0.24, -3.66), (1.4, 0.07, 0.18), color="#d5c4a0", rough=0.8)
        w.solid("sill%d" % k, "box", (x, y - hh / 2 - 0.12, -3.62), (1.3, 0.08, 0.3), color="#c9b896", rough=0.8)
        if balcony:                                                                                                                          # wrought-iron balcony: slab, rail, bars, a pot of geraniums
            w.solid("bs%d" % k, "box", (x, y - hh / 2 - 0.2, -3.4), (1.5, 0.07, 0.62), color="#7a6b58", rough=0.8)
            w.solid("br%d" % k, "box", (x, y - hh / 2 + 0.38, -3.1), (1.5, 0.04, 0.04), color="#17130f", metal=0.5, rough=0.5)
            for j in range(9):
                w.solid("bb%d_%d" % (k, j), "box", (x - 0.7 + j * 0.175, y - hh / 2 + 0.12, -3.1), (0.025, 0.5, 0.025), color="#17130f", metal=0.5, rough=0.5)
            w.solid("gp%d" % k, "box", (x - 0.35, y - hh / 2 + 0.05, -3.3), (0.32, 0.18, 0.16), color="#a95f3b", rough=0.85)
            w.solid("gf%d" % k, "box", (x - 0.35, y - hh / 2 + 0.2, -3.3), (0.34, 0.12, 0.17), color="#c43c4a", rough=0.9)
    for k, x in enumerate((-5.4, -3.2, -0.9, 1.9, 4.1, 6.3)):                                                                                # first floor
        win(k, x, 4.55, k in (1, 4), k in (1, 3, 5))
    for k, x in enumerate((-5.4, -3.2, -0.9, 1.9, 4.1, 6.3)):                                                                                # second floor, a little shorter
        win(10 + k, x, 7.05, k in (2, 5), False, hh=1.35)
    w.solid("pipe", "cyl", (-1.15, 3.9, -3.52), (0.1, 7.6), color="#3b342c", metal=0.5, rough=0.6)                                       # drainpipe
    w.card("viaplaque", (-4.2, 2.9, -3.6), w=0.8, h=0.28, text="VIA DELL'*AGO*", size=64, color="#d9d2c3", ink="#2b2a27", key="#8a4b2d", flat=True)   # a marble street plaque, Roman style
    # ---- a Vespa parked on the right (mint), a Roman cliche that reads at once
    VX, VZ = 4.6, -0.25
    w.solid("vbody", "box", (VX, 0.42, VZ), (0.62, 0.34, 0.24), color="#9cc9b4", rough=0.5, metal=0.2, rot_y=0.5)
    w.solid("vleg", "box", (VX - 0.2, 0.55, VZ - 0.12), (0.16, 0.6, 0.3), color="#9cc9b4", rough=0.5, rot_y=0.5)
    w.solid("vseat", "box", (VX + 0.12, 0.64, VZ + 0.06), (0.34, 0.08, 0.2), color="#2a1f19", rough=0.7, rot_y=0.5)
    w.solid("vfw", "cyl", (VX - 0.3, 0.17, VZ - 0.18), (0.34, 0.1), color="#17130f", rough=0.8, rot_y=0.5)
    w.solid("vbw", "cyl", (VX + 0.26, 0.17, VZ + 0.12), (0.34, 0.1), color="#17130f", rough=0.8, rot_y=0.5)
    w.solid("vbar", "box", (VX - 0.28, 0.98, VZ - 0.16), (0.08, 0.04, 0.4), color="#d9d2c3", metal=0.6, rough=0.4, rot_y=0.5)
    w.solid("vhl", "sphere", (VX - 0.4, 0.88, VZ - 0.23), (0.1,), color="#fff1c8", rough=0.2)
    # ---- inside the shop: warm back wall, a lit floor, the toy trouser on a pedestal
    w.solid("shopback", "box", (0.5, 1.6, -5.2), (3.6, 3.2, 0.1), color="#3a2a20", rough=0.9)
    w.solid("shopfloor", "box", (0.5, 0.02, -4.55), (3.6, 0.04, 1.8), color="#2b2018", rough=0.7)
    w.solid("shopped", "cyl", (0.5, 0.2, -4.6), (0.7, 0.4), color=GESSO, rough=0.7)
    w.prop("pendant", "shoplight", (0.5, 2.5, -4.3), (1.0,), color=INK, light=6, glow=1.1, glowColor="#ffffff", tint="#ffffff")   # the same white as the glow below
    w.card("plaque", (0.5, 0.22, -4.22), w=0.5, h=0.12, text="*DROP 1*", sub=None, size=60, color="#16120f", ink=GESSO, key="#d9b36a", flat=True)   # a small plaque on the pedestal
    w.prop("uplight", "shopglow", (0.5, 0.0, -4.5), (1.15,), glowColor="#ffffff", light=3.2, glow=0.5)                       # white glow from below, like a lit shop window
    if trouser: w.glb("shoptr", trouser, fit=1.5, pos=(0.5, 0.4, -4.6), rot_y=0.15, double=True)
    # ---- two lamp posts: a pole, an arm, a hanging lamp that really lights the street
    for i, (px, pz) in enumerate(POLES):
        w.solid("pole%d" % i, "cyl", (px, 1.6, pz), (0.09, 3.2), color=INK, metal=0.7, rough=0.5)
        w.solid("polefoot%d" % i, "cyl", (px, 0.15, pz), (0.2, 0.3), color=INK, metal=0.6, rough=0.5)
        w.solid("arm%d" % i, "box", (px + (0.35 if px < 0 else -0.35), 3.12, pz), (0.7, 0.05, 0.05), color=INK, metal=0.7, rough=0.5)
        col = "#3dff8a" if px < 0 else "#ff4a3a"                                                                    # left lamp = confirmations (green), right = slaps (red), steady for the whole video
        w.prop("pendant", "lamp%d" % i, (px + (0.7 if px < 0 else -0.7), 3.0, pz), (0.3,), color=INK, light=5, glow=1.0, glowColor=col, tint=col)
    w.solid("bench", "box", (-4.2, 0.28, -1.6), (1.4, 0.06, 0.45), color="#5a4330", rough=0.8)
    w.prop("plant", "plant1", (4.8, 0.12, -2.6), (1.3,))
    w.prop("plant", "plant2", (-3.1, 0.12, -2.8), (1.1,))
    return w
