"""Editable product example. Run inside Blender; creates a new scene, keeps others.

Native parent pivots articulate the mechanism; curves retain cable editability;
a lathed shell retains its mesh; GN keeps the base fasteners as instances.
No download, external assets, scene reset, render or save occurs on import.
"""
import math
import bpy
from mathutils import Vector
from observe import aim


def build(name='Articulated Lamp'):
    scene = bpy.data.scenes.new(name)
    bpy.context.window.scene = scene
    scene.unit_settings.system = 'METRIC'
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    scene.world = bpy.data.worlds.new(name + ' World')
    scene.world.color = (.18, .18, .18)

    def material(name, color, metal=0, rough=.35):
        m = bpy.data.materials.new(name)
        m.diffuse_color = (*color, 1)
        m.use_nodes = True
        bs = m.node_tree.nodes.get('Principled BSDF')
        bs.inputs['Base Color'].default_value = (*color, 1)
        bs.inputs['Metallic'].default_value = metal
        bs.inputs['Roughness'].default_value = rough
        return m

    green = material('Enamel - forest', (.025, .16, .12), .4, .28)
    brass = material('Brushed brass', (.55, .31, .09), .8, .26)
    dark = material('Rubber and cable', (.012, .018, .018), 0, .65)
    ivory = material('Shade interior', (.82, .77, .62), .15, .32)

    def link(obj, mat=None, parent=None):
        scene.collection.objects.link(obj)
        if mat and obj.data:
            obj.data.materials.append(mat)
        if parent:
            obj.parent = parent
        return obj

    def pivot(name, location, parent=None, angle=0):
        o = link(bpy.data.objects.new(name, None), parent=parent)
        o.empty_display_type = 'ARROWS'
        o.empty_display_size = .06
        o.location, o.rotation_euler.y = location, angle
        return o

    def lathe(name, profile, mat, parent=None, segments=96):
        vertices, rings, faces = [], [], []
        for r,z in profile:
            count = 1 if abs(r)<1e-10 else segments
            rings.append(list(range(len(vertices),len(vertices)+count)))
            vertices.extend((r*math.cos(2*math.pi*i/count),r*math.sin(2*math.pi*i/count),z) for i in range(count))
        pairs = list(zip(rings[:-1],rings[1:]))
        if len(rings[0])>1 and len(rings[-1])>1:
            pairs.append((rings[-1],rings[0]))  # Close shell wall at the neck/rim.
        for a,b in pairs:
            for i in range(segments):
                j=(i+1)%segments
                if len(a)==1:
                    faces.append((a[0],b[j],b[i]))
                elif len(b)==1:
                    faces.append((a[i],a[j],b[0]))
                else:
                    faces.append((a[i],a[j],b[j],b[i]))
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertices, [], faces)
        mesh.update()
        o = link(bpy.data.objects.new(name, mesh), mat, parent)
        for p in mesh.polygons:
            p.use_smooth = True
        return o

    def cylinder(name, radius, depth, mat, parent=None, location=(0,0,0), sideways=False):
        o = lathe(name, [(0,-depth/2),(radius,-depth/2),(radius,depth/2),(0,depth/2)], mat, parent, 64)
        o.location = location
        if sideways:
            o.rotation_euler.x = math.pi/2
        bevel = o.modifiers.new('Machined edge', 'BEVEL')
        bevel.width, bevel.segments = .0015, 3
        return o

    def rod(name, length, y, parent):
        return cylinder(name, .013, length, green, parent, (0,y,length/2))

    base = lathe('Weighted base', [(0,0),(.125,0),(.14,.012),(.14,.035),(.126,.055),(.045,.068),(0,.068)], green)
    cylinder('Base lower trim', .134, .008, brass, location=(0,0,.009))
    cylinder('Rubber foot', .121, .006, dark, location=(0,0,.003))
    cylinder('Swivel collar', .035, .053, brass, location=(0,0,.080))
    lower = pivot('Shoulder - rotate Y', (0,0,.11), angle=-.40)
    upper = pivot('Elbow - rotate Y', (0,0,.43), lower, 1.05)
    head = pivot('Head - rotate Y', (0,0,.40), upper, math.pi-.40-.65)
    for p, length, label in [(lower,.43,'Lower'), (upper,.40,'Upper')]:
        for y in [-.031,.031]:
            rod(label + ' link ' + str(y), length, y, p)
        for z in ([0] if p == lower else [0,length]):
            cylinder(label + ' hinge', .032, .10, green, p, (0,0,z), True)
            for y in [-.057,.057]:
                cylinder(label + ' brass cap', .020, .009, brass, p, (0,y,z), True)
                cylinder(label + ' bolt', .008, .011, dark, p, (0,y*1.11,z), True)
    cylinder('Shade mount', .023, .045, brass, head, (0,0,.005))
    profile = [(.023,.016),(.047,.020),(.064,.044),(.085,.080),(.13,.15),(.165,.198),
               (.168,.208),(.168,.214),(.160,.214),(.157,.203),(.122,.153),(.077,.083),(.056,.049),(.039,.032),(.023,.031)]
    shade = lathe('Spun shade - editable profile rings', profile, green, head)
    shade.data.materials.append(ivory)
    for poly in shade.data.polygons:
        if poly.index // 96 >= 7:
            poly.material_index = 1
    rim = lathe('Rolled brass rim', [(.160,.207),(.170,.207),(.172,.211),(.170,.217),(.160,.217)], brass, head)
    cylinder('Socket', .027, .058, dark, head, (0,0,.07))
    bulbmat = material('Warm frosted bulb', (1,.82,.55), 0,.3)
    bs = bulbmat.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Emission Color'].default_value = (1,.65,.25,1)
    bs.inputs['Emission Strength'].default_value = .6
    bulb = lathe('Bulb', [(0,.08),(.027,.085),(.039,.11),(.043,.145),(.036,.17),(.02,.188),(0,.195)], bulbmat, head)
    curve = bpy.data.curves.new('Flexible power cable', 'CURVE')
    curve.dimensions, curve.bevel_depth, curve.bevel_resolution = '3D', .004, 4
    spline = curve.splines.new('BEZIER')
    points = [(-.08,.04,.033),(-.18,.08,.018),(-.32,.12,.012),(-.42,.02,.009),(-.40,-.12,.009),(-.27,-.17,.009)]
    spline.bezier_points.add(len(points)-1)
    for p, co in zip(spline.bezier_points, points):
        p.co = co
        p.handle_left_type = p.handle_right_type = 'AUTO'
    link(bpy.data.objects.new('Power cable - editable Bezier', curve), dark)

    # Native GN fastener ring. Inspect actual sockets when adapting to another version.
    fasteners = link(bpy.data.objects.new('Base fasteners - Geometry Nodes', bpy.data.meshes.new('Fastener host')))
    group = bpy.data.node_groups.new('Radial fastener array', 'GeometryNodeTree')
    count = group.interface.new_socket(name='Count', in_out='INPUT', socket_type='NodeSocketInt')
    count.default_value, count.min_value, count.max_value = 6, 3, 64
    group.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    n, links = group.nodes, group.links
    inp, out = n.new('NodeGroupInput'), n.new('NodeGroupOutput')
    circle = n.new('GeometryNodeMeshCircle')
    circle.inputs['Radius'].default_value = .10
    links.new(inp.outputs['Count'], circle.inputs['Vertices'])
    bolt = n.new('GeometryNodeMeshCylinder')
    bolt.inputs['Vertices'].default_value = 6
    bolt.inputs['Radius'].default_value = .0055
    bolt.inputs['Depth'].default_value = .007
    mat = n.new('GeometryNodeSetMaterial')
    mat.inputs['Material'].default_value = brass
    links.new(bolt.outputs['Mesh'], mat.inputs['Geometry'])
    inst = n.new('GeometryNodeInstanceOnPoints')
    links.new(circle.outputs['Mesh'], inst.inputs['Points'])
    links.new(mat.outputs['Geometry'], inst.inputs['Instance'])
    links.new(inst.outputs['Instances'], out.inputs['Geometry'])
    for i, node in enumerate(n):
        node.location = ((i%4)*220, -(i//4)*240)
    fasteners.modifiers.new('Fastener count', 'NODES').node_group = group
    fasteners.location.z = .062

    floor_mat = material('Warm studio floor', (.23,.20,.16), 0,.65)
    mesh = bpy.data.meshes.new('Studio floor')
    mesh.from_pydata([(-200,-200,-.004),(200,-200,-.004),(200,200,-.004),(-200,200,-.004)],[],[(0,1,2,3)])
    floor = link(bpy.data.objects.new('Studio floor',mesh),floor_mat)
    for name, location, power, size in [('Key',(1,-2,2.5),180,2),('Fill',(-1,-.4,1.2),60,1.5),('Rim',(.4,1,1.8),150,1)]:
        data = bpy.data.lights.new(name,'AREA')
        data.energy, data.shape, data.size = power,'DISK',size
        o = link(bpy.data.objects.new(name,data))
        o.location = location
        aim(o,(0,0,.4))
    data = bpy.data.cameras.new('Product camera')
    cam = link(bpy.data.objects.new('Product camera',data))
    cam.location = (1.35,-2.0,1.15)
    cam.data.type, cam.data.ortho_scale = 'ORTHO',1.25
    aim(cam,(0,0,.43))
    scene.camera = cam
    scene.render.resolution_x = scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    bpy.context.view_layer.update()
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.region_3d.view_perspective = 'CAMERA'
    return {'scene':scene, 'camera':cam, 'lower':lower, 'upper':upper, 'head':head,
            'shade':shade, 'base':base, 'floor':floor, 'fasteners':fasteners}
