"""Aggiunge una MASCELLA che si apre a un GLB rigged (es. il pupazzo Tripo con scheletro Mixamo), come shape key `jawOpen` pilotabile dal motore.
Il volto del pupazzo non ha labbra (solo una piega scolpita): lo script (1) suddivide la zona bocca, (2) assegna le facce a forma di lente lungo la piega a un materiale SCURO ("mouth_dark"),
(3) crea la shape key `jawOpen`: i vertici sotto la piega ruotano attorno alla cerniera (davanti alle orecchie), con pesi che sfumano sulle guance; le facce scure si allargano e
la loro parte centrale rientra in profondita' (una tasca). La posa di riposo ha la mascella gia' chiusa: le facce scure si riducono a una linea sottilissima. Niente buchi nella mesh.
Uso: blender -b -P blender_add_jaw.py -- in.glb out.glb [angolo_gradi=9]
Le coordinate (centro bocca, cerniera, rotazione del viso) sono misurate sul pupazzo di Jacopo (Tripo, 17/11/2026): per un altro modello vanno rimisurate (costanti qui sotto).
"""
import bpy, bmesh, sys, math, mathutils
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
IN, OUT = a[0], a[1]; ANG = math.radians(float(a[2])) if len(a) > 2 else math.radians(9.0)

# ---- misure sul modello (metri, Blender: il pupazzo guarda verso -Y, viso girato di ~16 gradi verso +X)
YAW = math.radians(15.6)
L = Vector((math.cos(YAW), math.sin(YAW), 0.0))                  # asse laterale del viso (asse della cerniera)
F = Vector((math.sin(YAW), -math.cos(YAW), 0.0))                 # avanti del viso
MOUTH = Vector((0.0215, -0.0218, 0.775))                           # centro della piega della bocca, sulla superficie
HINGE = Vector((0.015, 0.135, 0.783))                            # cerniera: davanti alle orecchie
W = 0.022                                                        # mezza larghezza della fessura
BAND = 0.0050                                                    # spessore della fessura a mascella aperta zero (chiusa dalla posa di riposo)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=IN)
sc = bpy.context.scene
mesh = next(o for o in sc.objects if o.type == 'MESH'); arm = next(o for o in sc.objects if o.type == 'ARMATURE')
bpy.context.view_layer.objects.active = mesh
mw = mesh.matrix_world
assert (mw.to_translation().length < 1e-6), 'mesh non in origine'
def loc(v): return v - MOUTH
def uh(p):                                                       # (u lateral, h altezza)
    d = p - MOUTH; return d.dot(L), p.z

orig = mesh.copy(); orig.data = mesh.data.copy(); sc.collection.objects.link(orig); orig.modifiers.clear()      # copia originale (per le normali)
bpy.context.view_layer.objects.active = mesh
# ---- 1) suddividi la zona bocca
me = mesh.data
bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
box = lambda p: abs((p - MOUTH).dot(L)) < 0.030 and abs(p.z - MOUTH.z) < 0.010 and (p - MOUTH).dot(F) > -0.03
sel = [f for f in bm.faces if box(f.calc_center_median())]
edges = list({e for f in sel for e in f.edges})
bmesh.ops.subdivide_edges(bm, edges=edges, cuts=5, use_grid_fill=True)
bm.faces.ensure_lookup_table()
print('facce nella zona bocca', len(sel), '-> facce totali', len(bm.faces))

# ---- 2) fessura a lente
def lens(p):
    u, h = uh(p); r = u / W
    if abs(r) > 1: return False
    return abs(h - MOUTH.z) <= 0.0004 + BAND * 0.5 * (1 - r * r)
