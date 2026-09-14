# Prior Art — Reuse Before Rebuild

## Purpose

This repository should not reimplement a full Blender-agent stack before inspecting current public Skill systems that already solve part of the problem.

Before copying code:

1. read the current upstream implementation, not only this summary;
2. inspect the exact license and provenance;
3. compare behavior against this repo's architecture;
4. reuse/adapt only the compatible component;
5. preserve attribution/license obligations where required;
6. keep local behavior/evals as the authority for promotion.

## 1. `ifBars/blender-agent-studio`

Repository: https://github.com/ifBars/blender-agent-studio

Status: **highest-value overall workflow candidate**.

Observed useful ideas:

- specialist Blender Skills for modeling, validation, iterative refinement, Geometry Nodes/procedural work, rendering, character work, animation, simulation, and benchmarking;
- explicit Astra-oriented execution guidance;
- staged modeling contract rather than one open-ended Blender prompt;
- reference cameras with fixed crop/framing during geometry comparison;
- projected model silhouette + reference overlay;
- authored landmarks for precise local diagnosis;
- multiview evidence instead of optimizing one projection;
- individual high-detail views when a contact sheet cannot resolve a defect;
- durable/reproducible source and fresh-export validation;
- bounded Blender tooling rather than assuming arbitrary Python access is safe;
- benchmark methodology instead of assuming that more Skill text improves results.

### Reuse direction

Prefer to borrow/adapt:

- staged modeling workflow;
- reference-camera and overlay concepts;
- landmark comparison ideas;
- fixed-view evidence discipline;
- bounded inspection/adapter ideas;
- benchmark/evidence design.

Do **not** automatically inherit any architecture that forces Blender host operation into separate agents. In this repository Astra stays the solo/direct interactive host driver by default.

## 2. `RobLe3/cc-blender-skill`

Repository: https://github.com/RobLe3/cc-blender-skill

Status: **highest-value reference-analysis candidate**.

Observed relevant modules include:

- `reference-to-3d`
- `reference-analysis-validator`
- `source-part-segmentation`
- `contour-to-mesh`
- `orthographic-registration`
- `multiview-constraint-solver`
- `texture-driven-mesh-fitting`
- `landmark-fit-repair`
- `multiview-fit-loop`
- `fit-repair-optimizer`
- `reference-look-calibration`

Useful concepts already present:

- source manifests;
- masks/components/landmarks;
- render/reference overlays;
- part counts;
- centroids/bounding boxes;
- SSIM/IoU as bounded validation metrics;
- compare-like-with-like modality rules;
- render → compare → adjust → render loops;
- source-part segmentation and landmark repair.

### Reuse direction

Inspect and replay its analyzers before writing new versions of:

- edge-map generation;
- silhouette extraction;
- region-mask comparison;
- landmark fitting;
- paired overlays;
- multiview fit loops;
- image/reference manifests.

Keep this repo's stronger explicit contracts unless upstream proves equivalent behavior:

- boundary-class taxonomy;
- explicit occlusion graph;
- `UNKNOWN` handling;
- model-side Depth/Normal/exact object-region masks;
- mandatory paired semantic close-ups;
- Astra-solo active perception.

Metrics such as SSIM/IoU remain evidence, not semantic truth.

## 3. `CheshireJCat/create-3d-model-skill`

Repository: https://github.com/CheshireJCat/create-3d-model-skill

Status: **practical Codex-native base candidate**.

This project packages the RobLe3-style stack for Codex with one entry point, many on-demand modules, image-analysis/validation helpers, scene-safety handling, screenshot inspection, versioned `.blend` preservation, and output validation.

### Reuse direction

If the target harness benefits from an already Codex-shaped Skill tree, inspect this before manually porting the full upstream layout.

Do not assume its defaults equal this repository's final policy; retain Astra-solo and the visual-structure contract.

## 4. `nodecue/blender-node-skills`

Repository: https://github.com/nodecue/blender-node-skills

Status: **Geometry Nodes component candidate**.

Useful observed direction:

- dedicated Geometry Nodes Skill;
- version/evidence-aware node/socket knowledge;
- graph readback → verify → repair;
- avoidance of unnecessary `Realize Instances`;
- correspondence with normal Blender naming/tutorial language.

### Reuse direction

Use this as a candidate lower-level GN knowledge/adapter layer.

Keep this repository's higher-level procedural-authoring decisions above it:

- manual-source wrapper vs full generator;
- semantic part interfaces;
- contact/support solvers;
- environment/layout architecture;
- design parameter vs derived parameter policy.

## 5. Comparison baselines

### `Aztech-Lab/EZ_Blender`

Repository: https://github.com/Aztech-Lab/EZ_Blender

Useful as an **orchestrated baseline**. Its Planner + specialized agent topology is intentionally different from this repository's Astra-solo default.

Benchmark against it where possible before claiming that solo operation is faster/better.

### `achimala/dream-loop`

Repository: https://github.com/achimala/dream-loop

Useful prior art for closed-loop visual target → create → critic → iterate behavior.

Borrow the evidence/iteration idea. Do not automatically adopt a separate live visual critic because this repository aims to keep live visual/spatial state inside the same Astra context.

### `Top3d-ai/world-builder`

Repository: https://github.com/Top3d-ai/world-builder

Useful environment/world-building prior art for reference-driven scene generation, repeatable multi-angle renders, and iterative refinement.

Use it especially when designing environment/layout fixtures, while isolating provider-specific assumptions.

## 6. Current integration target

The implementation should be compositional:

```text
Blender Agent Studio
  -> staged host workflow / bounded evidence / benchmark ideas

cc-blender-skill / create-3d-model-skill
  -> reference analysis / segmentation / overlays / landmarks / fit loops

NodeCue Blender Node Skills
  -> version-qualified GN graph knowledge

THIS REPOSITORY
  -> Astra solo/direct host policy
  -> research-only subagent boundary
  -> active multi-scale observation
  -> paired semantic close-up requirement
  -> boundary classification
  -> occlusion graph
  -> Blender Depth/Normal/exact-mask ambiguity breakers
  -> procedural-leverage-first GN routing
  -> integrated eval/promotion contract
```

## 7. What appears to remain unique

As of the architecture scan, no inspected public Skill was found that explicitly combines all of these in one contract:

- Astra as solo/direct interactive Blender driver;
- research-only subagents;
- mandatory paired reference/model detail inspection;
- semantic region decomposition before local repair;
- boundary taxonomy separating silhouette / occlusion / construction / material / shading;
- explicit occlusion graph;
- model-side Depth / Normal / exact semantic masks as ambiguity breakers;
- Geometry Nodes procedural-leverage-first authoring;
- tutorial/practitioner method mining → replay → transfer verification → Skill promotion.

That integration layer is the primary reason for this repository to exist.
