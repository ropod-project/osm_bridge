from OBL.structs.wm.area import Area
from OBL.structs.wm.area import Door


class PlannerArea(Area):
    def __init__(self, pt):
        super(PlannerArea, self).__init__(pt)
        self.navigation_areas = []
        self.exit_door = None

#     def __repr__(self) :
#         s = "<"
#         s += "type " + str(self.type) + "\n"
#         s += "id " + str(self.id) + "\n"
#         s += "ref " + str(self.ref) + "\n"
#         s += "level " + str(self.level) + "\n"
#         for i in self.navigation_areas :
#             s += "navigation_areas id " + str(i.id)  + "\n"
#             s += "navigation_areas ref " + str(i.ref) + "\n"
#         s += ">"
#         return s
