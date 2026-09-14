# Prior art — seed map for research

This file is a starting point, not a shortlist Astra is expected to choose from.

The project should research broadly enough that its final architecture is not merely a remix of the first Blender Agent repositories we happened to find.

## Research posture

For each important design problem, Astra should generate several plausible solution families and use Luna/subagents to investigate them independently when useful.

Ask research workers for compact answers with current sources/code, what the approach is actually good at, its limitations, and what mechanism may transfer.

Astra owns synthesis. Research findings are inputs, not architecture authority.

Search outside Blender when the problem is more general than Blender.

Relevant adjacent fields may include:

- computer vision and active perception;
- robotics / visual servoing;
- CAD / geometric constraints;
- procedural modeling and scene grammars;
- Houdini-style workflows;
- game-editor prefabs / scene assembly;
- HCI and direct manipulation;
- differentiable rendering / inverse graphics;
- 3D vision and correspondence;
- production asset pipelines;
- autonomous software agents and Computer Use.

## Current Blender-agent seeds

### `ifBars/blender-agent-studio`

https://github.com/ifBars/blender-agent-studio

High-value ideas observed so far:

- Astra-oriented execution guidance;
- staged modeling workflows;
- reference cameras and overlays;
- landmarks;
- multiview inspection;
- bounded Blender tooling;
- reusable modeling/validation/GN/character workflows.

Inspect the current code before reusing anything. Borrow mechanisms, not necessarily its overall topology.

### `RobLe3/cc-blender-skill`

https://github.com/RobLe3/cc-blender-skill

Especially interesting for reference-driven work:

- source-part segmentation;
- contour analysis;
- orthographic registration;
- masks/components/landmarks;
- overlays;
- multiview fitting;
- render → compare → adjust loops;
- image-analysis helpers.

This is an obvious place to look before rebuilding deterministic visual-analysis utilities.

### `CheshireJCat/create-3d-model-skill`

https://github.com/CheshireJCat/create-3d-model-skill

A Codex-shaped derivative of the broader reference-to-3D Skill stack. Useful if its packaging or helper set can be reused directly.

### `nodecue/blender-node-skills`

https://github.com/nodecue/blender-node-skills

A strong seed for Geometry Nodes knowledge, node/socket/version handling, and graph-oriented agent workflows.

### `Aztech-Lab/EZ_Blender`

https://github.com/Aztech-Lab/EZ_Blender

Interesting because it explores a very different multi-agent Plan-and-ReAct topology. Even if this repository ultimately prefers Astra-solo operation, contrary architectures are useful research evidence.

### `achimala/dream-loop`

https://github.com/achimala/dream-loop

Interesting for visual closed-loop iteration and critic-driven refinement.

### `Top3d-ai/world-builder`

https://github.com/Top3d-ai/world-builder

Interesting for autonomous environment/world construction and repeated scene refinement.

## Questions worth researching

This is intentionally open-ended. Examples:

- How much better is Astra at direct GUI manipulation than scripted Blender control for different task classes?
- Can Astra discover and maintain spatial state reliably enough to avoid a large adapter layer?
- Which visual augmentations materially improve fine-detail recognition, and which merely add noise?
- Can semantic segmentation or correspondence be generated on demand more effectively than fixed CV pipelines?
- Can reference/model camera fitting be solved automatically enough to make visual comparison dramatically better?
- What procedural abstractions make Geometry Nodes easiest for an AI to author and repair?
- Can parts, anchors, contacts and support relations become a general scene-assembly language?
- Are there useful ideas in CAD constraint solvers or robotics contact reasoning that outperform ad-hoc GN logic?
- How should an AI choose its next view or zoom level to reduce uncertainty fastest?
- Which parts of existing Skills are actually useful in real Blender sessions rather than attractive on paper?
- What would a Blender workflow look like if designed specifically for a frontier multimodal model rather than for a human artist?

The best research questions may emerge only after implementation begins.

## Reuse policy

Before copying third-party code, inspect current source, provenance and license.

Prefer reuse when it saves work or preserves a stronger mechanism. Prefer a fresh implementation when integration cost, assumptions, quality or licensing make reuse worse.

Do not preserve local architecture merely to differentiate this repository from upstream. If an existing solution is already better, use it.
