'''
OSM tag
'''
class Tag():
    def __init__(self, key, value):
        self.key = key
        self.value = value


    def __eq__(self, other):
        if isinstance(other, (Tag)):
            return self.key == other.value and self.key == other.value

    def __repr__(self):
        return "<Tag key=%(key)s, value=%(val)s>" % {
            'key': self.key,
            'value': self.value
        }

    def __getattr__(self, item):
        return None
