"""video.py: "Il serpentone dell'Autogrill", un solo mondo 3D di circa 93 s (esterno al tramonto + store senza tetto), camera e etichette sulle parole della voce.
Uso: python video.py   -> scrive voce/voce-pause.wav (la voce con le pause tra i paragrafi) e la pagina in page/ (snapshot e render con hyperframes)."""
import json, math, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SK = "D:/ClaudeCodeTest/.claude/skills/youtube-edit"
sys.path.insert(0, SK + "/formats"); sys.path.insert(0, HERE)
from world3d import World3D, key  # noqa: E402
import store  # noqa: E402
from store import PATH, D  # noqa: E402

LEAD, TAIL = 0.35, 3.4          # v2: la voce parte subito (il primo secondo deve agganciare)
WORDS = json.load(open(os.path.join(HERE, "voce", "transcript.json"), encoding="utf-8"))
WORDS = WORDS if isinstance(WORDS, list) else WORDS["words"]
# pause aggiunte dopo queste parole (indice della parola che chiude il paragrafo -> secondi)
BREAKS = {"pavimento.": 1.1, "qualcosa.": 0.9, "serpentone.": 0.8, "mano.": 0.6, "tutto,": 0.6, "negozio.": 0.7, "sì.": 1.0, "Alemagna.": 0.4}


def plan_cuts():
    cuts, seen = [], set()
    for i, w in enumerate(WORDS[:-1]):
        t = w["text"]
        if t in BREAKS and (t, 1) not in seen:
            if t == "mano." and w["start"] < 60 and w["start"] > 45:      # non c'è: "mano." compare a 41.5 e a 65.2
                pass
            if t == "negozio." and w["start"] < 30:                        # "guarda il negozio" non chiude un paragrafo
                continue
            if t == "serpentone." and w["start"] > 40:
                continue
            cuts.append(((w["end"] + WORDS[i + 1]["start"]) / 2, BREAKS[t]))
    return cuts


CUTS = plan_cuts()


def V(t):
    """Tempo nella voce originale -> tempo nel video (attacco + pause aggiunte)."""
    return round(LEAD + t + sum(p for c, p in CUTS if t >= c), 3)


def at(word, n=1, after=0.0):
    """Tempo video dell'n-esima parola che comincia con `word` (dopo `after` secondi di voce)."""
    k = 0
    for w in WORDS:
        if w["start"] >= after and w["text"].lower().startswith(word.lower()):
            k += 1
            if k == n:
                return V(w["start"])
    raise KeyError(word)


def voice_track():
    src = os.path.join(HERE, "voce", "voce-v2.mp3"); out = os.path.join(HERE, "voce", "voce-only.wav")   # sfx.py ci aggiunge gli swish -> voce-pause.wav
    import wave
    raw = os.path.join(HERE, "voce", "voce-v2-48k.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", raw], check=True)
    with wave.open(raw, "rb") as r:
        sr, fr = r.getframerate(), r.getsampwidth() * r.getnchannels(); data = r.readframes(r.getnframes()); params = r.getparams()
    sil = lambda s: b"\0" * (int(round(s * sr)) * fr)
    out_b, prev = [sil(LEAD)], 0
    for c, p in CUTS:
        e = int(round(c * sr)) * fr
        out_b += [data[prev:e], sil(p)]; prev = e
    out_b += [data[prev:], sil(TAIL)]
    with wave.open(out, "wb") as w:
        w.setparams(params); w.writeframes(b"".join(out_b))
    return out


DUR = round(V(WORDS[-1]["end"]) + TAIL, 2)
RED = "#d2232a"

CSS = """<style>
  #host-w1 { background:linear-gradient(180deg, #1f3a66 0%, #4d6a94 30%, #e9a66b 62%, #ffd9a3 74%, #f1c08d 100%) !important; }
  #host-w1 .w3-wash, #host-w1 .w3-grid { display:none; }
  .w3-lab { font-size:40px !important; padding:16px 28px !important; }
  .w3-lab small { font-size:30px !important; }
  .ov { position:absolute; left:0; width:1920px; text-align:center; font-family:"Inter","Segoe UI",sans-serif; font-weight:800; color:#fbf7ee; letter-spacing:-.02em; opacity:0; white-space:nowrap;
        text-shadow:0 4px 30px rgba(0,0,0,.65), 0 2px 6px rgba(0,0,0,.55); }
  .ov i { font-family:"Playfair Display",Georgia,serif; font-style:italic; font-weight:500; color:#ffd98a; letter-spacing:0; }
  .ov.l { text-align:left; left:110px; width:auto; }
  .ov.pill { left:110px; width:auto; padding:18px 34px; border-radius:22px; background:rgba(18,17,16,.72); font-size:46px; font-weight:700; text-shadow:none; font-variant-numeric:tabular-nums; }
  .vig { position:absolute; inset:0; pointer-events:none; background:radial-gradient(closest-side at 50% 50%, transparent 68%, rgba(0,0,0,.32) 125%); }
</style>"""


