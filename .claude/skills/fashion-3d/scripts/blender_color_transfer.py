"""Trasferisce i colori di un GLB texturizzato (es. Hunyuan3D-2.1, 40k facce) su una forma dettagliata (GLB bianco, 400k facce): per ogni vertice, il punto piu' vicino sulla superficie texturizzata -> UV -> pixel. Poi alleggerisce e esporta GLB con colori per vertice.
Uso: blender -b -P blender_color_transfer.py -- bianco.glb texturizzato.glb out.glb [triangoli_target]
"""
import bpy, bmesh, sys, numpy as np, mathutils
from mathutils import bvhtree, interpolate
W, T, OUT = sys.argv[sys.argv.index('--')+1:][:3]
TARGET = int(sys.argv[sys.argv.index('--')+4]) if len(sys.argv) > sys.argv.index('--')+4 else 70000
bpy.ops.wm.read_factory_settings(use_empty=True)
# --- texturizzato: toglie la piattaforma, triangola, BVH + UV
bpy.ops.import_scene.gltf(filepath=T)
ot = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
bpy.context.view_layer.objects.active = ot; ot.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bm = bmesh.new(); bm.from_mesh(ot.data)
kill = [f for f in bm.faces if any(abs(v.co.x) > 0.55 or abs(v.co.y) > 0.45 for v in f.verts) or max(v.co.z for v in f.verts) < -0.395
        or (max(v.co.z for v in f.verts) < -0.36 and f.normal.z > 0.6 and any(abs(v.co.x) > 0.2 for v in f.verts))]
bmesh.ops.delete(bm, geom=kill, context='FACES')
bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
bmesh.ops.triangulate(bm, faces=bm.faces[:])
bm.faces.ensure_lookup_table(); bm.verts.ensure_lookup_table()
uvl = bm.loops.layers.uv.active
tv = np.array([v.co[:] for v in bm.verts]); tmn, tmx = tv.min(0), tv.max(0)
tree = bvhtree.BVHTree.FromBMesh(bm)
img = next(n.image for m in ot.data.materials for n in m.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image)
iw, ih = img.size; px = np.array(img.pixels[:], np.float32).reshape(ih, iw, img.channels)[:, :, :3]
print('texture', iw, ih, 'facce texturizzato', len(bm.faces))
# --- forma dettagliata
bpy.ops.import_scene.gltf(filepath=W)
ow = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o != ot][0]
bpy.context.view_layer.objects.active = ow; ow.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
me = ow.data; n = len(me.vertices)
P = np.empty(n*3, np.float32); me.vertices.foreach_get('co', P); P = P.reshape(-1, 3)
wmn, wmx = P.min(0), P.max(0)
s = (wmx[2]-wmn[2])/(tmx[2]-tmn[2]); wc = (wmn+wmx)/2; tc = (tmn+tmx)/2
print('scala', round(float(s), 3))
Q = np.empty_like(P)
Q[:, 0] = tc[0]+(P[:, 0]-wc[0])/s; Q[:, 1] = tc[1]+(P[:, 1]-wc[1])/s; Q[:, 2] = tmn[2]+(P[:, 2]-wmn[2])/s
col = np.empty((n, 3), np.float32)
for i in range(n):
    loc, nor, idx, dist = tree.find_nearest(mathutils.Vector(Q[i]))
    f = bm.faces[idx]; vs = [l.vert.co for l in f.loops]
    wgt = interpolate.poly_3d_calc(vs, loc)
    u = sum(w_*l[uvl].uv[0] for w_, l in zip(wgt, f.loops)); v = sum(w_*l[uvl].uv[1] for w_, l in zip(wgt, f.loops))
    col[i] = px[min(ih-1, max(0, int(v*(ih-1)))), min(iw-1, max(0, int(u*(iw-1))))]
col = np.where(col <= 0.04045, col/12.92, ((col+0.055)/1.055)**2.4)      # sRGB -> lineare (il glTF colori vertice e' lineare)
rgba = np.concatenate([col, np.ones((n, 1), np.float32)], axis=1)
ca = me.color_attributes.new('Col', 'FLOAT_COLOR', 'POINT'); ca.data.foreach_set('color', rgba.reshape(-1))
bpy.data.objects.remove(ot, do_unlink=True)
tris = len(me.polygons)
bpy.context.view_layer.objects.active = ow
m = ow.modifiers.new('dec', 'DECIMATE'); m.ratio = min(1.0, TARGET/max(tris, 1)); bpy.ops.object.modifier_apply(modifier='dec')
for p in ow.data.polygons: p.use_smooth = True
print('triangoli', tris, '->', len(ow.data.polygons))
mat = bpy.data.materials.new('toy'); mat.use_nodes = True; nt = mat.node_tree
bsdf = next(nd for nd in nt.nodes if nd.type == 'BSDF_PRINCIPLED')
vc = nt.nodes.new('ShaderNodeVertexColor'); vc.layer_name = 'Col'; nt.links.new(vc.outputs['Color'], bsdf.inputs['Base Color'])
bsdf.inputs['Roughness'].default_value = 0.9; bsdf.inputs['Metallic'].default_value = 0.0
ow.data.materials.clear(); ow.data.materials.append(mat)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_vertex_color='ACTIVE', export_all_vertex_colors=True, export_active_vertex_color_when_no_material=True)
print('salvato', OUT)
