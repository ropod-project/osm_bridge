from OBL.structs.wm.wm_entity import WMEntity
from OBL.structs.wm.wall import Wall
from OBL.structs.wm.room import Room
from OBL.structs.wm.corridor import Corridor
from OBL.structs.wm.area import Area
from OBL.structs.wm.point import Point
from OBL.structs.wm.connection import Connection


class Floor(WMEntity):

    def __init__(self, floor_ref, *args, **kwargs):

        super(Floor, self).__init__(floor_ref, *args, **kwargs)
        source = self._check_type(floor_ref)
        if source == "id":
            __, __, relations = self.osm_adapter.get_osm_element_by_id(
                ids=[floor_ref], data_type='relation')
        elif source == "ref":
            __, __, relations = self.osm_adapter.search_by_tag(
                data_type='relation', key='ref', value=floor_ref, **kwargs)
        elif source == "relation":
            relations = [floor_ref]

        # possible attributes
        # NOTE: attribute will have value only if its set by the mapper
        self.id = ''
        self.ref = ''
        self.name = ''
        self.height = ''
        self._member_ids = {}

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
                if member.role in self._member_ids:
                    self._member_ids[member.role].append(member.ref)
                else:
                    self._member_ids[member.role] = [member.ref]
        else:
            self.logger.error(
                "No floor found with given ref {}".format(floor_ref))
            raise Exception("No floor found")

    @property
    def connection_ids(self):
        return self._member_ids['global_connection'] if 'global_connection' in self._member_ids else []

    @property
    def walls(self):
        if 'wall' not in self._member_ids or len(self._member_ids['wall']) == 0:
            return None
        walls = []
        __, __, wall_relations = self.osm_adapter.get_osm_element_by_id(
            ids=self._member_ids['wall'], data_type='relation')
        for wall_id in wall_relations:
            walls.append(Wall(wall_id))
        return walls

    @property
    def connections(self):
        if 'global_connection' not in self._member_ids or len(self._member_ids['global_connection']) == 0:
            return None
        connections = []
        __, connections_ways, __ = self.osm_adapter.get_osm_element_by_id(
            ids=self._member_ids['global_connection'], data_type='way')
        for connection in connections_ways:
            connections.append(Connection(connection))
        return connections

    @property
    def rooms(self):
        if 'room' not in self._member_ids or len(self._member_ids['room']) == 0:
            return None
        rooms = []
        __, __, room_relations = self.osm_adapter.get_osm_element_by_id(
            ids=self._member_ids['room'], data_type='relation')
        for room in room_relations:
            rooms.append(Room(room))
        return rooms

    @property
    def corridors(self):
        if 'corridor' not in self._member_ids or len(self._member_ids['corridor']) == 0:
            return None
        corridors = []
        __, __, corridor_relations = self.osm_adapter.get_osm_element_by_id(
            ids=self._member_ids['corridor'], data_type='relation')
        for corridor in corridor_relations:
            corridors.append(Corridor(corridor))
        return corridors

    @property
    def areas(self):
        if 'area' not in self._member_ids or len(self._member_ids['area']) == 0:
            return None
        areas = []
        __, __, area_relations = self.osm_adapter.get_osm_element_by_id(
            ids=self._member_ids['area'], data_type='relation')
        for area in area_relations:
            areas.append(Area(area))
        return areas

    @property
    def wlans(self):
        if 'wlan' not in self._member_ids or len(self._member_ids['wlan']) == 0:
            return None
        wlans = []
        nodes, __, __ = self.osm_adapter.get_osm_element_by_id(
            ids=self._member_ids['wlan'], data_type='node')
        for node in nodes:
            wlans.append(Point(node))
        return wlans

    def room(self, ref):
        return Room(ref, scope_id=self.id, scope_role='room', scope_role_type='relation')

    def corridor(self, ref):
        return Corridor(ref, scope_id=self.id, scope_role='corridor', scope_role_type='relation')
