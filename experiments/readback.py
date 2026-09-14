"""Read back the delivered file after reopening; transient checks restore state."""
import json
from pathlib import Path
import bpy
from observe import SurfaceProbe, project, render
from gn import set_input

scene=bpy.data.scenes['Articulated Lamp']
bpy.context.window.scene=scene
cam=scene.camera
assert cam and cam.type=='CAMERA'
assert len([t for t in bpy.data.texts if t.name.startswith('Source - ')])==2
assert bpy.data.objects['Power cable - editable Bezier'].type=='CURVE'
assert bpy.data.objects['Elbow - rotate Y'].parent == bpy.data.objects['Shoulder - rotate Y']
render(SESSION_DIR.parent/'reopened.png',cam,mode='clay',size=(768,768))

settings=(cam.data.type,cam.data.lens,cam.data.shift_x,cam.data.shift_y,
          scene.render.resolution_x,scene.render.resolution_y)
roundtrip=[]
try:
    cam.data.type,cam.data.lens='PERSP',45
    cam.data.shift_x,cam.data.shift_y=.06,-.04
    scene.render.resolution_x,scene.render.resolution_y=900,600
    probe=SurfaceProbe()
    for u,v in [(.5,.5),(.6,.3),(.4,.7)]:
        hit=probe.pixel(cam,u,v)
        assert hit,(u,v)
        projected=project(cam,[hit['position']])[0]
        err=max(abs(projected[0]-u),abs(projected[1]-v))
        assert err<1e-5,err
        roundtrip.append(err)
finally:
    (cam.data.type,cam.data.lens,cam.data.shift_x,cam.data.shift_y,
     scene.render.resolution_x,scene.render.resolution_y)=settings

bpy.context.window.scene=bpy.data.scenes['Shelf variants']
shelf=bpy.data.objects['Parametric Shelf']
mod=shelf.modifiers[0]
set_input(mod,'Levels',3)
three=sum(i.is_instance and i.parent is not None and i.parent.original==shelf
          for i in bpy.context.evaluated_depsgraph_get().object_instances)
assert three==7,three
set_input(mod,'Levels',7)
seven=sum(i.is_instance and i.parent is not None and i.parent.original==shelf
          for i in bpy.context.evaluated_depsgraph_get().object_instances)
assert seven==11,seven
bpy.context.window.scene=scene
report={'reopened':Path(bpy.data.filepath).name,'source_texts':2,'perspective_shift_aspect_ray_roundtrip':roundtrip,
        'reopened_shelf_instances_levels_3':three,'reopened_shelf_instances_levels_7':seven}
(SESSION_DIR.parent/'readback.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