dark = [f for f in bm.faces if lens(f.calc_center_median()) and f.normal.dot(F) > 0.2]
for f in dark: f.material_index = 1
print('facce scure della bocca', len(dark))
bm.to_mesh(me); bm.free(); me.update()
# normali: il pupazzo e' liscio grazie a NORMALI PERSONALIZZATE (senza, la geometria a faccette si vede); l'operazione sulla bocca le perde: le ritrasferisco dalla copia originale (prima delle shape keys)
mod = mesh.modifiers.new('nrm', 'DATA_TRANSFER'); mod.object = orig; mod.use_loop_data = True; mod.data_types_loops = {'CUSTOM_NORMAL'}; mod.loop_mapping = 'POLYINTERP_NEAREST'
bpy.context.view_layer.objects.active = mesh
try: bpy.ops.object.modifier_move_to_index(modifier='nrm', index=0)
except Exception as e_: print('move modifier:', e_)
bpy.ops.object.modifier_apply(modifier='nrm')
bpy.data.objects.remove(orig, do_unlink=True)

# ---- 3) pesi della mascella (0..1) per ogni vertice
sm = lambda x: (lambda t: t * t * (3 - 2 * t))(max(0.0, min(1.0, x)))
def jaw_w(p):
    u, h = uh(p); au = abs(u)
    side = min(1.0, max(0.0, (au - W) / 0.02))
    zt = MOUTH.z + 0.012 * side                                    # sui lati la soglia sale poco: le guance seguono un po'
    width = 0.0025 + 0.012 * side
    down = sm((zt + 0.0025 - p.z) / (2 * width))                   # 1 sotto la piega, 0 sopra
    lat = sm((0.075 - au) / 0.030)                                 # le guance alte/ai lati restano ferme
    neck = sm((p.z - 0.660) / 0.035)                               # il collo non si muove
    corner = math.sqrt(max(0.0, 1.0 - (au / W) ** 2)) if au < W else 0.0
    near = 1.0 - sm((MOUTH.z - 0.003 - p.z) / 0.012)                # 1 vicino al bordo basso della fessura, 0 piu' giu' (mento)
    m = 1.0 - (1.0 - corner) * near                                # gli angoli della bocca si muovono meno del centro: bocca ovale
    return down * lat * neck * m
def rot_about(p, ang):
    r = p - HINGE; c, s = math.cos(ang), math.sin(ang)
    return HINGE + r * c + L.cross(r) * s + L * (L.dot(r)) * (1 - c)

verts = me.vertices
W_ = [jaw_w(v.co.copy()) for v in verts]
# materiale scuro (slot 1) creato prima di salvare
mat = bpy.data.materials.new('mouth_dark'); mat.use_nodes = True
bs = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'); bs.inputs['Base Color'].default_value = (0.015, 0.006, 0.006, 1); bs.inputs['Roughness'].default_value = 1.0
if len(me.materials) < 2: me.materials.append(mat)
# posa di riposo: mascella chiusa (ruota di -delta, cosi' il bordo basso della fessura sale e tocca il bordo alto)
dist = (MOUTH - HINGE).length
DELTA = BAND / dist
for v, w_ in zip(verts, W_):
    if w_ > 1e-4: v.co = rot_about(v.co.copy(), -DELTA * w_)
me.update()
print('mascella: vertici mossi', sum(1 for w_ in W_ if w_ > 1e-4), 'delta gradi', math.degrees(DELTA))

# ---- 4) shape keys
mesh.shape_key_add(name='Basis', from_mix=False)
sk = mesh.shape_key_add(name='jawOpen', from_mix=False)
for v, w_ in zip(verts, W_):
    if w_ > 1e-4:
        q = rot_about(v.co.copy(), (ANG + DELTA) * w_)
        u_, h_ = uh(v.co)
        if 0.02 < w_ < 0.98 and abs(u_) < W:                       # interno della fessura: la tasca rientra in profondita'
            q = q - F * (0.012 * math.sin(math.pi * (1 - w_)) * (1 - (u_ / W) ** 2) ** 0.5)
        sk.data[v.index].co = q
sk.value = 0.0

print('vertici', len(mesh.data.vertices), 'shape keys', [k.name for k in mesh.data.shape_keys.key_blocks])

bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_animations=True, export_skins=True, export_morph=True, export_image_format='JPEG', export_jpeg_quality=88)
print('salvato', OUT)
