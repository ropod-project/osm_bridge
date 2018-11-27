import utm
from OBL.structs.wm.wm_entity import WMEntity
from OBL.structs.osm.node import Node
from OBL.structs.osm.tag import Tag


class Point(WMEntity):

    coordinate_system = 'spherical'
    _parent_type = None

    def __init__(self, point_ref, *args, **kwargs):
        super(Point, self).__init__(point_ref, *args, **kwargs)
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
            raise Exception("No node found with given ref {}".format(point_ref))
        
    @property
    def parent_type(self) :
        if self._parent_type == None :
            self._assign_parent_attributes()
        return self._parent_type

    def _assign_parent_attributes(self) :
        __,__,relations = self.osm_adapter.get_parent(id=self.id, data_type='node', parent_child_role='topology')
        if len(relations) > 0 :
            for tag in relations[0].tags :
                if tag.key == "type" :
                    self._parent_type = tag.value
                    break

