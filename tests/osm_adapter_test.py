from osm_adapter import OSMAdapter
import unittest

class TestOSMAdapter(unittest.TestCase):

    def setUp(self):
        self.osm_adapter = OSMAdapter()

    def test_get_osm_element_by_id(self): 
        result_node = self.osm_adapter.get_osm_element_by_id(ids=[4865],data_type='node')
        self.assertEqual(len(result_node[0]), 1)

        result_way = self.osm_adapter.get_osm_element_by_id(ids=[499],data_type='way')
        self.assertEqual(len(result_way[1]), 1)

        result_relation = self.osm_adapter.get_osm_element_by_id(ids=[149],data_type='relation')
        self.assertEqual(len(result_relation[2]), 1)

        result_relation_role = self.osm_adapter.get_osm_element_by_id(ids=[149],data_type='relation',role='geometry',role_type='way')
        self.assertEqual(len(result_relation_role[1]), 1)

    def test_search_by_tag(self):
        result_node = self.osm_adapter.search_by_tag(data_type='node',key='highway',value='elevator')
        self.assertTrue(len(result_node[0]) >  0)

        result_way = self.osm_adapter.search_by_tag(data_type='way',key='highway',value='footway')
        self.assertTrue(len(result_way[1]) >  0)

        result_relation = self.osm_adapter.search_by_tag(data_type='relation',key='type',value='building')
        self.assertTrue(len(result_relation[2]) >  0)

if __name__ == '__main__':
    unittest.main()
