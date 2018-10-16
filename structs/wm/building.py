from structs.wm.wm_entity import WMEntity
from structs.wm.shape import Shape
from structs.wm.elevator import Elevator
from structs.wm.stairs import Stairs
from structs.wm.floor import Floor

class Building(WMEntity):

    def __init__(self, building_ref, *args, **kwargs):      

        if self._is_osm_id(building_ref):      
            __,__,relations = self.osm_adapter.get_osm_element_by_id(ids=[building_ref], data_type='relation')
        else:
            __,__,relations = self.osm_adapter.search_by_tag(data_type='relation',key='ref',value=building_ref)
        
        # possible attributes
        # NOTE: attirbute will have value only if its set by the mapper
        # Some attribute values will be available only after loading related property of the building
        self.building = ''              # purpose of the building eg. university, hospital etc.       
        self.name = ''
        self.city = ''
        self.country = ''
        self.height = ''
        self.min_level = ''
        self.max_level = ''
        self.non_existant_levels = ''   # string separated by semicolons 
        self.color = ''
        self.material = ''

        # private attributes
        self._floor_ids = []
        self._elevator_ids = []
        self._stairs_ids = []
        self._geometry_id = None 

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key.replace("-", "_"), tag.value) 

            for member in relations[0].members:
                if member.role == 'geometry':
                    self._geometry_id = member.ref
                if member.role == 'level':
                    self._floor_ids.append(member.ref)
                if member.role == 'elevator':
                    self._elevator_ids.append(member.ref)
                if member.role == 'stairs':
                    self._stairs_ids.append(member.ref)
        else:
            self.logger.error("No building found with given ref {}".format(building_ref))  

    @property
    def floors(self):
        floors = []
        for floor_id in self._floor_ids:
            floors.append(Floor(floor_id))
        return floors

    @property
    def elevators(self):
        elevators = []
        for elevator_id in self._elevator_ids:
            elevators.append(Elevator(elevator_id))
        return elevators

    @property
    def stairs(self):
        stairs = []
        for stairs_id in self._stairs_ids:
            stairs.append(Room(stairs_id))
        return stairs

    @property
    def geometry(self):
        __,geometries,__ = self.osm_adapter.get_osm_element_by_id(ids=[self._geometry_id], data_type='way')

        for tag in geometries[0].tags:
            setattr(self, tag.key, tag.value) 

        nodes = []
        for node_id in geometries[0].nodes:
            temp_nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=[node_id], data_type='node')
            nodes.append(temp_nodes[0])
        return Shape(nodes)