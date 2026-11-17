import bpy, sys, math, mathutils
a = sys.argv[sys.argv.index('--') + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=a[0])
sc = bpy.context.scene
ms = [o for o in sc.objects if o.type == 'MESH']
mn = [1e9]*3; mx=[-1e9]*3
for m in ms:
    for c in m.bound_box:
        w = m.matrix_world @ mathutils.Vector(c)
        for k in range(3): mn[k]=min(mn[k],w[k]); mx[k]=max(mx[k],w[k])
cx,cy,cz=[(mn[k]+mx[k])/2 for k in range(3)]; Hh=mx[2]-mn[2]
print('bbox size', [round(mx[k]-mn[k],3) for k in range(3)])
sc.render.engine='BLENDER_WORKBENCH'; sc.display.shading.light='STUDIO'; sc.display.shading.color_type='TEXTURE'
sc.display.shading.studio_light='studio.sl'
sc.render.resolution_x=800; sc.render.resolution_y=1200
sc.world=bpy.data.worlds.new('w'); sc.world.color=(0.5,0.5,0.5)
cam=bpy.data.objects.new('c',bpy.data.cameras.new('c')); sc.collection.objects.link(cam); sc.camera=cam
cam.data.type='ORTHO'; cam.data.ortho_scale=Hh*1.15
C=mathutils.Vector((cx,cy,cz))
for n,d in [('a',(0,-1,0)),('b',(0,1,0)),('c',(1,0,0)),('d',(-1,0,0))]:
    loc=C+mathutils.Vector(d)*5; cam.location=loc
    cam.rotation_euler=(C-loc).normalized().to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=a[1]+'/v_%s.png'%n; bpy.ops.render.render(write_still=True)
