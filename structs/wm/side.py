from structs.wm.wm_entity import WMEntity
from structs.wm.feature import Feature
from structs.wm.geometry import Point

class Side(WMEntity):

    def __init__(self, side_id, *args, **kwargs):     
        __,__,relations = self.osm_bridge.get_osm_element_by_id(ids=[side_id], data_type='relation')
        
        self.corner_ids = []
        self.feature_ids = []

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key, tag.value) 

            for member in relations[0].members:
                if member.role == 'corner':
                    self.corner_ids.append(member.ref)
                if member.role == 'feature':
                    self.feature_ids.append(member.ref)
        else:
            self.logger("No side found with specified id {}".format(side_id))  

    @property
    def corners(self):
        corners = []
        corner_nodes,__,__ = self.osm_bridge.get_osm_element_by_id(ids=self.corner_ids, data_type='node')
        for corner_node in corner_nodes:
            corners.append(Point(corner))
        return corners

    @property
    def features(self):
        features = []
        for feature_id in feature_ids:
            features.append(Feature(feature_id))
        return features