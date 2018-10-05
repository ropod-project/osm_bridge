from osm_bridge import OSMBridge
from structs.wm.feature import Feature

import unittest

class TestWMQueries(unittest.TestCase):

    def setUp(self):
        self.osm_bridge = OSMBridge()

    def test_get_feature(self): 
        f = self.osm_bridge.get_feature(4865)
        self.assertEqual(f.id, 4865)


if __name__ == '__main__':
    unittest.main()
