"""Shot gemello (23/11/2026): la stessa inquadratura da 5 s della clip AI `videos/_bench/ibrido/video/lipsync-v1.mp4`, tutta in Blender (EEVEE), senza AI generativa.
Jacopino sul tavolo da sarto di notte dice «Io parto da carta, matita e metro, meno di 30».

Uso (Blender 5.1, add-on in D:\\blender-user):
  set BLENDER_USER_RESOURCES=D:\\blender-user
  blender -b -P twin.py -- OUTDIR [--mouth decal|keys] [--frames 1-121] [--step 1] [--pct 100] [--samples 64] [--cam main|face] [--save]
Rende PNG in OUTDIR/frames (poi ffmpeg: grana, bloom, vignettatura, audio: vedi finish.sh).
Ingressi: GLB Tripo con scheletro Mixamo + mascella (social/short-03-tabellone/v8/jaw-raw.glb), cues di Rhubarb (OUTDIR/cues.json, `rhubarb -r phonetic -f json`).
Coordinate "raw" = quelle del GLB (pupazzo alto ~0,98 m, guarda -Y con il viso girato di 15,6 gradi verso +X); la radice lo porta a 22 cm.
"""
import bpy, bmesh, sys, os, json, math, random
from mathutils import Vector, Matrix, Euler

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]
def opt(name, default):
    return argv[argv.index(name) + 1] if name in argv else default
MOUTH_MODE = opt("--mouth", "decal")
F0, F1 = [int(x) for x in opt("--frames", "1-121").split("-")]
STEP = int(opt("--step", "1"))
PCT = int(opt("--pct", "100"))
SAMPLES = int(opt("--samples", "64"))
CAMMODE = opt("--cam", "main")
GLB = "D:/ClaudeCodeTest/social/short-03-tabellone/v8/jaw-raw.glb"
CUES = os.path.join(OUT, "cues.json")
FPS = 24
H = 0.22                       # altezza del giocattolo (m)
YAW = math.radians(15.6)       # il GLB ha il viso girato verso +X
random.seed(4)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, 121

# ------------------------------------------------------------------ materiali
def nodes_of(m):
    return m.node_tree.nodes, m.node_tree.links
def bsdf_of(m):
    return next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
def mat(name, rgb, rough=0.6, emit=None, strength=1.0, spec=0.5):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = bsdf_of(m)
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Specular IOR Level"].default_value = spec
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = strength
    return m
NOWEAR = "--nowear" in argv; VOLD = float(opt("--vol", "0.025")); KEY = float(opt("--key", "40"))
def wear(m, scale=180.0, amt=0.25, bump=0.15, coord="Object"):
    """Usura alla Lego Movie: rugosita' a macchie + graffi sottili (rumore stirato) + micro-bump."""
    if NOWEAR: return m
    nt = m.node_tree; N, L = nt.nodes, nt.links; b = bsdf_of(m)
    tc = N.new("ShaderNodeTexCoord")
    nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = scale; nz.inputs["Detail"].default_value = 6
    L.new(tc.outputs[coord], nz.inputs["Vector"])
    mp = N.new("ShaderNodeMapRange"); mp.inputs["To Min"].default_value = max(0.05, b.inputs["Roughness"].default_value - amt)
    mp.inputs["To Max"].default_value = min(1.0, b.inputs["Roughness"].default_value + amt)
    L.new(nz.outputs["Fac"], mp.inputs["Value"]); L.new(mp.outputs["Result"], b.inputs["Roughness"])
    # graffi: rumore stirato lungo X -> righe sottili
    mpv = N.new("ShaderNodeMapping"); mpv.inputs["Scale"].default_value = (scale * 0.08, scale * 2.5, scale * 2.5)
    L.new(tc.outputs[coord], mpv.inputs["Vector"])
    sn = N.new("ShaderNodeTexNoise"); sn.inputs["Scale"].default_value = 1.0; sn.inputs["Detail"].default_value = 2
    L.new(mpv.outputs["Vector"], sn.inputs["Vector"])
    cr = N.new("ShaderNodeMapRange"); cr.inputs["From Min"].default_value = 0.66; cr.inputs["From Max"].default_value = 0.70
    L.new(sn.outputs["Fac"], cr.inputs["Value"])
    add = N.new("ShaderNodeMath"); add.operation = "ADD"
    L.new(nz.outputs["Fac"], add.inputs[0]); L.new(cr.outputs["Result"], add.inputs[1])
    bp = N.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump; bp.inputs["Distance"].default_value = 0.0004
    L.new(add.outputs["Value"], bp.inputs["Height"]); L.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m

def box(name, size, loc, m, rot=(0, 0, 0), bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = size; o.data.materials.append(m)
    if bevel:
        bpy.ops.object.transform_apply(scale=True)
        md = o.modifiers.new("bev", "BEVEL"); md.width = bevel; md.segments = 3
    return o

# ------------------------------------------------------------------ set: tavolo, tappetino, oggetti
legno = mat("legno", (0.36, 0.17, 0.07), 0.45)
nt = legno.node_tree; N, L_ = nt.nodes, nt.links; b = bsdf_of(legno)
tc = N.new("ShaderNodeTexCoord"); wv = N.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value = 9; wv.inputs["Distortion"].default_value = 6; wv.inputs["Detail"].default_value = 4
L_.new(tc.outputs["Object"], wv.inputs["Vector"])
ramp = N.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].color = (0.22, 0.09, 0.03, 1); ramp.color_ramp.elements[1].color = (0.42, 0.21, 0.09, 1)
L_.new(wv.outputs["Fac"], ramp.inputs["Fac"]); L_.new(ramp.outputs["Color"], b.inputs["Base Color"])
wear(legno, 60, 0.15, 0.08)
box("tavolo", (2.2, 2.0, 0.04), (0, 0.2, -0.02), legno)

