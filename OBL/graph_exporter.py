import networkx as nx
from OBL import OSMBridge
import utm
import logging
import sys
import matplotlib.pyplot as plt


class GraphExporter(object):

    """Used for exporting floor and area level graphs
    """

    _debug = False
    _server_ip = "127.0.0.1"
    _osm_bridge = None
    _server_port = 8000
    _global_origin = [50.1363485, 8.6474024]
    _local_offset = [0, 0]

    def __init__(self, *args, **kwargs):
        """ 
        kwargs
        :osm_bridge: OSMBridge object
        :server_ip(str, optional): ip address of overpass server
        :server_port(int, optional): overpass server port
        :local_offset: [float, float]
        :debug: boolean
        """

        self._server_ip = kwargs.get("server_ip", self._server_ip)
        self._server_port = kwargs.get("server_port", self._server_port)
        self._osm_bridge = kwargs.get("osm_bridge", self._osm_bridge)
        self._global_origin = kwargs.get("global_origin", self._global_origin)

        if self._osm_bridge is None and (self._server_ip is None or self._server_port is None or self._global_origin is None):
            raise Exception(
                "Either OSMBridge object or (server_ip and server_port and global_origin) is required")

        if (self._osm_bridge is not None) and (not isinstance(self._osm_bridge, OSMBridge)):
            raise Exception(
                "Object provided with keyword \"osm_bridge\" is not a OSMBridge object")

        if self._osm_bridge is not None:
            self._server_ip = self._osm_bridge._server_ip
            self._server_port = self._osm_bridge._server_port
            self._global_origin = self._osm_bridge.global_origin

        self._local_offset = kwargs.get("local_offset", self._local_offset)
        self._global_origin_cartesian = utm.from_latlon(
            self._global_origin[0], self._global_origin[1])

        self.logger = logging.getLogger("GraphExporter")
        if kwargs.get("debug", self._debug):
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def get_global_topological_graph(self, floor_ref, visualize=False):
        floor = self._osm_bridge.get_floor(floor_ref)
        global_connections = floor.connections
        graph = nx.Graph()
        prev_area = None
        for global_connection in global_connections:
            for i, point in enumerate(global_connection.points):
                area = self._osm_bridge.get_area(point)
                graph.add_node(area.id, pos=(point.x, point.y),
                               type=area.type, name=area.ref)
                if i is not 0:
                    graph.add_edge(prev_area.id, area.id)
                prev_area = area
        # print(graph.nodes.data())
        # print(graph.edges.data())
        if visualize:
            self.visualize_graph(graph)
        return graph

    def get_local_topological_graph(self, building_ref, floor_ref, visualize=False):
        building = self._osm_bridge.get_building(building_ref)
        floor = self._osm_bridge.get_floor(floor_ref)
        areas = []

        if floor.rooms is not None:
            areas = areas + floor.rooms
        if floor.corridors is not None:
            areas = areas + floor.corridors
        if floor.corridors is not None:
            areas = areas + floor.corridors
        if floor.areas is not None:
            areas = areas + floor.areas

        elevators = building.elevators
        if elevators:
            areas = areas + elevators

        graph = nx.Graph()
    
        for area in areas:
            local_areas = area.local_areas
            if local_areas is not None:
                for local_area in local_areas:
                    local_area.geometry
                    point = local_area.topology
                    graph.add_node(local_area.id, pos=(point.x, point.y), parent_id=area.id, type=area.type,
                                   name=local_area.ref, behaviour=local_area.behaviour)
            doors = area.doors
            if doors is not None:
                for door in doors:
                    door.geometry
                    point = door.topology
                    graph.add_node(door.id, pos=(point.x, point.y), parent_id=area.id, type=area.type,
                                   name=door.ref, behaviour=door.type)
        prev_local_area = None
        for area in areas:
            local_connections = area.connections
            if local_connections is not None:
                for local_connection in local_connections:
                    for i, point in enumerate(local_connection.points):
                        local_area = self._osm_bridge.get_local_area(point)
                        if i is not 0:
                            if(graph.has_node(prev_local_area.id) and graph.has_node(local_area.id)):
                                graph.add_edge(prev_local_area.id, local_area.id,
                                               oneway=local_connection.oneway)
                        prev_local_area = local_area
        # print(graph.nodes.data())
        # print(graph.edges.data())
        if visualize:
            self.visualize_graph(graph)
        return graph


    def visualize_graph(self, graph):
        pos = nx.get_node_attributes(graph, 'pos')
        nx.draw(graph, pos)
        plt.show()
