"""Vestito a fascia con gonna a palloncino — cartamodello parametrico.

Uso:  python palloncino.py <cartella>   (la cartella contiene misure.json)
Esce: cartamodello-A0.pdf (1:1), cartamodello-A4.pdf (da incollare),
      cartamodello.dxf (copisteria/plotter), anteprima.png, controlli.txt

Unità interne: centimetri, y verso l'alto, vita a y = 0.
Corpino: 4 tagli princesse (davanti centrale intero, fianchetto davanti,
dietro centrale con zip, fianchetto dietro), dal bordo superiore ai fianchi.
Gonna: rettangoli (esterna arricciata sopra e sotto + fodera interna + tulle).
"""
import json
import sys
from pathlib import Path

import ezdxf
import fitz  # PyMuPDF, solo per l'anteprima
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from shapely.geometry import LineString, Polygon

PT = 72 / 2.54  # punti per cm
SA = 1.0        # margine di cucitura (cm)

# ---------------------------------------------------------------- misure
DIR = Path(sys.argv[1])
M = json.loads((DIR / "misure.json").read_text(encoding="utf-8"))

# Vestibilità (cm sulla circonferenza intera). Corpino a fascia: deve
# "aggrapparsi" sopra il seno, quindi agio negativo sul bordo superiore.
C_TOP = M["stima_circonferenza_bordo_superiore"] - 1
C_BUST = M["seno"] + 1
C_WAIST = M["vita"] + 1
C_HIP = M["fianchi"] + 3

# Ripartizione davanti/dietro per mezza figura (davanti più ampio al seno,
# dietro più ampio ai fianchi).
def split(c, k):
    return c / 4 + k, c / 4 - k

F_TOP, B_TOP = split(C_TOP, 0.5)
F_BUST, B_BUST = split(C_BUST, 1.0)
F_WAIST, B_WAIST = split(C_WAIST, 0.5)
F_HIP, B_HIP = split(C_HIP, -0.5)

# Altezze (sopra la vita = positivo)
Y_APEX = M["lunghezza_vita_davanti"] - M["lunghezza_seno"]          # 12
Y_HIP = -M["stima_altezza_fianchi"]                                  # -20
Y_UNDERARM = M["lunghezza_vita_dietro"] - (M["giromanica"] / 2 - 2)  # 19.5
Y_SIDE_TOP = Y_UNDERARM - 3.5        # 2.5 sotto l'ascella + 1 per lo smanicato
Y_CF_TOP = Y_APEX + 6                # centro davanti: 6 cm sopra il capezzolo
Y_FP_TOP = Y_APEX + 7                # sulla princesse il seno chiede +1 cm
Y_CB_TOP = Y_SIDE_TOP - 1
Y_BP_TOP = Y_SIDE_TOP - 0.5
Y_MID = Y_APEX                       # livello seno (usato anche dietro)

# Larghezze dei pannelli centrali (mezzo pannello per il davanti)
CF_BUST = M["larghezza_seno"] / 2 + 1   # la princesse passa 1 cm fuori dal capezzolo
CF = dict(top=CF_BUST - 1, mid=CF_BUST, waist=CF_BUST - 2, hip=CF_BUST + 1)
CB_MID = M["spalle_dietro"] / 4 - 0.5
CB = dict(top=CB_MID - 0.5, mid=CB_MID, waist=CB_MID - 1.5, hip=CB_MID + 2.5)
SF = dict(top=F_TOP - CF["top"], mid=F_BUST - CF["mid"],
          waist=F_WAIST - CF["waist"], hip=F_HIP - CF["hip"])
SB = dict(top=B_TOP - CB["top"], mid=B_BUST - CB["mid"],
          waist=B_WAIST - CB["waist"], hip=B_HIP - CB["hip"])
LEVELS = ("top", "mid", "waist", "hip")


# ---------------------------------------------------------------- geometria
def cr(points, n=24):
    """Curva Catmull-Rom che passa per tutti i punti."""
    P = np.array(points, float)
    P = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t
                              + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-2])
    return np.array(out)


