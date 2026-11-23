"""Layout della prova ibrida (23/11/2026): Jacopino giocattolo sul tavolo da taglio con foglio, matita e metro.
Uso: blender -b -P layout.py -- OUTDIR
Rende start.png (camera larga) e end.png (avvicinamento), 1080x1920, EEVEE. Unita' in metri, scala reale.
"""
import bpy, sys, math, os
from mathutils import Vector

OUT = sys.argv[sys.argv.index("--") + 1]
GLB = "D:/ClaudeCodeTest/social/short-03-tabellone/assets/jacopo-ps2-color.glb"
H = 0.22  # altezza di Jacopino (giocattolo)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def mat(name, rgb, rough=0.7, emit=None, strength=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = strength
    return m

def box(name, size, loc, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = size; o.data.materials.append(m); return o

# tavolo (piano a z=0) + tappetino verde con griglia
box("tavolo", (2.0, 2.0, 0.04), (0, -0.1, -0.02), mat("legno", (0.45, 0.22, 0.09), 0.55))
mm = mat("tappetino", (0.08, 0.32, 0.17), 0.8)
box("tappetino", (0.6, 0.6, 0.002), (0, -0.02, 0.001), mm)
for i in range(-6, 7):  # righe chiare della griglia
    box("rigaX%d" % i, (0.6, 0.0015, 0.0004), (0, 0.05 + i * 0.035, 0.0023), mat("riga", (0.6, 0.75, 0.6), 0.9))
    box("rigaY%d" % i, (0.0015, 0.45, 0.0004), (i * 0.045, 0.05, 0.0023), mat("riga2", (0.6, 0.75, 0.6), 0.9))

# parete di fondo con finestra di notte (fuori fuoco)
box("parete", (3, 0.05, 1.6), (0, 0.9, 0.6), mat("parete", (0.16, 0.08, 0.05), 0.9))
box("finestra", (0.7, 0.02, 0.5), (0.25, 0.87, 0.45), mat("notte", (0.02, 0.03, 0.08), 1, emit=(0.03, 0.05, 0.14), strength=1.0))
box("scaffale", (0.5, 0.25, 0.9), (-0.65, 0.75, 0.45), mat("scaffale", (0.6, 0.38, 0.18), 0.6))

# Jacopino (GLB vero), in piedi al centro un po' indietro, di fronte alla camera
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=GLB)
parts = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
bpy.ops.object.empty_add(location=(0, 0, 0)); root = bpy.context.object; root.name = "jacopino"
for o in [o for o in bpy.data.objects if o not in before and o.parent is None and o != root]:
    o.parent = root
bpy.context.view_layer.update()
pts = [o.matrix_world @ Vector(c) for o in parts for c in o.bound_box]
zmin = min(p.z for p in pts); zmax = max(p.z for p in pts)
cx = (min(p.x for p in pts) + max(p.x for p in pts)) / 2; cy = (min(p.y for p in pts) + max(p.y for p in pts)) / 2
s = H / (zmax - zmin)
root.scale = (s, s, s); root.location = (-cx * s, 0.12 - cy * s, -zmin * s)
# il GLB guarda verso -Y (camera): se guarda altrove lo correggo leggendo l'orientamento in render

# foglio A4 davanti a lui (lato camera), leggermente ruotato
box("foglio", (0.21, 0.297, 0.0008), (0.06, -0.06, 0.0035), mat("carta", (0.92, 0.9, 0.85), 0.9), rot=(0, 0, math.radians(-12)))
# matita gialla esagonale appoggiata sul foglio, quasi parallela al bordo camera
bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.0045, depth=0.17, location=(0.07, -0.1, 0.0085), rotation=(0, math.radians(90), math.radians(18)))
bpy.context.object.name = "matita"; bpy.context.object.data.materials.append(mat("giallo", (0.95, 0.7, 0.08), 0.5))
bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.0045, depth=0.018, location=(0.07 + 0.094 * math.cos(math.radians(18)), -0.1 + 0.094 * math.sin(math.radians(18)), 0.0085), rotation=(0, math.radians(90), math.radians(18)))
bpy.context.object.name = "punta"; bpy.context.object.data.materials.append(mat("legnochiaro", (0.85, 0.65, 0.45), 0.7))
# metro da sarta arrotolato a sinistra dei suoi piedi
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.035, depth=0.014, location=(-0.11, 0.02, 0.0075))
bpy.context.object.name = "metro"; bpy.context.object.data.materials.append(mat("metro", (0.92, 0.82, 0.35), 0.6))
box("metro-coda", (0.12, 0.013, 0.0012), (-0.06, -0.04, 0.0035), mat("metro2", (0.92, 0.82, 0.35), 0.6), rot=(0, 0, math.radians(-30)))

# luci: lampada da tavolo calda a destra camera, riempimento freddo dalla finestra, controluce
def light(kind, loc, energy, color, size=0.3, rot=None, target=(0, 0.12, 0.12)):
    bpy.ops.object.light_add(type=kind, location=loc); l = bpy.context.object
    l.data.energy = energy; l.data.color = color
    if kind == "AREA": l.data.size = size
    if kind == "SPOT": l.data.spot_size = math.radians(70); l.data.spot_blend = 0.6
    d = Vector(target) - Vector(loc); l.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
light("SPOT", (0.35, -0.15, 0.45), 18, (1.0, 0.78, 0.5))
light("AREA", (-0.5, -0.3, 0.35), 6, (0.75, 0.82, 1.0), 0.6)
light("AREA", (0.0, 0.6, 0.4), 5, (1.0, 0.85, 0.7), 0.4)
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[1].default_value = 0.15

# camera frontale, in asse, all'altezza del petto di Jacopino
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
cam.data.lens = 50; cam.data.dof.use_dof = True; cam.data.dof.aperture_fstop = 2.8
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
try:
    sc.render.engine = "BLENDER_EEVEE_NEXT"
except TypeError:
    sc.render.engine = "BLENDER_EEVEE"
sc.view_settings.view_transform = "AgX" if "AgX" in [i.identifier for i in bpy.types.ColorManagedViewSettings.bl_rna.properties["view_transform"].enum_items] else "Filmic"

SHOTS = {"start": ((0.0, -0.58, 0.17), (0.0, 0.06, 0.095)),   # da testa a stivali + oggetti in primo piano
         "end": ((0.0, -0.38, 0.165), (0.0, 0.1, 0.14))}    # avvicinamento: dalle ginocchia in su
for name, (loc, look) in SHOTS.items():
    cam.location = loc
    cam.rotation_euler = (Vector(look) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    focus = bpy.data.objects.get("fuoco") or bpy.data.objects.new("fuoco", None)
    if focus.name not in sc.collection.objects: sc.collection.objects.link(focus)
    focus.location = (0, 0.12, 0.16); cam.data.dof.focus_object = focus
    sc.render.filepath = os.path.join(OUT, name + ".png")
    bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "layout.blend"))
print("OK layout")
