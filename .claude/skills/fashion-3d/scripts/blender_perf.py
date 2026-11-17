"""Costruisce una PERFORMANCE (un'unica animazione lunga quanto il video) per un pupazzo rigged (Mixamo/Tripo), guidata dal PARLATO: braccia, mani, busto e testa si muovono
a tempo delle parole, non e' un taglia-e-incolla di clip.
Cosa fa:
 1. IMPARA dalle clip del file (es. le 4 clip Tripo): campiona le pose delle braccia/mani nelle clip "parlate" e ne ricava un vocabolario (cluster = pose tipo: braccia aperte, palmi in su,
    mani sui fianchi...), la posa di riposo (clip ferma), e le componenti principali del movimento di busto/testa (ampiezze e direzioni reali, senza indovinare gli assi).
 2. COMPONE la performance: sulle parole forti (parole chiave, parole lunghe, picchi di voce, inizio di frase) il corpo va in una posa del vocabolario (anticipo ~0.3 s, molla smorzata
    con un filo di overshoot), la tiene, e rientra a riposo nelle pause; il braccio sinistro e' in ritardo di 0.1 s sul destro; piccoli sbandamenti lenti; cenno della testa sugli accenti.
 3. SCRIVE un'azione 'performance' a 30 fps (rotation_quaternion di ogni osso) e la esporta nel GLB: nel motore e' una normale clip da riprodurre in funzione del tempo.
Uso: blender -b -P blender_perf.py -- in.glb out.glb words.json jaw.json durata_s [parole_chiave_virgola]
"""
import bpy, sys, json, math
import numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
IN, OUT, WORDS, JAW, DUR = a[0], a[1], a[2], a[3], float(a[4])
KEY = set((a[5] if len(a) > 5 else '').lower().split(',')) - {''}
FPS_OUT = 30
rng = np.random.RandomState(7)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=IN)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
sc.render.fps = FPS_OUT


def fcurves_of(act):
    try: return list(act.fcurves)
    except Exception:
        out = []
        for layer in act.layers:
            for strip in layer.strips:
                for cb in strip.channelbags: out += list(cb.fcurves)
        return out


# ---------- quaternion <-> tangent (rotation vector), Blender order (w, x, y, z)
def qlog(q):
    q = q / np.linalg.norm(q, axis=-1, keepdims=True)
    q = np.where(q[..., :1] < 0, -q, q)
    v = q[..., 1:]; n = np.linalg.norm(v, axis=-1, keepdims=True)
    ang = 2 * np.arctan2(n, q[..., :1])
    return np.where(n > 1e-9, v / np.maximum(n, 1e-12) * ang, 0.0 * v)


def qexp(t):
    ang = np.linalg.norm(t, axis=-1, keepdims=True)
    ax = np.where(ang > 1e-9, t / np.maximum(ang, 1e-12), 0.0 * t)
    return np.concatenate([np.cos(ang / 2), ax * np.sin(ang / 2)], axis=-1)


# ---------- 1) campiona le clip
bones = [b.name for b in arm.pose.bones]
ARM = [n for n in bones if any(s in n for s in ('Left', 'Right')) and any(s in n for s in ('Shoulder', 'Arm', 'Hand')) and not any(s in n for s in ('Leg', 'Foot', 'Toe'))]
TORSO = [n for n in bones if n.split(':')[-1] in ('Hips', 'Spine', 'Spine1', 'Spine2', 'Neck', 'Head')]
print('ossa braccia/mani', len(ARM), 'busto/testa', TORSO)
clips = {}
for act in bpy.data.actions:
    fcs = {}
    for fc in fcurves_of(act):
        if fc.data_path.endswith('rotation_quaternion'):
            nm = fc.data_path.split('"')[1]; fcs.setdefault(nm, {})[fc.array_index] = fc
    fr0, fr1 = int(act.frame_range[0]), int(act.frame_range[1])
    frames = list(range(fr0, fr1 + 1, 2))
    data = {}
    for nm in ARM + TORSO:
        if nm in fcs and len(fcs[nm]) == 4:
            q = np.array([[fcs[nm][k].evaluate(f) for k in range(4)] for f in frames])
            data[nm] = qlog(q)
    clips[act.name] = data