def length(a):
    return float(np.sum(np.hypot(*np.diff(a, axis=0).T)))


def x_at(edge, y):
    """x del bordo all'altezza y (bordo ordinato dall'alto verso il basso)."""
    return float(np.interp(y, edge[::-1, 1], edge[::-1, 0]))


class Piece:
    def __init__(self, name, lines, left, right, top_mid=None):
        self.name, self.lines = name, lines
        self.left, self.right = left, right  # bordi dall'alto verso il basso
        tops = [left[0], right[0]] if top_mid is None else [left[0], top_mid, right[0]]
        self.top = cr(tops, 16) if top_mid is not None else np.array(tops)
        self.stitch = np.vstack([self.top, right[1:], left[::-1][:-1]])
        poly = Polygon(self.stitch)
        self.cut = np.array(poly.buffer(SA, join_style=2, mitre_limit=2.5).exterior.coords)
        self.notches = []  # (x, y, direzione, doppia)

    def notch(self, side, y, double=False):
        edge = self.left if side == "L" else self.right
        d = -1 if side == "L" else 1
        for yy in ([y, y - 0.7] if double else [y]):
            self.notches.append((x_at(edge, yy), yy, d))

    def width_at(self, y):
        return Polygon(self.stitch).intersection(LineString([(-200, y), (200, y)])).length

    def bbox(self):
        return self.cut[:, 0].min(), self.cut[:, 1].min(), self.cut[:, 0].max(), self.cut[:, 1].max()


def edge(xs, ys, n=90):
    """Bordo verticale x(y): interpolazione monotona (PCHIP), non sborda oltre i punti."""
    from scipy.interpolate import PchipInterpolator
    f = PchipInterpolator(list(ys)[::-1], list(xs)[::-1])
    yy = np.linspace(ys[0], ys[-1], n)
    return np.column_stack([f(yy), yy])


def side_panel(s, top_left_y, top_right_y):
    """Fianchetto: fianco verticale nella parte alta (segue le costole);
    tutto il restringimento del bordo superiore va sulla princesse (seno)."""
    d = {l: 0.5 * (s[l] - s["waist"]) for l in LEVELS}
    rx = {l: s[l] - d[l] for l in LEVELS}
    rx["top"] = rx["mid"]
    lx = {l: -d[l] for l in LEVELS}
    lx["top"] = rx["top"] - s["top"]
    return edge([lx[l] for l in LEVELS], ys_f(top_left_y)), edge([rx[l] for l in LEVELS], ys_f(top_right_y))


ys_f = lambda top: [top, Y_MID, 0, Y_HIP]

# Davanti centrale: pezzo intero (niente piego: si taglia 1 aperto)
r = edge([CF[l] for l in LEVELS], ys_f(Y_FP_TOP))
l_ = r.copy(); l_[:, 0] *= -1
cf = Piece("DAVANTI CENTRALE", ["tessuto: taglia 1", "fodera: taglia 1", "centro davanti al centro del pezzo"],
           l_, r, top_mid=(0, Y_CF_TOP))

# Fianchetto davanti: bordo sinistro = princesse, destro = fianco.
# Il bordo superiore è inclinato (scende verso il fianco), quindi è più lungo
# della sua larghezza: si corregge stringendolo finché il bordo superiore
# totale torna all'obiettivo, e si regola la princesse finché le due
# cuciture hanno la stessa lunghezza.
def build_sf(w_adj, dy):
    s = dict(SF, top=SF["top"] + w_adj)
    return Piece("FIANCHETTO DAVANTI", ["tessuto: taglia 2 (una coppia)", "fodera: taglia 2"],
                 *side_panel(s, Y_FP_TOP + dy, Y_SIDE_TOP))


def top_total(sf_):
    return length(cf.top) + 2 * (length(sf_.top) + length(cb.top) + length(sb.top))

