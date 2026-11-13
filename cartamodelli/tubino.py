"""Tubino smanicato con scollo a barca e tagli princesse dal giromanica.

Uso:  python tubino.py <cartella>   (la cartella contiene misure.json)
Esce: cartamodello-A0.pdf (1:1), cartamodello-A4.pdf (da incollare),
      cartamodello.dxf (copisteria/plotter), anteprima.png, controlli.txt

Unità interne: centimetri, y verso l'alto, vita a y = 0, x dal centro.
Pezzi: davanti centrale (al piego), fianchetto davanti, dietro centrale
(zip al centro dietro), fianchetto dietro. Fodera = stessi pezzi, 2 cm più corti.
La pince del seno (davanti) e della scapola (dietro) è ruotata nella princesse
che parte dal giromanica.
"""
import json
import sys
from pathlib import Path

import ezdxf
import fitz  # PyMuPDF, solo per l'anteprima
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from scipy.interpolate import PchipInterpolator
from shapely.geometry import LineString, Polygon, box

PT = 72 / 2.54
SA = 1.0      # margine di cucitura
HEM = 3.0     # margine dell'orlo

DIR = Path(sys.argv[1])
M = json.loads((DIR / "misure.json").read_text(encoding="utf-8"))

# ---------------------------------------------------------------- vestibilità
# Tessuto consigliato: cotone satin stretch (2-3% elastan) -> agio contenuto.
C_BUST = M["seno"] + 3
C_WAIST = M["vita"] + 2
C_HIP = M["fianchi"] + 3
C_HEM = C_HIP - 2              # tubino: leggermente stretto in fondo


def split(c, k):               # (davanti, dietro) per mezza figura
    return c / 4 + k, c / 4 - k


F = {}; B = {}
F["mid"], B["mid"] = split(C_BUST, 1.0)
F["waist"], B["waist"] = split(C_WAIST, 0.5)
F["hip"], B["hip"] = split(C_HIP, -0.5)
F["hem"], B["hem"] = split(C_HEM, -0.5)
LOW = ("mid", "waist", "hip", "hem")

# ---------------------------------------------------------------- altezze
# Interpretazione delle lunghezze (l'unica coerente con giromanica e dietro):
# vita dietro = dalla nuca (7a vertebra); punto spalla-collo dietro 2 cm più su.
# Davanti: punto spalla-collo 1 cm sopra il dietro (volume del seno);
# lunghezza seno = dal punto spalla-collo al capezzolo (verticale ~ -0,5).
# "Lunghezza vita davanti" (36) risulta allora presa dal centro collo: è solo
# un controllo, non entra nel disegno.
YB_HPS = M["lunghezza_vita_dietro"] + 2                         # 40
YF_HPS = YB_HPS + 1                                             # 41
Y_APEX = YF_HPS - (M["lunghezza_seno"] - 0.5)                   # 17.5
Y_HIP = -M["altezza_fianchi"]                                   # -19
Y_HEM = Y_HIP - M["fianchi_orlo"]                               # -39
Y_LOW = {"mid": Y_APEX, "waist": 0.0, "hip": Y_HIP, "hem": Y_HEM}

NW_F = M["collo"] / 6 + 0.5               # mezza larghezza collo davanti
NW_B = NW_F + 0.3
BOAT = 4.0                                # lo scollo a barca si allarga di 4 cm sulla spalla
CUT_IN = 1.5                              # smanicato: spalla accorciata di 1,5 cm
F_NECK_DEPTH = NW_F + 1.5                 # centro davanti (sulle clavicole)
B_NECK_DEPTH = 3.0
DART_F, DART_B = 2.5, 1.2               # pince seno / scapola ruotate nel giromanica (cm sull'arco)

CF_BUST = M["larghezza_seno"] / 2 + 0.5   # la princesse passa 0,5 cm fuori dal capezzolo
CF = dict(mid=CF_BUST, waist=CF_BUST - 1.5, hip=CF_BUST + 1, hem=CF_BUST + 0.7)
CB_MID = M["spalle_dietro"] / 4 - 0.5
CB = dict(mid=CB_MID, waist=CB_MID - 1.5, hip=CB_MID + 2, hem=CB_MID + 1.7)
CBX = dict(mid=0, waist=0.6, hip=0.3, hem=0.3)  # leggera presa in vita al centro dietro


# ---------------------------------------------------------------- geometria
def cr(points, n=24):
    P = np.array(points, float)
    P = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-2])
    return np.array(out)


