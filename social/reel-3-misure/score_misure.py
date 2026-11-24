"""Partitura del Reel «Le 3 misure» (24/11/2026). Letta da social/gemello/reel.py (--score).
Voce FUORI CAMPO: Jacopino non parla (LIPS a riposo), lavora al tavolo e guarda i pantaloni, mai la camera.
Tempi dalla concatenazione della voce (videos/_bench/reel-3-misure/vo/vo.wav, 32.74 s):
  P1 0-2.84 | P2 3.24-6.45 | P3 6.75-12.08 | P4 12.38-17.82 | P5 18.12-22.75 | P6 23.15-28.88 | P7 29.33-32.74
Coordinate delle mani e dei pantaloni: MONDO in metri (IK_WORLD). Il pupazzo sta in x=0, y=0.13 e guarda verso -y (camera); il tavolo gli arriva all'anca.
"""
import math
DUR = 32.75
VO = "D:/ClaudeCodeTest/videos/_bench/reel-3-misure/vo/vo.wav"
LIPS = [(0.0, "X")]
STRESS = []
HIDE_OLD = True
TAPE_L = 0.09
ATELIER = dict(forbici=(0.100, 0.005), forbici_rot=28, gesso=(-0.100, 0.020), rocchetto=(0.112, 0.062), puntaspilli=(-0.112, 0.070), manichino=(-0.24, 0.34))
IK_WORLD = True

ZT = 0.075                                   # piano del tavolo
YW = 0.098                                   # bordo vita dei pantaloni (lato del pupazzo)
PA = dict(wh=0.024, hh=0.030, kh=0.0285, eh=0.0275, hemw=0.0255, rise=0.029, L=0.112)   # pantalone largo (sabbia, cotone drill): quello da misurare
PB = dict(wh=0.021, hh=0.0255, kh=0.022, eh=0.0195, hemw=0.019, rise=0.029, L=0.112)    # pantalone stretto (indaco): serve solo al gancio
SAND = (0.40, 0.31, 0.18); INDIGO = (0.035, 0.05, 0.11)
TAVOLO = dict(top=ZT, x0=-0.17, x1=0.17, y0=-0.06, y1=0.106, trousers=[
    dict(name="H1", P=PA, col=SAND, cx=-0.052, yw=YW, tag="M", tagrot=-4, hide_from=2.95),
    dict(name="H2", P=PB, col=INDIGO, cx=0.052, yw=YW, tag="M", tagrot=5, hide_from=2.95),
    dict(name="A", P=PA, col=SAND, cx=0.0, yw=YW, show_from=2.95),
])

# ------------------------------------------------------------------ linee di misura (si tracciano) + punto A (zero del metro) e B (direzione)
RISE_Y = YW - PA["rise"]                     # y dell'incrocio (cavallo)
HEM_Y = YW - PA["L"]
MISURE = [
    dict(name="vita", A=(-PA["wh"], YW - 0.0030), B=(PA["wh"], YW - 0.0030), path=[(-PA["wh"], YW - 0.0030), (PA["wh"], YW - 0.0030)], t0=8.40, t1=10.20, z=0.0062, tz=0.0049, w=0.0010, keep=True, tape_off=12.0),
    dict(name="cavallo", A=(0.0, RISE_Y), B=(0.0, YW - 0.0006), path=[(0.0, RISE_Y), (0.0, YW - 0.0006)], t0=14.60, t1=16.60, z=0.0050, tz=0.0035, w=0.0010, tape_off=17.8, keep=True),
    dict(name="interno", A=(-0.0015, RISE_Y - 0.003), B=(-0.0020, HEM_Y), path=[(-0.0015, RISE_Y - 0.003), (-0.0020, HEM_Y)], t0=20.30, t1=22.30, z=0.0050, tz=0.0035, w=0.0010, tape_off=22.9, keep=True),
]

