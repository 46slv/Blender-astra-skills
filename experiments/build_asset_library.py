"""Extract the existing examples into native reusable assets in a dedicated session.

Open artifacts/blender-skill-examples.blend in a separate request first (Blender's
window context settles after file load). Set ASSET_OUTPUT to a NEW directory.
Does not overwrite sources,
existing releases or preferences. Run from repository root with skill scripts on
sys.path. Preview renders go to the session's scratch directory.
"""
from pathlib import Path
import uuid
import bpy
from observe import aim, render
from gn import set_input

repo = Path.cwd()
output = Path(ASSET_OUTPUT).resolve()
assert not output.exists(), 'Choose a new release/staging directory'
output.mkdir(parents=True)
scratch = SESSION_DIR.parent / 'previews'
scratch.mkdir(exist_ok=True)
assert Path(bpy.data.filepath).resolve() == repo / 'artifacts/blender-skill-examples.blend'
assert bpy.context.window is not None, 'Wait for the file-load window context to settle'

catalogs = {name: str(uuid.uuid5(uuid.NAMESPACE_URL, 'astra-blender-assets/' + name))
            for name in ('Lighting', 'Furniture', 'Generators', 'Materials')}
(output / 'blender_assets.cats.txt').write_text(
    '# Blender Asset Catalog Definition File\nVERSION 1\n\n' +
    '\n'.join(f'{uid}:{name}:{name}' for name, uid in catalogs.items()) + '\n', encoding='utf-8')
source_url = ('https://github.com/46slv/Blender-astra-skills/blob/'
              'c7b6f1a/artifacts/blender-skill-examples.blend')
assets = []


def mark(data, name, catalog, slug, description, tags, source=None):
    data.name = name
    data.asset_mark()
    meta = data.asset_data
    meta.author = 'Astra / Blender-astra-skills project'
    meta.description = description + ' Source: ' + source_url
    meta.license = 'Project-authored; no standalone redistribution license specified.'
    meta.catalog_id = catalogs[catalog]
    for tag in tags:
        meta.tags.new(tag)
    data['asset_id'] = 'astra.' + slug
    data['asset_version'] = 1
    data['tested_blender'] = bpy.app.version_string
    if source:
        data['source_text'] = bpy.data.texts['Source - ' + source]
    assets.append(data)
    return data


def preview(data, path):
    with bpy.context.temp_override(id=data):
        result = bpy.ops.ed.lib_id_load_custom_preview(filepath=str(path))
    assert 'FINISHED' in result
    assert data.preview and min(data.preview.image_size) > 0, data.name


lamp_scene = bpy.data.scenes['Articulated Lamp']
bpy.context.window.scene = lamp_scene
lamp = bpy.data.collections.new('Lamp assembly')
root = bpy.data.objects.new('Lamp placement - move whole assembly', None)
root.empty_display_type = 'PLAIN_AXES'
lamp.objects.link(root)
for obj in list(lamp_scene.objects):
    if obj.type in {'MESH', 'CURVE', 'EMPTY'} and obj.name != 'Studio floor':
        lamp.objects.link(obj)
        if obj.parent is None:
            obj.parent = root  # identity placement frame preserves authored transforms
lamp_scene.collection.children.link(lamp)
mark(lamp, 'Articulated Lamp v1', 'Lighting', 'lighting.articulated-lamp',
     'Meters, Z up, base at origin. Move Lamp placement; pose Shoulder/Elbow/Head Y pivots. '
     'Editable shade shell and cable, 6 instanced fasteners. Cable is static; refit after large poses.',
     ['lamp', 'ランプ', 'articulated', 'collection', 'enamel'], 'articulated_lamp.py')
render(scratch / 'lamp.png', lamp_scene.camera, mode='material', size=(384, 384))
preview(lamp, scratch / 'lamp.png')

shelf_scene = bpy.data.scenes['Shelf variants']
bpy.context.window.scene = shelf_scene
shelf = bpy.data.objects['Parametric Shelf']
# The original example used viewport-only swatches. Preserve those colors in
# actual shader nodes so the reusable shelf also renders correctly in Cycles.
for material in (bpy.data.materials['Parametric Shelf oak'], bpy.data.materials['Parametric Shelf graphite']):
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = material.diffuse_color
    bsdf.inputs['Roughness'].default_value = .5
mark(shelf, 'Parametric Shelf v1', 'Furniture', 'furniture.parametric-shelf',
     'Meters, Z up, floor origin. Modifier Width/Depth/Height/Levels; 7 boards + 4 posts preset. '
     'Unrealized instances. Solid oak-color/graphite placeholders; no wood texture or joinery.',
     ['shelf', '棚', 'furniture', 'parametric'], 'parametric_shelf.py')
