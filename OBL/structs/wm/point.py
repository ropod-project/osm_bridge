import utm
from OBL.structs.wm.wm_entity import WMEntity
from OBL.structs.osm.node import Node
from OBL.structs.osm.tag import Tag


class Point(WMEntity):

    coordinate_system = 'spherical'

    def __init__(self, node, *args, **kwargs):
        self.coordinate_system = kwargs.get("coordinate_system", self.coordinate_system)
        self.parent_id = ''
        self.id = node.id
        self.lat = node.lat
        self.lon = node.lon
        self.x, self.y = self._convert_to_cartesian(node.lat, node.lon)
