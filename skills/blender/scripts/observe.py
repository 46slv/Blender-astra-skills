"""Import inside Blender: deliberate views, evaluated geometry, pixel-to-surface.

Pixel coordinates are normalized (u right, v DOWN), origin top-left.
Ray evidence is geometric: it does not model transparency, refraction or volumes.
"""
from contextlib import contextmanager
import json
from pathlib import Path

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def aim(camera, target):
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.view_layer.update()


def project(camera, points, scene=None):
    scene = scene or bpy.context.scene
    bpy.context.view_layer.update()
    result = [world_to_camera_view(scene, camera, Vector(p)) for p in points]
    return [(p.x, 1 - p.y, p.z) for p in result]


def summary(names=None):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    objects = [bpy.data.objects[n] for n in names] if names else list(bpy.context.scene.objects)
    result = []
    for obj in objects:
        ev = obj.evaluated_get(depsgraph)
        corners = [tuple(ev.matrix_world @ Vector(p)) for p in ev.bound_box] if obj.type in {'MESH', 'CURVE', 'FONT', 'SURFACE'} else []
        result.append({'name': obj.name, 'type': obj.type, 'parent': obj.parent.name if obj.parent else None,
                       'location_world': list(obj.matrix_world.translation), 'bounds_world': corners,
                       'modifiers': [(m.name, m.type) for m in obj.modifiers],
                       'hidden_render': obj.hide_render, 'visible_viewport': obj.visible_get()})
    return {'file': bpy.data.filepath, 'scene': bpy.context.scene.name, 'mode': bpy.context.mode,
            'objects': result, 'evaluated_instances': sum(i.is_instance for i in depsgraph.object_instances)}


@contextmanager
def restore_properties():
    saved = []
    def set_value(owner, key, value):
        old = getattr(owner, key)
        if isinstance(old,bpy.types.ID):
            pass  # ID.copy() DUPLICATES datablocks; preserve the original reference.
        elif hasattr(old, 'copy'):
            old = old.copy()
        elif not isinstance(old,(str,int,float,bool,type(None))) and hasattr(old,'__iter__'):
            old = tuple(old)  # bpy_prop_array is a live view, not a value snapshot.
        saved.append((owner, key, old))
        setattr(owner, key, value)
    try:
        yield set_value
    finally:
        for owner, key, value in reversed(saved):
            setattr(owner, key, value)


