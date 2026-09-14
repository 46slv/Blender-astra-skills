# AGENTS.md

This repository is for designing and implementing the `blender-astra-modeling` Agent Skill.

## Read order

Before substantial implementation:

1. `GOAL.md`
2. `docs/ARCHITECTURE.md`
3. only the relevant focused documents under `docs/`

Do not turn this file into the full manual. Durable architecture belongs in `docs/`; repeatable procedures belong in the Skill/scripts; current implementation outcome belongs in `GOAL.md`.

## Core operating rules

- **Astra is the default solo/direct interactive Blender driver.** Keep observation, planning, host operation, local review, and repair in one Astra context when working in live Blender.
- Subagents are **research-only by default**: Blender Manual/API lookup, tutorial mining, version checks, export/consumer specs, and prior-art research. Do not delegate interactive Blender GUI mutation, main `.blend` mutation, Computer Use, Blender write operations, or final visual acceptance to a child merely because the task is difficult or parallelizable.
- Prefer the shortest correct execution lane per operation: GUI/Computer Use for visual/spatial edits; bounded `bpy`/adapter operations for deterministic scene changes; Geometry Nodes/modifiers for persistent procedural logic.
- Treat broad screenshots as navigation evidence only. Fine-detail/final visual PASS requires target-framed and region-level evidence.
- Compare **reference and model together** at matched semantic region, view/orientation, framing, and useful scale. If the feature is not actually visible, result is `UNKNOWN`, not PASS.
- When raw visual judgement is ambiguous, build structured evidence: silhouette, edge map, semantic region mask, boundary class, occlusion/overlap relation, landmarks, and model-side Depth/Normal/object-mask/wireframe evidence as applicable.
- Edge detection is evidence, not semantic truth. Distinguish silhouette, occlusion, construction, material, shading, texture, and unknown boundaries before converting a line into geometry intent.
- Keep repair local: declare changed region/write set and protect accepted neighboring regions.
- Preserve editable authoring source. Do not destroy source `.blend`, apply/realize/remesh broadly, or overwrite accepted source solely to satisfy an export format.
- Use Geometry Nodes for **procedural leverage**, not for maximizing node usage. Manual high-quality source parts may remain authoritative and be wrapped/assembled procedurally.
- Prefer semantic/design parameters over raw transforms. Derive contact, alignment, spacing, and dependent transforms when the relation can be solved and verified.
- Inspect current upstream prior art before reimplementing equivalent analyzers or workflows. Check licenses before copying code.

## Prior art reuse

At minimum inspect `docs/PRIOR_ART.md` before implementing:

- reference comparison / overlays / landmarks;
- segmentation / contour / mask / multiview fitting;
- Geometry Nodes graph knowledge;
- Blender safety / bounded adapters;
- benchmark/eval harnesses.

Borrow concepts and compatible code where appropriate; do not silently vendor external code without license/provenance review.

## Verification

A task is not complete because a file exists or Blender returned success.

Use both:

- structural evidence: scene/object/node/modifier/topology/dependency/export reports;
- visual evidence: fixed/matched views, paired close-ups, relevant diagnostic passes.

For changed detail, regenerate the **same comparison packet** after repair, then perform a broader regression view.

## Skill activation boundary

The architecture may be implemented autonomously within repository scope, but do not declare the Skill generally qualified until representative host fixtures in `docs/EVALS.md` pass. Documentation completeness is not host qualification.
