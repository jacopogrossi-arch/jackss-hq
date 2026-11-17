"""Prepara un GLB con scheletro (es. Tripo "Anima"/rig Mixamo) per il motore three.js: toglie oggetti extra, riduce la texture colore, tiene normal map e scheletro, niente animazioni.
Uso: blender -b -P blender_prepare_rig.py -- in.glb out.glb [texture_px=2048] [anim] [smooth=2.5]   ('anim' = tieni le clip; 'smooth=N' = ammorbidisce le curve con un filtro gaussiano di N fotogrammi, in modo circolare cosi' il loop non salta)
"""
import bpy, sys
a = sys.argv[sys.argv.index('--')+1:]
IN, OUT = a[:2]; TEX = int(a[2]) if len(a) > 2 and a[2].isdigit() else 2048; ANIM = 'anim' in a
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=IN)
for o in list(bpy.context.scene.objects):
    if o.type == 'MESH' and len(o.data.polygons) < 1000:
        print('RIMOSSO', o.name, len(o.data.polygons), 'poly, pos', [round(v, 2) for v in o.location])
        bpy.data.objects.remove(o, do_unlink=True)
for mat in bpy.data.materials:
    if not mat.use_nodes: continue
    nt = mat.node_tree; bsdf = next((nd for nd in nt.nodes if nd.type == 'BSDF_PRINCIPLED'), None)
    if bsdf:
        for nm in ('Roughness', 'Metallic'):
            for l in list(bsdf.inputs[nm].links): nt.links.remove(l)
        bsdf.inputs['Roughness'].default_value = 0.8; bsdf.inputs['Metallic'].default_value = 0.0
    for nd in list(nt.nodes):
        if nd.type == 'TEX_IMAGE' and not any(l.from_node == nd for l in nt.links): nt.nodes.remove(nd)
SM = next((float(x.split('=')[1]) for x in a if x.startswith('smooth=')), 0.0)
if SM > 0:
    import numpy as np
    def fcurves_of(act):
        try: return list(act.fcurves)
        except Exception:
            out = []
            for layer in act.layers:
                for strip in layer.strips:
                    for cb in strip.channelbags: out += list(cb.fcurves)
            return out
    kk = int(np.ceil(SM*3)); ker = np.exp(-0.5*(np.arange(-kk, kk+1)/SM)**2); ker /= ker.sum()
    for act in bpy.data.actions:
        groups = {}
        for fc in fcurves_of(act): groups.setdefault(fc.data_path, {})[fc.array_index] = fc
        for dp, d in groups.items():
            idx = sorted(d); arr = np.array([[kp.co[1] for kp in d[i].keyframe_points] for i in idx]).T
            if len(arr) < 2*kk+2: continue
            pad = np.concatenate([arr[-kk:], arr, arr[:kk]])
            sm = np.stack([np.convolve(pad[:, c], ker, mode='valid') for c in range(arr.shape[1])], 1)
            if dp.endswith('rotation_quaternion'): sm /= np.linalg.norm(sm, axis=1, keepdims=True)
            for ci, i in enumerate(idx):
                for j, kp in enumerate(d[i].keyframe_points): kp.co[1] = sm[j, ci]
                d[i].update()
        print('LISCIATA', act.name[:30], len(groups), 'curve')
for im in list(bpy.data.images):
    if im.users == 0: bpy.data.images.remove(im)
    elif im.size[0] > TEX: im.scale(TEX, TEX)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_image_format='JPEG', export_jpeg_quality=88, export_animations=ANIM, export_skins=True, **({'export_animation_mode': 'ACTIONS'} if ANIM else {}))
print('salvato', OUT)
