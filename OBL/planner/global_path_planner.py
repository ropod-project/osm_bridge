import logging
import sys

from OBL.structs.wm.room import Room
from OBL.structs.wm.corridor import Corridor
from OBL.structs.wm.elevator import Elevator
from OBL.structs.wm.stairs import Stairs
from OBL.structs.wm.area import Area
from OBL.structs.wm.floor import Floor
from OBL.planner.router import Router
from OBL.planner.planner_node import PlannerNode
from OBL.planner.planner_connection import PlannerConnection
from OBL.planner.planner_area import PlannerArea


class GlobalPathPlanner(object):

    """Summary
    Plans global path between different indoor elements
    Attributes:
        logger (logging): logger
        osm_bridge (OSMBridge): bridge between wm and osm
        path_distance (int): path distance in km
        semantic_path (list): list of planner areas
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

        self.logger = logging.getLogger("GlobalPathPlanner")
        if kwargs.get("debug", self._debug):
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def plan(self, start_floor, destination_floor, start, destination, elevators):
        """Summary
        Plans global path using A* planner with straight line distance heuristics

        Args:
            start_floor (Floor): start floor wm entity
            destination_floor (Floor): destination floor wm entity
            start (Area): start area wm entity
            destination (Area): destination area wm entity
            elevators (Elevators): list of elevator wm entity

        Returns:
            [PlannerArea]: list of planner areas

        Raises:
            Exception: multiple exception
        """
        if not (isinstance(start_floor, Floor) and isinstance(destination_floor, Floor)):
            raise Exception("Invalid floor type")

        if not (isinstance(start, Room) or isinstance(start, Corridor) or isinstance(start, Area)):
            raise Exception(
                "For planning global path start position must be room, corridor or area")

        if not (isinstance(destination, Room) or isinstance(destination, Corridor) or isinstance(destination, Area)):
            raise Exception(
                "For planning global path destination position must be room, corridor or area")

        for elevator in elevators:
            if not (isinstance(elevator, Elevator) or isinstance(elevator, Stairs)):
                raise Exception("Invalid stairs or elevators type")

        self.path_distance = 0
        self.semantic_path = []
        self.topological_path = []

        start_node = PlannerNode(start.topology_id)
        destination_node = PlannerNode(destination.topology_id)

        connections = []

        if start_floor == destination_floor:
            for connection_id in start_floor._connection_ids:
                connections.append(PlannerConnection(connection_id))

            router = Router(start_node, destination_node, connections)
            router.route()
            self.topological_path = router.nodes
            self.path_distance = router.path_distance
        else:
            start_connections = []
            destination_connections = []

            for connection_id in start_floor._connection_ids:
                start_connections.append(PlannerConnection(connection_id))

            for connection_id in destination_floor._connection_ids:
                destination_connections.append(
                    PlannerConnection(connection_id))

            connections = start_connections + destination_connections

            elevator_nodes = []
            start_to_elevator_distances = []
            start_to_elevator_paths = []
            for elevator in elevators:
                elevator_node = PlannerNode(elevator.topology_id)
                elevator_nodes.append(elevator_node)
                router = Router(start_node, elevator_node, start_connections)
                router.route()
                start_to_elevator_distances.append(router.path_distance)
                start_to_elevator_paths.append(router.nodes)

            best_path_to_elevator_idx = start_to_elevator_distances.index(
                min(start_to_elevator_distances))
            elevator_node = elevator_nodes[best_path_to_elevator_idx]
            start_to_elevator_path = start_to_elevator_paths[
                best_path_to_elevator_idx]
            self.path_distance = start_to_elevator_distances[
                best_path_to_elevator_idx]

            router = Router(elevator_node, destination_node,
                            destination_connections)
            router.route()
            elevator_to_destination_path = router.nodes

            self.topological_path = start_to_elevator_path + \
                elevator_to_destination_path[1:]
            self.path_distance = self.path_distance + router.path_distance

        log_statement = "Successfully planned {} m long path between {} and {}".format(
            self.path_distance, start.ref, destination.ref)
        self.logger.info(log_statement)
#         print(log_statement)
        return self.get_semantic_path()

    def get_semantic_path(self):
        """Summary

        Returns:
            [PlannerArea]: path consisting of planner areas
        """
        semantic_path = []
        for p in self.topological_path:
            temp = PlannerArea(p.node)
            temp.geometry  # to get level info
            semantic_path.append(temp)

        return semantic_path
