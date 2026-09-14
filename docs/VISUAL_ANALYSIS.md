# Visual Analysis — Perception Before Judgement

## Purpose

Astra should not decide fine reference fidelity from one broad RGB screenshot.

Before local repair, build enough visual structure to distinguish:

- silhouette;
- semantic regions;
- boundary type;
- overlap/occlusion;
- attachment/contact;
- stable landmarks;
- model-side geometric truth.

The goal is not to replace Astra vision with classical CV. The goal is to **make the relevant evidence explicit before asking Astra to judge or repair**.

## 1. Multi-scale observation

### O0 — Context overview

Use for:

- full asset/scene context;
- gross silhouette/proportion;
- major placement;
- navigation.

O0 alone cannot establish fine-detail or final PASS.

### O1 — Target-framed view

Frame the target part/asset so it occupies useful screen area. Use task-specific front/side/back/3/4 or other fixed views.

Check:

- silhouette;
- part relationships;
- major seams/attachments;
- side effects from local repair.

### O2 — Paired semantic close-up

For changed/high-risk/reference-critical regions, enlarge **both**:

```text
REFERENCE CROP        MODEL CROP
same semantic region  same semantic region
same intended view    matched view/camera
similar framing       similar screen occupancy
same orientation      same orientation
```

Do not accept detail if only one side is enlarged or the feature remains only a few pixels wide.

### O3 — Diagnostic / structural view

When the cause remains ambiguous, add only the evidence needed to disambiguate:

Reference side:

- grayscale/high-contrast;
- edge map;
- silhouette;
- semantic region mask;
- boundary classification;
- landmark/junction map;
- occlusion/overlap hypothesis.

Model side:

- exact object/part mask;
- alpha/silhouette;
- Depth;
- Normal;
- material/object index or Cryptomatte where appropriate;
- Workbench outline/cavity;
- wireframe/topology;
- face orientation / x-ray;
- GN debug/intermediate geometry;
- exact scene landmarks/anchors.

### O4 — Final inspection sweep

Revisit:

- changed regions;
- previous defects;
- identity-critical regions;
- attachment/contact regions;
- consumer-risk regions.

## 2. Visual Structure Packet

Build this only to the depth needed by the task.

```yaml
comparison_packet:
  semantic_region: face.eye_left
  reference:
    raw_crop: ...
    silhouette: ...
    edge_map: ...
    semantic_mask: ...
    landmarks: ...
    boundary_hypotheses: ...
  model:
    raw_crop: ...
    exact_region_mask: ...
    silhouette: ...
    depth: ...
    normal: ...
    wireframe: ...
  correspondence:
    matched_view: ...
    aligned_overlay: ...
    landmark_delta: ...
    silhouette_delta: ...
  result: PASS|FAIL|UNKNOWN
  unresolved: [...]
```

Astra should interpret this packet, not blindly obey one metric.

## 3. Semantic region decomposition

Before saying “the eye is wrong,” decide what the eye region is.

Example:

```yaml
region_tree:
  character:
    head:
      face:
        eye_left:
          upper_lid: {}
          lower_lid: {}
          iris: {}
        eye_right: {}
        nose: {}
        mouth: {}
      hair:
        bangs: {}
        side_lock_left: {}
        side_lock_right: {}
        back_mass: {}
```

Rules:

- only visible evidence may be marked confirmed;
- hidden/occluded shape remains `inferred`;
- keep region-boundary confidence;
- preserve crop/resize coordinate transforms back to the original reference;
- model-side semantic masks should use exact Blender scene data when available instead of re-inferring part identity from RGB.

## 4. Boundary taxonomy

Low-level edges are not automatically modeling edges.

Classify boundaries where relevant:

```text
SILHOUETTE_BOUNDARY
OCCLUSION_BOUNDARY
CONSTRUCTION_BOUNDARY
MATERIAL_BOUNDARY
SHADING_BOUNDARY
TEXTURE_DETAIL
UNKNOWN_BOUNDARY
```

Geometry repair should normally be driven by silhouette, occlusion, or construction boundaries.

Do not model a shadow, highlight, texture line, or material break as geometry simply because Canny/Sobel produced an edge.

## 5. Occlusion / overlap graph

Represent front/back and contact semantics explicitly when they matter.

```yaml
occlusion_graph:
  - front: hair.bangs
    back: face.forehead
    relation: occludes
    confidence: high
  - front: sleeve
    back: upper_arm
    relation: covers
    confidence: high
  - front: lamp.shade
    back: bulb_socket
    relation: partial_occlusion
    confidence: medium
```

Useful relations:

