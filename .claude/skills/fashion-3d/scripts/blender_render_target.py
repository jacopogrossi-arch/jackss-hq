# render_target.py — a Blender still that matches the critic target (three-quarter front, night atelier, warm lamp camera-left).
# Globals: OUTPNG (path), ENGINE ("EEVEE" quick / "CYCLES" final), SAMPLES, VIEW ("front" | "waist" | "back"), RES (w, h)
import bpy, math, os
from mathutils import Vector
sc = bpy.context.scene
OUTPNG = globals().get("OUTPNG", r"D:\ClaudeCodeTest\.critic\blender.png"); VIEW = globals().get("VIEW", "front")
RES = globals().get("RES", (540, 960)); SAMPLES = globals().get("SAMPLES", 64); ENGINE = globals().get("ENGINE", "CYCLES")
def obj(name, data):
    o = bpy.data.objects.get(name)
    if o is None: o = bpy.data.objects.new(name, data); sc.collection.objects.link(o)
    return o
for o in sc.objects:
    if o.type == 'LIGHT' and not o.name.endswith("_t"): o.hide_render = True; o.hide_viewport = True
    if o.name == "wall": o.hide_render = True
cam = obj("cam_t", bpy.data.cameras.get("cam_t") or bpy.data.cameras.new("cam_t")); sc.camera = cam
V = {"front": ((0.62, -2.55, 0.62), (0.0, 0.0, 0.58), 34), "waist": ((0.30, -0.95, 0.98), (0.0, 0.0, 0.90), 45), "back": ((-0.6, 2.55, 0.62), (0.0, 0.0, 0.58), 34), "hem": ((0.30, -1.0, 0.22), (0.0, 0.0, 0.10), 40), "hero": ((0.42, -1.70, 0.66), (0.0, 0.0, 0.555), 50)}
p, l, lens = V[VIEW]; cam.location = p; cam.data.lens = lens
cam.rotation_euler = (Vector(l) - Vector(p)).to_track_quat('-Z', 'Y').to_euler()
cam.data.dof.use_dof = True; cam.data.dof.focus_distance = (Vector(l) - Vector(p)).length; cam.data.dof.aperture_fstop = 4.0
def light(name, kind, loc, energy, color, size):
    d = bpy.data.lights.get(name) or bpy.data.lights.new(name, kind); d.energy = energy; d.color = color
    if kind == 'AREA': d.size = size
    o = obj(name, d); o.location = loc; o.rotation_euler = (Vector((0, 0, 0.6)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); o.hide_render = False; o.hide_viewport = False; return o
light("key_t", 'AREA', (-1.4, -1.2, 1.5), 260, (1.0, 0.78, 0.55), 0.6)       # warm desk-lamp key, camera-left, above
light("fill_t", 'AREA', (1.6, -1.6, 0.9), 22, (1.0, 0.85, 0.7), 1.5)        # faint warm fill
light("rim_t", 'AREA', (0.8, 1.4, 1.4), 70, (1.0, 0.8, 0.6), 0.8)           # warm rim from behind
w = sc.world or bpy.data.worlds.new("World"); sc.world = w; w.use_nodes = True
bg = next(n for n in w.node_tree.nodes if n.type == 'BACKGROUND'); bg.inputs[0].default_value = (0.018, 0.012, 0.008, 1); bg.inputs[1].default_value = 1.0
fl = bpy.data.objects.get("floor_t")
if fl is None:
    bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0)); fl = bpy.context.active_object; fl.name = "floor_t"
    m = bpy.data.materials.new("floor_t"); m.use_nodes = True; b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    b.inputs["Base Color"].default_value = (0.09, 0.05, 0.03, 1); b.inputs["Roughness"].default_value = 0.55; fl.data.materials.append(m)
try: sc.render.engine = 'CYCLES' if ENGINE == "CYCLES" else 'BLENDER_EEVEE_NEXT'
except TypeError:
    try: sc.render.engine = 'BLENDER_EEVEE'
    except TypeError: pass
if ENGINE == "CYCLES":
    sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
    try: sc.cycles.device = 'GPU'
    except Exception: pass
sc.render.resolution_x, sc.render.resolution_y = RES; sc.render.resolution_percentage = 100
sc.view_settings.view_transform = 'AgX' if 'AgX' in [i.identifier for i in sc.view_settings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
sc.view_settings.exposure = globals().get("EXPOSURE", 0.0)
sc.render.filepath = OUTPNG; os.makedirs(os.path.dirname(OUTPNG), exist_ok=True)
bpy.ops.render.render(write_still=True)
print("rendered", OUTPNG)
