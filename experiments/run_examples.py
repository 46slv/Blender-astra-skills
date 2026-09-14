"""Reproduce the shipped live trials in a NEW dedicated session.

python skills/blender/scripts/session.py exec --session .work/verified \
  --script experiments/run_examples.py --timeout 30
Requires this repository as current working directory in the launched Blender.
"""
from pathlib import Path
import json
import sys
import bpy
import bmesh

repo = Path.cwd()
assert (repo/'GOAL.md').is_file(), 'Launch the session from the repository root'
sys.path.insert(0,str(repo/'skills/blender/examples'))
from articulated_lamp import build
from observe import render,aim
import parametric_shelf

assert len(bpy.data.objects) == 3 and bpy.data.filepath == '', 'Use a fresh factory session'
candidate=SESSION_DIR.parent/'blender-skill-examples.blend'
assert not candidate.exists(), 'Use a fresh experiment directory; preserve previous results'
lamp = build()
topology = {}
for obj in lamp['scene'].objects:
    if obj.type != 'MESH' or not obj.data.polygons or obj == lamp['floor']:
        continue
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bad_edges = sum(not e.is_manifold for e in bm.edges)
    zero_faces = sum(f.calc_area()<1e-12 for f in bm.faces)
    bm.free()
    topology[obj.name] = {'nonmanifold_edges':bad_edges,'degenerate_faces':zero_faces}
    assert bad_edges == zero_faces == 0,(obj.name,bad_edges,zero_faces)
print('CLOSED_MESH_PARTS',len(topology))
for filename in ['articulated_lamp.py','parametric_shelf.py']:
    text=bpy.data.texts.new('Source - '+filename)
    text.use_fake_user=True
    text.write((repo/'skills/blender/examples'/filename).read_text(encoding='utf-8'))
render(SESSION_DIR.parent/'lamp-hero.png',lamp['camera'],mode='material',size=(900,900))
exec(compile((repo/'experiments/lamp_refinement.py').read_text(encoding='utf-8'),
             str(repo/'experiments/lamp_refinement.py'),'exec'))
shelf_scene=bpy.data.scenes.new('Shelf variants')
bpy.context.window.scene=shelf_scene
shelf=parametric_shelf.build()
shelf_cam=bpy.data.objects.new('Shelf inspection camera',bpy.data.cameras.new('Shelf inspection camera'))
shelf_scene.collection.objects.link(shelf_cam)
shelf_cam.location=(2.5,-3.5,2.2)
shelf_cam.data.type,shelf_cam.data.ortho_scale='ORTHO',2.4
aim(shelf_cam,(0,0,.85))
shelf_scene.camera=shelf_cam
render(SESSION_DIR.parent/'shelf-before.png',shelf_cam)
exec(compile((repo/'experiments/active_view_and_gn.py').read_text(encoding='utf-8'),
             str(repo/'experiments/active_view_and_gn.py'),'exec'))
render(SESSION_DIR.parent/'shelf-after.png',shelf_cam)
(SESSION_DIR.parent/'topology.json').write_text(json.dumps(topology,indent=2),encoding='utf-8')
# One final file contains both editable examples, source Texts and inspection cameras.
bpy.context.window.scene=lamp['scene']
bpy.ops.wm.save_as_mainfile(filepath=str(candidate))
print('DELIVERABLE',candidate)
