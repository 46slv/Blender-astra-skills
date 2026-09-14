# A working native Asset Library

The bundled library is `assets/library` under the Skill directory. In code, use
`assets.LIBRARY` below to avoid path guessing.
Native `.blend` files hold marked IDs, descriptions, tags, previews and dependencies;
`blender_assets.cats.txt` holds Blender's catalogs. Optional `knowledge/*.json`
cards add structural meaning, methods and evidence outside the native datablocks;
see [knowledge.md](knowledge.md) for host-side search and staged learning. They
reference the native source rather than replacing Blender's asset storage.
The starter library works in Blender 5.2.1; probe other versions before promising
compatibility. Existing production scenes never have to run generator Python.

## Find and use before rebuilding

Inside Blender, with the Skill's `scripts` on `sys.path`:

```python
import assets
print(assets.find())                  # names/types/files, no scene mutation
print(assets.find('Shelf'))           # name substring; Browser also searches tags
library = assets.register()          # this process only, APPEND; no preferences save
# In an Asset Browser choose “Astra Project Assets” and the relevant catalog.
entry = next(a for a in assets.find('Lamp') if a['kind'] == 'collections')
lamp = assets.append(entry)          # fresh editable copy, internal hierarchy retained
print(lamp.asset_data.description, lamp.asset_data.license)
placement = next(o for o in lamp.objects if o.parent is None)
placement.location.x = 2.0
```

For parts/relations/use rather than names, search `knowledge.search(...)`, read
the full candidate and pass `knowledge.resolve(candidate)` to `assets.append`.
Use `assets.inspect(datablock)` on a staged candidate for native structural facts.
Native discovery still finds assets that have not yet received a knowledge card.

Pass an explicit project/private library directory to `find(root=...)` or
`register(root=...)`. Registration uses Blender preferences, so this helper disables
Auto-Save Preferences in the **dedicated process** before adding an entry. Do not
manually save those preferences. In a user's regular session use Current File or
an already configured library instead; don't change their preference workflow.
Read the brief, candidate descriptions and rights before use;
inspect promising candidates in staging if their quality or terms are unknown.
`find` supports collection, object, material and node-group assets. Use native
Blender discovery for other asset types. A missing configured library path is not
an empty, verified library; locate the intended files rather than inventing them.

Collections preserve assemblies. For the lamp, append an editable collection and
move its placement Empty; its three Y pivots pose the arms/head. Browser collection
drag can create an instance: suitable for placement, but append local objects or
make the instance real before independent posing. Avoid editing a shared source
collection when only one placed copy should change.

For a shelf object, edit its existing modifier with `gn.set_input`. For a standalone
generator, append the node group, assign it to a NODES modifier on a mesh host, then
set its inputs. Group defaults differ from an object preset's modifier overrides.
Materials append as datablocks for assignment to a material slot; inspect shared
mesh/material users before altering one copy. `assets.append` makes independent
copies across calls; reuse a returned material/group deliberately when sharing is
wanted. Blender `Append (Reuse Data)` has different sharing behavior.

## First reusable assets

All entries below are in `starter-v1.blend`, with custom native previews and stable
`asset_id` / `asset_version` custom properties. Catalog paths are browsing aids,
not identity; revise them when actual discovery needs change.

| Catalog | Native asset | Useful controls / limits |
|---|---|---|
| Lighting | Articulated Lamp v1 (Collection) | Base origin, meters, Z up, placement Empty, three pivots, shell, cable and GN fasteners. Cable is static; refit it after large pose changes. |
| Furniture | Parametric Shelf v1 (Object) | Width/Depth/Height/Levels; seven-board preset. Live instances, floor aligned. Solid color placeholder materials; no wood grain or joinery. Very low height with many levels can overlap boards. |
| Generators | Shelf Generator v1 | Four named inputs, five-level defaults; boards and four posts stay instanced. |
| Generators | Radial Fasteners v1 | Count 3–64. Fixed 0.10 m ring radius, hex bolt radius 0.0055 m/depth 0.007 m; brass included. |
| Materials | Forest Enamel v1, Satin Brass v1, Dark Rubber v1, Ivory Reflector v1, Warm Bulb v1 | Five Principled shaders. Brass has no brushed microtexture; bulb emission is not a calibrated light. |

