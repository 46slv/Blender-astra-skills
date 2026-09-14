"""GN shelf with derived spacing, live dimensions, and unrealized board/post instances.

build() adds to the current scene. No global reset/save. Four semantic controls;
GN derives levels, post centers and spacing. Units: meters. Tested Blender 5.2.
"""
import bpy
from gn import socket, set_input


def build(name='Parametric Shelf'):
    obj = bpy.data.objects.new(name,bpy.data.meshes.new(name+' host'))
    bpy.context.scene.collection.objects.link(obj)
    group = bpy.data.node_groups.new(name+' design','GeometryNodeTree')
    for label,typ,default,minimum,maximum in [('Width','NodeSocketFloat',1.2,.3,3),
                                             ('Depth','NodeSocketFloat',.38,.15,1),
                                             ('Height','NodeSocketFloat',1.5,.4,3),
                                             ('Levels','NodeSocketInt',5,2,12)]:
        s=group.interface.new_socket(name=label,in_out='INPUT',socket_type=typ)
        s.default_value,s.min_value,s.max_value=default,minimum,maximum
    group.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
    nodes, links = group.nodes, group.links
    def node(typ,label):
        n=nodes.new(typ)
        n.label=label
        return n
    def wire(a,output,b,input):
        links.new(socket(a.outputs,name=output),socket(b.inputs,name=input))
    def math(op,a,b,label):
        n=node('ShaderNodeMath',label)
        n.operation=op
        if isinstance(a,tuple):
            links.new(socket(a[0].outputs,name=a[1]),n.inputs[0])
        else:
            n.inputs[0].default_value=a
        n.inputs[1].default_value=b
        return n
    inp,out=node('NodeGroupInput','Design controls'),node('NodeGroupOutput','Editable instances')
    join=node('GeometryNodeJoinGeometry','Boards + uprights')
    wire(join,'Geometry',out,'Geometry')
    top=math('SUBTRACT',(inp,'Height'),.065,'Top shelf follows overall height')
    endpoint=node('ShaderNodeCombineXYZ','Upper level')
    wire(top,'Value',endpoint,'Z')
    points=node('GeometryNodeMeshLine','Evenly spaced shelf levels')
    points.mode='END_POINTS'
    points.inputs['Start Location'].default_value=(0,0,.09)
    wire(endpoint,'Vector',points,'Offset')  # Actual RNA identifier in END_POINTS mode.
    wire(inp,'Levels',points,'Count')
    panel_size=node('ShaderNodeCombineXYZ','Board dimensions')
    wire(inp,'Width',panel_size,'X'); wire(inp,'Depth',panel_size,'Y')
    panel_size.inputs['Z'].default_value=.035
    panel=node('GeometryNodeMeshCube','Board source')
    wire(panel_size,'Vector',panel,'Size')
    boardmat=bpy.data.materials.new(name+' oak')
    boardmat.diffuse_color=(.43,.22,.08,1)
    apply_mat=node('GeometryNodeSetMaterial','Oak shelves')
    apply_mat.inputs['Material'].default_value=boardmat
    wire(panel,'Mesh',apply_mat,'Geometry')
    boards=node('GeometryNodeInstanceOnPoints','Instance boards, retain editability')
    wire(points,'Mesh',boards,'Points'); wire(apply_mat,'Geometry',boards,'Instance')
    wire(boards,'Instances',join,'Geometry')
    centers=node('GeometryNodeMeshGrid','Four corner posts')
    centers.inputs['Vertices X'].default_value=centers.inputs['Vertices Y'].default_value=2
    wx=math('SUBTRACT',(inp,'Width'),.045,'Post inset X')
    dy=math('SUBTRACT',(inp,'Depth'),.045,'Post inset Y')
    wire(wx,'Value',centers,'Size X'); wire(dy,'Value',centers,'Size Y')
    half=math('MULTIPLY',(inp,'Height'),.5,'Base remains on floor')
    translation=node('ShaderNodeCombineXYZ','Post centers')
    wire(half,'Value',translation,'Z')
    move=node('GeometryNodeTransform','Center posts vertically')
    wire(centers,'Mesh',move,'Geometry'); wire(translation,'Vector',move,'Translation')
    post_size=node('ShaderNodeCombineXYZ','Upright dimensions')
    post_size.inputs['X'].default_value=post_size.inputs['Y'].default_value=.045
    wire(inp,'Height',post_size,'Z')
    post=node('GeometryNodeMeshCube','Upright source')
    wire(post_size,'Vector',post,'Size')
    metal=bpy.data.materials.new(name+' graphite')
    metal.diffuse_color=(.04,.06,.06,1)
    postmat=node('GeometryNodeSetMaterial','Graphite uprights')
    postmat.inputs['Material'].default_value=metal
    wire(post,'Mesh',postmat,'Geometry')
    posts=node('GeometryNodeInstanceOnPoints','Four upright instances')
    wire(move,'Geometry',posts,'Points'); wire(postmat,'Geometry',posts,'Instance')
    wire(posts,'Instances',join,'Geometry')
    for i,n in enumerate(nodes):
        n.location=((i%6)*210,-(i//6)*250)
    mod=obj.modifiers.new('Shelf dimensions','NODES')
    mod.node_group=group
    for label,value in [('Width',1.2),('Depth',.38),('Height',1.5),('Levels',5)]:
        set_input(mod,label,value)
    return obj
