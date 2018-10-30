import utm
from structs.wm.wm_entity import WMEntity
from structs.osm.node import Node
from structs.osm.tag import Tag


class Point(WMEntity):

    global_origin = [0,0]
    local_origin = [0,0]
    coordinate_system = 'spherical'

    def __init__(self, node, *args, **kwargs):
        global_origin = kwargs.get("global_origin", self.global_origin)
        local_origin = kwargs.get("local_origin", self.local_origin)
        self.coordinate_system = kwargs.get("coordinate_system", self.coordinate_system)
        self.parent_id = ''
        self.id = node.id
        if self.coordinate_system == 'spherical':
            self.lat = node.lat
            self.lon = node.lon
        elif self.coordinate_system == 'cartesian':
            temp = utm.from_latlon(node.lat, node.lon)
            self.x = temp[0] - global_origin[0] - local_origin[0]
            self.y = temp[1] - global_origin[1] - local_origin[1]

    @property
    def parent(self):
        __,__,relations = self.osm_adapter.get_parent(self.id, data_type='node', parent_child_role='topology', role_type='', role='')
        
        if len(relations) > 0:
            for tag in relations[0].tags:
                if tag == Tag("type", "corridor") or tag == Tag("type", "junction"):
                    from structs.wm.corridor import Corridor
                    c = Corridor(relations[0])
                    self.parent_id = c.id
                    return c
                elif tag == Tag("type", "room"):
                    from structs.wm.room import Room
                    r = Room(relations[0])
                    self.parent_id = r.id
                    return r
                elif tag == Tag("type", "area"):
                    from structs.wm.area import Area
                    a = Area(relations[0])
                    self.parent_id = a.id
                    return a
                elif tag == Tag("type", "door"):
                    from structs.wm.door import Door
                    d = Door(relations[0])
                    self.parent_id = d.id
                    return d
                elif tag == Tag("type","local_area"):
                    from structs.wm.local_area import LocalArea
                    l = LocalArea(relations[0])
                    self.parent_id = l.id
                    return l
                elif tag == Tag("type","elevator"):
                    from structs.wm.elevator import Elevator
                    e = Elevator(relations[0])
                    self.parent_id = e.id
                    return e
                elif tag == Tag("type","stairs"):
                    from structs.wm.stairs import Stairs
                    s = Stairs(relations[0])
                    self.parent_id = s.id
                    return s
        return None