names = list(clips)
motion = {n: sum(np.abs(np.diff(v, axis=0)).sum() for k, v in clips[n].items() if k in ARM) for n in names}
idle_name = min(motion, key=motion.get); talk_names = [n for n in names if n != idle_name]
print('clip ferma:', idle_name[:50], '| clip parlate:', len(talk_names))
IDLE = np.concatenate([clips[idle_name][b].mean(axis=0) for b in ARM])                 # posa di riposo (tangenti delle braccia)
X = np.concatenate([np.concatenate([clips[n][b] for b in ARM], axis=1) for n in talk_names], axis=0)        # (campioni, 3*ossa)
# k-means: vocabolario di pose
K = 9
cent = X[rng.choice(len(X), K, replace=False)]
for _ in range(40):
    d = ((X[:, None, :] - cent[None]) ** 2).sum(-1); lab = d.argmin(1)
    for k in range(K):
        if (lab == k).any(): cent[k] = X[lab == k].mean(0)
sizes = [(lab == k).sum() for k in range(K)]
arm_idx = [i for i, b in enumerate(ARM) if b.split(':')[-1][4:] in ('Arm', 'ForeArm') or b.split(':')[-1][5:] in ('Arm', 'ForeArm')]
def energy(c):                                                  # quanto e' lontana dal riposo la posa di braccia/avambracci
    return sum(np.linalg.norm((c - IDLE)[3 * i:3 * i + 3]) for i in arm_idx)
order = sorted(range(K), key=lambda k: energy(cent[k]))
POSES = [cent[k] for k in order]; EN = [energy(c) for c in POSES]
print('energie delle pose (rad, braccia+avambracci):', ' '.join('%.2f' % e for e in EN), '| riposo %.2f' % energy(IDLE))
LOW_I, MID_I, HIGH_I = [0, 1, 2], [3, 4, 5], list(range(6, K))
# busto/testa: componenti principali
T = np.concatenate([np.concatenate([clips[n][b] for b in TORSO], axis=1) for n in talk_names], axis=0)
Tm = T.mean(0); U, S, Vt = np.linalg.svd(T - Tm, full_matrices=False)
NPC = 4; sig = S[:NPC] / np.sqrt(len(T)); PCs = Vt[:NPC]
torso_idle = np.concatenate([clips[idle_name][b].mean(axis=0) for b in TORSO])
print('componenti busto/testa: sigma', np.round(sig, 3))
# il corpo segue le braccia: regressione (ridge) del busto/anche sulle prime componenti della posa delle braccia, imparata dalle clip (in un'animazione vera il busto si muove con i gesti)
Xm = X.mean(0); _, SX, VX = np.linalg.svd(X - Xm, full_matrices=False); NZ = 8; PX = VX[:NZ]
Z = (X - Xm) @ PX.T; lam = 0.5 * len(Z)
BR = np.linalg.solve(Z.T @ Z + lam * np.eye(NZ), Z.T @ (T - Tm))                # (NZ, 3*ossa_busto)
print('regressione braccia->corpo: residuo %.2f della varianza' % (((T - Tm - Z @ BR) ** 2).sum() / ((T - Tm) ** 2).sum()))


# quale componente e' un "cenno" (testa verso avanti/basso)? lo misuro sul rig
head = arm.pose.bones[[n for n in TORSO if n.endswith('Head')][0]]
def head_tip_after(vec):
    for i, b in enumerate(TORSO):
        pb = arm.pose.bones[b]; pb.rotation_mode = 'QUATERNION'; pb.rotation_quaternion = qexp(vec[3 * i:3 * i + 3]).tolist()
    bpy.context.view_layer.update()
    return np.array((arm.matrix_world @ head.tail)[:])
base = head_tip_after(torso_idle); nod = None
for i in range(NPC):
    d = head_tip_after(torso_idle + PCs[i] * sig[i] * 2) - base
    print('PC%d spostamento punta testa (x,y,z) cm:' % i, np.round(d * 100, 2))
    sc_ = abs(d[1]) + 0.3 * abs(d[2])                         # cenno = si muove in avanti/indietro (Y)
    if nod is None or sc_ > nod[0]: nod = (sc_, i, -1.0 if d[1] > 0 else 1.0)    # il viso guarda verso -Y: avanti = Y che diminuisce