def bezier(p0, p1, p2, n=30):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0) + 2 * (1 - t) * t * np.array(p1) + t ** 2 * np.array(p2)


def length(a):
    return float(np.sum(np.hypot(*np.diff(a, axis=0).T)))


def at_arc(curve, s):
    """Punto e indice a distanza s lungo la curva."""
    cum = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(curve, axis=0).T))])
    x = np.interp(s, cum, curve[:, 0]); y = np.interp(s, cum, curve[:, 1])
    return np.array([x, y]), int(np.searchsorted(cum, s))


def edge(xs, ys, n=110):
    f = PchipInterpolator(list(ys)[::-1], list(xs)[::-1])
    yy = np.linspace(ys[0], ys[-1], n)
    return np.column_stack([f(yy), yy])


def x_at(e, y):
    return float(np.interp(y, e[::-1, 1], e[::-1, 0]))


class Piece:
    def __init__(self, name, lines, left, right, top, fold=False):
        self.name, self.lines, self.fold = name, lines, fold
        self.left, self.right, self.top = left, right, top
        self.stitch = np.vstack([top, right[1:], left[::-1][:-1]])
        # orlo: i bordi si allungano di (HEM - SA) prima di aggiungere il margine
        ext = HEM - SA
        r2 = np.vstack([right[1:], [right[-1][0], right[-1][1] - ext]])
        l2 = np.vstack([[left[-1][0], left[-1][1] - ext], left[::-1][1:-1]])
        poly = Polygon(np.vstack([top, r2, l2])).buffer(SA, join_style=2, mitre_limit=2.5)
        if fold:  # nessun margine sul piego
            poly = poly.intersection(box(0, -500, 500, 500))
        self.cut = np.array(poly.exterior.coords)
        self.notches = []

    def notch(self, side, y, double=False):
        e = self.left if side == "L" else self.right
        d = -1 if side == "L" else 1
        for yy in ([y, y - 0.7] if double else [y]):
            self.notches.append((x_at(e, yy), yy, d))

    def width_at(self, y):
        return Polygon(self.stitch).intersection(LineString([(-200, y), (200, y)])).length

    def bbox(self):
        return self.cut[:, 0].min(), self.cut[:, 1].min(), self.cut[:, 0].max(), self.cut[:, 1].max()


def shoulder(nw, y_hps, tip_x_block, drop):
    """Spalla: dal punto collo al punto spalla (già accorciato per lo smanicato)."""
    hps = np.array([nw, y_hps]); tip = np.array([tip_x_block, y_hps - drop])
    u = (tip - hps) / np.linalg.norm(tip - hps)
    return hps, hps + u * BOAT, tip - u * CUT_IN, np.linalg.norm(tip - hps)


def armhole(tip, across_x, side_x, y_ua):
    ya = y_ua + 0.45 * (tip[1] - y_ua)
    c = cr([tip, (across_x, ya), (side_x - 2.3, y_ua + 1.1), (side_x, y_ua)], 40)
    return c, ya


