from OBL.structs.wm.area import Area


class PlannerArea(Area):
    def __init__(self, pt):
        super(PlannerArea, self).__init__(pt)
        self.navigation_areas = []
        self.exit_door = None

    def __repr__(self) :
        s = "\n<"
        s += "type:" + str(self.type) + ", "
        s += "id:" + str(self.id) + ", "
        s += "ref:" + str(self.ref) + ", "
        s += "navigation_areas:[" 
        for i in self.navigation_areas :
            s += "(id:" + str(i.id)  + ", "
            s += "ref:" + str(i.ref) + "), "
        s += "], " 
        s += "exit_door " + str(self.exit_door)
        s += ">"
        return s
