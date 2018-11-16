import utm
from OBL.structs.wm.wm_entity import WMEntity
from OBL.structs.osm.node import Node
from OBL.structs.osm.tag import Tag


class Point(WMEntity):

    coordinate_system = 'spherical'

    def __init__(self, point_ref, *args, **kwargs):
        self.coordinate_system = kwargs.get("coordinate_system", self.coordinate_system)
        self.parent_id = ''

        source = self._check_type(point_ref)
        if source == "id":      
            nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=[point_ref], data_type='node')
        elif source == "node":
            nodes = [point_ref]

        if len(nodes) == 1:
            self.id = nodes[0].id
            self.lat = nodes[0].lat
            self.lon = nodes[0].lon
            self.x, self.y = self._convert_to_cartesian(nodes[0].lat, nodes[0].lon)
        else:
            self.logger.error("No node found with given ref {}".format(point_ref))  
            raise Exception("No point found")
        
