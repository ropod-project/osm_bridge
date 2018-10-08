from osm_bridge import OSMBridge
from structs.wm.feature import Feature
from structs.wm.geometry import Point, Shape

import unittest

class TestWMQueries(unittest.TestCase):

    def setUp(self):
        self.osm_bridge = OSMBridge()

    def test_point_spherical(self):
        Point._coordinate_system = 'spherical'
        p = Point(self.osm_bridge,4865)
        assert p.lat is not None
        assert p.lon is not None
        assert p.x is None
        assert p.y is None

    def test_point_utm(self):
        Point._coordinate_system = 'utm'
        Point._global_origin = [50.1363485, 8.6474024]
        p = Point(self.osm_bridge,4865)
        assert p.lat is None
        assert p.lon is None
        assert p.x is not None
        assert p.y is not None

    def test_shape(self):
        s = Shape(self.osm_bridge,499)
        assert len(s.points) > 0

    def test_get_feature(self): 
        f = self.osm_bridge.get_feature(4865)
        self.assertEqual(f.id, 4865)


if __name__ == '__main__':
    unittest.main()
