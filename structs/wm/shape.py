import utm
from structs.wm.wm_entity import WMEntity
from structs.osm.node import Node
from structs.wm.point import Point

class Shape(WMEntity):

    global_origin = [0,0]
    local_origin = [0,0]
    coordinate_system = 'spherical'

    def __init__(self, nodes, *args, **kwargs):
        global_origin = kwargs.get("global_origin", self.global_origin)
        local_origin = kwargs.get("local_origin", self.local_origin)
        coordinate_system = kwargs.get("coordinate_system", self.coordinate_system)
    
        self.points = []

        for node in nodes:
            self.points.append(Point(node)) 