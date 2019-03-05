from OBL import OSMBridge

import unittest


class TestLocalAreaFinder(unittest.TestCase):
    '''
    Unit tests for local area finder class 
    '''

    def setUp(self):
        self.osm_bridge = OSMBridge()

    def test_given_area_name_inside_la_with_xy(self):
        """TODO: Docstring for test_given_area_name_inside_la_with_xy.

        """
        area_name = "AMK_B_L-1_C29"
        expected_local_area_ref = "AMK_B_L-1_C29_LA1"
        x = 14.054641069320496
        y = -20.23611060809344
        local_area = self.osm_bridge.get_local_area(
            x=x, y=y, area_name=area_name, isLatlong=False)
        self.assertEqual(local_area.ref, expected_local_area_ref)

    def test_given_area_name_outside_la_with_xy(self):
        """TODO: Docstring for test_given_area_name_outside_la_with_xy.

        """
        area_name = "AMK_B_L-1_C29"
        expected_local_area_ref = "AMK_B_L-1_C29_LA1"
        x = 13.190239037096035
        y = -20.165316094644368
        local_area = self.osm_bridge.get_local_area(
            x=x, y=y, area_name=area_name, isLatlong=False)
        self.assertEqual(local_area.ref, expected_local_area_ref)

    def test_given_area_name_inside_la_with_latlong(self):
        """TODO: Docstring for test_given_area_name_inside_la_with_xy.

        """
        area_name = "AMK_B_L-1_C29"
        expected_local_area_ref = "AMK_B_L-1_C29_LA1"
        latitude = 50.1361671
        longitude = 8.6476004
        local_area = self.osm_bridge.get_local_area(
            x=latitude, y=longitude, area_name=area_name, isLatlong=True)
        self.assertEqual(local_area.ref, expected_local_area_ref)

    def test_given_area_name_outside_la_with_latlong(self):
        """TODO: Docstring for test_given_area_name_outside_la_with_xy.

        """
        area_name = "AMK_B_L-1_C29"
        expected_local_area_ref = "AMK_B_L-1_C29_LA1"
        latitude = 50.1361677
        longitude = 8.6475883
        local_area = self.osm_bridge.get_local_area(
            x=latitude, y=longitude, area_name=area_name, isLatlong=True)
        self.assertEqual(local_area.ref, expected_local_area_ref)

    def test_not_given_area_name(self):
        """TODO: Docstring for test_not_given_area_name.

        """
        expected_local_area_ref = "AMK_B_L-1_C29_LA1"
        latitude = 50.1361677
        longitude = 8.6475883
        local_area = self.osm_bridge.get_local_area(
            x=latitude, y=longitude, isLatlong=True, floor_name="AMK_L-1")
        self.assertEqual(local_area.ref, expected_local_area_ref)

    def test_not_given_area_name_edge_case(self):
        """TODO: Docstring for test_not_given_area_name.
        Here, the position given is such that, the nearest topology node is actually another area

        """
        expected_local_area_ref = "AMK_B_L-1_C23_LA2"
        latitude = 50.1363136
        longitude = 8.6475123
        local_area = self.osm_bridge.get_local_area(
            x=latitude, y=longitude, isLatlong=True, floor_name="AMK_L-1")
        self.assertEqual(local_area.ref, expected_local_area_ref)

    def test_given_area_name_with_behaviour(self):
        """TODO: Docstring for test_given_area_name_with_behaviour.
        :returns: TODO

        """
        area_name = "AMK_D_L-1_C41"
        expected_local_area_ref = "AMK_D_L-1_C41_LA2"
        local_area = self.osm_bridge.get_local_area(
            area_name=area_name, behaviour="docking")
        self.assertEqual(local_area.ref, expected_local_area_ref)

        area_name = "AMK_A_L-1_RoomBU21"
        expected_local_area_ref = "AMK_A_L-1_RoomBU21_LA1"
        local_area = self.osm_bridge.get_local_area(
            area_name=area_name, behaviour="undocking")
        self.assertEqual(local_area.ref, expected_local_area_ref)

    def test_not_given_area_name_with_behaviour(self):
        """This test takes more than 10 seconds to run, as it uses a brute force approach
        :returns: TODO

        """
        floor_name = "AMK_L-1"
        expected_local_area_ref = "AMK_D_L-1_C41_LA2"
        local_area = self.osm_bridge.get_local_area(
            floor_name=floor_name, behaviour="docking")
        self.assertEqual(local_area.ref, expected_local_area_ref)

        floor_name = "AMK_L-1"
        expected_local_area_ref = "AMK_A_L-1_RoomBU21_LA1"
        local_area = self.osm_bridge.get_local_area(
            floor_name=floor_name, behaviour="undocking")
        self.assertEqual(local_area.ref, expected_local_area_ref)

if __name__ == '__main__':
    unittest.main()
