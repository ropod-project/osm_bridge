from structs.wm.area import Area

class Stairs(Area):

    def __init__(self, stairs_ref, *args, **kwargs):      
        super().__init__(elevator_ref, *args, **kwargs)
