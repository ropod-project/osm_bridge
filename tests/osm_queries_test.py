from osm_bridge import OSMBridge

import unittest

class TestConfiguration(unittest.TestCase):

    def setUp(self):
        self.osm_bridge = OSMBridge()

    def test_get_osm_element_by_id(self): 
        result_node = self.osm_bridge.get_osm_element_by_id(ids=[4865],data_type='node')
        self.assertEqual(len(result_node[0]), 1)

        result_way = self.osm_bridge.get_osm_element_by_id(ids=[499],data_type='way')
        self.assertEqual(len(result_way[1]), 1)

        result_relation = self.osm_bridge.get_osm_element_by_id(ids=[149],data_type='relation')
        self.assertEqual(len(result_relation[2]), 1)

        result_relation_role = self.osm_bridge.get_osm_element_by_id(ids=[149],data_type='relation',role='geometry',role_type='way')
        self.assertEqual(len(result_relation_role[1]), 1)


if __name__ == '__main__':
    unittest.main()
