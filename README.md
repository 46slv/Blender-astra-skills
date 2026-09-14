# Blender Astra Skills

Research-and-build repository for a Blender Skill designed around one premise:

> Give Astra enough context, access, and research depth to discover a better way to work in Blender than we can fully prescribe in advance.

## Status

**RESEARCH / ARCHITECTURE SEED — IMPLEMENTATION PENDING**

The repository currently contains prior research and design ideas. They are not a fixed specification.

## Goal

Build a practical, unusually capable Blender Skill for Astra.

Astra should understand the live capabilities available to it, research the problem space broadly, reuse strong prior art where useful, invent new mechanisms where useful, and finish something it can actually use in Blender.

See [`GOAL.md`](GOAL.md).

## Working hypothesis

Interactive Blender work probably benefits from keeping visual/spatial continuity inside one Astra context:

```text
Astra sees
→ Astra reasons
→ Astra acts
→ Astra looks again
→ Astra adapts
```

Research is different. Research can fan out aggressively to Luna/subagents because it does not require ownership of the live Blender state.

Astra should generate multiple plausible approaches for meaningful unknowns, delegate independent investigations, and synthesize the results itself.

## The docs are ideas, not obligations

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — current design space and hypotheses.
- [`docs/VISUAL_ANALYSIS.md`](docs/VISUAL_ANALYSIS.md) — ways to augment fine visual perception and reference/model comparison.
- [`docs/PROCEDURAL_AUTHORING.md`](docs/PROCEDURAL_AUTHORING.md) — Geometry Nodes / procedural-authoring opportunities.
- [`docs/PRIOR_ART.md`](docs/PRIOR_ART.md) — existing Blender Agent work worth inspecting and extending.

Astra may simplify, replace, or discard these ideas after research or implementation.

## Important directions discovered so far

- Keep live Blender manipulation with Astra by default rather than fragmenting visual context across host-operating agents.
- Use Luna/subagents heavily for research, including competing approaches and adjacent fields.
- Improve perception before editing when a detail is ambiguous: zoom, compare reference/model at the same region, expose structure, or use image/Blender-derived evidence when useful.
- Treat semantic regions, overlap/occlusion, landmarks, masks, Depth/Normal and similar signals as possible aids—not a mandatory visual pipeline.
- Use Geometry Nodes where procedural relationships create real leverage: reusable parts, parametric assets, modular assembly, contact/alignment, repeated layouts and environments.
- Do not force Geometry Nodes when ordinary modeling or another mechanism is better.
- Reuse strong existing Skills and code instead of rebuilding solved components.
- Avoid infrastructure that exists only to make the repository look rigorous.

## Prior art seed

Current high-value sources include:

- `ifBars/blender-agent-studio`
- `RobLe3/cc-blender-skill`
- `CheshireJCat/create-3d-model-skill`
- `nodecue/blender-node-skills`
- `Aztech-Lab/EZ_Blender`
- `achimala/dream-loop`

This list is deliberately incomplete. Astra should search beyond it and beyond Blender-specific agent projects.

## For Astra

Start with `AGENTS.md` and `GOAL.md`.

Then inspect the current repo, the live runtime, and whatever research is useful. Do not implement the current documents mechanically. Make the best Skill you can discover, and keep the repository only as complicated as the resulting capability actually requires.