# Dietro centrale: bordo sinistro = centro dietro (zip), leggera presa in vita
cbx = dict(top=0, mid=0, waist=0.6, hip=0.3)
cb = Piece("DIETRO CENTRALE", ["tessuto: taglia 2 (una coppia)", "fodera: taglia 2", "bordo sinistro = centro dietro, zip"],
           edge([cbx[l] for l in LEVELS], ys_f(Y_CB_TOP)),
           edge([cbx[l] + CB[l] for l in LEVELS], ys_f(Y_BP_TOP)))

# Fianchetto dietro
sb = Piece("FIANCHETTO DIETRO", ["tessuto: taglia 2 (una coppia)", "fodera: taglia 2"],
           *side_panel(SB, Y_BP_TOP, Y_SIDE_TOP))

w_adj, dy = 0.0, 0.0
for _ in range(8):
    sf = build_sf(w_adj, dy)
    w_adj -= (top_total(sf) - C_TOP) / 2
    dy += length(cf.right) - length(sf.left)
sf = build_sf(w_adj, dy)

# Tacche: 1 = princesse davanti (seno + vita), 2 = princesse dietro, fianco = 1 in vita
cf.notch("L", Y_MID); cf.notch("R", Y_MID); cf.notch("L", 0); cf.notch("R", 0)
sf.notch("L", Y_MID); sf.notch("L", 0); sf.notch("R", 0)
cb.notch("R", 0, double=True)
sb.notch("L", 0, double=True); sb.notch("R", 0)
PIECES = [cf, sf, cb, sb]

# ---------------------------------------------------------------- gonna
L_SKIRT = M["stima_lunghezza_gonna_finita"]
OUT_W = round(C_HIP * 2.2)          # gonna esterna: 2,2 volte i fianchi
OUT_L = L_SKIRT + 12                # +12 cm di "sbuffo"
IN_W = 120 if C_HIP < 105 else round(C_HIP + 25)  # fodera: serve per camminare
IN_L = L_SKIRT - 2
TULLE_W = round(C_HIP * 2)
TULLE_L = L_SKIRT - 4
SKIRT = [
    ("Gonna esterna — davanti", "taffetà", 1, OUT_W / 2 + 2 * SA, OUT_L + 2 * SA),
    ("Gonna esterna — dietro", "taffetà", 2, OUT_W / 4 + SA + 1.5, OUT_L + 2 * SA),
    ("Gonna interna — davanti", "fodera", 1, IN_W / 2 + 2 * SA, IN_L + 2 * SA),
    ("Gonna interna — dietro", "fodera", 2, IN_W / 4 + SA + 1.5, IN_L + 2 * SA),
    ("Strato di tulle", "tulle rigido", 1, TULLE_W, TULLE_L + SA),
]

# ---------------------------------------------------------------- controlli
def report():
    t = []
    t.append("CONTROLLI CARTAMODELLO — vestito a palloncino\n")
    t.append("Circonferenze sul cartamodello (linea di cucitura) vs obiettivo:")
    for lab, y, goal in [("seno", Y_MID, C_BUST),
                         ("vita", 0, C_WAIST), ("fianchi", Y_HIP + 0.02, C_HIP)]:
        tot = cf.width_at(y) + 2 * (sf.width_at(y) + cb.width_at(y) + sb.width_at(y))
        t.append(f"  {lab:22s} {tot:6.1f} cm" + (f"   (obiettivo {goal:.1f})" if goal else ""))
    top_len = length(cf.top) + 2 * (length(sf.top) + length(cb.top) + length(sb.top))
    t.append(f"  bordo superiore (lunghezza vera) {top_len:6.1f} cm   (obiettivo {C_TOP:.1f})")
    t.append("\nCuciture che si uniscono (devono avere la stessa lunghezza, tolleranza 0,3):")
    for lab, a, b in [("princesse davanti", cf.right, sf.left), ("princesse dietro", cb.right, sb.left),
                      ("fianco", sf.right, sb.right)]:
        la, lb = length(a), length(b)
        t.append(f"  {lab:18s} {la:5.1f} / {lb:5.1f}   diff {abs(la - lb):.2f} {'OK' if abs(la - lb) <= 0.3 else 'DA SISTEMARE'}")
    t.append(f"\nLunghezza totale al centro davanti: {Y_CF_TOP - Y_HIP + L_SKIRT:.0f} cm "
             f"(corpino {Y_CF_TOP - Y_HIP:.0f} + gonna {L_SKIRT})")
    t.append(f"Zip invisibile: {Y_CB_TOP - Y_HIP + 5:.0f} cm circa (centro dietro + 5 cm nella gonna) -> comprala da 40")
    return "\n".join(t)


