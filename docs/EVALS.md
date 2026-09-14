# Evaluation and Promotion Gates

## Purpose

This repository is not complete when the Skill files exist. The architecture becomes trustworthy only when a fresh Astra can execute representative Blender tasks and produce independently inspectable evidence.

The default comparison is:

```text
A = Astra solo/direct host operation
B = orchestrated baseline with host-operation worker(s)
```

A is the default topology. B is a benchmark, not the default implementation target.

## 1. Global metrics

Measure at least:

- verified completion rate;
- verified completion time;
- host tool-call count;
- handoff count;
- coordination latency;
- human intervention count;
- false visual PASS rate;
- detail-defect escape rate;
- `UNKNOWN -> PASS` error rate;
- protected-set regressions;
- repair iterations per accepted defect;
- final editability;
- fresh reopen / round-trip success;
- unnecessary destructive/realize operations;
- reference/model paired-closeup coverage.

Astra-solo should not be called superior until representative fixtures show equal-or-better quality with materially lower handoff/coordination cost or another clear benefit.

## 2. Modeling fixtures

### F01 — Radial + sweep prop

Asset: floor lamp or similar prop.

Measures:

- semantic decomposition;
- profile/revolve vs curve/sweep routing;
- large-form gate;
- local repair;
- part interfaces;
- editability.

### F02 — Boolean hard-surface

Asset: panel/housing with repeated cutouts.

Measures:

- non-destructive boolean preservation;
- modifier order;
- manifold/visual checks;
- no premature apply;
- local defect repair.

### F03 — Procedural repetition

Asset: fence/rack/tile layout.

Measures:

- instance/GN routing;
- parameter editability;
- stable variation;
- no unnecessary realization;
- source-part propagation.

### F04 — Organic primary form → retopo

Asset: stylized head/simple creature region.

Measures:

- design/large-form lock;
- sculpt/retopo routing;
- surface fit;
- local topology repair;
- visual + structural evidence.

### F05 — Deformation-aware facial region

Asset: mouth/eye patch.

Measures:

- landmark/articulation planning;
- loop/patch/pole strategy;
- localized repair;
- deformation smoke;
- protected neighboring regions.

### F06 — Consumer round-trip

Asset: small GLB/FBX/USD deliverable depending target.

Measures:

- source preservation;
- export/import structural diff;
- axis/scale/dependency/material behavior;
- fresh import;
- no false completion from file existence alone.

## 3. Geometry Nodes fixtures

### GN-F01 — Parametric floor lamp

Measures:

- hybrid vs fully procedural route selection;
- semantic parameter design;
- automatic floor contact;
- part swap;
- source preservation;
- parameter perturbation.

Expected behaviors include:

- change overall height without manual connector repair;
- change shade variant without breaking mount;
- change floor elevation and preserve contact;
- edit source part and see expected propagation.

### GN-F02 — Room furniture grounding

Inputs:

- uneven/offset floor variants;
- several furniture assets.

Measures:

- X/Y/heading authority;
- derived support Z;
- slope policy;
- no-hit handling;
- floor/wall/ceiling distinction.

### GN-F03 — Modular shelving/rack

Measures:

- count/spacing/width dependency;
- repeated component instances;
- end caps/connectors;
- invalid range behavior;
- no double-authored parameters.

### GN-F04 — Manual asset → procedural wrapper

Input: manually modeled chair/lamp/prop.

Measures:

- useful degrees of freedom extracted;
- no needless rebuild of source mesh;
- variant reuse;
- assembly reuse;
- source edit propagation.

### GN-F05 — Environment kit assembly

Measures:

- Object/Collection sources;
- semantic zones/anchors;
- support solving;
- exclusion/clearance filtering;
- stable variation;
- art-directed overrides.

### GN-F06 — Derived export

Measures:

- authoring graph preserved;
- realization/apply only in derived output;
- exported consumer asset valid after reimport;
- runtime optimization does not destroy authoring source.

## 4. Visual-structure fixtures

### VA-F01 — Face close-up

Use a reference/model eye-mouth-hairline task.

Measures:

- paired zoom;
- semantic region decomposition;
- landmarks;
- identity defect escape;
- local repair leakage.

### VA-F02 — Layered hair / garment overlap

Measures:

- front/back relation;
- occlusion-boundary classification;
- T-junction interpretation;
- local repair scope;
- neighboring protected region stability.

### VA-F03 — Floor-lamp joint

Measures:

- silhouette;
- hinge/mount boundary;
- contact;
- paired close-up;
- model Depth/Normal/mask evidence;
- geometry-vs-shading diagnosis.

### VA-F04 — Furniture floor/wall contact

Measures:

- region/contact mask;
- support relation;
- depth;
- gap vs near-contact;
- floor/wall semantics.

### VA-F05 — False shading edge

Use a reference containing strong shadow/highlight that resembles a structural line.

Measures:

- `SHADING_BOUNDARY` vs geometry misclassification;
- unnecessary geometry repair rate;
- `UNKNOWN` handling.

### VA-F06 — Camera mismatch

Intentionally offset reference/model projection or framing.

Measures:

- whether raw pixel difference is wrongly treated as geometry defect;
- landmark-coherent camera diagnosis;
- fixed-camera comparison discipline.

## 5. Visual metrics

Track:

```text
paired_closeup_coverage
false_visual_pass_rate
boundary_classification_error
occlusion_relation_error
landmark_localization_error
repair_scope_leakage
unknown_to_pass_error
shading_vs_geometry_misclassification
camera_mismatch_false_repair
human_correction_count
```

No one metric is a universal acceptance oracle.

## 6. Evidence packet requirements

For each fixture, keep enough evidence to independently understand the result:

- exact Blender version;
- source/reference identity;
- working-copy/source-preservation status;
- Modeling Plan or equivalent method record;
- structural scene/node/modifier report;
- fixed/matched views;
- paired region evidence for detail-critical checks;
- RepairTicket(s) and before/after packet identity;
- consumer/export/reopen result if applicable;
- known deviations / unresolved `UNKNOWN`;
- final status.

Suggested final states:

```text
VERIFIED_USABLE
BOUNDED_GAP
BLOCKED
```

## 7. Promotion gates

### Candidate

Skill structure exists and static/schema/script tests pass.

### Replay-qualified

Fresh Astra can reproduce a representative same-class task using repo docs/Skill without conversation history.

### Transfer-qualified

At least one different asset/shape passes using the same method family.

### Host-qualified

Representative Blender host fixtures pass with structural + visual evidence and source preservation.

### Active default

Only after host-qualified behavior shows acceptable quality/latency and failure rates across the intended task mix.

## 8. A/B baseline policy

Compare Astra-solo against at least one orchestrated baseline for representative interactive tasks.

Do not optimize the comparison to make either side win. Keep:

- same task/reference;
- same Blender/runtime constraints where possible;
- same acceptance criteria;
- same evidence requirements;
- same source-protection rules.

Record where orchestration does help. If a narrow scope clearly benefits from delegated host work, that may become an explicit exception without changing the default topology.
