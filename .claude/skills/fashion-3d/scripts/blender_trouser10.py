# build_trouser10.py — the Drop 1 trouser in Blender, v10 (16/11/2026).
# A quad mesh built by construction (classic trouser topology: two leg tubes merging at the crotch into one hip tube),
# columns placed ON the creases / pleat folds / fly edge so Subdivision edge creases keep them sharp; a hidden mannequin
# collider gives the cloth a body; cloth sim pinned at the waist; details as in v9; metric UVs; glb + .blend.
# Run inside Blender (MCP: exec(open(path).read())) or headless: blender -b --python build_trouser10.py
import bpy, bmesh, math, os, time
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

OUT = r"D:\ClaudeCodeTest\videos\_bench\fashion3d\blender"
P = dict(color="#4f5c30", tile=0.08, frames=globals().get("FRAMES", 45), M=96, Q=8, ZC=0.745, dz=0.008,
         crease=0.0022, pleat=0.0065, sim=globals().get("SIM", True), subd=(1, 2))
T0 = time.time(); LOG = {}
Y  = [0, 0.10, 0.5, 0.72, 0.80, 0.86, 0.92, 1.02, 1.06]
CX = [0.112, 0.113, 0.112, 0.105, 0.095, 0.080, 0.066, 0.048, 0.044]
RX = [0.094, 0.095, 0.101, 0.100, 0.099, 0.110, 0.118, 0.122, 0.122]
RZ = [0.090, 0.091, 0.098, 0.106, 0.110, 0.110, 0.108, 0.104, 0.102]
f = lambda tab, y: float(np.interp(y, Y, tab))
def sm(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def lerp(a, b, t): return a + (b - a) * t

# ---------- clean scene (keep camera, lights, wall)
for o in list(bpy.data.objects):
    if o.type == 'MESH' and o.name != "wall" or o.type == 'CURVE': bpy.data.objects.remove(o, do_unlink=True)
for m_ in list(bpy.data.meshes):
    if m_.users == 0: bpy.data.meshes.remove(m_)
coll = bpy.data.collections.get("details") or bpy.data.collections.new("details")
if coll.name not in bpy.context.scene.collection.children: bpy.context.scene.collection.children.link(coll)

# ---------- 1. the garment mesh, by construction
M, Q, ZC = P["M"], P["Q"], P["ZC"]
kf, kb = M - Q, M // 2 + Q                         # front / back crotch points on each leg ring (a = 330 / 210 deg)
INNER = list(range(kb, kf + 1))                    # 210 -> 330 deg through the inseam (270)
OUTER = list(range(kf, M)) + list(range(0, kb + 1))  # 330 -> 360/0 (front) -> 90 (outer side) -> 180 (back) -> 210
NO = len(OUTER) - 1                                # outer arc segments (64 for M=96)
J_CREASE = M - kf                                  # outer index of a=0 (front crease) -> pleat 1 continues it
J_PLEAT = (J_CREASE, J_CREASE + 5)
HX = lambda z: max(f(CX, z) + f(RX, z) + 0.004, 0.176)
def HZ(z, back): return max(f(RZ, z) + 0.004, 0.106) * (1.07 if back else 1.0)
def hip_pt(s, j, z):                               # full-depth ellipse; only the centre front/back dip in near the crotch (no shelf)
    th = math.pi * j / NO; c = math.cos(th); e = min(th, math.pi - th)
    dip = 1 - (1 - 0.866 * f(RZ, ZC) / HZ(ZC, c < 0)) * math.exp(-(e / 0.30) ** 2) * (1 - sm((z - ZC) / 0.10))
    return Vector((s * HX(z) * math.sin(th), -HZ(z, c < 0) * c * dip, z))
def flare(z): return 1 + 0.05 * sm((0.35 - z) / 0.35)
def leg_pt(s, k, z):
    a = 2 * math.pi * k / M; fl = flare(z); rx, rz = f(RX, z) * fl, f(RZ, z) * fl
    p = Vector((s * (f(CX, z) + rx * math.sin(a)), -rz * math.cos(a), z))
    t = sm((z - (ZC - 0.10)) / 0.10)
    if k in INNER_SET:                             # the inner arc flattens onto the x=0 plane: at ZC it IS the crotch curve
        p.x = lerp(p.x, 0.0, t)
    else:                                          # the outer arc blends into the hip ring
        j = OUTER.index(k); p = p.lerp(hip_pt(s, j, ZC), t)
    return p
INNER_SET = set(INNER)
zl = list(np.arange(0.0, ZC - 1e-6, P["dz"])); zh = list(np.linspace(ZC, 1.075, int(round((1.075 - ZC) / P["dz"])) + 1))
bm = bmesh.new(); V = {}                           # V[key] -> BMVert
def nv(key, co):
    if key not in V: V[key] = bm.verts.new(co)
    return V[key]
def ring_leg(s, i):                                # i < len(zl): row of leg s
    return [nv(("L", s, i, k), leg_pt(s, k, zl[i])) for k in range(M)]
def ring_zc(s):                                    # the crotch row: shared inner arc, per-side outer arc
    out = []
    for k in range(M):
        if k in INNER_SET: out.append(nv(("C", k), leg_pt(s, k, ZC)))
        else: out.append(nv(("H", s, 0, OUTER.index(k)), hip_pt(s, OUTER.index(k), ZC)))
    return out
def hip_row(s, h):                                 # h >= 0 index in zh; j=0 and j=NO are the shared centre front / back
    row = []
    for j in range(NO + 1):
        if h == 0: k = OUTER[j]; row.append(nv(("C", k), leg_pt(s, k, ZC)) if k in INNER_SET else nv(("H", s, 0, j), hip_pt(s, j, ZC)))
        elif j == 0: row.append(nv(("CF", h), hip_pt(1, 0, zh[h])))
        elif j == NO: row.append(nv(("CB", h), hip_pt(1, NO, zh[h])))
        else: row.append(nv(("H", s, h, j), hip_pt(s, j, zh[h])))
    return row
def quad(a, b, c, d):
    try: bm.faces.new((a, b, c, d))
    except ValueError: pass
for s in (-1, 1):
    rows = [ring_leg(s, i) for i in range(len(zl))] + [ring_zc(s)]
    for r0, r1 in zip(rows[:-1], rows[1:]):
        for k in range(M): quad(r0[k], r0[(k + 1) % M], r1[(k + 1) % M], r1[k])
    hr = [hip_row(s, h) for h in range(len(zh))]
    for r0, r1 in zip(hr[:-1], hr[1:]):
        for j in range(NO): quad(r0[j], r0[j + 1], r1[j + 1], r1[j])
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
me = bpy.data.meshes.new("trouser"); bm.to_mesh(me); bm.free()
ob = bpy.data.objects.new("trouser", me); bpy.context.collection.objects.link(ob)
LOG["verts0"] = len(me.vertices)

# per-vertex roles (from the generating keys we lost in to_mesh: recompute by geometry)
def role(v):
    """('leg', s, a) or ('hip', s, theta) from the rest position"""
    x, y, z = v
    s = 1 if x >= 0 else -1
    if z < ZC - 1e-4: return "leg", s, math.atan2(s * (x - s * f(CX, z)), -y) % (2 * math.pi)
    th = math.atan2(abs(x) / HX(z), -y / HZ(z, y > 0)); return "hip", s, th
REST = [v.co.copy() for v in me.vertices]

# ---------- 2. crotch relax (the inner-arc blend leaves a crease line at ZC), light Laplacian
bm = bmesh.new(); bm.from_mesh(me)
reg = [v for v in bm.verts if abs(v.co.x) < 0.09 and ZC - 0.07 < v.co.z < ZC + 0.06]
for it in range(25):
    new = {}
    for v in reg:
        w = sm((0.09 - abs(v.co.x)) / 0.04) * sm((v.co.z - (ZC - 0.07)) / 0.03) * sm((ZC + 0.06 - v.co.z) / 0.03)
        c = sum((e.other_vert(v).co for e in v.link_edges), Vector()) / max(1, len(v.link_edges)); new[v] = v.co.lerp(c, 0.5 * w)
    for v, c in new.items(): v.co = c
bm.to_mesh(me); bm.free()

# ---------- 3. pleats (real folds, opening towards the fly) + pressed creases + fly placket, on the rest shape
def outward(v):
    r, s, ang = role(v)
    if r == "leg": n = Vector((s * math.sin(ang), -math.cos(ang), 0))
    else: n = Vector((s * math.sin(ang), -math.cos(ang), 0))
    return n.normalized()
CR = []                                            # (vertex index) lying on a sharp line, for edge creases
for i, v in enumerate(me.vertices):
    r, s, ang = role(v.co); d = 0.0; z = v.co.z
    if r == "leg":
        da = (ang + math.pi) % (2 * math.pi) - math.pi                    # 0 = front
        db = (ang - math.pi + math.pi) % (2 * math.pi) - math.pi          # 0 = back
        step = 2 * math.pi / M
        if z < 0.80: d += P["crease"] * max(0, 1 - abs(da) / (1.5 * step)) * sm((z - 0.05) / 0.05)
        if z < 0.70: d += 0.7 * P["crease"] * max(0, 1 - abs(db) / (1.5 * step)) * sm((z - 0.05) / 0.05)
    else:
        th = ang; step = math.pi / NO
        for ip, jp in enumerate(J_PLEAT):            # v10b: a pressed pleat = a step (the fold lies over the cloth towards the side seam) + a thin shadow groove on the fly side
            thp = math.pi * jp / NO; u = (th - thp) / step
            prof = max(0, 1 - max(u, 0) / 4.0) if u > -0.3 else (-0.45 * max(0, 1 - abs(u + 1) ) if u > -2 else 0)
            d += P["pleat"] * (1.0, 0.6)[ip] * prof * sm((z - 0.86) / 0.13) * (1 - sm((z - 0.975) / 0.03))   # v10c: fade out under the waistband (no ridges poking through)
        if 0.84 < z < 1.0 and s > 0 and th < 4.5 * step:                 # fly placket: the left front overlaps by 1.8 mm
            d += 0.0018 * sm((z - 0.84) / 0.02)
        # the inner pleat continues into the leg crease below the hip
        thp = math.pi * J_CREASE / NO
        if z < ZC + 0.05 and abs(th - thp) < 1.5 * step: d += P["crease"] * (1 - abs(th - thp) / (1.5 * step))
    if d: v.co += outward(v.co) * d
me.update()

# ---------- 4. mannequin collider (hidden; legs + hips), then cloth sim pinned at the waist
def tube_obj(name, z0, z1, ring, ny=60, na=48):
    b_ = bmesh.new(); rows = []
    for i in range(ny + 1):
        z = z0 + (z1 - z0) * i / ny; rows.append([b_.verts.new(ring(z, 2 * math.pi * k / na)) for k in range(na)])
    for i in range(ny):
        for k in range(na): b_.faces.new((rows[i][k], rows[i][(k + 1) % na], rows[i + 1][(k + 1) % na], rows[i + 1][k]))
    b_.faces.new(rows[0][::-1]); b_.faces.new(rows[-1]); me_ = bpy.data.meshes.new(name); b_.to_mesh(me_); b_.free()
    o = bpy.data.objects.new(name, me_); bpy.context.collection.objects.link(o); return o
LEGR = [0, 0.1, 0.45, 0.7, 0.8]; LEGV = [0.042, 0.047, 0.056, 0.064, 0.070]   # v10b: a gap between the legs, the crotch hangs free
parts = [tube_obj("mq_leg%d" % s, 0.02, 0.82, lambda z, a, s=s: (s * lerp(0.085, 0.09, z) + float(np.interp(z, LEGR, LEGV)) * math.sin(a), -float(np.interp(z, LEGR, LEGV)) * 0.95 * math.cos(a), z)) for s in (-1, 1)]
parts.append(tube_obj("mq_hip", 0.80, 1.13, lambda z, a: (lerp(0.150, 0.168, sm((z - 0.72) / 0.14)) * (1 - 0.06 * sm((z - 1.0) / 0.12)) * math.sin(a),
                                                          -(0.094 if math.cos(a) > 0 else 0.104) * math.cos(a) * lerp(0.9, 1.0, sm((z - 0.72) / 0.1)), z)))
bpy.ops.object.select_all(action='DESELECT')
for o in parts: o.select_set(True)
bpy.context.view_layer.objects.active = parts[0]; bpy.ops.object.join(); mq = bpy.context.active_object; mq.name = "mannequin"
rm = mq.modifiers.new("rm", "REMESH"); rm.mode = 'VOXEL'; rm.voxel_size = 0.008; bpy.ops.object.modifier_apply(modifier="rm")
co = mq.modifiers.new("col", "COLLISION"); mq.collision.thickness_outer = 0.004; mq.collision.cloth_friction = 8
mq.hide_render = True; mq.display_type = 'WIRE'
if P["sim"]:
    pin = ob.vertex_groups.new(name="pin")
    for v in me.vertices: pin.add([v.index], sm((v.co.z - 0.70) / 0.14), 'REPLACE')   # v10b: the designed hip keeps its shape, legs hang
    cl = ob.modifiers.new("Cloth", "CLOTH"); s_ = cl.settings
    s_.quality = 8; s_.mass = 0.32; s_.air_damping = 2
    s_.tension_stiffness = 50; s_.compression_stiffness = 50; s_.shear_stiffness = 25; s_.bending_stiffness = 25
    s_.tension_damping = 5; s_.compression_damping = 5; s_.bending_damping = 1
    s_.vertex_group_mass = "pin"; s_.pin_stiffness = 1
    cl.collision_settings.use_collision = True; cl.collision_settings.distance_min = 0.003
    cl.collision_settings.use_self_collision = False
    sc = bpy.context.scene; sc.frame_start = 1; sc.frame_end = P["frames"]; cl.point_cache.frame_start = 1; cl.point_cache.frame_end = P["frames"]
    t = time.time()
    with bpy.context.temp_override(scene=sc, active_object=ob, point_cache=cl.point_cache): bpy.ops.ptcache.bake(bake=True)
    LOG["bake_s"] = round(time.time() - t, 1)
    sc.frame_set(P["frames"]); bpy.context.view_layer.objects.active = ob; bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True)
    bpy.ops.object.modifier_apply(modifier="Cloth"); sc.frame_set(1)
    for g in list(ob.vertex_groups): ob.vertex_groups.remove(g)
