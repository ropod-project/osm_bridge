from structs.wm.wm_entity import WMEntity
from structs.wm.wall import Wall
from structs.wm.room import Room
from structs.wm.corridor import Corridor
from structs.wm.connection import Connection

class Floor(WMEntity):

    def __init__(self, floor_ref, *args, **kwargs):      

        source = self._check_type(floor_ref)     
        if source == "id":      
            __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[floor_ref], data_type='relation')
        elif source == "ref":
            __,__,relations = self.osm_adapter.search_by_tag(data_type='relation',key='ref',value=floor_ref)
        elif source == "relation":
            relations = [floor_ref]

        # possible attributes
        # NOTE: attribute will have value only if its set by the mapper
        self.id = ''
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
            raise Exception("No floor found")

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
    def connections(self):
        if len(self._connection_ids) == 0 :
            return None
        connections = []
        __,connections_ways,__ = self.osm_adapter.get_osm_element_by_id(ids=self._connection_ids, data_type='way')
        for connection in connections_ways:
            connections.append(Connection(connection))
        return connections

    @property
    def rooms(self):
        if len(self._room_ids) == 0 :
            return None
        rooms = []
        __,__,room_relations = self.osm_adapter.get_osm_element_by_id(ids=self._room_ids, data_type='relation')
        for room in room_relations:
            rooms.append(Room(room))
        return rooms

    @property
    def corridors(self):
        if len(self._corridor_ids) == 0 :
            return None
        corridors = []
        __,__,corridor_relations = self.osm_adapter.get_osm_element_by_id(ids=self._corridor_ids, data_type='relation')
        for corridor in corridor_relations:
            corridors.append(Corridor(corridor))
        return corridors

    def room(self,ref):
        return Room(ref,scope_id=self.id, scope_role='room',scope_role_type='relation')

    def corridor(self,ref):
        return Corridor(ref,scope_id=self.id, scope_role='corridor',scope_role_type='relation')
