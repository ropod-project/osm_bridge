import utm
from structs.wm.wm_entity import WMEntity

class Point(WMEntity):

    _global_origin = [0,0]
    _local_origin = [0,0]
    _coordinate_system = 'spherical'

    def __init__(self, osm_bridge_instance, point_id, *args, **kwargs):
        global_origin = kwargs.get("global_origin", self._global_origin)
        local_origin = kwargs.get("local_origin", self._local_origin)
        coordinate_system = kwargs.get("coordinate_system", self._coordinate_system)

        nodes = []
        if kwargs.get("osm_node") is not None:
            nodes.append(kwargs.get("osm_node"))
        else:
            nodes,__,__ = osm_bridge_instance.get_osm_element_by_id(ids=[point_id], data_type='node')
        
        if len(nodes) == 1:
            self.id = nodes[0].id
            if coordinate_system == 'spherical':
                self.lat = nodes[0].lat
                self.lon = nodes[0].lon
            elif coordinate_system == 'utm':
                temp = utm.from_latlon(nodes[0].lat, nodes[0].lon)
                self.x = temp[0] - global_origin[0]
                self.y = temp[1] - global_origin[1]  
        else:
            print("No point found with given id {}".format(point_id))  


class Shape(WMEntity):

    def __init__(self, osm_bridge_instance, shape_id):
        __,ways,__ = osm_bridge_instance.get_osm_element_by_id(ids=[shape_id], data_type='way')

        self.points = []
        
        if len(ways) == 1:
            self.id = ways[0].id
            for node in ways[0].nodes:
                self.points.append(Point(osm_bridge_instance, node))
        else:
            print("No shape found with given id {}".format(shape_id))  