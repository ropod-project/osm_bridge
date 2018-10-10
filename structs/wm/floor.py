from structs.wm.wm_entity import WMEntity
from structs.wm.wall import Wall
from structs.wm.door import Door
from structs.wm.room import Room
from structs.wm.corridor import Corridor
from structs.wm.connection import Connection

class Floor(WMEntity):

    def __init__(self, floor_id, *args, **kwargs):      
        __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[floor_id], data_type='relation')
        
        self.connection_ids = []
        self.wall_ids = []
        self.room_ids = []
        self.corridor_ids = []

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key, tag.value) 

            for member in relations[0].members:
                if member.role == 'wall':
                    self.wall_ids.append(member.ref)
                if member.role == 'room':
                    self.room_ids.append(member.ref)
                if member.role == 'corridor':
                    self.corridor_ids.append(member.ref)
                if member.role == 'global_connection':
                    self.connection_ids.append(member.ref)
        else:
            self.logger.error("No floor found with given id {}".format(floor_id))  

    @property
    def walls(self):
        walls = []
        for wall_id in self.wall_ids:
            walls.append(Wall(wall_id))
        return walls

    @property
    def connections(self):
        connections = []
        for connection_id in self.connection_ids:
            connections.append(Connection(connection_id))
        return connections

    @property
    def rooms(self):
        rooms = []
        for room_id in self.room_ids:
            rooms.append(Room(room_id))
        return rooms

    @property
    def corridors(self):
        corridors = []
        for corridor_id in self.corridor_ids:
            corridors.append(Room(corridor_id))
        return corridors