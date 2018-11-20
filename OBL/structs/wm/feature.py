from OBL.structs.wm.wm_entity import WMEntity
from OBL.structs.wm.point import Point

class Feature(WMEntity):

    def __init__(self, feature_ref):          
        super(Feature, self).__init__(feature_ref)
        source = self._check_type(feature_ref)     
        if source == "id":      
            nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=[feature_ref], data_type='node')
        elif source == "ref":
            nodes,__,__ = self.osm_adapter.search_by_tag(data_type='node',key='ref',value=feature_ref)
        elif source == "node":
            nodes = [feature_ref]

        # mandatory attributes
        self.id = ''
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
            raise Exception("No feature found")
