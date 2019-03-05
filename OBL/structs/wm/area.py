from OBL.structs.wm.wm_entity import WMEntity
from OBL.structs.wm.feature import Feature
from OBL.structs.wm.point import Point
from OBL.structs.wm.shape import Shape
from OBL.structs.wm.wall import Wall
from OBL.structs.wm.pillar import Pillar
from OBL.structs.wm.door import Door
from OBL.structs.wm.local_area import LocalArea
from OBL.structs.wm.connection import Connection


class Area(WMEntity):

    def __init__(self, area_ref, *args, **kwargs):

        super(Area, self).__init__(area_ref, *args, **kwargs)
        source = self._check_type(area_ref)
        if source == "id":
            __, __, relations = self.osm_adapter.get_osm_element_by_id(
                ids=[area_ref], data_type='relation')
        elif source == "ref":
            __, __, relations = self.osm_adapter.search_by_tag(
                data_type='relation', key='ref', value=area_ref, **kwargs)
        elif source == "relation":
            relations = [area_ref]
        elif isinstance(area_ref, Point):
            __, __, relations = self.osm_adapter.get_parent(
                id=area_ref.id, data_type='node', parent_child_role='topology')

        # possible attributes
        # NOTE: attirbute will have value only if its set by the mapper
        # Some attribute values will be available only after loading related
        # property of the area
        self.id = ''
        self.surface = ''
        self.surface_smoothness = ''
        self.internet = ''
        self.level = ''
        self.ref = ''
        self.name = ''

        # private attributes
        self._geometry_id = None
        self._topology_id = None
        self._connection_ids = []
        self._recovery_connection_ids = []
        self._feature_ids = []
        self._wall_ids = []
        self._door_ids = []
        self._local_area_ids = []
        self._pillar_ids = []

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key.replace("-", "_"), tag.value)

            area_type = ['room', 'corridor', 'elevator',
                         'stairs', 'junction', 'area']
            if not (self.type in area_type):
                raise Exception("Invalid relation")

            for member in relations[0].members:
                if member.role == 'wall':
                    self._wall_ids.append(member.ref)
                if member.role == 'pillar':
                    self._pillar_ids.append(member.ref)
                if member.role == 'door':
                    self._door_ids.append(member.ref)
                if member.role == 'feature':
                    self._feature_ids.append(member.ref)
                if member.role == 'local_connection':
                    self._connection_ids.append(member.ref)
                if member.role == 'recovery_connection':
                    self._recovery_connection_ids.append(member.ref)
                if member.role == 'geometry':
                    self._geometry_id = member.ref
                if member.role == 'topology':
                    self._topology_id = member.ref
                if member.role == 'local_area':
                    self._local_area_ids.append(member.ref)
        else:
            self.logger.error(
                "No area found with specified ref {}".format(area_ref))
            raise Exception(
                "No area found with specified ref {}".format(area_ref))

    @property
    def geometry_id(self):
        return self._geometry_id

    @property
    def topology_id(self):
        return self._topology_id

    @property
    def geometry(self):
        __, geometries, __ = self.osm_adapter.get_osm_element_by_id(
            ids=[self._geometry_id], data_type='way')

        for tag in geometries[0].tags:
            setattr(self, tag.key, tag.value)

        nodes, __, __ = self.osm_adapter.get_osm_element_by_id(
            ids=geometries[0].nodes, data_type='node')
        return Shape(nodes)

    @property
    def topology(self):
        topological_nodes, __, __ = self.osm_adapter.get_osm_element_by_id(
            ids=[self._topology_id], data_type='node')
        return Point(topological_nodes[0])

    @property
    def walls(self):
        if len(self._wall_ids) == 0:
            return None
        walls = []
        __, __, wall_relations = self.osm_adapter.get_osm_element_by_id(
            ids=self._wall_ids, data_type='relation')
        for wall_id in wall_relations:
            walls.append(Wall(wall_id))
        return walls

    @property
    def doors(self):
        if len(self._door_ids) == 0:
            return None
        doors = []
        __, __, door_relations = self.osm_adapter.get_osm_element_by_id(
            ids=self._door_ids, data_type='relation')
        for door in door_relations:
            doors.append(Door(door))
        return doors

    @property
    def pillars(self):
        if len(self._pillar_ids) == 0:
            return None
        pillars = []
        __, __, pillar_relations = self.osm_adapter.get_osm_element_by_id(
            ids=self._pillar_ids, data_type='relation')
        for pillar in pillar_relations:
            pillars.append(Pillar(pillar))
        return pillars

    @property
    def features(self):
        if len(self._feature_ids) == 0:
            return None
        features = []
        feature_nodes, __, __ = self.osm_adapter.get_osm_element_by_id(
            ids=self._feature_ids, data_type='node')
        for feature in feature_nodes:
            features.append(Feature(feature))
        return features

    @property
    def connections(self):
        if len(self._connection_ids) == 0:
            return None
        connections = []
        __, connections_ways, __ = self.osm_adapter.get_osm_element_by_id(
            ids=self._connection_ids, data_type='way')
        for connection in connections_ways:
            connections.append(Connection(connection))
        return connections

    @property
    def recovery_connections(self):
        if len(self._recovery_connection_ids) == 0:
            return None
        recovery_connections = []
        __, recovery_connections_ways, __ = self.osm_adapter.get_osm_element_by_id(
            ids=self._recovery_connection_ids, data_type='way')
        for recovery_connection in recovery_connections_ways:
            recovery_connections.append(Connection(recovery_connection))
        return recovery_connections

    @property
    def local_areas(self):
        if len(self._local_area_ids) == 0:
            return None
        local_areas = []
        __, __, local_area_relations = self.osm_adapter.get_osm_element_by_id(
            ids=self._local_area_ids, data_type='relation')
        for local_area in local_area_relations:
            local_areas.append(LocalArea(local_area))
        return local_areas

    def local_area(self, ref):
        return LocalArea(ref, scope_id=self.id, scope_role='local_area', scope_role_type='relation')

    def __repr__(self):
        return "<" + self.__class__.__name__ + " id=%(id)s type=%(type)s>" % {
            'id': self.id, 'type': self.type
        }

    def get_local_area_ids(self):
        return self._local_area_ids
