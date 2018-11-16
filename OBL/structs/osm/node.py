from OBL.structs.osm.tag import Tag

class Node(object):
    '''
    OSM node
    '''
    def __init__(self, elm):
        element = elm
        self.id = element.get('id')
        self.lat = float(element.get('lat'))
        self.lon = float(element.get('lon'))
        self.tags = []

        tags = element.get('tags')
        if tags is not None:
            for tag in tags:
                self.tags.append(Tag(tag, tags.get(tag)))

    def __eq__(self, other):
        if isinstance(other, (Node)):
            return self.id == other.id

    def __repr__(self):
        return "<Node id=%(id)s, lat=%(lat)s, lon=%(lon)s>" % {
            'id': self.id,
            'lat': self.lat,
            'lon': self.lon,
        }

    def __getattr__(self, item):
        return None
