from structs.wm.wm_entity import WMEntity
from structs.wm.feature import Feature
from structs.wm.point import Point
from structs.wm.shape import Shape
from structs.wm.side import Side

class Wall(WMEntity):

    def __init__(self, wall_id, *args, **kwargs):      
        __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[wall_id], data_type='relation')
        
        # possible attributes
        # NOTE: attirbute will have value only if its set by the mapper
        # Some attribute values will be available only after loading wall geometry
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
            self.logger.error("No wall found with specified id {}".format(wall_id))  

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
    def sides(self):
        sides = []
        for side_id in self._side_ids:
            sides.append(Side(side_id))
        return sides