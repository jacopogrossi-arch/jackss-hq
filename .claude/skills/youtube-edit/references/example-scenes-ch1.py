# Video #2, chapter 1 (0-127 s), the way Jacopo asked on 01/11/2026: not "the old formats on a green background", but a motion plate IMPROVISED for every explanation, in Joseph's style
# (full-frame green scene, key word in gold serif, every element on the word that names it, dashed links, the face in the square PiP).
# usage: python build_ch1.py   -> C1/public (composed, not rendered)
import json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.abspath(os.path.join(HERE, ".."))
SK = os.path.abspath(os.path.join(HERE, "../../../.claude/skills/youtube-edit"))
sys.path.insert(0, os.path.join(SK, "formats"))
from scene import Scene  # noqa: E402
from tracker import tracker  # noqa: E402
from pip import pip  # noqa: E402
from plates_base import write_plate_sounds  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

SB = json.load(open(os.path.join(P, "storyboard.json"), encoding="utf-8"))
CROP = (630, 250, 700)
LOGO_CL, LOGO_CV = "img/logos/claude.svg", "img/logos/canva.svg"
TR = {"royal": "img/pres/p02.jpg", "body": "img/pres/p05.jpg", "onlife": "img/pres/p08.jpg"}

plates, pips, tracks = [], [], iter(range(10, 30))
ta = iter(range(20, 400, 30))


def S(cid, a, b, **kw):
    return Scene(cid, a, b, track=next(tracks), track_audio=next(ta), **kw)


# ---- P1  27.7-37.6  "lasciare carta bianca a Claude ... senza utilizzo di mano umana"
s = S("c1", 27.7, 37.6, title="Carta *bianca*")
page = s.photo(160, 320, 380, 520, "img/blank.png", t=28.32, anchor="carta bianca", rot=-3)
cl = s.disc(900, 580, t=28.96, anchor="claude", logo=LOGO_CL, label="Claude", r=110)
s.link(page, cl, 29.1)
solo = s.pill(1230, 420, "Da *solo*", t=32.72, anchor="solo", kind="mint")
s.link(cl, solo, 32.85)
mano = s.pill(1230, 570, "Mano umana", t=35.28, anchor="mano", w=330)
s.link(cl, mano, 35.4)
s.strike(mano, 36.16)
plates.append(s.build()); pips.append((27.7, 37.6))

# ---- P2  41.2-64.7  "uno strumento, non un sostituto"
s = S("c2", 41.2, 64.7, title="*Strumento*, non sostituto")
io = s.disc(880, 580, t=41.6, anchor="io", text="Io", r=100)
t1 = s.pill(150, 330, "Claude", t=42.56, anchor="claude", logo=LOGO_CL, w=330)
t2 = s.pill(150, 460, "Procreate", t=47.68, anchor="procreate", w=330)
t3 = s.pill(150, 590, "Canva", t=48.8, anchor="canva", logo=LOGO_CV, w=330)
for p, tt in ((t1, 42.7), (t2, 47.8), (t3, 48.9)):
    s.link(p, io, tt)
o1 = s.pill(1210, 330, "Risultati *migliori*", t=52.32, anchor="risultati migliori", w=470)
o2 = s.pill(1210, 460, "In meno *tempo*", t=53.6, anchor="minor tempo", w=470)
o3 = s.pill(1210, 590, "Sostituisce l'umano", t=55.68, anchor="sostituisce", w=470, kind="bad")
for p, tt in ((o1, 52.4), (o2, 53.7), (o3, 55.8)):
    s.link(io, p, tt)
s.strike(o3, 56.6)
fin = s.pill(150, 790, "La parte *umana*: la cosa principale", t=59.2, anchor="umana", kind="mint", size=36, w=960, h=92)
s.glow(fin, 59.4)
plates.append(s.build()); pips.append((41.2, 64.7))

# ---- P3  66.1-70.0  the step map (format 47)
labels = [t["label"] for t in SB["tags"]]
tk = tracker(labels, active=0, title="Dove *siamo*", t_in=66.1, t_out=70.0, at=67.003, anchor="primo capitolo", cid="tk1")
plates.append(tk); pips.append((66.1, 70.0))

# ---- P4  72.1-84.9  the book, the three trends, the photos sent to Claude
s = S("c4", 72.1, 84.9, title="Tre *trend*, A/I 27")
s.pill(150, 232, "Libro di *tendenze*", t=72.72, anchor="tendenze", kind="mint", w=520)
cards = []
for k, (nm, t, key) in enumerate((("Royal Humour", 76.77, "royal"), ("Body Talk", 77.33, "body"), ("Onlife", 78.13, "onlife"))):
    cards.append(s.photo(150 + k * 450, 330, 400, 360, TR[key], t=t, caption=nm, rot=(-2, 1.5, -1)[k]))
dc = s.disc(800, 850, t=81.89, anchor="claude", logo=LOGO_CL, label="Claude", r=90)
for k, c in enumerate(cards):
    s.link(c, dc, 82.45 + 0.2 * k, mode="v")
an = s.pill(1000, 800, "Analizza *i trend*", t=83.73, anchor="analizza", kind="mint", w=430)
s.link(dc, an, 83.8)
plates.append(s.build()); pips.append((72.1, 84.9))

