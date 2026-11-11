"""Variante forata del modulo: la Y non e' piu' una nervatura in rilievo ma un taglio passante
(proposta del professore, 11/11/2026). Piastra esagonale piatta in TPU, la pelle si vede attraverso la Y.

Genera modulo-forato.stl / .3mf / .step e le immagini di controllo.
Uso:  python modulo_forato.py
"""
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MplPath
from shapely import affinity
from shapely.geometry import Polygon
from shapely.ops import unary_union

import modulo as M

OUT = Path(__file__).parent

# --- quote (mm) ---
SPESSORE = 1.6        # piastra piatta, tutta dello stesso spessore
LARG_TAGLIO = 5.0     # larghezza dei bracci della Y al centro (poi vanno a punta)
BORDO_MIN = 4.0       # materiale che resta tra la punta del braccio e il lato dell'esagono
ANGOLI = (90, 210, 330)

APOTEMA = M.LATO_LATO / 2
LUNG_ASSE = APOTEMA - BORDO_MIN   # dal centro alla punta del braccio


def taglio_y():
    """Stella a tre punte: ogni braccio e' un triangolo, largo al centro e a spigolo vivo in punta."""
    bracci = []
    for a in ANGOLI:
        r = math.radians(a)
        dx, dy = math.cos(r), math.sin(r)
        nx, ny = -dy * LARG_TAGLIO / 2, dx * LARG_TAGLIO / 2
        bracci.append(Polygon([(nx, ny), (LUNG_ASSE * dx, LUNG_ASSE * dy), (-nx, -ny)]))
    return unary_union(bracci)


def piastra_2d():
    return M.hexagon().difference(unary_union(M.fori())).difference(taglio_y())


def costruisci():
    p2d = piastra_2d()
    return trimesh.creation.extrude_polygon(p2d, SPESSORE), p2d


def esporta_step():
    import cadquery as cq

    R = M.R
    solido = cq.Workplane("XY").polygon(6, 2 * R).extrude(SPESSORE)
    rf = M.INSET_FORO * R
    centri = [(rf * math.cos(math.radians(a)), rf * math.sin(math.radians(a))) for a in range(0, 360, 60)]
    solido = solido.faces(">Z").workplane().pushPoints(centri).hole(M.DIAM_FORO)
    contorno = list(taglio_y().exterior.coords)[:-1]
    stella = cq.Workplane("XY").polyline(contorno).close().extrude(SPESSORE)
    solido = solido.cut(stella).clean()
    cq.exporters.export(solido, str(OUT / "modulo-forato.step"))
    return solido.val().Volume(), solido.val().isValid()


def patch(geom, **kw):
    """Poligono shapely con buchi -> patch matplotlib."""
    verts, codes = [], []
    for ring in [geom.exterior, *geom.interiors]:
        pts = list(ring.coords)
        verts += pts
        codes += [MplPath.MOVETO] + [MplPath.LINETO] * (len(pts) - 2) + [MplPath.CLOSEPOLY]
    return PathPatch(MplPath(verts, codes), **kw)


def immagine_pianta(p2d):
    fig, ax = plt.subplots(figsize=(8, 7.2), dpi=200)
    ax.add_patch(patch(p2d, fc="#2b2829", ec="#111", lw=1.0))
    R, h = M.R, APOTEMA
    arr = dict(arrowstyle="<->", color="#222", lw=0.9)
    ax.annotate("", xy=(-R, -h - 5), xytext=(R, -h - 5), arrowprops=arr)
    ax.text(0, -h - 7.2, "60 mm (vertice-vertice)", ha="center", va="top", fontsize=10)
    ax.annotate("", xy=(R + 5, -h), xytext=(R + 5, h), arrowprops=arr)
    ax.text(R + 6.5, 0, "52 mm\n(lato-lato)", ha="left", va="center", fontsize=10)
    ax.annotate(f"taglio a Y passante\n{LARG_TAGLIO:g} mm al centro, a punta", xy=(0, 8), xytext=(-R - 6, h * 0.8), fontsize=9, ha="right",
                arrowprops=dict(arrowstyle="-", color="#222", lw=0.7))
    ax.annotate(f"bordo {BORDO_MIN:g} mm", xy=(0, h - BORDO_MIN / 2), xytext=(R * 0.2, h + 5), fontsize=9,
                arrowprops=dict(arrowstyle="-", color="#222", lw=0.7))
    f0 = M.fori()[0].centroid
    ax.annotate("foro Ø 3 mm", xy=(f0.x, f0.y), xytext=(R + 4, h * 0.55), fontsize=9,
                arrowprops=dict(arrowstyle="-", color="#222", lw=0.7))
    ax.set_aspect("equal")
    ax.set_xlim(-R - 26, R + 24)
    ax.set_ylim(-h - 14, h + 10)
    ax.axis("off")
    ax.set_title(f"Modulo forato - pianta quotata (spessore {SPESSORE:g} mm, quote in mm)", fontsize=11)
    fig.savefig(OUT / "05-forato-pianta-quotata.png", bbox_inches="tight")
    plt.close(fig)


def immagine_tassellatura(p2d):
    """Piu' moduli accostati su fondo color pelle: l'effetto del pattern forato."""
    fig, ax = plt.subplots(figsize=(8, 8), dpi=200)
    fig.patch.set_facecolor("#d9b79a")
    ax.set_facecolor("#d9b79a")
    passo_x, passo_y = 1.5 * M.R, M.LATO_LATO
    for i in range(-3, 4):
        for j in range(-3, 4):
            x = i * passo_x
            y = j * passo_y + (passo_y / 2 if i % 2 else 0)
            ax.add_patch(patch(affinity.translate(p2d, x, y), fc="#1b1a1a", ec="#3a3838", lw=0.6))
    ax.set_aspect("equal")
    ax.set_xlim(-110, 110)
    ax.set_ylim(-110, 110)
    ax.axis("off")
    fig.savefig(OUT / "06-forato-effetto-pattern.png", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    mesh, p2d = costruisci()
    mesh.export(OUT / "modulo-forato.stl")
    mesh.export(OUT / "modulo-forato.3mf")
    print("watertight:", mesh.is_watertight)
    print("ingombro mm:", np.round(mesh.extents, 2))
    print("volume mm3:", round(mesh.volume, 1))
    pieno = M.hexagon().area
    print("area aperta %:", round(100 * (1 - p2d.area / pieno), 1))
    immagine_pianta(p2d)
    immagine_tassellatura(p2d)
    try:
        vol, ok = esporta_step()
        print("STEP volume mm3:", round(vol, 1), " solido valido:", ok)
    except ImportError:
        print("cadquery non installato: STEP saltato")
