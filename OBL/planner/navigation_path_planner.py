import logging
import sys
from OBL.structs.wm.local_area import LocalArea
from OBL.structs.wm.floor import Floor
from OBL.structs.wm.door import Door
from OBL.planner.router import Router
from OBL.planner.planner_node import PlannerNode
from OBL.planner.planner_connection import PlannerConnection


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
        self.blocked_connections = []
        self.relax_traffic_rules = False

        self.logger = logging.getLogger("NavigationPathPlanner")
        if kwargs.get("debug", self._debug):
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

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
            raise Exception(
                "For planning navigation path start position must be local area")

        if not isinstance(destination, LocalArea):
            raise Exception(
                "For planning navigation path destination position must be local area")

        self.path_distance = 0
        self.topological_path = []

        start_node = PlannerNode(start.topology_id)
        destination_node = PlannerNode(destination.topology_id)

        connections = []

        for place in global_path:
            temp = place._connection_ids
            if temp is not None:
                for connection_id in temp:
                    connections.append(PlannerConnection(connection_id))
            if self.relax_traffic_rules:
                temp = place._recovery_connection_ids
                if temp is not None:
                    for connection_id in temp:
                        connections.append(PlannerConnection(connection_id))

        blocked_connections_nodes = []
        for blocked_connection in self.blocked_connections:
            blocked_connections_nodes.append([self.osm_bridge.get_local_area(blocked_connection[0]).topology_id,
                                              self.osm_bridge.get_local_area(blocked_connection[1]).topology_id])

        router = Router(start_node, destination_node, connections,
                        blocked_connections=blocked_connections_nodes,
                        relax_traffic_rules=self.relax_traffic_rules)
        router.route()

        local_path = router.nodes

        prev_idx = -1
        for local_pt in local_path:
            if local_pt.node.parent_type == "local_area":
                local_area = LocalArea(local_pt.node)
                local_area.geometry  # to get level info
            else:
                door = Door(local_pt.node)
                door.geometry
                global_path[prev_idx].exit_door = door
                continue

            global_pt = global_path[prev_idx]
            if global_pt.get_local_area_ids() is not None and local_area.id in global_pt.get_local_area_ids():
                global_pt.navigation_areas.append(local_area)
            else:
                prev_idx += 1
                global_pt = global_path[prev_idx]
                global_pt.navigation_areas.append(local_area)

        return global_path
