# Visual analysis — tools for seeing better

This document is a collection of promising ways to improve Astra's perception during Blender work.

It is not a required pipeline. Astra should use, combine, replace, or ignore these ideas according to the actual visual problem.

## Core idea

Fine 3D work can fail when the model acts on an image before it has actually understood the relevant local structure.

A useful strategy is to improve the observation before improving the object.

Possible sequence:

```text
notice uncertainty
  ↓
look closer / change view
  ↓
make hidden structure more explicit if useful
  ↓
compare reference and model at comparable detail
  ↓
form a better hypothesis
  ↓
edit
  ↓
look again
```

The important part is not the sequence itself. The important part is refusing to treat low-information perception as high-confidence understanding.

## 1. Paired detail inspection

When reference fidelity matters, it is often better to inspect the same semantic region on both sides:

```text
REFERENCE                  MODEL
same feature               same feature
useful enlargement         useful enlargement
similar orientation        matched orientation when possible
similar framing            similar screen occupancy
```

This is especially useful for eyes, mouth, hairline, seams, hinges, mounts, contact points, joints and other small high-information regions.

A broad reference next to a close model, or vice versa, can hide meaningful differences.

## 2. Structural views that may help Astra

Raw RGB is only one observation.

Useful derived views may include:

- silhouette;
- grayscale / contrast-enhanced view;
- Canny/Sobel or other edge extraction;
- semantic part masks;
- landmarks / junctions;
- aligned overlay;
- region difference;
- wireframe / topology;
- face orientation;
- Blender object/material identity;
- Depth;
- Normal;
- Cryptomatte/object masks;
- Geometry Nodes intermediate/debug geometry.

Use only what answers the current uncertainty.

## 3. Semantic decomposition

Before repairing a local feature, it can help to understand what region is actually being discussed.

Examples:

```text
head
  face
    left eye
    right eye
    nose
    mouth
  hair
    bangs
    side locks
    back mass
```

or

```text
lamp
  base
  pole
  arm
  joint
  shade
  cable
```

The decomposition does not need to become a formal schema. It is useful when it improves reasoning, correspondence, or edit locality.

Hidden/occluded geometry should remain an inference rather than silently becoming source truth.

## 4. Boundaries are not all the same

An extracted line may represent very different things:

- outer silhouette;
- one object occluding another;
- a real construction seam or hard shape break;
- a material/color boundary;
- shadow or highlight;
- texture/printed detail;
- an artifact or uncertain cue.

This distinction matters because only some boundaries should drive geometry edits.

Classical edge detection is useful evidence, not semantic truth.

## 5. Overlap and occlusion

Many important 3D relationships are easier to reason about as front/back or contact relations than as isolated 2D contours.

Examples:

- bangs pass in front of forehead;
- sleeve covers upper arm;
- lamp shade partially hides socket;
- chair leg touches floor;
- wall fixture attaches to wall but remains separated by a mount depth.

T-junctions and terminating contours can suggest these relationships, but stylized linework and shadows can create false cues.

When multiple reference views exist, use them to resolve uncertainty rather than averaging contradictions away.

## 6. Landmarks and correspondence

For some tasks, a few stable points are more useful than whole-image similarity.

Examples:

- eye corners;
- iris center;
- mouth corners;
- chin bottom;
- hairline intersections;
- hinge center;
- mount axis;
- shade rim extrema;
- floor-contact corners.

If many landmarks move together, camera/framing may be the problem rather than local geometry.

## 7. Blender-side truth

The model side often has information the reference side does not.

If Blender already knows the object, part, depth, surface normal, topology, transform or node relationship exactly, prefer that state over asking Astra to infer the same fact from an RGB screenshot.

This can help distinguish:

- dent vs shadow;
- overlap vs material boundary;
- surface-angle error vs lighting difference;
- gap vs near-contact;
- wrong part vs wrong appearance.

## 8. Classical CV and metrics

OpenCV-style helpers can be useful for deterministic evidence preparation:

- edges;
- contours;
- connected components;
- masks;
- bounding boxes;
- centroids;
- morphology;
- geometric transforms;
- overlay/difference images;
- SSIM/IoU or related metrics in appropriate cases.

Do not let a convenient metric become the objective unless the actual task justifies it.

A high silhouette IoU can coexist with a bad 3D model. A low pixel similarity can be caused by camera, lighting, texture or projection rather than geometry.

## 9. Repair locality

Better perception should make edits more local, not merely produce more analysis artifacts.

If Astra identifies a problem in one bang, hinge, seam or contact region, preserve surrounding accepted work unless evidence points to a broader cause.

After a repair, compare the relevant local region again and also look at enough surrounding context to notice side effects.

## 10. Open research questions

Astra should investigate alternatives rather than assuming the techniques above are best.

Interesting directions include:

- learned segmentation and semantic correspondence;
- vision-language segmentation;
- feature matching across stylized references and renders;
- depth/normal estimation from reference images;
- differentiable or optimization-based camera/shape fitting;
- active view selection;
- perceptual embeddings for local shape comparison;
- 3D-aware vision models;
- techniques from robotics/visual servoing for deciding what to observe next.

These are research prompts, not implementation requirements.
