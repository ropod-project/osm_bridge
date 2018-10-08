from structs.wm.wm_entity import WMEntity
from structs.wm.feature import Feature
from structs.wm.geometry import Point

class Side(WMEntity):

    def __init__(self, osm_bridge_instance, side_id, *args, **kwargs):
        self.osm_bridge = osm_bridge_instance        
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
            print("No side found with given id {}".format(side_id))  

    @property
    def corners(self):
        corners = []
        for corner_id in corner_ids:
            corners.append(Point(self.osm_bridge, corner_id))
        return corners

    @property
    def features(self):
        features = []
        for feature_id in feature_ids:
            features.append(Feature(self.osm_bridge,feature_id))
        return features