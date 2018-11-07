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
        self.occ_grid_generator = OccGridGenerator(self.osm_bridge, debug=False)

    def test_map_files_exists(self):
        self.occ_grid_generator.generate_map(floor=-1)
        file_list = os.listdir("../")
        for (dirpath, dirnames, filenames) in os.walk("../"):
            self.assertIn("maps", dirnames)
            break
        self.assertIn("map_floor_-1.pgm", os.listdir("../maps/"))
        self.assertIn("map_floor_-1.yaml", os.listdir("../maps/"))

    def test_map_files_exists_multiple_floor(self):
        self.occ_grid_generator.generate_map_all_floor(building="AMK")
        file_list = os.listdir("../")
        for (dirpath, dirnames, filenames) in os.walk("../"):
            self.assertIn("maps", dirnames)
            break
        self.assertIn("map_floor_-1.pgm", os.listdir("../maps/"))
        self.assertIn("map_floor_-1.yaml", os.listdir("../maps/"))
        self.assertIn("map_floor_4.pgm", os.listdir("../maps/"))
        self.assertIn("map_floor_4.yaml", os.listdir("../maps/"))
        

if __name__ == '__main__':
    unittest.main()


