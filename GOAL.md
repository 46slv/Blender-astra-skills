# Goal — Build `blender-astra-modeling`

## Goal

Implement a reusable Agent Skill for high-quality Blender modeling, procedural authoring, reference-driven repair, and visual/structural verification, optimized for **Astra as the solo/direct interactive Blender driver**.

The implementation should compose and adapt strong existing prior art rather than rebuild the entire Blender-agent stack from scratch.

## Done

A first usable version is complete when all of the following exist and are exercised on representative fixtures:

1. A native Skill entry point with precise trigger/non-trigger behavior and progressive disclosure.
2. Astra keeps live Blender observation, reasoning, host operation, repair, and final visual acceptance in one context by default.
3. Research-only subagent boundary is enforced/documented.
4. Multi-scale observation works: overview → target-framed → paired semantic close-up → diagnostic view when needed → final sweep.
5. Reference/model comparison supports structured evidence preparation: silhouette, edge, region mask, landmarks, overlays, and model-side diagnostic passes where applicable.
6. Ambiguous semantic region, boundary class, or occlusion relation remains `UNKNOWN` and blocks broad repair.
7. Repair is localized with declared write/protected scope and the same paired comparison packet is regenerated after repair.
8. Geometry Nodes routing supports manual-source wrappers, fully procedural generators, modular assembly, constraint/contact solving, and environment/layout workflows without forcing GN where it reduces quality or editability.
9. Authoring source remains editable; destructive realization/export is isolated to derived outputs where required.
10. Prior-art components are inspected, licensed appropriately, and reused/adapted when stronger than fresh implementations.
11. Representative host fixtures in `docs/EVALS.md` pass with structural + visual evidence.
12. The repository can explain why the resulting Skill is usable without relying on conversation history.

## Constraints

- Do not make a giant all-knowledge `SKILL.md`. Keep decision procedure in the Skill; detailed knowledge in references/docs; deterministic evidence preparation in scripts; schemas/validators for mechanical contracts.
- Do not create a multi-agent Blender host topology by default. A child may research; Astra owns live host manipulation and visual acceptance unless a separately qualified exception proves value.
- Do not treat one broad screenshot as detail/final acceptance.
- Do not infer model-side structure from RGB when Blender can expose exact scene/object/node/depth/normal/mask information.
- Do not treat edge detection, SSIM, IoU, or any single metric as semantic truth.
- Do not destroy source assets to satisfy export or verification convenience.
- Do not use Geometry Nodes merely to increase node usage.
- Do not silently copy external code without license/provenance review.

## Authority

Within this repository, normal implementation, tests, docs, scripts, schemas, fixtures, and reversible branches/commits are in scope.

Blender host interaction may be used for qualification when available, but source `.blend` overwrite, unrelated filesystem/network access, credentials, external paid services, release/publication, or destructive host actions require separate justification/authority.

## Starting point

Read in this order:

1. `AGENTS.md`
2. `docs/ARCHITECTURE.md`
3. `docs/VISUAL_ANALYSIS.md`
4. `docs/PROCEDURAL_AUTHORING.md`
5. `docs/PRIOR_ART.md`
6. `docs/EVALS.md`

## Evidence

Return compact evidence for each milestone:

- implemented paths and interfaces;
- tests/validators and results;
- exact Blender/version when host-tested;
- structural scene/node/export evidence;
- matched visual evidence and paired close-ups for detail work;
- known gaps and `UNKNOWN` results;
- prior-art provenance/license decisions;
- fixture results and regressions.

Do not claim general Skill qualification until host fixtures support it.
