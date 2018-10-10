from structs.wm.wm_entity import WMEntity
from structs.wm.point import Point
from structs.wm.shape import Shape

class LocalArea(WMEntity):

    def __init__(self, local_area_id, *args, **kwargs):      
        __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[local_area_id], data_type='relation')
        
        self.geometry_id = None
        self.topology_id = None

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key, tag.value) 

            for member in relations[0].members:
                if member.role == 'geometry':
                    self.geometry_id = member.ref
                if member.role == 'topology':
                    self.topology_id = member.ref
        else:
            self.logger.error("No local area found with given id {}".format(door_id))  

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