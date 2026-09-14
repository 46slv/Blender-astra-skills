"""Search by structure, reuse native GN, capture a local asset/card, and read back.

From repo root in a fresh Blender:
blender --background --factory-startup --disable-autoexec --python-exit-code 1
  --python experiments/learn_and_reuse.py -- --output .work/knowledge-trial
Then run the same command with --reopen. Never overwrites prior production.
"""
import argparse
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'skills/blender/scripts'))
import assets
import knowledge
from gn import set_input
from observe import aim, render

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True, type=Path)
parser.add_argument('--reopen', action='store_true')
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
output = args.output.resolve()


def measure(obj):
    bpy.context.view_layer.update()
    corners = []
    count = 0
    for inst in bpy.context.evaluated_depsgraph_get().object_instances:
        if inst.is_instance and inst.parent and inst.parent.original == obj:
            count += 1
            corners.extend(inst.matrix_world @ Vector(p) for p in inst.object.bound_box)
    lo = [min(p[i] for p in corners) for i in range(3)]
    hi = [max(p[i] for p in corners) for i in range(3)]
    return {'instances': count, 'bounds_min': lo, 'dimensions': [hi[i]-lo[i] for i in range(3)]}


def check(obj, width, depth, height, levels):
    actual = measure(obj)
    assert actual['instances'] == levels + 4, actual
    assert max(abs(a-b) for a, b in zip(actual['dimensions'], [width, depth, height])) < 1e-5, actual
    assert abs(actual['bounds_min'][2]) < 1e-5, actual
    return actual


