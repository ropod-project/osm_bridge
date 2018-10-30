from planner.node import Node
from structs.wm.connection import Connection

class Connection(Connection):
    def __init__(self, connection_ref):
        super().__init__(connection_ref)
        self.nodes = []
        for pt in self.points:
            self.nodes.append(Node(pt))
        self.oneway = True if self.oneway == "yes" else False


    def __repr__(self):
        return "<Connection id=%(id)s, highway=%(highway)s, oneway=%(oneway)s>" % {
            'id': self.id,
            'highway': self.highway,
            'oneway': self.oneway,
        }