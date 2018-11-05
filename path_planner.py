from osm_bridge import OSMBridge
import logging
import sys
from planner.global_path_planner import GlobalPathPlanner
from planner.navigation_path_planner import NavigationPathPlanner
from planner.local_area_finder import LocalAreaFinder


class PathPlanner(object):

    """Summary
    Provides methods for path planning, calculating estimated path distance and for configurating the path planner
    
    Attributes:
        global_path_planner (GlobalPathPlanner): plans global path 
        logger (): logger
        navigation_path_planner (NavigationPathPlanner): plans local navigation path for robot to follow
        osm_bridge (OSMBridge): bridge between world model and OSM
    """
    
    # default values
    _debug = False

    def __init__(self, osm_bridge, *args, **kwargs):
        """Summary
        
        Args:
            osm_bridge (OSMBridge): bridge between world model and OSM
        
        Raises:
            Exception: Description
        """
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
        """Summary
        
        Args:
            building_ref (int/string): uuid or semantic name of the building
        """
        self._building = self.osm_bridge.get_building(building_ref)
        self._elevators = self._building.elevators

    def set_coordinate_system(self, coordinate_system):
        """Summary
        
        Args:
            coordinate_system (string): spherical/cartesian
        """
        self._coordinate_system = coordinate_system


    def get_path_plan(self,start_floor, destination_floor, start_area, destination_area, *args, **kwargs):
        """Summary
        Plans detailed navigation path for robot
        Args:
            start_floor (str): start floor ref
            destination_floor (str): destination floor ref
            start_area (str): start area ref
            destination_area (str): destination area ref
            elevator(str, optional): ref of elevator to use
            start_local_area(str, optional): start local area ref
            destination_local_area(str, optional): destination local area ref
            robot_position([x,y]) : robot position in x/y or lat/lng
            destination_task(str) : task to be performed at destination eg. docking, charging etc.

        Returns:
            TYPE: navigation path
        
        Raises:
            Exception: can raise multiple exceptions
        """
        elevator_ref = kwargs.get("elevator")
        if elevator_ref:
            elevators = self.osm_bridge.get_elevator(elevator_ref)
        else:
            elevators = self._elevators

        start_local_area_ref = kwargs.get("start_local_area")
        destination_local_area_ref = kwargs.get("destination_local_area")
        destination_task = kwargs.get("destination_task")
        robot_position = kwargs.get("robot_position")

        if not start_local_area_ref and not robot_position:
            raise Exception("Start local area ref or robot position is must to determine starting position") 

        if not destination_local_area_ref and not destination_task:
            raise Exception("Destination local area ref or destination task is must to determine destination")

        isLatlong = True if self._coordinate_system == 'spherical' else False

        start_local_area = None
        if not start_local_area_ref:
            start_local_area = self.local_area_finder.get_local_area(robot_position[0], robot_position[1], area_name=start_area, isLatlong=isLatlong)
        else:
            start_local_area = self.osm_bridge.get_local_area(start_local_area_ref)

        destination_local_area = None
        if not destination_local_area_ref:
            destination_local_area = self.local_area_finder.get_local_area(area_name=destination_area, behaviour=destination_task)
        else:
            destination_local_area = self.osm_bridge.get_local_area(destination_local_area_ref)

        start_floor = self.osm_bridge.get_floor(start_floor)
        destination_floor = self.osm_bridge.get_floor(destination_floor)

        start_area = self.osm_bridge.get_area(start_area)
        destination_area = self.osm_bridge.get_area(destination_area)

        global_path = self.global_path_planner.plan(start_floor, destination_floor, start_area, destination_area, elevators)
        navigation_path = self.navigation_path_planner.plan(start_floor, destination_floor, start_local_area, destination_local_area, global_path)

        return navigation_path


    def get_estimated_path_distance(self,start_floor, destination_floor, start_area, destination_area, *args, **kwargs):
        """Summary
        Returns estimated path distance in Kms
        Args:
            start_floor (str): start floor
            destination_floor (str): destination floor
            start_area (str): start area
            destination_area (str): destination area
        
        Returns:
            TYPE: path distance (double)
        """
        elevators = kwargs.get("elevators", self._elevators)

        start_floor = self.osm_bridge.get_floor(start_floor)
        destination_floor = self.osm_bridge.get_floor(destination_floor)

        start_area = self.osm_bridge.get_area(start_area)
        destination_area = self.osm_bridge.get_area(destination_area)

        global_path = self.global_path_planner.plan(start_floor, destination_floor, start_area, destination_area, elevators)

        return global_path.path_distance



        