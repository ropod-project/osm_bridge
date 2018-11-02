from osm_bridge import OSMBridge
import logging
import sys
from planner.global_path_planner import GlobalPathPlanner
from planner.navigation_path_planner import NavigationPathPlanner
from planner.local_area_finder import LocalAreaFinder


class PathPlanner(object):

    # default values
    _debug = False

    def __init__(self, osm_bridge, *args, **kwargs):
        if not isinstance(osm_bridge, OSMBridge):
            raise Exception("Please pass OSM bridge object")
        self.osm_bridge = osm_bridge

        self.global_path_planner = GlobalPathPlanner(self.osm_bridge)
        self.navigation_path_planner = NavigationPathPlanner(self.osm_bridge)

        self._building = None
        self._elevators = None
        self._coordinate_system = 'cartesian'

        self.logger = logging.getLogger("PathPlanner")
        if kwargs.get("debug", self._debug):            
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def set_building(self, building_ref):
        self._building = self.osm_bridge.get_building(building_ref)
        self._elevators = self._building.elevators

    def get_path_plan(self,start_floor='', destination_floor='', start_area='', destination_area='', *args, **kwargs):

        elevators = kwargs.get("elevators", self._elevators)
        start_local_area_ref = kwargs.get("start_local_area")
        destination_local_area_ref = kwargs.get("destination_local_area")
        destination_task = kwargs.get("destination_task")
        robot_position = kwargs.get("robot_position")

        if not start_local_area_ref and not robot_position:
            raise Exception("Start local area ref or robot position is must to determine starting position") 

        if not destination_local_area_ref and not destination_task:
            raise Exception("Destination local area ref or destination task is must to determine destination")

        start_local_area = None
        if not start_local_area_ref:
            start_local_area = self.local_area_finder.get_local_area(robot_position[0], robot_position[1], area_name=start_area, isLatlong=False)
        else:
            start_local_area = self.osm_bridge.get_local_area(start_local_area_ref)

        destination_local_area = None
        if not destination_local_area_ref:
            #TODO
            pass
        else:
            destination_local_area = self.osm_bridge.get_local_area(destination_local_area_ref)

        start_floor = self.osm_bridge.get_floor(start_floor)
        destination_floor = self.osm_bridge.get_floor(destination_floor)

        start_area = self.osm_bridge.get_area(start_area)
        destination_area = self.osm_bridge.get_area(destination_area)

        global_path = self.global_path_planner.plan(start_floor, destination_floor, start_area, destination_area, elevators)
        navigation_path = self.navigation_path_planner.plan(start_floor, destination_floor, start_local_area, destination_local_area, global_path)

        return navigation_path


    def get_estimated_path_distance(self,start_floor='', destination_floor='', start_area='', destination_area='', *args, **kwargs):

        elevators = kwargs.get("elevators", self._elevators)

        start_floor = self.osm_bridge.get_floor(start_floor)
        destination_floor = self.osm_bridge.get_floor(destination_floor)

        start_area = self.osm_bridge.get_area(start_area)
        destination_area = self.osm_bridge.get_area(destination_area)

        global_path = self.global_path_planner.plan(start_floor, destination_floor, start_area, destination_area, elevators)

        return global_path.path_distance



        