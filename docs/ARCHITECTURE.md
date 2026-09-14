# Architecture — `blender-astra-modeling`

## 1. System thesis

The Skill is not a Blender command encyclopedia. It is a **decision + perception + repair procedure** for Astra.

Interactive Blender work should normally stay in one Astra context:

```text
Goal / references / consumer
        ↓
classify geometry truth + uncertainty
        ↓
retrieve only relevant methods
        ↓
Construction Graph + Modeling Plan
        ↓
Astra direct host loop
  OBSERVE → REASON → ACT → RE-OBSERVE → REPAIR → VERIFY
        ↓
consumer / reopen / round-trip acceptance
        ↓
receipt + reusable learning
```

The key optimization is continuity: the same model that saw the defect should usually remain responsible for the edit and the follow-up inspection.

## 2. Responsibility boundaries

### Astra

Owns:

- live Blender observation;
- reference interpretation;
- method selection;
- GUI / Computer Use / bounded bpy / Geometry Nodes lane selection;
- interactive mutation;
- semantic interpretation of visual evidence;
- local repair;
- final visual acceptance.

### Research subagent

May be used for:

- current Blender Manual / Python API / node lookup;
- version differences;
- tutorial / production-method mining;
- external consumer/export requirements;
- prior-art inspection;
- long-source summarization.

Does not own by default:

- interactive Blender GUI;
- main `.blend` writes;
- Blender write APIs/MCP;
- Computer Use;
- repair of accepted geometry;
- final PASS.

Return a compact `ResearchPacket` only:

```yaml
question: ...
findings: [...]
sources: [...]
version_scope: ...
confidence: high|medium|low
options: [...]
unresolved: [...]
```

### Deterministic scripts / adapters

Own mechanical tasks with stable inputs/outputs:

- scene reports;
- screenshot/render capture;
- crop/resize/alignment bookkeeping;
- edge/silhouette extraction;
- Blender diagnostic passes;
- schema validation;
- evidence-packet completeness;
- export/reimport smoke checks.

They do not decide what the asset should look like.

## 3. Skill package target

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

This is a modular target. Upstream components may replace local files when they are better, compatible, and license-safe.

## 4. Skill progressive disclosure

`SKILL.md` should stay small and own only:

- trigger / meaningful non-trigger;
- preflight;
- Astra-solo host rule;
- method retrieval rule;
- active-observation loop;
- execution-lane routing;
- repair loop;
- verification / stop conditions;
- routing to focused references.

Do not preload all Blender knowledge. Load 1–3 relevant MethodCards/references for the current problem.

## 5. State preflight

Before non-trivial mutation, acquire a bounded scene snapshot:

```yaml
scene_snapshot:
  blender_version: exact
  blend_path: current
  source_authority: original|working_copy|derived
  save_state: saved|dirty|unknown
  mode: ...
  active_object: stable_ref|null
  selected_objects: [...]
  target_refs: [...]
  target_types: [...]
  coordinate_space: ...
  units: ...
  bounds: ...
  hierarchy: ...
  modifiers: ...
  dependencies: ...
  fixed_views: [...]
  protected_set: [...]
```

Object name alone is not sufficient stable identity when a stronger current-host reference is available.

Non-trivial editing should use a task-scoped working copy/checkpoint rather than overwriting the source asset by default.

## 6. Method representation

A reusable modeling method is execution-ready only when it contains at least:

- when / problem signature;
- why / optimization target;
- preconditions;
- invariants;
- write set;
- protected set;
- semantic actions;
- observables;
- decision rules;
- postcondition / oracle;
- failure signals;
- rollback / local-repair boundary;
- provenance / confidence / version scope.

Method authority order:

1. current user / project / consumer contract;
2. current `.blend`, repo, runtime evidence;
3. target Blender official docs/runtime behavior;
4. transfer-verified local MethodCard;
5. practitioner/tutorial evidence;
6. mined inference.

## 7. Construction routing

Choose the construction family per semantic part/region rather than forcing one global style.

Candidate families:

- primitive composition;
- profile + extrude;
- profile + revolve;
- curve + sweep;
- shell + thickness;
- non-destructive boolean;
- mirror / array / instances;
- surface conform;
- manual retopology;
- sculpt → retopo;
- Geometry Nodes assembly/generation;
- parametric CAD when exact solid constraints dominate.

Hard reject a method before ranking if it:

- loses a required consumer capability;
- fails its preconditions;
- violates a protected invariant;
- conflicts with reference authority;
- cannot be verified in the current runtime.

Then prefer:

1. consumer fit;
2. editability / downstream compatibility;
3. reversibility;
4. observability / verifier strength;
5. local repairability;
6. deterministic execution potential;
7. evidence strength;
8. lower unnecessary complexity;
9. procedural leverage when it reduces repeated manual work without degrading the contract.

## 8. Stage gates

### G0 — Intake / authority

- exact target Blender/version/file/consumer known;
- reference authority and inferred areas separated;
- working-copy/source protection established;
- baseline snapshot captured.

### G1 — Structure

