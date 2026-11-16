# build_trouser.py — the Drop 1 trouser in Blender, rebuilt from scratch each run (16/11/2026, v2).
# Run inside Blender (MCP: exec(open(path).read())) or headless: blender -b --python build_trouser.py
# Steps: profile loft (engine tables) -> voxel remesh -> crotch smoothing -> pleats/crease -> cloth sim (pinned at the waist)
#        -> mix with rest shape -> metric UVs (uv = metres / 0.08, cut at the inseam, fly and centre back) -> details -> materials -> glb.
import bpy, bmesh, math, os, time
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

OUT = r"D:\ClaudeCodeTest\videos\_bench\fashion3d\blender"
P = dict(mix=globals().get("MIX", 0.85), frames=40, voxel=0.007, color="#6f7452", tile=0.08)
T0 = time.time(); LOG = {}
Y  = [0, 0.10, 0.5, 0.72, 0.80, 0.86, 0.92, 1.02, 1.06]
CX = [0.112, 0.113, 0.112, 0.105, 0.095, 0.080, 0.066, 0.048, 0.044]
RX = [0.094, 0.095, 0.101, 0.100, 0.099, 0.110, 0.118, 0.122, 0.122]
RZ = [0.090, 0.091, 0.098, 0.106, 0.110, 0.110, 0.108, 0.104, 0.102]
f = lambda tab, y: float(np.interp(y, Y, tab))
def sm(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)

# ---------- clean scene (keep camera, lights, wall)
for o in list(bpy.data.objects):
    if o.type == 'MESH' and o.name != "wall" or o.type == 'CURVE': bpy.data.objects.remove(o, do_unlink=True)
coll = bpy.data.collections.get("details") or bpy.data.collections.new("details")
if coll.name not in bpy.context.scene.collection.children: bpy.context.scene.collection.children.link(coll)

# ---------- 1. loft + remesh
def tube(name, y0, y1, ring, ny=140, na=96):
    bm = bmesh.new(); rows = []
    for i in range(ny + 1):
        y = y0 + (y1 - y0) * i / ny; row = []
        for k in range(na):
            x, z = ring(y, 2 * math.pi * k / na); row.append(bm.verts.new((x, -z, y)))
        rows.append(row)
    for i in range(ny):
        for k in range(na): bm.faces.new((rows[i][k], rows[i][(k + 1) % na], rows[i + 1][(k + 1) % na], rows[i + 1][k]))
    bm.faces.new(rows[0][::-1]); bm.faces.new(rows[-1])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob); return ob
def legring(y, a, s):
    fl = 1 + 0.05 * sm((0.35 - y) / 0.35); rx = f(RX, y) * fl
    if math.sin(a) < 0 and y < 0.74: rx = min(rx, f(CX, y) - 0.017)          # keep a gap between the legs
    return s * (f(CX, y) + rx * math.sin(a)), f(RZ, y) * fl * math.cos(a)
def hip(y, a):
    hx = max(f(CX, y) + f(RX, y) + 0.006, 0.176); hz = max(f(RZ, y) + 0.004, 0.106)
    return hx * math.sin(a), hz * math.cos(a) * (0.2 + 0.8 * sm((y - 0.775) / 0.06))
objs = [tube("leg%d" % s, 0.0, 0.95, lambda y, a, s=s: legring(y, a, s)) for s in (-1, 1)] + [tube("hip", 0.77, 1.08, hip)]
bpy.ops.object.select_all(action='DESELECT')
for o in objs: o.select_set(True)
bpy.context.view_layer.objects.active = objs[0]; bpy.ops.object.join()
ob = bpy.context.active_object; ob.name = "trouser"
m = ob.modifiers.new("rm", "REMESH"); m.mode = 'VOXEL'; m.voxel_size = P["voxel"]; bpy.ops.object.modifier_apply(modifier="rm")
m = ob.modifiers.new("sm", "SMOOTH"); m.factor = 0.6; m.iterations = 8; bpy.ops.object.modifier_apply(modifier="sm")
bm = bmesh.new(); bm.from_mesh(ob.data)
bmesh.ops.delete(bm, geom=[fc for fc in bm.faces if all(v.co.z > 1.072 for v in fc.verts) or all(v.co.z < 0.006 for v in fc.verts)], context='FACES')
# ---------- 2. crotch: relax the crumpled bridge (strong local Laplacian)
reg = [v for v in bm.verts if abs(v.co.x) < 0.075 and 0.66 < v.co.z < 0.88]
for it in range(40):
    new = {}
    for v in reg:
        w = sm((0.075 - abs(v.co.x)) / 0.03) * sm((v.co.z - 0.66) / 0.05) * sm((0.88 - v.co.z) / 0.04)
        c = sum((e.other_vert(v).co for e in v.link_edges), Vector()) / max(1, len(v.link_edges))
        new[v] = v.co.lerp(c, 0.5 * w)
    for v, c in new.items(): v.co = c