def render(path, camera=None, mode='clay', size=(768, 768)):
    """Render an existing camera, restoring scene settings even after failure.

mode='material' uses the scene engine/lights. 'clay'/'ids' use Workbench.
IDs are flat object colors for visual identity, not semantic segmentation or
Cryptomatte. Instances of the same source share its ID; antialiasing mixes edges.
"""
    if mode not in {'clay', 'ids', 'material'}:
        raise ValueError(mode)
    scene = bpy.context.scene
    camera = camera or scene.camera
    if camera is None or camera.type != 'CAMERA':
        raise ValueError('An explicit CAMERA object is required')
    path = Path(path).resolve()
    if path.suffix.lower() != '.png':
        raise ValueError('Use a .png output path')
    path.parent.mkdir(parents=True, exist_ok=True)
    previous_stamp = path.stat().st_mtime_ns if path.exists() else None
    legend = {}
    with restore_properties() as setv:
        setv(scene, 'camera', camera)
        setv(scene.render, 'resolution_x', size[0])
        setv(scene.render, 'resolution_y', size[1])
        setv(scene.render, 'resolution_percentage', 100)
        setv(scene.render, 'use_border', False)
        setv(scene.render, 'use_sequencer', False)
        setv(scene.render, 'filepath', str(path))
        setv(scene.render.image_settings, 'file_format', 'PNG')
        setv(scene.render.image_settings, 'color_mode', 'RGBA')
        if mode != 'material':
            setv(scene.render, 'use_compositing', False)
            setv(scene.render, 'engine', 'BLENDER_WORKBENCH')
            sh = scene.display.shading
            setv(sh, 'light', 'FLAT' if mode == 'ids' else 'STUDIO')
            setv(sh, 'color_type', 'OBJECT' if mode == 'ids' else 'SINGLE')
            setv(sh, 'single_color', (0.65, 0.65, 0.65))
            setv(sh, 'show_shadows', mode == 'clay')
            setv(sh, 'show_cavity', mode == 'clay')
            setv(sh, 'show_specular_highlight', mode == 'clay')
            setv(sh, 'show_object_outline', False)
            setv(sh, 'background_type', 'WORLD')
            setv(scene.render, 'film_transparent', True)
        if mode == 'ids':
            # Changing view_transform can reset look; preserve it before that side effect.
            setv(scene.view_settings, 'look', scene.view_settings.look)
            setv(scene.view_settings, 'view_transform', 'Standard')
            setv(scene.view_settings, 'look', 'None')
            setv(scene.view_settings, 'exposure', 0)
            setv(scene.view_settings, 'gamma', 1)
            for i, obj in enumerate(sorted(scene.objects, key=lambda o: o.name), 1):
                # Deterministic separated palette; legend records LINEAR object colors.
                color = (((i * 73) % 251 + 4) / 255, ((i * 137) % 251 + 4) / 255, ((i * 199) % 251 + 4) / 255, 1)
                setv(obj, 'color', color)
                legend[obj.name] = color
        outcome = bpy.ops.render.render(write_still=True)
        if 'FINISHED' not in outcome or not path.is_file() or not path.stat().st_size or path.stat().st_mtime_ns == previous_stamp:
            raise RuntimeError(f'Render did not produce a fresh PNG: {path}; outcome={outcome}')
        metadata = {'path': str(path), 'camera': camera.name, 'mode': mode, 'size': list(size),
                    'camera_matrix': [list(row) for row in camera.matrix_world],
                    'projection': camera.data.type, 'lens': camera.data.lens,
                    'ortho_scale': camera.data.ortho_scale, 'shift': [camera.data.shift_x, camera.data.shift_y],
                    'pixel_aspect': [scene.render.pixel_aspect_x, scene.render.pixel_aspect_y],
                    'legend_linear_rgba': legend}
        path.with_suffix('.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    return metadata


class SurfaceProbe:
    """Snapshot of evaluated visible geometry, including GN/collection instances.

Rebuild after edits. Uses current VIEWPORT depsgraph visibility, NOT render
visibility; discrepancies with a render require inspecting modifier/visibility
settings. Transparent surfaces are still hit. Not a persistent scene cache.
"""
    def __init__(self):
        bpy.context.view_layer.update()
        depsgraph = bpy.context.evaluated_depsgraph_get()
        trees = {}
        self.parts = []
        for inst in depsgraph.object_instances:
            obj = inst.object
            if not inst.show_self or obj.type not in {'MESH', 'CURVE', 'FONT', 'SURFACE'}:
                continue
            # GN can reuse a temporary Object address for different instance meshes.
            # Evaluated geometry identity, not that temporary Object, keys the BVH.
            key = (obj.type, obj.data.as_pointer())
            if key not in trees:
                mesh = obj.to_mesh()
                try:
                    trees[key] = BVHTree.FromPolygons([v.co.copy() for v in mesh.vertices],
                                                     [list(p.vertices) for p in mesh.polygons]) if mesh and mesh.polygons else None
                finally:
                    obj.to_mesh_clear()
            tree = trees[key]
            if tree is not None:
                matrix = inst.matrix_world.copy()
                if abs(matrix.determinant()) < 1e-12:
                    continue
                self.parts.append((obj.original.name, tuple(inst.persistent_id), tree, matrix, matrix.inverted()))

    def ray(self, origin, direction, max_distance=float('inf')):
        origin, direction = Vector(origin), Vector(direction).normalized()
        best = None
        for name, instance, tree, matrix, inverse in self.parts:
            local_direction = (inverse.to_3x3() @ direction).normalized()
            pos, normal, face, _ = tree.ray_cast(inverse @ origin, local_direction)
            if pos is None:
                continue
            world = matrix @ pos
            distance = (world - origin).dot(direction)
            if distance < 0 or distance > max_distance or (best and distance >= best['distance']):
                continue
            n = (inverse.transposed().to_3x3() @ normal).normalized()
            best = {'object': name, 'instance': instance, 'position': list(world),
                    'normal': list(n), 'face_evaluated': face, 'distance': distance}
        return best

    def pixel(self, camera, u, v, scene=None):
        scene = scene or bpy.context.scene
        if camera.data.type not in {'PERSP', 'ORTHO'}:
            raise ValueError('Pixel probing supports perspective/orthographic cameras only')
        frame = camera.data.view_frame(scene=scene)
        xs, ys = [p.x for p in frame], [p.y for p in frame]
        local = Vector((min(xs) + u * (max(xs) - min(xs)), max(ys) - v * (max(ys) - min(ys)), frame[0].z))
        matrix = camera.matrix_world
        if camera.data.type == 'ORTHO':
            origin = matrix @ Vector((local.x, local.y, 0))
            direction = matrix.to_3x3() @ Vector((0, 0, -1))
        else:
            origin = matrix.translation
            direction = matrix.to_3x3() @ local
        direction.normalize()
        optical_axis = (matrix.to_3x3() @ Vector((0,0,-1))).normalized()
        factor = direction.dot(optical_axis)
        near, far = camera.data.clip_start/factor, camera.data.clip_end/factor
        hit = self.ray(origin+direction*near, direction, far-near)
        if hit:
            hit['distance'] += near
        return hit

    def visibility(self, camera, points, tolerance=0.002):
        """Surface-point visibility, not visibility of internal semantic anchors.

Use a few points on the uncertain feature. Rank candidate cameras by visible
points, then inspect the resulting image. This cannot reveal unknown reference
geometry; it only chooses a diagnostic view of the model we have.
"""
        results = []
        for point, (u,v,z) in zip(points,project(camera,points)):
            if not (0 <= u <= 1 and 0 <= v <= 1 and camera.data.clip_start <= z <= camera.data.clip_end):
                results.append({'state':'outside','pixel':[u,v]})
                continue
            hit = self.pixel(camera,u,v)
            visible = hit is not None and (Vector(hit['position'])-Vector(point)).length <= tolerance
            results.append({'state':'visible' if visible else 'occluded_or_missing',
                            'pixel':[u,v], 'hit':hit})
        return {'visible':sum(r['state']=='visible' for r in results),
                'total':len(results),'points':results}
