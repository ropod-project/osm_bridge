from structs.wm.wm_entity import WMEntity
from structs.wm.wall import Wall
from structs.wm.room import Room
from structs.wm.corridor import Corridor
from structs.wm.connection import Connection

class Floor(WMEntity):

    def __init__(self, floor_ref, *args, **kwargs):      

        if self._is_osm_id(floor_ref):      
            __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[floor_ref], data_type='relation')
        else:
            __,__,relations = self.osm_adapter.search_by_tag(data_type='relation',key='ref',value=floor_ref)

        # possible attributes
        # NOTE: attribute will have value only if its set by the mapper
        self.ref = ''
        self.name = ''
        self.height = ''

        # private attributes
        self._connection_ids = []
        self._wall_ids = []
        self._room_ids = []
        self._corridor_ids = []

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key.replace("-", "_"), tag.value) 

            for member in relations[0].members:
                if member.role == 'wall':
                    self._wall_ids.append(member.ref)
                if member.role == 'room':
                    self._room_ids.append(member.ref)
                if member.role == 'corridor':
                    self._corridor_ids.append(member.ref)
                if member.role == 'global_connection':
                    self._connection_ids.append(member.ref)
        else:
            self.logger.error("No floor found with given ref {}".format(floor_ref))  

    @property
    def walls(self):
        walls = []
        for wall_id in self._wall_ids:
            walls.append(Wall(wall_id))
        return walls

    @property
    def connections(self):
        connections = []
        for connection_id in self._connection_ids:
            connections.append(Connection(connection_id))
        return connections

    @property
    def rooms(self):
        rooms = []
        for room_id in self._room_ids:
            rooms.append(Room(room_id))
        return rooms

    @property
    def corridors(self):
        corridors = []
        for corridor_id in self._corridor_ids:
            corridors.append(Corridor(corridor_id))
        return corridors