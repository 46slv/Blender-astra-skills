"""Native asset discovery and local append, run inside Blender. No saved preferences.

find() lists marked IDs without loading them into the scene. Pass another library
root for project/private libraries; metadata stays on the native Blender asset.
"""
from pathlib import Path
import bpy


LIBRARY = Path(__file__).resolve().parents[1] / 'assets' / 'library'
KINDS = ('collections', 'objects', 'materials', 'node_groups')


def find(query='', root=LIBRARY):
    root = Path(root).resolve()
    if not root.is_dir():
        raise FileNotFoundError(root)
    result = []
    for path in sorted(root.rglob('*.blend')):
        with bpy.data.libraries.load(str(path), assets_only=True) as (source, _):
            for kind in KINDS:
                result.extend({'file': str(path), 'kind': kind, 'name': name}
                              for name in getattr(source, kind)
                              if query.casefold() in name.casefold())
    return result


def append(asset, collection=None):
    """Append a fresh editable copy plus dependencies; link object/collection IDs.

    Choose an exact entry from find(). Shared dependencies within this append stay
    shared; repeated calls create independent copies. Materials/groups are returned
    for assignment. This deliberately does not execute embedded generator Texts.
    """
    kind, name = asset['kind'], asset['name']
    if kind not in KINDS:
        raise ValueError(kind)
    with bpy.data.libraries.load(asset['file'], link=False, assets_only=True) as (source, target):
        if name not in getattr(source, kind):
            raise KeyError((asset['file'], kind, name))
        setattr(target, kind, [name])
    datablock = getattr(target, kind)[0]
    destination = collection if collection is not None else bpy.context.scene.collection
    if kind == 'collections':
        destination.children.link(datablock)
    elif kind == 'objects':
        destination.objects.link(datablock)
    return datablock


def register(root=LIBRARY, name='Astra Project Assets'):
    """Expose a library in a dedicated Blender process; disable preference auto-save.

    This is a preferences entry, not a separate transient registry. Auto-save stays
    off in this process; do not manually save its preferences. Use a dedicated
    session so the user's normal preference editing is unaffected.
    """
    root = Path(root).resolve()
    if not root.is_dir():
        raise FileNotFoundError(root)
    preferences = bpy.context.preferences
    libraries = preferences.filepaths.asset_libraries
    for library in libraries:
        if Path(library.path).resolve() == root:
            return library
    preferences.use_preferences_save = False
    library = libraries.new(name=name, directory=str(root))
    library.import_method = 'APPEND'
    return library


def inspect(datablock):
    """Read bounded structural facts from an already staged ID, without evaluating.

    This is evidence for an agent to interpret, not reverse-engineered design intent.
    No mesh coordinates, weight arrays or embedded source scripts are executed.
    Use observe.SurfaceProbe/depsgraph and pose trials for evaluated behavior.
    """
    def value(v):
        if isinstance(v, bpy.types.ID):
            return {'name': v.name, 'type': v.id_type}
        if isinstance(v, (str, int, float, bool, type(None))):
            return v
        try:
            return list(v)
        except TypeError:
            return str(v)

    def group_info(group):
        return {'name': group.name, 'type': group.bl_idname,
                'inputs': [{'name': s.name, 'identifier': s.identifier,
                            'type': s.socket_type,
                            'default': value(getattr(s, 'default_value', None))}
                           for s in group.interface.items_tree
                           if s.item_type == 'SOCKET' and s.in_out == 'INPUT'],
                'nodes': [{'name': n.name, 'label': n.label, 'type': n.bl_idname,
                           'group': n.node_tree.name if getattr(n, 'node_tree', None) else None}
                          for n in group.nodes],
                'links': [[l.from_node.name, l.from_socket.identifier,
                           l.to_node.name, l.to_socket.identifier] for l in group.links]}

    def input_value(mod, socket):
        if hasattr(mod, 'properties'):
            prop = getattr(mod.properties.inputs, socket.identifier, None)
            return {'mode': getattr(prop, 'type', 'VALUE'),
                    'value': value(getattr(prop, 'value', None)),
                    'attribute': getattr(prop, 'attribute_name', None)}
        return {'value': value(mod.get(socket.identifier, getattr(socket, 'default_value', None))),
                'attribute': mod.get(socket.identifier + '_attribute_name'),
                'use_attribute': mod.get(socket.identifier + '_use_attribute', False)}

    meta = datablock.asset_data
    report = {'name': datablock.name, 'type': datablock.id_type,
              'asset_id': datablock.get('asset_id'), 'asset_version': datablock.get('asset_version'),
              'description': meta.description if meta else None,
              'license': meta.license if meta else None,
              'tags': [t.name for t in meta.tags] if meta else [],
              'source_text': value(datablock.get('source_text')),
              'scope': 'Authored data only; pose/deformation, evaluated geometry and intent need trials.'}
    objects = (list(datablock.all_objects) if isinstance(datablock, bpy.types.Collection)
               else [datablock] if isinstance(datablock, bpy.types.Object) else [])
    groups = {}
    report['objects'] = []
    for obj in objects:
        modifiers = []
        for mod in obj.modifiers:
            item = {'name': mod.name, 'type': mod.type,
                    'viewport': mod.show_viewport, 'render': mod.show_render}
            if getattr(mod, 'node_group', None):
                group = mod.node_group
                groups[group.name] = group
                item['group'] = group.name
                item['inputs'] = {s.name: input_value(mod, s)
                                  for s in group.interface.items_tree
                                  if s.item_type == 'SOCKET' and s.in_out == 'INPUT'}
            if getattr(mod, 'object', None):
                item['target'] = mod.object.name
            modifiers.append(item)
        mesh = obj.data if obj.type == 'MESH' else None
        keys = getattr(obj.data, 'shape_keys', None)
        report['objects'].append({
            'name': obj.name, 'type': obj.type, 'parent': obj.parent.name if obj.parent else None,
            'parent_type': obj.parent_type, 'parent_bone': obj.parent_bone,
            'location': list(obj.location), 'rotation_mode': obj.rotation_mode,
            'matrix_local': [list(row) for row in obj.matrix_local],
            'modifiers': modifiers,
            'constraints': [{'name': c.name, 'type': c.type, 'influence': c.influence,
                             'target': value(getattr(c, 'target', None)),
                             'subtarget': getattr(c, 'subtarget', None)} for c in obj.constraints],
            'materials': [s.material.name if s.material else None for s in obj.material_slots],
            'mesh': {'vertices': len(mesh.vertices), 'polygons': len(mesh.polygons),
                     'uv_layers': [uv.name for uv in mesh.uv_layers]} if mesh else None,
            'vertex_groups': [v.name for v in obj.vertex_groups],
            'shape_keys': [{'name': k.name, 'value': k.value} for k in keys.key_blocks] if keys else [],
            'bones': [{'name': b.name, 'parent': b.parent.name if b.parent else None,
                       'deform': b.use_deform} for b in obj.data.bones] if obj.type == 'ARMATURE' else [],
            'drivers': [{'path': d.data_path, 'index': d.array_index}
                        for d in obj.animation_data.drivers] if obj.animation_data else []})
    if isinstance(datablock, bpy.types.NodeTree):
        groups[datablock.name] = datablock
    if isinstance(datablock, bpy.types.Material) and datablock.node_tree:
        groups[datablock.node_tree.name] = datablock.node_tree
    report['node_groups'] = [group_info(g) for g in groups.values()]
    return report