NOD_PC, NOD_SIGN = nod[1], nod[2]
print('PC del cenno:', NOD_PC, 'segno', NOD_SIGN)
for b in TORSO + ARM:
    pb = arm.pose.bones[b]; pb.rotation_quaternion = (1, 0, 0, 0)

# ---------- 2) la partitura dal parlato
W = json.load(open(WORDS)); JAWC = np.array(json.load(open(JAW)))
NS = int(DUR * 60)
def loud(t0, t1): seg = JAWC[int(t0 * 60):int(t1 * 60) + 1]; return float(seg.max()) if len(seg) else 0.0
strip = lambda s: ''.join(ch for ch in s.lower() if ch.isalnum())
phrases, cur = [], []
for i, w in enumerate(W):
    if cur and w['s'] - cur[-1]['e'] > 0.35: phrases.append(cur); cur = []
    cur.append(w)
    if w['w'][-1] in '.?!': phrases.append(cur); cur = []
if cur: phrases.append(cur)
events = []                                                     # (apex, class 0..2)
for ph in phrases:
    cands = []
    for j, w in enumerate(ph):
        sc_ = (1.0 if strip(w['w']) in KEY else 0) + (0.5 if len(strip(w['w'])) >= 6 else 0) + (0.5 if j == 0 else 0) + 0.8 * loud(w['s'], w['e']) + (0.6 if w['w'][-1] in '?!' else 0)
        cands.append((sc_, w['s'] + 0.04))
    cands.sort(reverse=True); chosen = []
    for sc_, t in cands:
        if all(abs(t - c[1]) >= 0.9 for c in chosen) and sc_ >= 0.9: chosen.append((sc_, t))
    if not chosen: chosen = [cands[0]]
    for sc_, t in chosen: events.append((t, 2 if sc_ >= 2.0 else 1 if sc_ >= 1.3 else 0, ph[-1]['e'], ph))
events.sort()
print('gesti:', len(events), 'in', len(phrases), 'frasi')

K1 = len(POSES) + 1                                             # + il riposo (ultimo)
IDLE_I = K1 - 1
allP = POSES + [IDLE]
target = np.full(NS, IDLE_I, dtype=int)
prev = -1; seq = []
last_end_of = {}
for ei, (t, cls, pend, ph) in enumerate(events):
    ids = [LOW_I, MID_I, HIGH_I][cls]
    ids = [i for i in ids if i != prev] or ids
    k = ids[ei % len(ids)]; prev = k
    nxt = events[ei + 1][0] if ei + 1 < len(events) else 1e9
    a0 = max(0.0, t - 0.30)
    hold_to = min(pend + 0.30, nxt - 0.30)                      # tiene la posa fino a fine frase (o all'anticipo del prossimo gesto)
    gap_after = nxt - pend
    seq.append((a0, hold_to, k, gap_after))
for a0, hold_to, k, gap_after in seq:
    i0, i1 = int(a0 * 60), int(min(DUR, max(hold_to, a0 + 0.4)) * 60)
    target[i0:i1] = k
# tra una frase e l'altra, se la pausa e' lunga: riposo; se e' corta: posa bassa di transizione
for (a0, hold_to, k, gap_after), (a1, *_r) in zip(seq, seq[1:] + [(DUR, 0, 0, 0)]):
    i0, i1 = int(max(hold_to, a0) * 60), int(max(a1, 0) * 60)
    if i1 > i0: target[i0:i1] = IDLE_I if (a1 - hold_to) > 0.9 else 0       # pausa lunga: riposo; corta: posa bassa di transizione

# molla smorzata sui pesi (overshoot leggero)
OM, ZE = 8.0, 0.60; dt = 1 / 60
w_ = np.zeros(K1); w_[IDLE_I] = 1; vel = np.zeros(K1); WH = np.zeros((NS, K1))
for i in range(NS):
    tgt = np.zeros(K1); tgt[target[i]] = 1
    acc = OM * OM * (tgt - w_) - 2 * ZE * OM * vel
    vel += acc * dt; w_ += vel * dt; WH[i] = w_
Pmat = np.array(allP)                                           # (K1, D)
def pose_at(i, lag=0):
    j = max(0, i - lag); return WH[j] @ Pmat