# ------------------------------------------------------------------ camera (una per inquadratura, taglio netto)
SHOTS = [
    dict(name="s1_gancio", t0=0.00, t1=3.24, lens=35, P0=(0.02, -0.32, 0.31), P1=(-0.01, -0.22, 0.27), L0=(0.0, 0.05, 0.105), L1=(0.0, 0.05, 0.105), fstop=7.0, FOC0=(0, 0.045, ZT), FOC1=(0, 0.045, ZT)),
    dict(name="s2_setup", t0=3.24, t1=6.75, lens=50, P0=(-0.13, -0.17, 0.21), P1=(-0.11, -0.14, 0.20), L0=(0.0, 0.085, 0.10), L1=(0.0, 0.085, 0.10), fstop=8.0, FOC0=(0, 0.085, ZT), FOC1=(0, 0.085, ZT)),
    dict(name="s3_vita", t0=6.75, t1=12.38, lens=40, P0=(-0.15, -0.20, 0.29), P1=(-0.08, -0.13, 0.25), L0=(0.0, 0.085, 0.125), L1=(0.0, 0.087, 0.125), fstop=8.0, FOC0=(0, 0.095, ZT), FOC1=(0, 0.095, ZT)),
    dict(name="s4_cavallo", t0=12.38, t1=18.12, lens=40, P0=(0.06, -0.24, 0.27), P1=(0.02, -0.15, 0.24), L0=(0.0, 0.080, 0.125), L1=(0.0, 0.082, 0.125), fstop=8.0, FOC0=(0, 0.080, ZT), FOC1=(0, 0.080, ZT)),
    dict(name="s5_interno", t0=18.12, t1=23.15, lens=50, P0=(-0.11, -0.12, 0.20), P1=(-0.09, -0.09, 0.19), L0=(0.0, 0.065, 0.095), L1=(0.0, 0.050, 0.095), fstop=8.0, FOC0=(0, 0.05, ZT), FOC1=(0, 0.04, ZT)),
    dict(name="s6_numeri", t0=23.15, t1=29.33, lens=50, P0=(0.0, -0.30, 0.28), P1=(0.0, -0.20, 0.23), L0=(0.0, 0.060, 0.090), L1=(0.0, 0.060, 0.090), fstop=7.0, FOC0=(0, 0.05, ZT), FOC1=(0, 0.05, ZT)),
    dict(name="s7_domanda", t0=29.33, t1=32.76, lens=50, P0=(-0.10, -0.15, 0.19), P1=(-0.08, -0.12, 0.18), L0=(0.0, 0.085, 0.11), L1=(0.0, 0.085, 0.11), fstop=6.0, FOC0=(0, 0.085, ZT), FOC1=(0, 0.085, ZT)),
]


def lead_track(path, t0, t1, off, n=9, lo=None, hi=None):
    """Chiavi (t, pos) di una mano che segue la punta della linea (path in mondo) tra t0 e t1; off = scostamento del polso dal punto; lo/hi limitano y (portata del braccio)."""
    seg = [math.dist(path[i], path[i + 1]) for i in range(len(path) - 1)]; tot = sum(seg); out = []
    for k in range(n + 1):
        u = k / n; u = u * u * (3 - 2 * u); d = tot * u; i = 0
        while i < len(seg) - 1 and d > seg[i]: d -= seg[i]; i += 1
        f = 0.0 if seg[i] == 0 else min(1.0, d / seg[i])
        x = path[i][0] + (path[i + 1][0] - path[i][0]) * f; y = path[i][1] + (path[i + 1][1] - path[i][1]) * f
        y = y + off[1]
        if lo is not None: y = max(y, lo)
        if hi is not None: y = min(y, hi)
        out.append((t0 + (t1 - t0) * k / n, (x + off[0], y, off[2])))
    return out

