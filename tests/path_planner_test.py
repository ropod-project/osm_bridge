from osm_bridge import OSMBridge
from path_planner import PathPlanner
from planner.navigation_path_planner import NavigationPathPlanner
from planner.global_path_planner import GlobalPathPlanner

import unittest

class TestPathPlanner(unittest.TestCase):

    def setUp(self):
        self.osm_bridge = OSMBridge()
        self.global_path_planner = GlobalPathPlanner(self.osm_bridge)
        self.navigation_path_planner = NavigationPathPlanner(self.osm_bridge)
        self.semantic_global_path = None

    def test_global_plan_same_floor(self):
        building = self.osm_bridge.get_building('AMK')
        start_floor = self.osm_bridge.get_floor('AMK_L-1')
        destination_floor = self.osm_bridge.get_floor('AMK_L-1')
        start = self.osm_bridge.get_corridor('AMK_B_L-1_C1')
        destination = self.osm_bridge.get_corridor('AMK_D_L-1_C41')
        self.global_path_planner.plan(start_floor, destination_floor, start, destination, building.elevators)

    def test_global_plan_different_floors_plus_local_planner(self):
        building = self.osm_bridge.get_building('AMK')
        start_floor = self.osm_bridge.get_floor('AMK_L-1')
        destination_floor = self.osm_bridge.get_floor('AMK_L4')

        start_global = self.osm_bridge.get_corridor('AMK_D_L-1_C41')
        destination_global = self.osm_bridge.get_corridor('AMK_B_L4_C1')

        global_path = self.global_path_planner.plan(start_floor, destination_floor, start_global, destination_global, building.elevators)

        start_local = self.osm_bridge.get_local_area('AMK_D_L-1_C41_LA1')
        destination_local = self.osm_bridge.get_local_area('AMK_B_L4_C1_LA1')
        path = self.navigation_path_planner.plan(start_floor, destination_floor, start_local, destination_local, global_path)

        for pt in path:
            print(pt)
            print(pt.exit_door)
            print(pt.navigation_areas)
            print("---------------------------------------------")
        
if __name__ == '__main__':
    unittest.main()
