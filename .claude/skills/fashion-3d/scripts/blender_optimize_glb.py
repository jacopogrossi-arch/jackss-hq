"""Alleggerisce un GLB pesante (es. da Tripo: 800k triangoli, 3 texture 4K) per il motore three.js: decima a N triangoli, riduce la texture colore, toglie normal/roughness-metal e rende il materiale opaco.
Uso: blender -b -P blender_optimize_glb.py -- in.glb out.glb [triangoli=100000] [texture_px=2048]
"""
import bpy, sys
a = sys.argv[sys.argv.index('--')+1:]
IN, OUT = a[:2]; TRIS = int(a[2]) if len(a) > 2 else 100000; TEX = int(a[3]) if len(a) > 3 else 2048
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=IN)
ob = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
bpy.context.view_layer.objects.active = ob; ob.select_set(True); bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
n0 = sum(len(p.vertices)-2 for p in ob.data.polygons)
m = ob.modifiers.new('dec', 'DECIMATE'); m.decimate_type = 'COLLAPSE'; m.ratio = min(1.0, TRIS/max(n0, 1)); m.use_collapse_triangulate = True; m.delimit = {'UV'}   # 17/11: senza delimit UV la decimazione scompone le isole di texture e compaiono puntini bianchi/scuri
bpy.ops.object.modifier_apply(modifier='dec')
for p in ob.data.polygons: p.use_smooth = True
print('triangoli', n0, '->', len(ob.data.polygons))
for mat in ob.data.materials:
    nt = mat.node_tree
    bsdf = next(nd for nd in nt.nodes if nd.type == 'BSDF_PRINCIPLED')
    for nm in ('Normal', 'Roughness', 'Metallic'):
        for l in list(bsdf.inputs[nm].links): nt.links.remove(l)
    bsdf.inputs['Roughness'].default_value = 0.8; bsdf.inputs['Metallic'].default_value = 0.0
    for nd in list(nt.nodes):
        if nd.type == 'TEX_IMAGE' and not any(l.from_node == nd for l in nt.links):
            nt.nodes.remove(nd)
for im in list(bpy.data.images):
    if im.users == 0 or im.name.endswith(('_normal.png', '_rm.jpg')): 
        if im.users == 0: bpy.data.images.remove(im)
    elif im.size[0] > TEX:
        im.scale(TEX, TEX)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_image_format='JPEG', export_jpeg_quality=88)
print('salvato', OUT)
