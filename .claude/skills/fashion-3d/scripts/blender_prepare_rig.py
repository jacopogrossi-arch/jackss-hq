"""Prepara un GLB con scheletro (es. Tripo "Anima"/rig Mixamo) per il motore three.js: toglie oggetti extra, riduce la texture colore, tiene normal map e scheletro, niente animazioni.
Uso: blender -b -P blender_prepare_rig.py -- in.glb out.glb [texture_px=2048] [anim]   ('anim' = tieni le clip di animazione)
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
for im in list(bpy.data.images):
    if im.users == 0: bpy.data.images.remove(im)
    elif im.size[0] > TEX: im.scale(TEX, TEX)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_image_format='JPEG', export_jpeg_quality=88, export_animations=ANIM, export_skins=True, **({'export_animation_mode': 'ACTIONS'} if ANIM else {}))
print('salvato', OUT)
