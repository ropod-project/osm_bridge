from osm_bridge import OSMBridge
import logging
from structs.wm.point import Point
from structs.wm.room import Room
from structs.wm.corridor import Corridor
from structs.wm.elevator import Elevator
from structs.wm.stairs import Stairs
from structs.wm.area import Area
from structs.wm.local_area import LocalArea
from structs.wm.building import Building
from structs.wm.floor import Floor
from planner.router import Router
from planner.planner_node import PlannerNode
from planner.planner_connection import PlannerConnection
from planner.planner_area import PlannerArea


class NavigationPathPlanner(object):

    """Summary
    Plans very detailed path for robot with traffic rule information and other semantics
    Attributes:
        logger (logging): logger
        osm_bridge (OSMBridge): bridge between wm and osm
        path_distance (double): distance in km
        topological_path (list): list of points
    """
    
    # default values
    _debug = False

    def __init__(self, osm_bridge, *args, **kwargs):
        """Summary
        
        Args:
            osm_bridge (OSMBridge): bridge between wm and osm
        """
        self.osm_bridge = osm_bridge
        self.topological_path = []
        self.semantic_path = []
        self.path_distance = 0

        self.logger = logging.getLogger("NavigationPathPlanner")
        if kwargs.get("debug", self._debug):
            self.logger.basicConfig(stream=sys.stdout, level=logging.DEBUG)


    def plan(self, start_floor, destination_floor, start, destination, global_path):
        """Summary
        Plans navigation path using A* planner with straight line distance heuristics

        Args:
            start_floor (Floor): start floor wm entity
            destination_floor (Floor): destination floor wm entity
            start (LocalArea): start local area wm entity
            destination (LocalArea): destination local area wm entity
        
        Returns:
            [PlannerArea]: list of planner areas 
        
        Raises:
            Exception: multiple exceptions
        """
        if not (isinstance(start_floor, Floor) and isinstance(destination_floor, Floor)):
            raise Exception("Invalid floor type")

        if not isinstance(start, LocalArea):
            raise Exception("For planning navigation path start position must be local area")

        if not isinstance(destination, LocalArea):
            raise Exception("For planning navigation path destination position must be local area")

        self.path_distance = 0
        self.topological_path = []

        start_node = PlannerNode(start.topology)
        destination_node = PlannerNode(destination.topology)

        connections = []

        for place in global_path:
            temp = place._connection_ids
            if temp is not None:
                for connection_id in temp:
                    connections.append(PlannerConnection(connection_id))

        router = Router(start_node, destination_node, connections)
        router.route()

        local_path = router.nodes

        for local_pt in local_path:
            local_area = LocalArea(local_pt.node)            
            for global_pt in global_path:
                if global_pt.get_local_area_ids() is not None and local_area.id in global_pt.get_local_area_ids():
                    global_pt.navigation_areas.append(local_area)
                    break 
        return global_path






        



        
        


        