# tappetino da taglio verde con griglia (1 cm, ogni 5 cm piu' marcata)
mm = mat("tappetino", (0.03, 0.17, 0.10), 0.75)
nt = mm.node_tree; N, L_ = nt.nodes, nt.links; b = bsdf_of(mm)
tc = N.new("ShaderNodeTexCoord"); sp = N.new("ShaderNodeSeparateXYZ"); L_.new(tc.outputs["Object"], sp.inputs[0])
def gridline(axis, period, width):
    m1 = N.new("ShaderNodeMath"); m1.operation = "MULTIPLY"; m1.inputs[1].default_value = 1.0 / period
    L_.new(sp.outputs[axis], m1.inputs[0])
    fr = N.new("ShaderNodeMath"); fr.operation = "PINGPONG"; fr.inputs[1].default_value = 0.5
    L_.new(m1.outputs[0], fr.inputs[0])
    lt = N.new("ShaderNodeMath"); lt.operation = "LESS_THAN"; lt.inputs[1].default_value = width
    L_.new(fr.outputs[0], lt.inputs[0]); return lt
mx = N.new("ShaderNodeMath"); mx.operation = "MAXIMUM"
mx2 = N.new("ShaderNodeMath"); mx2.operation = "MAXIMUM"
mx3 = N.new("ShaderNodeMath"); mx3.operation = "MAXIMUM"
# coordinate oggetto del tappetino: scala 1 dopo transform_apply -> metri
L_.new(gridline("X", 0.02, 0.05).outputs[0], mx.inputs[0]); L_.new(gridline("Y", 0.02, 0.05).outputs[0], mx.inputs[1])
L_.new(gridline("X", 0.10, 0.018).outputs[0], mx2.inputs[0]); L_.new(gridline("Y", 0.10, 0.018).outputs[0], mx2.inputs[1])
L_.new(mx.outputs[0], mx3.inputs[0]); L_.new(mx2.outputs[0], mx3.inputs[1])
mix = N.new("ShaderNodeMix"); mix.data_type = "RGBA"
mix.inputs["A"].default_value = (0.03, 0.17, 0.10, 1); mix.inputs["B"].default_value = (0.42, 0.62, 0.50, 1)
L_.new(mx3.outputs[0], mix.inputs["Factor"]); L_.new(mix.outputs["Result"], b.inputs["Base Color"])
wear(mm, 90, 0.12, 0.05)
mat_o = box("tappetino", (0.9, 0.46, 0.002), (0.02, -0.06, 0.001), mm)   # finisce subito dietro i piedi: dietro si vede il tavolo caldo
bpy.ops.object.transform_apply(scale=True)

carta = wear(mat("carta", (0.80, 0.76, 0.68), 0.85, spec=0.3), 300, 0.05, 0.04)
foglio = box("foglio", (0.21, 0.297, 0.0006), (0.02, -0.165, 0.0026), carta, rot=(0, 0, math.radians(-64)))
# matita gialla esagonale, punta di legno e grafite
pmat = wear(mat("vernice", (0.85, 0.52, 0.02), 0.35), 400, 0.15, 0.1)
bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.0042, depth=0.15, location=(0, 0, 0)); pen = bpy.context.object; pen.name = "matita"; pen.data.materials.append(pmat)
bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.0042, radius2=0.0009, depth=0.016, location=(0, 0, 0.083)); tip = bpy.context.object; tip.data.materials.append(mat("legnochiaro", (0.75, 0.52, 0.30), 0.7))
bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.0011, depth=0.004, location=(0, 0, 0.0925)); gr = bpy.context.object; gr.data.materials.append(mat("grafite", (0.03, 0.03, 0.03), 0.3))
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.0044, depth=0.008, location=(0, 0, -0.079)); fe = bpy.context.object; fe.data.materials.append(mat("ottone", (0.6, 0.45, 0.2), 0.3)); bsdf_of(fe.data.materials[0]).inputs["Metallic"].default_value = 1
for o in (tip, gr, fe): o.parent = pen
pen.location = (0.035, -0.185, 0.0072); pen.rotation_euler = (0, math.radians(90), math.radians(12))
# metro da sarta arrotolato + coda
tmat = mat("metro", (0.80, 0.60, 0.12), 0.55)
nt = tmat.node_tree; N, L_ = nt.nodes, nt.links; b = bsdf_of(tmat)
tc = N.new("ShaderNodeTexCoord"); sp2 = N.new("ShaderNodeSeparateXYZ"); L_.new(tc.outputs["Object"], sp2.inputs[0])
m1 = N.new("ShaderNodeMath"); m1.operation = "MULTIPLY"; m1.inputs[1].default_value = 400; L_.new(sp2.outputs["X"], m1.inputs[0])
fr = N.new("ShaderNodeMath"); fr.operation = "FRACT"; L_.new(m1.outputs[0], fr.inputs[0])
lt = N.new("ShaderNodeMath"); lt.operation = "LESS_THAN"; lt.inputs[1].default_value = 0.18; L_.new(fr.outputs[0], lt.inputs[0])
yy = N.new("ShaderNodeMath"); yy.operation = "GREATER_THAN"; yy.inputs[1].default_value = 0.0; L_.new(sp2.outputs["Y"], yy.inputs[0])
an = N.new("ShaderNodeMath"); an.operation = "MULTIPLY"; L_.new(lt.outputs[0], an.inputs[0]); L_.new(yy.outputs[0], an.inputs[1])
mixm = N.new("ShaderNodeMix"); mixm.data_type = "RGBA"; mixm.inputs["A"].default_value = (0.80, 0.60, 0.12, 1); mixm.inputs["B"].default_value = (0.05, 0.04, 0.03, 1)
L_.new(an.outputs[0], mixm.inputs["Factor"]); L_.new(mixm.outputs["Result"], b.inputs["Base Color"])
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.03, depth=0.016, location=(-0.105, -0.10, 0.008)); roll = bpy.context.object; roll.name = "metro"; roll.data.materials.append(tmat)
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.011, depth=0.0165, location=(-0.105, -0.10, 0.008)); hub = bpy.context.object; hub.data.materials.append(mat("buco", (0.02, 0.015, 0.01), 0.9))
coda = box("metro-coda", (0.16, 0.016, 0.0007), (-0.045, -0.14, 0.0016), tmat, rot=(0, 0, math.radians(-30)))
bpy.ops.object.transform_apply(scale=True)

