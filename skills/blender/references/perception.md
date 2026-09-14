# See enough to make the right edit

## Establish correspondence before optimizing

Record the reference's projection hypothesis, image dimensions and a few named landmarks or parts. On the reference, an edge may be silhouette, overlap, seam, paint or shadow. Automatic threshold masks and edge maps do not decide which. Keep hidden regions uncertain.

For stylized drawings, try orthographic/weak perspective first when the evidence supports it. For perspective photographs, known 3D points and camera calibration help; with OpenCV already available, PnP-RANSAC is a useful alternative. Do not add a dependency just to fit a handful of controls.

Hold canonical object scale fixed. Object scale trades against orthographic scale or perspective camera distance; focal length also trades against depth. Camera translation and lens shift can explain the same 2D offset. Lock one representative of each ambiguity. Fit camera on trustworthy fixed geometry, then fit shape with that camera held fixed. For large pose uncertainty, compare several initial views rather than trusting one local solve.

`fit.solve(initial, evaluate, steps, bounds, iterations, tolerance)` uses NumPy and bounded finite differences. `evaluate(parameters)` applies a candidate and returns residuals (typically projected landmark pixel errors). Use a few semantic controls, parameter-specific steps, realistic bounds and stable visible correspondences. `rank < parameter_count` warns of local ambiguity; convergence means only that the supplied residual became small. Correlated/outlier correspondences can still mislead it. For uncertain points, downweight residuals or omit them; the solver is ordinary least squares, not RANSAC or a robust reconstruction engine.

```python
from observe import project
from fit import solve
def residual(x):
    camera.data.shift_x, camera.data.shift_y, camera.data.ortho_scale = x
    uv = project(camera, known_world_points)
    return [(a[i]-b[i])*image_size[i] for a,b in zip(uv,target_uv) for i in (0,1)]
result = solve([0,0,2], residual, [.005,.005,.01],
               bounds=([-.3,-.3,.5],[.3,.3,4]), tolerance=.5)
```

Target UV coordinates are normalized, **top-left origin, u right, v down**. `project` returns `(u,v,camera_depth)`; reject points behind the camera. Do not change render aspect while fitting. The bundled synthetic lamp experiment demonstrates camera-then-pose recovery, not automatic point recognition.

Evaluators must be idempotent absolute assignments and must restore all state they
vary. The solver reapplies the best vector even after an exception; this is not
transactional rollback if the evaluator itself fails or mutates unrelated state.
Use checkpoints for complicated material/topology evaluators. Prefer manual local
edits when a clean low-dimensional evaluator would cost more than the repair.

## Ask Blender instead of guessing pixels

```python
from observe import SurfaceProbe, render, project
probe = SurfaceProbe()  # Snapshot: rebuild after any relevant scene edit.
hit = probe.pixel(camera, .62, .39)
print(hit)  # object, transient instance identity, world position/normal, face, distance
render('/task/detail.png', camera, mode='clay', size=(900,900))
render('/task/parts.png', camera, mode='ids', size=(900,900))
```

The BVH includes evaluated mesh/curve geometry and unexpanded GN/collection instances, with transforms and inverse-transpose normal conversion. GN temporary object addresses can be reused; the helper keys geometry by evaluated data identity. Evaluated face indexes and instance `persistent_id` are observation-local, not permanent semantic IDs. Resolve edits to the source object/group and named authoring controls.

The probe follows **viewport** depsgraph visibility/modifiers, whereas render visibility can differ. Ray hits are geometric: transparent glass still blocks them; refraction, volumes, displacement visible only at render and material alpha need renderer passes. Camera probing supports perspective/orthographic and clipping, not panoramic/stereo cameras. `ids` uses flat object colors; AA blends boundaries and copies share source colors. It is an identity aid, not semantic segmentation or Cryptomatte.

Use Blender Z/Position/Normal/Cryptomatte passes when those renderer-specific distinctions are decisive. Inspect the actual renderer's supported passes and compositor API; don't infer those maps from beauty RGB. Dense per-pixel ray queries are unnecessary for a handful of disputed points.

## Choose a diagnostic view

Use `probe.visibility(camera, world_surface_points, tolerance=...)` to compare candidate cameras around a particular feature. Pick a view that exposes the feature or separates competing shape hypotheses; inspect that rendered close-up. Internal joint anchors aren't surface points and may correctly report occluded. An alternate model view reveals a flaw in the candidate; it cannot supply missing evidence about the reference's hidden side.

The lamp experiment selected a side/underside view because the front/top hid the bulb. This is a small practical transfer from active perception: spend observations where they resolve uncertainty, instead of always rendering the same six views.

## Matched image inspection

On host Python with Pillow + NumPy:

```text
python /skill/scripts/compare.py reference.png model.png --out paired.png
python /skill/scripts/compare.py reference.png model.png --out detail.png --region .4 .15 .8 .5
python /skill/scripts/compare.py reference.png model.png --out silhouette.png --alpha-masks
```

Images must already share a registered canvas. Region applies equally to both; no independent recentering hides errors. Alpha-mask mode requires transparent silhouettes, and rejects opaque/empty masks. Red shows reference-only area, blue model-only. Inspect the original and the enlarged comparison; lighting differences are not necessarily geometry errors. After a local repair, look at both the repaired feature and enough surrounding shape to catch regressions.
