# The Inverso studio at night (13/11/2026, Short #2): a second world next to the atelier of Short #1.
# Bosco-green walls, a terrazzo floor, a black steel factory window on Rome at night, warm pendants, books, a cork board, the palette on the wall.
# furnish(w, hide=...) fills a World3D; `hide` = spans when the pendants fade out (the camera flies up to the map through them).
import math
PI = math.pi
BOSCO, INK, GESSO, RUGGINE, SABBIA = "#2F3A2E", "#1E1B18", "#EFE9DD", "#8A4B2D", "#B9AE98"
WIN = (3.6, 1.75, 2.4, 2.0)          # window: centre x, centre y, width, height (back wall)


def furnish(w, hide=None):
    H = {"hide": hide} if hide else {}
    w.room(bg="#07090c", key="#9fb4ff", dir=(3.4, 3.2, -9.0), key_i=1.45, aim=(2.6, 0.4, 0.2), hemi=("#ffd9a8", "#151210"), hemi_i=0.42, side_i=0.55,
           rim="#7f9be0", rim_i=0.5, box=(10, 7, 40), fog=("#07090c", 16, 42), exposure=1.18)
    P = w.prop
    P("terrazzo", "floor", (0.5, 0, 0.75), (9.4, 8.4))
    cx = WIN[0] - 0.5                                                                  # the wall's centre is x = 0.5
    P("wall", "wback", (0.5, 0, -3.1), (9.4, 3.4, 0.2), color=BOSCO, base=INK, hole=[cx, WIN[1], WIN[2], WIN[3]])
    P("wall", "wleft", (-4.1, 0, 0.75), (8.4, 3.4, 0.2), rot_y=PI / 2, color=BOSCO, base=INK)
    P("wall", "wright", (5.1, 0, 0.75), (8.4, 3.4, 0.2), rot_y=PI / 2, color=BOSCO, base=INK)
    P("crittall", "win", (WIN[0], WIN[1], -3.08), (WIN[2], WIN[3]), cols=6, rows=4)
    P("cityview", "city", (WIN[0], -1.2, -6.5), (14, 7), dim=0.95)
    # --- back wall, left to right: books, cork board, palette, clock, window
    P("bookshelf", "books", (-3.15, 0, -2.83), (1.55, 2.3, 0.34), seed=3)
    P("pinboard", "board", (-1.35, 1.6, -3.0), (1.5, 1.0), items=[
        dict(x=-0.72, y=0.55, w=0.22, h=0.16, swatch="#6f7452", rot=0.05), dict(x=-0.35, y=0.62, w=0.2, h=0.27, text="vita *alta*", lines=True, rot=-0.04),
        dict(x=0.62, y=0.6, w=0.24, h=0.17, swatch="#2F3A2E", kind="linen", rot=-0.06), dict(x=0.78, y=-0.55, w=0.18, h=0.24, text="Drop 1", sub="pre-order", rot=0.07),
        dict(x=-0.8, y=-0.62, w=0.19, h=0.13, swatch="#8A4B2D", rot=-0.08)],
      cards=getattr(w, "board_cards", []))
    P("swatchwall", "palette", (0.42, 1.55, -2.99), (0.85, 1.15))
    P("wallclock", "clock", (1.9, 2.2, -3.0), (0.46,), spin=getattr(w, "clock_spin", []))
    P("plant", "plant1", (4.55, 0, -2.5), (1.5,))
    P("plant", "plant2", (-3.7, 0, 1.55), (1.1,))
    # --- station 1: the work table
    P("table", "tableA", (-2.05, 0, 0.35), (2.1, 0.9, 1.05), color="#7a5236")
    P("rug", "rug1", (-2.0, 0, 0.6), (3.2, 2.4), color=SABBIA)
    P("laptop", "laptop", (-2.75, 0.9, 0.2), rot_y=0.35)
    P("deskset", "desk", (-1.3, 0.9, 0.05), rot_y=-0.3)
    P("desklamp", "dlamp", (-2.95, 0.9, -0.05), rot_y=0.4, color=INK)
    P("ruler", "tape", (-2.98, 0.905, 0.62), (0.5, 0.03), rot_y=1.35)
    P("chalk", "chalk", (-1.22, 0.905, 0.62), rot_y=0.7)
    P("pendant", "pend1", (-2.05, 2.15, 0.35), (1.5,), color=RUGGINE, light=4.5, **H)
    # --- the letter cubes in the middle
    # --- station 2: the rail (fast fashion) under the clock
    P("pendant", "pend3", (2.8, 2.75, -0.55), (1.1,), color=INK, light=4, **H)
    P("mannequin", "man1", (-0.35, 0, -2.35), rot_y=0.3)
    P("bolts", "bolts1", (4.55, 0, 0.6), (0.6, 0.45), n=6, seed=4, rot_y=-PI / 2, palette=["#6f7452", BOSCO, RUGGINE, SABBIA, GESSO, INK])
    # --- station 3: the shoe boxes on a low plinth
    w.solid("plinth", "box", (3.45, 0.26, 1.35), (1.25, 0.52, 0.5), color="#7a6248", rough=0.6)
    w.solid("plinthTop", "box", (3.45, 0.535, 1.35), (1.3, 0.03, 0.54), color="#6b4a30", rough=0.45)
    P("pendant", "pend4", (3.45, 2.45, 1.35), (1.1,), color=RUGGINE, light=6, **H)
    return w