# ------------------------------------------------------------------ fondo: parete, scaffali con libri, lampadine (bokeh), finestra con la citta' di notte
box("parete", (3.0, 0.05, 1.6), (0, 1.05, 0.6), wear(mat("parete", (0.10, 0.05, 0.03), 0.8), 20, 0.1, 0.1))
scaff = wear(mat("scaffale", (0.20, 0.09, 0.035), 0.5), 40, 0.15, 0.1)
for z in (0.10, 0.36, 0.62):
    box("mensola", (1.0, 0.24, 0.02), (-0.45, 0.92, z), scaff)
    x = -0.93
    while x < 0.02:
        wdt = random.uniform(0.018, 0.04); hgt = random.uniform(0.14, 0.21)
        c = random.choice([(0.25, 0.08, 0.05), (0.10, 0.12, 0.08), (0.30, 0.22, 0.12), (0.06, 0.06, 0.07), (0.32, 0.27, 0.18), (0.12, 0.05, 0.03)])
        box("libro", (wdt, 0.17, hgt), (x + wdt / 2, 0.91, z + 0.01 + hgt / 2), mat("libro", c, random.uniform(0.4, 0.8)), rot=(0, random.uniform(-0.05, 0.05), 0))
        x += wdt + random.uniform(0.0, 0.006)
        if random.random() < 0.08: x += 0.06
warm = (1.0, 0.62, 0.28)
for (x, z) in ((-0.62, 0.23), (-0.15, 0.49), (-0.78, 0.75), (-0.33, 0.78), (0.12, 0.30)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.012, location=(x, 0.86, z)); bpy.context.object.data.materials.append(mat("bulbo", (1, 0.7, 0.4), 0.5, emit=warm, strength=25))
# finestra: griglia di finestrelle della citta' (teal e ambra) dietro un telaio scuro
city = mat("citta", (0, 0, 0), 1.0)
nt = city.node_tree; N, L_ = nt.nodes, nt.links; b = bsdf_of(city)
tc = N.new("ShaderNodeTexCoord"); br = N.new("ShaderNodeTexBrick"); br.inputs["Scale"].default_value = 5; br.inputs["Mortar Size"].default_value = 0.08
br.inputs["Color1"].default_value = (0.02, 0.35, 0.32, 1); br.inputs["Color2"].default_value = (0.004, 0.012, 0.02, 1); br.inputs["Bias"].default_value = 0.55; br.inputs["Mortar"].default_value = (0.0, 0.0, 0.0, 1)
br.offset = 0.0; br.squash = 1.0
L_.new(tc.outputs["Object"], br.inputs["Vector"])
nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 12; L_.new(tc.outputs["Object"], nz.inputs["Vector"])
gt = N.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.62; L_.new(nz.outputs["Fac"], gt.inputs[0])
mu = N.new("ShaderNodeMix"); mu.data_type = "RGBA"; mu.inputs["B"].default_value = (1.0, 0.55, 0.2, 1)
L_.new(br.outputs["Color"], mu.inputs["A"]); L_.new(gt.outputs[0], mu.inputs["Factor"])
b.inputs["Emission Strength"].default_value = 0.9; L_.new(mu.outputs["Result"], b.inputs["Emission Color"])
bpy.ops.mesh.primitive_plane_add(size=1, location=(0.42, 1.02, 0.55), rotation=(math.radians(90), 0, 0)); win = bpy.context.object; win.scale = (0.75, 0.8, 1); win.data.materials.append(city)
telaio = mat("telaio", (0.03, 0.03, 0.035), 0.5)
for xx in (0.05, 0.29, 0.53, 0.79):
    box("montante", (0.025, 0.03, 0.8), (xx, 1.0, 0.55), telaio)
for zz in (0.17, 0.42, 0.68, 0.93):
    box("traverso", (0.75, 0.03, 0.02), (0.42, 1.0, zz), telaio)

# ------------------------------------------------------------------ Jacopino
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=GLB)
new = [o for o in bpy.data.objects if o not in before]
arm = next(o for o in new if o.type == "ARMATURE")
body = max((o for o in new if o.type == "MESH"), key=lambda o: len(o.data.vertices))
drop = [o for o in new if o.type == "MESH" and o is not body]
new = [o for o in new if o not in drop]
for o in drop: bpy.data.objects.remove(o, do_unlink=True)
if arm.animation_data: arm.animation_data.action = None
for act in list(bpy.data.actions): bpy.data.actions.remove(act)
for pb in arm.pose.bones:
    pb.rotation_mode = "QUATERNION"; pb.rotation_quaternion = (1, 0, 0, 0); pb.location = (0, 0, 0)
bpy.context.view_layer.update()
LAT = Vector((math.cos(YAW), math.sin(YAW), 0.0))   # destra-schermo del viso (raw)
FWD = Vector((math.sin(YAW), -math.cos(YAW), 0.0))  # avanti del viso (raw)
UP = Vector((0, 0, 1))
MOUTH_C = Vector((0.0215, -0.0218, 0.7764))
HEAD = "mixamorig:Head"
BODY_C = Vector((0.008, 0.06, 0.0))                  # asse del corpo (raw), dalle ossa Hips/Spine

