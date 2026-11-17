# The atelier room (14/11/2026): shared by the lab and the video. furnish(w) fills a World3D with the whole atelier.
import math
PI = math.pi


def furnish(w, hide=None):
    H = {"hide": hide} if hide else {}
    # low golden sun through the two left windows (the wall really blocks it: shadows are real)
    w.room(bg="#1a1410", key="#ffe2b8", dir=(-8, 2.7, 1.2), key_i=5.0, aim=(0.5, 0.8, 0.4), hemi=("#fff1e0", "#7a5a3a"), hemi_i=0.85, side_i=0.5, rim="#9db4e0", rim_i=0.45, box=(9, 6, 40), fog=("#1a1410", 18, 46), exposure=1.28)
    P = w.prop
    P("woodfloor", "floor", (0.5, 0, 0.75), (9.4, 8.2))
    P("wall", "wback", (0.5, 0, -3.1), (9.4, 3.4, 0.2), color="#ebe3d3")
    P("wall", "wleft", (-4.1, 0, 0.75), (8.2, 3.4, 0.2), rot_y=PI / 2, color="#ebe3d3", hole=[0.55, 1.75, 1.8, 1.6])
    P("wall", "wleft2", (-4.1, 0, 0.75), (8.2, 3.4, 0.2), rot_y=PI / 2, color="#d9c9a8", hole=[-1.85, 1.75, 1.8, 1.6]) if False else None
    P("wall", "wright", (5.1, 0, 0.75), (8.2, 3.4, 0.2), rot_y=PI / 2, color="#e4dac6")
    P("window", "win1", (-4.0, 1.75, 0.2), (1.8, 1.6), rot_y=PI / 2)
    P("rug", "rug1", (-2.2, 0, 0.9), (3.4, 2.4), color="#b9ae98")
    # --- A: the drawing table under the window
    P("table", "tableA", (-2.6, 0, 0.6), (2.3, 0.92, 1.0))
    P("cuttingmat", "mat", (-2.75, 0.92, 0.62), (1.25, 0.7))
    P("paper", "swatch", (-2.3, 0.932, 1.0), (0.32, 0.22), kind="swatch", rot_y=-0.2)
    P("ruler", "tape", (-2.62, 0.928, 0.2), (0.6, 0.03), rot_y=0.15)
    P("weight", "wt1", (-3.07, 0.928, 0.3))
    P("weight", "wt2", (-2.62, 0.928, 0.88))
    P("chalk", "chalk", (-2.48, 0.928, 0.45), rot_y=0.7)
    P("chalk", "chalk2", (-2.44, 0.928, 0.5), rot_y=-0.4, color="#2f5d8a")
    P("lsquare", "sq", (-3.32, 0.928, 1.02), (0.5, 0.32), rot_y=0.12)
    P("desklamp", "dlamp", (-3.55, 0.92, 0.3), rot_y=0.6)
    P("pendant", "pend1", (-2.6, 2.25, 0.6), (1.5,), color="#8a4b2d", light=9, **H)
    P("buttonjar", "jar", (-1.7, 0.92, 0.3))
    P("pincushion", "pinc", (-1.95, 0.92, 0.95))
    P("spool", "spoolA", (-3.35, 0.92, 0.95), color="#2f3a2e", rot_y=0.5)
    P("spool", "spoolA2", (-3.28, 0.92, 1.08), color="#8a4b2d", rot_y=-0.3)
    # --- B: the centre: the hero hangs, a sewing table and two dress forms
    P("table", "tableB", (1.9, 0, 0.5), (1.4, 0.78, 0.68), shelfstuff=False)
    P("sewing", "machine", (1.8, 0.78, 0.5), rot_y=-0.15)
    P("pincushion", "pincB", (2.55, 0.78, 0.7))
    P("spool", "spoolB", (1.4, 0.78, 0.35), color="#c9a24a", rot_y=0.8)
    P("mannequin", "man1", (1.75, 0, -1.6))   # moved right: the skirt outline at 51 s crossed it
    P("mannequin", "man2", (2.15, 0, -1.9), rot_y=-0.5, linen="#cfc2a3")
    P("pendant", "pend3", (1.6, 2.45, 0.5), (1.3,), color="#c9a24a", light=6, **H)
    P("pendant", "pend4", (3.0, 2.5, -0.4), (1.2,), color="#8a4b2d", light=5, **H)
    # --- C: the stock wall and the rail
    P("rollrack", "rack", (3.55, 0, -2.82), (3.0, 2.3, 0.5), seed=4)
    P("spoolwall", "spools", (0.1, 1.0, -2.98), (2.1, 1.55))
    P("frame", "fr1", (-1.6, 1.95, -2.97), (0.55, 0.72), kind="sketch")
    P("frame", "fr2", (-0.8, 1.85, -2.97), (0.45, 0.45), kind="swatch")
    P("frame", "fr3", (-2.5, 1.9, -2.97), (0.7, 0.5), kind="lines")
    P("rail", "rail", (4.7, 0, 0.5), (2.6, 1.7), rot_y=-PI / 2, seed=5)
    P("plant", "plant1", (4.6, 0, -2.4), (1.4,))
    P("plant", "plant2", (-3.7, 0, -2.4), (1.0,))
    P("bolts", "bolts1", (-1.3, 0, -2.3), (0.6, 0.42), n=6, seed=3)
    P("bolts", "bolts2", (-0.55, 0, -2.45), (0.55, 0.4), n=4, seed=9)
    w.solid("stool", "box", (-1.2, 0.22, 1.7), (0.36, 0.44, 0.36), color="#8a6a44", rough=0.7)
    w.solid("crate", "box", (4.5, 0.2, -1.0), (0.6, 0.4, 0.45), color="#a58a6a", rough=0.8)
    return w
