from osm_bridge.config.config_file_reader import ConfigFileReader
from osm_bridge.osm_bridge_class import OSMBridge

import unittest

class TestConfiguration(unittest.TestCase):

    def setUp(self):
        self.config_params = ConfigFileReader.load("test_config.yaml")

    def test_overpass_connection_success(self):
        osm_bridge = OSMBridge(self.config_params)
        status = osm_bridge.test_overpass_connection()
        self.assertTrue(status)

    def test_overpass_connection_failure(self):
        self.config_params.overpass_server_port = 80
        osm_bridge = OSMBridge(self.config_params)
        status = osm_bridge.test_overpass_connection()
        self.assertFalse(status)


if __name__ == '__main__':
    unittest.main()
