from structs.wm.wm_entity import WMEntity
from structs.wm.feature import Feature
from structs.wm.point import Point
from structs.wm.shape import Shape
from structs.wm.wall import Wall
from structs.wm.door import Door
from structs.wm.local_area import LocalArea
from structs.wm.connection import Connection

class Elevator(WMEntity):

    def __init__(self, elevator_ref, *args, **kwargs):      
        source = self._check_type(elevator_ref)     
        if source == "id":      
            __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[elevator_ref], data_type='relation')
        elif source == "ref":
            __,__,relations = self.osm_adapter.search_by_tag(data_type='relation',key='ref',value=elevator_ref)
        elif source == "relation":
            relations = [elevator_ref]

        # possible attributes
        # NOTE: attirbute will have value only if its set by the mapper
        self.id = ''
        self.levels = '' # available only after loading geometry or topology
        self.ref = ''

        # private attributes
        self._geometry_id = None
        self._topology_id = None
        self._connection_ids = []
        self._feature_ids = []
        self._wall_ids = []
        self._door_ids = []
        self._local_area_ids = []

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key.replace("-", "_"), tag.value) 

            for member in relations[0].members:
                if member.role == 'wall':
                    self._wall_ids.append(member.ref)
                if member.role == 'door':
                    self._door_ids.append(member.ref)
                if member.role == 'feature':
                    self._feature_ids.append(member.ref)
                if member.role == 'local_connection':
                    self._connection_ids.append(member.ref)
                if member.role == 'geometry':
                    self._geometry_id = member.ref
                if member.role == 'topology':
                    self._topology_id = member.ref
                if member.role == 'local_area':
                    self._local_area_ids.append(member.ref)
        else:
            self.logger.error("No  elevator found with specified id {}".format(elevator_ref))  
            raise Exception("No elevator found")

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

        for tag in topological_nodes[0].tags:
            setattr(self, tag.key, tag.value) 

        return Point(topological_nodes[0])

    @property
    def walls(self):
        if len(self._wall_ids) == 0 :
            return None
        walls = []
        __,__,wall_relations = self.osm_adapter.get_osm_element_by_id(ids=self._wall_ids, data_type='relation')
        for wall_id in wall_relations:
            walls.append(Wall(wall_id))
        return walls

    @property
    def doors(self):
        if len(self._door_ids) == 0 :
            return None
        doors = []
        __,__,door_relations = self.osm_adapter.get_osm_element_by_id(ids=self._door_ids, data_type='relation')
        for door in door_relations :
            doors.append(Door(door))
        return doors

    @property
    def features(self):
        if len(self._feature_ids) == 0 :
            return None
        features = []
        feature_nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=self._feature_ids, data_type='node')
        for feature in feature_nodes:
            features.append(Feature(feature))
        return features

    @property
    def connections(self):
        if len(self._connection_ids) == 0 :
            return None
        connections = []
        __,connections_ways,__ = self.osm_adapter.get_osm_element_by_id(ids=self._connection_ids, data_type='way')
        for connection in connections_ways:
            connections.append(Connection(connection))
        return connections

    @property
    def local_areas(self):
        if len(self._local_area_ids) == 0 :
            return None
        local_areas = []
        __,__,local_area_relations = self.osm_adapter.get_osm_element_by_id(ids=self._local_area_ids, data_type='relation')
        for local_area in local_area_relations :
            local_areas.append(LocalArea(local_area))
        return local_areas

    def local_area(self, ref):
        return LocalArea(ref,scope_id=self.id, scope_role='local_area',scope_role_type='relation')