# ---------------------------------------------------------------- disegno
def draw_piece(c, p, ox, oy):
    def path(pts, close=True):
        pa = c.beginPath()
        pa.moveTo((pts[0][0] + ox) * PT, (pts[0][1] + oy) * PT)
        for x, y in pts[1:]:
            pa.lineTo((x + ox) * PT, (y + oy) * PT)
        if close:
            pa.close()
        return pa
    c.setLineWidth(1.2); c.setDash(); c.drawPath(path(p.cut), stroke=1, fill=0)
    c.setLineWidth(0.5); c.setDash(4, 3); c.drawPath(path(p.stitch), stroke=1, fill=0)
    c.setDash()
    c.setLineWidth(0.9)
    for x, y, dr in p.notches:
        c.line((x + ox) * PT, (y + oy) * PT, (x + dr * (SA + 0.15) + ox) * PT, (y + oy) * PT)
    # vita e livello seno (riferimento)
    c.setLineWidth(0.3); c.setDash(1, 2)
    for y in (0, Y_MID):
        w = LineString([(-200, y), (200, y)]).intersection(Polygon(p.stitch))
        if not w.is_empty:
            (x0, _), (x1, _) = w.coords[0], w.coords[-1]
            c.line((x0 + ox) * PT, (y + oy) * PT, (x1 + ox) * PT, (y + oy) * PT)
    c.setDash()
    # drittofilo
    cx = p.stitch[:, 0].max() - 3.5  # freccia a destra, etichetta a sinistra
    y0, y1 = Y_HIP + 4, Y_MID + 2
    c.setLineWidth(0.8)
    c.line((cx + ox) * PT, (y0 + oy) * PT, (cx + ox) * PT, (y1 + oy) * PT)
    for yy, s in ((y1, -1), (y0, 1)):
        c.line((cx + ox) * PT, (yy + oy) * PT, (cx - 0.4 + ox) * PT, (yy + s * 1 + oy) * PT)
        c.line((cx + ox) * PT, (yy + oy) * PT, (cx + 0.4 + ox) * PT, (yy + s * 1 + oy) * PT)
    # etichette
    tx = (p.stitch[:, 0].min() + 1 + ox) * PT
    ty = (-4 + oy) * PT
    c.setFont("Helvetica-Bold", 10); c.drawString(tx, ty, p.name)
    c.setFont("Helvetica", 7.5)
    for i, s in enumerate(p.lines + ["margine 1 cm compreso", "drittofilo = freccia"]):
        c.drawString(tx, ty - (i + 1) * 9.5, s)
    c.setFont("Helvetica", 6.5)
    c.drawString(tx, (0.25 + oy) * PT, "VITA")
    if p in (cf, sf):
        c.drawString(tx, (Y_MID + 0.25 + oy) * PT, "LIVELLO SENO")


def test_square(c, x, y):
    c.setLineWidth(1); c.rect(x * PT, y * PT, 10 * PT, 10 * PT)
    c.setFont("Helvetica-Bold", 9); c.drawString((x + 0.6) * PT, (y + 5.3) * PT, "QUADRATO DI PROVA")
    c.setFont("Helvetica", 8); c.drawString((x + 0.6) * PT, (y + 4.3) * PT, "deve misurare 10 x 10 cm")


# posizione dei pezzi sul foglio (cm, origine in basso a sinistra)
def layout(x0, ytop, gap=3.0):
    pos, x = [], x0
    for p in PIECES:
        bx0, by0, bx1, by1 = p.bbox()
        pos.append((p, x - bx0, ytop - by1))
        x += (bx1 - bx0) + gap
    return pos, x


