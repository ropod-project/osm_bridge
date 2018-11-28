class VisitedNode(object):
    def __init__(self, node, parent=None, g=None, h=None):
        self.node = node
        self.parent = parent
        self.g = g
        self.h = h

    @property
    def id(self):
        return self.node.id

    @property
    def f(self):
        return self.g + self.h if self.g is not None and self.h is not None else None

    @property
    def lat(self):
        return self.node.lat

    @property
    def lon(self):
        return self.node.lon

    def __eq__(self, other):
        if isinstance(other, VisitedNode):
            return self.node.id == other.node.id
        if isinstance(other, (Node)):
            return self.node.id == other.id

    def __gt__(self, other):
        return self.f > other.f

    def __repr__(self):
        return "<VisitedNode node=%(node)s, g=%(g).3f, h=%(h).3f>" % {
            'node': repr(self.node),
            'f': self.f,
            'g': self.g,
            'h': self.h,
        }
