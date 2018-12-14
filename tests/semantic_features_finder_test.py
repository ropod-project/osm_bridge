###############################################################################
# NOTE!!!!!!!!!
# This tests requires BRSU OSM database

# TODO: modify these tests to work with AMK database
###############################################################################
from OBL import OSMBridge
from OBL import SemanticFeaturesFinder
import unittest

class TestSemanticFeaturesFinder(unittest.TestCase):
    '''
    Unit tests for local area finder class 
    '''

    def setUp(self):
        self.osm_bridge = OSMBridge(global_origin=[50.7800401, 7.18226])
        self.semantic_feature_finder = SemanticFeaturesFinder(self.osm_bridge)

    def test_feature_finder(self):
        features = self.semantic_feature_finder.get_features('BRSU_C_L0_RoomC022') 
        self.assertEqual(len(features),5)

    def test_check_intersection(self):
        pt1 = self.osm_bridge.get_point(333)
        pt2 = self.osm_bridge.get_point(334)
        line1 = self.semantic_feature_finder._line(pt1, pt2)

        pt1 = self.osm_bridge.get_point(1015)
        pt2 = self.osm_bridge.get_point(1013)
        line2 = self.semantic_feature_finder._line(pt1, pt2)

        pt1 = self.osm_bridge.get_point(1013)
        pt2 = self.osm_bridge.get_point(1014)
        line3 = self.semantic_feature_finder._line(pt1, pt2)

        pt1 = self.osm_bridge.get_point(1021)
        pt2 = self.osm_bridge.get_point(1015)
        line4 = self.semantic_feature_finder._line(pt1, pt2)

        print(self.semantic_feature_finder._check_intersection(line1, line2))
        print(self.semantic_feature_finder._check_intersection(line1, line3))
        print(self.semantic_feature_finder._check_intersection(line1, line4))

        pt1 = self.osm_bridge.get_point(396)
        pt2 = self.osm_bridge.get_point(395)
        line5 = self.semantic_feature_finder._line(pt1, pt2)
        print(self.semantic_feature_finder._check_intersection(line5, line4))

        pt1 = self.osm_bridge.get_point(393)
        pt2 = self.osm_bridge.get_point(394)
        line6 = self.semantic_feature_finder._line(pt1, pt2)
        print(self.semantic_feature_finder._check_intersection(line6, line4))

if __name__ == '__main__':
    unittest.main()

