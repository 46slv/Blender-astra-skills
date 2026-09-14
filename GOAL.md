# Goal — Build the best Blender Skill Astra can discover

Create a genuinely useful Blender Skill that lets Astra do high-quality 3D work with as little unnecessary mediation as possible.

The Skill should amplify Astra's own strengths rather than force Astra through an architecture designed in advance by a weaker understanding of the problem.

## Outcome

A future Astra should be able to use this repository's Skill to take on real Blender work—modeling, reference-driven refinement, procedural authoring, scene assembly, and related tasks—and reach a result that is actually usable, editable where that matters, and visually/structurally coherent.

How that is achieved is deliberately open.

Astra may keep, replace, simplify, or discard the architecture ideas currently in `docs/`. It may reuse existing public Skills, invent new mechanisms, combine visual reasoning with deterministic tools, lean heavily on Geometry Nodes, use ordinary modeling where that is stronger, or discover an approach not anticipated here.

## Research expectation

Before settling on major design choices, investigate the space deeply.

Generate multiple plausible approaches and research them broadly. Use Luna/subagents as research workers for independent questions and competing possibilities when useful. Search beyond Blender-specific agent projects when adjacent fields may contain better ideas.

Astra owns synthesis and the final design.

Interactive Blender manipulation should normally remain with Astra itself rather than being delegated to a host-operating worker, because continuity of visual/spatial state is valuable. Research is the main place where parallel delegation is encouraged.

## Self-understanding

Astra should discover what it can actually do in the current environment and design around those real capabilities.

Do not freeze assumptions about Astra, Computer Use, image understanding, Blender tooling, Python, MCP, Geometry Nodes, or available Skill mechanisms from this document. Inspect and exploit the live capability surface.

If Astra can solve part of the problem directly and elegantly, do not wrap that ability in unnecessary infrastructure.

## Completion

Finish the Skill, not just the architecture.

The work is complete when Astra can actually use what it built for representative real Blender tasks and the result behaves like a practical tool rather than a design proposal.

Use whatever checks, experiments, retries, comparisons, or live Blender work Astra judges necessary to become confident that it works. No fixed validation ritual, test count, benchmark suite, schema set, or package topology is prescribed here.

Keep only machinery that proves useful.

## Boundaries

- preserve user/source assets unless destructive change is explicitly appropriate;
- respect repository and host authority;
- do not use credentials or paid/external services implicitly;
- inspect licenses/provenance before copying third-party code;
- do not delegate interactive Blender control merely to satisfy an orchestration pattern.

Everything else is a design problem for Astra to solve.

## Starting point

1. Read `AGENTS.md`.
2. Inspect the current repository and runtime capabilities.
3. Read `docs/PRIOR_ART.md` and any other focused document that appears useful.
4. Research aggressively.
5. Decide what architecture is actually warranted.
6. Build it to completion.
