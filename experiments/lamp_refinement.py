"""Run via session.py after examples/articulated_lamp.build().

Synthetic controlled experiment, NOT proof of arbitrary photo reconstruction.
The target image and correspondences come from a known editable lamp. We disturb
camera and articulation, then recover them in separate stages without rerendering
inside the optimizer. At entry the live namespace must contain `lamp`.
"""
import json
import math
import numpy as np
from mathutils import Vector
from observe import render, project, SurfaceProbe
from fit import solve

output = SESSION_DIR.parent / 'refinement'
output.mkdir(exist_ok=True)
cam = lamp['camera']
scene = lamp['scene']
bpy.context.window.scene = scene
floor = lamp['floor']
floor.hide_render = True
floor.hide_set(True)
truth_pose = [lamp[k].rotation_euler.y for k in ('lower','upper','head')]
fixed_anchors = [(0,0,.11),(.10,0,.055),(-.1,0,.055),(0,.1,.055),(0,-.1,.055)]

def moving_anchors():
    bpy.context.view_layer.update()
    return [list(lamp['upper'].matrix_world.translation),
            list(lamp['head'].matrix_world.translation),
            list(lamp['head'].matrix_world @ Vector((.165,0,.208))),
            list(lamp['head'].matrix_world @ Vector((-.165,0,.208)))]

def pixels(points):
    return np.asarray([p[:2] for p in project(cam,points)])*768

truth_camera = [cam.data.shift_x, cam.data.shift_y, cam.data.ortho_scale]
target_fixed, target_moving = pixels(fixed_anchors), pixels(moving_anchors())
render(output/'reference.png',cam,size=(768,768))
cam.data.shift_x,cam.data.shift_y,cam.data.ortho_scale = .07,-.045,1.45
for k, value in zip(('lower','upper','head'),[-.17,.76,2.40]):
    lamp[k].rotation_euler.y = value
render(output/'before.png',cam,size=(768,768))

def camera_residual(x):
    cam.data.shift_x,cam.data.shift_y,cam.data.ortho_scale = x
    return (pixels(fixed_anchors)-target_fixed).ravel()

camera_fit = solve([.07,-.045,1.45],camera_residual,[.005,.005,.01],
                   bounds=([-.3,-.3,.6],[.3,.3,2.5]),tolerance=.02)
render(output/'camera-only.png',cam,size=(768,768))

def pose_residual(x):
    for k, value in zip(('lower','upper','head'),x):
        lamp[k].rotation_euler.y = value
    return (pixels(moving_anchors())-target_moving).ravel()

pose_fit = solve([-.17,.76,2.40],pose_residual,[.01,.01,.01],
                 bounds=([-.9,.1,1.3],[.2,1.7,3.1]),tolerance=.02)
render(output/'after.png',cam,size=(768,768))
render(output/'identities.png',cam,mode='ids',size=(768,768))

# A known visible shade point maps back to the evaluated shell, not the floor.
probe = SurfaceProbe()
shade_center = lamp['head'].matrix_world @ Vector((0,0,.12))
uv = project(cam,[shade_center])[0]
hit = probe.pixel(cam,uv[0],uv[1])
assert hit and 'shade' in hit['object'].lower(), hit
surface_pixel = project(cam,[hit['position']])[0]
assert max(abs(surface_pixel[i]-uv[i]) for i in range(2)) < 1e-5

# GN-only geometry must remain instances and still be available to spatial probes.
dg = bpy.context.evaluated_depsgraph_get()
instance_origins = [list(i.matrix_world.translation) for i in dg.object_instances
                    if i.is_instance and i.parent and i.parent.original == lamp['fasteners']]
bolt_hit = probe.ray((.10,0,.2),(0,0,-1))
assert bolt_hit and 'fastener' in bolt_hit['object'].lower(), bolt_hit
assert len(instance_origins) == 6, len(instance_origins)
assert not any(n.bl_idname == 'GeometryNodeRealizeInstances' for n in lamp['fasteners'].modifiers[0].node_group.nodes)
assert camera_fit['converged'] and pose_fit['converged']
report = {'kind':'synthetic known-correspondence recovery', 'camera':camera_fit, 'pose':pose_fit,
          'truth_camera':truth_camera, 'truth_pose':truth_pose, 'shade_pixel_hit':hit,
          'fastener_instances':len(instance_origins), 'fastener_ray_hit':bolt_hit,
          'limits':'Correspondences supplied from known model. No inference of unseen shape or automatic reference segmentation.'}
(output/'results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
floor.hide_render = False
floor.hide_set(False)
bpy.ops.wm.save_as_mainfile(filepath=str(SESSION_DIR.parent/'articulated-lamp.blend'))
print(json.dumps(report,indent=2))
