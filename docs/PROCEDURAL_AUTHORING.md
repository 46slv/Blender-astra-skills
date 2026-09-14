# Procedural authoring — leverage, not doctrine

This document records promising ways to use Geometry Nodes and related procedural methods.

It is not a requirement that Astra use Geometry Nodes, nor a fixed contract for how procedural assets must be built.

The question is simpler:

> Where can relationships, reuse, parameters, or automatic structure remove repeated manual work without reducing quality or editability?

## 1. Useful procedural directions

### Manual source + procedural wrapper

Keep a strong manually modeled source asset and use procedural logic for things around it:

- placement;
- repetition;
- variants;
- attachments;
- layout;
- dependent transforms.

This is often better than rebuilding a good mesh as a fully procedural generator.

### Fully procedural generator

When a shape is naturally described by a compact set of design variables, generating the object can be powerful.

Examples:

- lamps;
- shelving/racks;
- fences;
- simple architecture systems;
- repeated product families;
- vegetation/rock classes.

### Modular assembly

Treat reusable parts as parts, not as geometry that must be manually reassembled every time.

Potential concepts:

```text
part library
+ anchors / sockets / contacts
+ rules / parameters
→ assembled object
```

The implementation might use Geometry Nodes, empties, named attributes, curves, collections, custom properties, Python, or something Astra discovers to be better.

### Derived relationships

Some values should perhaps not be user parameters at all.

Examples:

- furniture height derived from floor contact;
- wall object orientation derived from wall normal;
- connector transforms derived from part anchors;
- repeated spacing derived from width/count;
- lamp shade position derived from pole/end point;
- dependent segment lengths derived from overall height.

A meaningful design input is usually more valuable than a raw XYZ offset whose correct value can be inferred.

### Procedural environments

Environment authoring may benefit from separating:

- room/terrain/support geometry;
- asset library;
- semantic zones or anchors;
- placement rules;
- constraints/clearance;
- art-directed exceptions.

Random scatter is only one tiny subset of procedural layout.

## 2. Geometry Nodes may be one implementation, not the architecture

Geometry Nodes is attractive because it is native, inspectable, non-destructive, instance-aware, and interactive.

But Astra should compare it against alternatives when appropriate:

- ordinary Blender modifiers;
- constraints;
- collections/linked data;
- Python-generated or maintained structures;
- drivers;
- custom operators/tools;
- CAD-style parameterization;
- simulations/solvers;
- combinations of the above.

Do not force a relationship into GN merely because this repository is interested in GN.

## 3. Parameter design

A strong procedural asset exposes the choices a person actually means to make.

Good examples:

- overall height;
- base radius;
- shade diameter;
- shelf count;
- spacing intent;
- variant selection.

Potentially weak examples:

- arbitrary Z offset that should follow floor height;
- connector translation that should follow an anchor;
- repeated spacing duplicated in several places;
- implementation-specific node values exposed only because they exist.

Astra should decide what should be authored, what should be derived, and what should remain internal.

## 4. Contact and attachment

One especially promising direction is to treat physical relationships semantically.

Possible relationships:

- supported_by;
- attached_to;
- aligned_to;
- inside;
- clears;
- follows;
- distributed_along.

For example, furniture placement could use floor geometry to derive vertical contact instead of requiring a raw Z parameter.

A lamp shade could attach to a semantic mount point rather than depending on hand-tuned coordinates.

The exact representation is open.

## 5. Instances and source preservation

Instances are valuable when they preserve reusable source authority and cheap variation.

Avoid realizing or joining instances simply because that makes a later step easier, unless the later consumer really needs realized geometry.

A useful distinction is:

```text
authoring source
→ derived/export result
```

The source can stay editable/procedural even when an exported artifact must be flattened, triangulated, joined, or otherwise transformed.

## 6. Floor lamp as a research object

A floor lamp remains a useful example because it combines several authoring ideas:

```text
base       rotational / profile-defined
pole/arm   curve or repeated structural element
shade      manual or procedural source
joints     reusable parts
assembly   relationships between parts
floor      support/contact relation
```

A good implementation might allow changes to height, proportions, shade variant, joint type, or floor level without hidden manual repair.

How to achieve that is intentionally open.

## 7. What to learn from production work

When studying procedural artists or tutorials, look beyond node names.

Useful questions include:

- What repeated problem motivated the graph?
- Which decisions remain artist-controlled?
- Which values became derived?
- What source parts stayed manual?
- Where are anchors/interfaces encoded?
- How are invalid or missing inputs handled?
- What must remain editable later?
- Where does performance become limiting?
- What is realized only for delivery?
- What would the artist automate differently next time?

Old tutorials can still contain strong methods even when node names changed.

## 8. Research directions

Astra should investigate more than existing GN tutorials.

Potentially relevant fields:

- constraint solving;
- procedural CAD;
- assembly graphs;
- parametric product design;
- scene grammars;
- robotics contact/pose reasoning;
- layout optimization;
- spatial databases;
- game-editor prefab systems;
- Houdini procedural workflows;
- node-based modeling systems outside Blender.

The goal is not to imitate these systems. It is to discover ideas that make Blender authoring more powerful for Astra.
