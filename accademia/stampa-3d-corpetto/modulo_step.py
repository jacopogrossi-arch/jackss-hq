"""Stesso modulo di modulo.py, ma come solido vero (BRep) in formato STEP, che Fusion apre senza convertire.
Uso:  python modulo_step.py   ->  modulo.step
"""
import math
from pathlib import Path

import cadquery as cq

import modulo as M

OUT = Path(__file__).parent
R = M.R
BASE, TOT = M.SPESSORE_BASE, M.ALTEZZA_TOT
LUNG_BRACCIO = 24.2   # dal centro alla fine dell'asse del braccio (come modulo.py)

base = cq.Workplane("XY").polygon(6, 2 * R).extrude(BASE)

raggio_foro = M.INSET_FORO * R
centri = [(raggio_foro * math.cos(math.radians(a)), raggio_foro * math.sin(math.radians(a))) for a in range(0, 360, 60)]
base = base.faces(">Z").workplane().pushPoints(centri).hole(M.DIAM_FORO)

nerv = None
for ang in (90, 210, 330):
    c = (LUNG_BRACCIO / 2 * math.cos(math.radians(ang)), LUNG_BRACCIO / 2 * math.sin(math.radians(ang)))
    braccio = (
        cq.Workplane("XY").workplane(offset=BASE).center(*c)
        .slot2D(LUNG_BRACCIO + M.LARG_NERV, M.LARG_NERV, ang).extrude(TOT - BASE)
    )
    nerv = braccio if nerv is None else nerv.union(braccio)

apotema_interno = R * math.sqrt(3) / 2 - 0.6
taglio = cq.Workplane("XY").workplane(offset=BASE).polygon(6, 2 * apotema_interno * 2 / math.sqrt(3)).extrude(TOT - BASE)
nerv = nerv.intersect(taglio)

modulo = base.union(nerv).clean()
cq.exporters.export(modulo, str(OUT / "modulo.step"))

bb = modulo.val().BoundingBox()
print("ingombro mm:", round(bb.xlen, 3), round(bb.ylen, 3), round(bb.zlen, 3))
print("volume mm3:", round(modulo.val().Volume(), 1), " solido valido:", modulo.val().isValid())