def build_world():
    w = World3D("w1", 0.0, DUR, fov=40, fade=0.01)
    base = w.spec
    overlays = []      # (id, html, css, t, out)

    def ov(html, t, out, top, size=110, cls=""):
        i = "ov%d" % len(overlays); overlays.append((i, key(html), "top:%dpx;font-size:%dpx" % (top, size), cls, round(t, 3), round(out, 3)))

    def spec():
        s = base(); s.update(shadows=True, far=420, exposure=1.12, light="store", keyPos=[-26, 30, 30], shadowBox=[46, 40, 140], fog=["#f1c08d", 55, 330])
        s["texts"] = [dict(id=i, t=t, out=o) for i, _, _, _, t, o in overlays]
        return s
    w.spec = spec

    # ------------------------------------------------------------------ il mondo fuori
    w._obj("box", "grass", (0, -0.06, 20), 0, None, None, None, size=[700, 0.1, 500], color="#ffffff", rough=1.0, tex="grass")
    w._obj("road", "park", (0, 0.0, 13.5), 0, None, None, None, size=[62.4, 17], rk="parking")
    w._obj("road", "a1", (0, 0.0, 34), 0, None, None, None, size=[600, 15])
    w._obj("box", "kerb", (0, 0.1, 23.6), 0, None, None, None, size=[62.4, 0.25, 0.5], color="#cfcabe", rough=0.9)
    # v2.1: la vegetazione. Alberi "eroe" vicino all'edificio (ombre vere), un bosco fitto dietro e oltre l'autostrada, siepi, colline all'orizzonte
    seed = 11
    for k in range(18):
        seed = (seed * 1103515245 + 12345) % 2147483648; x = seed / 2147483648 * 110 - 55
        seed = (seed * 1103515245 + 12345) % 2147483648; z = -9 - seed / 2147483648 * 22
        w._obj("tree", "tr%d" % k, (x, 0, z), 0, None, None, None, size=[6.0 + (k % 4) * 1.3], kind="pine" if k % 3 == 0 else "leaf")
    for k, (x, z) in enumerate(((-40, 3), (-34, 7), (34, 3), (41, 9), (-46, 13), (47, 15), (-37, 17), (38, 18))):
        w._obj("tree", "ts%d" % k, (x, 0, z), 0, None, None, None, size=[6.5 + (k % 3)], kind="leaf" if k % 4 else "pine")
    w._obj("forest", "wood1", (0, 0, 0), 0, None, None, None, area=[-170, -95, 170, -32], n=520, h=9, seed=3, pines=0.35)
    w._obj("forest", "wood2", (0, 0, 0), 0, None, None, None, area=[-170, -32, -48, 26], n=150, h=8, seed=5, pines=0.3)
    w._obj("forest", "wood3", (0, 0, 0), 0, None, None, None, area=[48, -32, 170, 26], n=150, h=8, seed=7, pines=0.3)
    w._obj("forest", "wood4", (0, 0, 0), 0, None, None, None, area=[-200, 50, 200, 120], n=420, h=9, seed=9, pines=0.4)
    w._obj("hedge", "hg1", (-31, 0, 4.5), 0, None, None, None, to=[-31, 0, 22.5], n=22, r=0.75)
    w._obj("hedge", "hg2", (31, 0, 4.5), 0, None, None, None, to=[31, 0, 22.5], n=22, r=0.75)
    w._obj("hedge", "hg3", (-31, 0, 4.5), 0, None, None, None, to=[-8, 0, 4.5], n=22, r=0.6)
    w._obj("hedge", "hg4", (8, 0, 4.5), 0, None, None, None, to=[31, 0, 4.5], n=22, r=0.6)
    w._obj("hills", "hills", (0, 0, 0), 0, None, None, None, list=[[-160, -190, 70, 26], [-40, -210, 90, 34], [90, -200, 80, 30], [210, -180, 70, 22], [-220, 170, 80, 25], [40, 190, 90, 30], [200, 175, 70, 24]])
    for k, x in enumerate((-22, -8, 8, 22)):
        w._obj("lamp", "lp%d" % k, (x, 0, 22.6), math.pi / 2, None, None, None, size=[7])
    for k, (x, z, c, ry) in enumerate(((-12.6, 8.2, "#e9e6df", math.pi / 2), (-7.4, 8.2, "#2f3b4a", math.pi / 2), (8.2, 8.2, "#a7acb3", math.pi / 2), (13.4, 8.2, "#27496d", -math.pi / 2), (-15.2, 17.5, "#3b3b3d", math.pi / 2), (10.8, 17.5, "#e9e6df", -math.pi / 2))):
        w._obj("car", "pk%d" % k, (x, 0, z), ry, None, None, None, color=c)
    # traffico sull'autostrada: due carreggiate, passaggi a tempi fissi
    cols = ("#e9e6df", "#2f3b4a", "#a7acb3", "#27496d", "#7d1f1f", "#3b3b3d", "#c9b037")
    for k in range(22):
        t0 = -1.0 + k * 1.35 if k < 17 else at("Il", 1, 77) - 2.5 + (k - 17) * 1.5
        fwd = k % 2 == 0; z = (31.2, 28.6)[k // 2 % 2] if fwd else (36.8, 39.4)[k // 2 % 2]
        x0, x1 = (-130, 130) if fwd else (130, -130)
        w._obj("car", "tf%d" % k, (x0, 0, z), 0 if fwd else math.pi, None, [(max(t0, 0), 7.5 + (k % 3) * 0.8, (x1, 0, z), "linear")], None, color=cols[k % len(cols)])
    # l'auto di chi guarda: arriva nel parcheggio all'inizio, riparte alla fine
    tk = at("Il", 1, 77)
    w._obj("car", "me", (-27, 0, 19.5), 0, None, [(0.0, 2.9, (-2.6, 0, 19.5), "out")], None, color=RED, out=at("Ogni") - 1)
    w._obj("car", "me2", (-2.6, 0, 19.5), 0, None, [(tk + 0.6, 6.0, (70, 0, 19.5), "glide")], tk - 0.6, color=RED, rise=0)

    # ------------------------------------------------------------------ l'edificio
    store.add_store(w, "reale", walls=False)
    H = 3.3
    wall = dict(color="#ece8de", rough=0.9)
    w._obj("box", "wb", (0, H / 2, -D / 2 - 0.1), 0, None, None, None, size=[13.4, H, 0.2], **wall)
    w._obj("box", "wl", (-6.6, H / 2, 0), 0, None, None, None, size=[0.2, H, D], **wall)
    w._obj("box", "wr", (6.6, H / 2, 0), 0, None, None, None, size=[0.2, H, D], **wall)
    t_roof = at("guarda")
    w._obj("box", "glass", (0.1, 1.3, D / 2 + 0.05), 0, None, None, None, size=[8.4, 2.6, 0.08], color="#9fc6d8", rough=0.1, metal=0.3, alpha=0.28, out=t_roof)
    for k, x in enumerate((-6.2, -3.9, 4.3, 6.2)):
        w._obj("box", "fp%d" % k, (x, 1.3, D / 2 + 0.05), 0, None, None, None, size=[0.5 if abs(x) > 6 else 0.3, 2.6, 0.2], out=t_roof, **wall)
    w._obj("box", "fascia", (0, 2.95, D / 2 + 0.1), 0, None, [(t_roof, 1.6, (0, 9.5, D / 2 + 0.1), "glide")], None, size=[13.6, 0.75, 0.3], color=RED, rough=0.5, out=t_roof + 0.5)
    w._obj("box", "roof", (0, H + 0.15, 0), 0, None, [(t_roof, 1.6, (0, 10.0, 0), "glide")], None, size=[14.0, 0.3, 9.8], color="#dcd8ce", rough=0.9, out=t_roof + 0.5)
    w._obj("card", "sign", (0, 4.25, D / 2 + 0.2), 0, None, [(t_roof, 1.6, (0, 10.8, D / 2 + 0.2), "glide")], None, w=6.4, h=1.25, text="AUTOGRILL", color=RED, ink="#ffffff", size=150, radius=0.12, out=t_roof + 0.5)
    w._obj("box", "totp", (-21, 3.5, 22.4), 0, None, None, None, size=[0.35, 7, 0.35], color="#8b8f94", rough=0.4, metal=0.6)
    w._obj("card", "tots", (-21, 7.6, 22.4), 0.5, None, None, None, w=3.4, h=1.5, text="AUTOGRILL", color=RED, ink="#ffffff", size=170, radius=0.1)
    # il tetto torna per il finale
    w._obj("box", "roof2", (0, H + 0.15, 0), 0, None, None, tk - 2.2, size=[14.0, 0.3, 9.8], color="#dcd8ce", rough=0.9, rise=3.0, tin=1.2)
    w._obj("box", "fascia2", (0, 2.95, D / 2 + 0.1), 0, None, None, tk - 2.2, size=[13.6, 0.75, 0.3], color=RED, rough=0.5, rise=3.0, tin=1.2)
    w._obj("card", "sign2", (0, 4.25, D / 2 + 0.2), 0, None, None, tk - 2.2, w=6.4, h=1.25, text="AUTOGRILL", color=RED, ink="#ffffff", size=150, radius=0.12, rise=3.0, tin=1.2)

    # ------------------------------------------------------------------ il serpentone
    t_dritta, t_sola, t_piu, t_si = at("strada"), at("ce"), at("serpentone", 2), at("sì")
    a, b = PATH[0], PATH[-1]
    w._obj("dots", "dritta", (a[0], 0.07, a[1] - 0.7), 0, None, None, t_dritta, size=[0.16], to=[b[0], 0.07, b[1] - 0.7], n=26, color="#8b8f94", rise=0, tin=0.4, out=t_sola - 0.1)
    for name, t0, out in (("pa", t_sola, t_piu + 0.6), ("pb", None, None)):
        t = t0
        for k, (p, q) in enumerate(zip(PATH, PATH[1:])):
            ln = math.hypot(q[0] - p[0], q[1] - p[1])
            kw = dict(size=[0.16], to=[q[0], 0.07, q[1]], n=max(2, round(ln / 0.34)), color=RED, rise=0, tin=0.3)
            if name == "pa":
                w._obj("dots", "%s%d" % (name, k), (p[0], 0.07, p[1]), 0, None, None, t, out=out, **kw); t += 0.17
            else:
                w._obj("dots", "%s%d" % (name, k), (p[0], 0.07, p[1]), 0, None, None, t_si - 0.6 + 0.06 * k, **kw)

    # ------------------------------------------------------------------ la camera (una mossa alla volta) e le etichette
    TOP = ((0.0, 21.5, 10.5), (0.0, 0.0, 0.4))
    CAMS = []

    def C(pos, look, t, d, ease="hand"):
        CAMS.append((pos, look, t, d, ease))
    w.cam((-31.5, 0.9, 23.2), look=(-21, 1.6, 17.5))                                                     # v2: si parte già in corsa, bassi accanto all'auto rossa
    C((-10.5, 2.3, 19.5), look=(-4.6, 1.9, 4.5), t=0.0, d=at("caff") - 0.1, ease="out")              # "Entri in Autogrill per un caffè"
    ov("Perché in Autogrill *non si va mai dritti*?", -0.6, at("Esci") - 0.15, 90, 84)
    w.label("in", (0, 2.4, 0), "un *caffè*", t=at("caff"), anchor="caffè", dx=-330, dy=-150, out=at("Non") - 0.2)
    C((0.5, 2.3, 18.5), look=(4.6, 1.7, 4.5), t=at("Esci") - 0.05, d=1.1)                            # "Esci con..."
    w.label("outg", (0.6, 2.4, 0), "un *salame*", t=at("salame"), anchor="salame", dx=90, dy=-190, out=at("Non") - 0.2)
    w.label("outg", (0.6, 1.5, 0), "un *peluche*", t=at("peluche"), anchor="peluche", dx=110, dy=-50, out=at("Non") - 0.2)
    w.label("outg", (0.6, 0.6, 0), "un Toblerone *gigante*", t=at("tublerone"), anchor="Toblerone", dx=110, dy=60, out=at("Non") - 0.2)
    C((3.4, 2.45, 8.4), look=(1.0, 0.2, 1.4), t=at("Non"), d=2.2)                                     # dentro, verso il pavimento
    ov("È colpa del *pavimento*.", at("colpa", 2), at("Autogill") - 0.25, 150, 120)
    C((1.5, 4.2, 27), look=(0, 2.9, 4.5), t=at("Autogill") - 0.3, d=1.6)                             # la facciata con l'insegna
    ov("*1977*", at("1977"), at("E", 1, 16) - 0.2, 110, 190)
    w.label("sign", (-2.4, -0.5, 0), "*Pavesi*", t=at("Pavesi"), anchor="Pavesi", dx=-300, dy=260, out=at("E", 1, 16) - 0.2)
    w.label("sign", (0, -0.5, 0), "*Motta*", t=at("Motta"), anchor="Motta", dx=-90, dy=260, out=at("E", 1, 16) - 0.2)
    w.label("sign", (2.4, -0.5, 0), "*Alemagna*", t=at("Alemagna"), anchor="Alemagna", dx=110, dy=260, out=at("E", 1, 16) - 0.2)
    C((-16, 3.2, 26.5), look=(2, 0.9, 30.5), t=at("E", 1, 16) - 0.1, d=1.7)                          # l'autostrada: il cliente che passa
    ov("ha *fretta*", at("fretta"), at("Ha", 1, 21) - 0.1, 150, 96, "l")
    ov("è *stanco*", at("stanco"), at("Ha", 1, 21) - 0.1, 270, 96, "l")
    ov("domani non *tornerà*", at("domani"), at("Ha", 1, 21) - 0.1, 390, 96, "l")
    ov("pochi *minuti* per vendergli qualcosa", at("pochi"), at("Allora", 1, 22) - 0.3, 820, 84)
    C(TOP[0], look=TOP[1], t=at("Allora", 1, 22) - 0.2, d=at("L'ingresso") - at("Allora", 1, 22) + 0.15)                                              # il tetto si alza: lo store dall'alto
    w.label("in", (0, 2.3, 0), "*ingresso*", t=at("L'ingresso"), anchor="ingresso", dx=-360, dy=-10)
    w.label("outg", (0, 2.3, 0), "*uscita*", t=at("l'uscita"), anchor="uscita", dx=150, dy=-10)
    w.label("s2", (0, 0.2, 3.3), "il *serpentone*", t=at("serpentone"), anchor="serpentone", dx=-170, dy=120, out=at("Più") + 0.2)
    C((0.0, 20.0, 9.2), look=(0.0, 0.0, 0.2), t=at("L'ingresso"), d=at("L'idea") - at("L'ingresso") - 0.1, ease="linear")
    w.labels[-3]["out"] = w.labels[-2]["out"] = w._r(at("Più") + 0.2)
    C((-2.9, 1.65, -3.6), look=(-2.9, 1.15, 3.0), t=at("Più") + 0.25, d=2.0)                         # dentro: prima corsia
    C((-2.9, 1.65, 1.3), look=(-2.4, 1.1, 4.4), t=at("prodotti") + 0.4, d=1.9, ease="glide")
    C((-0.9, 1.65, 3.4), look=(-0.9, 1.1, -3.0), t=at("quello") - 0.2, d=1.5)                        # la curva, seconda corsia
    C((-0.9, 1.65, 0.6), look=(-0.9, 1.1, -3.4), t=at("prima", 1, 39), d=1.7, ease="glide")
    C((-2.75, 0.75, 0.9), look=(-1.9, 0.45, 0.0), t=at("La", 1, 43.5) - 0.3, d=1.4)                  # giocattoli: ad altezza bambino, orsetti e palloni
    w.label("s1", (-0.6, 0.62, -0.36), "i *giocattoli*", t=at("giocattoli"), anchor="giocattoli", dx=80, dy=-260, out=at("la", 1, 48) - 0.1)
    w.label("s1", (-1.3, 0.22, -0.36), "altezza *bambino*", t=at("altezza"), anchor="altezza bambino", dx=120, dy=60, out=at("non", 1, 46.5) + 0.2)
    C((-2.8, 1.7, 1.2), look=(-1.9, 0.95, -0.4), t=at("non", 1, 46.5), d=1.2)                        # ...non ad altezza tua
    C((-1.0, 1.5, -1.6), look=(-0.15, 1.25, 1.2), t=at("la", 1, 48) - 0.1, d=1.2)                    # tipici: la corsia con l'insegna
    w.label("s2", (0.4, 1.95, -0.36), "prodotti *tipici*", t=at("prodotici"), anchor="tipici", dx=-330, dy=-200, out=at("Formaggi") - 0.1)
    C((-0.9, 0.6, -0.4), look=(-0.2, 0.25, 0.7), t=at("Formaggi") - 0.15, d=0.85)                     # le forme di parmigiano
    w.label("s2", (0.6, 0.24, -0.36), "*formaggi*", t=at("Formaggi"), anchor="formaggi", dx=90, dy=-200, out=at("salumi") - 0.1)
    C((-0.95, 1.45, -0.3), look=(-0.05, 1.85, 1.1), t=at("salumi") - 0.15, d=0.85)                  # i salami appesi
    w.label("s2", (0.4, 2.0, 0.0), "*salumi*", t=at("salumi"), anchor="salumi", dx=110, dy=60, out=at("regalo") - 0.1)
    C((-0.9, 0.85, -0.1), look=(-0.2, 0.6, 1.1), t=at("regalo") - 0.15, d=0.9)                       # il vino: il regalo per casa
    w.label("s2", (0.3, 0.55, -0.36), "il *regalo* per casa", t=at("regalo"), anchor="regalo", dx=-560, dy=-160, out=at("la", 1, 54) - 0.1)
    C((1.0, 1.3, 1.7), look=(1.95, 1.0, -0.1), t=at("la", 1, 54) - 0.1, d=1.2)                      # dolci: biscotti, panettoni
    w.label("s3", (-0.6, 1.45, -0.36), "i *dolci*", t=at("dolci"), anchor="dolci", dx=-360, dy=-170, out=at("Giganti") - 0.1)
    C((1.1, 1.0, -0.6), look=(1.8, 0.9, -1.8), t=at("Giganti") - 0.15, d=0.9)                       # le barrette giganti
    w.label("s3", (0.6, 0.98, -0.36), "*giganti*", t=at("Giganti"), anchor="giganti", dx=120, dy=-200, out=at("quando") - 0.1)
    C((5.45, 1.65, -2.9), look=(4.3, 0.95, 0.4), t=at("quando") - 0.1, d=1.8)                        # la cassa
    w.label("till0", (0, 0.5, 0.2), "la *cassa*", t=at("cassa"), anchor="cassa", dx=-420, dy=-260, out=at("È", 1, 65) - 0.1)
    w.label("imp0", (0, 0.3, 0.16), "le *caramelle*, le *gomme*", t=at("caramelle"), anchor="caramelle", dx=-640, dy=30, out=at("È", 1, 65) - 0.1)
    ov("l'ultima *tentazione*", at("l'ultima"), at("È", 1, 65) - 0.1, 880, 84)
    C((5.3, 1.65, -0.4), look=(4.45, 0.95, 2.4), t=at("l'ultima"), d=1.5, ease="glide")
    C(TOP[0], look=TOP[1], t=at("È", 1, 65) - 0.05, d=2.0)                                           # di nuovo dall'alto
    ov("lo stesso trucco di *Ikea* e dei *duty free*", at("Ikea") - 0.2, at("un", 1, 68.5) - 0.1, 90, 84)
    ov("un percorso *obbligato*", at("percorso", 1, 68), at("Oggi") - 0.2, 90, 110)
    ov("travestito da *negozio*", at("travestito"), at("Oggi") - 0.2, 225, 84)
    C((0.0, 19.6, 9.0), look=(0.0, 0.0, 0.2), t=at("un", 1, 68.5), d=at("Il", 1, 77) - at("un", 1, 68.5) - 2.4, ease="linear")
    ov("in alcuni locali nuovi: *niente serpentone*", at("serpentone", 2), at("in", 1, 75) - 0.1, 90, 80)
    ov("in quasi tutti gli altri: *sì*", at("quasi"), tk - 2.3, 90, 96)
    C((13, 3.4, 28), look=(4, 1.9, 8), t=tk - 2.3, d=2.4)                                            # fuori: si riparte
    ov("il caffè: poco più di *un euro*", at("caffè", 2), DUR, 130, 84)
    ov("il percorso per uscire: un po' di *più*", at("percorso", 2), DUR, 245, 84)
    C((17, 3.0, 30), look=(9, 1.7, 9), t=tk + 0.2, d=DUR - tk - 0.3, ease="linear")
    CAMS.sort(key=lambda c: c[2])
    for k, (pos, look, t, d, ease) in enumerate(CAMS):
        nxt = CAMS[k + 1][2] if k + 1 < len(CAMS) else DUR
        d2 = min(d, nxt - t - 0.03)
        if d2 < d - 0.01: print("  mossa a %.2f accorciata %.2f -> %.2f" % (t, d, d2))
        w.cam(pos, look=look, t=t, d=d2, ease=ease)
        gap = nxt - (t + d2) - 0.06
        if gap > 0.35:
            # deriva lenta fino alla mossa dopo: la camera non sta mai ferma (dolly verso il soggetto + un po' di carrello laterale)
            dx, dy, dz = look[0] - pos[0], look[1] - pos[1], look[2] - pos[2]
            dist = math.sqrt(dx * dx + dy * dy + dz * dz); hl = math.hypot(dx, dz) or 1.0
            f = min(0.07, 0.022 * gap); lx, lz = -dz / hl * dist * f * 0.6, dx / hl * dist * f * 0.6
            p2 = (pos[0] + dx * f + lx, pos[1] + dy * f, pos[2] + dz * f + lz); l2 = (look[0] + lx, look[1], look[2] + lz)
            w.cam(p2, look=l2, t=t + d2 + 0.03, d=gap, ease="linear")
    return w, overlays


def counter_js():
    """Il contatore dei prodotti visti mentre si cammina (seek-safe: funzione del tempo)."""
    t0, t1 = at("Più"), at("Ogni") - 0.3
    return ("<div class='ov pill' id='cnt' style='top:900px'>prodotti che ti passano davanti: <b id='cntn'>0</b></div>"
            "<script>window.addEventListener('hf-seek', function(e){ var t=e.detail.time, a=%.3f, b=%.3f, el=document.getElementById('cnt'); "
            "var k=Math.max(0,Math.min(1,(t-a)/(b-a))); el.style.opacity=(t>a+0.4&&t<b)?Math.min(1,(t-a-0.4)/0.3, (b-t)/0.3):0; "
            "document.getElementById('cntn').textContent=Math.round(k*k*640); });</script>" % (t0, t1)
            + "<div id='endf' style='position:absolute;inset:0;background:#000;opacity:0;pointer-events:none'></div>"
            "<script>window.addEventListener('hf-seek', function(e){ var t=e.detail.time; document.getElementById('endf').style.opacity=Math.max(0,Math.min(1,(t-%.3f)/0.6)); });</script>" % (DUR - 0.7))


def main():
    voice_track()
    w, overlays = build_world()
    page = os.path.join(HERE, "page")
    World3D.page(page, [w], duration=DUR)
    shutil.copy(os.path.join(HERE, "vendor", "world3d.js"), os.path.join(page, "vendor", "world3d.js"))
    p = os.path.join(page, "index.html"); s = open(p, encoding="utf-8").read()
    extra = "".join('<div class="ov %s" id="%s" style="%s">%s</div>' % (cls, i, css, html) for i, html, css, cls, _, _ in overlays) + '<div class="vig"></div>' + counter_js()
    mark = '<svg class="w3-ln"'
    assert s.count(mark) == 1
    s = s.replace(mark, extra + mark).replace("</head>", CSS + "</head>").replace("html, body { margin: 0; background: #0A2B1E; }", "html, body { margin: 0; background: #1f3a66; }")
    open(p, "w", encoding="utf-8").write(s)
    json.dump({"duration": DUR, "cuts": CUTS, "labels": [(L["text"], L["at"]) for L in w.labels], "overlays": [(o[1], o[4], o[5]) for o in overlays]}, open(os.path.join(HERE, "timing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    subprocess.run([sys.executable, os.path.join(HERE, "sfx.py")], check=True)
    print("durata %.2f s, %d oggetti, %d mosse di camera, %d etichette, %d scritte" % (DUR, len(w.objects), len(w.cams) - 1, len(w.labels), len(overlays)))


if __name__ == "__main__":
    main()
