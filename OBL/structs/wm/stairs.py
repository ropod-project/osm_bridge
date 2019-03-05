from OBL.structs.wm.area import Area


class Stairs(Area):

    def __init__(self, stairs_ref, *args, **kwargs):
        super(Stairs, self).__init__(stairs_ref, *args, **kwargs)
