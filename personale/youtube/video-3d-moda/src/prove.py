# Proofs of the new 3D effects (13/11/2026): each one is a short Prima | Dopo pair on the same scene. Pages go in prove/<name>/ ; render them with prove-render.sh logic (see README).
import os, sys
SK = "D:/ClaudeCodeTest/.claude/skills/youtube-edit"
sys.path.insert(0, SK + "/formats")
from world3d import World3D

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE + "/prove"


def scene(name, title, sub, dur, look=True, shutter=None, whip=False, dof=None, passes=False, close=False):
    w = World3D("p", 0.0, dur, title=title, sub=sub, title_out=dur - 0.3, fov=34, fade=0.3)
    if look:
        w.look(floor="#3a281b", wall="#4d3827")
    if shutter is not None:
        w.shutter(shutter)
    w.trouser("tr", pos=(0, 0, 0), rot_y=-0.35, color="#6f7452", turn=[(0, dur, 0.5, "smooth")])
    w.card("sheet", (-0.95, 0.45, -0.4), w=0.62, h=0.86, text="*Scheda*", sub="tecnica · Drop 1", rot_y=0.45)
    w.solid("roll", "cyl", (0.72, 0.21, -0.2), (0.22, 0.42), fabric=True, color="#7b7d5a", rot_y=0.3)
    w.solid("roll2", "cyl", (1.0, 0.21, -0.5), (0.22, 0.42), fabric=True, color="#8a4b2d", rot_y=0.1)
    if passes:
        w.base_pass("ink")
        w.wipe("clay", 1.7, 0.9)
        w.wipe("final", 3.9, 0.9)
    if close:
        w.cam((0.5, 1.0, 1.3), look=(0.08, 0.98, 0.1))
        w.cam((0.3, 1.1, 0.95), look=(0.075, 1.0, 0.11), t=0.5, d=dur - 1.0, ease="glide")
        if dof:
            w.dof(0.4, dur - 0.8, dof)
    elif whip:
        w.cam((1.3, 0.9, 2.2), look=(0.1, 0.7, 0))
        w.cam((-1.4, 0.9, 2.2), look=(-0.1, 0.7, 0), t=1.2, d=0.55, ease="hand")         # a whip across the room: ~4.6 m/s
        w.cam((-1.0, 0.85, 2.0), look=(0, 0.7, 0), t=1.9, d=dur - 2.0, ease="glide")
    else:
        w.cam((1.2, 0.95, 2.6), look=(0, 0.72, 0))
        w.cam((0.3, 0.9, 1.9), look=(0, 0.72, 0), t=0.3, d=dur - 0.6, ease="glide")
    return w


PAIRS = {
    "01-veneziana":   [("prima", dict(title="Prima", sub="luce verde, ombre finte a macchia", look=False, dur=5.0)),
                       ("dopo", dict(title="Dopo", sub="una luce con un motivo: la veneziana", look=True, dur=5.0))],
    "02-passaggi":    [("dopo", dict(title="Tre passaggi, una scena", sub="inchiostro, argilla, finale: la barra rossa li lega", look=True, dur=6.5, passes=True))],
    "03-motion-blur": [("prima", dict(title="Prima", sub="shutter chiuso: lo scatto è netto", look=True, dur=3.6, shutter=0, whip=True)),
                       ("dopo", dict(title="Dopo", sub="shutter 0,8: lo scatto sfuma", look=True, dur=3.6, shutter=0.8, whip=True))],
    "04-profondita":  [("prima", dict(title="Prima", sub="tutto a fuoco", look=True, dur=4.0, close=True)),
                       ("dopo", dict(title="Dopo", sub="profondità di campo: il fuoco resta sulla piega", look=True, dur=4.0, close=True, dof=0.03))],
}
for pair, items in PAIRS.items():
    for tag, kw in items:
        d = "%s/%s-%s" % (OUT, pair, tag)
        os.makedirs(d, exist_ok=True)
        kw = dict(kw)
        dur = kw.pop("dur")
        w = scene(pair, kw.pop("title"), kw.pop("sub"), dur, **kw)
        World3D.page(d, [w], duration=dur)
        print(d)
