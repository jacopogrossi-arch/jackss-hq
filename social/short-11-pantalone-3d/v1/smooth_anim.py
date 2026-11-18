"""Ammorbidisce le rotazioni dell'animazione 'performance' di un GLB (stessa dimensione del file): filtro gaussiano sui quaternioni, sigma in fotogrammi per osso.
Perche': blender_perf.py mette un colpetto a ogni parola su mano e avambraccio (fino a 25 gradi in 1/24 s) e sul rendering sembra "glitchato".
Uso: python smooth_anim.py in.glb out.glb   (valori usati il 18/11/2026: mani 2.5, avambracci 2.0, braccia/spalle/collo/testa 1.5, busto/anche 1.0)"""
import json, struct, sys
import numpy as np
from scipy.ndimage import gaussian_filter1d
src, dst = sys.argv[1:3]
b = bytearray(open(src, 'rb').read()); l = struct.unpack('<I', b[12:16])[0]; j = json.loads(bytes(b[20:20 + l])); bin0 = 20 + l + 8
SIG = (('ForeArm', 2.0), ('Hand', 2.5), ('Shoulder', 1.5), ('Arm', 1.5), ('Neck', 1.5), ('Head', 1.5), ('Spine', 1.0), ('Hips', 1.0))
sig = lambda name: next((s for k, s in SIG if k in name), 1.0)
an = j['animations'][0]
for ch in an['channels']:
    if ch['target']['path'] != 'rotation': continue
    a = j['accessors'][an['samplers'][ch['sampler']]['output']]; n = a['count']
    if n < 10: continue
    o = bin0 + j['bufferViews'][a['bufferView']].get('byteOffset', 0) + a.get('byteOffset', 0)
    q = np.frombuffer(b, dtype='<f4', count=n * 4, offset=o).reshape(n, 4).astype(np.float64).copy()
    for i in range(1, n):
        if (q[i] * q[i - 1]).sum() < 0: q[i] = -q[i]
    q = gaussian_filter1d(q, sig(j['nodes'][ch['target']['node']]['name']), axis=0, mode='nearest'); q /= np.linalg.norm(q, axis=1, keepdims=True)
    b[o:o + n * 16] = q.astype('<f4').tobytes()
open(dst, 'wb').write(b)
