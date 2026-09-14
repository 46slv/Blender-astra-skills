# Procedural Authoring — Geometry Nodes Leverage Contract

## Purpose

Geometry Nodes is a persistent authoring layer for reuse, parameterization, assembly, placement, constraints, and environment layout.

The objective is **procedural leverage**, not Geometry-Nodes-at-all-costs.

```text
manual modeling where it is the best primitive
+
Geometry Nodes where rules / relationships / repetition / parameters add leverage
=
editable procedural authoring source
```

## 1. Procedural modes

### P1 — Manual source + procedural wrapper

Keep a high-quality manual source mesh/curve and use GN for:

- placement;
- repetition;
- variants;
- attachment;
- scale/spacing rules;
- environment assembly.

Do not rebuild good source geometry only to claim that the asset is “fully procedural.”

### P2 — Fully procedural generator

Generate the shape itself from primitives/curves/mesh operations/fields/instances when the asset is naturally described by a small set of design parameters.

Examples:

- floor lamp;
- shelving/rack/fence;
- simple architecture modules;
- vegetation/rock classes;
- repeatable product families.

### P3 — Modular part assembly

Treat source parts as a library with semantic interfaces.

```text
Part Library
  -> anchors / sockets / contact metadata
  -> select / instance / transform
  -> connect / orient / scale
  -> assembled asset
```

The truth is `parts + interfaces + relations`, not merely `Join Geometry`.

### P4 — Constraint / relation solver

Derive values that should not require manual XYZ tuning.

Examples:

- furniture Z from floor contact;
- wall-mounted object position/orientation from wall surface + normal;
- fastener count/spacing from panel width;
- lamp shade transform from pole/end anchor;
- dependent segment lengths from overall height;
- clearance/attachment transforms from geometry.

### P5 — Procedural environment / layout

Keep authorities separate:

```text
Room / terrain / support surfaces
Asset library
Placement rules
Art-directed overrides
Derived scene
```

Do not bake furniture/props into the room shell when scene assembly can remain procedural.

### P6 — Interactive Node Tool

If a repeated editing gesture is useful across assets, consider a Node Tool instead of repeatedly rebuilding a modifier graph manually.

## 2. Procedural leverage test

Before choosing GN, ask:

```text
Q1 Does this operation/relation recur?
Q2 Is there a meaningful parameter the user will change later?
Q3 Can an existing source part be reused?
Q4 Can a relation be derived from geometry/scene state?
Q5 Is variation valuable?
Q6 Is persistent procedural source useful downstream?
Q7 Is GN complexity/performance cost lower than the manual alternative?
```

If Q1–Q6 has a strong YES, GN is a candidate. If Q7 is strongly NO, do not force it.

## 3. Parameter philosophy

Expose design intent, not implementation noise.

Parameter classes:

```text
author_input
reference_fit
derived
constraint_solved
internal
```

Expose values such as:

- `overall_height`
- `base_radius`
- `shade_diameter`
- `shelf_count`
- `panel_width`
- `variant`

Prefer derived/solved values for:

- raw Z contact offsets;
- dependent endpoints;
- connector transforms;
- repeated spacing;
- part attachment transforms;
- counts implied by size/clearance.

Avoid double-authoring the same relationship with two user parameters.

## 4. Part Interface Contract

Reusable parts should expose semantic connection information where practical.

```yaml
part_interface:
  part_id: lamp.shade.A
  source_type: object|collection|generated
  local_axes:
    up: +Z
    forward: +Y
  bounds: available|derived
  anchors:
    - id: mount.bottom
      role: attach
    - id: visual.center
      role: reference
  contact:
    - id: support.bottom
      type: support_contact
  clearance:
    footprint: optional
  parameters:
    exposed: [...]
```

Implementation may use empties, points/curves, named attributes, helper geometry, or current Blender mechanisms. The semantic interface is the durable contract, not one object name.

## 5. Support / contact placement

### Floor-supported asset

```text
user/layout chooses X/Y + heading + asset
        ↓
support surface
        ↓
hit / nearest support position
        ↓
asset contact point / bounds bottom
        ↓
derive Z offset
        ↓
optional supported orientation policy
        ↓
placed instance
```

