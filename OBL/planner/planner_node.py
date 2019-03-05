from OBL.planner.visited_node import VisitedNode
from OBL.structs.wm.point import Point


class PlannerNode(Point):

    def __init__(self, point_ref):
        super(PlannerNode, self).__init__(point_ref)

    def __eq__(self, other):
        if isinstance(other, VisitedNode):
            return self.id == other.node.id
        if isinstance(other, (PlannerNode)):
            return self.id == other.id
