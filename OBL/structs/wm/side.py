from OBL.structs.wm.wm_entity import WMEntity
from OBL.structs.wm.feature import Feature
from OBL.structs.wm.point import Point

class Side(WMEntity):

    def __init__(self, side_ref, *args, **kwargs):     

        super(Side, self).__init__(side_ref, *args, **kwargs)
        source = self._check_type(side_ref)     
        if source == "id":      
            __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[side_ref], data_type='relation')
        elif source == "ref":
            __,__,relations = self.osm_adapter.search_by_tag(data_type='relation',key='ref',value=side_ref)
        elif source == "relation":
            relations = [side_ref]
        
        # no mandatory attributes, but it can still have some tags added by user as attributes

        # private attributes
        self.id = ''
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
            self.logger.error("No side found with specified ref {}".format(side_ref))  
            raise Exception("No side found with specified ref {}".format(side_ref))

    @property
    def corners(self):
        if len(self._corner_ids) == 0 :
            return None
        corners = []
        corner_nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=self._corner_ids, data_type='node')
        for corner_node in corner_nodes:
            corners.append(Point(corner))
        return corners

    @property
    def features(self):
        if len(self._feature_ids) == 0 :
            return None
        features = []
        feature_nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=self._feature_ids, data_type='node')
        for feature in feature_nodes:
            features.append(Feature(feature))
        return features
