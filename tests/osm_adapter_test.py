from OBL import OSMAdapter
import unittest

class TestOSMAdapter(unittest.TestCase):

    def setUp(self):
        self.osm_adapter = OSMAdapter(debug=False)

    def test_get_osm_element_by_id(self): 
        result_node = self.osm_adapter.get_osm_element_by_id(ids=[4865],data_type='node')
        self.assertEqual(len(result_node[0]), 1)

        result_way = self.osm_adapter.get_osm_element_by_id(ids=[499],data_type='way')
        self.assertEqual(len(result_way[1]), 1)

        result_relation = self.osm_adapter.get_osm_element_by_id(ids=[149],data_type='relation')
        self.assertEqual(len(result_relation[2]), 1)

        result_relation_role = self.osm_adapter.get_osm_element_by_id(ids=[149],data_type='relation',role='geometry',role_type='way')
        self.assertEqual(len(result_relation_role[1]), 1)

    def test_get_osm_element_by_multiple_id(self): 
        nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=[4866,4865,4864],data_type='node')
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].id, 4866)
        self.assertEqual(nodes[1].id, 4865)
        self.assertEqual(nodes[2].id, 4864)

        __,way,__ = self.osm_adapter.get_osm_element_by_id(ids=[500,501,499],data_type='way')
        self.assertEqual(len(way), 3)
        self.assertEqual(way[0].id, 500)
        self.assertEqual(way[1].id, 501)
        self.assertEqual(way[2].id, 499)

        __,__,relation = self.osm_adapter.get_osm_element_by_id(ids=[149,151,150],data_type='relation')
        self.assertEqual(len(relation), 3)
        self.assertEqual(relation[0].id, 149)
        self.assertEqual(relation[1].id, 151)
        self.assertEqual(relation[2].id, 150)

        __,way,__ = self.osm_adapter.get_osm_element_by_id(ids=[150,151,149],data_type='relation',role='geometry',role_type='way')
        self.assertEqual(len(way), 3)
        self.assertEqual(way[0].id, 1309)
        self.assertEqual(way[1].id, 1312)
        self.assertEqual(way[2].id, 1352)
        
    def test_search_by_tag(self):
        result_node = self.osm_adapter.search_by_tag(data_type='node',key='highway',value='elevator')
        self.assertTrue(len(result_node[0]) >  0)

        result_way = self.osm_adapter.search_by_tag(data_type='way',key='highway',value='footway')
        self.assertTrue(len(result_way[1]) >  0)

        """ search with multiple tags"""
        __,result_ways,__ = self.osm_adapter.search_by_tag(data_type='way', key_val_dict={'level':'-1','indoor':'wall'})
        self.assertEqual(len(result_ways), 198)

        result_relation = self.osm_adapter.search_by_tag(data_type='relation',key='type',value='building')
        self.assertTrue(len(result_relation[2]) >  0)

    def test_get_parent(self):
        __,__,result_relation = self.osm_adapter.get_parent(4865, 'node', 'topology', role_type='', role='')
        self.assertTrue(len(result_relation) > 0)

        __,result_way,__ = self.osm_adapter.get_parent(4865, 'node', 'topology', 'way', 'geometry')
        self.assertTrue(len(result_way) > 0)



if __name__ == '__main__':
    unittest.main()
