from structs.wm.area import Area

class Room(Area):

    def __init__(self, room_id, *args, **kwargs): 
        self.amenity = ''     
        super().__init__(room_id, *args, **kwargs)

