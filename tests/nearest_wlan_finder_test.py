from OBL import OSMBridge
from OBL import NearestWLANFinder

import unittest

class TestNearestWLANFinder(unittest.TestCase):
    '''
    Unit tests for nearest wlan finder class 
    '''

    def setUp(self):
        self.global_origin = [50.7800401, 7.18226]  # uni (coordinates of node id 1307)
        self.osm_bridge = OSMBridge(global_origin=self.global_origin)
        self.wlan_finder = NearestWLANFinder(self.osm_bridge)
        self.floor_name = 'BRSU_L0'

    def test_wlan_finder_given_x_and_y(self):
        x = 0.0
        y = 5.0
        point_obj = self.wlan_finder.get_nearest_wlan(x=x, y=y, floor_name=self.floor_name)
        self.assertEqual(point_obj.id, 2658)

    def test_wlan_finder_given_area_name(self):
        area_name = 'BRSU_A_L0_A1'
        point_obj = self.wlan_finder.get_nearest_wlan(area_name=area_name)
        self.assertEqual(point_obj.id, 2658)

    def test_wlan_finder_given_local_area_name(self):
        local_area_name = 'BRSU_A_L0_A1_LA1'
        point_obj = self.wlan_finder.get_nearest_wlan(local_area_name=local_area_name, floor_name=self.floor_name)
        self.assertEqual(point_obj.id, 2658)

    def test_wlan_finder_without_any_info(self):
        point_obj = self.wlan_finder.get_nearest_wlan()
        self.assertIsNone(point_obj)


if __name__ == '__main__':
    unittest.main()
