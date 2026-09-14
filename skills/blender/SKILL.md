---
name: blender
description: Create, refine and inspect editable Blender models and scenes using direct visual feedback, bpy, Geometry Nodes and reference images. Use for real Blender modeling, reference matching, procedural assets, scene assembly and repairs.
---

# Blender

Keep the agent that sees the scene responsible for the next edit. Use research workers for independent questions; keep live Blender operation in one context. Deliver usable geometry and an editable `.blend`, with the views needed to judge the result.

## Start with the actual scene, runtime, and reusable assets

Find the intended Blender/file, inspect its version, mode, active scene and visible result. Discover available tools before assuming an MCP exists. Prefer an already working direct bpy channel. GUI is useful for visual selection, sculpting, topology work and inspection; Python is useful for exact geometry and repeated changes. Switch as the task demands.

Before rebuilding something common, inspect the reusable assets already available to the current Blender environment or project. Prefer adapting a good existing object, collection, material, node group, procedural generator, or reusable part when it gives a better result faster than starting over.

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

When the work produces something that would materially accelerate later work, **harvest it as a reusable asset instead of leaving it buried in a one-off scene**. Prefer Blender-native assets for objects, collections, materials and node groups, and keep procedural controls/source intact. This applies both to finished objects and to reusable building blocks such as lamp joints, furniture collections, Geometry Nodes generators, support/contact helpers, room modules and materials. Read [assets.md](references/assets.md) when promoting or reusing assets.

Do not assetize every temporary object. Promote the pieces that have real reuse value, are understandable outside the current scene, and can be brought back without hidden project-specific dependencies. The goal is a compounding library, not a larger archive.

Report what is visually verified, what is structurally checked, what remains inferred, and any reusable asset that was added or improved. Do not call a reference match complete if its decisive region is still hidden or too small to inspect.
