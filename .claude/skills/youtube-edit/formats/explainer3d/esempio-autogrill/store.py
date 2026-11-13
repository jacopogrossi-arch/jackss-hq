"""store.py: l'autogrill in 3D, uguale per ogni plate. Metri; x verso destra, z verso la camera, pavimento a y = 0.
Pianta 13 x 9: ingresso davanti a sinistra, bar in fondo a sinistra, tre gondole che obbligano al serpentone, casse a destra, uscita davanti a destra."""
import math

W, D = 13.0, 9.0
# il serpentone: i punti del percorso (x, z)
PATH = [(-5.0, 4.3), (-5.0, -1.6), (-2.9, -1.6), (-2.9, 3.0), (-0.9, 3.0), (-0.9, -3.0), (1.1, -3.0), (1.1, 3.0), (3.2, 3.0), (3.2, -3.0), (5.2, -3.0), (5.2, 4.3)]
SHELVES = [("s1", -1.9, -1.2, "giocattoli", "#e3c47f"), ("s2", 0.1, 1.2, "tipici", "#c9703f"), ("s3", 2.1, -1.2, "dolci", "#5EE6A8")]     # id, x, z del centro, reparto, colore della testata
SHELF = (6.2, 1.7, 0.7)
HDR = {"giocattoli": ("GIOCATTOLI", "#e0a400"), "tipici": ("PRODOTTI TIPICI", "#b5541c"), "dolci": ("DOLCI", "#c2185b")}       # lunghezza, altezza, profondità
THEMES = {"reale": {"giocattoli": ["#e63946", "#ffb703", "#219ebc", "#8ecae6", "#f28482", "#90be6d"], "tipici": ["#8d5524", "#c68642", "#f4f1de", "#a4161a", "#e9c46a", "#606c38"],
                    "dolci": ["#6a4c93", "#f4a261", "#e76f51", "#ffd166", "#f4f1de", "#9d4edd"]},
          "plastico": {"giocattoli": ["#e3c47f", "#f4efe6", "#d8c9a3", "#f1dcaa"], "tipici": ["#c9703f", "#e9e2d2", "#a85a30", "#d8c9a3"], "dolci": ["#5EE6A8", "#f4efe6", "#2f8f6a", "#bfeeda"]}}


def add_store(w, look="plastico", walls=True):
    """Mette lo store nel mondo `w` (World3D). look: "plastico" (lo stile delle plate) o "reale"."""
    R = look == "reale"
    w._obj("floor", "floor", (0, 0, 0), 0, None, None, None, size=[W, D], look=look)
    wall = dict(color="#ece8de" if R else "#f4efe6", rough=0.9, alpha=None if R else 0.16)
    if walls:
        h = 2.6 if R else 1.3
        w._obj("box", "wb", (0, h / 2, -D / 2 - 0.06), 0, None, None, None, size=[W + 0.24, h, 0.12], **wall)
        w._obj("box", "wl", (-W / 2 - 0.06, h / 2, 0), 0, None, None, None, size=[0.12, h, D], **wall)
        w._obj("box", "wr", (W / 2 + 0.06, h / 2, 0), 0, None, None, None, size=[0.12, h, D], **wall)
    # il bar: bancone, retrobanco, macchina del caffè
    w._obj("box", "bar", (-4.6, 0.55, -3.0), 0, None, None, None, size=[3.4, 1.1, 0.7], color="#3a2a1e" if R else "#e9e2d2", rough=0.5)
    w._obj("box", "bartop", (-4.6, 1.12, -3.0), 0, None, None, None, size=[3.5, 0.05, 0.8], color="#d9d5cb" if R else "#e3c47f", rough=0.3, metal=0.2)
    w._obj("box", "back", (-4.6, 1.0, -4.15), 0, None, None, None, size=[3.4, 2.0, 0.4], color="#5a4332" if R else "#d8c9a3", rough=0.7)
    w._obj("box", "mac", (-5.2, 1.37, -3.0), 0, None, None, None, size=[0.7, 0.45, 0.5], color="#c9ccd1", rough=0.25, metal=0.85)
    for k in range(4):
        w._obj("cyl", "cup%d" % k, (-4.3 + 0.28 * k, 1.19, -2.9), 0, None, None, None, size=[0.09, 0.09], color="#ffffff", rough=0.4)
    # le tre gondole (lungo z)
    for sid, x, z, theme, accent in SHELVES:
        if R:
            w._obj("shelf", sid, (x, 0, z), math.pi / 2, None, None, None, size=list(SHELF), look=look, accent=HDR[theme][1], label=HDR[theme][0], theme=theme, hang=theme == "tipici", seed=len(theme), rows=4)
        else:
            w._obj("shelf", sid, (x, 0, z), math.pi / 2, None, None, None, size=list(SHELF), look=look, accent=accent, palette=THEMES[look][theme], seed=len(theme), rows=4)
    # casse: due banchi con l'espositore degli acquisti d'impulso
    for k, z in enumerate((-0.6, 1.7)):
        w._obj("box", "till%d" % k, (4.25, 0.45, z), 0, None, None, None, size=[0.7, 0.9, 1.5], color="#3a2a1e" if R else "#e9e2d2", rough=0.5)
        w._obj("box", "reg%d" % k, (4.25, 1.05, z - 0.4), 0, None, None, None, size=[0.4, 0.3, 0.35], color="#2b2b2e" if R else "#0d3524", rough=0.4)
        w._obj("shelf", "imp%d" % k, (4.25, 0.9, z + 0.45), 0, None, None, None, size=[0.6, 0.5, 0.3], look=look, palette=THEMES[look]["dolci"], rows=2, pw=0.1, seed=9 + k, **({"theme": "cassa"} if R else {}))
    # ingresso e uscita
    w._obj("gate", "in", (PATH[0][0], 0, D / 2), 0, None, None, None, size=[1.6, 2.2], look=look, color="#5EE6A8")
    w._obj("gate", "outg", (PATH[-1][0], 0, D / 2), 0, None, None, None, size=[1.6, 2.2], look=look, color="#e3c47f")


def add_path(w, t0=None, step=0.35, y=0.06, color="#e3c47f", size=0.11):
    """Il serpentone a puntini sul pavimento. t0 (tempo del video) = i tratti si accendono uno dopo l'altro; None = tutto acceso."""
    t = t0
    for k, (a, b) in enumerate(zip(PATH, PATH[1:])):
        ln = math.hypot(b[0] - a[0], b[1] - a[1])
        w._obj("dots", "pt%d" % k, (a[0], y, a[1]), 0, None, None, t, size=[size], to=[b[0], y, b[1]], n=max(2, round(ln / 0.32)), color=color, rise=0, tin=0.35)
        if t is not None:
            t += step


def room(w, look="plastico"):
    """Imposta il mondo per una stanza intera: ombre vere, piano lontano, luce da negozio nel look reale."""
    base = w.spec

    def spec():
        s = base(); s.update(shadows=True, far=120, exposure=1.15 if look == "reale" else 1.3)
        if look == "reale":
            s["light"] = "store"
        return s
    w.spec = spec
    return w


REALE_CSS = "<style>#host-%s { background:#16130f !important; } #host-%s .w3-wash { background:radial-gradient(1200px 700px at 50%% 40%%, #3a332a, rgba(22,19,15,0) 75%%) !important; } #host-%s .w3-grid { display:none; }</style>"
