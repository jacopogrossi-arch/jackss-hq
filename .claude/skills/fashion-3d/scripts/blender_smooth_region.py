"""Ammorbidisce una zona "a pixel" della texture colore (es. il collo di un pupazzo Tripo): trova le facce in una fascia di altezza, prende il rettangolo UV che le contiene,
e sfuoca SOLO i pixel color pelle dentro quel rettangolo. Mesh, ossa, animazioni e shape keys restano come sono.
Uso: blender -b -P blender_smooth_region.py -- in.glb out.glb zmin zmax [raggio_px=6]
"""
import bpy, sys, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
IN, OUT, ZMIN, ZMAX = a[0], a[1], float(a[2]), float(a[3]); R = int(a[4]) if len(a) > 4 else 6
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=IN)
mesh = max([o for o in bpy.context.scene.objects if o.type == 'MESH'], key=lambda o: len(o.data.polygons))
me = mesh.data; uv = me.uv_layers.active.data
mat = me.materials[0]; bsdf = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
img = bsdf.inputs['Base Color'].links[0].from_node.image
W, H = img.size; px = np.array(img.pixels[:], dtype=np.float32).reshape(H, W, 4)
mask = np.zeros((H, W), dtype=bool)
def raster(tri):                                                    # riempie un triangolo UV nella maschera (coordinate barycentriche)
    P = np.array([[u * W, v * H] for u, v in tri]); xa, ya = int(P[:, 0].min()), int(P[:, 1].min()); xb, yb = int(P[:, 0].max()) + 1, int(P[:, 1].max()) + 1
    xa, ya, xb, yb = max(0, xa), max(0, ya), min(W, xb), min(H, yb)
    if xb <= xa or yb <= ya: return
    gx, gy = np.meshgrid(np.arange(xa, xb) + 0.5, np.arange(ya, yb) + 0.5)
    d = (P[1, 1] - P[2, 1]) * (P[0, 0] - P[2, 0]) + (P[2, 0] - P[1, 0]) * (P[0, 1] - P[2, 1])
    if abs(d) < 1e-9: return
    l1 = ((P[1, 1] - P[2, 1]) * (gx - P[2, 0]) + (P[2, 0] - P[1, 0]) * (gy - P[2, 1])) / d
    l2 = ((P[2, 1] - P[0, 1]) * (gx - P[2, 0]) + (P[0, 0] - P[2, 0]) * (gy - P[2, 1])) / d
    mask[ya:yb, xa:xb] |= (l1 >= -0.02) & (l2 >= -0.02) & ((1 - l1 - l2) >= -0.02)
nf = 0
for p in me.polygons:
    zs = [me.vertices[i].co.z for i in p.vertices]
    if min(zs) >= ZMIN and max(zs) <= ZMAX and p.material_index == 0:
        L = [tuple(uv[li].uv) for li in p.loop_indices]
        for j in range(1, len(L) - 1): raster([L[0], L[j], L[j + 1]])
        nf += 1
print('facce nella fascia', nf, 'pixel di texture coperti', int(mask.sum()))
k = np.ones(2 * R + 1) / (2 * R + 1)
def blur(ch):
    t = np.pad(ch, ((R, R), (R, R)), mode='edge')
    t = np.apply_along_axis(lambda r: np.convolve(r, k, mode='valid'), 1, t)
    return np.apply_along_axis(lambda r: np.convolve(r, k, mode='valid'), 0, t)
rgb = px[..., :3]
skin = (rgb[..., 0] > rgb[..., 1]) & (rgb[..., 1] > rgb[..., 2]) & ((rgb[..., 0] - rgb[..., 2]) > 0.12) & (rgb[..., 0] > 0.35) & mask
print('pixel pelle da ammorbidire', int(skin.sum()))
ys, xs = np.where(mask); y0, y1, x0, x1 = max(0, ys.min() - R), min(H, ys.max() + R + 1), max(0, xs.min() - R), min(W, xs.max() + R + 1)
sub = rgb[y0:y1, x0:x1]; sk = skin[y0:y1, x0:x1].astype(np.float32)
out = sub.copy()
for c in range(3):
    bnum = blur(sub[..., c] * sk); bden = blur(sk)
    bl = np.where(bden > 1e-3, bnum / np.maximum(bden, 1e-3), sub[..., c])
    out[..., c] = np.where(sk > 0, bl, sub[..., c])
px[y0:y1, x0:x1, :3] = out
img.pixels.foreach_set(px.ravel()); img.update(); img.pack()
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_animations=True, export_skins=True, export_morph=True, export_image_format='JPEG', export_jpeg_quality=92)
print('salvato', OUT)
