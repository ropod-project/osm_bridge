import networkx as nx
from OBL import OSMBridge
import utm
import logging
import sys
import os
import matplotlib.pyplot as plt


class GraphExporter(object):

    """Generates occupancy grids for a map based on the OSM map
    """

    _debug = False
    _dirname = "~/graph"
    _file_name = "graph"
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
        :dirname: String
        :filename: String
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
        self._dirname = kwargs.get("dirname", self._dirname)
        self._file_name = kwargs.get("filename", self._file_name)
        self._global_origin_cartesian = utm.from_latlon(
            self._global_origin[0], self._global_origin[1])

        self.logger = logging.getLogger("GraphExporter")
        if kwargs.get("debug", self._debug):
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def get_global_topological_graph(self, floor_ref):
        floor = self._osm_bridge.get_floor(floor_ref)
        global_connections = floor.connections
        graph = nx.Graph()
        for global_connection in global_connections:
            for point in global_connection.points:
                graph.add_node(point.id, pos=(point.x, point.y))
        # print(graph.nodes.data())

        for global_connection in global_connections:
            for i, point in enumerate(global_connection.points):
                if i is not 0:
                    graph.add_edge(global_connection.points[
                                   i - 1].id, point.id)
        # print(graph.edges.data())
        self.plot_graph(graph)
        return graph

    def get_local_topological_graph(self, floor_ref):
        floor = self._osm_bridge.get_floor(floor_ref)
        areas = []
        if floor.rooms is not None:
            areas = areas + floor.rooms
        if floor.corridors is not None:
            areas = areas + floor.corridors

        graph = nx.Graph()

        for area in areas:
            if area.connections is not None:
                for local_connection in area.connections:
                    for point in local_connection.points:
                        graph.add_node(point.id, pos=(point.x, point.y))

        # print(graph.nodes.data())

        for area in areas:
            if area.connections is not None:
                for local_connection in area.connections:
                    for i, point in enumerate(local_connection.points):
                        if i is not 0:
                            graph.add_edge(local_connection.points[
                                           i - 1].id, point.id,
                                           oneway=local_connection.oneway)

        # print(graph.edges.data())
        self.plot_graph(graph)
        return graph

    def get_local_topological_graph_of_area(self, area_ref):
        pass

    def plot_graph(self, graph):
        pos = nx.get_node_attributes(graph, 'pos')
        nx.draw(graph, pos)   # default spring_layout
        plt.show()
