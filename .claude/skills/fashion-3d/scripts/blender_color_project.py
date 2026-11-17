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
wf *= k_f; wb *= k_b; wl *= k_l; wr *= k_r
# pesi minimi cosi' i vertici dove tutti i campioni sono scartati restano colorati
wf += 1e-3*k_f; wb += 1e-3*k_b; wl += 1e-3*k_l; wr += 1e-3*k_r
W = wf+wb+wl+wr+1e-6
col = (c_front*wf[:, None]+c_back*wb[:, None]+c_sideL*wl[:, None]+c_sideR*wr[:, None])/W[:, None]
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
