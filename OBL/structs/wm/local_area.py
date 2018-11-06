from OBL.structs.wm.wm_entity import WMEntity
from OBL.structs.wm.point import Point
from OBL.structs.wm.shape import Shape

class LocalArea(WMEntity):

    def __init__(self, local_area_ref, *args, **kwargs):      

        source = self._check_type(local_area_ref)     
        if source == "id":      
            __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[local_area_ref], data_type='relation')
        elif source == "ref":
            __,__,relations = self.osm_adapter.search_by_tag(data_type='relation',key='ref',value=local_area_ref)
        elif source == "relation":
            relations = [local_area_ref]
        elif isinstance(local_area_ref, Point) :
            __,__,relations = self.osm_adapter.get_parent(id=local_area_ref.id, data_type='node', parent_child_role='topology')
        
        # possible attributes
        # NOTE: attirbute will have value only if its set by the mapper
        # These attributes will be available only after fetching geometry
        self.id = ''
        self.behaviour = ''
        self.ref = ''

        # private attributes
        self._geometry_id = None
        self._topology_id = None

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key.replace("-", "_"), tag.value) 

            for member in relations[0].members:
                if member.role == 'geometry':
                    self._geometry_id = member.ref
                if member.role == 'topology':
                    self._topology_id = member.ref
        else:
            self.logger.error("No local area found with specified ref {}".format(local_area_ref))  
            raise Exception("No local area found")

    @property
    def geometry(self):
        __,geometries,__ = self.osm_adapter.get_osm_element_by_id(ids=[self._geometry_id], data_type='way')

        for tag in geometries[0].tags:
            setattr(self, tag.key, tag.value) 

        nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=geometries[0].nodes, data_type='node')
        return Shape(nodes)

    @property
    def topology(self):
        topological_nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=[self._topology_id], data_type='node')
        return Point(topological_nodes[0])
