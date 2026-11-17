"""Dipinge un personaggio "giocattolo" pezzo per pezzo: un colore piatto per parte (giacca, maglia, jeans, stivali, mani, pelle, capelli, occhiali).
Parte da un GLB con colori per vertice (anche rumorosi, es. dal render texturizzato di Hunyuan): le parti si riconoscono dalla POSIZIONE sul corpo (altezza/larghezza) piu' un filtro di maggioranza,
e il colore di ogni parte e' la mediana dei colori di riferimento di quella parte. Uso: blender -b -P blender_paint_parts.py -- in.glb out.glb
"""
import bpy, sys, numpy as np, mathutils
IN, OUT = sys.argv[sys.argv.index('--')+1:][:2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=IN)
ob = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
bpy.context.view_layer.objects.active = ob; ob.select_set(True); bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
me = ob.data; n = len(me.vertices)
ca = me.color_attributes.get('Col') or me.color_attributes[0]
P = np.empty(n*3, np.float32); me.vertices.foreach_get('co', P); P = P.reshape(-1, 3)
m_ = len(ca.data); C0 = np.empty(m_*4, np.float32); ca.data.foreach_get('color', C0); C0 = C0.reshape(-1, 4)
li = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', li)
if ca.domain == 'CORNER': C = np.zeros((n, 4), np.float32); C[li] = C0
else: C = C0.copy()
col = C[:, :3]
mn, mx = P.min(0), P.max(0); z = (P[:, 2]-mn[2])/(mx[2]-mn[2]); x = (P[:, 0]-mn[0])/(mx[0]-mn[0]); y = (P[:, 1]-mn[1])/(mx[1]-mn[1])
lum = col @ np.array([0.2126, 0.7152, 0.0722], np.float32)           # luminanza lineare
ymid = np.median(y)
# ---- etichette per posizione + colore
BOOT, JEANS, HAND, TEE, JACKET, SKIN, HAIR, GLASS = range(8)
lab = np.full(n, JACKET, np.int32)
head = (z > 0.69) | ((z > 0.665) & (y < np.median(y)) & (np.abs(x-0.5) < 0.16))     # testa; il colletto/le spalle restano giacca
lab[(z <= 0.09)] = BOOT
lab[(z > 0.09) & (z <= 0.33)] = JEANS
hands = (z > 0.24) & (z < 0.36) & ((x < 0.22) | (x > 0.78))
lab[hands] = HAND
torso = (z > 0.33) & (z <= 0.665)
lab[torso] = JACKET
lab[torso & (np.abs(x-0.5) < 0.105) & (y < ymid) & (lum < 0.02)] = TEE      # maglia: scura, al centro, sul davanti
face_z = head
lab[face_z] = HAIR
skin_like = (lum > 0.26)
lab[face_z & skin_like & (z < 0.93)] = SKIN
lab[face_z & (z >= 0.795) & (z <= 0.85) & (y < ymid) & (np.abs(x-0.5) < 0.30)] = GLASS
lab[face_z & (z < 0.835) & (y < ymid) & (np.abs(x-0.5) < 0.055)] = SKIN       # il naso resta pelle      # occhiali: scuri, davanti, all'altezza degli occhi
lab[face_z & (z <= 0.775) & (y < ymid) & (np.abs(x-0.5) < 0.28)] = SKIN                          # mento/guance/naso: sempre pelle
# ---- filtro a maggioranza sui vicini (toglie macchie isolate)
kd = mathutils.kdtree.KDTree(n)
for i in range(n): kd.insert(P[i], i)
kd.balance()
nb = np.array([[j for (_, j, _) in kd.find_n(P[i], 14)] for i in range(n)], np.int32)
for _ in range(3):
    new = np.empty(n, np.int32)
    for i in range(n):
        new[i] = np.bincount(lab[nb[i]], minlength=8).argmax()
    keep = (lab == GLASS) | (new == GLASS)       # gli occhiali sono sottili: non li "mangia" la maggioranza
    lab = np.where((lab == GLASS), GLASS, new)
# ---- palette: mediana dei colori di riferimento di ogni parte (poi in lineare gia')
pal = {}
for k, nm in enumerate(['stivali', 'jeans', 'mani', 'maglia', 'giacca', 'pelle', 'capelli', 'occhiali']):
    sel = lab == k
    pal[k] = np.median(col[sel], axis=0) if sel.sum() > 50 else np.array([0.5, 0.5, 0.5], np.float32)
    print('PARTE', nm, int(sel.sum()), [round(float(v), 3) for v in pal[k]])
pal[HAIR] = np.array([0.065, 0.032, 0.016], np.float32)     # castano scuro (dal render di Hunyuan)
pal[HAND] = pal[SKIN]                       # mani = stessa pelle del viso
pal[GLASS] = np.array([0.012, 0.012, 0.014], np.float32)
pal[TEE] = np.minimum(pal[TEE], 0.03)
new_col = np.stack([pal[k] for k in lab]).astype(np.float32)
Cn = np.concatenate([new_col, np.ones((n, 1), np.float32)], axis=1)
out_ = (Cn[li] if ca.domain == 'CORNER' else Cn).astype(np.float32); ca.data.foreach_set('color', out_.reshape(-1))
mat = bpy.data.materials.new('toy'); mat.use_nodes = True; nt = mat.node_tree
bsdf = next(nd for nd in nt.nodes if nd.type == 'BSDF_PRINCIPLED')
vc = nt.nodes.new('ShaderNodeVertexColor'); vc.layer_name = ca.name; nt.links.new(vc.outputs['Color'], bsdf.inputs['Base Color'])
bsdf.inputs['Roughness'].default_value = 0.85; bsdf.inputs['Metallic'].default_value = 0.0
me.materials.clear(); me.materials.append(mat)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_vertex_color='ACTIVE', export_all_vertex_colors=True, export_active_vertex_color_when_no_material=True)
print('salvato', OUT)