# ------------------------------------------------------------------ mani (mondo). Polso = bersaglio IK; il palmo sta ~2 cm avanti al polso.
REST_R = (-0.026, 0.119, 0.078); REST_L = (0.029, 0.130, 0.077)
EDGE_L = (0.060, 0.112, 0.083); EDGE_R = (-0.060, 0.112, 0.083)
ZH = 0.090                                   # altezza del polso quando la mano e' sul tessuto
A_VITA_R = (-0.027, 0.116, ZH)               # mano destra (a sinistra dello schermo) tiene lo zero del metro all'angolo sinistro della vita
A_CAV_R = (-0.006, RISE_Y + 0.024, ZH)       # mano destra all'incrocio
A_INT_L = (0.008, RISE_Y + 0.024, ZH)        # mano sinistra all'incrocio (interno gamba)
SMOOTH = [(3.30, (-0.030, 0.100, 0.084)), (3.80, (0.020, 0.075, 0.084)), (4.30, (-0.020, 0.095, 0.084)), (4.80, (0.025, 0.060, 0.084)), (5.30, (-0.010, 0.085, 0.084))]

# Coreografia delle mani (24/11): una mano TIENE lo zero del metro, l'altra lo porta all'altra estremita'; arrivano dai due lati e non si incrociano mai;
# prima di posarsi passano SOPRA il tessuto (z 0.105-0.110) poi scendono (z 0.090). x < 0: mano destra del pupazzo (sinistra dello schermo); x > 0: sinistra.
HV = 0.108                                   # quota di volo della mano
IKR_POS = [(0, REST_R), (3.20, (-0.030, 0.108, 0.086))] + SMOOTH + [(6.30, EDGE_R),
           (6.75, (-0.040, 0.120, HV)), (7.15, A_VITA_R), (10.90, A_VITA_R), (11.25, (-0.040, 0.118, HV)), (11.70, EDGE_R),
           (12.55, EDGE_R), (13.00, (-0.025, 0.121, HV)), (13.40, (-0.012, 0.118, ZH)), (17.20, (-0.012, 0.118, ZH)), (17.60, (-0.025, 0.121, HV)),
           (18.30, (-0.016, 0.100, HV)), (18.70, (-0.013, 0.092, ZH))] + lead_track([(-0.002, RISE_Y - 0.003), (-0.002, HEM_Y)], 20.3, 22.3, (-0.012, 0.022, ZH), lo=0.040) + [(22.80, (-0.016, 0.060, HV)), (23.30, EDGE_R), (29.0, EDGE_R)]
IKR_INF = [(0, 0.0), (3.10, 1.0), (28.9, 1.0), (30.5, 0.0)]
IKL_POS = [(0, REST_L), (2.95, EDGE_L), (7.60, EDGE_L), (8.00, (0.040, 0.116, HV)), (8.35, (0.031, 0.114, ZH)), (10.90, (0.031, 0.114, ZH)), (11.25, (0.045, 0.114, HV)), (11.70, EDGE_L),
           (12.55, EDGE_L), (13.00, (0.026, 0.100, HV)), (13.45, (0.011, 0.088, ZH)), (22.80, (0.011, 0.088, ZH)), (23.25, (0.030, 0.100, HV)), (23.70, EDGE_L), (30.0, EDGE_L)]
IKL_INF = [(0, 0.0), (2.95, 1.0), (30.5, 1.0), (31.5, 0.0)]
HANDL = [(0, (0, 0, 0)), (8.2, (20, 0, 0)), (11.0, (0, 0, 0)), (13.3, (20, 0, 0)), (22.9, (0, 0, 0))]
HANDR = [(0, (0, 0, 0)), (7.0, (20, 0, 0)), (11.0, (0, 0, 0)), (13.2, (20, 0, 0)), (17.4, (0, 0, 0)), (18.6, (20, 0, 0)), (22.9, (0, 0, 0))]
FING_L_IDX = [(0, 0.0)]; FING_L_OTH = [(0, 0.0)]       # mani aperte e piatte sul tessuto
FING_R_IDX = [(0, 0.0)]; FING_R_OTH = [(0, 0.0)]

