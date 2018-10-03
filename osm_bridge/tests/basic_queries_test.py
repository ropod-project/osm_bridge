from osm_bridge.config.config_file_reader import ConfigFileReader
from osm_bridge.osm_bridge_class import OSMBridge

import unittest

class TestConfiguration(unittest.TestCase):

    def setUp(self):
        self.config_params = ConfigFileReader.load("test_config.yaml")
        self.osm_bridge = OSMBridge(self.config_params)

    def test_info_queries(self): 
        result_node = self.osm_bridge.query(ids=[4865],data_type='node',query_type='info')
        self.assertEqual(len(result_node[0]), 1)

        result_way = self.osm_bridge.query(ids=[499],data_type='way',query_type='info')
        self.assertEqual(len(result_way[1]), 1)

        result_relation = self.osm_bridge.query(ids=[149],data_type='relation',query_type='info')
        self.assertEqual(len(result_relation[2]), 1)

        result_relation_role = self.osm_bridge.query(ids=[149],data_type='relation',query_type='info',role='geometry',role_type='way')
        self.assertEqual(len(result_relation_role[1]), 1)

    def test_geometry_queries(self): 
        result_geometry = self.osm_bridge.query(ids=[4865],data_type='node',query_type='geometry')
        self.assertEqual(len(result_geometry[1]), 1)

    def test_topological_node_queries(self): 
        result_topological_node = self.osm_bridge.query(ids=[1216],data_type='way',query_type='topological_node')
        self.assertEqual(len(result_topological_node[0]), 1)

    def test_graph_queries(self): 
        result_graph = self.osm_bridge.query(ids=[4865],data_type='node',query_type='graph')
        self.assertEqual(len(result_graph[1]), 2)



if __name__ == '__main__':
    unittest.main()
