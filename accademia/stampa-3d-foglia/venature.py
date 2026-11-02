"""Aggiunge le venature in rilievo alla foglia disegnata su Fusion (foglia.3mf).

Legge il contorno della foglia dal 3MF, disegna una nervatura centrale leggermente
storta e venature laterali irregolari (curve, ondulate, alcune biforcate) che si
assottigliano verso il bordo, e le unisce alla lastra.
Genera foglia-venature.3mf / .stl e l'anteprima foglia-venature.png (unita' = mm).
Uso:  python venature.py            (oppure: python venature.py altra-foglia.3mf)
Cambia SEME per avere un'altra foglia con lo stesso stile.
"""
import sys
from pathlib import Path

import numpy as np
import trimesh
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

OUT = Path(__file__).parent

# --- quote (mm) ---
ALT_CENTRALE = 1.6      # rilievo della nervatura centrale sopra la lastra
ALT_LATERALI = 0.8      # rilievo delle venature laterali
ALT_RAMI = 0.6          # rilievo delle biforcazioni
LARG_CENTRALE = (3.6, 1.6)   # larghezza all'attacco del picciolo -> in punta
LARG_LATERALI = (2.0, 1.0)   # larghezza sulla nervatura centrale -> verso il bordo
LARG_RAMI = (1.3, 1.0)
LARG_MINIMA = 1.0       # sotto ~2 passate dell'ugello 0,4 lo slicer scarta la parete
STACCO_BORDO = 3.0      # le venature si fermano a questa distanza dal bordo
STACCO_FORO = 2.5       # margine intorno al foro del picciolo

# --- irregolarita' ---
SEME = 7                # cambia il numero = cambia la foglia
VENATURE_PER_LATO = (7, 9)   # minimo, massimo (scelto a caso per ogni lato)
STORTA_CENTRALE = 4.0   # quanto la nervatura centrale si piega di lato
INCLINAZIONE = (0.35, 0.8)   # quanto scendono verso la punta (0 = orizzontali)
ONDA = (0.015, 0.04)    # ampiezza dell'ondulazione, in frazione della lunghezza della venatura
PROB_RAMO = 0.6         # probabilita' che una venatura si biforchi


def contorno(mesh):
    """Poligono 2D della faccia superiore della lastra."""
    z = mesh.bounds[1, 2]
    tri = mesh.vertices[mesh.faces]
    sopra = tri[np.all(np.isclose(tri[:, :, 2], z), axis=1)]
    return unary_union([Polygon(t[:, :2]) for t in sopra]).buffer(0), z


def bordo(foglia, y, lato=1):
    """x del bordo della foglia all'altezza y, a destra (lato=1) o a sinistra (lato=-1)."""
    riga = foglia.intersection(LineString([(0, y), (lato * 1e3, y)]))
    if riga.is_empty:
        return 0.0
    return riga.bounds[2] if lato > 0 else riga.bounds[0]


def rastremata(punti, w0, w1):
    """Striscia che passa da larghezza w0 a w1 lungo la polilinea (catena di cerchi)."""
    n = len(punti)
    w1 = max(w1, LARG_MINIMA)
    cerchi = [Point(p).buffer((w0 + (w1 - w0) * i / (n - 1)) / 2, 16) for i, p in enumerate(punti)]
    return unary_union([unary_union([a, b]).convex_hull for a, b in zip(cerchi, cerchi[1:])])


def bezier3(p0, p1, p2, p3, n=48):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = map(np.array, (p0, p1, p2, p3))
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3


def ondula(pts, ampiezza, onde, fase):
    """Sposta i punti di lato con un'onda che vale zero agli estremi."""
    d = np.gradient(pts, axis=0)
    normale = np.c_[-d[:, 1], d[:, 0]] / np.linalg.norm(d, axis=1)[:, None]
    t = np.linspace(0, 1, len(pts))
    return pts + normale * (ampiezza * np.sin(np.pi * t) * np.sin(2 * np.pi * onde * t + fase))[:, None]


