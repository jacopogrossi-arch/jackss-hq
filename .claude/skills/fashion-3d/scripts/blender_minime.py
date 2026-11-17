# blender_minime.py (17/11/2026): "mini-me", a stylised toy-figure Jacopo modelled in Blender (no glasses): sculpted head, 3D eyes, brows, nose, ears, a mouth (closed or open), real hair strands
# swept up in a quiff, black tee with folds, indigo selvage jeans, Texan boots. Exports mini_closed.glb and mini_open.glb (the same figure, mouth shut / open) + preview PNGs.
# Headless: "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" -b -P blender_minime.py   (env MINI_OUT = output folder, MINI_PREVIEW=1 to render previews)
import bpy, bmesh, math, os, random, time
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

OUT = os.environ.get("MINI_OUT", r"D:\ClaudeCodeTest\videos\_bench\minime")
os.makedirs(OUT, exist_ok=True)
PREVIEW = os.environ.get("MINI_PREVIEW", "1") == "1"
T0 = time.time()
sm = lambda x: (lambda t: t * t * (3 - 2 * t))(min(1.0, max(0.0, x)))
lerp = lambda a, b, t: a + (b - a) * t


def hexc(h, a=1.0):
    h = h.lstrip("#"); return tuple(((int(h[i:i + 2], 16) / 255.0) ** 2.2) for i in (0, 2, 4)) + (a,)


def clear():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.images, bpy.data.textures):
        for d in list(coll):
            if d.users == 0: coll.remove(d)


MATS = {}


def material(name, color, rough=0.6, metal=0.0, image=None):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = hexc(color); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if image is not None:
        t = m.node_tree.nodes.new("ShaderNodeTexImage"); t.image = image; m.node_tree.links.new(t.outputs["Color"], b.inputs["Base Color"])
    MATS[name] = m; return m


def add(name, mesh, mat=None, loc=(0, 0, 0), rot=(0, 0, 0), smooth=True, subd=0, crease=None):
    o = bpy.data.objects.new(name, mesh); bpy.context.scene.collection.objects.link(o); o.location = loc; o.rotation_euler = rot
    if mat: o.data.materials.append(mat)
    if smooth:
        for p in o.data.polygons: p.use_smooth = True
    if subd:
        md = o.modifiers.new("subd", "SUBSURF"); md.levels = subd; md.render_levels = subd
    return o


def loft_z(name, rings, sides=28, mat=None, loc=(0, 0, 0), rot=(0, 0, 0), subd=2, caps=(True, True)):
    """rings: (z, cx, cy, rx, ry), a closed tube along Z; caps closed."""
    bm = bmesh.new(); rows = []
    for (z, cx, cy, rx, ry) in rings:
        rows.append([bm.verts.new((cx + rx * math.cos(2 * math.pi * i / sides), cy + ry * math.sin(2 * math.pi * i / sides), z)) for i in range(sides)])
    for r in range(len(rows) - 1):
        for i in range(sides): bm.faces.new((rows[r][i], rows[r][(i + 1) % sides], rows[r + 1][(i + 1) % sides], rows[r + 1][i]))
    if caps[0]: bm.faces.new(rows[0][::-1])
    if caps[1]: bm.faces.new(rows[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:]); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    return add(name, me, mat, loc, rot, True, subd)


def loft_y(name, rings, sides=28, mat=None, loc=(0, 0, 0), subd=2):
    """rings: (y, cx, cz, rx, rz), a closed tube along Y (toes, feet)."""
    bm = bmesh.new(); rows = []
    for (y, cx, cz, rx, rz) in rings:
        rows.append([bm.verts.new((cx + rx * math.cos(2 * math.pi * i / sides), y, cz + rz * math.sin(2 * math.pi * i / sides))) for i in range(sides)])
    for r in range(len(rows) - 1):
        for i in range(sides): bm.faces.new((rows[r][i], rows[r][(i + 1) % sides], rows[r + 1][(i + 1) % sides], rows[r + 1][i]))
    bm.faces.new(rows[0][::-1]); bm.faces.new(rows[-1]); bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); return add(name, me, mat, loc, (0, 0, 0), True, subd)


