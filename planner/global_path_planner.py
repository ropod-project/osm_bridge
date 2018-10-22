from osm_bridge import OSMBridge
import logging
from structs.wm.point import Point
from structs.wm.room import Room
from structs.wm.corridor import Corridor
from structs.wm.area import Area
from structs.wm.building import Building
from structs.wm.floor import Floor
from planner.router import Router
from planner.node import Node
from planner.connection import Connection


class GlobalPathPlanner(object):

    # default values
    _debug = False

    def __init__(self, osm_bridge, *args, **kwargs):
        self.osm_bridge = osm_bridge

        self.logger = logging.getLogger("GlobalPathPlanner")
        if kwargs.get("debug", self._debug):            
            self.logger.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def get_plan(self, building, start_floor, destination_floor, start, destination):
        if not isinstance(building, Building):
            raise Exception("Invalid building type")

        if not (isinstance(start_floor, Floor) and isinstance(destination_floor, Floor)):
            raise Exception("Invalid floor type")

        if not (isinstance(start, Room) or isinstance(start, Corridor) or isinstance(start, Area)):
            raise Exception("For planning global path start position must be room, corridor or area")

        if not (isinstance(destination, Room) or isinstance(destination, Corridor) or isinstance(destination, Area)):
            raise Exception("For planning global path destination position must be room, corridor or area")

        start_node = Node(start.topology)
        destination_node = Node(destination.topology)

        connections = []

        if start_floor == destination_floor:
            for connection in start_floor.connections:
                connections.append(Connection(connection))
        else:
            start_floor_connections = start_floor.connections
            destination_floor_connections = destination_floor.connections

        router = Router(start_node, destination_node, connections)
        router.route()


        