from structs.osm.node import Node
from structs.osm.tag import Tag
from structs.osm.way import Way
from structs.osm.relation import Relation

class WMEntity():

    def __init__(self, osm_bridge_instance, entity_id):        
        pass

    def __eq__(self, other):
        if isinstance(other, (WMEntity)):
            return self.id == other.id

    def __repr__(self):
        return "<" + self.__class__.__name__ + "id=%(id)s>" % {
            'id': self.id
        }

    def __getattr__(self, item):
        return None