from OBL.structs.wm.wm_entity import WMEntity
from OBL.structs.wm.feature import Feature
from OBL.structs.wm.point import Point
from OBL.structs.wm.shape import Shape

class Pillar(WMEntity):

    def __init__(self, pillar_ref, *args, **kwargs):      

        super(Pillar, self).__init__(pillar_ref, *args, **kwargs)
        source = self._check_type(pillar_ref)     
        if source == "id":      
            __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[pillar_ref], data_type='relation')
        elif source == "ref":
            __,__,relations = self.osm_adapter.search_by_tag(data_type='relation',key='ref',value=pillar_ref)
        elif source == "relation":
            relations = [pillar_ref]
        
        # possible attributes
        # NOTE: attirbute will have value only if its set by the mapper
        # Some attribute values will be available only after loading wall geometry
        self.id = ''
        self.height = ''
        self.min_height = ''  # height from ground by default 0
        self.level = ''

        # private attributes
        self._geometry_id = None

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key.replace("-", "_"), tag.value) 

            for member in relations[0].members:
                if member.role == 'geometry':
                    self._geometry_id = member.ref
        else:
            self.logger.error("No pillar found with specified ref {}".format(pillar_ref))  
            raise Exception("No pillar found with specified ref {}".format(pillar_ref))


    @property
    def geometry(self):
        __,geometries,__ = self.osm_adapter.get_osm_element_by_id(ids=[self._geometry_id], data_type='way')

        for tag in geometries[0].tags:
            setattr(self, tag.key, tag.value) 

        nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=geometries[0].nodes, data_type='node')
        return Shape(nodes)