- semantic parts / hierarchy / interfaces / scale policy defined;
- Construction Graph exists;
- uncertainty/hidden regions recorded.

### G2 — Blockout / large form

- primary silhouette, proportion, and major placement accepted from matching views;
- do not proceed to detail while large-form mismatch remains.

### G3 — Medium form / construction logic

- major seams, cuts, curves, interfaces, supports established;
- chosen modifier/GN/retopo strategy still preserves editability and local repair.

### G4 — Topology / procedural / material structure

Use asset-specific oracles: deformation topology, manifold/supports, modifier order, GN interface, UV/material boundaries, dependencies.

### G5 — Detail / deformation / look

- small detail does not break larger forms;
- animation assets get required deformation smoke;
- geometry problems are separated from material/lighting problems.

### G6 — Consumer / round-trip

- target import/export/runtime/render contract passes;
- fresh reopen/reimport when required;
- Completion Receipt can explain usability.

## 9. Direct execution lanes

Astra chooses the shortest correct lane for each coherent mutation.

### GUI / Computer Use

Best for:

- sculpt;
- visual retopology;
- spatial placement;
- node visual debugging;
- local shape repair driven by immediate viewport feedback.

### Bounded bpy / adapter

Best for:

- deterministic object/data creation;
- properties;
- modifiers/node groups;
- hierarchy/collections;
- exact reports;
- repeatable validation.

Guard UI/context-dependent `bpy.ops`; do not blind-retry poll/context failures.

### Geometry Nodes / modifiers

Best for:

- parameterized generators;
- manual-source wrappers;
- modular part assembly;
- repeated layouts;
- derived contact/alignment/spacing;
- persistent procedural authoring.

Do not apply/realize merely because downstream work is inconvenient. Keep authoring source and derive export geometry separately when needed.

## 10. Closed-loop repair

```text
OBSERVE
  current target + matched reference context
      ↓
SELECT METHOD / HYPOTHESIS
      ↓
ACT
  smallest coherent write-set
      ↓
VERIFY STRUCTURE
      ↓
VERIFY VISUAL
      ↓
PASS → checkpoint / next stage
FAIL → RepairTicket
      ↓
LOCAL REPAIR / STRATEGY SWITCH / ROLLBACK
```

One RepairTicket should represent one defect class.

Accepted regions become protected. Repair the defect region, then re-check both the local packet and the broader target view.

Do not repeat the same repair against the same evidence state. New attempt requires new evidence or a changed hypothesis.

## 11. Structural + visual dual oracle

Vision-only cannot prove:

- topology/manifold;
- hierarchy/instances;
- UV/material assignments;
- rig/weights/shape keys;
- external dependencies;
- transform/scale;
- procedural editability.

Structure-only cannot prove:

- silhouette;
- proportion;
- surface artifacts;
- design identity;
- reference fidelity.

Default evidence pair:

```text
machine-readable scene/target report
+
matched fixed-view / paired visual evidence
```

## 12. Visual architecture

The visual system is active perception, not passive screenshot review.

```text
O0 context overview
→ O1 target-framed view
→ O2 paired semantic close-up
→ O3 diagnostic / structural view when needed
→ O4 final inspection sweep
```

For detail work, pair reference and model at the same semantic region and comparable view/framing/scale. When raw vision is ambiguous, construct a Visual Structure Packet. See `docs/VISUAL_ANALYSIS.md`.

## 13. Geometry Nodes architecture

Geometry Nodes is a leverage layer, not a mandatory modeling style.

Supported procedural modes:

1. manual source + procedural wrapper;
2. fully procedural generator;
3. modular part assembly;
4. constraint/relation solver;
5. procedural environment/layout;
6. interactive Node Tool when a repeatable edit gesture merits one.

Prefer semantic user inputs and derive dependent transforms. See `docs/PROCEDURAL_AUTHORING.md`.

## 14. Safety / authority

Default safety boundaries:

- do not overwrite source `.blend`;
- do not expose arbitrary host authority to every child agent;
- do not grant modeling methods implicit filesystem/network/credential authority;
- do not broad-remesh/decimate/apply/triangulate/delete/recalculate/bake without a method, checkpoint, and postcondition;
- external paid/generative providers require separate authority;
- current Blender adapter/MCP transport is not itself a sandbox.

## 15. Prior-art policy

Before implementing a helper or workflow, inspect `docs/PRIOR_ART.md` and current upstream code.

Reuse/adapt first when appropriate. Preserve provenance and license obligations. Do not copy code based only on remembered behavior or a stale summary.

## 16. Qualification boundary

The architecture becomes a qualified active Skill only after representative fixtures prove that a fresh Astra can:

- keep live host control;
- retrieve relevant methods without loading the whole corpus;
- actively zoom/focus into uncertain regions;
- compare reference/model at matched detail scale;
- use structured evidence rather than hallucinated certainty;
- perform local repair without protected-region regressions;
- select GUI/bpy/GN lanes appropriately;
- preserve editability;
- pass consumer/reopen checks;
- achieve acceptable quality/latency against the orchestrated baseline.

Until then, report `HOST_VALIDATION_PENDING`.