A0W, A0H = 84.1, 118.9


def bodice_block(c, ox=0, oy=0):
    """Tutto ciò che è in scala 1:1 (pezzi + quadrato), in coordinate foglio A0."""
    pos, _ = layout(3 + ox, A0H - 6 + oy)
    for p, px, py in pos:
        draw_piece(c, p, px, py)
    test_square(c, 3 + ox, A0H - 6 - 48 - 12 + oy)
    return pos


def a0_pdf(path):
    c = canvas.Canvas(str(path), pagesize=(A0W * PT, A0H * PT))
    c.setTitle("Vestito a palloncino — cartamodello A0")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(3 * PT, (A0H - 2.8) * PT, "VESTITO A FASCIA CON GONNA A PALLONCINO — cartamodello in scala 1:1")
    c.setFont("Helvetica", 9)
    c.drawString(3 * PT, (A0H - 3.8) * PT, "Stampa al 100% (dimensioni effettive, NON 'adatta alla pagina'). "
                 "Prima di tagliare misura il quadrato di prova: deve fare 10 x 10 cm.")
    bodice_block(c)
    # gonna e istruzioni in scala ridotta / testo
    x, y = 17, A0H - 6 - 48 - 2
    c.setFont("Helvetica-Bold", 12); c.drawString(x * PT, y * PT, "GONNA — rettangoli da tracciare direttamente sul tessuto (misure con margini)")
    c.setFont("Helvetica", 9)
    for i, (n, fab, q, w, h) in enumerate(SKIRT):
        c.drawString(x * PT, (y - 1.4 - i * 0.9) * PT, f"{n:28s}  {fab:13s}  taglia {q}   {w:.1f} x {h:.1f} cm  (larghezza x altezza, altezza in drittofilo)")
    # schemino 1:10
    sx, sy = x, y - 7.5
    c.setFont("Helvetica", 7)
    for n, fab, q, w, h in SKIRT:
        c.rect(sx * PT, (sy - h / 10) * PT, w / 10 * PT, h / 10 * PT)
        c.drawString(sx * PT, (sy - h / 10 - 0.6) * PT, n.split("—")[-1].strip() + f" x{q}")
        sx += w / 10 + 2.5
    c.drawString(x * PT, (sy + 0.4) * PT, "schema in scala 1:10")
    # istruzioni
    steps = [
        "ORDINE DI CUCITURA",
        "1. Teletta termoadesiva leggera sul rovescio di tutti i pezzi del corpino in tessuto.",
        "2. Corpino esterno: cuci le princesse (tacca singola davanti, doppia dietro), poi i fianchi. Stira aperto.",
        "3. Fodera corpino: stessi passaggi. Sui margini di princesse, fianchi e centro davanti della fodera cuci il rigilene 8 mm",
        "   (da 1,5 cm sotto il bordo superiore a 2 cm sopra il fondo; punte arrotondate e rivestite).",
        "4. Bordo superiore: dritto contro dritto tessuto + fodera, cuci, rifila, ribatti la fodera (impuntura sotto) e rivolta.",
        "5. Gonna interna (fodera) e gonna esterna: cuci fianchi e centro dietro lasciando aperti gli ultimi 6 cm in alto.",
        "6. Arriccia il fondo della gonna esterna fino alla larghezza del fondo della gonna interna; cucili rovescio contro rovescio.",
        "7. Rivolta: ora la gonna esterna fa il 'palloncino'. Imbastisci insieme le due gonne in alto, con il tulle in mezzo.",
        "8. Arriccia la cima delle gonne fino al fondo del corpino (fianchi). Cuci al solo tessuto esterno, tacche ai fianchi.",
        "9. Zip invisibile da 40 cm al centro dietro (scende ~5 cm nella gonna). Chiudi la fodera a mano sopra la cucitura.",
        "10. Nastro gros-grain in vita all'interno, fermato alle cuciture, con gancetto. Attacchi per le spalline (opzionali).",
        "PROVA SEMPRE PRIMA IN TELA: il corpino senza spalline deve aderire. Foto davanti, fianco, dietro -> correzioni.",
    ]
    yy = y - 17
    for i, s in enumerate(steps):
        c.setFont("Helvetica-Bold" if i in (0, len(steps) - 1) else "Helvetica", 9)
        c.drawString(x * PT, (yy - i * 0.85) * PT, s)
    c.setFont("Helvetica", 7)
    c.drawString(3 * PT, 2 * PT, "Linea continua = taglio · tratteggio = cucitura (margine 1 cm) · trattini sul bordo = tacche · "
                 "puntinato = vita e livello seno · generato da cartamodelli/palloncino.py")
    c.showPage(); c.save()


