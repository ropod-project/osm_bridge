from osm_bridge import OSMBridge
from path_planner import PathPlanner

import unittest

class TestPathPlanner(unittest.TestCase):

    def setUp(self):
        self.osm_bridge = OSMBridge()
        self.path_planner = PathPlanner(self.osm_bridge)

    def test_global_plan(self):
        building = self.osm_bridge.get_building('AMK')
        start_floor = self.osm_bridge.get_floor('AMK_L-1')
        destination_floor = self.osm_bridge.get_floor('AMK_L-1')
        start = self.osm_bridge.get_corridor('AMK_B_L-1_C1')
        destination = self.osm_bridge.get_corridor('AMK_D_L-1_C41')
        self.path_planner.get_global_plan(building, start_floor, destination_floor, start, destination)
        
if __name__ == '__main__':
    unittest.main()
