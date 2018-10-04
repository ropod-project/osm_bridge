'''
OSM way
'''
class Way(object):
    def __init__(self, elm):
        element = elm
        self.id = element.get('id')
        self.level = None
        self.indoor = None
        self.highway = None
        self.oneway = None

        self.nodes =  []
        nodes = element.get('nodes')
        for node in nodes:
            self.nodes.append(node)

        tags = element.get('tags')
        if tags is not None:
            for tag in tags:
                setattr(self, tag, tags.get(tag))      

    def __eq__(self, other):
        return other is not None and self.id == other.id

    def __repr__(self):
        return "<Way id=%(id)s, nodes=%(nodes)s>" % {
            'id': self.id,
            'nodes': self.nodes
        }

    def __getattr__(self, item):
        return None