# ---- P5  86.6-102.3  what Claude has to present
s = S("c5", 86.6, 102.3, title="Deve *presentare*")
dc = s.disc(270, 500, t=87.17, anchor="presenti", logo=LOGO_CL, label="Claude", r=100)
rows = [("Outfit", 89.33, "img/pres/p04.jpg", 270), ("Mood board *tecnica*", 90.37, "img/pres/p03.jpg", 390), ("Mood board *evolutiva*", 91.89, "img/pres/p06.jpg", 510), ("Pagina di *concept*", 99.65, "img/pres/p02.jpg", 630)]
ids = []
for lab, t, im, y in rows:
    p = s.pill(520, y, lab, t=t, w=560, h=100, img=im, size=34)
    s.link(dc, p, t + 0.05)
    ids.append(p)
for lab, t, y in (("Mood", 95.01, 470), ("Vibe", 95.73, 538), ("Materia", 98.53, 606)):
    s.pill(1130, y, lab, t=t, w=260, h=56, kind="mint", size=30)
plates.append(s.build()); pips.append((86.6, 102.3))

# ---- P6  107.0-114.3  3 + 3 + 3 + 3 = 12
s = S("c6", 107.0, 114.3, title="Alla *fine*", fade_out=0.3)
for k, (lab, t) in enumerate((("Outfit", 109.37), ("Mood evocative", 110.01), ("Mood tecniche", 111.61), ("Concept", 112.81))):
    x = 150 + k * 345
    s.pill(x, 330, lab, t=t, w=320, h=90, size=30)
    s.big(x + 90, 410, "3", t=t + 0.25, size=220)
s.big(150, 700, "= 12", t=113.1, size=260)
plates.append(s.build())

# ---- P7  114.0-124.4  Claude mixes the titles up, then they are put straight
s = S("c7", 114.0, 124.4, title="I *titoli*", title_t=114.57)
cl = s.disc(1640, 360, t=115.37, anchor="claude", logo=LOGO_CL, label="Claude", r=90)
for k, (key, t) in enumerate((("royal", 116.89), ("body", 117.15), ("onlife", 117.35))):
    s.photo(150 + k * 450, 280, 400, 340, TR[key], t=t)
tags = []
for k, (nm, t) in enumerate((("Royal Humour", 117.5), ("Body Talk", 117.7), ("Onlife", 117.9))):
    tags.append(s.pill(160 + k * 450, 650, nm, t=t, w=380, h=72))
conf = s.pill(1480, 520, "Si confonde", t=118.57, anchor="confondeva", kind="bad", w=330)
wrong = [450, 450, -900]
for tg, dx in zip(tags, wrong):
    s.shift(tg, 118.6, dx=dx, frm=(0, 0), d=0.7)
    s.glow(tg, 118.7, color="224,100,92")
for tg, dx in zip(tags, wrong):
    s.shift(tg, 120.49, dx=0, frm=(dx, 0), d=0.7)
    s.glow(tg, 120.6)
for tg in tags:
    s.tick(tg, 122.73)
s.strike(conf, 120.6)
plates.append(s.build()); pips.append((107.0, 124.4))


def prep(name):
    dst = os.path.join(HERE, name, "public")
    shutil.rmtree(os.path.join(HERE, name), ignore_errors=True)
    os.makedirs(dst)
    for n in os.listdir(os.path.join(P, "public")):
        s_, d = os.path.join(P, "public", n), os.path.join(dst, n)
        if n in ("renders", "snapshots", "index.html") or n.startswith("work-") or n == ".hyperframes":
            continue
        if os.path.isdir(s_):
            shutil.copytree(s_, d)
        elif os.path.getsize(s_) > 50e6:
            os.link(s_, d)
        else:
            shutil.copy2(s_, d)
    return dst


dst = prep("C1")
im = Image.new("RGB", (760, 1040), (250, 248, 243)); d = ImageDraw.Draw(im)
for y in range(150, 1000, 70):
    d.line((70, y, 690, y), fill=(226, 222, 212), width=3)
im.save(os.path.join(dst, "img/blank.png"))

B = json.loads(json.dumps(SB))
B.pop("preset", None); B.pop("glass_bg", None)
CH = 127.0
B["duration"] = CH + 0.5
B["beats"] = [b for b in B["beats"] if b.get("in", 0) < 20 and b["type"] == "gallery"]     # the hook gallery stays; every other beat of the chapter is replaced by a plate
B["camera"] = [c for c in B["camera"] if c[1] < 26]
B["tags"] = []
B["loops"] = [l for l in B.get("loops", []) if l.get("payoff", 0) < CH]
html, js = [], []
for pl in plates:
    html.append(pl["html"]); js.append(pl["js"])
for k, (a, b) in enumerate(pips):
    pp = pip(a, b, crop=CROP, cid="pip%d" % (k + 1))
    html.append(pp["html"]); js.append(pp["js"])
B["raw_html"] = "\n".join(html)
B["raw_js"] = "\n        ".join(js)
spec = os.path.join(HERE, "C1", "storyboard.json")
json.dump(B, open(spec, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
r = subprocess.run([sys.executable, os.path.join(SK, "scripts/compose.py"), "--spec", spec, "--out", dst], capture_output=True, text=True)
print(r.stdout[-500:].strip().replace("\n", " | "), r.stderr[-1500:])
write_plate_sounds(os.path.join(HERE, "C1", "public"), SK)