def a4_pdf(path):
    """Solo la parte in scala 1:1, divisa in fogli A4 con sovrapposizione 0 e segni di allineamento."""
    pos, xend = layout(3, A0H - 6)
    ymin = min(py + p.bbox()[1] for p, px, py in pos) - 1
    ymin = min(ymin, A0H - 6 - 48 - 12 - 1)
    x0, x1, y1 = 2, xend, A0H - 5
    pw, ph = 19.0, 27.7   # area utile A4 con 1 cm di margine
    cols = int(np.ceil((x1 - x0) / pw)); rows = int(np.ceil((y1 - ymin) / ph))
    c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle("Vestito a palloncino — cartamodello A4 da incollare")
    for r_ in range(rows):
        for k in range(cols):
            wx0 = x0 + k * pw; wy1 = y1 - r_ * ph
            c.saveState()
            pa = c.beginPath(); pa.rect(1 * PT, 1 * PT, pw * PT, ph * PT)
            c.clipPath(pa, stroke=0, fill=0)
            c.translate((1 - wx0) * PT, (1 + ph - wy1) * PT)
            bodice_block(c)
            c.restoreState()
            c.setLineWidth(0.3); c.setDash(2, 2)
            c.rect(1 * PT, 1 * PT, pw * PT, ph * PT); c.setDash()
            c.setFont("Helvetica-Bold", 9)
            c.drawString(1.2 * PT, 0.4 * PT, f"riga {r_ + 1} / colonna {k + 1}   (fogli: {rows} righe x {cols} colonne) — "
                         "rifila sul tratteggio e affianca")
            c.showPage()
    c.save()
    return rows * cols


def dxf(path):
    doc = ezdxf.new(units=4)  # mm
    msp = doc.modelspace()
    for lay, col in (("TAGLIO", 7), ("CUCITURA", 1), ("TACCHE", 3), ("TESTO", 5)):
        doc.layers.add(lay, color=col)
    pos, _ = layout(3, A0H - 6)
    mm = lambda pts, ox, oy: [((x + ox) * 10, (y + oy) * 10) for x, y in pts]
    for p, ox, oy in pos:
        msp.add_lwpolyline(mm(p.cut, ox, oy), close=True, dxfattribs={"layer": "TAGLIO"})
        msp.add_lwpolyline(mm(p.stitch, ox, oy), close=True, dxfattribs={"layer": "CUCITURA"})
        for x, y, dr in p.notches:
            msp.add_line(*mm([(x, y), (x + dr * SA, y)], ox, oy), dxfattribs={"layer": "TACCHE"})
        msp.add_text(p.name, height=8, dxfattribs={"layer": "TESTO"}).set_placement(
            ((p.stitch[:, 0].min() + 1 + ox) * 10, (-4 + oy) * 10))
    doc.saveas(path)


if __name__ == "__main__":
    a0 = DIR / "cartamodello-A0.pdf"
    a0_pdf(a0)
    n = a4_pdf(DIR / "cartamodello-A4.pdf")
    dxf(DIR / "cartamodello.dxf")
    pg = fitz.open(a0)[0]
    pg.get_pixmap(dpi=40).save(DIR / "anteprima.png")
    rep = report() + f"\nFogli A4 da stampare: {n}\n"
    (DIR / "controlli.txt").write_text(rep, encoding="utf-8")
    print(rep)