# 4b. reinforce the sharp lines after the sim (the solver softens them), using the rest-pose roles
for i, v in enumerate(me.vertices):
    r, s, ang = role(REST[i]); z = REST[i].z
    if r == "leg":
        da = abs((ang + math.pi) % (2 * math.pi) - math.pi)
        if da < 0.5 * 2 * math.pi / M and 0.06 < z < 0.80: CR.append(i)
        db = abs((ang - math.pi + math.pi) % (2 * math.pi) - math.pi)
        if db < 0.5 * 2 * math.pi / M and 0.06 < z < 0.70: CR.append(i)
    else:
        for jp in J_PLEAT:
            if abs(ang - math.pi * jp / NO) < 0.5 * math.pi / NO and 0.90 < z < 1.02: CR.append(i)
CRS = set(CR)

# ---------- 5. metric UVs (as v9: around each leg centre, cut at the inseam), smooth shading, edge creases, subdivision
uvl = me.uv_layers.new(name="UVMap"); TILE = P["tile"]
for poly in me.polygons:
    c = poly.center; sgn = 1 if c.x >= 0 else -1; uu = []
    for li in poly.loop_indices:
        v = REST[me.loops[li].vertex_index]
        cx = sgn * f(CX, min(v.z, 1.0))
        a = math.atan2(sgn * (v.x - cx), -v.y); a2 = (a + math.pi / 2) % (2 * math.pi)
        r = (f(RX, v.z) + f(RZ, v.z)) / 2; uu.append([a2 * r / TILE, v.z / TILE])
    us = [q[0] for q in uu]
    if max(us) - min(us) > 1.5:
        per = 2 * math.pi * 0.1 / TILE; mid = (max(us) + min(us)) / 2
        for q in uu:
            if q[0] < mid: q[0] += per
    for li, q in zip(poly.loop_indices, uu): uvl.data[li].uv = (q[0] * sgn, q[1])
