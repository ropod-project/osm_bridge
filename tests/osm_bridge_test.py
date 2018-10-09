from osm_bridge import OSMBridge
from structs.wm.feature import Feature
from structs.wm.point import Point
from osm_adapter import OSMAdapter
from structs.osm.node import Node

import unittest

class TestWMQueries(unittest.TestCase):

    def setUp(self):
        self.osm_bridge = OSMBridge()
        self.osm_adapter = OSMAdapter()

    def test_point_spherical(self):
        node_result,__,__ = self.osm_adapter.get_osm_element_by_id(ids=[4865],data_type='node')
        Point.coordinate_system = 'spherical'
        p = Point(node_result[0])
        assert p.lat is not None
        assert p.lon is not None
        assert p.x is None
        assert p.y is None

    def test_point_utm(self):
        node_result,__,__ = self.osm_adapter.get_osm_element_by_id(ids=[4865],data_type='node')
        Point.coordinate_system = 'utm'
        Point.global_origin = [50.1363485, 8.6474024]
        p = Point(node_result[0])
        assert p.lat is None
        assert p.lon is None
        assert p.x is not None
        assert p.y is not None

    # def test_shape(self):
    #     s = Shape(self.osm_bridge,499)
    #     assert len(s.points) > 0

    def test_get_feature(self): 
        f = self.osm_bridge.get_feature(4865)
        self.assertEqual(f.id, 4865)


if __name__ == '__main__':
    unittest.main()
