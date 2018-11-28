class Tag(object):
    '''
    OSM tag
    '''
    def __init__(self, key, value):
        # self.key = key.encode()
        self.key = key
        # self.value = value.encode()
        self.value = value


    def __eq__(self, other):
        if isinstance(other, (Tag)):
            return self.key == other.key and self.value == other.value

    def __repr__(self):
        return "<Tag key=%(key)s, value=%(value)s>" % {
            'key': self.key,
            'value': self.value
        }

    def __getattr__(self, item):
        return None
