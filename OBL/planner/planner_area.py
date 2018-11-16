from OBL.structs.wm.area import Area
from OBL.structs.wm.area import Door


class PlannerArea(Area):
    def __init__(self, pt):
        super(PlannerArea, self).__init__(pt)
        self.navigation_areas = []
        self.exit_door = None
