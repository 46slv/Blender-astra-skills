# Anime mesh-hair method candidate

Read this only when stylized/anime hair, mesh-clump topology, bangs, or a hair-authoring representation is actually relevant. It is prior art and a decision aid, not a recipe to reproduce mechanically. Current references, the live Blender result, and a clearly better method outrank this document.

## Core idea

Treat an anime hairstyle as an assembly of regions that may need different topology. Do not assume the whole hairstyle should be one cap, one curve system, or many identical independent locks.

Three useful topology families were inferred from the practitioner source and supplied still frames:

- **Shared-root shell** — a scalp-conformed local patch whose root area stays continuous while partial slits free the lower strips. Useful where root continuity matters, especially bangs or face-adjacent sheets.
- **Solid ribbon clump** — a thin prism/ribbon/wedge with cross-sections placed where bend, width, depth, roll, taper or tip shape needs control. Useful for independently shaped side/back locks.
- **Compound accent clump** — one or more authored ribbon/wedge sub-clumps forming a curl, fork, hook, hane or other silhouette feature. Keep a good manual source when a generic generator would reduce shape quality.

Topology family and hairstyle role are separate questions. A `PRIMARY` silhouette element can be a shared shell or an independent clump; `ACCENT` describes visual function, not mesh construction.

Useful layer roles:

- `BASE / SCALP MASS` — broad volume or coverage when needed;
- `PRIMARY` — bangs, sides, back locks that define the main silhouette;
- `INNER / NAPE FILL` — fills gaps and supports depth/readability;
- `ACCENT` — curls, forks, hane, ahoge and deliberate silhouette breaks.

## Shared-root shell: semantic construction

A useful interpretation of the observed front-hair sequence is:

```text
coarse plane / patch
→ fit to the relevant scalp/front surface
→ place coarse cross-sections for curvature control
→ establish longitudinal flow edges
→ add local control sections only where curvature/silhouette needs them
→ cut partial slits from the free edge toward the root
→ preserve a shared root bridge
→ shape each freed strip tip independently
```

The point is not this exact Blender operation order. Preserve the meaning:

`surface fit → control sections → flow topology → partial separation → strip-tip shaping`.

A slit is not merely a cut to make separate objects. It can increase tip freedom while leaving the upper/root area continuous. Cross-loops are primarily control sections, not uniform subdivision targets. Longitudinal edges express flow and strip width boundaries.

Potential authoring controls:

```text
shell_patch
cut_graph
root_bridge_depth
strip_length / direction / curl
local width/depth
local tip shape
```

## Solid ribbon clump: semantic construction

A simple clump can be thought of as:

```text
ribbon / thin prism / wedge
→ section placement
→ bend / roll
→ width + depth shaping
→ taper
→ pointed / swept / hooked / blunt tip
```

A guide curve plus a custom cross-section can be a good implementation, but it is not mandatory. Place more sections where curvature or tip behavior changes; do not add loops uniformly just because the tutorial did.

## Compound accent clumps

Strong curls, forks and silhouette hooks may be better as manually authored reusable sources or as a small modular assembly of compatible sub-clumps. Preserve the source and proceduralize only the parts that buy leverage: root placement, guide deformation, scale, roll, local variation, attachment and layer placement.

Do not force every distinctive lock through one universal Geometry Nodes generator.

## Choosing a representation

A useful heuristic:

```text
root continuity matters strongly
    → consider shared-root shell

independent local deformation matters more
    → consider solid ribbon clump

shape identity depends on a special curl/fork/hook
    → consider compound/manual source
```

Mix these in one hairstyle when that gives a better editable source. Geometry Nodes, bpy, curves, normal mesh editing and GUI work may all coexist.

## Reference-driven fitting

For anime hair, prioritize what changes identity most:

1. outer silhouette in front and side views;
2. bangs-to-face boundary and the negative spaces around eyes, cheeks and ears;
3. parting/root zones and major flow directions;
4. side/back depth and overall volume;
5. primary clump widths/depths;
6. accents and small silhouette breaks.

If front/side references are strong, reduce the 3D search space by extracting or mentally tracing 2D silhouettes/flows first, then fit the 3D shell/clumps to both views. Bangs usually deserve higher visual authority than hidden filler hair.

Do not treat generated hidden views as stronger truth than the original visible reference.

## Optional bounded experiment when the right method is unclear

Before committing a full character, Astra may choose a small disposable experiment rather than arguing about topology in the abstract.

One useful pattern is:

```text
preserve the accepted character/source
→ make a duplicate candidate .blend or isolated collection
→ derive or copy only the head/scalp needed for the test
→ keep body/outfit complexity out of the experiment
→ build a representative hair slice or full short-hair candidate
→ compare front / side / 3/4 silhouette and close topology
→ ask the human for visual audit if that would resolve a real ambiguity
→ keep, revise or reject the method
```

For an `ss` task, a head-only derivative can be a good fixture if the current project already has a usable head. Do not damage the authoritative model to create the fixture. A human audit is useful as a design signal when two plausible interpretations remain; it is not a mandatory gate for every hair edit.

A candidate experiment can compare, for example:

- shared-root front shell versus fully independent front clumps;
- manual ribbon clumps versus curve-driven wrappers;
- a hand-authored accent source versus a generalized generator.

Judge by final silhouette, face framing, overlap, editability and repair cost—not by how procedural the graph looks.

## Source preservation and output

Keep source shells, clumps, guides and meaningful parameters editable. Joining, realization, triangulation, optimization and consumer-specific merge belong to derived output unless the target format truly requires them in the authoring master.

Do not make every short-hair element dynamic. Head-following base regions can stay rigid/skinned; add sub-rig or dynamics only where visible secondary motion earns it.

## Evidence and confidence

Status: **candidate method / visual-source interpretation, not host-qualified production truth**.

Evidence basis:

- practitioner source: たたかう伊藤, `3D Model Topology 1 | Short Hair`, https://www.youtube.com/watch?v=QjwhdX6AHnU
- user-provided chronological summary and multiple still frames inspected on 2026-09-15;
- a one-second local frame sequence may be supplied by the task runtime; inspect it directly when available instead of treating this summary as exhaustive.

Observed/inferred distinction:

- observed in supplied frames: local scalp-conformed patch, longitudinal/cross-loop topology, partial slit behavior, independent ribbon/wedge clumps, compound curled elements, layered exploded assembly;
- inferred: the three-family abstraction and the transfer heuristics above;
- untested here: exact reconstruction in Blender, transfer to `ss`, deformation behavior, GN implementation, production export.

If a real character test succeeds and the method is useful again, deepen the knowledge card with what actually transferred. If it fails, revise or retire the candidate rather than protecting the document.
