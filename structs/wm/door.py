from structs.wm.wm_entity import WMEntity
from structs.wm.feature import Feature
from structs.wm.geometry import Point, Shape
from structs.wm.side import Side

class Door(WMEntity):

    def __init__(self, osm_bridge_instance, door_id, *args, **kwargs):
        self.osm_bridge = osm_bridge_instance        
        __,__,relations = self.osm_bridge.get_osm_element_by_id(ids=[door_id], data_type='relation')
        
        self.side_ids = []
        self.geometry_id = None
        self.topology_id = None

        if len(relations) == 1:
            self.id = relations[0].id

            for tag in relations[0].tags:
                setattr(self, tag.key, tag.value) 

            for member in relations[0].members:
                if member.role == 'side':
                    self.side_ids.append(member.ref)
                if member.role == 'geometry':
                    self.geometry_id = member.ref
                if member.role == 'topology':
                    self.topology_id = member.ref
        else:
            print("No side found with given id {}".format(side_id))  

    @property
    def geometry(self):
        return Shape(self.osm_bridge, self.geometry_id)

    @property
    def topology(self):
        return Point(self.osm_bridge, self.topology_id)

    @property
    def sides(self):
        sides = []
        for side_id in side_ids:
            sides.append(Side(self.osm_bridge, side_id))
        return sides