def build(y_ua):
    # --- dietro: spalla più lunga di 0,5 (si "mollega" sul davanti)
    b_hps, b_boat, b_tip, sl_b = shoulder(NW_B, YB_HPS, M["spalle_dietro"] / 2, 4.0)
    sl_f = sl_b - 0.5
    f_drop = 5.0
    f_hps, f_boat, f_tip, _ = shoulder(NW_F, YF_HPS, NW_F + np.sqrt(sl_f ** 2 - f_drop ** 2), f_drop)

    # --- davanti
    f_neck = bezier((0, YF_HPS - F_NECK_DEPTH), (f_boat[0] * 0.75, YF_HPS - F_NECK_DEPTH), f_boat)
    f_arm, _ = armhole(f_tip, M["spalle_davanti"] / 2 - 0.5, F["mid"], y_ua)
    s1 = length(f_arm[:np.argmin(np.abs(f_arm[:, 1] - (y_ua + 0.4 * (f_tip[1] - y_ua)))) + 1])
    a1, i1 = at_arc(f_arm, s1)
    a2, i2 = at_arc(f_arm, s1 + DART_F)

    cf_r = edge([a1[0]] + [CF[l] for l in LOW], [a1[1]] + [Y_LOW[l] for l in LOW])
    cf_top = np.vstack([f_neck, [f_tip], f_arm[1:i1], [a1]])
    cf = Piece("DAVANTI CENTRALE", ["tessuto: taglia 1 AL PIEGO", "fodera: taglia 1 al piego"],
               np.array([[0, YF_HPS - F_NECK_DEPTH], [0, Y_HEM]]), cf_r, cf_top, fold=True)

    sf_w = {l: F[l] - CF[l] for l in LOW}
    d = {l: 0.5 * (sf_w["mid"] - sf_w[l]) for l in LOW}

    def make_sf(dy):
        seg = np.vstack([[a2], f_arm[i2:]])
        t = np.linspace(0, 1, len(seg))[:, None]
        seg = seg + np.column_stack([np.zeros(len(seg)), dy * (1 - t[:, 0])])
        left = edge([seg[0][0]] + [CF_BUST + d[l] for l in LOW], [seg[0][1]] + [Y_LOW[l] for l in LOW])
        right = edge([F["mid"]] + [F["mid"] - d[l] for l in LOW], [y_ua] + [Y_LOW[l] for l in LOW])
        return Piece("FIANCHETTO DAVANTI", ["tessuto: taglia 2 (una coppia)", "fodera: taglia 2"],
                     left, right, seg)

    dy = 0.0
    for _ in range(10):
        sf = make_sf(dy)
        dy += length(cf.right) - length(sf.left)
    sf = make_sf(dy)

    # --- dietro
    b_neck = bezier((0, YB_HPS - B_NECK_DEPTH), (b_boat[0] * 0.75, YB_HPS - B_NECK_DEPTH), b_boat)
    b_arm, _ = armhole(b_tip, M["spalle_dietro"] / 2 - 1.5, B["mid"], y_ua)
    s1b = length(b_arm[:np.argmin(np.abs(b_arm[:, 1] - (y_ua + 0.45 * (b_tip[1] - y_ua)))) + 1])
    b1, j1 = at_arc(b_arm, s1b)
    b2, j2 = at_arc(b_arm, s1b + DART_B)
    cb_l = edge([0] + [CBX[l] for l in LOW], [YB_HPS - B_NECK_DEPTH] + [Y_LOW[l] for l in LOW])
    cb_r = edge([b1[0]] + [CBX[l] + CB[l] for l in LOW], [b1[1]] + [Y_LOW[l] for l in LOW])
    cb_top = np.vstack([b_neck, [b_tip], b_arm[1:j1], [b1]])
    cb = Piece("DIETRO CENTRALE", ["tessuto: taglia 2 (una coppia)", "fodera: taglia 2",
                                   "bordo sinistro = centro dietro, zip"], cb_l, cb_r, cb_top)

    sb_w = {l: B[l] - CB[l] for l in LOW}
    e = {l: 0.5 * (sb_w["mid"] - sb_w[l]) for l in LOW}

    def make_sb(dy):
        seg = np.vstack([[b2], b_arm[j2:]])
        t = np.linspace(0, 1, len(seg))
        seg = seg + np.column_stack([np.zeros(len(seg)), dy * (1 - t)])
        left = edge([seg[0][0]] + [CB_MID + e[l] for l in LOW], [seg[0][1]] + [Y_LOW[l] for l in LOW])
        right = edge([B["mid"]] + [B["mid"] - e[l] for l in LOW], [y_ua] + [Y_LOW[l] for l in LOW])
        return Piece("FIANCHETTO DIETRO", ["tessuto: taglia 2 (una coppia)", "fodera: taglia 2"],
                     left, right, seg)

    dyb = 0.0
    for _ in range(10):
        sb = make_sb(dyb)
        dyb += length(cb.right) - length(sb.left)
    sb = make_sb(dyb)

    info = dict(sl_f=np.linalg.norm(f_tip - f_boat), sl_b=np.linalg.norm(b_tip - b_boat),
                arm=length(f_arm[:i1]) + length(sf.top) + length(b_arm[:j1]) + length(sb.top),
                neck=2 * (length(f_neck) + length(b_neck)), y_ua=y_ua)
    return cf, sf, cb, sb, info


# giromanica del cartamodello = giromanica misurato + 1 (smanicato aderente):
# si cerca l'altezza del sottobraccio che lo dà, entro limiti ragionevoli.
# Il giromanica misurato (41) non è compatibile con le lunghezze: il
# sottobraccio finirebbe sotto il seno. Si usa la profondità standard
# (metà giromanica dal punto spalla-collo dietro) e il giromanica resta un controllo.
TARGET_ARM = M["giromanica"] + 1
Y_UA = YB_HPS - M["giromanica"] / 2
cf, sf, cb, sb, INFO = build(Y_UA)
PIECES = [cf, sf, cb, sb]
ZIP_END = Y_HIP - 2

