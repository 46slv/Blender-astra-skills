"""Small GN helpers: inspect first, address sockets unambiguously, read back."""
import bpy


def socket(sockets, name=None, identifier=None):
    candidates = [s for s in sockets if s.enabled and not getattr(s,'is_unavailable',False)
                  and (s.identifier == identifier if identifier is not None else s.name == name)]
    if len(candidates) != 1:
        raise ValueError(f'Ambiguous/missing socket: {name or identifier}. '
                         f'Available: {[(s.name,s.identifier,s.enabled) for s in sockets]}')
    return candidates[0]


def input_socket(modifier, name):
    sockets = [s for s in modifier.node_group.interface.items_tree
               if s.item_type == 'SOCKET' and s.in_out == 'INPUT' and s.name == name]
    if len(sockets) != 1:
        raise ValueError(f'Expected one interface input named {name}; got {len(sockets)}')
    return sockets[0]


def set_input(modifier, name, value):
    """Set a literal value, switching off attribute mode for this input."""
    s = input_socket(modifier,name)
    if hasattr(modifier, 'properties'):  # Blender 5.2: the value is typed RNA.
        prop = getattr(modifier.properties.inputs,s.identifier)
        if hasattr(prop,'type') and prop.type == 'ATTRIBUTE':
            prop.type = 'VALUE'
        prop.value = value
        readback = prop.value
    else:  # Older API; probe/evaluate on that Blender before claiming support.
        modifier[s.identifier] = value
        readback = modifier[s.identifier]
    modifier.id_data.update_tag()
    bpy.context.view_layer.update()
    return readback


def graph(group):
    """Focused graph readback: endpoints include identifiers, not just labels."""
    return {'name':group.name,
            'nodes':[{'name':n.name,'type':n.bl_idname,'muted':n.mute,
                      'inputs':[(s.name,s.identifier,s.enabled,s.is_linked) for s in n.inputs]}
                     for n in group.nodes],
            'links':[(l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier)
                     for l in group.links]}