for p in me.polygons: p.use_smooth = True
bm = bmesh.new(); bm.from_mesh(me)
lay = bm.edges.layers.float.get("crease_edge") or bm.edges.layers.float.new("crease_edge")
nc = 0
for e in bm.edges:
    a, b = e.verts
    if a.index in CRS and b.index in CRS and abs(a.co.z - b.co.z) > 0.6 * abs(a.co.x - b.co.x) + 0.0005: e[lay] = 0.9; nc += 1
    elif e.is_boundary: e[lay] = 1.0
bm.to_mesh(me); bm.free(); LOG["creased_edges"] = nc
sd = ob.modifiers.new("subd", "SUBSURF"); sd.levels, sd.render_levels = P["subd"]; sd.use_creases = True

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
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.3
        nt.links.new(tc.outputs["UV"], w.inputs["Vector"]); nt.links.new(w.outputs[1], bp.inputs["Height"]); nt.links.new(bp.outputs[0], b.inputs["Normal"])
    return m
C = P["color"]
cloth = mat("drill", lin(C), rough=0.82, sheen=0.4); dark = mat("drill_dark", lin(C, 0.86)); mouth = mat("mouth", lin(C, 0.22), twill=False, sheen=0)
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
def band(name, zs, offs, m_, s=0, N=160, zray=None, smooth=0):
    b_ = bmesh.new(); rows = []
    base = [surf(zray if zray is not None else zs[0], 2 * math.pi * k / N, s) for k in range(N)]
    if smooth:                                      # v10b: a pressed band does not follow the pleat ridges underneath; smooth its radius
        r = np.array([math.hypot(p.x, p.y) for p, n in base]); rs = np.array([np.mean(np.take(r, range(k - smooth, k + smooth + 1), mode='wrap')) for k in range(N)])
        base = [(Vector((p.x, p.y, p.z)) * (rs[k] / r[k]), Vector((p.x, p.y, 0)).normalized()) for k, (p, n) in enumerate(base)]
    for z, off in zip(zs, offs):
        row = []
        for k in range(N):
            p, n = base[k] if zray is not None else surf(z, 2 * math.pi * k / N, s); v = b_.verts.new(p + n * off); v.co.z = z; row.append(v)
        rows.append(row)
    for i in range(len(rows) - 1):
        for k in range(N): b_.faces.new((rows[i][k], rows[i][(k + 1) % N], rows[i + 1][(k + 1) % N], rows[i + 1][k]))
    me_ = bpy.data.meshes.new(name); b_.to_mesh(me_); b_.free(); o = link(bpy.data.objects.new(name, me_), m_)
    for p in o.data.polygons: p.use_smooth = True
    so = o.modifiers.new("sol", "SOLIDIFY"); so.thickness = 0.0018; so.offset = -1; return o
