from OBL.structs.wm.wm_entity import WMEntity
from OBL.structs.wm.shape import Shape
from OBL.structs.wm.side import Side


class Wall(WMEntity):

    def __init__(self, wall_ref, *args, **kwargs):

        super(Wall, self).__init__(wall_ref, *args, **kwargs)
        source = self._check_type(wall_ref)
        if source == "id":
            __, __, relations = self.osm_adapter.get_osm_element_by_id(
                ids=[wall_ref], data_type='relation')
        elif source == "ref":
            __, __, relations = self.osm_adapter.search_by_tag(
                data_type='relation', key='ref', value=wall_ref)
        elif source == "relation":
            relations = [wall_ref]

        # possible attributes
        # NOTE: attirbute will have value only if its set by the mapper
        # Some attribute values will be available only after loading wall
        # geometry
        self.id = ''
        self.height = ''
        self.min_height = ''  # height from ground by default 0
        self.level = ''

        # private attributes
        self._side_ids = []
        self._geometry_id = None

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key.replace("-", "_"), tag.value)

            for member in relations[0].members:
                if member.role == 'side':
                    self._side_ids.append(member.ref)
                if member.role == 'geometry':
                    self._geometry_id = member.ref
        else:
            self.logger.error(
                "No wall found with specified ref {}".format(wall_ref))
            raise Exception(
                "No wall found with specified ref {}".format(wall_ref))

    @property
    def geometry_id(self):
        return self._geometry_id

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
    def sides(self):
        if len(self._side_ids) == 0:
            return None
        sides = []
        __, __, side_relations = self.osm_adapter.get_osm_element_by_id(
            ids=self._side_ids, data_type='relation')
        for side in side_relations:
            sides.append(Side(side))
        return sides
