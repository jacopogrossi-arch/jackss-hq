# The Inverso sample room at night (16/11/2026, Short #3): a third world in the language of the night studio (Short #2), NEW room and objects.
# Dark rust plaster walls, a terrazzo floor, a black steel window on Rome, warm pendants. Four stations (drawing desk, cutting table, photo set, pre-order wall) + a hero rail.
import math
PI = math.pi
BOSCO, INK, GESSO, RUGGINE, SABBIA, PLASTER = "#2F3A2E", "#1E1B18", "#EFE9DD", "#8A4B2D", "#B9AE98", "#3a2923"
WIN = (-1.6, 1.8, 1.9, 2.1)          # window: centre x, centre y, width, height (back wall, left)


def furnish(w, hide=None, hide2=None):
    H = {"hide": hide} if hide else {}
    H2 = {"hide": (hide or []) + (hide2 or [])}
    w.room(bg="#07090c", key="#9fb4ff", dir=(-3.0, 3.4, -9.0), key_i=1.35, aim=(0.4, 0.4, 0.2), hemi=("#ffd9a8", "#151210"), hemi_i=0.8, side_i=0.8,
           rim="#7f9be0", rim_i=0.5, box=(10, 7, 40), fog=("#07090c", 16, 42), exposure=1.6)
    P = w.prop
    P("terrazzo", "floor", (0.5, 0, 0.75), (9.4, 8.4))
    cx = WIN[0] - 0.5
    P("wall", "wback", (0.5, 0, -3.1), (9.4, 3.4, 0.2), color=PLASTER, base=INK, hole=[cx, WIN[1], WIN[2], WIN[3]])
    P("wall", "wleft", (-4.1, 0, 0.75), (8.4, 3.4, 0.2), rot_y=PI / 2, color=PLASTER, base=INK)
    P("wall", "wright", (5.1, 0, 0.75), (8.4, 3.4, 0.2), rot_y=PI / 2, color=PLASTER, base=INK)
    P("crittall", "win", (WIN[0], WIN[1], -3.08), (WIN[2], WIN[3]), cols=4, rows=5)
    P("cityview", "city", (WIN[0], -1.0, -6.5), (14, 7), dim=0.95)
    # --- back wall: window (left), the pre-order wall (right, in build.py), palette between
    P("swatchwall", "palette", (-3.2, 1.5, -2.99), (0.85, 1.15))
    P("bookshelf", "books", (4.3, 0, -2.83), (1.3, 2.2, 0.34), seed=7)
    P("wallclock", "clock", (-3.2, 2.75, -3.0), (0.42,))
    P("plant", "plant1", (4.6, 0, -2.5), (1.5,))
    P("plant", "plant2", (-3.7, 0, 1.9), (1.15,))
    P("rollrack", "rr", (-3.85, 0, -0.6), (2.0, 1.6, 0.5), rot_y=PI / 2)
    # --- station 1: the drawing desk
    P("rug", "rug1", (-2.5, 0, 0.5), (3.0, 2.4), color=SABBIA)
    P("table", "tableA", (-2.5, 0, 0.2), (2.0, 0.9, 1.0), color="#7a5236")
    P("deskset", "desk", (-1.7, 0.9, 0.0), rot_y=-0.3)
    P("desklamp", "dlamp", (-3.3, 0.9, -0.1), rot_y=0.4, color=INK)
    P("ruler", "tape", (-3.25, 0.905, 0.65), (0.5, 0.03), rot_y=1.35)
    P("pendant", "pend1", (-2.5, 2.2, 0.2), (1.5,), color=RUGGINE, light=4.5, **H)
    # --- station 2: the cutting table
    P("table", "tableB", (0.5, 0, 0.95), (2.7, 0.9, 1.3), color="#6b4a30")
    P("cuttingmat", "mat", (0.5, 0.905, 0.95), (2.1, 1.0))
    P("shears", "shears0", (1.65, 0.915, 1.4), rot_y=0.5)
    P("pendant", "pend2", (0.5, 2.3, 0.95), (1.5,), color=INK, light=4.5, **H2)
    # --- station 3: the photo set (backdrop on two stands, softbox, tripod + camera)
    S = (3.5, 0.0, 0.5)
    w.solid("bdpaper", "box", (S[0], 1.05, S[2] - 1.15), (2.3, 2.1, 0.02), color="#b9ae98", rough=0.95)
    w.solid("bdroll", "cyl", (S[0], 2.12, S[2] - 1.13), (0.1, 2.4), color="#d8cfbd", rough=0.9, rot_y=0)
    for i, sx in enumerate((-1.2, 1.2)):
        w.solid("bdstand%d" % i, "cyl", (S[0] + sx, 1.1, S[2] - 1.15), (0.04, 2.2), color=INK, metal=0.8, rough=0.4)
        w.solid("bdfoot%d" % i, "cyl", (S[0] + sx, 0.02, S[2] - 1.15), (0.5, 0.04), color=INK, metal=0.8, rough=0.4)
    w.solid("sbox", "box", (S[0] - 1.3, 1.5, S[2] + 0.1), (0.62, 0.8, 0.4), color=INK, rough=0.6, rot_y=0.7)
    w.solid("sface", "box", (S[0] - 1.1, 1.5, S[2] + 0.28), (0.5, 0.68, 0.02), color="#fff3d6", rough=1.0, rot_y=0.7)
    w.solid("sstand", "cyl", (S[0] - 1.3, 0.7, S[2] + 0.1), (0.035, 1.4), color=INK, metal=0.8, rough=0.4)
    w.solid("sfoot", "cyl", (S[0] - 1.3, 0.02, S[2] + 0.1), (0.5, 0.04), color=INK, metal=0.8, rough=0.4)
    w.solid("tripod", "cyl", (S[0] + 0.5, 0.65, S[2] + 1.2), (0.035, 1.3), color=INK, metal=0.8, rough=0.4)
    w.solid("tripodf", "cyl", (S[0] + 0.5, 0.02, S[2] + 1.2), (0.55, 0.04), color=INK, metal=0.8, rough=0.4)
    w.solid("cambody", "box", (S[0] + 0.5, 1.4, S[2] + 1.2), (0.3, 0.2, 0.18), color="#2a2a2e", rough=0.4, metal=0.5, rot_y=PI + 0.35)
    w.solid("camlens", "cyl", (S[0] + 0.46, 1.4, S[2] + 1.07), (0.12, 0.14), color="#101012", rough=0.2, metal=0.6, rot_y=0.0)
    P("pendant", "pend3", (S[0], 2.5, S[2] + 0.2), (1.1,), color=RUGGINE, light=7, **H)
    P("mannequin", "man1", (S[0] - 0.1, 0, S[2] - 0.5), rot_y=-0.4)
    # --- station 5: the hero rail (arrival)
    P("rug", "rugH", (1.0, 0, 2.7), (2.4, 1.7), color=BOSCO)
    P("pendant", "pend5", (1.0, 2.7, 2.5), (1.1,), color=RUGGINE, light=7, **H)
    P("bolts", "bolts1", (-3.8, 0, 2.4), (0.6, 0.45), n=6, seed=4, rot_y=PI / 2, palette=["#6f7452", BOSCO, RUGGINE, SABBIA, GESSO, INK])
    return w
