"""Exercise the shipped library in a fresh dedicated GUI session.

No generator source is executed. Outputs stay under SESSION_DIR.parent. Inspect
asset-reuse.png, then reopen asset-reuse.blend and check the saved native controls.
"""
from pathlib import Path
import json
import math
import bpy
from mathutils import Vector
import assets
from gn import set_input
from observe import aim, render

assert bpy.data.filepath == '' and len(bpy.data.objects) == 3, 'Use a fresh factory session'
output = SESSION_DIR.parent
assert not (output / 'asset-reuse.blend').exists(), 'Preserve previous candidates'
scene = bpy.data.scenes.new('Asset reuse')
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
before = len(bpy.data.objects)
entries = assets.find()
assert len(entries) == 9, entries
assert len(bpy.data.objects) == before, 'Discovery must not append anything'
existing_libraries = [(p.name, p.path, p.import_method) for p in bpy.context.preferences.filepaths.asset_libraries]
registered = assets.register()
assert assets.register() == registered
assert [(p.name, p.path, p.import_method) for p in bpy.context.preferences.filepaths.asset_libraries][:-1] == existing_libraries


def entry(name):
    return next(a for a in entries if a['name'] == name)


def count(obj):
    bpy.context.view_layer.update()
    return sum(i.is_instance and i.parent is not None and i.parent.original == obj
               for i in bpy.context.evaluated_depsgraph_get().object_instances)


lamp = assets.append(entry('Articulated Lamp v1'))
lamp2 = assets.append(entry('Articulated Lamp v1'))
assert not set(lamp.all_objects) & set(lamp2.all_objects)
assert all(o.parent is None or o.parent in set(lamp.all_objects) for o in lamp.all_objects)
root = next(o for o in lamp.objects if o.parent is None)
root2 = next(o for o in lamp2.objects if o.parent is None)
head = next(o for o in lamp.all_objects if o.name.startswith('Head -'))
bulb = next(o for o in lamp.all_objects if o.name.startswith('Bulb'))
head2 = next(o for o in lamp2.all_objects if o.name.startswith('Head -'))
original_angle = head.rotation_euler.y
original_angle2 = head2.rotation_euler.y
bpy.context.view_layer.update()
old_bulb = bulb.matrix_world @ bulb.data.vertices[-1].co
head.rotation_euler.y += .12
bpy.context.view_layer.update()
pose_delta = (bulb.matrix_world @ bulb.data.vertices[-1].co - old_bulb).length
assert pose_delta > .001
assert head2.rotation_euler.y == original_angle2
root2.location = (2.2, 0, 0)
fasteners = next(o for o in lamp.all_objects if o.name.startswith('Base fasteners'))
assert count(fasteners) == 6
assert any(o.type == 'CURVE' for o in lamp.all_objects)
assert not any(o.type in {'CAMERA', 'LIGHT'} or o.name == 'Studio floor' for o in lamp.all_objects)

shelf = assets.append(entry('Parametric Shelf v1'))
assert count(shelf) == 11
mod = shelf.modifiers[0]
for name, value in [('Width', 1.4), ('Depth', .5), ('Height', 1.2), ('Levels', 4)]:
    set_input(mod, name, value)
assert count(shelf) == 8
shelf.location = (0, 0, 0)
# Shelf top surface = Height - .065 + .035/2; place the lamp's base on it.
root.location = (0, 0, 1.2 - .065 + .035 / 2)
bpy.context.view_layer.update()
corners = []
for instance in bpy.context.evaluated_depsgraph_get().object_instances:
    if instance.is_instance and instance.parent is not None and instance.parent.original == shelf:
        corners.extend(tuple(instance.matrix_world @ Vector(p)) for p in instance.object.bound_box)
bounds = [[min(p[i] for p in corners), max(p[i] for p in corners)] for i in range(3)]
assert abs(bounds[0][1] - bounds[0][0] - 1.4) < 1e-5
assert abs(bounds[2][0]) < 1e-5 and abs(bounds[2][1] - 1.2) < 1e-5

