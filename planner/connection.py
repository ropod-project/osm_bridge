from planner.node import Node

class Connection(object):
    def __init__(self, connection):
        self.connection = connection
        self.nodes = []
        for pt in self.connection.points:
            self.nodes.append(Node(pt))

    @property
    def id(self):
        return self.connection.id

    @property
    def highway(self):
        return self.tags.connection.highway

    @property
    def oneway(self):
        return True if self.connection.oneway == "yes" else False

    def __eq__(self, other):
        return other is not None and self.id== other.id

    def __repr__(self):
        return "<Connection id=%(id)s, highway=%(highway)s, oneway=%(oneway)s>" % {
            'id': self.id,
            'highway': self.highway,
            'oneway': self.oneway,
        }