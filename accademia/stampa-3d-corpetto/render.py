"""Immagini del modulo con le quote in mm: vista d'insieme, sezione con spessori, pianta quotata."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon as MplPoly, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from shapely.geometry import LineString

import modulo as M

mesh, base_2d, nerv_2d = M.costruisci()
VERDE, GRIGIO, NERO = "#1D9E75", "#d9d7cf", "#222222"


def poly_patch(geom, **kw):
    ext = MplPoly(np.array(geom.exterior.coords), closed=True, **kw)
    return ext


def pianta():
    fig, ax = plt.subplots(figsize=(8, 7.2), dpi=200)
    esa = M.hexagon()
    ax.add_patch(poly_patch(esa, fc=GRIGIO, ec=NERO, lw=1.2))
    geoms = nerv_2d.geoms if hasattr(nerv_2d, "geoms") else [nerv_2d]
    for g in geoms:
        ax.add_patch(poly_patch(g, fc=VERDE, ec="#0F6E56", lw=0.8))
    for f in M.fori():
        c = f.centroid
        ax.add_patch(Circle((c.x, c.y), M.DIAM_FORO / 2, fc="white", ec=NERO, lw=0.8))
    R, h = M.R, M.LATO_LATO / 2
    arr = dict(arrowstyle="<->", color=NERO, lw=0.9)
    ax.annotate("", xy=(-R, -h - 5), xytext=(R, -h - 5), arrowprops=arr)
    ax.text(0, -h - 7.2, "60 mm (vertice-vertice)", ha="center", va="top", fontsize=10)
    ax.annotate("", xy=(R + 5, -h), xytext=(R + 5, h), arrowprops=arr)
    ax.text(R + 6.5, 0, "52 mm\n(lato-lato)", ha="left", va="center", fontsize=10)
    f0 = M.fori()[0].centroid
    ax.annotate("foro Ø 3 mm", xy=(f0.x, f0.y), xytext=(R + 4, h * 0.55), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=NERO, lw=0.7))
    ax.annotate("nervatura 4 mm", xy=(0, 14), xytext=(-R - 6, h * 0.8), fontsize=9, ha="right",
                arrowprops=dict(arrowstyle="-", color=NERO, lw=0.7))
    ax.annotate("rami 2 mm", xy=M.px(222, 96), xytext=(-R - 6, h * 1.05 + 2), fontsize=9, ha="right",
                arrowprops=dict(arrowstyle="-", color=NERO, lw=0.7))
    ax.set_aspect("equal")
    ax.set_xlim(-R - 22, R + 24)
    ax.set_ylim(-h - 14, h + 8)
    ax.axis("off")
    ax.set_title("Modulo esagonale - pianta quotata (scala 1:1, quote in mm)", fontsize=11)
    fig.savefig(M.OUT / "01-pianta-quotata.png", bbox_inches="tight")
    plt.close(fig)


def sezione():
    fig, axs = plt.subplots(2, 1, figsize=(8, 6.6), dpi=200, gridspec_kw=dict(height_ratios=[1, 1.15]))
    inter = LineString([(0, -40), (0, 40)]).intersection(nerv_2d)
    segs = [(g.coords[0][1], g.coords[-1][1]) for g in (inter.geoms if hasattr(inter, "geoms") else [inter])]
    h = M.LATO_LATO / 2
    ax = axs[0]
    ax.add_patch(Rectangle((-h, 0), 2 * h, M.SPESSORE_BASE, fc=GRIGIO, ec=NERO, lw=0.8))
    for a, b in segs:
        lo, hi = sorted((a, b))
        ax.add_patch(Rectangle((lo, M.SPESSORE_BASE), hi - lo, M.ALTEZZA_TOT - M.SPESSORE_BASE, fc=VERDE, ec="#0F6E56", lw=0.8))
    ax.set_xlim(-h - 3, h + 3)
    ax.set_ylim(-1.5, 5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Sezione lungo l'asse del braccio superiore (altezze x4)", fontsize=10)
    ax.text(0, -1.2, "52 mm", ha="center", fontsize=9)
    ax = axs[1]
    k = 10
    ax.add_patch(Rectangle((0, 0), 30, M.SPESSORE_BASE * k, fc=GRIGIO, ec=NERO, lw=0.8))
    ax.add_patch(Rectangle((13, M.SPESSORE_BASE * k), M.LARG_NERV, (M.ALTEZZA_TOT - M.SPESSORE_BASE) * k, fc=VERDE, ec="#0F6E56", lw=0.8))
    ax.add_patch(Rectangle((22, M.SPESSORE_BASE * k), M.LARG_RAMO, (M.ALTEZZA_TOT - M.SPESSORE_BASE) * k * 0.0 + 0.001, fc=VERDE))
    arr = dict(arrowstyle="<->", color=NERO, lw=0.9)
    ax.annotate("", xy=(33, 0), xytext=(33, M.SPESSORE_BASE * k), arrowprops=arr)
    ax.text(34, 4, "base 0,8 mm", va="center", fontsize=10)
    ax.annotate("", xy=(-1.5, 0), xytext=(-1.5, M.ALTEZZA_TOT * k), arrowprops=arr)
    ax.text(-2.5, 12, "altezza totale 2,4 mm", ha="right", va="center", fontsize=10)
    ax.annotate("", xy=(13, 27), xytext=(13 + M.LARG_NERV, 27), arrowprops=arr)
    ax.text(15, 29.5, "nervatura 4 mm", ha="center", fontsize=10)
    ax.annotate("", xy=(13 + M.LARG_NERV, 17), xytext=(13 + M.LARG_NERV + 0.001, 8), arrowprops=dict(arrowstyle="-", color=NERO, lw=0))
    ax.text(21, 16.5, "rilievo sopra la base 1,6 mm", fontsize=10, va="center")
    ax.set_xlim(-26, 52)
    ax.set_ylim(-3, 33)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Dettaglio spessori (ingrandito x10 in altezza)", fontsize=10)
    fig.tight_layout()
    fig.savefig(M.OUT / "02-dettaglio-spessori.png", bbox_inches="tight")
    plt.close(fig)


def insieme():
    fig = plt.figure(figsize=(8, 6.4), dpi=200)
    ax = fig.add_subplot(111, projection="3d")
    fine = mesh.subdivide_to_size(1.5)
    tri = fine.vertices[fine.faces]
    n = fine.face_normals
    luce = np.array([-0.4, -0.6, 0.7])
    luce /= np.linalg.norm(luce)
    sh = np.clip(n @ luce, 0.15, 1)
    alt = tri[:, :, 2].mean(axis=1)
    base_rgb = np.where((alt > M.SPESSORE_BASE + 0.01)[:, None], np.array([0.11, 0.62, 0.46]), np.array([0.85, 0.84, 0.81]))
    cols = np.clip(base_rgb * (0.45 + 0.55 * sh[:, None]), 0, 1)
    pc = Poly3DCollection(tri, facecolors=cols, edgecolors="none")
    ax.add_collection3d(pc)
    ax.set_xlim(-32, 32)
    ax.set_ylim(-32, 32)
    ax.set_zlim(0, 8)
    ax.set_box_aspect((64, 64, 16))
    ax.view_init(elev=40, azim=-62)
    ax.axis("off")
    ax.set_title("Modulo esagonale - vista d'insieme (60 x 52 x 2,4 mm, altezza ingrandita x2)", fontsize=10)
    fig.savefig(M.OUT / "03-vista-insieme.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    pianta()
    sezione()
    insieme()
    print("ok")