if args.reopen:
    bpy.ops.wm.open_mainfile(filepath=str(output / 'knowledge-reuse.blend'))
    stand = bpy.data.objects['Low display stand']
    rack = bpy.data.objects['Tall rack']
    check(stand, 1.4, .5, .65, 3)
    check(rack, .85, .34, 1.9, 6)
    set_input(stand.modifiers[0], 'Levels', 4)
    changed = check(stand, 1.4, .5, .65, 4)
    unchanged = check(rack, .85, .34, 1.9, 6)
    hit = knowledge.search('low display stand', roots=[output / 'library'])[0]
    native = assets.append(knowledge.resolve(hit))
    assert native.get('asset_id') == hit['card']['source']['asset_id']
    captured = check(native, 1.4, .5, .65, 3)
    set_input(native.modifiers[0], 'Levels', 5)
    check(native, 1.4, .5, .65, 5)
    check(stand, 1.4, .5, .65, 4)
    result = {'saved_scene_reopened': True, 'changed_stand': changed,
              'unchanged_rack': unchanged, 'captured_asset_append': captured,
              'captured_asset_independent_edit': True}
    (output / 'readback.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))
else:
    assert not output.exists(), 'Choose a fresh output directory'
    output.mkdir(parents=True)
    scene = bpy.data.scenes.new('Knowledge-driven reuse')
    bpy.context.window.scene = scene
    scene.unit_settings.system = 'METRIC'
    query = 'vertical supports repeated horizontal members count spacing'
    hits = knowledge.search(query)
    hit = next(h for h in hits if h['card']['id'] == 'astra.furniture.parametric-shelf')
    ja_hits = knowledge.search('支柱 横板 段数 間隔')
    assert hit['card']['id'] in [h['card']['id'] for h in ja_hits[:3]]
    before = len(bpy.data.objects)
    entry = knowledge.resolve(hit)
    assert len(bpy.data.objects) == before
    stand = assets.append(entry)
    rack = assets.append(entry)
    assert stand.modifiers[0].node_group != rack.modifiers[0].node_group
    stand.name, rack.name = 'Low display stand', 'Tall rack'
    evidence = {'blender': bpy.app.version_string, 'query': query,
                'matched': hit['matched'], 'retrieved': hit['card']['id'],
                'japanese_top3': [h['card']['id'] for h in ja_hits[:3]], 'variants': {}}
    for obj, values in [(stand, (1.4, .5, .65, 3)), (rack, (.85, .34, 1.9, 6))]:
        for name, val in zip(('Width', 'Depth', 'Height', 'Levels'), values):
            set_input(obj.modifiers[0], name, val)
        evidence['variants'][obj.name] = check(obj, *values)
        evidence['variants'][obj.name]['board_center_spacing'] = (values[2]-.155)/(values[3]-1)
    # Learn the actual limit on this copy, then restore the accepted stand.
    set_input(stand.modifiers[0], 'Height', .4)
    set_input(stand.modifiers[0], 'Levels', 12)
    crowded = measure(stand)
    centers = []
    thicknesses = []
    for inst in bpy.context.evaluated_depsgraph_get().object_instances:
        if inst.is_instance and inst.parent and inst.parent.original == stand:
            points = [inst.matrix_world @ Vector(p) for p in inst.object.bound_box]
            thickness = max(p.z for p in points)-min(p.z for p in points)
            if thickness < .04:
                centers.append(sum(p.z for p in points)/len(points))
                thicknesses.append(thickness)
    spacings = [b-a for a,b in zip(sorted(centers), sorted(centers)[1:])]
    assert len(centers) == 12 and max(spacings) < min(thicknesses)
    evidence['crowded_limit'] = {'height': .4, 'levels': 12, 'instances': crowded['instances'],
        'measured_center_spacing': spacings[0], 'measured_board_thickness': thicknesses[0],
        'overlap_confirmed': True}
    set_input(stand.modifiers[0], 'Height', .65)
    set_input(stand.modifiers[0], 'Levels', 3)

    # Capture a useful preset into a separate project library, not the shipped source.
    library = output / 'library'
    library.mkdir()
    stand.asset_mark()
    stand['asset_id'], stand['asset_version'] = 'trial.display-stand', 1
    stand.asset_data.description = 'Low display stand; editable Width Depth Height Levels. Origin on floor.'
    path = library / 'display-stand-v1.blend'
    bpy.data.libraries.write(str(path), {stand}, fake_user=True, compress=True)
    card = dict(id='trial.display-stand', kind='asset', title='Low display stand',
        summary='Four vertical supports and three repeated horizontal members for a low display stand.',
        terms=['展示台 支柱 横板 段数 間隔'],
        source=dict(file=path.name, kind='objects', name=stand.name,
                    sha256=knowledge.fingerprint(path), asset_id='trial.display-stand', asset_version=1),
        provenance=hit['card']['provenance'], links=['astra.generators.shelf'],
        limits=hit['card']['limits'])
    saved = knowledge.save(card, library)
    saved['evidence'] = [{'status': 'tested', 'claim': '3 boards + 4 posts at 1.4 x 0.5 x 0.65 m.',
                          'basis': '../evidence.json (relative to this library root)'}]
    saved = knowledge.save(saved, library, expected_revision=saved['revision'])
    assert knowledge.search('展示台', [library])[0]['card']['revision'] == 2
    evidence['captured_card_revision'] = 2
    evidence['source_unchanged'] = knowledge.resolve(hit) == entry
    (output / 'inspection.json').write_text(json.dumps(assets.inspect(stand), indent=2), encoding='utf-8')

    stand.location.x = -.9
    rack.location.x = .75
    cam = bpy.data.objects.new('Reuse camera', bpy.data.cameras.new('Reuse camera'))
    scene.collection.objects.link(cam)
    cam.location = (3.4, -5.5, 3.0)
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = 4.1
    aim(cam, (0, 0, .9))
    scene.camera = cam
    render(output / 'knowledge-reuse.png', cam, size=(1000, 700))
    bpy.ops.wm.save_as_mainfile(filepath=str(output / 'knowledge-reuse.blend'))
    (output / 'evidence.json').write_text(json.dumps(evidence, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(evidence))
