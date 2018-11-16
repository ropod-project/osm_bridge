import utm
from OBL.structs.wm.wm_entity import WMEntity
from OBL.structs.osm.node import Node
from OBL.structs.wm.point import Point

class Shape(WMEntity):

    global_origin = [0,0]
    local_origin = [0,0]
    coordinate_system = 'spherical'

    def __init__(self, nodes, *args, **kwargs):
        global_origin = kwargs.get("global_origin", self.global_origin)
        local_origin = kwargs.get("local_origin", self.local_origin)
        coordinate_system = kwargs.get("coordinate_system", self.coordinate_system)

        if isinstance(nodes, int):
            __,ways,__ = self.osm_adapter.get_osm_element_by_id(ids=[nodes], data_type='way')
            if len(ways) == 1:
                print(ways[0])
                nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=ways[0].nodes, data_type='node')

    
        self.points = []

        for node in nodes:
            self.points.append(Point(node)) 
