from structs.wm.wm_entity import WMEntity
from structs.wm.point import Point

class Feature(WMEntity):

    def __init__(self, feature_id):        
        nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=[feature_id], data_type='node')
        
        if len(nodes) == 1:
            self.id = nodes[0].id

            for tag in nodes[0].tags:
                setattr(self, tag.key, tag.value) 

            self.point = Point(nodes[0])
        else:
            self.logger.error("No feature found with specified id {}".format(feature_id))  