render(scratch / 'shelf.png', shelf_scene.camera, size=(384, 384))
preview(shelf, scratch / 'shelf.png')
group = shelf.modifiers[0].node_group
group.is_modifier = True
mark(group, 'Shelf Generator v1', 'Generators', 'generators.shelf',
     'Geometry Nodes modifier generator, meters, Z up. Width/Depth/Height/Levels, '
     '5-level defaults; object preset has independent modifier values. No Python required to evaluate.',
     ['shelf', '棚', 'geometry-nodes', 'generator'], 'parametric_shelf.py')
for name, value in [('Width', 1.2), ('Height', 1.5), ('Levels', 5)]:
    set_input(shelf.modifiers[0], name, value)
render(scratch / 'shelf-generator.png', shelf_scene.camera, size=(384, 384))
preview(group, scratch / 'shelf-generator.png')
for name, value in [('Width', 1.55), ('Height', 1.8), ('Levels', 7)]:
    set_input(shelf.modifiers[0], name, value)
fasteners = bpy.data.node_groups['Radial fastener array']
fasteners.is_modifier = True
mark(fasteners, 'Radial Fasteners v1', 'Generators', 'generators.radial-fasteners',
     'Geometry Nodes modifier generator. Count 3..64; radius fixed at 0.10 m; '
     'hex bolts radius 0.0055 m, depth 0.007 m, centers at local Z=0. Brass included.',
     ['fastener', 'bolt', 'radial', 'geometry-nodes'], 'articulated_lamp.py')

# A tiny isolated studio gives materials and the generator their own truthful previews.
studio = bpy.data.scenes.new('Asset preview studio')
bpy.context.window.scene = studio
studio.render.engine = 'CYCLES'
studio.cycles.samples = 16
studio.cycles.use_denoising = True
studio.world = bpy.data.worlds.new('Asset preview world')
studio.world.color = (.2, .2, .2)
cam = bpy.data.objects.new('Asset preview camera', bpy.data.cameras.new('Asset preview camera'))
studio.collection.objects.link(cam)
studio.camera = cam
cam.data.type = 'ORTHO'
for name, pos, power, size in [('Key', (1, -2, 3), 300, 2), ('Fill', (-2, -1, 1), 150, 2)]:
    light = bpy.data.lights.new('Asset preview ' + name, 'AREA')
    light.energy, light.size = power, size
    obj = bpy.data.objects.new(light.name, light)
    studio.collection.objects.link(obj)
    obj.location = pos
    aim(obj, (0, 0, 0))
host = bpy.data.objects.new('Fasteners preview host', bpy.data.meshes.new('Preview host'))
studio.collection.objects.link(host)
host.modifiers.new('Fasteners', 'NODES').node_group = fasteners
cam.location, cam.data.ortho_scale = (.18, -.25, .35), .28
aim(cam, (0, 0, 0))
render(scratch / 'fasteners.png', cam, mode='material', size=(256, 256))
preview(fasteners, scratch / 'fasteners.png')
studio.collection.objects.unlink(host)
bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=.4)
sphere = bpy.context.object
for polygon in sphere.data.polygons:
    polygon.use_smooth = True
cam.location, cam.data.ortho_scale = (1, -2, 1), 1.05
aim(cam, (0, 0, 0))
for original, name, slug, description in [
    ('Enamel - forest', 'Forest Enamel v1', 'forest-enamel', 'Forest green metallic enamel, roughness 0.28.'),
    ('Brushed brass', 'Satin Brass v1', 'satin-brass', 'Uniform metallic brass, roughness 0.26. No brushed microtexture.'),
    ('Rubber and cable', 'Dark Rubber v1', 'dark-rubber', 'Dark matte rubber/cable, roughness 0.65.'),
    ('Shade interior', 'Ivory Reflector v1', 'ivory-reflector', 'Warm ivory shade interior, roughness 0.32.'),
    ('Warm frosted bulb', 'Warm Bulb v1', 'warm-bulb', 'Warm bulb surface, emission strength 0.6; not a calibrated light source.'),
]:
    material = mark(bpy.data.materials[original], name, 'Materials', 'materials.' + slug,
                    description + ' Principled shader; no external textures.',
                    ['material', 'principled', slug], 'articulated_lamp.py')
    sphere.data.materials.clear()
    sphere.data.materials.append(material)
    path = scratch / (slug + '.png')
    render(path, cam, mode='material', size=(256, 256))
    preview(material, path)

# write() follows ID dependencies, including parent chains, nested groups, materials
# and the source Text pointers. No scene, camera, studio or workspace is selected.
bpy.data.libraries.write(str(output / 'starter-v1.blend'), set(assets),
                         path_remap='RELATIVE_ALL', fake_user=True, compress=True)
print('LIBRARY', str(output), [(a.name, a.id_type, list(a.preview.image_size)) for a in assets])
