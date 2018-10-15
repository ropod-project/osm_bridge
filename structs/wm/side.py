from structs.wm.wm_entity import WMEntity
from structs.wm.feature import Feature
from structs.wm.point import Point

class Side(WMEntity):

    def __init__(self, side_id, *args, **kwargs):     
        __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[side_id], data_type='relation')
        
        # no mandatory attributes, but it can still have some tags added by user as attributes

        # private attributes
        self._corner_ids = []
        self._feature_ids = []

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key, tag.value) 

            for member in relations[0].members:
                if member.role == 'corner':
                    self._corner_ids.append(member.ref)
                if member.role == 'feature':
                    self._feature_ids.append(member.ref)
        else:
            self.logger.error("No side found with specified id {}".format(side_id))  

    @property
    def corners(self):
        corners = []
        corner_nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=self._corner_ids, data_type='node')
        for corner_node in corner_nodes:
            corners.append(Point(corner))
        return corners

    @property
    def features(self):
        features = []
        for feature_id in _feature_ids:
            features.append(Feature(feature_id))
        return features