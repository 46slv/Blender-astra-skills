# Decisions and evidence — 2026-09-14

## Continuing production and native assets

The Skill is deliberately not permanently complete. Subsequent production should
reuse/adapt existing assets and methods, investigate failures or better approaches,
and retain improvements only when they improve actual work. User feedback is a
signal about the result; Astra remains responsible for technical diagnosis and
live observation → decision → edit → observation. GOAL and Skill now say this
explicitly; current taxonomy and architecture are revisable.

Native Blender storage won over a separate manifest/database: the Asset Browser
already handles catalogs, tags, descriptions and previews, while bpy can discover
marked IDs without importing the scene. The small `scripts/assets.py` helper adds
discovery, independent append and registration for a dedicated process. Registration
is a preferences entry, not a transient registry: disable preference auto-save
before adding it and never manually save that process's preferences. No global
Skill registration or preferences save was performed.

`skills/blender/assets/library/starter-v1.blend` contains **9 assets / 4 catalogs**:
lamp collection, shelf object, shelf and radial-fastener GN groups, and five lamp
materials. All have 256 px custom previews, native descriptions/license/source
information, stable custom identity/version and generator Text pointers. The lamp's
new placement Empty preserves its internal pivots. Both GN groups enable Modifier
usage. Shelf swatches now also drive Principled Base Color for material renders.
Original example assets/scripts remain intact. Native graphs need no Python to
evaluate; re-executing source Texts uses the bundled Skill helpers.

Actual production evidence is in `artifacts/asset-reuse.png` and
the `asset_library` section of `artifacts/evidence.json`; reproduction is in
`experiments/build_asset_library.py` and `experiments/reuse_assets.py`.

- Astra visually inspected all previews, the reused assembly render and the native
  Asset Browser showing nine assets in Furniture, Generators, Lighting and Materials.
- Two appended lamps share no objects. Changing one head by 0.12 radians moved a
  bulb surface point 0.02339 m without changing the other head. Cable and hierarchy survive.
- Shelf preset has 11 instances; changing to four levels gives eight, at measured
  1.4 × 0.5 × 1.2 m bounds and floor Z=0. Lamp placement rests on the top board.
- Separately appended shelf/fastener generators give seven and ten instances;
  original shelf and lamp fasteners remain eight and six. Appended brass is independent.
- A separate factory-startup process reopened the **614,539-byte** library: all nine
  previews, catalog references and source Texts survive; no cameras, lights, floor,
  external images, linked libraries, sounds or clips. Reopened reuse-scene shelf
  controls still yield ten instances at six levels; lamp placement/pivots/cable survive.

Trials exposed two practical details: file loading temporarily clears the timer's
window context (edits now start in the following request), and Blender 5.2 can retain
an unused Library ID after append. Check actual linked ID dependencies, not just
Library record count; the owned reuse example removes empty records before saving.
Blender auto-save preferences is enabled by default, so omitting `save_userpref`
alone is insufficient for temporary registration.

Limits remain visible on each asset: fixed-radius fastener ring, static cable,
untextured shelf placeholder materials and no joinery; extreme shelf height/level
combinations can overlap boards. No third-party acquisition was needed here, and
the configured legacy User Library path was absent. Acquired resources can use
explicit private/project library roots; retain license evidence and permitted-use
limits rather than treating a public download as permission to redistribute.
External texture packing is documented, not claimed as exercised by these texture-free assets.

