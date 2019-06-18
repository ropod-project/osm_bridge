from OBL import OSMBridge
from OBL import PathPlanner
from OBL.planner.navigation_path_planner import NavigationPathPlanner
from OBL.planner.global_path_planner import GlobalPathPlanner

import unittest


class TestPathPlanner(unittest.TestCase):

    def setUp(self):
        self.osm_bridge = OSMBridge()
        # self.global_origin = [50.7800401, 7.18226]  # uni (coordinates of node id 1307)
        # self.osm_bridge = OSMBridge(global_origin=self.global_origin)
        self.global_path_planner = GlobalPathPlanner(self.osm_bridge)
        self.navigation_path_planner = NavigationPathPlanner(self.osm_bridge)
        self.semantic_global_path = None

    def test_global_plan_same_floor_plus_local_planner(self):
        building = self.osm_bridge.get_building('AMK')
        start_floor = self.osm_bridge.get_floor('AMK_L-1')
        destination_floor = self.osm_bridge.get_floor('AMK_L-1')
        start = self.osm_bridge.get_corridor('AMK_B_L-1_C1')
        destination = self.osm_bridge.get_corridor('AMK_D_L-1_C41')
        global_path = self.global_path_planner.plan(
            start_floor, destination_floor, start, destination, building.elevators)

        start_local = self.osm_bridge.get_local_area('AMK_D_L-1_C41_LA1')
        destination_local = self.osm_bridge.get_local_area('AMK_B_L-1_C2_LA1')
        path = self.navigation_path_planner.plan(
            start_floor, destination_floor, start_local, destination_local, global_path)

    def test_global_plan_different_floors_plus_local_planner(self):
        building = self.osm_bridge.get_building('AMK')
        start_floor = self.osm_bridge.get_floor('AMK_L-1')
        destination_floor = self.osm_bridge.get_floor('AMK_L4')

        start_global = self.osm_bridge.get_corridor('AMK_D_L-1_C41')
        destination_global = self.osm_bridge.get_corridor('AMK_B_L4_C1')

        global_path = self.global_path_planner.plan(
            start_floor, destination_floor, start_global, destination_global, building.elevators)

        start_local = self.osm_bridge.get_local_area('AMK_D_L-1_C41_LA1')
        destination_local = self.osm_bridge.get_local_area('AMK_B_L4_C1_LA1')
        path = self.navigation_path_planner.plan(
            start_floor, destination_floor, start_local, destination_local, global_path)

#         for pt in path:
#             print(pt)
#             print(pt.exit_door)
#             print(pt.navigation_areas)
#             print("---------------------------------------------")
        self.assertEqual(path[1].id, 119)
        self.assertEqual(len(path), 25)

    def test_overall_path_planner(self):
        path_planner = PathPlanner(self.osm_bridge)
        path_planner.set_building('AMK')
        path = path_planner.get_path_plan(
            start_floor='AMK_L-1',
            destination_floor='AMK_L4',
            start_area='AMK_D_L-1_C41',
            destination_area='AMK_B_L4_C1',
            start_local_area='AMK_D_L-1_C41_LA1',
            destination_local_area='AMK_B_L4_C1_LA1')
        print(path)
        self.assertEqual(path[1].id, 119)
        self.assertEqual(len(path), 25)

    # def test_overall_path_planner(self):
    #     path_planner = PathPlanner(self.osm_bridge)
    #     path_planner.set_building('BRSU')
    #     path = path_planner.get_path_plan(
    #             destination_floor='BRSU_L0',
    #             start_floor='BRSU_L0',
    #             start_area='BRSU_C_L0_C9',
    #             start_local_area='BRSU_C_L0_C9_LA1',
    #             destination_area='BRSU_A_L0_C9',
    #             destination_local_area='BRSU_C_L0_C9_LA2'
    #             )
    #     print(path)

    def test_dynamic_path_planner_blocked_with_traffic_rules(self):
        path_planner = PathPlanner(self.osm_bridge)
        path_planner.set_building('AMK')

        # path planning should fail here as connections are blocked and traffic rules are
        # still in effect
        with self.assertRaises(Exception) as context:
            self.assertRaises(path_planner.get_path_plan(
                start_floor='AMK_L-1',
                destination_floor='AMK_L4',
                start_area='AMK_D_L-1_C41',
                destination_area='AMK_B_L4_C1',
                start_local_area='AMK_D_L-1_C41_LA1',
                destination_local_area='AMK_B_L4_C1_LA1',
                blocked_connections=[
                    ['AMK_C_L-1_C36_LA2', 'AMK_C_L-1_C35_LA2'],
                    ['AMK_C_L-1_C35_LA2', 'AMK_C_L-1_C34_Door1']],
                relax_traffic_rules=False))
        self.assertTrue("Couldn't plan the path" in str(context.exception))

    def test_dynamic_path_planner_blocked_wo_traffic_rules(self):
        path_planner = PathPlanner(self.osm_bridge)
        path_planner.set_building('AMK')

        try:
            # even though connections are blocked since traffic rules are relaxed
            # path planning should be successful in this case
            path_planner.get_path_plan(
                start_floor='AMK_L-1',
                destination_floor='AMK_L4',
                start_area='AMK_D_L-1_C41',
                destination_area='AMK_B_L4_C1',
                start_local_area='AMK_D_L-1_C41_LA1',
                destination_local_area='AMK_B_L4_C1_LA1',
                blocked_connections=[
                    ['AMK_C_L-1_C36_LA2', 'AMK_C_L-1_C35_LA2'],
                    ['AMK_C_L-1_C35_LA2', 'AMK_C_L-1_C34_Door1']],
                relax_traffic_rules=True)
        except:
            self.fail("In this case path shhould be successfully planned")

    def test_get_estimated_path_distance(self):
        path_planner = PathPlanner(self.osm_bridge)
        path_planner.set_building('AMK')

        try:
            # even though connections are blocked since traffic rules are relaxed
            # path planning should be successful in this case
            distance = path_planner.get_estimated_path_distance(start_floor='AMK_L-1',
                                                                destination_floor='AMK_L4',
                                                                start_area='AMK_D_L-1_C41',
                                                                destination_area='AMK_B_L4_C1')
            print("Path distance:", distance)
        except:
            self.fail("In this case path shhould be successfully planned")


if __name__ == '__main__':
    unittest.main()
