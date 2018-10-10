from structs.wm.wm_entity import WMEntity
from structs.wm.feature import Feature
from structs.wm.point import Point
from structs.wm.shape import Shape
from structs.wm.side import Side

class Wall(WMEntity):

    def __init__(self, wall_id, *args, **kwargs):      
        __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[wall_id], data_type='relation')
        
        self.side_ids = []
        self.geometry_id = None

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key, tag.value) 

            for member in relations[0].members:
                if member.role == 'side':
                    self.side_ids.append(member.ref)
                if member.role == 'geometry':
                    self.geometry_id = member.ref
        else:
            self.logger.error("No wall found with specified id {}".format(wall_id))  

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
    def sides(self):
        sides = []
        for side_id in self.side_ids:
            sides.append(Side(side_id))
        return sides