"""Dipinge un personaggio "giocattolo" pezzo per pezzo con confini NETTI: ogni triangolo ha UN colore piatto (giacca, maglia, jeans, stivali, mani, pelle, capelli, occhiali).
Le parti si decidono con regole geometriche sulla posizione del baricentro del triangolo (altezza z, larghezza x, fronte/retro y, tutte normalizzate sul personaggio); i colori sono la mediana dei colori di
riferimento (GLB con colori per vertice, anche rumorosi) della parte, tranne capelli/occhiali impostati a mano. Uso: blender -b -P blender_paint_parts.py -- in.glb out.glb [debug]
"""
import bpy, sys, numpy as np
a = sys.argv[sys.argv.index('--')+1:]
IN, OUT = a[:2]; DEBUG = len(a) > 2 and a[2] == 'debug'
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=IN)
ob = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
bpy.context.view_layer.objects.active = ob; ob.select_set(True); bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
me = ob.data; n = len(me.vertices)
ca = me.color_attributes.get('Col') or me.color_attributes[0]
P = np.empty(n*3, np.float32); me.vertices.foreach_get('co', P); P = P.reshape(-1, 3)
nl = len(me.loops); li = np.empty(nl, np.int32); me.loops.foreach_get('vertex_index', li)
C0 = np.empty(len(ca.data)*4, np.float32); ca.data.foreach_get('color', C0); C0 = C0.reshape(-1, 4)
Ccorner = C0[:, :3] if ca.domain == 'CORNER' else C0[li, :3]
npoly = len(me.polygons); assert nl == npoly*3, 'serve una mesh di soli triangoli'
tri = li.reshape(-1, 3)
mn, mx = P.min(0), P.max(0)
G = P[tri].mean(1)                                   # baricentri
z = (G[:, 2]-mn[2])/(mx[2]-mn[2]); x = (G[:, 0]-mn[0])/(mx[0]-mn[0]); y = (G[:, 1]-mn[1])/(mx[1]-mn[1])
ymid = np.median(y); front = y < ymid; cx = np.abs(x-0.5)
Cface = Ccorner.reshape(-1, 3, 3).mean(1)
lum = Cface @ np.array([0.2126, 0.7152, 0.0722], np.float32)
BOOT, JEANS, HAND, TEE, JACKET, SKIN, HAIR, GLASS = range(8)
lab = np.full(npoly, JACKET, np.int32)
# ---- corpo
lab[z < 0.09] = BOOT
lab[(z >= 0.09) & (z < 0.345) & (x >= 0.17) & (x <= 0.83)] = JEANS                 # i jeans arrivano fino alla vita (orlo della giacca), solo nella larghezza delle gambe
lab[(z >= 0.255) & (z < 0.335) & ((x < 0.19) | (x > 0.81))] = HAND       # mani: solo sotto il polsino
lab[(z >= 0.345) & front & (cx < 0.098)] = TEE            # maglia: sotto il colletto, solo sul davanti (bordo geometrico, dritto)
# ---- testa (solo geometria)
head = (z >= 0.69) | ((z >= 0.675) & front & (cx < 0.15))
lab[head] = SKIN
hair = head & (((z >= 0.915 - 0.25*cx) & front) | ((z >= 0.80) & (cx >= 0.27)) | ((~front) & (z >= 0.72)) | (z >= 0.95))      # attaccatura a V: piu' alta al centro, piu' bassa ai lati
lab[hair] = HAIR
glass = head & front & (z >= 0.795) & (z <= 0.85) & (cx < 0.30) & ~((cx < 0.045) & (z < 0.835))
lab[glass] = GLASS
# ---- palette: mediana dei colori di riferimento per parte
names = ['stivali', 'jeans', 'mani', 'maglia', 'giacca', 'pelle', 'capelli', 'occhiali']
pal = {}
for k, nm in enumerate(names):
    sel = lab == k
    pal[k] = np.median(Cface[sel], axis=0) if sel.sum() > 30 else np.array([0.5, 0.5, 0.5], np.float32)
    print('PARTE', nm, int(sel.sum()), [round(float(v), 3) for v in pal[k]])
pal[SKIN] = pal[HAND]          # pelle di viso e mani = colore di riferimento delle mani (pulito)
pal[HAIR] = np.array([0.065, 0.032, 0.016], np.float32)       # castano scuro (dal render di Hunyuan)
pal[GLASS] = np.array([0.012, 0.012, 0.014], np.float32)
pal[TEE] = np.minimum(pal[TEE], 0.03)
if DEBUG:
    dbg = {BOOT: (0.5, 0, 0.5), JEANS: (0, 0, 1), HAND: (1, 0.5, 0), TEE: (0, 0, 0), JACKET: (0, 0.7, 0), SKIN: (1, 0.85, 0.7), HAIR: (0.45, 0.2, 0.05), GLASS: (1, 0, 0)}
    for k_, v_ in dbg.items(): pal[k_] = np.array(v_, np.float32)
face_col = np.stack([pal[k] for k in lab]).astype(np.float32)
corner = np.repeat(face_col, 3, axis=0)                          # 3 angoli per triangolo, stesso colore
cc = np.concatenate([corner, np.ones((nl, 1), np.float32)], axis=1)
if ca.domain == 'CORNER':
    ca.data.foreach_set('color', cc.reshape(-1))
else:                                                             # colori per vertice: porta il colore di ogni triangolo ai suoi vertici (ultimo vince)
    Cv = np.zeros((n, 4), np.float32); Cv[li] = cc; ca.data.foreach_set('color', Cv.reshape(-1))
mat = bpy.data.materials.new('toy'); mat.use_nodes = True; nt = mat.node_tree
bsdf = next(nd for nd in nt.nodes if nd.type == 'BSDF_PRINCIPLED')
vc = nt.nodes.new('ShaderNodeVertexColor'); vc.layer_name = ca.name; nt.links.new(vc.outputs['Color'], bsdf.inputs['Base Color'])
bsdf.inputs['Roughness'].default_value = 0.85; bsdf.inputs['Metallic'].default_value = 0.0
me.materials.clear(); me.materials.append(mat)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_vertex_color='ACTIVE', export_all_vertex_colors=True, export_active_vertex_color_when_no_material=True)
print('salvato', OUT)
