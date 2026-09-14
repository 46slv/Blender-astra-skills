# Procedural authoring — implemented choices

The production guidance is maintained in
[the Skill authoring reference](../skills/blender/references/authoring.md).
Read [RESEARCH.md](RESEARCH.md) for alternatives, evidence and limits.

## Adopted

- Keep separate moving parts on native parent pivots; use explicit local frames for attachments.
- Use editable profile-ring meshes and Bezier curves where those describe the shape directly.
- Use GN for repetition and derived dimensions, retaining instances until a consumer needs mesh geometry.
- Probe the installed node mode and sockets before wiring. Set Blender 5.2 modifier inputs through typed RNA and verify evaluated geometry afterwards.
- Preserve generating source, material assignments, camera links and useful authoring structure through save/reopen.

The articulated lamp combines these representations instead of making the entire
asset a procedural graph. The shelf exposes Width, Depth, Height and Levels;
spacing and post centers follow those inputs. Instance counts, bounds and surface
hits were measured after changes and after reopening the file.

## Boundaries

Blender constraints are an ordered stack, not a global CAD solver. Origin placement
is not full mesh contact; a single ray or AABB overlap is not a collision proof.
Generic assembly solving, terrain contact, production character deformation and
large environment generation remain task-specific work rather than claimed
capabilities of these examples.