bm.to_mesh(ob.data); bm.free()
# ---------- 3. pleats (two per side, front) + pressed crease, as in the engine
def angle_of(x, y, z):
    s = 1 if x >= 0 else -1; cx = s * f(CX, z) if z < 0.95 else 0.0
    return s, math.atan2(s * (x - cx), -y)   # 0 = front, +pi/2 = outer side
for v in ob.data.vertices:
    x, y, z = v.co; s, a = angle_of(x, y, z); d = 0.0
    if z < 0.80:
        for c, amp in ((0, 0.0035), (math.pi, 0.0025), (-math.pi, 0.0025)): d += amp * math.exp(-((a - c) / 0.07) ** 2) * min(1, (0.80 - z) / 0.1)
    fp = 0.008 * sm((z - 0.80) / 0.1) * (1 - sm((z - 1.0) / 0.03)) + 0.0015 * sm((z - 0.55) / 0.25) * (1 - sm((z - 1.0) / 0.03))
    pl = lambda at: math.exp(-((a - at) / 0.03) ** 2) if a > at else math.exp(-((a - at) / 0.12) ** 2)
    d += fp * (pl(-0.30) + pl(-0.66))
    if d: v.co.x += s * math.sin(a) * d; v.co.y += -math.cos(a) * d
ob.data.update()
# ---------- 4. cloth simulation, pinned at the waist
pin = ob.vertex_groups.new(name="pin"); shr = ob.vertex_groups.new(name="shrink")
for v in ob.data.vertices:
    pin.add([v.index], sm((v.co.z - 0.995) / 0.05), 'REPLACE'); shr.add([v.index], sm((0.82 - v.co.z) / 0.2) * sm((v.co.z - 0.05) / 0.07), 'REPLACE')
cl = ob.modifiers.new("Cloth", "CLOTH"); s_ = cl.settings
s_.quality = 6; s_.mass = 0.3; s_.air_damping = 3
s_.tension_stiffness = 40; s_.compression_stiffness = 40; s_.shear_stiffness = 20; s_.bending_stiffness = 12
s_.tension_damping = 5; s_.compression_damping = 5; s_.bending_damping = 2
s_.vertex_group_mass = "pin"; s_.pin_stiffness = 1; s_.shrink_min = globals().get("SHRINK", -0.03); s_.vertex_group_shrink = "shrink"
cl.collision_settings.use_self_collision = False
sc = bpy.context.scene; sc.frame_start = 1; sc.frame_end = P["frames"]; cl.point_cache.frame_start = 1; cl.point_cache.frame_end = P["frames"]
t = time.time()
with bpy.context.temp_override(scene=sc, active_object=ob, point_cache=cl.point_cache): bpy.ops.ptcache.bake(bake=True)
LOG["bake_s"] = round(time.time() - t, 1)
sc.frame_set(P["frames"]); bpy.context.view_layer.objects.active = ob; ob.select_set(True)
ob.shape_key_add(name="Basis"); bpy.ops.object.modifier_apply_as_shapekey(modifier="Cloth", keep_modifier=False)
kb = ob.data.shape_keys.key_blocks; base = [k.co.copy() for k in kb[0].data]; simk = [k.co.copy() for k in kb[-1].data]
for k in list(kb)[::-1]: ob.shape_key_remove(k)
for v, b, q in zip(ob.data.vertices, base, simk):            # per-vertex mix: full drape on the legs, none at the turn-ups (crisp hems)
    w = P["mix"] + (1 - P["mix"]) * (1 - sm((b.z - 0.05) / 0.12)); v.co = b.lerp(q, w)   # the hem follows the sim fully (no bell)
