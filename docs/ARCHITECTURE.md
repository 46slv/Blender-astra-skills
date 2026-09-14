# Implemented architecture

The runtime entrypoint is `skills/blender/SKILL.md`; don't load the research archive
as a second instruction framework.

Astra owns the image → decision → edit → image loop. It chooses between available
GUI, direct bpy and persistent native authoring structures. Research can fan out;
live scene mutation has one operator.

The only execution fallback is a local file queue serviced by a Blender main-thread
timer. It avoids an add-on install, socket/MCP service, process restart per edit and
background-thread bpy. Requests have IDs, file/session checks and explicit unknown
outcomes. Arbitrary Python remains trusted local code; there is no sandbox or rollback.

Observation uses existing cameras, temporary render settings, analytic projection,
evaluated geometry BVHs and matched image crops. NumPy least squares operates on a
small set of author-selected controls. Native parents and GN retain editability.

NodeCue's live node probe is reused under MIT. No SceneIR, mandatory segmentation
stack, semantic database, global solver, new agent role, paid asset service or model
download proved necessary for the completed trials.

Reusable production work lives in ordinary native Blender asset libraries: marked
collections/objects/materials/node groups, native metadata/previews and catalog
UUIDs. A small bpy helper discovers and appends assets; there is no parallel asset
database. Authored and acquired resources follow the same reuse approach, with
provenance and rights controlling which library can contain/distribute them.

The Skill remains in continuing development. Production starts by considering
existing assets and methods; demonstrated solutions and better authoring return
to the appropriate asset, focused reference or helper. User feedback describes
the desired result; Astra owns diagnosis and method selection. Architecture and
taxonomy can change when actual production benefits.

See [RESEARCH.md](RESEARCH.md) for competing approaches, actual evidence and limits.
