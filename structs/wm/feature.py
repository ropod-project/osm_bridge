from structs.wm.wm_entity import WMEntity
from structs.wm.geometry import Point

class Feature(WMEntity):

    def __init__(self, osm_bridge_instance, feature_id):        
        nodes,__,__ = osm_bridge_instance.get_osm_element_by_id(ids=[feature_id], data_type='node')
        
        if len(nodes) == 1:
            self.id = nodes[0].id
            
            self.point = Point(osm_bridge_instance, self.id, osm_node=nodes[0])

            for tag in nodes[0].tags:
                setattr(self, tag.key, tag.value) 
        else:
            print("No feature found with given id {}".format(feature_id))  