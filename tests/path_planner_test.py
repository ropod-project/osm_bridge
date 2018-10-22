from osm_bridge import OSMBridge
from path_planner import PathPlanner

import unittest

class TestPathPlanner(unittest.TestCase):

    def setUp(self):
        self.osm_bridge = OSMBridge()
        self.path_planner = PathPlanner(self.osm_bridge)

    def test_global_plan_same_floor(self):
        building = self.osm_bridge.get_building('AMK')
        start_floor = self.osm_bridge.get_floor('AMK_L-1')
        destination_floor = self.osm_bridge.get_floor('AMK_L-1')
        start = self.osm_bridge.get_corridor('AMK_B_L-1_C1')
        destination = self.osm_bridge.get_corridor('AMK_D_L-1_C41')
        self.path_planner.get_global_plan(start_floor, destination_floor, start, destination, building.elevators)

    def test_global_plan_different_floors(self):
        building = self.osm_bridge.get_building('AMK')
        start_floor = self.osm_bridge.get_floor('AMK_L-1')
        destination_floor = self.osm_bridge.get_floor('AMK_L4')
        start = self.osm_bridge.get_corridor('AMK_D_L-1_C41')
        destination = self.osm_bridge.get_corridor('AMK_B_L4_C1')
        self.path_planner.get_global_plan(start_floor, destination_floor, start, destination, building.elevators)
        
if __name__ == '__main__':
    unittest.main()
