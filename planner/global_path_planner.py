from osm_bridge import OSMBridge
import logging
from structs.wm.point import Point
from structs.wm.room import Room
from structs.wm.corridor import Corridor
from structs.wm.elevator import Elevator
from structs.wm.stairs import Stairs
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

    def get_plan(self, start_floor, destination_floor, start, destination, elevators):
        if not (isinstance(start_floor, Floor) and isinstance(destination_floor, Floor)):
            raise Exception("Invalid floor type")

        if not (isinstance(start, Room) or isinstance(start, Corridor) or isinstance(start, Area)):
            raise Exception("For planning global path start position must be room, corridor or area")

        if not (isinstance(destination, Room) or isinstance(destination, Corridor) or isinstance(destination, Area)):
            raise Exception("For planning global path destination position must be room, corridor or area")

        for elevator in elevators:
            if not (isinstance(elevator, Elevator) or isinstance(elevator, Stairs)):
                raise Exception("Invalid stairs or elevators type")

        start_node = Node(start.topology)
        destination_node = Node(destination.topology)

        connections = []
        topological_path = []

        if start_floor == destination_floor:
            for connection in start_floor.connections:
                connections.append(Connection(connection))

            router = Router(start_node, destination_node, connections)
            router.route()
            topological_path = router.nodes
        else:
            start_connections = []
            destination_connections = []
            
            for connection in start_floor.connections:
                start_connections.append(Connection(connection))

            for connection in destination_floor.connections:
                destination_connections.append(Connection(connection))

            connections = start_connections + destination_connections

            elevator_nodes = []
            start_to_elevator_distances = []
            start_to_elevator_paths = []
            for elevator in elevators:
                elevator_node = Node(elevator.topology)
                elevator_nodes.append(elevator_node)
                router = Router(start_node, elevator_node, start_connections)
                router.route()
                start_to_elevator_distances.append(router.path_distance)
                start_to_elevator_paths.append(router.nodes)

            best_path_to_elevator_idx = start_to_elevator_distances.index(min(start_to_elevator_distances))
            elevator_node = elevator_nodes[best_path_to_elevator_idx]
            start_to_elevator_path = start_to_elevator_paths[best_path_to_elevator_idx]

            router = Router(elevator_node, destination_node, destination_connections)
            router.route()
            elevator_to_destination_path = router.nodes

            topological_path = start_to_elevator_path + elevator_to_destination_path




        


        