# energia del parlato (liscia) per il busto
E = np.convolve(JAWC[:NS] if len(JAWC) >= NS else np.pad(JAWC, (0, NS - len(JAWC))), np.ones(30) / 30, mode='same')
def smoothnoise(freqs, ph0):
    t = np.arange(NS) / 60; return sum(np.sin(2 * np.pi * f * t + p) for f, p in zip(freqs, ph0)) / len(freqs)
noise_arm = [smoothnoise([0.13, 0.27, 0.41], rng.uniform(0, 6.28, 3)) for _ in ARM]
arm_std = X.std(axis=0)
pcn = [smoothnoise([0.09 + 0.05 * i, 0.21 + 0.03 * i], rng.uniform(0, 6.28, 2)) for i in range(NPC)]
nod_env = np.zeros(NS)
for t, cls, *_x in events:                                       # cenno sugli accenti
    i = int(t * 60); L = int(0.45 * 60)
    for q in range(L):
        if i + q < NS: nod_env[i + q] += (0.5 + 0.35 * cls) * math.sin(math.pi * q / L) ** 2
BEAT_G, BODY_G = 0.22, 1.5
bump = np.zeros(NS)                                              # colpetto all'attacco di ogni parola (decade in ~0.12 s)
for w in W:
    i0 = int(w['s'] * 60); amp = 0.4 + 0.6 * loud(w['s'], w['e'])
    for q in range(int(0.5 * 60)):
        if i0 + q < NS: bump[i0 + q] += amp * math.exp(-q / (0.12 * 60))
bump = np.clip(bump, 0, 1.6)
print('keyframes: 30 fps x', int(DUR * FPS_OUT), 'frame x', len(ARM) + len(TORSO), 'ossa')

# ---------- 3) scrivi l'azione
for act in list(bpy.data.actions): bpy.data.actions.remove(act)
arm.animation_data_clear(); arm.animation_data_create()
for b in arm.pose.bones: b.rotation_mode = 'QUATERNION'
nF = int(DUR * FPS_OUT) + 1
for fi in range(nF):
    i = min(NS - 1, int(fi / FPS_OUT * 60))
    for bi, b in enumerate(ARM):
        nm = b.split(':')[-1]
        dl = 0 if ('Shoulder' in nm or nm.endswith('Arm') and 'Fore' not in nm) else 4 if 'ForeArm' in nm else 8 if nm.endswith('Hand') else 11      # il gesto parte dalla spalla e "frusta" verso mano e dita
        side_lag = dl + (6 if 'Left' in b else 0)                      # il sinistro e' in ritardo di 0.1 s
        base_ = pose_at(i, side_lag)
        v = base_[3 * bi:3 * bi + 3]
        if dl >= 4: v = v + BEAT_G * bump[max(0, i - side_lag)] * (v - IDLE[3 * bi:3 * bi + 3])        # colpetto su ogni parola, solo avambraccio/mano/dita
        v = v + noise_arm[bi][i] * arm_std[3 * bi:3 * bi + 3] * 0.32
        pb = arm.pose.bones[b]; pb.rotation_quaternion = qexp(v).tolist(); pb.keyframe_insert('rotation_quaternion', frame=fi + 1)
    pv = pose_at(i, 3)
    coup = (((pv - Xm) @ PX.T) @ BR) * BODY_G                            # il corpo segue le braccia (appreso dalle clip)
    tv = torso_idle + Tm * 0 + coup + (0.5 + 0.9 * E[i]) * sum(sig[k] * pcn[k][i] * PCs[k] * 1.1 for k in range(NPC)) + NOD_SIGN * 0.9 * sig[NOD_PC] * nod_env[i] * PCs[NOD_PC]
    for bi, b in enumerate(TORSO):
        pb = arm.pose.bones[b]; pb.rotation_quaternion = qexp(tv[3 * bi:3 * bi + 3]).tolist(); pb.keyframe_insert('rotation_quaternion', frame=fi + 1)
sc.frame_start, sc.frame_end = 1, nF
act = arm.animation_data.action; act.name = 'performance'
print('azione', act.name, 'frames', nF)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_animations=True, export_skins=True, export_morph=True, export_image_format='JPEG', export_jpeg_quality=88)
print('salvato', OUT)
