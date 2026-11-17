"""Colora un GLB bianco (es. da Hunyuan3D shape) proiettando 3 immagini di riferimento
(fronte/retro/lato) sui vertici, poi alleggerisce e esporta GLB con colori per vertice.
Uso: blender -b -P blender_color_project.py -- in.glb front.png back.png side.png out.glb [triangoli_target]
"""
import bpy, sys, numpy as np, mathutils
a = sys.argv[sys.argv.index('--')+1:]
IN, FR, BK, SD, OUT = a[:5]
TARGET = int(a[5]) if len(a) > 5 else 70000
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=IN)
ob = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
me = ob.data
# applica trasformazioni
bpy.context.view_layer.objects.active = ob; ob.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
n = len(me.vertices)
P = np.empty(n*3, np.float32); me.vertices.foreach_get('co', P); P = P.reshape(-1, 3)
N = np.empty(n*3, np.float32); me.vertices.foreach_get('normal', N); N = N.reshape(-1, 3)

def load(path):
    im = bpy.data.images.load(path)
    w, h = im.size
    px = np.array(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1, :, :3]
    return px
def fg_bbox(px):
    bg = np.median(np.concatenate([px[:8, :8].reshape(-1, 3), px[:8, -8:].reshape(-1, 3)]), axis=0)
    d = np.abs(px - bg).max(axis=2) > 0.12
    cols = np.where(d.sum(0) > 3)[0]; rows = np.where(d.sum(1) > 3)[0]
    return cols[0], cols[-1], rows[0], rows[-1]
def bgcolor(px):
    return np.median(np.concatenate([px[:8, :8].reshape(-1, 3), px[:8, -8:].reshape(-1, 3)]), axis=0)
def sample(px, bb, u, v):
    # restituisce (colore, validita'): scarta pixel simili allo sfondo e pixel di bordo
    x0, x1, y0, y1 = bb
    bg = bgcolor(px)
    fg = np.abs(px - bg).max(axis=2) > 0.12
    from numpy import ones
    k = fg.copy()
    for dx, dy in ((3,0),(-3,0),(0,3),(0,-3)):
        k &= np.roll(np.roll(fg, dx, 1), dy, 0)   # erosione ~3px
    xs = np.clip(x0 + u*(x1-x0), 0, px.shape[1]-1).astype(int)
    ys = np.clip(y0 + (1-v)*(y1-y0), 0, px.shape[0]-1).astype(int)
    return px[ys, xs], k[ys, xs].astype(np.float32)

mn, mx = P.min(0), P.max(0)
z = (P[:, 2]-mn[2])/(mx[2]-mn[2])
x = (P[:, 0]-mn[0])/(mx[0]-mn[0])
y = (P[:, 1]-mn[1])/(mx[1]-mn[1])
fr, bk, sd = load(FR), load(BK), load(SD)
bf, bb_, bs = fg_bbox(fr), fg_bbox(bk), fg_bbox(sd)
print('bbox img', bf, bb_, bs)
c_front, k_f = sample(fr, bf, x, z)       # fronte: x verso destra immagine
c_back, k_b = sample(bk, bb_, 1-x, z)     # retro specchiato
c_sideL, k_l = sample(sd, bs, 1-y, z)     # lato -X (vista dal -X: -Y a destra)
c_sideR, k_r = sample(sd, bs, y, z)       # lato +X (specchiato)
p = 4
wf = np.clip(-N[:, 1], 0, 1)**p; wb = np.clip(N[:, 1], 0, 1)**p
wl = np.clip(-N[:, 0], 0, 1)**p; wr = np.clip(N[:, 0], 0, 1)**p
# visibilita': ogni vista colora solo cio' che vede (z-buffer ortografico): le mani non si dipingono sulle cosce
def visible(u, depth, W=320, H=640, eps=0.025):
    ui = np.clip((u*(W-1)).astype(int), 0, W-1); vi = np.clip((z*(H-1)).astype(int), 0, H-1)
    G = np.full((H, W), 1e9, np.float32); np.minimum.at(G, (vi, ui), depth.astype(np.float32))
    return (depth <= G[vi, ui]+eps).astype(np.float32)
S = (mx-mn)
v_f = visible(x, P[:, 1]); v_b = visible(1-x, -P[:, 1]); v_l = visible(1-y, P[:, 0]); v_r = visible(y, -P[:, 0])
k_f, k_b, k_l, k_r = k_f*v_f, k_b*v_b, k_l*v_l, k_r*v_r
wf *= k_f; wb *= k_b; wl *= k_l; wr *= k_r
# pesi minimi cosi' i vertici dove tutti i campioni sono scartati restano colorati
wf += 1e-3*k_f; wb += 1e-3*k_b; wl += 1e-3*k_l; wr += 1e-3*k_r
W = wf+wb+wl+wr+1e-6
col = (c_front*wf[:, None]+c_back*wb[:, None]+c_sideL*wl[:, None]+c_sideR*wr[:, None])/W[:, None]
valid = (wf+wb+wl+wr) > 2e-3
ed0 = np.empty(len(me.edges)*2, np.int32); me.edges.foreach_get('vertices', ed0); ed0 = ed0.reshape(-1, 2)
ja, jb = np.concatenate([ed0[:, 0], ed0[:, 1]]), np.concatenate([ed0[:, 1], ed0[:, 0]])
for _ in range(60):
    if valid.all(): break
    acc = np.zeros_like(col); cnt = np.zeros(n, np.float32)
    ok = valid[jb] & ~valid[ja]
    np.add.at(acc, ja[ok], col[jb[ok]]); np.add.at(cnt, ja[ok], 1)
    nv = cnt > 0; col[nv] = acc[nv]/cnt[nv, None]; valid = valid | nv
