from planner.visited_node import VisitedNode
from structs.wm.point import Point

class Node(Point):
    def __eq__(self, other):
        if isinstance(other, VisitedNode):
            return self.id == other.node.id
        if isinstance(other, (Node)):
            return self.id == other.id