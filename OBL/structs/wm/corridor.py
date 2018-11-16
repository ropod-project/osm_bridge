from OBL.structs.wm.area import Area

class Corridor(Area):

    def __init__(self, corridor_ref, *args, **kwargs):
        super(Corridor, self).__init__(corridor_ref, *args, **kwargs)
