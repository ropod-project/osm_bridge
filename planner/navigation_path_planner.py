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
from planner.node import Node
from planner.connection import Connection


class NavigationPathPlanner(object):

    # default values
    _debug = False

    def __init__(self, osm_bridge, *args, **kwargs):
        self.osm_bridge = osm_bridge
        self.topological_path = []
        self.semantic_path = []
        self.path_distance = 0

        self.logger = logging.getLogger("NavigationPathPlanner")
        if kwargs.get("debug", self._debug):
            self.logger.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    '''
    Plans navigation path using A* planner with straight line distance heuristics
    '''
    def plan(self, start_floor, destination_floor, start, destination, global_path):
        if not (isinstance(start_floor, Floor) and isinstance(destination_floor, Floor)):
            raise Exception("Invalid floor type")

        if not isinstance(start, LocalArea):
            raise Exception("For planning navigation path start position must be local area")

        if not isinstance(destination, LocalArea):
            raise Exception("For planning navigation path destination position must be local area")

        self.path_distance = 0
        self.semantic_path = []
        self.topological_path = []

        start_node = Node(start.topology)
        destination_node = Node(destination.topology)

        connections = []

        



        
        


        