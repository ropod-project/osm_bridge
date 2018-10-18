from structs.wm.wm_entity import WMEntity
from structs.wm.feature import Feature
from structs.wm.point import Point
from structs.wm.shape import Shape
from structs.wm.side import Side

class Door(WMEntity):

    def __init__(self, door_ref, *args, **kwargs):      

        if self._is_osm_id(door_ref):      
            __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[door_ref], data_type='relation')
        else:
            __,__,relations = self.osm_adapter.search_by_tag(data_type='relation',key='ref',value=door_ref)
        
        # possible attributes
        # NOTE: attirbute will have value only if its set by the mapper
        # Some attribute values will be available only after loading door geometry
        self.id = ''
        self.door = ''              # type of door - hinged, sliding etc.
        self.door_automatic = ''    # yes/no
        self.door_direction = ''    # inside/outside/both
        self.step_count = ''        # steps if any else 0
        self.double_doors = ''      # yes/no
        self.always_closed = ''     # yes/no
        self.level = ''


        # private attributes
        self._side_ids = []
        self._geometry_id = None
        self._topology_id = None

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key.replace("-", "_"), tag.value) 

            for member in relations[0].members:
                if member.role == 'side':
                    self._side_ids.append(member.ref)
                if member.role == 'geometry':
                    self._geometry_id = member.ref
                if member.role == 'topology':
                    self._topology_id = member.ref
        else:
            self.logger.error("No door found with given ref {}".format(door_ref))  
            raise Exception("No door found")

    @property
    def geometry(self):
        __,geometries,__ = self.osm_adapter.get_osm_element_by_id(ids=[self._geometry_id], data_type='way')

        for tag in geometries[0].tags:
            setattr(self, tag.key, tag.value) 

        nodes = []
        for node_id in geometries[0].nodes:
            temp_nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=[node_id], data_type='node')
            nodes.append(temp_nodes[0])
        return Shape(nodes)

    @property
    def topology(self):
        topological_nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=[self._topology_id], data_type='node')
        return Point(topological_nodes[0])

    @property
    def sides(self):
        sides = []
        for side_id in self._side_ids:
            sides.append(Side(side_id))
        return sides