def ellipsoid(name, r, mat, loc, scale=(1, 1, 1), rot=(0, 0, 0), subd=1, seg=24):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=r)
    for v in bm.verts: v.co.x *= scale[0]; v.co.y *= scale[1]; v.co.z *= scale[2]
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); return add(name, me, mat, loc, rot, True, subd)


def curve(name, pts, mat, depth=0.0013, radii=None, loc=(0, 0, 0), res=4, closed=False):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = depth; cu.bevel_resolution = res; cu.use_fill_caps = True; cu.resolution_u = 6
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1)
    for i, p in enumerate(pts):
        bp = sp.bezier_points[i]; bp.co = p; bp.handle_left_type = bp.handle_right_type = "AUTO"
        if radii: bp.radius = radii[i]
    o = bpy.data.objects.new(name, cu); bpy.context.scene.collection.objects.link(o); o.location = loc; o.data.materials.append(mat); return o


def noise_displace(o, strength, size):
    t = bpy.data.textures.new(o.name + "_n", "CLOUDS"); t.noise_scale = size
    md = o.modifiers.new("fold", "DISPLACE"); md.texture = t; md.strength = strength; md.mid_level = 0.5
    o.modifiers.move(len(o.modifiers) - 1, 0)       # displace first, then subdivide


# ------------------------------------------------------------------------------------------------ the face texture (skin, stubble, blush, freckles)
def skin_image():
    S = 1024; yy, xx = np.mgrid[0:S, 0:S].astype(np.float32) / S
    base = np.array([0.88, 0.68, 0.53], np.float32); img = np.ones((S, S, 3), np.float32) * base
    rng = np.random.default_rng(3)
    jaw = np.clip((0.40 - yy) / 0.22, 0, 1) * (np.abs(xx - 0.5) < 0.36)                     # v small = low on the head
    img *= (1 - 0.10 * jaw[..., None])
    for _ in range(26000):                                                                      # stubble
        x, y = rng.random(), rng.random() * 0.36 + 0.14
        if abs(x - 0.5) < 0.30 and (y < 0.32 or abs(x - 0.5) < 0.10):
            xi, yi = int(x * S), int(y * S); img[yi:yi + 2, xi:xi + 2] *= 0.82
    for sd in (-1, 1):                                                                            # cheeks
        d = ((xx - (0.5 + sd * 0.17)) ** 2 + (yy - 0.43) ** 2) / 0.012
        img += (np.exp(-d)[..., None]) * np.array([0.06, -0.02, -0.02], np.float32)
    for _ in range(160):                                                                          # a few freckles
        x, y = 0.5 + (rng.random() - 0.5) * 0.4, 0.45 + rng.random() * 0.12
        xi, yi = int(x * S), int(y * S); img[yi:yi + 3, xi:xi + 3] *= 0.93
    img = np.clip(img, 0, 1); rgba = np.dstack([img, np.ones((S, S), np.float32)])
    im = bpy.data.images.new("skin", S, S); im.pixels = rgba.flatten().tolist(); im.pack(); return im