- `occludes`
- `covers`
- `partial_occlusion`
- `touches`
- `attached_to`
- `separated_from`
- `passes_behind`
- `passes_in_front`
- `inside`
- `unknown`

T-junctions and edge termination are evidence, not certainty. Stylized linework/shadow can create false cues.

If multiple reference views exist, reconcile the same semantic region across views. Conflicts remain conflicts; do not average them away.

## 6. Landmark / junction map

Stable landmarks can localize repair better than whole-image similarity.

Character examples:

- eye corners;
- iris/pupil center;
- nose tip / nostril endpoints;
- mouth corners;
- chin bottom;
- ear attachment;
- hairline intersections;
- shoulder seam / cuff endpoints.

Prop examples:

- hinge center;
- mount axis;
- rim extrema;
- cable exit;
- contact point.

Environment examples:

- floor contact corners;
- wall mount center;
- doorway corners;
- trim intersections.

If many landmarks move together, inspect camera/framing before deforming local geometry.

## 7. Deterministic CV helpers

Potential helpers:

- Canny / Sobel edge extraction;
- silhouette extraction;
- contour hierarchy;
- morphology for mask cleanup;
- aligned overlay;
- region-mask IoU/centroid/bbox;
- landmark displacement;
- edge-distance maps.

Rules:

- thresholds are image/dataset dependent; do not hard-code universal gates without fixture evidence;
- compare like with like: edge↔edge, silhouette↔silhouette, mask↔mask;
- processed images are evidence, not replacements for source truth;
- preserve coordinate transforms after crop/resize/rotation/perspective normalization;
- SSIM/IoU/edge metrics cannot establish semantic correctness alone.

## 8. Model-side ground truth

Use Blender internal truth instead of re-inference whenever possible.

Preferred sources:

```text
scene semantic part
→ exact object / collection / material / named-attribute identity
→ render-space mask / landmark / depth / normal
→ paired comparison against reference inference
```

This is especially important when RGB ambiguity could confuse:

- shadow vs dent;
- material boundary vs part boundary;
- overlap vs gap;
- contact vs near-contact;
- surface-angle difference vs lighting difference.

## 9. Repair scope from segmentation

Convert semantic understanding into a bounded write set.

```yaml
repair_scope:
  semantic_region: hair.bangs.left
  model_region: exact_scene_ref
  neighboring_protected:
    - eye_left
    - forehead
    - side_lock_left
  allowed_changes:
    - local_curve_shape
    - local_root_position
  forbidden_changes:
    - global_head_scale
    - eye_geometry
```

A local defect must not justify broad asset mutation without new evidence.

## 10. Repair loop

```text
O0/O1 raw pair
→ choose defect region
→ O2 paired close-up
→ if ambiguous: build Visual Structure Packet + O3
→ classify likely cause:
     geometry / material / lighting / camera / unknown
→ RepairTicket
→ smallest coherent mutation
→ regenerate the SAME region packet
→ compare before/after under matched conditions
→ O1 broader regression
→ O4 final sweep
```

Do not change comparison camera/crop and then claim the result improved unless the camera change itself was the intended repair.

## 11. Visual receipt

```yaml
visual_receipt:
  purpose: overview|target|detail|diagnostic|final
  target_semantics: [...]
  view: front|side|back|three_quarter|free|diagnostic
  scale_class: context|target_framed|region_close
  comparison_reference: ...
  paired_model_view: ...
  changed_regions_visible: [...]
  risk_regions_visible: [...]
  structural_evidence:
    - raw
    - silhouette
    - edge
    - region_mask
    - occlusion
    - landmark
    - depth
    - normal
    - object_mask
    - wireframe
  result: PASS|FAIL|UNKNOWN
  unknown_because: ...
```

Verifier guards:

- fine detail / identity / attachment / topology-surface checks cannot PASS without region-close evidence;
- final PASS cannot come from O0 only;
- `UNKNOWN` does not auto-promote to PASS;
- detail comparison cannot PASS when reference/model are not meaningfully paired.

## 12. Failure classes to test

- `BROAD_SCREENSHOT_FALSE_PASS`
- `REFERENCE_DETAIL_NOT_ZOOMED`
- `MODEL_DETAIL_NOT_ZOOMED`
- `UNPAIRED_SCALE_COMPARISON`
- `SHADING_EDGE_MISTAKEN_FOR_GEOMETRY`
- `OCCLUSION_RELATION_MISREAD`
- `SEMANTIC_REGION_BOUNDARY_UNCLEAR`
- `MODEL_STRUCTURE_REINFERRED_FROM_RGB`
- `CAMERA_MISMATCH_FALSE_DIFF`
- `REPAIR_SCOPE_TOO_BROAD`
- `UNKNOWN_PROMOTED_TO_PASS`
