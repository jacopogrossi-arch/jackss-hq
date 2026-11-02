"""Aggiunge le venature in rilievo alla foglia disegnata su Fusion (foglia.3mf).

Legge il contorno della foglia dal 3MF, disegna una nervatura centrale e coppie di
venature laterali curve che si assottigliano verso il bordo, e le unisce alla lastra.
Genera foglia-venature.3mf / .stl e l'anteprima foglia-venature.png (unita' = mm).
Uso:  python venature.py            (oppure: python venature.py altra-foglia.3mf)
"""
import sys
from pathlib import Path

import numpy as np
import trimesh
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

OUT = Path(__file__).parent

# --- quote (mm) ---
ALT_CENTRALE = 1.2      # rilievo della nervatura centrale sopra la lastra
ALT_LATERALI = 0.8      # rilievo delle venature laterali
LARG_CENTRALE = (3.0, 1.0)   # larghezza all'attacco del picciolo -> in punta
LARG_LATERALI = (1.8, 0.6)   # larghezza sulla nervatura centrale -> verso il bordo
COPPIE = 8              # coppie di venature laterali
STACCO_BORDO = 3.0      # le venature si fermano a questa distanza dal bordo
STACCO_FORO = 2.5       # margine intorno al foro del picciolo
SFASAMENTO = 0.35       # 0 = venature opposte, 0.5 = perfettamente alternate
INCLINAZIONE = 0.55     # quanto scendono verso la punta (0 = orizzontali)


def contorno(mesh):
    """Poligono 2D della faccia superiore della lastra."""
    z = mesh.bounds[1, 2]
    tri = mesh.vertices[mesh.faces]
    sopra = tri[np.all(np.isclose(tri[:, :, 2], z), axis=1)]
    return unary_union([Polygon(t[:, :2]) for t in sopra]).buffer(0), z


def mezza_larghezza(foglia, y):
    riga = foglia.intersection(LineString([(0, y), (1e3, y)]))
    return riga.bounds[2] if not riga.is_empty else 0.0


def rastremata(punti, w0, w1):
    """Striscia che passa da larghezza w0 a w1 lungo la polilinea (catena di cerchi)."""
    n = len(punti)
    cerchi = [Point(p).buffer((w0 + (w1 - w0) * i / (n - 1)) / 2, 16) for i, p in enumerate(punti)]
    return unary_union([unary_union([a, b]).convex_hull for a, b in zip(cerchi, cerchi[1:])])


def bezier(p0, p1, p2, n=30):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0) + 2 * (1 - t) * t * np.array(p1) + t ** 2 * np.array(p2)


def venature(foglia):
    (xmin, ymin, xmax, ymax) = foglia.bounds
    foro = Polygon(foglia.interiors[0]) if foglia.interiors else Point(0, ymax).buffer(0.1)
    y_punta = ymin
    # la lama comincia dove la foglia si allarga oltre il picciolo
    larg_picciolo = mezza_larghezza(foglia, foro.centroid.y)
    ys = np.linspace(ymax, ymin, 600)
    y_attacco = next(y for y in ys if mezza_larghezza(foglia, y) > larg_picciolo + 0.5)
    y_inizio = foro.bounds[1] - STACCO_FORO - LARG_CENTRALE[0] / 2

    centrale = rastremata(bezier((0, y_inizio), (0, (y_inizio + y_punta) / 2), (0, y_punta + STACCO_BORDO)),
                          *LARG_CENTRALE)

    laterali = []
    lama = y_attacco - y_punta
    passo = lama * 0.8 / COPPIE
    for i in range(COPPIE):
        for lato, sfasa in ((1, 0.0), (-1, SFASAMENTO)):
            y0 = y_attacco - lama * 0.08 - (i + sfasa) * passo
            if y0 < y_punta + lama * 0.06:
                continue
            w0 = mezza_larghezza(foglia, y0)
            y1 = y0 - INCLINAZIONE * w0
            x1 = max(mezza_larghezza(foglia, y1) - STACCO_BORDO, 2.0)
            ctrl = (0.45 * x1, y0 - 0.2 * (y0 - y1))
            pts = bezier((0, y0), ctrl, (x1, y1)) * [lato, 1]
            laterali.append(rastremata(pts, *LARG_LATERALI))

    interno = foglia.buffer(-STACCO_BORDO + 0.5)
    vuoto = foro.buffer(STACCO_FORO)
    return (centrale.intersection(interno).difference(vuoto),
            unary_union(laterali).intersection(interno).difference(vuoto))


def costruisci(file_foglia):
    lastra = trimesh.load(file_foglia, force="mesh")
    foglia, z = contorno(lastra)
    centrale_2d, laterali_2d = venature(foglia)
    parti = [lastra]
    for forma, alt in ((centrale_2d, ALT_CENTRALE), (laterali_2d, ALT_LATERALI)):
        for pezzo in getattr(forma, "geoms", [forma]):
            p = trimesh.creation.extrude_polygon(pezzo, alt + 0.01)
            p.apply_translation([0, 0, z - 0.01])   # piccola compenetrazione per un'unione pulita
            parti.append(p)
    return trimesh.boolean.union(parti, engine="manifold"), foglia, centrale_2d, laterali_2d


def anteprima(foglia, centrale_2d, laterali_2d, file_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from shapely.plotting import plot_polygon

    fig, ax = plt.subplots(figsize=(5, 11))
    plot_polygon(foglia, ax=ax, add_points=False, facecolor="#cfd8c4", edgecolor="#333")
    plot_polygon(laterali_2d, ax=ax, add_points=False, facecolor="#6b8f4e", edgecolor="none")
    plot_polygon(centrale_2d, ax=ax, add_points=False, facecolor="#3d5a2a", edgecolor="none")
    ax.set_aspect("equal")
    ax.set_title(f"Venature: centrale +{ALT_CENTRALE} mm, laterali +{ALT_LATERALI} mm", fontsize=9)
    fig.savefig(file_png, dpi=110, bbox_inches="tight")


if __name__ == "__main__":
    sorgente = Path(sys.argv[1]) if len(sys.argv) > 1 else OUT / "foglia.3mf"
    mesh, foglia, centrale_2d, laterali_2d = costruisci(sorgente)
    mesh.export(OUT / "foglia-venature.stl")
    mesh.export(OUT / "foglia-venature.3mf")
    anteprima(foglia, centrale_2d, laterali_2d, OUT / "foglia-venature.png")
    print("watertight:", mesh.is_watertight)
    print("ingombro mm:", np.round(mesh.extents, 2))
    print("volume mm3:", round(mesh.volume, 1))