ob.data.update()
sc.frame_set(1)
for g in list(ob.vertex_groups): ob.vertex_groups.remove(g)
bm = bmesh.new(); bm.from_mesh(ob.data)   # trim what the sim pushed under the turn-ups
bmesh.ops.delete(bm, geom=[fc for fc in bm.faces if all(v.co.z < 0.013 for v in fc.verts)], context='FACES'); bm.to_mesh(ob.data); bm.free()
# ---------- 5. metric UVs: panels cut at the inseam, the fly and the centre back (real seams), uv = metres / tile
me = ob.data; uvl = me.uv_layers.new(name="UVMap"); TILE = P["tile"]
for poly in me.polygons:
    c = poly.center; sgn = 1 if c.x >= 0 else -1; uu = []
    for li in poly.loop_indices:
        v = me.vertices[me.loops[li].vertex_index].co
        cx = sgn * f(CX, v.z)
        a = math.atan2(sgn * (v.x - cx), -v.y); a2 = (a + math.pi / 2) % (2 * math.pi)     # 0 at the inseam
        r = (f(RX, v.z) + f(RZ, v.z)) / 2
        uu.append([a2 * r / TILE, v.z / TILE])
    us = [q[0] for q in uu]
    if max(us) - min(us) > 1.5:                                                          # a face across the inseam cut
        per = 2 * math.pi * 0.1 / TILE; mid = (max(us) + min(us)) / 2
        for q in uu:
            if q[0] < mid: q[0] += per
    for li, q in zip(poly.loop_indices, uu): uvl.data[li].uv = (q[0] * sgn, q[1])
for p in me.polygons: p.use_smooth = True

# ---------- 6. materials
def lin(h, k=1.0): h = h.lstrip('#'); return [((int(h[i:i + 2], 16) / 255) * k) ** 2.2 for i in (0, 2, 4)] + [1]
def mat(name, col, rough=0.9, sheen=0.15, twill=True, metal=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    b.inputs["Base Color"].default_value = col; b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    b.inputs["Sheen Weight"].default_value = sheen; nt.links.new(b.outputs[0], out.inputs[0])
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.25
    if twill:   # Blender-side weave (for Cycles stills); the engine uses its own clothMat
        tc = nt.nodes.new("ShaderNodeTexCoord"); w = nt.nodes.new("ShaderNodeTexWave"); w.wave_type = 'BANDS'; w.bands_direction = 'DIAGONAL'
        w.inputs["Scale"].default_value = 40; w.inputs["Distortion"].default_value = 0.6
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.18
        nt.links.new(tc.outputs["UV"], w.inputs["Vector"]); nt.links.new(w.outputs[1], bp.inputs["Height"]); nt.links.new(bp.outputs[0], b.inputs["Normal"])
    return m
C = P["color"]
cloth = mat("drill", lin(C)); dark = mat("drill_dark", lin(C, 0.86)); mouth = mat("mouth", lin(C, 0.22), twill=False, sheen=0)
thread = mat("drill_thread", lin(C, 0.72), twill=False); horn = mat("horn", lin("#2b2118"), rough=0.35, sheen=0, twill=False)
brass = mat("brass", lin("#c9a15a"), rough=0.3, sheen=0, twill=False, metal=1.0)
me.materials.clear(); me.materials.append(cloth)

# ---------- 7. details, placed by ray-cast on the simulated cloth
bm = bmesh.new(); bm.from_mesh(me); bvh = BVHTree.FromBMesh(bm); bm.free()
def surf(z, a, s=0):
    cx = 0 if s == 0 else s * f(CX, z); d = Vector((math.sin(a) * (s if s else 1), -math.cos(a), 0))
    if s == 0: h = bvh.ray_cast(Vector((cx, 0, z)) + d * 0.5, -d, 1.0)
    else: h = bvh.ray_cast(Vector((cx, 0, z)), d, 0.3)
    return (h[0], h[1].normalized() if h[1].dot(d) > 0 else -h[1].normalized()) if h[0] else (Vector((cx, 0, z)) + d * 0.12, d)
def link(o, m_): o.data.materials.append(m_); coll.objects.link(o); return o
def curve(name, pts, r, m_):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r; cu.bevel_resolution = 3
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts): p.co = (q[0], q[1], q[2], 1)
    return link(bpy.data.objects.new(name, cu), m_)
def box(name, c, n, size, m_, bevel=0.0):
    me_ = bpy.data.meshes.new(name); b_ = bmesh.new(); bmesh.ops.create_cube(b_, size=1); b_.to_mesh(me_); b_.free()
    o = bpy.data.objects.new(name, me_); zz = n.normalized(); xx = Vector((0, 0, 1)).cross(zz).normalized(); yy = zz.cross(xx)
    o.matrix_world = Matrix.Translation(c) @ Matrix((xx, yy, zz)).transposed().to_4x4() @ Matrix.Diagonal((*size, 1))
    if bevel: bv = o.modifiers.new("bv", "BEVEL"); bv.width = bevel; bv.segments = 2
    return link(o, m_)
