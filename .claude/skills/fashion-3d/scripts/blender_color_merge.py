"""Unisce due colorazioni: parte da un GLB con colori per vertice (es. proiezione dalle foto) e sostituisce SOLO il corpo (giacca/maglia/jeans) con i colori di un GLB texturizzato (Hunyuan3D). Testa, mani e stivali restano come nella base.
Uso: blender -b -P blender_color_merge.py -- base_colori.glb texturizzato.glb out.glb
"""
import bpy, bmesh, sys, numpy as np, mathutils
from mathutils import bvhtree, interpolate
B, T, OUT = sys.argv[sys.argv.index('--')+1:][:3]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=T)
ot = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
bpy.context.view_layer.objects.active = ot; ot.select_set(True); bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bm = bmesh.new(); bm.from_mesh(ot.data)
kill = [f for f in bm.faces if any(abs(v.co.x) > 0.55 or abs(v.co.y) > 0.45 for v in f.verts) or max(v.co.z for v in f.verts) < -0.395
        or (max(v.co.z for v in f.verts) < -0.36 and f.normal.z > 0.6 and any(abs(v.co.x) > 0.2 for v in f.verts))]
bmesh.ops.delete(bm, geom=kill, context='FACES'); bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
bmesh.ops.triangulate(bm, faces=bm.faces[:]); bm.faces.ensure_lookup_table(); bm.verts.ensure_lookup_table()
uvl = bm.loops.layers.uv.active
tv = np.array([v.co[:] for v in bm.verts]); tmn, tmx = tv.min(0), tv.max(0)
tree = bvhtree.BVHTree.FromBMesh(bm)
img = next(n.image for m in ot.data.materials for n in m.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image)
iw, ih = img.size; px = np.array(img.pixels[:], np.float32).reshape(ih, iw, img.channels)[:, :, :3]
bpy.ops.import_scene.gltf(filepath=B)
ob = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o != ot][0]
bpy.context.view_layer.objects.active = ob; ob.select_set(True); bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
me = ob.data; n = len(me.vertices)
P = np.empty(n*3, np.float32); me.vertices.foreach_get('co', P); P = P.reshape(-1, 3)
ca = me.color_attributes.get('Col') or me.color_attributes[0]
m_ = len(ca.data); C0 = np.empty(m_*4, np.float32); ca.data.foreach_get('color', C0); C0 = C0.reshape(-1, 4)
if ca.domain == 'CORNER':                       # colori per angolo (glTF importato): li porto per vertice e poi li riscrivo sugli angoli
    li = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', li)
    C = np.zeros((n, 4), np.float32); C[li] = C0
else:
    C = C0.copy()
wmn, wmx = P.min(0), P.max(0); s = (wmx[2]-wmn[2])/(tmx[2]-tmn[2]); wc = (wmn+wmx)/2; tc = (tmn+tmx)/2
z = (P[:, 2]-wmn[2])/(wmx[2]-wmn[2]); x = (P[:, 0]-wmn[0])/(wmx[0]-wmn[0])
hands = (z > 0.24) & (z < 0.36) & ((x < 0.22) | (x > 0.78))
body = (z > 0.09) & (z < 0.655) & ~hands
cnt = 0
for i in np.where(body)[0]:
    q = mathutils.Vector((tc[0]+(P[i, 0]-wc[0])/s, tc[1]+(P[i, 1]-wc[1])/s, tmn[2]+(P[i, 2]-wmn[2])/s))
    loc, nor, idx, dist = tree.find_nearest(q)
    f = bm.faces[idx]; wgt = interpolate.poly_3d_calc([l.vert.co for l in f.loops], loc)
    u = sum(w_*l[uvl].uv[0] for w_, l in zip(wgt, f.loops)); v = sum(w_*l[uvl].uv[1] for w_, l in zip(wgt, f.loops))
    c = px[min(ih-1, max(0, int(v*(ih-1)))), min(iw-1, max(0, int(u*(iw-1))))]
    c = np.where(c <= 0.04045, c/12.92, ((c+0.055)/1.055)**2.4)
    C[i, :3] = c; cnt += 1
print('vertici corpo sostituiti', cnt, 'di', n)
out_ = (C[li] if ca.domain == 'CORNER' else C).astype(np.float32); ca.data.foreach_set('color', out_.reshape(-1))
bpy.data.objects.remove(ot, do_unlink=True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_vertex_color='ACTIVE', export_all_vertex_colors=True, export_active_vertex_color_when_no_material=True)
print('salvato', OUT)
