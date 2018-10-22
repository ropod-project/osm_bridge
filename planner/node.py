from planner.visited_node import VisitedNode
from structs.wm.point import Point

class Node(object):
    def __init__(self, point):
        self.point = point

    @property
    def id(self):
        return self.point.id

    @property
    def lat(self):
        return self.point.lat

    @property
    def lon(self):
        return self.point.lon

    def __eq__(self, other):
        if isinstance(other, VisitedNode):
            return self.id == other.node.id
        if isinstance(other, (Node)):
            return self.id == other.id

    def __repr__(self):
        return "<Node id=%(id)s, lat=%(lat)s, lon=%(lon)s>" % {
            'id': self.id,
            'lat': self.lat,
            'lon': self.lon,
        }
