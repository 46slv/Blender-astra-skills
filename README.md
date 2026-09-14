# Blender Astra Skills

Architecture-first repository for a Blender Agent Skill designed around **Astra as the solo/direct interactive Blender driver**.

The intended final Skill is currently named `blender-astra-modeling`.

## Current status

**ARCHITECTURE_ONLY / IMPLEMENTATION_PENDING / HOST_VALIDATION_PENDING**

This repository currently defines the implementation contract. It does **not** yet claim that the Skill, Blender adapters, visual-analysis helpers, or host fixtures are implemented or qualified.

## Core idea

Keep the live Blender visual/spatial state in one Astra context:

```text
OBSERVE
  -> reason about geometry / uncertainty
  -> choose the shortest execution lane
       GUI / Computer Use
       bpy / bounded Blender adapter
       Geometry Nodes / modifiers
  -> ACT directly
  -> re-observe at the required scale
  -> local repair
  -> structural + visual verification
```

Subagents are research-only by default: Blender Manual/API lookup, tutorial mining, version checks, export/consumer specs, and prior-art research. They do not own interactive Blender mutation or final visual acceptance.

## Read order

1. [`AGENTS.md`](AGENTS.md) — durable repository rules and routing.
2. [`GOAL.md`](GOAL.md) — current implementation outcome and acceptance.
3. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — system architecture and Skill boundary.
4. [`docs/VISUAL_ANALYSIS.md`](docs/VISUAL_ANALYSIS.md) — paired reference/model inspection, segmentation, boundaries, occlusion, detail verification.
5. [`docs/PROCEDURAL_AUTHORING.md`](docs/PROCEDURAL_AUTHORING.md) — Geometry Nodes procedural-leverage contract.
6. [`docs/PRIOR_ART.md`](docs/PRIOR_ART.md) — existing Blender Agent Skills to inspect and reuse before rebuilding.
7. [`docs/EVALS.md`](docs/EVALS.md) — representative fixtures and promotion gates.

## Intended Skill shape

```text
blender-astra-modeling/
  SKILL.md
  references/
    observation-protocol.md
    visual-structural-analysis.md
    method-routing.md
    geometry-nodes-routing.md
    repair-policy.md
    consumer-checks.md
  scripts/
    scene_report.py
    capture_fixed_views.py
    frame_target.py
    capture_region.py
    make_edge_map.py
    extract_silhouette.py
    align_comparison_pair.py
    compose_comparison_packet.py
    blender_diagnostic_passes.py
    compare_region_masks.py
    validate_evidence_packet.py
  schemas/
    observation_plan.schema.json
    visual_receipt.schema.json
    semantic_region_map.schema.json
    occlusion_graph.schema.json
    comparison_packet.schema.json
    repair_ticket.schema.json
```

The structure above is a target, not a requirement to implement every file immediately. Reuse upstream components where they are better and compatible.

## Design priorities

- Astra solo/direct host operation for interactive Blender work.
- Active perception rather than one-shot screenshot judgement.
- Paired reference/model close-ups at comparable view, framing, orientation, and scale.
- Perception-before-judgement: silhouette, edge, semantic region, boundary class, occlusion, landmark, Depth/Normal/object-mask evidence when useful.
- `UNKNOWN` remains `UNKNOWN`; invisible or ambiguous detail is not a PASS.
- Geometry Nodes used for procedural leverage, not for maximizing node usage.
- Preserve manual high-quality source parts and wrap/assemble them procedurally when appropriate.
- Derive contact/alignment/dependent transforms rather than exposing unnecessary raw XYZ controls.
- Preserve editable authoring source; destructive/export realization belongs in derived outputs.
- Reuse prior art before reimplementing analyzers, reference-fit loops, or GN knowledge.
- Promotion to active Skill requires representative host fixtures, not documentation completeness.

## Prior art

The current architecture intentionally builds on ideas from public projects including:

- `ifBars/blender-agent-studio`
- `RobLe3/cc-blender-skill`
- `CheshireJCat/create-3d-model-skill`
- `nodecue/blender-node-skills`
- `Aztech-Lab/EZ_Blender` as an orchestrated comparison baseline
- `achimala/dream-loop` as visual closed-loop prior art

See [`docs/PRIOR_ART.md`](docs/PRIOR_ART.md) before copying or reimplementing anything. Inspect current upstream code and licenses first.
