from structs.wm.area import Area

class Elevator(Area):

    def __init__(self, elevator_ref, *args, **kwargs):      
        super().__init__(elevator_ref, *args, **kwargs)

