from OBL.structs.wm.wm_entity import WMEntity
from OBL.structs.wm.point import Point
from OBL.structs.wm.shape import Shape
from OBL.structs.wm.side import Side

class Door(WMEntity):

    def __init__(self, door_ref, *args, **kwargs):      
        super(Door, self).__init__(door_ref, *args, **kwargs)
        source = self._check_type(door_ref)     
        if source == "id":      
            __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[door_ref], data_type='relation')
        elif source == "ref":
            __,__,relations = self.osm_adapter.search_by_tag(data_type='relation',key='ref',value=door_ref)
        elif source == "relation":
            relations = [door_ref]
        elif isinstance(door_ref, Point) :
            __,__,relations = self.osm_adapter.get_parent(id=door_ref.id, data_type='node', parent_child_role='topology')
        
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
            raise Exception("No door found with given ref {}".format(door_ref))

    @property
    def geometry_id(self) :
        return self._geometry_id

    @property
    def topology_id(self) :
        return self._topology_id

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
        p = Point(topological_nodes[0])
        p.parent_id = self.id
#        p.parent_type = 'Area'
        return p

    @property
    def sides(self):
        if len(self._side_ids) == 0 :
            return None
        sides = []
        for side_id in self._side_ids:
            sides.append(Side(side_id))
        return sides