# ------------------------------------------------------------------ testa e corpo: guarda in basso verso i pantaloni, non verso la camera
# HEAD = (beccheggio, imbardata, rollio) in gradi; beccheggio positivo = chinare. L'imbardata di base (-15.6) e' gia' in reel.py.
HEAD = [(0, (-22, 10, 0)), (1.0, (-24, 10, 0)), (1.5, (-26, -10, 0)), (2.5, (-28, -8, 0)), (3.0, (-32, 4, 0)), (6.9, (-32, 6, 0)), (10.9, (-30, -2, 0)), (12.8, (-32, 0, 0)), (14.3, (-32, -2, 0)), (17.9, (-30, 0, 0)), (18.3, (-34, 5, 0)), (22.8, (-30, 0, 0)), (23.3, (-20, 0, 0)), (23.7, (-34, 0, 0)), (26.5, (-28, 0, 0)), (29.5, (-26, 4, 0)), (32.0, (-28, 0, 0))]
SPINE = [(0, (6, 0, 0)), (3.0, (14, 0, 0)), (18.0, (20, 0, 0)), (22.8, (20, 0, 0)), (23.6, (8, 0, 0)), (29.5, (12, 0, 0))]
BROW_R = [(0, (0, 0)), (5.0, (0.004, 2)), (9.0, (0.003, -2)), (20.0, (0.004, 2))]
BROW_L = [(0, (0, 0)), (5.0, (0.004, 2)), (9.0, (0.003, -2)), (20.0, (0.004, 2))]
SMILE = [(0, 0.10), (24.0, 0.10), (28.8, 0.35), (32.0, 0.35)]
SMIRK = [(0, 0.0)]


# ===== V2 STABILE (24/11/2026): Jacopino NON muove le mani sugli oggetti (mani ferme sul bordo del tavolo: solo respiro e sguardo); il metro si srotola da solo, le linee si tracciano da sole.
# La retention la fanno la camera (livellata, senza shake, un cambio ogni ~2 s), le prospettive diverse e gli eventi in scena.
NO_SHAKE = True
IKR_POS = [(0, EDGE_R)]; IKR_INF = [(0, 1.0)]
IKL_POS = [(0, EDGE_L)]; IKL_INF = [(0, 1.0)]
HANDL = [(0, (0, 0, 0))]; HANDR = [(0, (0, 0, 0))]
def shot(name, t0, t1, lens, P0, P1, L0, L1, fstop=8.0):
    return dict(name=name, t0=t0, t1=t1, lens=lens, P0=P0, P1=P1, L0=L0, L1=L1, fstop=fstop, FOC0=L0, FOC1=L1)
