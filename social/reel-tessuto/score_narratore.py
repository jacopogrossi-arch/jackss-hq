"""[VARIANTE NARRATORE 24/11/2026: bocca ferma, vedi LIPS] Partitura del Reel «Il tessuto non torna indietro» (23/11/2026). Letta da social/gemello/reel.py (--score).
Tutti i tempi in secondi dall'inizio del Reel (voce montata: videos/_bench/reel-tessuto/vo/vo.wav, 16 s).
Stato: P3 (8.2-11.0 s, «Poi prendi il metro, e misuri due volte») con labiale scritto A MANO sull'inviluppo in dB; P1, P2, P4 = bozza automatica
(lips_auto.json) da rifinire a mano dopo la clip di prova. Gesti e camera: prima stesura, tarati solo sulla finestra di prova.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 16.0
VO = "D:/ClaudeCodeTest/videos/_bench/reel-tessuto/vo/vo.wav"

# ------------------------------------------------------------------ labiale
# Mappa: a=D e=C i=B o=E u=F; m b p = A (chiusura piena); f v = G; l = H; t d n s r k = B; X = riposo. Tempi = suono reale (reel.py anticipa di LEAD).
LIPS_AUTO = [tuple(x) for x in json.load(open(os.path.join(HERE, "lips_auto.json")))]
LIPS_P3 = [  # a mano, 23/11: dall'inviluppo in dB; chiusure: p(Poi) 8.18, p(prendi) 8.57, m(metro) 9.03, m(misuri) 9.99; v(volte) 10.50; t(volte) 10.70-10.80
    (8.18, "A"), (8.26, "E"), (8.42, "B"), (8.53, "X"), (8.57, "A"), (8.65, "B"), (8.68, "C"), (8.79, "B"), (8.95, "B"), (9.00, "H"), (9.03, "A"), (9.07, "C"),
    (9.23, "B"), (9.29, "E"), (9.46, "X"), (9.77, "C"), (9.99, "A"), (10.04, "B"), (10.15, "B"), (10.19, "F"), (10.28, "B"), (10.39, "F"), (10.46, "C"),
    (10.50, "G"), (10.55, "E"), (10.63, "H"), (10.70, "B"), (10.81, "C"), (10.97, "X")]
LIPS = [(0.0, "X")]   # NARRATORE (24/11): Jacopino non parla, la voce e' fuori campo; bocca sempre a riposo, resta il sorriso/ghigno (SMILE, SMIRK)

# sillabe accentate (nod della testa + sopracciglia): TES-su-to, ta-GLIA-to, TOR-na, in-DIE-tro | PAR-ti, CAR-ta, di-SE-gni, CA-po, SCA-la, SBA-gli, lì | POI, PREN-di, ME-tro, mi-SU-ri, DUE, VOL-te | SBA-glia-re, CAR-ta, CO-sta, ZE-ro, TES-su-to, NO
STRESS = [0.18, 0.80, 1.50, 2.05, 3.40, 4.10, 5.15, 5.62, 6.25, 7.15, 7.55, 8.27, 8.68, 9.07, 10.17, 10.40, 10.55, 11.55, 12.20, 12.65, 13.20, 14.25, 15.20]

# ------------------------------------------------------------------ camera: una camera per inquadratura (taglio netto)
SHOTS = [
    dict(name="s1_gancio", t0=0.00, t1=2.80, P0=(0.0, -0.60, 0.165), P1=(0.008, -0.54, 0.165), L0=(0.0, 0.13, 0.095), L1=(0.0, 0.13, 0.105), fstop=3.5, mw0=1.22, mw1=1.18, FOC0=(0, 0.11, 0.19), FOC1=(0, 0.11, 0.19)),
    dict(name="s2_medio", t0=2.80, t1=5.20, lens=65, P0=(0.0, -0.37, 0.16), P1=(0.01, -0.31, 0.165), L0=(0.0, 0.13, 0.12), L1=(0.0, 0.13, 0.125), fstop=3.5, mw0=1.12, mw1=1.05, FOC0=(0, 0.11, 0.19), FOC1=(0, 0.11, 0.19)),
    dict(name="s3_carta", macro=True, t0=5.20, t1=6.60, lens=50, P0=(0.02, -0.225, 0.21), P1=(0.02, -0.207, 0.17), L0=(0.02, -0.165, 0.003), L1=(0.02, -0.165, 0.003), fstop=6.3, mw0=1.0, mw1=1.0, FOC0=(0.02, -0.165, 0.003), FOC1=(0.02, -0.165, 0.003)),  # narratore: il disegno si deve leggere (vista alta sul foglio)
    dict(name="s4_medio", t0=6.60, t1=8.95, lens=65, P0=(0.0, -0.36, 0.165), P1=(0.006, -0.33, 0.167), L0=(0.0, 0.13, 0.135), L1=(0.0, 0.13, 0.14), fstop=3.5, mw0=1.08, mw1=1.04, FOC0=(0, 0.11, 0.19), FOC1=(0, 0.11, 0.19)),
    dict(name="s5_metro", t0=8.95, t1=9.60, lens=85, P0=(-0.02, -0.545, 0.150), P1=(-0.02, -0.525, 0.150), L0=(-0.02, 0.12, 0.140), L1=(-0.02, 0.12, 0.140), fstop=5.0, mw0=1.0, mw1=1.0, FOC0=(-0.012, 0.11, 0.185), FOC1=(-0.012, 0.11, 0.185)),  # narratore: viso + mano che indica insieme
    dict(name="s6_medio_stretto", t0=9.60, t1=11.40, lens=50, P0=(-0.01, -0.215, 0.150), P1=(-0.01, -0.195, 0.150), L0=(-0.015, 0.13, 0.140), L1=(-0.015, 0.13, 0.140), fstop=3.5, mw0=1.0, mw1=1.0, FOC0=(0, 0.11, 0.19), FOC1=(0, 0.11, 0.19)),
    dict(name="s7_battuta", t0=11.40, t1=16.04, lens=65, P0=(0.0, -0.34, 0.158), P1=(0.0, -0.27, 0.160), L0=(0.0, 0.13, 0.140), L1=(0.0, 0.13, 0.142), fstop=4.5, mw0=1.0, mw1=1.0, FOC0=(0, 0.11, 0.19), FOC1=(0, 0.11, 0.19)),
]

# ------------------------------------------------------------------ performance (secondi -> valore a gradino, la molla smorzata li insegue)
REST_R = (-0.113, 0.047, 0.344); REST_L = (0.126, -0.001, 0.339)
ANTIC_L = (0.135, -0.01, 0.37); POINT_L = (0.20, 0.15, 0.43); TAP_L = (0.20, 0.155, 0.405)
ANTIC_R = (-0.135, -0.01, 0.37); POINT_R = (-0.20, 0.15, 0.43); TAP_R = (-0.20, 0.155, 0.405)   # specchio della sinistra: il metro e' a sinistra sullo schermo = mano destra
OPEN_R = (-0.15, 0.17, 0.47); OPEN_L = (0.15, 0.17, 0.47)
FL, TW = -35, 80

IKL_POS = [(0, REST_L), (3.70, ANTIC_L), (4.05, POINT_L), (5.35, TAP_L), (5.48, POINT_L), (6.30, TAP_L), (6.43, POINT_L), (7.75, REST_L), (12.45, (0.12, 0.03, 0.38)), (12.70, OPEN_L), (13.15, (0.17, 0.18, 0.485)), (15.9, OPEN_L)]
IKL_INF = [(0, 0.0), (3.60, 1.0), (7.85, 0.0)]   # 24/11: sul finale il braccio sinistro resta a riposo (alzato gonfiava la manica)
IKR_POS = [(0, REST_R), (8.75, ANTIC_R), (9.00, POINT_R), (10.34, TAP_R), (10.45, POINT_R), (10.55, TAP_R), (10.66, POINT_R), (11.0, REST_R), (12.45, (-0.12, 0.03, 0.38)), (12.70, OPEN_R), (13.15, (-0.17, 0.18, 0.485)), (15.9, OPEN_R)]
IKR_INF = [(0, 0.0), (8.60, 1.0), (11.0, 0.0), (12.40, 1.0)]
HANDL = [(0, (0, 0, 0)), (3.80, (FL, 0, 0)), (7.85, (0, 0, 0))]
HANDR = [(0, (0, 0, 0)), (8.80, (FL, 0, 0)), (11.0, (0, 0, 0)), (12.55, (10, TW, 0))]
FING_L_IDX = [(0, 0.3), (3.80, 0.05), (7.85, 0.3)]
FING_L_OTH = [(0, 0.3), (3.78, 1.0), (7.85, 0.3)]
FING_R_IDX = [(0, 0.3), (8.80, 0.05), (11.0, 0.3), (12.5, 0.1)]
FING_R_OTH = [(0, 0.3), (8.78, 1.0), (11.0, 0.3), (12.5, 0.12)]
HEAD = [(0, (0, 0, 0)), (0.15, (-3, 0, 4)), (0.60, (-2, 0, 6)), (1.10, (4, 0, 2)), (1.50, (8, 0, 0)), (2.10, (10, 0, -2)), (2.50, (2, 0, 0)),
        (2.90, (-2, 2, 0)), (3.90, (8, 6, 0)), (4.90, (3, 3, -2)), (5.60, (9, 7, 0)), (6.50, (12, 7, 0)), (7.20, (2, 0, -4)), (7.80, (0, 0, 0)),
        (8.20, (-2, 0, 0)), (8.60, (6, -3, 0)), (9.00, (14, -7, 0)), (9.50, (10, -5, 0)), (9.80, (-2, 0, -2)), (10.30, (-3, 0, -4)), (10.70, (-4, 0, -5)), (11.20, (0, 0, 0)),
        (11.50, (-2, 0, 0)), (12.10, (8, 3, 0)), (12.65, (-3, 0, -3)), (13.20, (-4, -2, -7)), (13.90, (-2, 0, -6)), (14.30, (1, 5, -3)), (14.55, (1, -5, -3)), (14.80, (2, 4, -4)), (15.10, (0, -3, -5)), (15.9, (-2, -2, -4))]
SPINE = [(0, (0, 0, 0)), (2.8, (-1, 0, 0)), (3.9, (4, 4, 0)), (7.7, (0, 0, 0)), (8.9, (4, -5, 0)), (9.8, (0, 0, 0)), (12.6, (-3, -4, 0)), (13.3, (-1, -6, -2)), (15.9, (-2, -3, -1))]
BROW_R = [(0, (0, 0)), (0.2, (0.006, 0)), (0.55, (0.008, 6)), (1.2, (0.004, 0)), (2.0, (0.003, -4)), (2.6, (0.0, 0)), (3.5, (0.004, 0)), (7.1, (0.005, -4)), (7.8, (0.0, 0)),
          (8.2, (0.004, 0)), (8.9, (0.0, -6)), (9.7, (0.004, 0)), (10.35, (0.009, 8)), (10.9, (0.003, 0)), (12.6, (0.006, 4)), (13.2, (0.009, 10)), (14.0, (0.006, 4)), (15.2, (0.008, 8))]
BROW_L = [(0, (0, 0)), (0.2, (0.006, 0)), (0.55, (0.008, -6)), (1.2, (0.004, 0)), (2.0, (0.003, 4)), (2.6, (0.0, 0)), (3.5, (0.004, 0)), (7.1, (0.005, 4)), (7.8, (0.0, 0)),
          (8.2, (0.004, 0)), (8.9, (0.0, 6)), (9.7, (0.004, 0)), (10.35, (0.005, -4)), (10.9, (0.002, 0)), (12.6, (0.004, -2)), (13.2, (0.003, -4)), (14.0, (0.003, -2)), (15.2, (0.003, -3))]
SMILE = [(0, 0.15), (2.6, 0.2), (3.5, 0.45), (7.2, 0.75), (7.9, 0.45), (8.2, 0.35), (9.8, 0.45), (10.4, 0.7), (11.0, 0.45), (12.6, 0.6), (13.15, 1.0), (15.9, 0.9)]
SMIRK = [(0, 0.0), (7.2, 0.3), (7.9, 0.0), (10.4, 0.4), (11.0, 0.0), (13.15, 0.9), (15.9, 0.7)]


# ------------------------------------------------------------------ DISEGNO sul foglio (24/11): il macro s3 (5.2-6.6 s, «in scala») mostra un pantalone che si traccia, tratto unico, la matita lo segue.
# Coordinate relative al centro del foglio, metri sul piano del tavolo; il macro inquadra circa 5 cm di larghezza.
DISEGNO = dict(t0=5.30, t1=6.45, c=(0.02, -0.165), w=0.00050, path=[
    (-0.018, 0.045), (0.018, 0.045),                       # vita
    (0.022, -0.040), (0.004, -0.040), (0.001, -0.002),     # gamba destra: esterno, orlo, interno, cavallo
    (-0.002, -0.040), (-0.020, -0.040), (-0.018, 0.045)])  # gamba sinistra: orlo, esterno
