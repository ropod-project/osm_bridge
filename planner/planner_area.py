from structs.wm.area import Area
from structs.wm.area import Door


class PlannerArea(Area):
    def __init__(self, pt):
        Area.__init__(pt)
        self.navigation_areas = []
        self.doors = []