# ------------------------------------------------------------------------------------------------ build
def build(open_mouth, preview_prefix=None):
    clear(); MATS.clear(); random.seed(11)
    SKIN = material("skin", "#dfa97f", 0.55, image=skin_image())
    EYEW = material("eye_white", "#f4f1ea", 0.2); IRIS = material("iris", "#5e8450", 0.25); PUPIL = material("pupil", "#0c0f0a", 0.2); GLINT = material("glint", "#ffffff", 0.05)
    HAIR = material("hair", "#4b3322", 0.5); HAIR2 = material("hair2", "#5f4029", 0.5); HAIR3 = material("hair3", "#3a2618", 0.55)
    BROW = material("brow", "#3a2416", 0.6); LIP = material("lip", "#a14f48", 0.4); MOUTH = material("mouth", "#4a1a18", 0.5); TEETH = material("teeth", "#f2eee4", 0.3); TONGUE = material("tongue", "#c8626a", 0.4)
    TEE = material("tee", "#171717", 0.85); JEAN = material("jeans", "#2b3c68", 0.9); SELV = material("selvage", "#b8432a", 0.7); BOOT = material("boot", "#5a3820", 0.4); SOLE = material("sole", "#171210", 0.7)
    BELT = material("belt", "#2a1c12", 0.5); SILVER = material("silver", "#cfd3da", 0.25, 0.9)
    D = 0.0   # (kept for symmetry)

    # ---------------- head: an ellipsoid deformed into a face shape (jaw, cheekbones, brow, chin)
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=5, radius=1.0)
    drop = 0.0065 if open_mouth else 0.0
    for v in bm.verts:
        x, y, z = v.co.x, v.co.y, v.co.z; fy = -y                                                     # fy > 0 = toward the face (-Y)
        X, Y, Z = x * 0.050, y * 0.056, z * 0.060
        lo = sm((-z - 0.05) / 0.9)                                                                      # 0 at the equator, 1 at the chin
        X *= 1 - 0.34 * lo ** 1.4                                                                        # narrower jaw
        Y *= 1 - 0.12 * lo; Z -= 0.0035 * lo * fy                                                       # a firm chin line
        X *= 1 + 0.05 * sm(1 - abs(z + 0.05) / 0.35) * sm(fy)                                          # cheekbones
        Y -= 0.003 * sm(fy) * sm((z - 0.15) / 0.5)                                                      # forehead pushed forward
        Y -= 0.002 * sm(fy) * sm(1 - abs(z + 0.4) / 0.2)                                               # a little chin
        Z -= drop * sm(((-0.032 - Z) / 0.02)) * sm((fy * 0.056 + 0.01) / 0.03)                       # jaw drop (open mouth)
        v.co = (X, Y, Z)
    me = bpy.data.meshes.new("head"); bm.to_mesh(me)
    # front-projected UVs
    uvl = me.uv_layers.new(name="UVMap")
    for p in me.polygons:
        for li in p.loop_indices:
            c = me.vertices[me.loops[li].vertex_index].co; uvl.data[li].uv = (0.5 + c.x / 0.11, 0.5 + c.z / 0.13)
    head = add("head", me, SKIN, (0, 0, 0), smooth=True, subd=1)
    bvh = BVHTree.FromBMesh(bm)
    surf = lambda x, z: (lambda h: h[0] if h[0] else Vector((x, 0.0, z)))(bvh.ray_cast(Vector((x, -0.2, z)), Vector((0, 1, 0))))
    parts = [head]
    # ---------------- eyes (3D): white globe, green iris, pupil, a glint, a soft upper lid
    for sd in (-1, 1):
        ex, ez = sd * 0.0215, 0.009; sp = surf(ex, ez); cy = sp.y + 0.0042
        parts.append(ellipsoid("eye%d" % sd, 0.0108, EYEW, (ex, cy, ez), subd=1))
        parts.append(ellipsoid("iris%d" % sd, 0.0066, IRIS, (ex, cy - 0.0089, ez), (1, 0.32, 1), subd=1))
        parts.append(ellipsoid("pupil%d" % sd, 0.0031, PUPIL, (ex, cy - 0.0103, ez), (1, 0.3, 1), subd=1, seg=16))
        parts.append(ellipsoid("glint%d" % sd, 0.0012, GLINT, (ex + 0.0022, cy - 0.0112, ez + 0.0028), (1, 0.4, 1), subd=0, seg=12))
        bm2 = bmesh.new(); bmesh.ops.create_uvsphere(bm2, u_segments=24, v_segments=14, radius=0.0116)
        bmesh.ops.delete(bm2, geom=[f for f in bm2.faces if f.calc_center_median().z < 0.0012], context="FACES")
        me2 = bpy.data.meshes.new("lid%d" % sd); bm2.to_mesh(me2); bm2.free(); lid = add("lid%d" % sd, me2, SKIN, (ex, cy, ez + 0.0006), subd=1); lid.rotation_euler = (math.radians(-12), 0, 0); parts.append(lid)
        # eyebrow: thick, arched
        pts = []
        for k in range(5):
            u = k / 4; bx = sd * lerp(0.0085, 0.0365, u); bz = 0.0295 + 0.0048 * math.sin(u * math.pi) - 0.0012 * u; s = surf(bx, bz)
            pts.append((bx, s.y - 0.0007, bz))
        parts.append(curve("brow%d" % sd, pts, BROW, depth=0.0024, radii=[0.7, 1.0, 1.0, 0.9, 0.55]))
        # ear
        ea = ellipsoid("ear%d" % sd, 0.01, SKIN, (sd * 0.0485, 0.004, -0.0035), (0.55, 0.9, 1.4), subd=1); parts.append(ea)
    # ---------------- nose and mouth
    ns = surf(0, -0.012); parts.append(ellipsoid("nose", 0.01, SKIN, (0, ns.y + 0.0038, -0.0125), (0.82, 1.0, 1.2), subd=1))
    parts.append(ellipsoid("tip", 0.0072, SKIN, (0, ns.y - 0.0022, -0.0185), (1.0, 1.0, 0.95), subd=1))
    zc = -0.0345 - drop * 0.55
    def lip(name, z0, zc_amp, x0, mat, depth, dz):
        pts = []
        for k in range(7):
            u = k / 6; bx = lerp(-x0, x0, u); bz = z0 + zc_amp * (1 - (2 * u - 1) ** 2) * 1.0 + dz * (1 - (2 * u - 1) ** 2); s = surf(bx, bz); pts.append((bx, s.y - 0.0004, bz))
        return curve(name, pts, mat, depth=depth, radii=[0.45, 0.85, 1.0, 1.0, 1.0, 0.85, 0.45][:7])
    if not open_mouth:
        parts.append(lip("lips", -0.0335, -0.0042, 0.0185, LIP, 0.0016, 0.0))                           # a gentle smile
    else:
        parts.append(lip("upperlip", -0.0305, 0.0012, 0.0185, LIP, 0.0015, 0.0))
        parts.append(lip("lowerlip", -0.0305 - drop * 0.95, -0.0055 - drop * 0.4, 0.0165, LIP, 0.0016, 0.0))
        s = surf(0, zc); cav = ellipsoid("cavity", 0.01, MOUTH, (0, s.y - 0.0006, zc + 0.0005), (1.55, 0.18, 0.62 + drop * 60), subd=1); parts.append(cav)
        parts.append(ellipsoid("teeth", 0.01, TEETH, (0, s.y - 0.0011, -0.0305 - 0.0012), (1.15, 0.12, 0.2), subd=1))
        parts.append(ellipsoid("tongue", 0.01, TONGUE, (0, s.y - 0.0011, zc - 0.003), (0.8, 0.12, 0.2), subd=1))
    # ---------------- hair: a scalp cap under real strands combed up and back (a quiff), short on the sides and back
    hairline = lambda ph, zz: 0.035 - 0.021 * sm(abs(ph) / 1.5) - 0.025 * sm((abs(ph) - 2.0) / 1.0)      # phi = angle from the front
    bmc = bmesh.new(); bmc.from_mesh(me)
    dele = []
    for f in bmc.faces:
        c = f.calc_center_median(); ph = math.atan2(c.x, -c.y)
        if c.z < hairline(ph, c.z) - 0.001: dele.append(f)
    bmesh.ops.delete(bmc, geom=dele, context="FACES")
    for v in bmc.verts:
        n = v.normal; v.co += n * 0.0016
    mc = bpy.data.meshes.new("scalp"); bmc.to_mesh(mc); bmc.free(); parts.append(add("scalp", mc, HAIR3, (0, 0, 0), smooth=True, subd=1))
    cu = bpy.data.curves.new("hair", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.0019; cu.bevel_resolution = 2; cu.resolution_u = 5; cu.use_fill_caps = False
    up = Vector((0, 0, 1)); back = Vector((0, 1, 0)); n_strands = 0
    rng = random.Random(5)
    for _ in range(2600):
        # a random direction from the head centre -> a point on the scalp
        th = math.acos(1 - rng.random() * 1.45)                  # 0 = straight up
        ph = rng.uniform(-math.pi, math.pi)
        d = Vector((math.sin(th) * math.sin(ph), -math.sin(th) * math.cos(ph), math.cos(th)))
        hit = bvh.ray_cast(Vector((0, 0, 0)), d, 0.2)
        if not hit[0]: continue
        p, n = hit[0], hit[1]
        if p.z < hairline(ph, p.z): continue
        if rng.random() > 0.17: continue
        front = sm((-p.y + 0.01) / 0.05) * sm((p.z - 0.02) / 0.03)
        top = sm((p.z - 0.03) / 0.03)
        L = lerp(0.014, 0.034, top) * rng.uniform(0.8, 1.2) * lerp(1.0, 1.15, front)
        comb = (up * 0.95 + back * (0.25 + 0.5 * (1 - front)) + Vector((rng.uniform(-0.2, 0.2), -0.25 * front, 0))).normalized()
        side = (1 - top)
        dir0 = (n * (0.6 + 0.4 * top) + comb * (0.5 * top)).normalized()
        if side > 0.5: dir0 = (n * 0.6 + Vector((0, 0.3, -0.6)) * (1 - top)).normalized()
        a0 = p - n * 0.0015; a1 = p + dir0 * L * 0.35; a2 = a1 + (dir0 * 0.5 + comb * 0.6).normalized() * L * 0.4
        a3 = a2 + (comb * 0.6 + back * 0.6 * (1 - front) + Vector((0, 0.5, -0.15))).normalized() * L * 0.35
        sp = cu.splines.new("BEZIER"); sp.bezier_points.add(3)
        for i, (pp, r) in enumerate(zip((a0, a1, a2, a3), (1.0, 0.95, 0.7, 0.18))):
            bp = sp.bezier_points[i]; bp.co = pp; bp.radius = r; bp.handle_left_type = bp.handle_right_type = "AUTO"
        n_strands += 1
    ho = bpy.data.objects.new("hair", cu); bpy.context.scene.collection.objects.link(ho); ho.data.materials.append(HAIR); parts.append(ho)
    # ---------------- body
    HZ = 0.425; HY = -0.003
    for o in parts: o.location += Vector((0, HY, HZ))
    neck = loft_z("neck", [(0.338, 0, 0, 0.0158, 0.0168), (0.372, 0, 0, 0.0158, 0.0168)], 20, SKIN, subd=1)
    torso = loft_z("torso", [(0.205, 0, 0, 0.0505, 0.0305), (0.215, 0, 0, 0.0505, 0.0305), (0.245, 0, 0, 0.0545, 0.0322), (0.30, 0, 0, 0.0610, 0.0335), (0.335, 0, 0, 0.0625, 0.0318), (0.348, 0, 0, 0.0505, 0.0262), (0.353, 0, 0, 0.0215, 0.0180)], 32, TEE, subd=2)
    noise_displace(torso, 0.0011, 0.05)
    collar = loft_z("collar", [(0.341, 0, -0.0015, 0.0215, 0.0195), (0.352, 0, -0.0015, 0.0215, 0.0195), (0.352, 0, -0.0015, 0.0172, 0.0156), (0.341, 0, -0.0015, 0.0172, 0.0156)], 28, material("collar", "#262626", 0.8), subd=1, caps=(False, False))
    belt = loft_z("belt", [(0.208, 0, 0, 0.0522, 0.0322), (0.2205, 0, 0, 0.0522, 0.0322)], 32, BELT, subd=1)
    buckle = loft_z("buckle", [(0.2075, 0, 0, 0.009, 0.0016), (0.2215, 0, 0, 0.009, 0.0016)], 4, SILVER, loc=(0, -0.0332, 0), subd=0)
    hips = loft_z("hips", [(0.178, 0, 0, 0.0545, 0.0322), (0.20, 0, 0, 0.0528, 0.0315), (0.218, 0, 0, 0.0505, 0.0305)], 32, JEAN, subd=2)
    for sd in (-1, 1):
        # legs: boot-cut jeans, a red selvage line down the outer seam, a Texan boot
        leg = loft_z("leg%d" % sd, [(0.195, 0, 0, 0.0265, 0.0292), (0.14, 0, 0, 0.0248, 0.0275), (0.085, 0, 0, 0.0238, 0.0262), (0.066, 0, 0, 0.0262, 0.0285), (0.060, 0, 0, 0.0262, 0.0285)], 28, JEAN, loc=(sd * 0.0275, 0, 0), subd=2)
        noise_displace(leg, 0.0008, 0.04)
        sv = curve("selv%d" % sd, [(sd * (0.0275 + 0.0265), 0, 0.19), (sd * (0.0275 + 0.0248), 0, 0.14), (sd * (0.0275 + 0.0238), 0, 0.09), (sd * (0.0275 + 0.0262), 0, 0.062)], SELV, depth=0.0012)
        shaft = loft_z("shaft%d" % sd, [(0.0, 0, 0, 0.0225, 0.0255), (0.03, 0, 0, 0.0228, 0.026), (0.072, 0, 0, 0.0232, 0.0262)], 26, BOOT, loc=(sd * 0.0275, 0, 0), subd=2, caps=(False, False))
        foot = loft_y("foot%d" % sd, [(0.034, 0, 0.0125, 0.0215, 0.0125), (0.014, 0, 0.0145, 0.0242, 0.0145), (-0.020, 0, 0.0165, 0.0258, 0.0165), (-0.048, 0, 0.0125, 0.0215, 0.0122), (-0.066, 0, 0.0085, 0.0125, 0.0085), (-0.0765, 0, 0.0062, 0.0048, 0.0052)], 26, BOOT, loc=(sd * 0.0275, 0, 0.002), subd=2)
        heel = loft_z("heel%d" % sd, [(0.0, 0, 0.026, 0.017, 0.0105), (0.0185, 0, 0.026, 0.0175, 0.0115)], 20, SOLE, loc=(sd * 0.0275, 0, 0), subd=1)
        sole = loft_y("sole%d" % sd, [(0.020, 0, 0.0018, 0.0215, 0.0018), (-0.050, 0, 0.0018, 0.0245, 0.0018), (-0.076, 0, 0.0016, 0.0042, 0.0016)], 20, SOLE, loc=(sd * 0.0275, 0, 0), subd=1)
        # arms: a short sleeve, a skin forearm, a mitten hand with a thumb
        sx = sd * 0.0655
        sleeve = loft_z("sleeve%d" % sd, [(0.012, 0, 0, 0.0225, 0.0235), (0, 0, 0, 0.0255, 0.027), (-0.022, 0, 0, 0.0268, 0.0278), (-0.048, 0, 0, 0.0300, 0.0305)], 26, TEE, loc=(sx, 0, 0.335), rot=(0, sd * 0.22, 0), subd=2, caps=(True, True))
        noise_displace(sleeve, 0.0009, 0.04)
        arm = loft_z("arm%d" % sd, [(-0.040, 0, 0, 0.0128, 0.0132), (-0.085, 0, 0, 0.0118, 0.0122), (-0.108, 0, 0, 0.0126, 0.0118), (-0.122, 0, 0, 0.0142, 0.0095), (-0.140, 0, 0, 0.0128, 0.0078), (-0.151, 0, 0, 0.0070, 0.0050), (-0.1545, 0, 0, 0.0025, 0.0022)], 22, SKIN, loc=(sx, 0, 0.335), rot=(0, sd * 0.22, 0), subd=2)
        thumb = ellipsoid("thumb%d" % sd, 0.01, SKIN, (sx + sd * 0.0095, -0.0075, 0.335 - 0.127), (0.42, 0.42, 1.1), (0, sd * 0.1, 0), subd=1)
        thumb.location = arm.matrix_world @ Vector((sd * (-0.0105), -0.0095, -0.128)) if False else thumb.location
    # ---------------- lighting + camera for the previews
    if preview_prefix and PREVIEW:
        scn = bpy.context.scene; scn.render.engine = "CYCLES"; scn.cycles.device = "CPU"; scn.cycles.samples = 40; scn.cycles.use_denoising = True
        scn.render.resolution_x = 640; scn.render.resolution_y = 860; scn.render.film_transparent = False
        wd = bpy.data.worlds.new("w"); wd.use_nodes = True; wd.node_tree.nodes["Background"].inputs["Color"].default_value = hexc("#8a7660"); wd.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9; scn.world = wd
        def light(name, loc, energy, size):
            l = bpy.data.lights.new(name, "AREA"); l.energy = energy; l.size = size; o = bpy.data.objects.new(name, l); bpy.context.scene.collection.objects.link(o); o.location = loc
            d = Vector((0, 0, 0.26)) - Vector(loc); o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        light("key", (0.5, -1.0, 0.8), 90, 0.8); light("fill", (-0.7, -0.8, 0.4), 30, 1.0); light("rim", (0.1, 0.9, 0.7), 60, 0.8)
        fl = bpy.data.objects.new("floor", bpy.data.meshes.new("floor")); bm3 = bmesh.new(); bmesh.ops.create_grid(bm3, x_segments=1, y_segments=1, size=2.0); bm3.to_mesh(fl.data); bm3.free(); fl.data.materials.append(material("floor", "#a56a3f", 0.7)); bpy.context.scene.collection.objects.link(fl)
        cam = bpy.data.cameras.new("cam"); cam.lens = 55; co = bpy.data.objects.new("cam", cam); bpy.context.scene.collection.objects.link(co); scn.camera = co
        shots = {"front": ((0.0, -1.55, 0.27), (0, 0, 0.26)), "three": ((0.55, -1.25, 0.30), (0, 0, 0.27)), "head": ((0.0, -0.42, 0.44), (0, 0, 0.43)), "head3": ((0.25, -0.38, 0.45), (0, 0, 0.44)), "back": ((0.2, 1.4, 0.40), (0, 0, 0.36))}
        for nm, (loc, tgt) in shots.items():
            if nm == "head" or nm == "head3": cam.lens = 85
            else: cam.lens = 55
            co.location = loc; co.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
            scn.render.filepath = os.path.join(OUT, "%s_%s.png" % (preview_prefix, nm)); bpy.ops.render.render(write_still=True)
    # ---------------- export (figure only)
    for o in list(bpy.data.objects):
        if o.name in ("key", "fill", "rim", "cam", "floor"): bpy.data.objects.remove(o, do_unlink=True)
    # hair/brows/curves -> meshes (evaluated), so the glb carries geometry and the materials
    dg = bpy.context.evaluated_depsgraph_get()
    for o in list(bpy.data.objects):
        if o.type == "CURVE":
            me_ = bpy.data.meshes.new_from_object(o.evaluated_get(dg)); ob = bpy.data.objects.new(o.name + "_m", me_); bpy.context.scene.collection.objects.link(ob)
            ob.matrix_world = o.matrix_world; ob.data.materials.clear(); [ob.data.materials.append(m_) for m_ in o.data.materials]
            for p in ob.data.polygons: p.use_smooth = True
            bpy.data.objects.remove(o, do_unlink=True)
    path = os.path.join(OUT, "mini_%s.glb" % ("open" if open_mouth else "closed"))
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", export_apply=True, export_yup=True, use_selection=False)
    print("exported", path, "%.1fs" % (time.time() - T0), "strands", n_strands)


build(False, "closed")
build(True, "open" if os.environ.get("MINI_PREVIEW_OPEN") else None)
print("done %.1fs" % (time.time() - T0))
