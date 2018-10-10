from osm_bridge import OSMBridge
from structs.wm.point import Point
from osm_adapter import OSMAdapter
from structs.osm.node import Node

import unittest

class TestOSMBridge(unittest.TestCase):

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

    def test_get_feature(self): 
        f = self.osm_bridge.get_feature(4865)
        self.assertEqual(f.id, 4865)

    def test_get_side(self): 
        s = self.osm_bridge.get_side(99999)
        assert s.id is None

    def test_get_door(self):
        d = self.osm_bridge.get_door(161)
        self.assertEqual(d.id,161)
        assert d.geometry is not None
        assert d.topology is not None
        assert len(d.sides) == 0 

    def test_get_wall(self):
        d = self.osm_bridge.get_wall(99999)
        assert d.id is None

    def test_get_local_area(self):
        l = self.osm_bridge.get_local_area(173)
        assert l.id == 173
        assert l.geometry is not None
        assert l.topology is not None

    def test_get_connection(self):
        c = self.osm_bridge.get_connection(1199)
        assert c.id == 1199
        assert len(c.points) > 0


if __name__ == '__main__':
    unittest.main()
