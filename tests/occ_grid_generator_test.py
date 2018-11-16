from OBL import OSMBridge
from OBL import OccGridGenerator

import unittest
import os

class TestOccGridGenerator(unittest.TestCase):
    '''
    Unit tests for occupancy grid generator class 
    '''

    def setUp(self):
        self.osm_bridge = OSMBridge()
        self.server_ip = "127.0.0.1"
        self.server_port = 8000
        self.global_origin = [50.1363485, 8.6474024] # amk
#         self.global_origin = [50.7800401, 7.18226]  # uni (coordinates of node id 1307)

        self.local_offset = [25, 25] # amk
#         self.local_offset = [25, 80] # brsu
        self.floor = 4
        self.debug = True

    def test_require_osm_bridge(self) :
        self.assertRaises(Exception, OccGridGenerator(debug=self.debug))

    def test_require_server_info_and_global_origin(self) :
        self.assertRaises(Exception, OccGridGenerator(server_ip=self.server_ip, server_port=self.server_port, debug=self.debug))

    def test_map_files_exists_with_bridge_object(self):
        occ_grid_generator = OccGridGenerator(osm_bridge=self.osm_bridge, local_offset=self.local_offset, debug=self.debug)
        filename = occ_grid_generator.generate_map(floor=-1)
        print(filename)
        self.assertTrue(os.path.isfile(filename))

    def test_map_files_exists_with_server_info(self):
        occ_grid_generator = OccGridGenerator(server_ip=self.server_ip, \
                server_port=self.server_port, global_origin=self.global_origin, local_offset=self.local_offset, debug=self.debug)
        filename = occ_grid_generator.generate_map(floor=-1)
        print(filename)
        self.assertTrue(os.path.isfile(filename))

#     def test_map_files_exists_multiple_floor(self):
#         self.occ_grid_generator.generate_map_all_floor(building="AMK")
#         file_list = os.listdir("../")
#         for (dirpath, dirnames, filenames) in os.walk("../"):
#             self.assertIn("maps", dirnames)
#             break
#         self.assertIn("map_floor_-1.pgm", os.listdir("../maps/"))
#         self.assertIn("map_floor_-1.yaml", os.listdir("../maps/"))
#         self.assertIn("map_floor_4.pgm", os.listdir("../maps/"))
#         self.assertIn("map_floor_4.yaml", os.listdir("../maps/"))
        

if __name__ == '__main__':
    unittest.main()


