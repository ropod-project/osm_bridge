from structs.osm.node import Node
from structs.osm.tag import Tag
from structs.osm.way import Way
from structs.osm.relation import Relation
import logging

class WMEntity():

    osm_adapter = None
    logger = logging.getLogger("WMEntity")

    def __init__(self, entity_id): 
        pass

    def __eq__(self, other):
        if isinstance(other, (WMEntity)):
            return self.id == other.id

    def __repr__(self):
        return "<" + self.__class__.__name__ + " id=%(id)s>" % {
            'id': self.id
        }

    def __getattr__(self, item):
        return None