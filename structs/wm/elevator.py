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

        if self._is_osm_id(elevator_ref):      
            __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[elevator_ref], data_type='relation')
        else:
            __,__,relations = self.osm_adapter.search_by_tag(data_type='relation',key='ref',value=elevator_ref)

        # possible attributes
        # NOTE: attirbute will have value only if its set by the mapper
        self.levels = '' # available only after loading geometry or topology

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
        else:
            self.logger.error("No  elevator found with specified id {}".format(elevator_ref))  

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

        for tag in topological_nodes[0].tags:
            setattr(self, tag.key, tag.value) 

        return Point(topological_nodes[0])

    @property
    def walls(self):
        walls = []
        for wall_id in self._wall_ids:
            walls.append(Wall(wall_id))
        return walls

    @property
    def doors(self):
        doors = []
        for door_id in self._door_ids:
            doors.append(Door(door_id))
        return doors

    @property
    def features(self):
        features = []
        for feature_id in self._feature_ids:
            features.append(Feature(feature_id))
        return features

    @property
    def connections(self):
        connections = []
        for connection_id in self._connection_ids:
            connections.append(Connection(connection_id))
        return connections

    @property
    def local_areas(self):
        local_areas = []
        for local_area_id in self._local_area_ids:
            local_areas.append(LocalArea(local_area_id))
        return local_areas