from OBL.structs.wm.area import Area

class Room(Area):

    def __init__(self, room_ref, *args, **kwargs):
        self.amenity = ''
        super(Room, self).__init__(room_ref, *args, **kwargs)