def disc(name, c, n, r, dep, m_):
    me_ = bpy.data.meshes.new(name); b_ = bmesh.new(); bmesh.ops.create_cone(b_, cap_ends=True, segments=24, radius1=r, radius2=r, depth=dep); b_.to_mesh(me_); b_.free()
    o = bpy.data.objects.new(name, me_); o.matrix_world = Matrix.Translation(c) @ n.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    for p in o.data.polygons: p.use_smooth = True
    return link(o, m_)
def band(name, zs, offs, m_, s=0, N=160, zray=None):
    b_ = bmesh.new(); rows = []
    for z, off in zip(zs, offs):
        row = []
        for k in range(N):
            p, n = surf(zray if zray is not None else z, 2 * math.pi * k / N, s); v = b_.verts.new(p + n * off); v.co.z = z; row.append(v)
        rows.append(row)
    for i in range(len(rows) - 1):
        for k in range(N): b_.faces.new((rows[i][k], rows[i][(k + 1) % N], rows[i + 1][(k + 1) % N], rows[i + 1][k]))
    me_ = bpy.data.meshes.new(name); b_.to_mesh(me_); b_.free(); o = link(bpy.data.objects.new(name, me_), m_)
    for p in o.data.polygons: p.use_smooth = True
    so = o.modifiers.new("sol", "SOLIDIFY"); so.thickness = 0.0018; so.offset = -1; return o
wb = band("waistband", [1.003, 1.012, 1.074, 1.08], [0.0045, 0.005, 0.0042, 0.0015], dark, zray=1.045)
for a in (-1.32, -0.88, -0.46, 0.46, 0.88, 1.32, math.pi - 0.3, math.pi + 0.3, math.pi):            # belt loops, 1 x 4.6 cm, standing proud
    p, n = surf(1.046, a, 0); box("loop", p + n * 0.0058, n, (0.0105, 0.047, 0.0032), dark, bevel=0.0012)
p, n = surf(1.047, -0.16, 0); disc("button", p + n * 0.0062, n, 0.0095, 0.0035, horn)                 # waistband button
for s in (-1, 1):                                                                                     # side adjusters: tab + brass buckle
    a = s * math.pi / 2; p, n = surf(1.047, a - s * 0.12, 0); box("adj_tab", p + n * 0.0055, n, (0.045, 0.02, 0.0025), dark, bevel=0.001)
    p, n = surf(1.047, a, 0)
    for dy, h in ((0.0, 0.026), ):
        box("buckle", p + n * 0.007, n, (0.012, h, 0.0022), brass, bevel=0.0008)
fly = []
for k in range(25):                                                                                   # J-stitch of the fly, tone on tone
    u = k / 24
    if u < 0.75: z = 1.01 - 0.17 * u / 0.75; a = -0.17
    else: t_ = (u - 0.75) / 0.25; z = 0.84 - 0.025 * math.sin(t_ * math.pi / 2); a = -0.17 + 0.17 * t_
    p, n = surf(z, a, 0); fly.append(p + n * 0.0011)