Rules:

- floor/wall/ceiling semantics should be explicit or strongly evidenced;
- no-hit / invalid-contact / excessive-slope cases must not silently become zero offsets;
- not every floor asset should align fully to terrain normal;
- fixed-view + numeric/structural evidence should confirm support relation.

### Wall-mounted asset

Use wall surface, outward normal, semantic mount anchor, and a declared clearance/offset.

### Ceiling-mounted asset

Use inverted support direction and semantic ceiling contact anchor.

## 6. Parametric floor-lamp reference pattern

```text
base profile       -> procedural revolve/generator
pole/arm           -> curve + profile
shade              -> manual source OR procedural profile
hinges/connectors  -> reusable parts
assembly           -> Geometry Nodes
floor contact      -> automatic
parameters         -> semantic interface
```

Possible author inputs:

- overall height;
- base radius;
- pole radius;
- arm length / curve strength;
- shade diameter / height;
- shade variant;
- joint variant;
- optional design lean/angle.

Derived/internal:

- base-bottom support contact;
- pole endpoints;
- shade mount transform;
- connector transforms;
- dependent segment lengths;
- optional cable/path length.

A good generator survives parameter changes, part swaps, source edits, and floor changes without manual repair of hidden offsets.

## 7. Environment layout layers

Recommended order:

1. coarse semantic zones;
2. candidate points / art-directed anchors;
3. asset selection;
4. support solve;
5. orientation;
6. clearance/exclusion filtering;
7. controlled variation;
8. final manual/art-directed override.

Do not default to random scattering when the scene has semantic structure.

Geometry Nodes is not a universal rigid-body packing solver. Use another solver or interactive adjustment when physical/layout complexity exceeds a practical GN contract.

## 8. Instances and realization

Default to preserving instance semantics for repeated geometry.

- Keep source assets separate and reusable.
- Keep stable IDs/seeds for variation.
- Perform operations on instances before realization when practical.
- Treat `Realize Instances` as a justified downstream boundary, not a generic fix.
- Test that source-part edits propagate to the derived assembly.

Authoring and derived output are different:

```text
AUTHORING MASTER
  source parts
  + node groups
  + semantic parameters
  + support/placement inputs
  + overrides
        ↓
DERIVED OUTPUT
  realized mesh if required
  optimized/joined/triangulated runtime asset
  cache/bake/export package
```

Do not push runtime optimization backward into the authoring source.

## 9. GN-specific verification

A procedural method should not become execution-ready until applicable checks pass:

- parameter perturbation across representative min/default/max and combinations;
- part swap;
- source-part propagation;
- support/contact transfer when floor/wall changes;
- stable variation / ID behavior;
- manual override persistence;
- realization/export boundary;
- representative performance envelope;
- invalid/no-hit/empty-source behavior.

Default-value beauty is not sufficient evidence.

## 10. Performance rules

- keep instance operations before realization;
- scope expensive proximity/raycast/boolean queries;
- avoid unnecessary recomputation of equivalent fields;
- do not run expensive solvers across every point without need;
- separate viewport/final quality lanes when helpful;
- measure evaluation cost rather than judging by node count.

## 11. GN method mining

When learning from tutorials/production files, extract:

- procedural authoring mode;
- source-part contract;
- public parameter contract;
- derived-parameter graph;
- constraint solvers;
- anchor/contact/interface semantics;
- instance/realization boundary;
- field/domain/attribute assumptions;
- manual override policy;
- invalid-input behavior;
- performance hotspots;
- consumer/export policy;
- reason for subgroup/interface boundaries.

Learn the data flow and design decision, not the screenshot layout of the node tree.

Old tutorials remain useful if their semantic method is remapped to the target Blender version instead of copying stale node/socket spelling.

## 12. Anti-patterns

- full GN reconstruction only because GN is preferred;
- exposing dozens of raw transform controls that can be derived;
- giant one-off node trees that are harder to edit than the mesh;
- early realize/join destroying source reuse;
- unstable random variation after every graph edit;
- graph interfaces filled with implementation details;
- unbounded raycast/proximity over all points;
- silent success for no-hit / empty collection / invalid range;
- destructive apply in the authoring master solely for export convenience.