cf.notch("R", Y_APEX); cf.notch("R", 0)
sf.notch("L", Y_APEX); sf.notch("L", 0); sf.notch("R", 0)
cb.notch("R", 0, double=True); cb.notch("L", ZIP_END)
sb.notch("L", 0, double=True); sb.notch("R", 0)

HEM_FINISHED = 2 * (cf.width_at(Y_HEM + 0.02) + sf.width_at(Y_HEM + 0.02)
                    + cb.width_at(Y_HEM + 0.02) + sb.width_at(Y_HEM + 0.02))
LACE_LEN = HEM_FINISHED + 2


# ---------------------------------------------------------------- controlli
def total(y):
    return 2 * (cf.width_at(y) + sf.width_at(y) + cb.width_at(y) + sb.width_at(y))


def report():
    t = ["CONTROLLI CARTAMODELLO — tubino smanicato\n",
         "Circonferenze sul cartamodello (linea di cucitura) vs obiettivo:"]
    t.append(f"  {'sottobraccio (petto alto)':26s} {total(Y_UA - 0.3):6.1f} cm   (info: petto alto + ~2)")
    for lab, y, goal in [("seno", Y_APEX, C_BUST), ("vita", 0, C_WAIST),
                         ("fianchi", Y_HIP + 0.02, C_HIP), ("orlo", Y_HEM + 0.02, C_HEM)]:
        t.append(f"  {lab:26s} {total(y):6.1f} cm   (obiettivo {goal:.1f})")
    t.append(f"  {'giromanica':26s} {INFO['arm']:6.1f} cm   (misurato {M['giromanica']}: da verificare in tela; "
             f"sottobraccio a {Y_UA:.1f} cm sopra la vita)")
    t.append(f"  {'scollo (giro intero)':26s} {INFO['neck']:6.1f} cm")
    t.append("\nCuciture che si uniscono (stessa lunghezza, tolleranza 0,3):")
    for lab, a, b, ease in [("princesse davanti", cf.right, sf.left, 0), ("princesse dietro", cb.right, sb.left, 0),
                            ("fianco", sf.right, sb.right, 0)]:
        la, lb = length(a), length(b)
        t.append(f"  {lab:18s} {la:5.1f} / {lb:5.1f}   diff {abs(la - lb):.2f} {'OK' if abs(la - lb) <= 0.3 else 'DA SISTEMARE'}")
    t.append(f"  {'spalla':18s} {INFO['sl_f']:5.1f} / {INFO['sl_b']:5.1f}   il dietro è 0,5 più lungo apposta: "
             "si mollega (arricciatura invisibile) sul davanti")
    t.append(f"\nLunghezza al centro davanti: {YF_HPS - F_NECK_DEPTH - Y_HEM:.0f} cm "
             f"(dallo scollo all'orlo, pizzo escluso)")
    t.append(f"Zip invisibile: {YB_HPS - B_NECK_DEPTH - ZIP_END:.0f} cm di apertura -> comprala da 55-60 cm")
    t.append(f"Pizzo per l'orlo: {LACE_LEN:.0f} cm (giro orlo + 2)")
    return "\n".join(t)


