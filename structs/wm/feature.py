from structs.wm.wm_entity import WMEntity
from structs.wm.point import Point

class Feature(WMEntity):

    def __init__(self, feature_ref):
          
        if self._is_osm_id(feature_ref):      
            nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=[feature_ref], data_type='node')
        else:
            nodes,__,__ = self.osm_adapter.search_by_tag(data_type='node',key='ref',value=feature_ref)

        # mandatory attributes
        self.height = ''
        self.width = ''
        self.length = ''
        
        if len(nodes) == 1:
            self.id = nodes[0].id

            for tag in nodes[0].tags:
                setattr(self, tag.key, tag.value) 

            self.point = Point(nodes[0])
        else:
            self.logger.error("No feature found with specified ref {}".format(feature_ref))  