Provenance: project-generated lamp/shelf from
[the original example artifact at c7b6f1a](https://github.com/46slv/Blender-astra-skills/blob/c7b6f1a/artifacts/blender-skill-examples.blend)
and the Skill's `examples/articulated_lamp.py` / `parametric_shelf.py`.
Generator Texts travel with the assets via `source_text` ID pointers. Those source
scripts import the Skill's `gn` / `observe` helpers if executed; the native assets
themselves have no Python dependency. Studio, cameras and floor are excluded.
There are no external textures or linked libraries in this starter release.
These are user-project assets, with no third-party input and no standalone license
grant specified by the owner. Public GitHub availability is not a reuse license
for unrelated users; do not invent CC0/MIT terms. No third-party assets were acquired
for this delivery.

The `.blend` is a datablock library, so opening it directly produces an empty scene
with assets available in Current File. Append/drag assets to use them in a scene.

## Capture work that will save future effort

Choose the useful unit and a sensible origin, real scale and editable controls.
Keep a branch/leaf source part separate from its scatter system when each is
independently useful. Mark the assembly, material or group with `ID.asset_mark()`.
Describe purpose, controls, coordinate/scale assumptions and meaningful limitations;
add a few searchable names/tags (including useful synonyms) and a catalog UUID.
Use native author/license fields and source references, keeping original author
credit on acquired work. Stable IDs and integer versions are the starter convention,
not a schema every future asset must obey.

Work on a copy in a dedicated staging session. Inspect dependencies: parents,
constraints, drivers, source objects, nested groups, textures, caches and fonts.
Pack permitted image files with `image.pack()` in that copy; make linked dependencies
local or deliberately retain and document a resolvable library relationship.
Path remapping alone does not copy textures. Keep non-packable resources alongside
the asset with relative paths and usage notes; do not call such a bundle self-contained
until it works without the source directory. Remove irrelevant scenes/private paths.
Do not pack or publish private references just because Blender can do so.

Use a truthful isolated render as a custom preview (`ed.lib_id_load_custom_preview`
with an ID context), or native preview generation when it works for that ID type.
For a generator, show a representative output and state the settings. Publish a
small `.blend` with `bpy.data.libraries.write(path, {asset_ids}, ...)`: referenced
IDs follow automatically, external files do not. Catalog definitions live at the
library root. Keep existing UUIDs when renaming/reorganizing catalogs.

Reopen/append from the saved bundle into a fresh scene, inspect the actual result,
change a meaningful control and check the dependencies relevant to this asset.
Keep original sources and released versions intact; write a new revision for a
behavior/interface change so linked consumers do not silently change. Record the
reason and replacement in the existing project notes. Git tracks scripts/catalogs
and small owned binaries here; large or restricted assets belong in an appropriate
authorized local library, not automatically in a public PR.

For downloads/acquisitions, retain the original archive/files and license evidence
beside the private source or bundle. Record source URL, creator, acquired version/date,
license and allowed uses: commercial use, modification, attribution and redistribution
where relevant. Preserve notices and derivative attribution; distinguish permission
to render an asset from permission to republish its source/texture. Unclear terms:
leave outside the reusable published library and investigate the source. Known
restrictions: keep in a suitably scoped private library with visible usage limits.
No new service, purchase or bulk download is needed merely to exercise this policy.

After capture, leave a light knowledge card with the exact source reference, rights,
purpose and useful structural terms. On real reuse, update its understanding and
evidence without changing the native asset version unless the asset itself changes.
Method cards can link several assets or tutorials without duplicating their geometry.

The extraction example is `experiments/build_asset_library.py` at repo root; it writes
to a new `ASSET_OUTPUT` directory and keeps the original scene file intact. Adapt
that small production script when it helps; do not force unrelated assets through it.
