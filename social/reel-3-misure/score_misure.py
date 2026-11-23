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
    dict(name="vita", A=(-PA["wh"], YW - 0.0030), B=(PA["wh"], YW - 0.0030), path=[(-PA["wh"], YW - 0.0030), (PA["wh"], YW - 0.0030)], t0=8.40, t1=10.20, z=0.0053, tz=0.0049, keep=True, tape_off=12.0),
    dict(name="cavallo", A=(0.0, RISE_Y), B=(0.0, YW - 0.0006), path=[(0.0, RISE_Y), (0.0, YW - 0.0006)], t0=14.60, t1=16.60, tape_off=17.8, keep=True),
    dict(name="interno", A=(-0.0015, RISE_Y - 0.003), B=(-0.0020, HEM_Y), path=[(-0.0015, RISE_Y - 0.003), (-0.0020, HEM_Y)], t0=20.30, t1=22.30, tape_off=22.9, keep=True),
]

# ------------------------------------------------------------------ camera (una per inquadratura, taglio netto)
SHOTS = [
    dict(name="s1_gancio", t0=0.00, t1=3.24, lens=35, P0=(0.0, -0.20, 0.27), P1=(0.0, -0.16, 0.25), L0=(0.0, 0.040, 0.078), L1=(0.0, 0.045, 0.078), fstop=5.0, FOC0=(0, 0.045, ZT), FOC1=(0, 0.045, ZT)),
    dict(name="s2_setup", t0=3.24, t1=6.75, lens=50, P0=(-0.13, -0.17, 0.21), P1=(-0.11, -0.14, 0.20), L0=(0.0, 0.085, 0.10), L1=(0.0, 0.085, 0.10), fstop=4.0, FOC0=(0, 0.085, ZT), FOC1=(0, 0.085, ZT)),
    dict(name="s3_vita", t0=6.75, t1=12.38, lens=50, P0=(-0.12, -0.10, 0.20), P1=(-0.10, -0.07, 0.19), L0=(0.0, 0.090, 0.095), L1=(0.0, 0.092, 0.095), fstop=4.0, FOC0=(0, 0.095, ZT), FOC1=(0, 0.095, ZT)),
    dict(name="s4_cavallo", t0=12.38, t1=18.12, lens=50, P0=(0.11, -0.10, 0.20), P1=(0.09, -0.07, 0.19), L0=(0.0, 0.080, 0.095), L1=(0.0, 0.082, 0.095), fstop=4.0, FOC0=(0, 0.080, ZT), FOC1=(0, 0.080, ZT)),
    dict(name="s5_interno", t0=18.12, t1=23.15, lens=50, P0=(-0.11, -0.12, 0.20), P1=(-0.09, -0.09, 0.19), L0=(0.0, 0.065, 0.095), L1=(0.0, 0.050, 0.095), fstop=4.0, FOC0=(0, 0.05, ZT), FOC1=(0, 0.04, ZT)),
    dict(name="s6_numeri", t0=23.15, t1=29.33, lens=50, P0=(0.0, -0.26, 0.26), P1=(0.0, -0.22, 0.24), L0=(0.0, 0.060, 0.090), L1=(0.0, 0.060, 0.090), fstop=5.0, FOC0=(0, 0.05, ZT), FOC1=(0, 0.05, ZT)),
    dict(name="s7_domanda", t0=29.33, t1=32.76, lens=50, P0=(-0.10, -0.15, 0.19), P1=(-0.08, -0.12, 0.18), L0=(0.0, 0.085, 0.11), L1=(0.0, 0.085, 0.11), fstop=3.5, FOC0=(0, 0.085, ZT), FOC1=(0, 0.085, ZT)),
]

# ------------------------------------------------------------------ mani (mondo). Polso = bersaglio IK; il palmo sta ~2 cm avanti al polso.
REST_R = (-0.026, 0.119, 0.078); REST_L = (0.029, 0.130, 0.077)
EDGE_L = (0.060, 0.112, 0.083); EDGE_R = (-0.060, 0.112, 0.083)
ZH = 0.090                                   # altezza del polso quando la mano e' sul tessuto
A_VITA_R = (-0.027, 0.116, ZH)               # mano destra (a sinistra dello schermo) tiene lo zero del metro all'angolo sinistro della vita
A_CAV_R = (-0.006, RISE_Y + 0.024, ZH)       # mano destra all'incrocio
A_INT_L = (0.008, RISE_Y + 0.024, ZH)        # mano sinistra all'incrocio (interno gamba)
SMOOTH = [(3.30, (-0.030, 0.100, 0.084)), (3.80, (0.020, 0.075, 0.084)), (4.30, (-0.020, 0.095, 0.084)), (4.80, (0.025, 0.060, 0.084)), (5.30, (-0.010, 0.085, 0.084))]

IKR_POS = [(0, REST_R), (3.20, (-0.030, 0.108, 0.086))] + SMOOTH + [(6.30, EDGE_R), (7.00, A_VITA_R), (10.90, A_VITA_R), (11.30, EDGE_R),
           (12.70, EDGE_R), (13.10, A_CAV_R), (17.40, A_CAV_R), (17.90, EDGE_R), (29.0, EDGE_R)]
IKR_INF = [(0, 0.0), (3.10, 1.0), (28.9, 1.0), (30.5, 0.0)]
IKL_POS = [(0, REST_L), (2.95, EDGE_L), (17.90, EDGE_L), (18.30, A_INT_L), (22.80, A_INT_L), (23.20, EDGE_L), (30.0, EDGE_L)]
IKL_INF = [(0, 0.0), (2.95, 1.0), (30.5, 1.0), (31.5, 0.0)]
HANDL = [(0, (0, 0, 0)), (18.2, (25, 0, 0)), (22.8, (0, 0, 0))]
HANDR = [(0, (0, 0, 0)), (3.2, (25, 0, 0)), (5.8, (0, 0, 0)), (6.9, (25, 0, 0)), (11.0, (0, 0, 0)), (13.0, (25, 0, 0)), (17.8, (0, 0, 0))]
FING_L_IDX = [(0, 0.3)]; FING_L_OTH = [(0, 0.3)]
FING_R_IDX = [(0, 0.3)]; FING_R_OTH = [(0, 0.3)]

# ------------------------------------------------------------------ testa e corpo: guarda in basso verso i pantaloni, non verso la camera
# HEAD = (beccheggio, imbardata, rollio) in gradi; beccheggio positivo = chinare. L'imbardata di base (-15.6) e' gia' in reel.py.
HEAD = [(0, (22, 0, 0)), (3.0, (30, 4, 0)), (6.9, (30, 6, 0)), (10.9, (28, -2, 0)), (12.8, (30, 0, 0)), (14.3, (30, -2, 0)), (17.9, (28, 0, 0)), (18.3, (30, 5, 0)), (22.8, (28, 0, 0)), (24.0, (26, 0, 0)), (29.5, (24, 4, 0)), (32.0, (26, 0, 0))]
SPINE = [(0, (6, 0, 0)), (3.0, (14, 0, 0)), (24.0, (14, 0, 0)), (29.5, (12, 0, 0))]
BROW_R = [(0, (0, 0)), (5.0, (0.004, 2)), (9.0, (0.003, -2)), (20.0, (0.004, 2))]
BROW_L = [(0, (0, 0)), (5.0, (0.004, 2)), (9.0, (0.003, -2)), (20.0, (0.004, 2))]
SMILE = [(0, 0.10), (24.0, 0.10), (28.8, 0.35), (32.0, 0.35)]
SMIRK = [(0, 0.0)]
