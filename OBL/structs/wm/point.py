import utm
from OBL.structs.wm.wm_entity import WMEntity
from OBL.structs.osm.node import Node
from OBL.structs.osm.tag import Tag


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