Z0 = ZT + 0.002
SHOTS = [
    # gancio: push frontale, poi radente sui cartellini «M»
    shot("h1_largo", 0.00, 3.24, 35, (0.02, -0.32, 0.31), (0.0, -0.20, 0.24), (0.0, 0.05, 0.095), (0.0, 0.05, 0.095), 7.0),
    # stesura: giro alto attorno al pantalone, poi radente lungo le gambe verso la vita
    shot("s2a_alto", 3.24, 5.00, 40, (0.0, -0.30, 0.30), (0.0, -0.19, 0.21), (0.0, 0.04, ZT), (0.0, 0.04, ZT), 8.0),
    shot("s2b_radente", 5.00, 6.75, 40, (0.10, -0.20, 0.15), (0.06, -0.11, 0.125), (0.0, 0.05, 0.085), (0.0, 0.06, 0.085), 8.0),
    # vita: tre quarti, poi dall'alto che segue la linea, poi macro sull'angolo destro (×2)
    shot("s3a_tre_quarti", 6.75, 8.40, 40, (-0.15, -0.20, 0.29), (-0.12, -0.16, 0.27), (0.0, 0.085, 0.125), (0.0, 0.087, 0.12), 8.0),
    shot("s3b_alto_linea", 8.40, 10.20, 50, (-0.035, 0.015, 0.20), (0.035, 0.015, 0.20), (-0.024, YW - 0.003, ZT), (0.026, YW - 0.003, ZT), 8.0),
    shot("s3c_alto_destra", 10.20, 12.38, 40, (0.13, -0.17, 0.25), (0.10, -0.12, 0.22), (0.0, 0.085, 0.09), (0.0, 0.088, 0.09), 9.0),
    # cavallo: tre quarti da destra, dall'alto sulla linea che sale, frontale basso all'incrocio
    shot("s4a_destra", 12.38, 14.60, 40, (0.14, -0.17, 0.24), (0.10, -0.14, 0.22), (0.0, 0.08, 0.10), (0.0, 0.08, 0.10), 8.0),
    shot("s4b_alto_linea", 14.60, 16.60, 50, (0.0, -0.02, 0.18), (0.0, 0.025, 0.17), (0.0, RISE_Y, ZT), (0.0, YW, ZT), 8.0),
    shot("s4c_alto_frontale", 16.60, 18.12, 40, (0.0, -0.20, 0.22), (0.0, -0.14, 0.19), (0.0, 0.08, 0.09), (0.0, 0.082, 0.09), 9.0),
    # interno gamba: tre quarti da sinistra, dall'alto che scende lungo la gamba, allargo
    shot("s5a_sinistra", 18.12, 20.30, 40, (-0.13, -0.14, 0.21), (-0.10, -0.12, 0.20), (0.0, 0.06, 0.09), (0.0, 0.05, 0.09), 8.0),
    shot("s5b_alto_gamba", 20.30, 22.30, 50, (0.0, 0.0, 0.17), (0.0, -0.07, 0.17), (-0.002, RISE_Y, ZT), (-0.002, HEM_Y, ZT), 8.0),
    shot("s5c_allargo", 22.30, 23.15, 35, (0.0, -0.20, 0.20), (0.0, -0.24, 0.22), (0.0, 0.04, 0.09), (0.0, 0.05, 0.09), 8.0),
    # tre numeri: giro lento attorno ai pantaloni con le tre linee visibili
    shot("s6a_giro", 23.15, 26.25, 40, (-0.12, -0.25, 0.22), (0.0, -0.28, 0.26), (0.0, 0.05, 0.09), (0.0, 0.05, 0.09), 8.0),
    shot("s6b_giro", 26.25, 29.33, 40, (0.0, -0.28, 0.26), (0.12, -0.25, 0.22), (0.0, 0.05, 0.09), (0.0, 0.05, 0.09), 8.0),
    # domanda: spinta da tavolo a Jacopino
    shot("s7_domanda", 29.33, 32.76, 50, (-0.06, -0.18, 0.12), (0.0, -0.12, 0.16), (0.0, 0.09, 0.11), (0.0, 0.11, 0.16), 6.0),
]


# ===== V3 (24/11): Jacopino 7 cm dietro il tavolo (sagoma separata, niente giacca-tavolo), misure dirette (colore, segnalini, nome sul tessuto), inquadrature piu' larghe
PUPPET_Y = 0.18
MAT_DEPTH = 0.62
ARANCIO = (0.92, 0.10, 0.04); AZZURRO = (0.10, 0.55, 1.0); MAGENTA = (0.85, 0.10, 0.50)
MISURE[0].update(col=ARANCIO, caps=True, capl=0.010, label="VITA", lpos=(-0.0105, YW - 0.0145), lsize=0.011, w=0.0013, tz=0.0049)
MISURE[1].update(col=AZZURRO, caps=True, capl=0.009, label="CAVALLO", lpos=(0.0135, 0.0745), lrot=90, lsize=0.0066, w=0.0013)
MISURE[2].update(col=MAGENTA, caps=True, capl=0.009, label="INTERNO", lpos=(-0.0175, (RISE_Y + HEM_Y) / 2), lrot=90, lsize=0.0085, w=0.0013)
