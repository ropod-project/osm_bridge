from structs.osm.tag import Tag

class Way(object):
    '''
    OSM way
    '''
    def __init__(self, elm):
        element = elm
        self.id = element.get('id')

        self.nodes =  []
        nodes = element.get('nodes')
        for node in nodes:
            self.nodes.append(node)

        self.tags = []
        tags = element.get('tags')
        if tags is not None:
            for key in tags:
                self.tags.append(Tag(key, tags.get(key)))

    def __eq__(self, other):
        return other is not None and self.id == other.id

    def __repr__(self):
        return "<Way id=%(id)s, nodes=%(nodes)s>" % {
            'id': self.id,
            'nodes': self.nodes
        }

    def __getattr__(self, item):
        return None
