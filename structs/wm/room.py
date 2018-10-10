from structs.wm.wm_entity import WMEntity
from structs.wm.feature import Feature
from structs.wm.point import Point
from structs.wm.shape import Shape
from structs.wm.wall import Wall
from structs.wm.door import Door
from structs.wm.local_area import LocalArea
from structs.wm.connection import Connection

class Room(WMEntity):

    def __init__(self, room_id, *args, **kwargs):      
        __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[room_id], data_type='relation')
        
        self.geometry_id = None
        self.topology_id = None
        self.connection_ids = []
        self.feature_ids = []
        self.wall_ids = []
        self.door_ids = []
        self.local_area_ids = []

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key, tag.value) 

            for member in relations[0].members:
                if member.role == 'wall':
                    self.wall_ids.append(member.ref)
                if member.role == 'door':
                    self.door_ids.append(member.ref)
                if member.role == 'feature':
                    self.feature_ids.append(member.ref)
                if member.role == 'local_connection':
                    self.connection_ids.append(member.ref)
                if member.role == 'geometry':
                    self.geometry_id = member.ref
                if member.role == 'topology':
                    self.topology_id = member.ref
        else:
            self.logger.error("No room found with given id {}".format(room_id))  

    @property
    def geometry(self):
        __,geometries,__ = self.osm_adapter.get_osm_element_by_id(ids=[self.geometry_id], data_type='way')

        for tag in geometries[0].tags:
            setattr(self, tag.key, tag.value) 

        nodes = []
        for node_id in geometries[0].nodes:
            temp_nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=[node_id], data_type='node')
            nodes.append(temp_nodes[0])
        return Shape(nodes)

    @property
    def topology(self):
        topological_nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=[self.topology_id], data_type='node')
        return Point(topological_nodes[0])

    @property
    def walls(self):
        walls = []
        for wall_id in self.wall_ids:
            walls.append(Wall(wall_id))
        return walls

    @property
    def doors(self):
        doors = []
        for door_id in self.door_ids:
            doors.append(Door(door_id))
        return doors

    @property
    def features(self):
        features = []
        for feature_id in self.feature_ids:
            features.append(Feature(feature_id))
        return features

    @property
    def connections(self):
        connections = []
        for connection_id in self.connection_ids:
            connections.append(Connection(connection_id))
        return connections

    @property
    def local_areas(self):
        local_areas = []
        for local_area_id in self.local_area_ids:
            local_areas.append(LocalArea(local_area_id))
        return local_areas