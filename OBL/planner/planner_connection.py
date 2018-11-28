from OBL.planner.planner_node import PlannerNode
from OBL.structs.wm.connection import Connection

class PlannerConnection(Connection):
    def __init__(self, connection_ref):
        super(PlannerConnection, self).__init__(connection_ref)
        self.nodes = []
        for pt in self.point_ids:
            self.nodes.append(PlannerNode(pt))
        self.oneway = (self.oneway == "yes")


    def __repr__(self):
        return "<Planner connection id=%(id)s, highway=%(highway)s, oneway=%(oneway)s>" % {
            'id': self.id,
            'highway': self.highway,
            'oneway': self.oneway,
        }
