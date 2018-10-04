from osm_bridge import OSMBridge

import unittest

class TestConfiguration(unittest.TestCase):

    def setUp(self):
        pass

    def test_overpass_connection_success(self):
        osm_bridge = OSMBridge()
        status = osm_bridge.test_overpass_connection()
        self.assertTrue(status)

    def test_overpass_connection_failure(self):
        osm_bridge = OSMBridge(server_port=80)
        status = osm_bridge.test_overpass_connection()
        self.assertFalse(status)


if __name__ == '__main__':
    unittest.main()
