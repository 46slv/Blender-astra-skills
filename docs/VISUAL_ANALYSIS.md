# Visual analysis — implementation and remaining questions

The production workflow is maintained in
[the Skill perception reference](../skills/blender/references/perception.md).
Read [RESEARCH.md](RESEARCH.md) for measured outcomes and source attribution.

## Adopted

- Match reference/model projection and canvas, then inspect the same feature at a useful scale.
- Use analytic projection and evaluated, instance-aware ray hits to connect pixels to source parts, surface positions and normals.
- Compare candidate cameras by the visibility of the uncertain feature; inspect the selected view.
- Correct camera and a few meaningful shape controls separately, with bounded finite differences.
- Use flat identities and alpha silhouettes as evidence, not automatic semantics.

`observe.py`, `fit.py` and `compare.py` implement these mechanisms. The lamp
experiment demonstrates known-correspondence correction and visibility-driven
inspection of a hidden bulb. Exact model-side information does not establish
that the model matches unknown reference geometry.

## Still optional research

Learned segmentation/correspondence, dense renderer passes, edge-distance losses,
robust camera initialization and differentiable rendering may help specific tasks.
They are not implemented dependencies. Only add them when the actual task needs
more evidence than the direct multimodal + Blender-state loop supplies.
