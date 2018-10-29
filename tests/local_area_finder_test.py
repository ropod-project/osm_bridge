from osm_bridge import OSMBridge
from planner.local_area_finder import LocalAreaFinder

import unittest

class TestLocalAreaFinder(unittest.TestCase):
    '''
    Unit tests for local area finder class 
    '''

    def setUp(self):
        self.osm_bridge = OSMBridge()
        self.local_area_finder = LocalAreaFinder(self.osm_bridge, debug=False)

    def test_given_area_name_inside_la_with_xy(self):
        """TODO: Docstring for test_given_area_name_inside_la_with_xy.

        """
        area_name = "AMK_B_L-1_C29"
        expected_local_area_ref = "AMK_B_L-1_C29_LA1"
        x = 1909.5119518548017
        y = 2258.2658047322184
        local_area = self.local_area_finder.get_local_area(x, y, area_name=area_name, isLatlong=False)
        self.assertEqual(local_area.ref, expected_local_area_ref)

    def test_given_area_name_outside_la_with_xy(self):
        """TODO: Docstring for test_given_area_name_outside_la_with_xy.

        """
        area_name = "AMK_B_L-1_C29"
        expected_local_area_ref = "AMK_B_L-1_C29_LA1"
        x = 1909.5119518548017
        y = 2258.2658047322184
        local_area = self.local_area_finder.get_local_area(x, y, area_name=area_name, isLatlong=False)
        self.assertEqual(local_area.ref, expected_local_area_ref)

    def test_given_area_name_inside_la_with_latlong(self):
        """TODO: Docstring for test_given_area_name_inside_la_with_xy.

        """
        area_name = "AMK_B_L-1_C29"
        expected_local_area_ref = "AMK_B_L-1_C29_LA1"
        latitude = 50.1361671
        longitude = 8.6476004
        local_area = self.local_area_finder.get_local_area(latitude, longitude, area_name=area_name, isLatlong=True)
        self.assertEqual(local_area.ref, expected_local_area_ref)

    def test_given_area_name_outside_la_with_latlong(self):
        """TODO: Docstring for test_given_area_name_outside_la_with_xy.

        """
        area_name = "AMK_B_L-1_C29"
        expected_local_area_ref = "AMK_B_L-1_C29_LA1"
        latitude = 50.1361677
        longitude = 8.6475883
        local_area = self.local_area_finder.get_local_area(latitude, longitude, area_name=area_name, isLatlong=True)
        self.assertEqual(local_area.ref, expected_local_area_ref)

    def test_not_given_area_name(self):
        """TODO: Docstring for test_not_given_area_name.

        """
        expected_local_area_ref = "AMK_B_L-1_C29_LA1"
        latitude = 50.1361677
        longitude = 8.6475883
        local_area = self.local_area_finder.get_local_area(latitude, longitude, isLatlong=True, floor_name="AMK_L-1")
        self.assertEqual(local_area.ref, expected_local_area_ref)

    def test_not_given_area_name_edge_case(self):
        """TODO: Docstring for test_not_given_area_name.
        Here, the position given is such that, the nearest topology node is actually another area

        """
        expected_local_area_ref = "AMK_B_L-1_C23_LA2"
        latitude = 50.1363136
        longitude = 8.6475123
        local_area = self.local_area_finder.get_local_area(latitude, longitude, isLatlong=True, floor_name="AMK_L-1")
        self.assertEqual(local_area.ref, expected_local_area_ref)

if __name__ == '__main__':
    unittest.main()

