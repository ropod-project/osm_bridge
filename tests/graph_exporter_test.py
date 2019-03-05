from OBL import OSMBridge
from OBL import GraphExporter

import unittest
import os


class TestGraphExporter(unittest.TestCase):
    '''
    Unit tests for occupancy grid generator class 
    '''

    def setUp(self):
        self.osm_bridge = OSMBridge()
        self.server_ip = "127.0.0.1"
        self.server_port = 8000
        self.global_origin = [50.1363485, 8.6474024]  # amk
        # self.global_origin = [50.7800401, 7.18226]  # uni (coordinates of node id 1307)

        self.local_offset = [25, 25]  # amk
        # self.local_offset = [25, 80] # brsu

        self.debug = False

    # def test_get_global_topological_graph(self):
    #     graph_exporter = GraphExporter(osm_bridge=self.osm_bridge, local_offset=self.local_offset, debug=self.debug)
    #     graph_exporter.get_global_topological_graph('AMK_L-1')

    def test_get_local_topological_graph(self):
        graph_exporter = GraphExporter(osm_bridge=self.osm_bridge, local_offset=self.local_offset, debug=self.debug)
        graph_exporter.get_local_topological_graph('AMK_L-1')


if __name__ == '__main__':
    unittest.main()