wb = band("waistband", [1.002, 1.007, 1.074, 1.078], [0.0012, 0.0030, 0.0030, 0.0022], dark, zray=1.045, smooth=8)   # v10b: nearly flush, crisp top
for a in (-1.32, -0.88, -0.46, 0.46, 0.88, 1.32, math.pi - 0.3, math.pi + 0.3, math.pi):            # belt loops, 1 x 4.6 cm, standing proud
    p, n = surf(1.046, a, 0); box("loop", p + n * 0.0042, n, (0.0085, 0.044, 0.0020), dark, bevel=0.0008)
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
    lip = ribbon("pocket_lip", path, [(-0.009, 0.0004), (-0.005, 0.0007), (-0.0025, 0.0011), (-0.0010, 0.0014), (-0.0002, 0.0012), (0.0, 0.0008)], dark, s)
    for i, row in enumerate([lip.data.vertices[j * 6:(j + 1) * 6] for j in range(41)]):            # flatten the lip into the cloth at both ends of the opening
        f_ = fade(i)
        for v in row:
            p, n = bvh.find_nearest(v.co)[:2]; v.co = p + (v.co - p) * (0.35 + 0.65 * f_)
    gap = ribbon("pocket_gap", path[3:-3], [(0.0, 0.0008), (0.0012, 0.0006)], mouth, s)
    mo = [surf(z, a, 0)[0] for z, a in (path[0], path[-1])]
    for z, a in (path[1], path[-2]):                                                                   # bar-tacks: a short flat bar of dense stitches across the end of the opening
        q, n = surf(z, a, 0); box("bartack", q + n * 0.0009, n, (0.006, 0.0018, 0.0008), thread, bevel=0.0003)