# lisciatura che preserva i bordi: toglie le "pennellate" dei disegni di riferimento (ombre dipinte), tiene netti i confini giacca/jeans/pelle
ed = np.empty(len(me.edges)*2, np.int32); me.edges.foreach_get('vertices', ed); ed = ed.reshape(-1, 2)
ia, ib = np.concatenate([ed[:, 0], ed[:, 1]]), np.concatenate([ed[:, 1], ed[:, 0]])
SIG = float(a[6]) if len(a) > 6 else 0.07
for _ in range(int(a[7]) if len(a) > 7 else 30):
    wgt = np.exp(-((col[ia]-col[ib])**2).sum(1)/(2*SIG**2)).astype(np.float32)
    acc = np.zeros_like(col); ws = np.ones(n, np.float32)
    np.add.at(acc, ia, col[ib]*wgt[:, None]); np.add.at(ws, ia, wgt)
    col = (col + acc)/ws[:, None]
# passaggio "giocattolo": poche zone di colore (k-means) e il colore di ogni vertice si avvicina al centro della sua zona
K = int(a[8]) if len(a) > 8 else 10; MIX = float(a[9]) if len(a) > 9 else 0.7
rng = np.random.default_rng(3); cen = col[rng.choice(n, K, replace=False)].copy()
sub = col[rng.choice(n, min(n, 60000), replace=False)]
for _ in range(15):
    lab = ((sub[:, None, :]-cen[None])**2).sum(2).argmin(1)
    for k in range(K):
        if (lab == k).any(): cen[k] = sub[lab == k].mean(0)
lab = np.empty(n, np.int32)
for i0 in range(0, n, 50000): lab[i0:i0+50000] = ((col[i0:i0+50000, None, :]-cen[None])**2).sum(2).argmin(1)
# regola geometrica: sulle gambe (sotto i fianchi, lontano dalle mani) il colore pelle non e' ammesso -> colore jeans; poi filtro a maggioranza
skin_c = np.array([(c[0] > c[2]*1.25) and (c.mean() > 0.35) for c in cen])
leg = (z > 0.07) & (z < 0.32) & (x > 0.21) & (x < 0.79)
mid = (z > 0.10) & (z < 0.30) & (x > 0.3) & (x < 0.7)
jeans_c = np.bincount(lab[mid], minlength=K).argmax()
lab[leg & skin_c[lab]] = jeans_c
if len(a) > 10 and a[10] == 'indigo': cen[jeans_c] = np.array([0.12, 0.16, 0.28])   # jeans: indaco scuro come nel disegno
for _ in range(4):
    cnt = np.zeros((n, K), np.float32); np.add.at(cnt, (ia, lab[ib]), 1); cnt[np.arange(n), lab] += 1.5
    lab = cnt.argmax(1).astype(np.int32)
col = col*(1-MIX) + cen[lab]*MIX
col = np.where(col <= 0.04045, col/12.92, ((col+0.055)/1.055)**2.4)     # le immagini sono sRGB, l'attributo colore e il glTF sono lineari: senza questo i colori escono sbiaditi
rgba = np.concatenate([col, np.ones((n, 1), np.float32)], axis=1)
if 'Col' in me.color_attributes: me.color_attributes.remove(me.color_attributes['Col'])
ca = me.color_attributes.new('Col', 'FLOAT_COLOR', 'POINT')
ca.data.foreach_set('color', rgba.reshape(-1))
# alleggerisci
tris = len(me.polygons)
m = ob.modifiers.new('dec', 'DECIMATE'); m.ratio = min(1.0, TARGET/max(tris, 1))
bpy.ops.object.modifier_apply(modifier='dec')
print('triangoli', tris, '->', len(ob.data.polygons))
# materiale che usa il colore vertice
mat = bpy.data.materials.new('toy'); mat.use_nodes = True
nt = mat.node_tree
bsdf = next(nd for nd in nt.nodes if nd.type == 'BSDF_PRINCIPLED')
vc = nt.nodes.new('ShaderNodeVertexColor'); vc.layer_name = 'Col'
nt.links.new(vc.outputs['Color'], bsdf.inputs['Base Color'])
bsdf.inputs['Roughness'].default_value = 0.8
ob.data.materials.clear(); ob.data.materials.append(mat)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_vertex_color='ACTIVE', export_all_vertex_colors=True, export_active_vertex_color_when_no_material=True)
print('salvato', OUT)
