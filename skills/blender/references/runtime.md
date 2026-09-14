# Direct execution

Use a suitable existing bpy/MCP channel if one is available and the target identity is clear. A generic Python endpoint is trusted code execution, not a sandbox. Don't install a second bridge just for consistency.

## Local session fallback

`scripts/session.py` runs on ordinary host Python (standard library only). `live.py`, `observe.py`, `gn.py` and `fit.py` run inside Blender; Blender supplies bpy, mathutils and NumPy. No package install, credential, network service or persistent Blender preference change is needed.

Resolve paths against this skill directory, not the task's working directory. Example shell commands (replace paths with observed locations):

```text
python /skill/scripts/session.py start --blender /installed/blender --session /task/work/live
python /skill/scripts/session.py status --session /task/work/live
python /skill/scripts/session.py exec --session /task/work/live --script /task/work/edit.py
python /skill/scripts/session.py result --session /task/work/live --id REQUEST_ID
python /skill/scripts/session.py stop --session /task/work/live
```

`start` requires a fresh empty directory. It launches a new GUI Blender with factory startup and automatic file scripts disabled. It preserves the user's existing processes/preferences. The session directory is trusted local code storage; it is not protected from other processes running as the same user. Keep one writer per session. `stop` disarms the timer and leaves the Blender window and its work open.

Each script executes in a persistent namespace containing `bpy` and `SESSION_DIR`. The skill's scripts directory is already on `sys.path`. For example:

```python
import json
from observe import summary, render
print(json.dumps(summary()))
# Use the observed exact names for edits. Then render a camera and inspect PNG.
print(render(SESSION_DIR.parent / 'candidate.png', bpy.context.scene.camera))
```

The response includes request ID, Python output, elapsed time, active file and error traceback. Save with `bpy.ops.wm.save_as_mainfile(filepath=...)` to an explicitly chosen candidate. Open a known source in the dedicated session with `bpy.ops.wm.open_mainfile(filepath=...)`; the persistent timer survives file loading. File changes invalidate object references: reacquire `bpy.data` objects afterwards. Stop running animation/modal operators before scripted mutations.

Read `status`, inspect the intended scene, then edit. Each request checks session identity and the filepath observed on submission. Use `--expect-file /known/candidate.blend` when a script must apply to that file. File identity is a guard against a changed target, not a diff of concurrent UI edits.

## Uncertain outcomes

A client timeout returns `unknown` plus an ID. Read that same result later; **do not resubmit**. One long render can be working correctly while the client has timed out. A Python error may follow successful partial edits. Inspect state and repair from the known point or reopen your checkpoint. A crash leaves `.running` as evidence and is never replayed automatically. If `submit.lock` remains after client failure, inspect pending/running/results and the owning process before manually removing that stale lock. Never clear another writer's lock.

`session.json` is a heartbeat and file summary; `blender.log` captures native render/startup errors. Main-thread scripts temporarily block the UI. Keep commands short except intentional renders. File queues add roughly one timer tick (~0.1 s), avoiding repeated Blender startup. There is no arbitrary-script cancellation/rollback feature.

For background batch work, use Blender directly with `--background --factory-startup --disable-autoexec --python-exit-code 1 --python script.py`. For an authorized existing GUI session, the same `live.start(fresh_directory)` can be called through its established Python channel; inspect that target first. No ad-hoc console typing is necessary when an API already works.

## Computer Use

Use the environment's current computer-use skill/API, not a remembered tool name. Select the exact returned window object; refresh after actions or script changes. Screenshots are useful for menus, topology/sculpt tools, viewport composition and confirming the user's visible workspace. Camera renders are smaller, repeatable and easier to compare. The two observations serve different purposes.

Validated here: Windows, Blender 5.2.1 LTS, host Python 3.12, Blender Python 3.13, Cycles CPU, Workbench, `node_repl` + `@oai/sky` screenshots and keyboard action. These are observations, not requirements for a future runtime. Other Blender versions/platforms need live probes.
