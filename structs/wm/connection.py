from structs.wm.wm_entity import WMEntity
from structs.wm.point import Point

class Connection(WMEntity):

    def __init__(self, connection_id, *args, **kwargs):      
        __,ways,__ = self.osm_adapter.get_osm_element_by_id(ids=[connection_id], data_type='way')
        
        self.point_ids = []

        if len(ways) == 1:
            self.id = ways[0].id

            for tag in ways[0].tags:
                setattr(self, tag.key, tag.value) 

            self.point_ids = ways[0].nodes
        else:
            self.logger.error("No connection found with given id {}".format(connection_id))  

    @property
    def points(self):
        points = []
        for point_id in self.point_ids:
            nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=[point_id], data_type='node')
            points.append(Point(nodes[0]))
        return points