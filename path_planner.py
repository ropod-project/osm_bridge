from osm_bridge import OSMBridge
import logging
import sys
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
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def get_global_plan(self,start_floor, destination_floor, start, destination, elevators):
        self.global_path_planner.plan(start_floor, destination_floor, start, destination, elevators)
        # return semantic path here

    def get_estimated_path_length(self):
        return self.global_path_planner.path_distance


        