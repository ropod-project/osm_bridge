from osm_adapter import OSMAdapter

import unittest

class TestConfiguration(unittest.TestCase):

    def setUp(self):
        pass

    def test_overpass_connection_success(self):
        osm_adapter = OSMAdapter()
        status = osm_adapter.test_overpass_connection()
        self.assertTrue(status)

    def test_overpass_connection_failure(self):
        osm_adapter = OSMAdapter(server_port=80)
        status = osm_adapter.test_overpass_connection()
        self.assertFalse(status)


if __name__ == '__main__':
    unittest.main()
