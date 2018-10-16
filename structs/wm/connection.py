from structs.wm.wm_entity import WMEntity
from structs.wm.point import Point

class Connection(WMEntity):

    def __init__(self, connection_ref, *args, **kwargs):      
        
        if self._is_osm_id(connection_ref):      
            __,ways,__ = self.osm_adapter.get_osm_element_by_id(ids=[connection_ref], data_type='way')
        else:
            __,ways,__ = self.osm_adapter.search_by_tag(data_type='way',key='ref',value=connection_ref)
        
        # possible attributes
        self.highway = '' # type of connection eg. localway, footway etc.
        self.oneway = '' # yes/no
        self.lanes_forward = ''
        self.lanes_backward = ''
        self.lanes_forward_speed = ''
        self.lanes_backward_speed = '' 

        # private attributes
        self._point_ids = []

        if len(ways) == 1:
            self.id = ways[0].id

            for tag in ways[0].tags:
                setattr(self, tag.key.replace(":", "_"), tag.value) 

            self._point_ids = ways[0].nodes
        else:
            self.logger.error("No connection found with given id {}".format(connection_ref))  

    @property
    def points(self):
        points = []
        for point_id in self._point_ids:
            nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=[point_id], data_type='node')
            points.append(Point(nodes[0]))
        return points