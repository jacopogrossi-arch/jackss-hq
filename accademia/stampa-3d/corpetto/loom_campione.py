"""Campione di telo "LOOM" (rif. Maria Alejandra Mora-Sanchez): foglio continuo in TPU con tagli a Y.

Il foglio e' una tassellatura di triangoli equilateri. Da ogni vertice partono tre tagli (0, 120, 240 gradi)
che si fermano poco prima del vertice successivo: li' resta una cerniera. Tirando il telo i triangoli ruotano,
i tagli a Y si aprono a stella e il telo si allarga in tutte le direzioni (pattern auxetico a triangoli rotanti).

Genera loom-campione-04.3mf / -06.3mf (+ stl, step) e l'immagine di controllo.
Uso:  python loom_campione.py
"""
import math
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.patches import PathPatch, Polygon as MplPoly
from matplotlib.path import Path as MplPath
from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union

OUT = Path(__file__).parent

# --- quote (mm) ---
LATO = 16.0          # lato del triangolo
CERNIERA = 1.6       # tratto di lato lasciato intero vicino al vertice (la cerniera)
LARG_TAGLIO = 0.5    # larghezza della fessura da chiusa
LARG_CAMP, ALT_CAMP = 84.0, 80.0   # ingombro indicativo del campione
SPESSORI = (0.4, 0.6)

E1 = np.array([LATO, 0.0])
E2 = np.array([LATO / 2, LATO * math.sqrt(3) / 2])


def V(i, j):
    return i * E1 + j * E2


def triangoli():
    """Triangoli (terne di indici di vertice) il cui centro cade nel rettangolo del campione."""
    out = []
    for i in range(-12, 13):
        for j in range(-12, 13):
            for tri, su in (((i, j), (i + 1, j), (i, j + 1)), True), (((i + 1, j), (i + 1, j + 1), (i, j + 1)), False):
                c = sum(V(*v) for v in tri) / 3
                if abs(c[0]) <= LARG_CAMP / 2 and abs(c[1]) <= ALT_CAMP / 2:
                    out.append((tri, su))
    return out


def telo_2d(tris):
    pieno = unary_union([Polygon([V(*v) for v in t]).buffer(1e-6) for t, _ in tris])
    conta = Counter(frozenset(e) for t, _ in tris for e in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])))
    tagli = []
    for lato, n in conta.items():
        if n < 2:
            continue                      # lato sul bordo: niente taglio
        a, b = sorted(lato)
        # il taglio parte dal vertice da cui il lato esce a 0, 120 o 240 gradi
        d = np.array(b) - np.array(a)
        partenza, arrivo = (a, b) if tuple(d) in ((1, 0), (-1, 1), (0, -1)) else (b, a)
        p, q = V(*partenza), V(*arrivo)
        u = (q - p) / LATO
        fine = p + u * (LATO - CERNIERA - LARG_TAGLIO / 2)
        tagli.append(LineString([p, fine]).buffer(LARG_TAGLIO / 2, cap_style=3))
    return pieno.difference(unary_union(tagli)).buffer(0)


def aperto(tris, gradi):
    """Posizione dei triangoli quando il telo e' tirato: ruotano di +/- gradi e il reticolo si allarga."""
    th = math.radians(gradi)
    for segno in (1, -1):
        s = math.cos(th) + math.sqrt(3) * math.sin(th)
        polys = []
        for t, su in tris:
            pts = np.array([V(*v) for v in t])
            c = pts.mean(axis=0)
            a = segno * th * (1 if su else -1)
            R = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
            polys.append((pts - c) @ R.T + s * c)
        angoli = Counter(tuple(np.round(p, 3)) for poly in polys for p in poly)
        if sum(1 for n in angoli.values() if n == 2) > len(tris):   # gli angoli si toccano a coppie: verso giusto
            return polys, s
    return polys, s


def patch(geom, **kw):
    verts, codes = [], []
    for ring in [geom.exterior, *geom.interiors]:
        pts = list(ring.coords)
        verts += pts
        codes += [MplPath.MOVETO] + [MplPath.LINETO] * (len(pts) - 2) + [MplPath.CLOSEPOLY]
    return PathPatch(MplPath(verts, codes), **kw)


def immagine(tris, telo):
    pelle, nero = "#d9b79a", "#1b1a1a"
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.6), dpi=170)
    fig.patch.set_facecolor(pelle)
    geoms = telo.geoms if hasattr(telo, "geoms") else [telo]
    for g in geoms:
        axs[0].add_patch(patch(g, fc=nero, ec="none"))
    axs[0].set_title(f"A riposo (come esce dalla stampante)\nlato {LATO:g} mm, cerniera {CERNIERA:g} mm, fessura {LARG_TAGLIO:g} mm", fontsize=10)
    lim = 0
    for ax, gradi in ((axs[1], 12), (axs[2], 28)):
        polys, s = aperto(tris, gradi)
        for p in polys:
            ax.add_patch(MplPoly(p, closed=True, fc=nero, ec="none"))
        ax.set_title(f"Tirato: +{round((s - 1) * 100)}% in larghezza e in altezza", fontsize=10)
        lim = max(lim, np.abs(np.vstack(polys)).max())
    for ax in axs:
        ax.set_facecolor(pelle)
        ax.set_aspect("equal")
        ax.set_xlim(-lim - 4, lim + 4)
        ax.set_ylim(-lim - 4, lim + 4)
        ax.axis("off")
    fig.savefig(OUT / "07-loom-campione.png", bbox_inches="tight", facecolor=pelle)
    plt.close(fig)


def esporta_step(telo, spessore, nome):
    import cadquery as cq

    def pulito(ring):
        pts = [tuple(round(c, 4) for c in p) for p in list(ring.coords)[:-1]]
        return [p for k, p in enumerate(pts) if p != pts[k - 1]]

    solido = cq.Workplane("XY").polyline(pulito(telo.exterior)).close().extrude(spessore)
    for buco in telo.interiors:
        solido = solido.cut(cq.Workplane("XY").polyline(pulito(buco)).close().extrude(spessore))
    cq.exporters.export(solido, str(OUT / nome))
    return solido.val().isValid()


if __name__ == "__main__":
    tris = triangoli()
    telo = telo_2d(tris)
    assert telo.geom_type == "Polygon", "il telo deve restare un pezzo unico"
    minx, miny, maxx, maxy = telo.bounds
    print("triangoli:", len(tris), " ingombro mm:", round(maxx - minx, 1), "x", round(maxy - miny, 1), " tagli a Y chiusi:", len(telo.interiors))
    for sp in SPESSORI:
        tag = f"{round(sp * 10):02d}"
        mesh = trimesh.creation.extrude_polygon(telo, sp)
        mesh.export(OUT / f"loom-campione-{tag}.stl")
        mesh.export(OUT / f"loom-campione-{tag}.3mf")
        print(f"spessore {sp} mm: watertight {mesh.is_watertight}, volume {round(mesh.volume)} mm3, circa {round(mesh.volume * 1.21 / 1000, 2)} g di TPU")
    immagine(tris, telo)
    try:
        print("STEP valido:", esporta_step(telo, SPESSORI[0], "loom-campione-04.step"))
    except Exception as e:
        print("STEP saltato:", type(e).__name__, e)
