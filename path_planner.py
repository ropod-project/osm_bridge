from osm_bridge import OSMBridge
import logging
from structs.wm.point import Point
from structs.wm.room import Room
from structs.wm.corridor import Corridor
from structs.wm.area import Area
from planner.global_path_planner import GlobalPathPlanner

class PathPlanner(object):

    # default values
    _debug = False

    def __init__(self, osm_bridge, *args, **kwargs):
        self.osm_bridge = osm_bridge

        self.global_path_planner = GlobalPathPlanner(self.osm_bridge)

        self.logger = logging.getLogger("PathPlanner")
        if kwargs.get("debug", self._debug):            
            self.logger.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def get_global_plan(self,building, start_floor, destination_floor, start, destination):
        return self.global_path_planner.get_plan(building, start_floor, destination_floor, start, destination)


        