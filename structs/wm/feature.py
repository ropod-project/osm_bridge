from structs.osm.node import Node
from structs.osm.tag import Tag

class Feature():

    def __init__(self, osm_bridge_instance, feature_id):        
        nodes,__,__ = osm_bridge_instance.get_osm_element_by_id(ids=[feature_id], data_type='node')
        
        if len(nodes) == 1:
            self.id = nodes[0].id
            self.lat = nodes[0].lat
            self.lon = nodes[0].lon

            for tag in nodes[0].tags:
                etattr(self, tag.key, tag.value) 
        else:
            print("No feature found with given id {}".format(feature_id))  

    def __eq__(self, other):
        if isinstance(other, (Feature)):
            return self.id == other.id

    def __repr__(self):
        return "<Feature id=%(id)s>" % {
            'id': self.id
        }

    def __getattr__(self, item):
        return None