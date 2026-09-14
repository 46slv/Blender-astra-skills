"""Live integration: hidden detail, instance bounds, semantic GN controls.

Requires `lamp`, `shelf`, `shelf_scene` made by the two shipped examples.
Creates only diagnostic cameras and local evidence; keeps the editable sources.
"""
import importlib
import json
import math
from pathlib import Path
import observe
importlib.reload(observe)
from observe import SurfaceProbe, aim, render
from gn import set_input
from mathutils import Vector

bpy.context.window.scene = lamp['scene']
head = lamp['head']
bulb_points = [list(head.matrix_world @ Vector((.02*math.cos(t),.02*math.sin(t),.188)))
               for t in (0,math.pi/2,math.pi,3*math.pi/2)]
target = head.matrix_world @ Vector((0,0,.15))
probe = SurfaceProbe()
choices = []
for label,offset in [('front',(0,-1.5,.1)),('side',(1.5,0,.1)),
                     ('below',(0,-.8,-.65)),('above',(0,-.5,1.2))]:
    camera = bpy.data.objects.new('Detail '+label,bpy.data.cameras.new('Detail '+label))
    lamp['scene'].collection.objects.link(camera)
    camera.location = target + Vector(offset)
    camera.data.type,camera.data.ortho_scale = 'ORTHO',.48
    aim(camera,target)
    evidence = probe.visibility(camera,bulb_points,tolerance=.004)
    choices.append((evidence['visible'],camera,evidence))
best = max(choices,key=lambda item:item[0])
assert best[0] > 0
assert any(item[0] == 0 for item in choices), 'Test did not include an occluded view'
render(SESSION_DIR.parent/'lamp-detail.png',best[1],mode='material',size=(700,700))

bpy.context.window.scene = shelf_scene
set_input(shelf.modifiers[0],'Levels',7)
set_input(shelf.modifiers[0],'Height',1.8)
set_input(shelf.modifiers[0],'Width',1.55)
dg = bpy.context.evaluated_depsgraph_get()
world_corners, count = [], 0
for inst in dg.object_instances:
    if inst.is_instance and inst.parent and inst.parent.original == shelf:
        count += 1
        world_corners.extend([inst.matrix_world @ Vector(p) for p in inst.object.bound_box])
assert count == 11, count  # Seven boards + four uprights, never realized.
mins = [min(p[k] for p in world_corners) for k in range(3)]
maxs = [max(p[k] for p in world_corners) for k in range(3)]
assert abs(mins[2]) < 1e-6 and abs(maxs[2]-1.8) < 1e-6, (mins,maxs)
assert abs(maxs[0]-mins[0]-1.55) < 1e-6
ray = SurfaceProbe().ray((0,0,3),(0,0,-1))
assert ray and abs(ray['position'][2]-(1.8-.065+.0175)) < 1e-5,ray

report = {'active_view':{camera.name:evidence['visible'] for _,camera,evidence in choices},
          'chosen_view':best[1].name,'shelf_instances':count,'bounds_min':mins,'bounds_max':maxs,
          'shelf_surface_hit':ray}
(SESSION_DIR.parent/'active-view-and-gn.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(SESSION_DIR.parent/'shelf-variants.blend'))
print(json.dumps(report,indent=2))