generator = assets.append(entry('Shelf Generator v1'))
host = bpy.data.objects.new('Standalone shelf generator reuse', bpy.data.meshes.new('Shelf host'))
scene.collection.objects.link(host)
gm = host.modifiers.new('Independent shelf controls', 'NODES')
gm.node_group = generator
set_input(gm, 'Levels', 3)
assert count(host) == 7 and count(shelf) == 8
host.location = (-2.2, 0, 0)
ring = assets.append(entry('Radial Fasteners v1'))
ring_host = bpy.data.objects.new('Standalone fasteners reuse', bpy.data.meshes.new('Ring host'))
scene.collection.objects.link(ring_host)
rm = ring_host.modifiers.new('Independent count', 'NODES')
rm.node_group = ring
set_input(rm, 'Count', 10)
assert count(ring_host) == 10 and count(fasteners) == 6
ring_host.location = (2.2, -.3, .02)

mat = assets.append(entry('Satin Brass v1'))
source_mat = next(o for o in lamp.all_objects if o.name.startswith('Rolled brass rim')).data.materials[0]
assert mat != source_mat
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=.12, location=(.4, 0, root.location.z + .12))
sphere = bpy.context.object
sphere.name = 'Reused brass material sample'
sphere.data.materials.append(mat)
for face in sphere.data.polygons:
    face.use_smooth = True
# Blender 5.2 can retain an unused Library ID after append. Check actual ID links
# before removing that bookkeeping record from this owned fresh scene.
users = bpy.data.user_map()
assert not [data for data in users if data.library]
for library in list(bpy.data.libraries):
    assert not users.get(library)
    bpy.data.libraries.remove(library)
assert not [i for i in bpy.data.images if i.source == 'FILE']
metadata = []
for asset in [lamp, shelf, generator, ring, mat]:
    assert asset.preview and min(asset.preview.image_size) > 0
    assert asset['source_text'].as_string()
    metadata.append({'name': asset.name, 'id': asset['asset_id'], 'version': asset['asset_version'],
                     'preview': list(asset.preview.image_size)})

scene.render.engine = 'CYCLES'
scene.cycles.samples = 32
scene.cycles.use_denoising = True
scene.world = bpy.data.worlds.new('Reuse world')
scene.world.color = (.2, .2, .2)
camera = bpy.data.objects.new('Reuse camera', bpy.data.cameras.new('Reuse camera'))
scene.collection.objects.link(camera)
camera.location = (4.5, -8, 4)
camera.data.type, camera.data.ortho_scale = 'ORTHO', 6.6
aim(camera, (0, 0, .9))
scene.camera = camera
for name, pos, power, size in [('Key', (1, -3, 5), 1000, 4), ('Fill', (-4, -1, 3), 700, 3)]:
    light = bpy.data.lights.new('Reuse ' + name, 'AREA')
    light.energy, light.size = power, size
    obj = bpy.data.objects.new(light.name, light)
    scene.collection.objects.link(obj)
    obj.location = pos
    aim(obj, (0, 0, 1))
bpy.ops.mesh.primitive_plane_add(size=200)
floor = bpy.context.object
floor.name = 'Reuse studio floor'
floor.location.z = -.004
floor_mat = bpy.data.materials.new('Reuse floor')
floor_mat.use_nodes = True
floor_mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value = (.15, .18, .2, 1)
floor.data.materials.append(floor_mat)
render(output / 'asset-reuse.png', camera, mode='material', size=(1200, 720))
bpy.ops.wm.save_as_mainfile(filepath=str(output / 'asset-reuse.blend'))
report = {'blender': bpy.app.version_string, 'native_assets_discovered': len(entries),
          'independent_lamp_copies': 2, 'lamp_pose_bulb_displacement_m': pose_delta,
          'shelf_preset_instances': 11, 'shelf_edited_instances': count(shelf),
          'shelf_bounds_m': bounds, 'standalone_shelf_instances': count(host),
          'standalone_fasteners_instances': count(ring_host), 'lamp_fasteners_unchanged': count(fasteners),
          'metadata_samples': metadata, 'external_libraries': len(bpy.data.libraries),
          'preferences_saved': False}
(output / 'asset-reuse-evidence.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report))