Research sources: [native libraries](https://docs.blender.org/manual/en/5.2/files/asset_libraries/introduction.html),
[Asset Browser](https://docs.blender.org/manual/en/5.2/editors/asset_browser.html),
[library read/write API](https://docs.blender.org/api/5.2/bpy.types.BlendDataLibraries.html).
Luna researched alternatives and API pitfalls; Astra owned extraction and live reuse.
The stock Skill validator was invoked again but still cannot run without PyYAML;
no dependency was installed for that check.

The original branch contained research documents only. Implementation was built
against actual local capability: Windows Blender **5.2.1 LTS**, bpy/Python 3.13,
NumPy, Cycles CPU and Workbench; host Python 3.12 with Pillow/NumPy; direct Windows
screenshots and keyboard input through `@oai/sky`. No Blender MCP was exposed in
this session. Two pre-existing Blender windows were left untouched; trials used
new dedicated sessions. Luna Max workers researched independently; Astra operated
Blender, implemented the Skill and made the final choices.

## Alternatives investigated

| Question | Compared | Adopted and why |
|---|---|---|
| Execution | GUI-only, installed MCP, subprocess per edit, live bpy | Existing direct channel first; small main-thread file queue when absent. No network/add-on setup; ~0.1 s polling. GUI remains available. |
| Perception | RGB critique, threshold segmentation, learned correspondence, renderer truth | Direct reasoning and deliberate crops; exact model-side rays/projection/identity. Classical masks are not semantic recognition. |
| Fitting | PnP, differentiable renderers, finite differences | Bounded finite differences over native controls; analytic landmark projection avoids rerendering every optimizer step. |
| Active views | Fixed turntable, information-gain planning, feature visibility | Rank a few cameras for the uncertain feature. Larger information models didn't earn their cost. |
| Authoring | All-GN, Python rebuild, native constraints, hybrid | Native pivots/curves/profile meshes for lamp; GN for repetition and derived dimensions. |
| Reuse | Complete stacks vs small components | NodeCue probe unchanged with MIT notice; original helpers where integration/dependency costs outweighed reuse. |

## Prior-art findings

- [ifBars/blender-agent-studio](https://github.com/ifBars/blender-agent-studio): MIT;
  strong bounded processes, camera fitting, evidence and asset inspection. Its
  broader validator/SceneIR stack was unnecessary for these trials.
- [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill): MIT;
  useful masks/contours/correspondence recipes. Thresholding/watershed is not
  semantic recognition; bounding-box reports do not establish registration.
- [CheshireJCat/create-3d-model-skill](https://github.com/CheshireJCat/create-3d-model-skill):
  MIT with derivative provenance; useful discoverable entrypoint and staged detail.
- [NodeCue](https://github.com/nodecue/blender-node-skills): MIT; live mode/socket
  probing is reused. Fixed commit, hash and license are in bundled provenance.
- [dream-loop](https://github.com/achimala/dream-loop): MIT; critique and stall
  handling transfer. Generated images are art direction, not geometric truth.
- [EZ_Blender](https://github.com/Aztech-Lab/EZ_Blender) and
  [world-builder](https://github.com/Top3d-ai/world-builder): examined contrary
  multi-agent/world-building approaches. No clear reusable root license found;
  no code copied. Their service/architecture requirements were not adopted.

## Adjacent fields that changed the design

[Visual servoing](https://hal.inria.fr/inria-00350283) suggests correcting a small
parameter vector from feature error, instead of rebuilding an entire object.
[EPnP](https://imagine.enpc.fr/~lepetitv/pdfs/lepetit_ijcv08.pdf) is a calibrated-camera
alternative for known noncoplanar landmarks. Joint camera/shape fitting has gauge
freedoms; the implementation separates blocks and reports local rank.
[Single View Metrology](https://ora.ox.ac.uk/objects/uuid%3A9b99df78-df75-49a9-a1b8-1b38e1b173a8)
and [PAniC-3D](https://openaccess.thecvf.com/content/CVPR2023/papers/Chen_PAniC-3D_Stylized_Single-View_3D_Reconstruction_From_Portraits_of_Anime_Characters_CVPR_2023_paper.pdf)
reinforce why projection evidence and stylization priors matter.

[Active reconstruction](https://rpg.ifi.uzh.ch/docs/ICRA16_Isler.pdf) motivates
observing the feature whose visibility resolves uncertainty. This implementation
uses a few visibility queries, not a robotics planner.
[Onshape Mate Connectors](https://cad.onshape.com/help/Content/Assembly/assembly_mate_connector.htm)
and [ROS tf2](https://docs.ros.org/en/galactic/Concepts/About-Tf2.html) motivate named
local frames and acyclic attachment trees. [OpenUSD instancing](https://openusd.org/dev/api/_usd__page__scenegraph_instancing.html)
reinforces prototype/instance separation. These are independently implemented
ideas; no paper text or implementation code was copied.

Blender-specific authorities include the [5.2 Python changes](https://developer.blender.org/docs/release_notes/5.2/python_api/),
[dependency graph API](https://docs.blender.org/api/5.2/bpy.types.Depsgraph.html),
[projection API](https://docs.blender.org/api/5.2/bpy_extras.object_utils.html) and
[main-thread timer guidance](https://docs.blender.org/api/current/bpy.app.timers.html).

## What actually passed

### Main finding: use known 3D state as perception

The useful change is not a larger RGB critique pipeline. On the model side,
Blender already knows the geometry, transforms and source relationships. A camera
pixel becomes a ray through evaluated geometry; its nearest hit identifies the
source part, world position and surface normal. Reprojecting that hit checks the
pixel/3D convention. This also works for unexpanded GN instances by transforming
the ray into each instance's local frame. That information can localize a repair
without asking vision to infer the same surface from highlights or shadows.

The same geometry answers which candidate view exposes an uncertain feature.
Analytic landmark projection then supplies a cheap error signal for bounded
camera/parameter corrections. This connects observation to editable source
controls, rather than repeatedly replacing a whole model from a screenshot.

Exactness belongs to the **current model and evaluated geometry**, not to the
reference image or its unseen side. A wrong model yields precisely described
wrong geometry. Appearance, renderer-only effects and semantic correspondence
still require visual judgment and appropriate renderer evidence. Persistent
instance IDs and evaluated face indexes are temporary observations, not a durable
semantic naming system. These distinctions belong in future Astra's reasoning,
not only in a benchmark disclaimer.

### Measured results

Evidence is in `artifacts/evidence.json` and the adjacent images/`.blend`.

- Created an articulated enamel/brass lamp with an inner shade wall, 3 native
  pivots, Bezier cable and 6 GN fastener instances. Inspected hero and bulb close-up.
- Corrected degenerate poles and closed shell necks. All **28** tested closed
  authored mesh parts had zero nonmanifold edges and zero degenerate faces.
- With synthetic known correspondences, corrected orthographic framing from
  **59.31 px RMS to 0.000082 px**, and joint angles from **27.60 px to 0.00045 px**.
  Near-exact results reflect a controlled same-model experiment, not photo accuracy.
- Front/top had 0/4 visible bulb points, side/below 3/4. The chosen side close-up
  exposed the bulb and inner shade.
- Changed shelf Width/Height/Levels; evaluated 7 boards + 4 posts as **11 instances**,
  width 1.55 m, height 1.8 m and floor-aligned minimum Z, without realization.
- Pixel → evaluated surface → pixel passed with perspective, lens shift and
  nonsquare aspect, below 1e-5 normalized error.
- Reopened the saved `.blend`: camera links, source Texts, curves, pivots and live
  GN controls survived. Changing levels 3 → 7 yielded 7 → 11 instances.
- Checked render-setting restoration, unchanged camera identity/object count,
  colors and failure-path restoration. A wrong-file request was rejected before
  its marker write. Timed-out rendering completed under the original request ID.

Live trials caught obsolete Workbench properties, transient instance RNA wrappers,
reused GN temporary Object addresses and accidental camera ID duplication during
property snapshots. These were repaired and affected behavior retested. Camera
preservation was caught by reopening, not by inspecting a successful render.
An independent read-only Skill review led to explicit material-sharing guidance,
literal GN input semantics and fresh-image verification after rendering.

Python syntax compilation passed. The stock Skill validator was invoked but could
not run because PyYAML is absent from both Python runtimes; frontmatter and linked
resources were inspected directly. No dependency was installed just for that check.

## Limits

### Repository publication

The public example file contains only the two generated scenes and their exact
generator Texts, with a fresh default workspace and project-relative file-browser
directories. It is 184,555 bytes. A separate factory-startup Blender process
reopened it and confirmed no external asset paths, linked libraries, packed
reference images, movie clips or sounds; both camera links and GN level changes
remained functional. Publication evidence is appended to `artifacts/evidence.json`.
PNG text/EXIF metadata, including render-source paths, was removed without changing
decoded pixels; color metadata was preserved.
Local session queues, logs, backups and machine-specific evidence paths are not
part of the commit. Reproduction writes into the session's experiment directory,
so it does not overwrite the published example.

### Capability limits

Correspondences/shape controls are chosen by Astra. Arbitrary photo reconstruction,
learned segmentation, transparent/volumetric visibility, collision resolution and
production character deformation are not validated capabilities. Good silhouettes
do not certify 3D truth. SurfaceProbe follows viewport geometry, which can differ
from render-only modifiers/displacement/visibility. Trusted Python execution has
no rollback or arbitrary-script interruption. Only Blender 5.2.1 on this Windows
host was exercised; older API fallback needs its own runtime probe.
