from structs.wm.wm_entity import WMEntity
from structs.wm.elevator import Elevator
from structs.wm.stairs import Stairs
from structs.wm.floor import Floor

class Building(WMEntity):

    def __init__(self, building_id, *args, **kwargs):      
        __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[building_id], data_type='relation')
        
        self.floor_ids = []
        self.elevator_ids = []
        self.stairs_ids = []

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key, tag.value) 

            for member in relations[0].members:
                if member.role == 'level':
                    self.floor_ids.append(member.ref)
                if member.role == 'elevator':
                    self.elevator_ids.append(member.ref)
                if member.role == 'stairs':
                    self.stairs_ids.append(member.ref)
        else:
            self.logger.error("No floor found with given id {}".format(floor_id))  

    @property
    def floors(self):
        floors = []
        for floor_id in self.floor_ids:
            floors.append(Floor(floor_id))
        return floors

    @property
    def elevators(self):
        elevators = []
        for elevator_id in self.elevator_ids:
            elevators.append(Elevator(elevator_id))
        return elevators

    @property
    def stairs(self):
        stairs = []
        for stairs_id in self.stairs_ids:
            stairs.append(Room(stairs_id))
        return stairs