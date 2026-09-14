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