def venature(foglia, rng):
    (xmin, ymin, xmax, ymax) = foglia.bounds
    foro = Polygon(foglia.interiors[0]) if foglia.interiors else Point(0, ymax).buffer(0.1)
    y_punta = ymin
    # la lama comincia dove la foglia si allarga oltre il picciolo
    larg_picciolo = bordo(foglia, foro.centroid.y)
    ys = np.linspace(ymax, ymin, 600)
    y_attacco = next(y for y in ys if bordo(foglia, y) > larg_picciolo + 0.5)
    y_inizio = foro.bounds[1] - STACCO_FORO - LARG_CENTRALE[0] / 2
    lama = y_attacco - y_punta

    # nervatura centrale: dritta nel picciolo, poi si piega appena e torna in punta
    c1, c2 = rng.uniform(-1, 1, 2) * [STORTA_CENTRALE, STORTA_CENTRALE * 0.4]

    def x_centrale(y):
        t = np.clip((y_attacco - y) / lama, 0, 1)
        return c1 * np.sin(np.pi * t) + c2 * np.sin(2 * np.pi * t)

    yc = np.linspace(y_inizio, y_punta + STACCO_BORDO, 80)
    centrale = rastremata(np.c_[x_centrale(yc), yc], *LARG_CENTRALE)

    laterali, rami = [], []
    for lato in (1, -1):
        n = rng.integers(VENATURE_PER_LATO[0], VENATURE_PER_LATO[1] + 1)
        # posizioni lungo la lama, distribuite ma con passo irregolare
        tt = np.linspace(0.07, 0.86, n) + rng.uniform(-0.35, 0.35, n) * (0.79 / n)
        for t0 in np.sort(tt):
            y0 = y_attacco - t0 * lama
            x0 = x_centrale(y0)
            larghezza = abs(bordo(foglia, y0, lato) - x0)
            y1 = y0 - rng.uniform(*INCLINAZIONE) * larghezza
            x1 = bordo(foglia, y1, lato) - lato * STACCO_BORDO * rng.uniform(1.0, 2.5)
            dx, dy = x1 - x0, y1 - y0
            lunghezza = np.hypot(dx, dy)
            if lato * dx < 4 or lunghezza < 10:
                continue
            # parte quasi perpendicolare alla centrale, poi curva verso la punta
            p1 = (x0 + dx * rng.uniform(0.2, 0.45), y0 + dy * rng.uniform(-0.15, 0.2))
            p2 = (x0 + dx * rng.uniform(0.55, 0.85), y0 + dy * rng.uniform(0.5, 1.0))
            pts = bezier3((x0, y0), p1, p2, (x1, y1))
            pts = ondula(pts, rng.uniform(*ONDA) * lunghezza, rng.uniform(1.0, 2.0), rng.uniform(0, 2 * np.pi))
            laterali.append(rastremata(pts, *LARG_LATERALI))

            if rng.random() < PROB_RAMO:
                k = rng.integers(len(pts) * 4 // 10, len(pts) * 7 // 10)
                dir_ = pts[k + 1] - pts[k - 1]
                dir_ /= np.linalg.norm(dir_)
                ang = np.radians(rng.uniform(25, 45)) * rng.choice([-1, 1])
                rot = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
                if lato * (rot @ dir_)[0] < 0.3:   # il ramo deve andare verso il bordo, non tornare indietro
                    rot = rot.T
                lung = np.linalg.norm(pts[-1] - pts[k]) * rng.uniform(0.5, 0.9)
                fine = pts[k] + rot @ dir_ * lung
                curva = pts[k] + (rot @ dir_) * lung * 0.5 + dir_ * lung * 0.2
                ramo = bezier3(pts[k], (pts[k] + curva) / 2, curva, fine, n=24)
                rami.append(rastremata(ondula(ramo, rng.uniform(0.3, 0.8), 1.2, rng.uniform(0, 6.3)), *LARG_RAMI))

    interno = foglia.buffer(-STACCO_BORDO + 0.5)
    vuoto = foro.buffer(STACCO_FORO)

    def pulisci(forma):
        # toglie i ritagli sul bordo piu' stretti di LARG_MINIMA, che lo slicer non stamperebbe
        forma = forma.intersection(interno).difference(vuoto)
        return forma.buffer(-LARG_MINIMA / 2 + 0.05).buffer(LARG_MINIMA / 2 - 0.05)

    return pulisci(centrale), pulisci(unary_union(laterali)), pulisci(unary_union(rami))


def costruisci(file_foglia):
    lastra = trimesh.load(file_foglia, force="mesh")
    foglia, z = contorno(lastra)
    forme = venature(foglia, np.random.default_rng(SEME))
    parti = [lastra]
    for forma, alt in zip(forme, (ALT_CENTRALE, ALT_LATERALI, ALT_RAMI)):
        for pezzo in getattr(forma, "geoms", [forma]):
            p = trimesh.creation.extrude_polygon(pezzo, alt + 0.01)
            p.apply_translation([0, 0, z - 0.01])   # piccola compenetrazione per un'unione pulita
            parti.append(p)
    return trimesh.boolean.union(parti, engine="manifold"), foglia, forme


def anteprima(foglia, forme, file_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from shapely.plotting import plot_polygon

    centrale_2d, laterali_2d, rami_2d = forme
    fig, ax = plt.subplots(figsize=(5, 11))
    plot_polygon(foglia, ax=ax, add_points=False, facecolor="#cfd8c4", edgecolor="#333")
    plot_polygon(rami_2d, ax=ax, add_points=False, facecolor="#8fae72", edgecolor="none")
    plot_polygon(laterali_2d, ax=ax, add_points=False, facecolor="#6b8f4e", edgecolor="none")
    plot_polygon(centrale_2d, ax=ax, add_points=False, facecolor="#2f4a20", edgecolor="none")
    ax.set_aspect("equal")
    ax.set_title(f"Seme {SEME} - centrale +{ALT_CENTRALE}, laterali +{ALT_LATERALI}, rami +{ALT_RAMI} mm",
                 fontsize=9)
    fig.savefig(file_png, dpi=110, bbox_inches="tight")


if __name__ == "__main__":
    sorgente = Path(sys.argv[1]) if len(sys.argv) > 1 else OUT / "foglia.3mf"
    mesh, foglia, forme = costruisci(sorgente)
    mesh.export(OUT / "foglia-venature.stl")
    mesh.export(OUT / "foglia-venature.3mf")
    anteprima(foglia, forme, OUT / "foglia-venature.png")
    print("watertight:", mesh.is_watertight)
    print("ingombro mm:", np.round(mesh.extents, 2))
    print("volume mm3:", round(mesh.volume, 1))