# materiale del pupazzo: vinile con usura
for m in body.data.materials:
    if m.name.startswith("tripo"):
        b = bsdf_of(m); b.inputs["Roughness"].default_value = 0.45; b.inputs["Specular IOR Level"].default_value = 0.45
        wear(m, 220, 0.12, 0.05)
    if m.name == "mouth_dark" and MOUTH_MODE == "decal":
        pass

def surface_point(u, v, off):
    """Punto della faccia (raw) alla posizione (u laterale, v verticale) attorno alla bocca + offset in avanti."""
    org = MOUTH_C + LAT * u + UP * v + FWD * 0.2
    ok, loc, nrm, idx = body.ray_cast(org, -FWD, distance=0.5)
    if not ok: return MOUTH_C + LAT * u + UP * v + FWD * off
    return loc + FWD * off

def parent_to_bone(o, bone):
    mw = o.matrix_world.copy()
    o.parent = arm; o.parent_type = "BONE"; o.parent_bone = bone
    bpy.context.view_layer.update()
    o.matrix_world = mw

# ---------------- bocche a sostituzione (stile stop motion / Lego): 9 forme di Rhubarb
def clip_poly(poly, keep_above, yv):
    out = []
    for i in range(len(poly)):
        a, b_ = poly[i - 1], poly[i]
        ina = (a[1] >= yv) if keep_above else (a[1] <= yv)
        inb = (b_[1] >= yv) if keep_above else (b_[1] <= yv)
        if ina != inb:
            t = (yv - a[1]) / (b_[1] - a[1]); out.append((a[0] + t * (b_[0] - a[0]), yv))
        if inb: out.append(b_)
    return out
def mouth_outline(w, h, n=2.4, top=0.42, smile=6.0, pts=56):
    P = []
    for i in range(pts):
        t = 2 * math.pi * i / pts; c, s = math.cos(t), math.sin(t)
        x = w / 2 * math.copysign(abs(c) ** (2 / n), c)
        y = (h * top if s > 0 else h * (1 - top)) * math.copysign(abs(s) ** (2 / n), s)
        y += smile * x * x                       # angoli in su: Jacopino sorride
        P.append((x, y))
    return P
