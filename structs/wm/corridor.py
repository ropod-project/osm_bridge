from structs.wm.area import Area

class Corridor(Area):

    def __init__(self, corridor_ref, *args, **kwargs):      
        super().__init__(corridor_ref, *args, **kwargs)

    def __repr__(self):
        return "<" + self.__class__.__name__ + " id=%(id)s type=%(type)s>" % {
            'id': self.id, 'type': self.type
        }