# ---------------------------------------------------------------- disegno
def draw_piece(c, p, ox, oy):
    def path(pts):
        pa = c.beginPath()
        pa.moveTo((pts[0][0] + ox) * PT, (pts[0][1] + oy) * PT)
        for x, y in pts[1:]:
            pa.lineTo((x + ox) * PT, (y + oy) * PT)
        pa.close()
        return pa
    c.setLineWidth(1.2); c.setDash(); c.drawPath(path(p.cut), stroke=1, fill=0)
    c.setLineWidth(0.5); c.setDash(4, 3); c.drawPath(path(p.stitch), stroke=1, fill=0)
    c.setDash(); c.setLineWidth(0.9)
    for x, y, dr in p.notches:
        c.line((x + ox) * PT, (y + oy) * PT, (x + dr * (SA + 0.15) + ox) * PT, (y + oy) * PT)
    c.setLineWidth(0.3); c.setDash(1, 2)
    for y in (0, Y_APEX, Y_HIP):
        w = LineString([(-200, y), (200, y)]).intersection(Polygon(p.stitch))
        if not w.is_empty:
            (x0, _), (x1, _) = w.coords[0], w.coords[-1]
            c.line((x0 + ox) * PT, (y + oy) * PT, (x1 + ox) * PT, (y + oy) * PT)
    c.setDash()
    if p.fold:
        c.setLineWidth(2.0)
        c.line(ox * PT, (YF_HPS - F_NECK_DEPTH - 1 + oy) * PT, ox * PT, (Y_HEM + oy) * PT)
        c.saveState(); c.translate((0.5 + ox) * PT, (Y_HIP - 10 + oy) * PT); c.rotate(90)
        c.setFont("Helvetica-Bold", 9); c.drawString(0, 0, "PIEGO — centro davanti"); c.restoreState()
    # drittofilo
    w = LineString([(-200, Y_HIP), (200, Y_HIP)]).intersection(Polygon(p.stitch))
    cx = (w.coords[0][0] + w.coords[-1][0]) / 2 + 3
    y0, y1 = Y_HEM + 4, Y_APEX + 2
    c.setLineWidth(0.8)
    c.line((cx + ox) * PT, (y0 + oy) * PT, (cx + ox) * PT, (y1 + oy) * PT)
    for yy, s in ((y1, -1), (y0, 1)):
        c.line((cx + ox) * PT, (yy + oy) * PT, (cx - 0.4 + ox) * PT, (yy + s + oy) * PT)
        c.line((cx + ox) * PT, (yy + oy) * PT, (cx + 0.4 + ox) * PT, (yy + s + oy) * PT)
    # etichette
    xl = x_at(p.left, Y_HIP - 3)
    tx = (xl + (2 if p.fold else 0.8) + ox) * PT
    ty = (Y_HIP - 3 + oy) * PT
    c.setFont("Helvetica-Bold", 9.5); c.drawString(tx, ty, p.name)
    c.setFont("Helvetica", 7)
    for i, s in enumerate(p.lines + ["margini 1 cm compresi", "orlo 3 cm compreso", "drittofilo = freccia"]):
        c.drawString(tx, ty - (i + 1) * 8.5, s)
    c.setFont("Helvetica", 6.5)
    for y, lab in ((0, "VITA"), (Y_HIP, "FIANCHI")):
        c.drawString((x_at(p.left, y) + (2 if p.fold else 0.5) + ox) * PT, (y + 0.25 + oy) * PT, lab)
    if p in (cf, sf):
        c.drawString((x_at(p.left, Y_APEX) + (2 if p.fold else 0.5) + ox) * PT, (Y_APEX + 0.25 + oy) * PT, "LIVELLO SENO")


def test_square(c, x, y):
    c.setLineWidth(1); c.rect(x * PT, y * PT, 10 * PT, 10 * PT)
    c.setFont("Helvetica-Bold", 9); c.drawString((x + 0.6) * PT, (y + 5.3) * PT, "QUADRATO DI PROVA")
    c.setFont("Helvetica", 8); c.drawString((x + 0.6) * PT, (y + 4.3) * PT, "deve misurare 10 x 10 cm")


A0W, A0H = 84.1, 118.9
TOP = A0H - 6


def layout(x0=3, gap=2.5):
    pos, x = [], x0
    for p in PIECES:
        bx0, by0, bx1, by1 = p.bbox()
        pos.append((p, x - bx0, TOP - by1))
        x += (bx1 - bx0) + gap
    return pos, x


def pieces_bottom():
    pos, _ = layout()
    return min(py + p.bbox()[1] for p, px, py in pos)


SQ_Y = None


def bodice_block(c):
    pos, _ = layout()
    for p, px, py in pos:
        draw_piece(c, p, px, py)
    test_square(c, 3, pieces_bottom() - 13)
    return pos


