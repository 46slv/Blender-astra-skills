# Authoring decisions that preserve leverage

## Geometry Nodes

Probe the installed Blender when uncertain. The MIT-licensed NodeCue probe is bundled unchanged:

```python
from vendor.probe_node import run
print(run({'bl_idname':'GeometryNodeMeshLine','properties':{'mode':'END_POINTS'}}))
```

It creates and removes a temporary node tree and reports sockets, active modes and cleanup. Set node `mode`/`data_type` first: these can replace sockets or leave inactive sockets with duplicate labels. `gn.socket(collection, name=..., identifier=...)` refuses missing/ambiguous active sockets. The Mesh Line endpoint is still RNA `Offset` in the tested END_POINTS mode: inspect instead of guessing from UI text.

Create group inputs via `tree.interface.new_socket(...)`. Blender 5.2 modifier input values use typed RNA:

```python
from gn import set_input, graph
print(set_input(modifier, 'Levels', 7))
print(graph(modifier.node_group))
# Underlying 5.2 API: getattr(modifier.properties.inputs, interface_socket.identifier).value
```

Assign `modifier.node_group` first. `modifier[identifier] = value` may silently write an irrelevant custom property on newer Blender. `set_input` handles the live typed path and returns the actual value; evaluate geometry afterwards. Count instantiated boards, measure bounds and check the output trunk, not just that input assignment succeeded.

Keep sources/instances until the consumer needs per-copy geometry. `obj.to_mesh()` and `bound_box` alone can miss GN-only instances. Iterate `depsgraph.object_instances`, copy matrix/bounds/IDs **inside** the iterator and don't retain its transient RNA objects. Named attributes live on specific domains; fields are evaluated by the consuming node's context. A Raycast/Proximity input in the wrong coordinate space is a plausible-looking wrong graph. Check hit/valid outputs. Avoid shared node-group edits when only one asset should change: copy the group or use modifier inputs.

## Assembly and support

Separate rigid parts work well with semantic Empty anchors and parent pivots. For child-object-local socket matrix `S` and target-world socket matrix `P`:

```python
child.matrix_world = P @ S.inverted()
bpy.context.view_layer.update()
```

If mating normals oppose, insert an explicit rotation: `P @ flip @ S.inverted()`. Read back `(child.matrix_world @ S)` against `P @ flip`. If an existing socket is stored in world coordinates, first convert with `child.matrix_world.inverted() @ socket_world`. Native parents or a deliberate Copy Transforms/Child Of constraint can retain following; plain matrix assignment is a one-time placement. Use an acyclic hierarchy; Blender constraints are an ordered stack, not a global CAD solver.

For support, ray-cast from the intended contact/foot along a known direction, then offset the assembly by the measured signed gap. Test all intended feet: placing one origin on a surface does not make a chair stand correctly. Preserve upright orientation unless the brief calls for normal alignment. Nonplanar support may require adjustable feet, a different placement or rejecting the candidate. AABB overlap is only a broad-phase warning, not proof of collision or contact.

## Modeling and organic work

Begin from useful existing assets when available and authorized. Inspect their transforms, dimensions, topology, modifiers, shape keys, rig and materials before replacing structure. Use high-level proportions or shape keys for reference fitting; unrestricted vertex fitting to one view collapses depth and damages deformation.

For rotational products, lathed profiles expose the actual design decisions. Merge poles to single vertices, close thickness at the rim/neck, and check nonmanifold edges/degenerate faces. A shaded render can hide invalid topology. The lamp example retains profile-ring meshes, a real inner wall, editable Bezier cable and three native pivots.

For hair, use authored guide curves/cross sections and explicit clump overlap before fine strands. For stylized/anime mesh hair, when the representation or topology itself is uncertain, search the knowledge cards for `anime short hair shared root shell ribbon clump` and read [anime_hair.md](anime_hair.md) if it looks relevant. Treat it as a candidate method rather than a required recipe; the current references and observed Blender result outrank it. For faces, align camera and head proportions, then inspect paired eye/mouth/hairline regions. Use side/three-quarter views to distinguish projection from depth. Preserve rig, shape keys and accepted topology during local repairs. Use actual sculpt/retopology tools for freeform work where a parameterized mesh is weaker; do not substitute primitive assemblages and call them finished anatomy. These choices are workflow guidance; the shipped experiments do not validate production character rigging.

Keep procedural relationships only where they remove repeated repair. The lamp uses native pivots for moving separate parts and GN only for fastener repetition. The shelf derives spacing/post centers from Width, Depth, Height and Levels, with meters as units. No custom scene schema or global constraint engine is needed.

## Saved source

For material refinements, inspect actual shader inputs and links; viewport
`diffuse_color` need not control the rendered Base Color. A linked socket ignores
its unlinked default. Check material/mesh users before a local edit: copy shared
materials, and copy shared mesh data before replacing its material slots. Preserve
face material indexes (the lamp shade's exterior and interior use different slots).

Keep the generator beside the output or in a Blender Text datablock along with parameter values. The saved artifact must remain directly editable without the session helper. Reopen a candidate and check its visible geometry and procedural controls. Export requirements (applied modifiers, realization, triangulation, textures, units) depend on the requested consumer; don't flatten the authoring source by default.