def poly_mesh(name, poly, off, m, rings=6):
    cx = sum(p[0] for p in poly) / len(poly); cy = sum(p[1] for p in poly) / len(poly)
    bm = bmesh.new(); ctr = bm.verts.new(surface_point(cx, cy, off)); grid = []
    for k in range(1, rings + 1):
        f = k / rings
        grid.append([bm.verts.new(surface_point(cx + (x - cx) * f, cy + (y - cy) * f, off)) for (x, y) in poly])
    n_ = len(poly)
    for i in range(n_): bm.faces.new((ctr, grid[0][i], grid[0][(i + 1) % n_]))
    for k in range(rings - 1):
        for i in range(n_):
            bm.faces.new((grid[k][i], grid[k + 1][i], grid[k + 1][(i + 1) % n_], grid[k][(i + 1) % n_]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); me.materials.append(m)
    for p in me.polygons: p.use_smooth = True
    return o
# (w, h, n, denti_sopra, denti_sotto, lingua) in metri raw (larghezza della piega a riposo: 0,043)
SHAPES = {
    "X": (0.040, 0.0030, 2.2, 0.0, 0.0, 0.0),
    "A": (0.036, 0.0036, 2.2, 0.0, 0.0, 0.0),
    "B": (0.044, 0.0105, 2.6, 0.0042, 0.0034, 0.0),
    "C": (0.046, 0.0170, 2.4, 0.0050, 0.0, 0.0),
    "D": (0.048, 0.0270, 2.2, 0.0055, 0.0, 0.0075),
    "E": (0.034, 0.0190, 2.0, 0.0040, 0.0, 0.0045),
    "F": (0.020, 0.0150, 2.0, 0.0, 0.0, 0.0),
    "G": (0.042, 0.0090, 2.6, 0.0060, 0.0, 0.0),
    "H": (0.044, 0.0180, 2.4, 0.0045, 0.0, 0.0080),
}
m_in = mat("bocca", (0.045, 0.008, 0.008), 0.6, spec=0.3)
m_lip = mat("labbro", (0.30, 0.13, 0.09), 0.5, spec=0.5)
m_teeth = mat("denti", (0.80, 0.76, 0.68), 0.35)
m_tongue = mat("lingua", (0.45, 0.10, 0.09), 0.5)
mouths = {}
if MOUTH_MODE == "decal":
    MS = float(opt("--mscale", "1.15"))   # bocche un filo piu' grandi della piega scolpita: si leggono anche a figura intera
    for key, (w, h, n, tt, tb, tg) in SHAPES.items():
        w, h, tt, tb, tg = w * MS, h * MS, tt * MS, tb * MS, tg * MS
        parts = []
        inner = mouth_outline(w, h, n)
        lip = mouth_outline(w + 0.004, h + 0.0034, n)
        parts.append(poly_mesh("lab_" + key, lip, 0.0006, m_lip))
        parts.append(poly_mesh("boc_" + key, inner, 0.0010, m_in))
        topv = max(p[1] for p in inner); botv = min(p[1] for p in inner)
        if tg:
            tp = clip_poly(mouth_outline(w * 0.62, h * 0.9, 2.0), False, botv + tg)
            if len(tp) > 2: parts.append(poly_mesh("lin_" + key, [(x, y - h * 0.05) for x, y in tp], 0.0013, m_tongue))
        if tt:
            tp = clip_poly(inner, True, topv - tt)
            if len(tp) > 2: parts.append(poly_mesh("dsu_" + key, [(x * 0.92, y) for x, y in tp], 0.0015, m_teeth))
        if tb:
            tp = clip_poly(inner, False, botv + tb)
            if len(tp) > 2: parts.append(poly_mesh("dso_" + key, [(x * 0.9, y) for x, y in tp], 0.0015, m_teeth))
        bpy.ops.object.empty_add(location=MOUTH_C); grp = bpy.context.object; grp.name = "mouth_" + key; grp.empty_display_size = 0.01
        for p in parts: p.parent = grp; p.matrix_parent_inverse = grp.matrix_world.inverted()
        parent_to_bone(grp, HEAD)
        mouths[key] = (grp, parts)

# ---------------- sopracciglia: ossa nuove che muovono le sopracciglia SCOLPITE (niente doppioni)
BROWS = {"browR": (-0.036 + 0.0, 0.882), "browL": (0.044, 0.882)}   # (laterale rispetto alla bocca, z) misurati sul primo piano
bpy.context.view_layer.objects.active = arm; arm.select_set(True)
bpy.ops.object.mode_set(mode="EDIT")
for bn, (u, z) in BROWS.items():
    eb = arm.data.edit_bones.new(bn)
    base = MOUTH_C + LAT * u; base.z = z
    eb.head = base - FWD * 0.01; eb.tail = base + FWD * 0.02; eb.parent = arm.data.edit_bones[HEAD]
bpy.ops.object.mode_set(mode="OBJECT")
vg_head = body.vertex_groups.get(HEAD)
def sm(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
for bn, (u0, z0) in BROWS.items():
    vg = body.vertex_groups.new(name=bn)
    for v in body.data.vertices:
        p = v.co; d = p - MOUTH_C
        u = d.dot(LAT); fw = d.dot(FWD)
        if fw < -0.02: continue
        wu = sm((0.040 - abs(u - u0)) / 0.012)               # larghezza ~6,4 cm + sfumatura
        wz = sm((0.016 - abs(p.z - (z0 + 0.003))) / 0.010)   # fascia sopra gli occhiali
        wgl = sm((p.z - 0.872) / 0.004)                      # mai gli occhiali
        w_ = wu * wz * wgl
        if w_ > 0.01:
            vg.add([v.index], w_, "REPLACE")
            if vg_head: vg_head.add([v.index], 1.0 - w_, "REPLACE")

# shape key bocca (modalita' "keys"): jawOpen guidato dai cues
jaw_key = body.data.shape_keys.key_blocks.get("jawOpen") if body.data.shape_keys else None

# ------------------------------------------------------------------ radice: scala giocattolo, viso verso la camera
bpy.ops.object.empty_add(location=(0, 0, 0)); root = bpy.context.object; root.name = "jacopino"
for o in new:
    if o.name in bpy.data.objects and o.parent is None: o.parent = root
S = H / 0.983
root.scale = (S, S, S)   # il corpo guarda gia' la camera: solo la testa e' girata (corretta sull'osso Head)
zmin = min((body.matrix_world @ Vector(c)).z for c in body.bound_box)
root.location = Vector((0, 0.13, 0)) - BODY_C * S - Vector((0, 0, zmin * S))
bpy.context.view_layer.update()

# ------------------------------------------------------------------ IK delle braccia (bersagli in coordinate raw, figli della radice)
def empty(name, loc, parent=root):
    o = bpy.data.objects.new(name, None); sc.collection.objects.link(o); o.parent = parent; o.location = loc; o.empty_display_size = 0.02; return o
def raw(lat, fwd, z):
    """Coordinate raw da (laterale: + = sinistra del personaggio = destra schermo, avanti verso la camera, z)."""
    return BODY_C + Vector((lat, -fwd, z))   # assi del CORPO (non del viso)
tR = empty("ikR", raw(-0.10, 0.0, 0.34)); pR = empty("poleR", raw(-0.35, -0.25, 0.48))
tL = empty("ikL", raw(0.14, 0.0, 0.34)); pL = empty("poleL", raw(0.38, -0.25, 0.48))
def ik(bone, tgt, pole):
    c = arm.pose.bones[bone].constraints.new("IK"); c.target = tgt; c.pole_target = pole; c.chain_count = 2; c.pole_angle = math.radians(-90); c.influence = 0.0; return c
ikR = ik("mixamorig:RightForeArm", tR, pR); ikL = ik("mixamorig:LeftForeArm", tL, pL)

# ------------------------------------------------------------------ PERFORMANCE: partitura -> molle smorzate -> chiavi a ogni fotogramma
def spring_track(keys, nfr, omega=14.0, zeta=0.55, dim=1):
    """keys: lista (t_sec, valore) a gradino; la molla smorzata li insegue (anticipo e overshoot naturali)."""
    import itertools
    keys = sorted(keys); out = []; sub = 8; dt = 1.0 / (FPS * sub)
    x = list(keys[0][1]) if dim > 1 else [keys[0][1]]; v = [0.0] * len(x); ki = 0
    for f in range(nfr * sub):
        t = f * dt
        while ki + 1 < len(keys) and keys[ki + 1][0] <= t: ki += 1
        tg = list(keys[ki][1]) if dim > 1 else [keys[ki][1]]
        for j in range(len(x)):
            a = omega * omega * (tg[j] - x[j]) - 2 * zeta * omega * v[j]; v[j] += a * dt; x[j] += v[j] * dt
        if f % sub == 0: out.append(list(x) if dim > 1 else x[0])
    return out
NFR = 121
T = lambda s: s
# tempi delle parole (inviluppo a 50 Hz): Io 0.22, parto 0.40, da 0.80, carta 1.00, matita 1.45, metro 2.00, pausa 2.40-2.82, meno 2.82, di 3.05, trenta 3.30-3.80
# GESTO 1: la mano destra indica il foglio (carta... matita... metro con due colpetti); GESTO 2: palmi in su su "meno di trenta", tenuti fino alla fine.
REST_R = (-0.113, 0.047, 0.344); REST_L = (0.126, -0.001, 0.339)   # polsi a riposo (misurati sulle ossa)
# GESTO 1 (mano SINISTRA, lato del foglio): mano aperta che presenta/indica il foglio, due colpetti su "matita" e "metro"; torna giu' nella pausa.
# GESTO 2 (mano DESTRA): palmo in su su "meno di trenta" (torsione +80 verificata), tenuto fino alla fine con un assestamento.
POINT_L = (0.20, 0.15, 0.43); TAP_L = (0.20, 0.155, 0.405); ANTIC_L = (0.135, -0.01, 0.37)
OPEN_R = (-0.15, 0.17, 0.47)
ikL_pos = spring_track([(0, REST_L), (0.28, ANTIC_L), (0.50, POINT_L), (1.40, TAP_L), (1.53, POINT_L), (1.94, TAP_L), (2.08, POINT_L), (2.45, REST_L)], NFR, 13, 0.6, 3)
ikL_inf = spring_track([(0, 0.0), (0.20, 1.0), (2.75, 0.0)], NFR, 8, 0.9)
ikR_pos = spring_track([(0, REST_R), (2.40, (-0.12, 0.03, 0.38)), (2.66, OPEN_R), (3.30, (-0.17, 0.18, 0.485)), (3.85, OPEN_R)], NFR, 13, 0.6, 3)
ikR_inf = spring_track([(0, 0.0), (2.35, 1.0)], NFR, 9, 0.9)
TW = float(opt("--twist", "80")); FL = float(opt("--flex", "-35"))
handL = spring_track([(0, (0, 0, 0)), (0.42, (FL, 0, 0)), (2.45, (0, 0, 0))], NFR, 12, 0.6, 3)
handR = spring_track([(0, (0, 0, 0)), (2.60, (10, TW, 0))], NFR, 12, 0.6, 3)
fingR_idx = spring_track([(0, 0.3), (2.5, 0.1)], NFR, 14, 0.7)
fingR_oth = spring_track([(0, 0.3), (2.5, 0.12)], NFR, 14, 0.7)
fingL = spring_track([(0, 0.3), (0.42, 0.05), (2.45, 0.3)], NFR, 12, 0.7)
# testa (pitch +giu', yaw + verso destra schermo, roll) gradi; busto; sopracciglia (alza m raw, inclinazione gradi)
head = spring_track([(0, (0, 0, 0)), (0.20, (-4, 0, 2)), (0.62, (13, 7, 0)), (1.0, (16, 9, 2)), (1.45, (14, 5, -1)), (2.0, (16, 3, 1)), (2.42, (-2, 0, 0)), (2.85, (-5, -4, -6)), (3.30, (2, -6, -8)), (3.75, (-2, -3, -5)), (4.4, (-1, -2, -4))], NFR, 9, 0.62, 3)
spine = spring_track([(0, (0, 0, 0)), (0.30, (-2, 0, 0)), (0.55, (5, 5, 0)), (2.45, (0, 0, 0)), (2.80, (-3, -4, 0)), (3.30, (-1, -6, -2)), (4.0, (-2, -3, -1))], NFR, 7, 0.7, 3)
browR = spring_track([(0, (0, 0)), (0.18, (0.006, 0)), (0.70, (0.0, -6)), (1.95, (0.004, 0)), (2.30, (0.001, 0)), (2.85, (0.007, 6)), (3.35, (0.009, 10)), (3.95, (0.005, 4))], NFR, 12, 0.6, 2)
browL = spring_track([(0, (0, 0)), (0.20, (0.006, 0)), (0.70, (0.0, 6)), (1.95, (0.004, 0)), (2.30, (0.001, 0)), (2.85, (0.004, -2)), (3.35, (0.002, -4)), (3.95, (0.002, -2))], NFR, 12, 0.6, 2)
# respiro e micro-ondeggiamento (mai fermo)
def breath(t): return 1.4 * math.sin(2 * math.pi * 0.28 * t)
def sway(t): return 0.8 * math.sin(2 * math.pi * 0.17 * t + 1.0)

def qrot(pb, ex, ey, ez):
    pb.rotation_quaternion = Euler((math.radians(ex), math.radians(ey), math.radians(ez)), "XYZ").to_quaternion()
PB = arm.pose.bones
FINGERS = {s: [n for n in PB.keys() if ("%sHand" % s) in n and any(k in n for k in ("Index", "Middle", "Ring", "Pinky", "Thumb")) and n[-1] in "123"] for s in ("Right", "Left")}
VIS = {}
HEADYAW = float(opt("--headyaw", "-15.6"))   # gradi: riporta il viso verso la camera
for f in range(NFR):
    t = f / FPS; fr = f + 1
    tR.location = raw(*ikR_pos[f]); tR.keyframe_insert("location", frame=fr)
    tL.location = raw(*ikL_pos[f]); tL.keyframe_insert("location", frame=fr)
    ikR.influence = max(0, min(1, ikR_inf[f])); ikR.keyframe_insert("influence", frame=fr)
    ikL.influence = max(0, min(1, ikL_inf[f])); ikL.keyframe_insert("influence", frame=fr)
    qrot(PB["mixamorig:RightHand"], *handR[f]); PB["mixamorig:RightHand"].keyframe_insert("rotation_quaternion", frame=fr)
    qrot(PB["mixamorig:LeftHand"], *handL[f]); PB["mixamorig:LeftHand"].keyframe_insert("rotation_quaternion", frame=fr)
    for side, lst in FINGERS.items():
        for n in lst:
            if side == "Right": c = fingR_idx[f] if "Index" in n else fingR_oth[f]
            else: c = fingL[f]
            ang = (35 if "Thumb" not in n else 15) * c + 8
            qrot(PB[n], ang, 0, 0); PB[n].keyframe_insert("rotation_quaternion", frame=fr)
    hp, hy, hr = head[f]
    qrot(PB["mixamorig:Head"], hp * 0.6, hy * 0.6 + HEADYAW * 0.6, hr * 0.6); PB["mixamorig:Head"].keyframe_insert("rotation_quaternion", frame=fr)
    qrot(PB["mixamorig:Neck"], hp * 0.4, hy * 0.4 + HEADYAW * 0.4, hr * 0.4); PB["mixamorig:Neck"].keyframe_insert("rotation_quaternion", frame=fr)
    sp_, sy, sr = spine[f]
    qrot(PB["mixamorig:Spine1"], sp_ * 0.5 + breath(t) * 0.5, sy * 0.5, sr * 0.5 + sway(t) * 0.5); PB["mixamorig:Spine1"].keyframe_insert("rotation_quaternion", frame=fr)
    qrot(PB["mixamorig:Spine2"], sp_ * 0.5 + breath(t), sy * 0.5, sr * 0.5); PB["mixamorig:Spine2"].keyframe_insert("rotation_quaternion", frame=fr)
    qrot(PB["mixamorig:Hips"], 0, sway(t) * 0.6, sway(t) * 0.4); PB["mixamorig:Hips"].keyframe_insert("rotation_quaternion", frame=fr)
    for bn, tr in (("browR", browR[f]), ("browL", browL[f])):
        pb = PB[bn]; up_local = arm.data.bones[bn].matrix_local.to_3x3().inverted() @ UP
        pb.location = up_local * tr[0] * 1.5; pb.keyframe_insert("location", frame=fr)
        qrot(pb, 0, tr[1] * 1.5, 0); pb.keyframe_insert("rotation_quaternion", frame=fr)

# ---------------- bocca: cues di Rhubarb -> forma visibile (anticipo di 1 fotogramma, minimo 2 fotogrammi: "sui due" come lo stop motion)
cues = json.load(open(CUES))["mouthCues"]
seq = []
for c in cues:
    f = max(1, int(round(c["start"] * FPS)) + 1 - 1)
    if seq and f - seq[-1][0] < 2: f = seq[-1][0] + 2
    seq.append((f, c["value"]))
def shape_at(fr):
    cur = "X"
    for f, v in seq:
        if f <= fr: cur = v
    return cur
JAW = {"X": 0.0, "A": 0.0, "B": 0.25, "C": 0.55, "D": 1.0, "E": 0.6, "F": 0.35, "G": 0.2, "H": 0.6}
for fr in range(1, NFR + 1):
    s_ = shape_at(fr)
    if MOUTH_MODE == "decal":
        for key, (grp, parts) in mouths.items():
            for p in parts:
                p.hide_render = (key != s_); p.keyframe_insert("hide_render", frame=fr)
if MOUTH_MODE == "keys" and jaw_key:   # confronto: la stessa partitura sulla shape key jawOpen, liscia (molla) invece che a sostituzione
    jt = spring_track([(0, 0.0)] + [((f - 1) / FPS, JAW[v]) for f, v in seq], NFR, 30, 0.8)
    for f in range(NFR):
        jaw_key.value = max(0.0, jt[f]); jaw_key.keyframe_insert("value", frame=f + 1)

# ------------------------------------------------------------------ luci
def light(kind, loc, energy, color, size=0.3, target=(0, 0.13, 0.12), spot=70, blend=0.6, shadow_soft=None):
    bpy.ops.object.light_add(type=kind, location=loc); l = bpy.context.object
    l.data.energy = energy; l.data.color = color
    if kind == "AREA": l.data.size = size
    if kind == "SPOT": l.data.spot_size = math.radians(spot); l.data.spot_blend = blend; l.data.shadow_soft_size = size
    d = Vector(target) - Vector(loc); l.rotation_euler = d.to_track_quat("-Z", "Y").to_euler(); return l
light("SPOT", (0.30, -0.42, 0.42), KEY, (1.0, 0.66, 0.38), 0.08, target=(0.0, 0.10, 0.10), spot=55, blend=0.8)        # lampada da tavolo: key calda
light("AREA", (-0.45, -0.35, 0.25), 1.5, (1.0, 0.82, 0.68), 0.5)                                                     # riempimento morbido
light("AREA", (-0.25, 0.55, 0.32), 2.5, (0.35, 0.85, 0.80), 0.25, target=(0, 0.13, 0.15))                            # controluce teal (dalla finestra)
light("AREA", (0.30, 0.45, 0.35), 4.0, (1.0, 0.65, 0.35), 0.25, target=(0, 0.13, 0.15))                             # controluce caldo
light("SPOT", (-0.1, 0.95, 0.9), 30, (1.0, 0.6, 0.3), 0.05, target=(-0.4, 0.9, 0.3), spot=80, blend=1.0)           # luce sugli scaffali
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.04, 0.035, 0.03, 1); bg.inputs[1].default_value = 0.12
vol = w.node_tree.nodes.new("ShaderNodeVolumePrincipled"); vol.inputs["Density"].default_value = VOLD; vol.inputs["Anisotropy"].default_value = 0.35
vol.inputs["Color"].default_value = (1.0, 0.92, 0.85, 1)
wo = next(n for n in w.node_tree.nodes if n.type == "OUTPUT_WORLD")
if VOLD > 0: w.node_tree.links.new(vol.outputs["Volume"], wo.inputs["Volume"])

# ------------------------------------------------------------------ camera: rig (avvicinamento con easing su arco) + Shakify
rig = bpy.data.objects.new("cam_rig", None); sc.collection.objects.link(rig)
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam; cam.parent = rig
cam.location = (0, 0, 0); cam.rotation_euler = (0, 0, 0)
cam.data.lens = 50; cam.data.sensor_width = 36; cam.data.sensor_fit = "AUTO"; cam.data.clip_start = 0.005
cam.data.dof.use_dof = True; cam.data.dof.aperture_fstop = 2.2; cam.data.dof.aperture_blades = 7
focus = bpy.data.objects.new("fuoco", None); sc.collection.objects.link(focus); cam.data.dof.focus_object = focus
def ease(x): x = max(0.0, min(1.0, x)); return x * x * x * (x * (6 * x - 15) + 10)
P0, L0 = Vector((0.0, -0.60, 0.165)), Vector((0.0, 0.13, 0.095))   # piede del tavolo: largo, testa-stivali + oggetti in primo piano
P1, L1 = Vector((0.012, -0.43, 0.165)), Vector((0.0, 0.13, 0.118))  # avvicinamento: dalle cosce in su, la faccia piu' grande
if CAMMODE == "mid":
    P0 = P1 = Vector((0.0, -0.33, 0.13)); L0 = L1 = Vector((0.0, 0.13, 0.10))
if CAMMODE == "hand":
    P0 = P1 = Vector((-0.03, -0.16, 0.10)); L0 = L1 = Vector((-0.04, 0.13, 0.085)); cam.data.dof.aperture_fstop = 11
if CAMMODE == "face":
    P0 = P1 = Vector((0.0, 0.0, 0.185)); L0 = L1 = Vector((0.0, 0.13, 0.180)); cam.data.dof.aperture_fstop = 8
for f in range(NFR):
    t = f / (NFR - 1); e = ease((t - 0.08) / 0.84)
    p = P0.lerp(P1, e); p.x += 0.010 * math.sin(math.pi * e)              # leggero arco laterale, mai lineare
    look = L0.lerp(L1, e)
    rig.location = p; rig.rotation_euler = (look - p).to_track_quat("-Z", "Y").to_euler()
    rig.keyframe_insert("location", frame=f + 1); rig.keyframe_insert("rotation_euler", frame=f + 1)
    focus.location = (0.0, 0.11, 0.19); focus.keyframe_insert("location", frame=f + 1)
try:
    bpy.ops.preferences.addon_enable(module="bl_ext.user_default.camera_shakify")
    bpy.context.view_layer.objects.active = cam; cam.select_set(True)
    bpy.ops.object.camera_shake_add()
    sh = cam.camera_shakes[0]; sh.shake_type = "INVESTIGATION"; sh.influence = 0.35; sh.scale = 0.12
    bpy.ops.object.camera_shake_add()
    sh2 = cam.camera_shakes[1]; sh2.shake_type = "THE_CLOSEUP"; sh2.influence = 0.25; sh2.scale = 0.10; sh2.offset = 40
    print("Shakify OK", [s.shake_type for s in cam.camera_shakes])
except Exception as ex:
    print("Shakify NON disponibile:", ex)

# ------------------------------------------------------------------ render
for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
    try: sc.render.engine = eng; break
    except TypeError: pass
ee = sc.eevee
ee.taa_render_samples = SAMPLES
for k, v in (("use_raytracing", True), ("use_shadows", True), ("volumetric_tile_size", "4"), ("volumetric_samples", 64), ("volumetric_start", 0.02), ("volumetric_end", 3.0),
             ("use_volumetric_shadows", True), ("shadow_ray_count", 2), ("shadow_step_count", 8), ("use_fast_gi", True)):
    try: setattr(ee, k, v)
    except Exception as ex: print("eevee", k, ex)
sc.render.use_motion_blur = True
try: sc.render.motion_blur_shutter = 0.45
except Exception: pass
vt = [i.identifier for i in bpy.types.ColorManagedViewSettings.bl_rna.properties["view_transform"].enum_items]
sc.view_settings.view_transform = "AgX" if "AgX" in vt else "Filmic"
looks = [i.identifier for i in bpy.types.ColorManagedViewSettings.bl_rna.properties["look"].enum_items]
for lk in (opt("--look", "AgX - Punchy"), "AgX - Medium High Contrast", "Medium High Contrast"):
    if lk in looks: sc.view_settings.look = lk; break
sc.view_settings.exposure = float(opt("--exp", "0.0"))
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920; sc.render.resolution_percentage = PCT
sc.render.image_settings.file_format = "PNG"
fdir = os.path.join(OUT, opt("--dir", "frames_%s_%s" % (MOUTH_MODE, CAMMODE))); os.makedirs(fdir, exist_ok=True)
if "--save" in argv:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "twin_%s.blend" % MOUTH_MODE))
import time
for fr in range(F0, F1 + 1, STEP):
    t0 = time.time(); sc.frame_set(fr)
    if "--debug" in argv:
        hb = arm.pose.bones["mixamorig:RightHand"]
        print("DBG", fr, "polso", tuple(round(x, 3) for x in arm.matrix_world @ hb.head), "bersaglio", tuple(round(x, 3) for x in tR.matrix_world.translation), "infl", round(ikR.influence, 2))
        if "--norender" in argv: continue
    sc.render.filepath = os.path.join(fdir, "f%04d.png" % fr)
    bpy.ops.render.render(write_still=True)
    print("FRAME", fr, "%.1fs" % (time.time() - t0), flush=True)
print("OK twin")