def a0_pdf(path):
    c = canvas.Canvas(str(path), pagesize=(A0W * PT, A0H * PT))
    c.setTitle("Tubino — cartamodello A0")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(3 * PT, (A0H - 2.8) * PT, "TUBINO SMANICATO, SCOLLO A BARCA, PRINCESSE — cartamodello in scala 1:1")
    c.setFont("Helvetica", 9)
    c.drawString(3 * PT, (A0H - 3.8) * PT, "Stampa al 100% (dimensioni effettive, NON 'adatta alla pagina'). "
                 "Prima di tagliare misura il quadrato di prova: deve fare 10 x 10 cm.")
    bodice_block(c)
    x, y = 16, pieces_bottom() - 2.5
    lines = [
        ("b", "MATERIALI (tessuto alto 140 cm)"),
        ("", "Tessuto: cotone satin stretch blu notte a pois, 1,2 m  ·  Fodera: bemberg (cupro) blu, 1,1 m"),
        ("", f"Pizzo festonato avorio alto 5-6 cm: {LACE_LEN / 100:.1f} m  ·  Zip invisibile 55-60 cm blu  ·  "
             "Nastro termoadesivo 1 cm: 2 m"),
        ("b", "ORDINE DI CUCITURA"),
        ("", "1. Nastro termoadesivo sul rovescio del tessuto lungo scollo e giromanica (non si sformano)."),
        ("", "2. Tessuto: cuci le princesse (tacca singola davanti, doppia dietro); tacchetta i margini curvi; stira aperto."),
        ("", "3. Cuci i fianchi (tacca in vita). NON cucire ancora le spalle e il centro dietro."),
        ("", "4. Fodera: stessi passaggi. Rifila la fodera di 2 cm in fondo (deve restare più corta del vestito)."),
        ("", "5. Dritto contro dritto tessuto + fodera: cuci scollo e giromanica, fermandoti a 2 cm dalle spalle."),
        ("", "   Rifila a 0,5 cm, tacca le curve, ribatti i margini sulla fodera (impuntura a 2 mm), rivolta."),
        ("", "6. Spalle: cuci quelle del tessuto (il dietro è 0,5 cm più lungo: mollegalo), poi chiudi la fodera a mano."),
        ("", "7. Zip invisibile al centro dietro sul tessuto (fino alla tacca sotto i fianchi), poi chiudi il centro"),
        ("", "   dietro sotto la zip. Fodera fermata a mano lungo la zip."),
        ("", "8. Orlo: risvolta 3 cm. Appoggia il pizzo sul rovescio dell'orlo in modo che sporga 3 cm, impuntura."),
        ("", "9. Orlo della fodera 1+1 cm a macchina. Fermapunti fodera-vestito alle cuciture dei fianchi, in vita."),
        ("b", "PROVA PRIMA IN TELA (solo davanti e dietro, fino ai fianchi). Foto davanti, fianco, dietro -> correzioni."),
    ]
    for i, (st, s) in enumerate(lines):
        c.setFont("Helvetica-Bold" if st else "Helvetica", 9)
        c.drawString(x * PT, (y - i * 0.85) * PT, s)
    c.setFont("Helvetica", 7)
    c.drawString(3 * PT, 1.5 * PT, "Linea continua = taglio · tratteggio = cucitura (margine 1 cm, orlo 3 cm) · trattini = tacche · "
                 "puntinato = seno, vita, fianchi · generato da cartamodelli/tubino.py")
    c.showPage(); c.save()


def a4_pdf(path):
    _, xend = layout()
    ymin = pieces_bottom() - 14
    x0, x1, y1 = 2, xend, A0H - 5
    pw, ph = 19.0, 27.7
    cols = int(np.ceil((x1 - x0) / pw)); rows = int(np.ceil((y1 - ymin) / ph))
    c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle("Tubino — cartamodello A4 da incollare")
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
    doc = ezdxf.new(units=4)
    msp = doc.modelspace()
    for lay, col in (("TAGLIO", 7), ("CUCITURA", 1), ("TACCHE", 3), ("TESTO", 5)):
        doc.layers.add(lay, color=col)
    pos, _ = layout()
    mm = lambda pts, ox, oy: [((x + ox) * 10, (y + oy) * 10) for x, y in pts]
    for p, ox, oy in pos:
        msp.add_lwpolyline(mm(p.cut, ox, oy), close=True, dxfattribs={"layer": "TAGLIO"})
        msp.add_lwpolyline(mm(p.stitch, ox, oy), close=True, dxfattribs={"layer": "CUCITURA"})
        for x, y, dr in p.notches:
            msp.add_line(*mm([(x, y), (x + dr * SA, y)], ox, oy), dxfattribs={"layer": "TACCHE"})
        msp.add_text(p.name, height=8, dxfattribs={"layer": "TESTO"}).set_placement(
            ((x_at(p.left, Y_HIP - 3) + 1 + ox) * 10, (Y_HIP - 3 + oy) * 10))
    doc.saveas(path)


if __name__ == "__main__":
    a0 = DIR / "cartamodello-A0.pdf"
    a0_pdf(a0)
    n = a4_pdf(DIR / "cartamodello-A4.pdf")
    dxf(DIR / "cartamodello.dxf")
    fitz.open(a0)[0].get_pixmap(dpi=40).save(DIR / "anteprima.png")
    rep = report() + f"\nFogli A4 da stampare: {n}\n"
    (DIR / "controlli.txt").write_text(rep, encoding="utf-8")
    print(rep)
