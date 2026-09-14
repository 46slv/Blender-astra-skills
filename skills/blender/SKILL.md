---
name: blender
description: Create, refine and inspect editable Blender models and scenes using direct visual feedback, bpy, Geometry Nodes, references and reusable assets. Use for Blender modeling, reference matching, procedural authoring, scene assembly, asset-library and model-knowledge work, and repairs.
---

# Blender

Keep the agent that sees the scene responsible for the next edit. Use research workers for independent questions; keep live Blender operation in one context. Deliver usable geometry and an editable `.blend`, with the views needed to judge the result.

This is a growing production skill, not a finished fixed recipe. Receive the goal,
references, available assets and authority; choose the research, representation,
operations and checks yourself. Treat user feedback as evidence about the desired
result; diagnose technical causes and choose the remedy rather than mechanically
following a suggested topology or modeling procedure.

## Start with the actual scene and runtime

Find the intended Blender/file, inspect its version, mode, active scene and visible result. Discover available tools before assuming an MCP exists. Prefer an already working direct bpy channel. GUI is useful for visual selection, sculpting, topology work and inspection; Python is useful for exact geometry and repeated changes. Switch as the task demands.

Before building from zero, look for useful project/library assets, generators and
methods in the focused references/examples. Inspect promising candidates and decide
whether reuse, adaptation or new authoring best serves this brief. Read
[assets.md](references/assets.md) for the working native Asset Library, discovery,
editable import and capture of authored or acquired resources. A poor existing
asset is not a reason to compromise the result.

For structural discovery and learning from past production, read
[knowledge.md](references/knowledge.md). Search explicit library roots for asset
and method cards by parts, relationships and use, then inspect the promising native
source. Choose direct reuse, adaptation, parts, a generator or new authoring from
the actual fit. Partial search matches do not prove requested capabilities.

If no suitable persistent channel exists, [runtime.md](references/runtime.md) gives a local session that needs only Blender and host Python. It starts a separate factory session, runs scripts on Blender's main thread and returns results without a network listener or add-on. It does not attach to an arbitrary open file. Other Blender windows may contain unsaved work.

## Make the next edit earn its cost

Establish the object scale, coordinate convention, silhouette and major part relationships. Choose a small next result you can see and judge. Author it, inspect its actual image, then inspect precise Blender state where that answers a remaining question. An executable script is not proof of a good model.

For a disputed detail, ask what observation distinguishes the competing explanations: a closer paired crop, a side view, a flat ID image, a surface normal, a topology view, or a contact measurement. Don't regenerate accepted regions to repair one seam or hinge. Keep a saved candidate before topology changes or broad edits; Python execution is not transactional undo.

Use the simplest editable representation with enough control:

| Intent | Usually useful starting point |
|---|---|
| Proportions, hard surface, exact components | Data API meshes, profiles, curves, modifiers |
| Hair locks, cables, pipes | Curves and editable cross sections |
| Repetition, dimensions that must stay related | Geometry Nodes, linked parts, instances |
| Separate moving components | Parent pivots, anchors, native constraints/drivers |
| Organic surface or animation topology | Existing mesh/rig, shape keys, sculpt/retopology tools |

See [authoring.md](references/authoring.md) for live GN probing, Blender 5.2 input changes, assembly frames and organic-work decisions. The [lamp](examples/articulated_lamp.py) and [shelf](examples/parametric_shelf.py) are working patterns to adapt, not templates that constrain unrelated requests.

## Reference refinement

Read [perception.md](references/perception.md) when fidelity or occlusion matters. Separate camera error from shape error; distinguish silhouette, overlap, material boundaries and shadows. Match projection and canvas before interpreting an overlay. A few trustworthy semantic correspondences beat a large set of guessed edges.

Use `observe.py` inside Blender for camera renders, projected points and evaluated, instance-aware surface probing. Use `fit.py` for a bounded, low-dimensional correction when you can define meaningful parameters and residuals. It applies each candidate to the actual scene and retains the best one. It does not discover correspondences or reconstruct arbitrary images.

Use `compare.py` on host Python for matched crops and overlays; Pillow and NumPy must be available there. Inspect resulting images directly. A silhouette metric cannot certify depth, anatomy, material quality or animation readiness.

## Finish with the source intact

Save a new candidate at the intended output location; preserve original user assets. Keep useful modifiers, curves, instances, parameter names/units and source scripts. Export a derived copy only when requested and inspect that exported result. Check the properties relevant to use: contacts and scale for assembly, actual evaluated instances for GN, normals/topology for meshes, deformation for rigged assets. Confirm a saved file reopens when persistence matters.

Report what is visually verified, what is structurally checked, and what remains inferred. Do not call a reference match complete if its decisive region is still hidden or too small to inspect.

## Leave the next production better equipped

Capture work worth reusing: props, furniture, materials, node groups, GN generators,
leaf/branch source parts, modular components or complete procedural systems. Keep
the smallest useful editable unit with its dependencies and usage knowledge; a
finished scene is not always the best asset. Use the same library approach for
acquired resources once their provenance and allowed uses are understood.

Store growing asset/model meaning and reuse evidence in library knowledge cards,
not an expanding Skill encyclopedia. Start with light indexing; deepen the card
when actual use reveals valuable structure, controls, failure modes or a better
method. Separate observed data, tested behavior and inferred design intent. A
static mesh cannot establish rig/deformation intent. When independent uses expose
a useful common invariant, link them in a method and consider a generic part, kit
or generator; preserve source quality and validate the claimed range of variation.

When production exposes a limitation, investigate the cause, try a remedy and
inspect the result. Generalize only what will improve another real task: a concise
method in the relevant reference, a useful helper or a reusable asset. Better shape,
topology, authoring or procedural reuse is worth adopting even if the old approach
already worked. Record measured discoveries and remaining limits in the project's
existing research/decision notes (here: `docs/RESEARCH.md`); replace stale advice
rather than accumulating rules. The current repo design and taxonomy can change.
Do not create a framework or documentation project to demonstrate improvement.
Complete individual deliveries without declaring the Skill permanently complete.