curve("fly", fly, 0.0007, thread)
def ribbon(name, path, prof, m_, s, n_along=40):
    """a strip of cloth lying ON the surface along path [(z, a)]: prof = [(d metres across, +front side negative), offset out]; metric uvs"""
    b_ = bmesh.new(); rows = []
    for (z, a) in path:
        row = []
        for d, off in prof:
            p, n = surf(z, a + s * d / 0.18, 0); row.append(b_.verts.new(p + n * off))
        rows.append(row)
    for i in range(len(rows) - 1):
        for j in range(len(prof) - 1): b_.faces.new((rows[i][j], rows[i][j + 1], rows[i + 1][j + 1], rows[i + 1][j]))
    b_.normal_update(); b_.faces.ensure_lookup_table(); fc = b_.faces[len(b_.faces) // 2]; c0 = fc.calc_center_median(); _, nn = surf(c0.z, math.atan2(c0.x, -c0.y), 0)
    if fc.normal.dot(nn) < 0: bmesh.ops.reverse_faces(b_, faces=list(b_.faces))                   # face outwards, like the cloth
    me_ = bpy.data.meshes.new(name); b_.to_mesh(me_); b_.free(); o = link(bpy.data.objects.new(name, me_), m_)
    ul = o.data.uv_layers.new(name="UVMap")
    for poly in o.data.polygons:
        poly.use_smooth = True
        for li in poly.loop_indices:
            v = o.data.vertices[o.data.loops[li].vertex_index].co; ul.data[li].uv = ((math.atan2(v.x, -v.y) * 0.18) / P["tile"], v.z / P["tile"])
    return o
for s in (-1, 1):                                                                                     # slanted side pockets: the front panel ends in a soft folded edge standing ~2.5 mm proud, a thin shadow gap behind it, bar-tacks
    path = []
    for k in range(41):
        u = k / 40; path.append((1.012 - 0.152 * u ** 0.95, s * (1.30 - 0.58 * u ** 1.15)))
    fade = lambda i: sm(i / 4) * sm((40 - i) / 4)
    lip = ribbon("pocket_lip", path, [(-0.011, 0.0006), (-0.007, 0.0013), (-0.0035, 0.0021), (-0.0013, 0.0026), (-0.0003, 0.0021), (0.0, 0.0012)], dark, s)
    for i, row in enumerate([lip.data.vertices[j * 6:(j + 1) * 6] for j in range(41)]):            # flatten the lip into the cloth at both ends of the opening
        f_ = fade(i)
        for v in row:
            p, n = bvh.find_nearest(v.co)[:2]; v.co = p + (v.co - p) * (0.35 + 0.65 * f_)
    gap = ribbon("pocket_gap", path[2:-2], [(0.0, 0.0011), (0.0022, 0.0009)], mouth, s)
    mo = [surf(z, a, 0)[0] for z, a in (path[0], path[-1])]
    for z, a in (path[1], path[-2]):                                                                   # bar-tacks: a short flat bar of dense stitches across the end of the opening
        q, n = surf(z, a, 0); box("bartack", q + n * 0.0012, n, (0.009, 0.0026, 0.0012), thread, bevel=0.0005)
def onsurf(z, a0, a1, off, n=14):
    return [surf(z, a0 + (a1 - a0) * k / (n - 1), 0) for k in range(n)]
for s in (-1, 1):                                                                                     # back welt pockets: welts FOLLOW the curve of the seat
    a = math.pi - s * 0.62; half = 0.06 / 0.18
    for z in (0.9605, 0.9515):
        pts = [p + n * 0.0024 for p, n in onsurf(z, a - half, a + half, 0)]; curve("welt", pts, 0.0042, dark)
    curve("slit", [p + n * 0.0038 for p, n in onsurf(0.956, a - half * 0.98, a + half * 0.98, 0)], 0.0011, mouth)
    for e in (a - half, a + half): q, n = surf(0.956, e, 0); box("bartack", q + n * 0.003, n, (0.0026, 0.012, 0.0012), thread, bevel=0.0005)
    p, n = surf(0.944, a, 0); disc("bbutton", p + n * 0.0035, n, 0.0066, 0.003, horn)
for s in (-1, 1): band("cuff", [0.004, 0.009, 0.042, 0.047], [0.0022, 0.0042, 0.0042, 0.0016], dark, s=s, N=120, zray=0.03)   # turn-ups
so = ob.modifiers.new("sol", "SOLIDIFY"); so.thickness = 0.0018; so.offset = -1
# metric UVs on the cloth details too (waistband, loops, tabs, turn-ups), so the engine twill covers them
for o in coll.objects:
    if o.type != 'MESH' or o.data.materials[0].name not in ("drill", "drill_dark") or len(o.data.uv_layers): continue
    ul = o.data.uv_layers.new(name="UVMap"); mw = o.matrix_world
    for poly in o.data.polygons:
        for li in poly.loop_indices:
            v = mw @ o.data.vertices[o.data.loops[li].vertex_index].co
            if o.name.startswith(("waistband", "cuff")):
                cx = 0 if o.name.startswith("waistband") else (1 if poly.center.x > 0 else -1) * 0.112
                a = math.atan2(v.x - cx, -v.y) % (2 * math.pi); ul.data[li].uv = (a * 0.15 / P["tile"], v.z / P["tile"])
            else: ul.data[li].uv = ((v.x - v.y) / P["tile"], v.z / P["tile"])

# ---------- 8. save + export the garment
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "trouser_test.blend"))
bpy.ops.object.select_all(action='DESELECT')
for o in [ob] + list(coll.objects): o.select_set(True)
gl = os.path.join(OUT, "trouser.glb"); t = time.time()
bpy.ops.export_scene.gltf(filepath=gl, use_selection=True, export_apply=True, export_format='GLB', export_yup=True)
LOG.update(glb_s=round(time.time() - t, 1), glb_mb=round(os.path.getsize(gl) / 1e6, 2), verts=len(me.vertices), total_s=round(time.time() - T0, 1))
print(LOG)
