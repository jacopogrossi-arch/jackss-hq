"""Modulo esagonale con nervatura a Y per il corpetto (Laboratorio Stampa 3D).

Genera modulo.stl e modulo.3mf in scala 1:1 (unita' = mm), piu' le immagini di controllo.
Uso:  python modulo.py
"""
import math
from pathlib import Path

import numpy as np
import trimesh
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

OUT = Path(__file__).parent

# --- quote (mm) ---
DIAM_VERTICI = 60.0   # da vertice a vertice
SPESSORE_BASE = 0.8
ALTEZZA_TOT = 2.4     # base + nervatura
LARG_NERV = 4.0
LARG_RAMO = 2.0
DIAM_FORO = 3.0
INSET_FORO = 0.86     # posizione del foro lungo il raggio verso il vertice

R = DIAM_VERTICI / 2
LATO_LATO = R * math.sqrt(3)  # 51,96 mm


def hexagon():
    pts = [(R * math.cos(math.radians(a)), R * math.sin(math.radians(a))) for a in range(0, 360, 60)]
    return Polygon(pts)


def px(x, y):
    """Coordinate del disegno (4,5 px/mm, centro 190,170) -> mm."""
    return ((x - 190) / 4.5, (170 - y) / 4.5)


def nervatura():
    bracci = [((0, 0), px(190, 61)), ((0, 0), px(96, 224)), ((0, 0), px(284, 224))]
    rami = [(px(190, 112), px(222, 96)), (px(240, 199), px(256, 168)), (px(140, 199), px(124, 168))]
    forme = [LineString(b).buffer(LARG_NERV / 2) for b in bracci]
    forme += [LineString(r).buffer(LARG_RAMO / 2) for r in rami]
    return unary_union(forme)


def fori():
    centri = [(INSET_FORO * R * math.cos(math.radians(a)), INSET_FORO * R * math.sin(math.radians(a))) for a in range(0, 360, 60)]
    return [Point(c).buffer(DIAM_FORO / 2, 48) for c in centri]


def costruisci():
    esa = hexagon()
    buchi = unary_union(fori())
    base_2d = esa.difference(buchi)
    nerv_2d = nervatura().intersection(esa.buffer(-0.6)).difference(buchi.buffer(1.0))

    base = trimesh.creation.extrude_polygon(base_2d, SPESSORE_BASE)
    nerv = trimesh.creation.extrude_polygon(nerv_2d, ALTEZZA_TOT - SPESSORE_BASE)
    nerv.apply_translation([0, 0, SPESSORE_BASE])
    return trimesh.boolean.union([base, nerv], engine="manifold"), base_2d, nerv_2d


if __name__ == "__main__":
    mesh, base_2d, nerv_2d = costruisci()
    mesh.export(OUT / "modulo.stl")
    mesh.export(OUT / "modulo.3mf")
    print("watertight:", mesh.is_watertight)
    print("ingombro mm:", np.round(mesh.extents, 2))
    print("volume mm3:", round(mesh.volume, 1))
    print("area base mm2:", round(base_2d.area, 1), " area nervatura mm2:", round(nerv_2d.area, 1))
