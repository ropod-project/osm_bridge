from OBL import OSMAdapter

import unittest


class TestConfiguration(unittest.TestCase):

    def setUp(self):
        pass

    def test_overpass_connection_success(self):
        osm_adapter = OSMAdapter()
        status = osm_adapter.test_overpass_connection()
        self.assertTrue(status)

    def test_overpass_connection_failure(self):
        self.assertRaises(Exception, OSMAdapter, server_port=80)

if __name__ == '__main__':
    unittest.main()