def onsurf(z, a0, a1, off, n=14):
    return [surf(z, a0 + (a1 - a0) * k / (n - 1), 0) for k in range(n)]
for s in (-1, 1):                                                                                     # back welt pockets: welts FOLLOW the curve of the seat
    a = math.pi - s * 0.62; half = 0.06 / 0.18
    for z in (0.9605, 0.9515):
        pts = [p + n * 0.0024 for p, n in onsurf(z, a - half, a + half, 0)]; curve("welt", pts, 0.0042, dark)
    curve("slit", [p + n * 0.0038 for p, n in onsurf(0.956, a - half * 0.98, a + half * 0.98, 0)], 0.0011, mouth)
    for e in (a - half, a + half): q, n = surf(0.956, e, 0); box("bartack", q + n * 0.003, n, (0.0026, 0.012, 0.0012), thread, bevel=0.0005)
    p, n = surf(0.944, a, 0); disc("bbutton", p + n * 0.0035, n, 0.0066, 0.003, horn)
def cuff(s, zs=(0.003, 0.0068, 0.0432, 0.047), offs=(0.0010, 0.0032, 0.0032, 0.0010), N=144, zray=0.028):   # v10: a clean smoothed ring, crisp top edge
    cx = s * f(CX, zray); pts = [surf(zray, 2 * math.pi * k / N, s)[0] for k in range(N)]
    r = np.array([math.hypot(p.x - cx, p.y) for p in pts]); rs = np.array([np.mean(np.take(r, range(k - 9, k + 10), mode='wrap')) for k in range(N)])
    b_ = bmesh.new(); rows = []
    for z, off in zip(zs, offs):
        rows.append([b_.verts.new(Vector((cx, 0, z)) + Vector((s * math.sin(2 * math.pi * k / N), -math.cos(2 * math.pi * k / N), 0)) * (rs[k] + off)) for k in range(N)])
    for i in range(len(rows) - 1):
        for k in range(N): b_.faces.new((rows[i][k], rows[i][(k + 1) % N], rows[i + 1][(k + 1) % N], rows[i + 1][k]))
    b_.normal_update(); lay_ = b_.edges.layers.float.new("crease_edge")
    for e in b_.edges:
        if abs(e.verts[0].co.z - e.verts[1].co.z) < 1e-6 and e.verts[0].co.z > 0.04: e[lay_] = 0.8
    me_ = bpy.data.meshes.new("cuff"); b_.to_mesh(me_); b_.free(); o = link(bpy.data.objects.new("cuff", me_), dark)
    for p in o.data.polygons: p.use_smooth = True
    sd_ = o.modifiers.new("subd", "SUBSURF"); sd_.levels, sd_.render_levels = 1, 2; sd_.use_creases = True
    so_ = o.modifiers.new("sol", "SOLIDIFY"); so_.thickness = 0.0015; so_.offset = -1
    return o
for s in (-1, 1): cuff(s)
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
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "trouser10_test.blend"))
bpy.ops.object.select_all(action='DESELECT')
for o in [ob] + list(coll.objects): o.select_set(True)
gl = os.path.join(OUT, "trouser10.glb"); t = time.time()
bpy.ops.export_scene.gltf(filepath=gl, use_selection=True, export_apply=True, export_format='GLB', export_yup=True)
LOG.update(glb_s=round(time.time() - t, 1), glb_mb=round(os.path.getsize(gl) / 1e6, 2), verts=len(me.vertices), total_s=round(time.time() - T0, 1))
print(LOG)
