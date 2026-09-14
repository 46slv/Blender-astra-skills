# Architecture — design space, not blueprint

This document records strong ideas discovered so far. It is not a specification Astra must obey.

Astra may replace any part of it if research, implementation experience, or its own capabilities suggest something better.

## 1. Central hypothesis

The most important architectural bet is continuity of intelligence around the live Blender state.

For interactive work, keep the model that sees the scene responsible for deciding what to do next whenever practical:

```text
Astra
  observe
  understand
  choose a method
  act
  look again
  change its mind if needed
  continue
```

Do not split this loop into multiple agents unless doing so clearly improves the work.

The likely exception is research: external knowledge gathering can parallelize without fragmenting Blender's live visual/spatial state.

## 2. Astra should model itself before designing the Skill

The runtime is part of the design problem.

Astra should inspect what is actually available and useful now:

- visual understanding quality and limits;
- Computer Use / GUI control;
- Blender/Python/API/MCP surfaces;
- local code execution;
- screenshot/render access;
- Geometry Nodes access and authoring methods;
- existing Skills and plugin mechanisms;
- context limits and persistence;
- research-worker availability.

This need not become a formal capability matrix. The point is to avoid designing wrappers around abilities Astra already has, or assuming abilities it does not.

Small probes are appropriate when they answer a real design question.

## 3. Research architecture

Research is intentionally allowed to be much more parallel than host operation.

For a meaningful open question, Astra can:

```text
identify design question
  ↓
generate several plausible approaches
  ↓
fan out independent research to Luna/subagents
  ↓
collect current code, primary sources, practitioner evidence, limitations
  ↓
compare incompatible approaches
  ↓
ask a second wave of questions if the search space changed
  ↓
Astra synthesizes and decides
```

Research should not be constrained to Blender Agent repositories. Useful transfers may come from:

- active perception and computer vision;
- robotics and visual servoing;
- CAD and constraint systems;
- procedural modeling;
- DCC automation;
- scene graphs and asset systems;
- HCI / direct manipulation;
- graphics and differentiable rendering;
- game/editor tooling;
- production art workflows.

Research workers return findings and evidence. They do not become the authority over the design.

## 4. Avoid architecture by anticipation

Do not create a layer because a mature system might eventually need one.

A schema, validator, service, wrapper, cache, benchmark, abstraction, agent role, or database should appear because the actual Skill benefits from it.

Prefer this progression:

```text
solve the task directly
  ↓
notice recurring friction or uncertainty
  ↓
extract the smallest useful mechanism
  ↓
keep it only if it improves subsequent work
```

The same applies to documentation. Write what future Astra needs to make better decisions; do not narrate the project for its own sake.

## 5. Existing architecture ideas worth testing

### Live Astra ownership

Astra directly owns interactive Blender observation and manipulation by default.

Luna/subagents research APIs, techniques, prior art, versions, or alternative approaches. They normally do not drive the main Blender session.

### Dynamic execution lanes

Astra may mix methods inside one task:

- GUI / Computer Use for spatial and visually driven edits;
- Python/API/adapter operations when exact state changes are easier that way;
- Geometry Nodes or modifiers when persistent procedural relationships create leverage;
- ordinary modeling, sculpting or retopology when those are the strongest primitives.

There is no target percentage for any lane.

### Visual augmentation

Astra may be weaker than a skilled human at noticing some fine visual differences from a broad screenshot.

Promising remedies include:

- enlarging both reference and model at the same region;
- silhouette or edge views;
- semantic segmentation / part masks;
- landmarks and correspondence;
- overlap / occlusion reasoning;
- Blender-side Depth, Normal, object identity, topology or other exact state;
- aligned overlays and differences;
- alternative views when projection is ambiguous.

These are tools for perception, not a mandatory pipeline. See `VISUAL_ANALYSIS.md` for the current possibility space.

### Procedural leverage

Geometry Nodes may be especially valuable for:

- reusable source parts;
- parametric families;
- modular assembly;
- automatic contact/alignment;
- repeated layout;
- scene/environment construction;
- deriving dependent values instead of exposing raw transforms.

Do not proceduralize something merely to satisfy this hypothesis. See `PROCEDURAL_AUTHORING.md` for candidate patterns.

### Prior-art composition

Strong existing work should be reused or adapted where it is genuinely better than fresh implementation. `PRIOR_ART.md` is a seed list, not an exhaustive map.

## 6. Visual state and detail

One useful invariant remains: do not pretend to understand detail that is not actually visible.

If Astra cannot distinguish a feature, it should improve the observation—zoom, change view, expose structure, process the image, or inspect Blender state—rather than confidently editing from an ambiguous overview.

Reference and model should usually be inspected at comparable detail when fidelity matters.

How this is implemented is open.

## 7. Editability and authoring source

Prefer retaining useful authoring structure when it gives future work leverage.

That may mean curves, modifiers, Geometry Nodes, source parts, semantic anchors, ordinary editable meshes, procedural scripts, or some combination.

Do not destroy useful source structure merely to make one output easier to produce. Derived/export artifacts may be destructive when the consumer requires it.

## 8. Safety boundaries

These are product boundaries, not architecture prescriptions:

- do not casually overwrite user source assets;
- do not grant research children unnecessary host authority;
- do not assume MCP or arbitrary Python is a sandbox;
- do not use credentials, network authority, or paid providers implicitly;
- respect third-party licenses and provenance.

## 9. What completion means

Completion is not a particular directory tree or set of framework components.

The repository succeeds when the resulting Skill is something Astra can actually use to produce strong Blender work, and when the implementation is understandable enough for a future Astra to continue improving it without reconstructing this conversation.

Astra decides what experiments or checks are needed to reach that confidence.
