from OBL.structs.osm.node import Node
from OBL.structs.osm.tag import Tag
from OBL.structs.osm.way import Way
from OBL.structs.osm.relation import Relation
import logging

class WMEntity(object):

    osm_adapter = None
    logger = logging.getLogger("WMEntity")

    def __init__(self, entity_id, *args, **kwargs):
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

    def _check_type(self,ref):
        if isinstance(ref, int):
            return "id"
        elif isinstance(ref, str):
            return "ref"
        elif isinstance(ref, Relation):
            return "relation"
        elif isinstance(ref, Node):
            return "node"
        elif isinstance(ref, Way):
            return "way"
        else:
            return None
