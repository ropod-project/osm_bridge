from OBL import OSMBridge
from OBL.structs.wm.point import Point
from OBL import OSMAdapter

import unittest


class TestOSMBridge(unittest.TestCase):

    def setUp(self):
        self.osm_bridge = OSMBridge()
        self.osm_adapter = OSMAdapter()

    def test_point(self):
        node_result, __, __ = self.osm_adapter.get_osm_element_by_id(
            ids=[4865], data_type='node')
        Point.coordinate_system = 'spherical'
        p = self.osm_bridge.get_point(node_result[0])
        assert p.lat is not None
        assert p.lon is not None
        assert p.x is not None
        assert p.y is not None

        # point by id
        p = self.osm_bridge.get_point(4865)
        assert p.id == 4865

    def test_shape(self):
        # point by id
        s = self.osm_bridge.get_shape(1021)
        assert len(s.points) > 0

    def test_get_feature_by_id(self):
        f = self.osm_bridge.get_feature(4865)
        self.assertEqual(f.id, 4865)

    def test_get_side_by_id(self):
        self.assertRaises(Exception, self.osm_bridge.get_side, 99999)

    def test_get_door_by_id(self):
        d = self.osm_bridge.get_door(161)
        self.assertEqual(d.id, 161)
        assert d.geometry is not None
        assert d.topology is not None
        assert d.sides is None

    def test_get_door_by_name(self):
        d = self.osm_bridge.get_door('AMK_B_L-1_C2_Door1')
        self.assertEqual(d.id, 161)
        assert d.geometry is not None
        assert d.topology is not None
        assert d.sides is None

    def test_get_door_from_point(self):
        node_result, __, __ = self.osm_adapter.get_osm_element_by_id(
            ids=[4978], data_type='node')
        Point.coordinate_system = 'cartesian'
        Point.global_origin = [50.1363485, 8.6474024]
        p = Point(node_result[0])
        d = self.osm_bridge.get_door(p)
        self.assertEqual(d.id, 150)

    def test_get_wall_by_id(self):
        self.assertRaises(Exception, self.osm_bridge.get_wall, 99999)

    def test_get_local_area_by_id(self):
        l = self.osm_bridge.get_local_area(173)
        assert l.id == 173
        assert l.geometry is not None
        assert l.topology is not None

    def test_get_local_area_by_name(self):
        l = self.osm_bridge.get_local_area('AMK_B_L4_RoomB404_LA2')
        assert l.id == 173
        assert l.geometry is not None
        assert l.topology is not None

    def test_get_local_area_from_point(self):
        node_result, __, __ = self.osm_adapter.get_osm_element_by_id(
            ids=[4743], data_type='node')
        Point.coordinate_system = 'cartesian'
        Point.global_origin = [50.1363485, 8.6474024]
        p = Point(node_result[0])
        l = self.osm_bridge.get_local_area(p)
        self.assertEqual(l.id, 27)

    def test_get_connection_by_id(self):
        c = self.osm_bridge.get_connection(1199)
        assert c.id == 1199
        assert len(c.points) > 0

    def test_get_room_by_id(self):
        r = self.osm_bridge.get_room(22)
        assert r.id == 22
        assert r.walls is None
        assert r.doors is not None
        assert r.local_areas is not None
        assert r.connections is not None
        assert r.geometry is not None
        assert r.topology is not None

    def test_get_room_by_ref(self):
        r = self.osm_bridge.get_room('AMK_B_L4_RoomB401')
        assert r.id == 22
        assert r.walls is None
        assert r.doors is not None
        assert r.local_areas is not None
        assert r.connections is not None
        assert r.geometry is not None
        assert r.topology is not None

    def test_get_room_from_point(self):
        node_result, __, __ = self.osm_adapter.get_osm_element_by_id(
            ids=[4678], data_type='node')
        Point.coordinate_system = 'cartesian'
        Point.global_origin = [50.1363485, 8.6474024]
        p = Point(node_result[0])
        r = self.osm_bridge.get_room(p)
        self.assertEqual(r.id, 22)

    def test_get_corridor_by_id(self):
        r = self.osm_bridge.get_corridor(140)
        assert r.id == 140
        assert r.walls is None
        assert r.doors is None
        assert r.local_areas is not None
        assert r.connections is not None
        assert r.geometry is not None
        assert r.topology is not None

    def test_get_corridor_by_ref(self):
        r = self.osm_bridge.get_corridor('AMK_B_L-1_C14')
        assert r.id == 140
        assert r.walls is None
        assert r.doors is None
        assert r.local_areas is not None
        assert r.connections is not None
        assert r.geometry is not None
        assert r.topology is not None

    def test_get_corridor_from_point(self):
        node_result, __, __ = self.osm_adapter.get_osm_element_by_id(
            ids=[4666], data_type='node')
        Point.coordinate_system = 'cartesian'
        Point.global_origin = [50.1363485, 8.6474024]
        p = Point(node_result[0])
        c = self.osm_bridge.get_corridor(p)
        self.assertEqual(c.id, 14)

    def test_get_elevator_by_id(self):
        e = self.osm_bridge.get_elevator(5)
        assert e.id == 5
        assert e.walls is None
        assert e.doors is None
        assert e.local_areas is not None
        assert e.connections is not None
        assert e.geometry is not None
        assert e.topology is not None

    def test_get_elevator_by_name(self):
        e = self.osm_bridge.get_elevator('AMK_B_E1')
        assert e.id == 5
        assert e.walls is None
        assert e.doors is None
        assert e.local_areas is not None
        assert e.connections is not None
        assert e.geometry is not None
        assert e.topology is not None

    def test_search_by_scope_for_elevator(self):
        e = self.osm_bridge.get_elevator('AMK_B_E1')
        assert e.id == 5
        la = e.local_area('AMK_B_E1_LA1')
        assert la.id == 163

    def test_get_floor(self):
        f = self.osm_bridge.get_floor(164)
        assert f.id == 164
        assert f.walls is None
        assert f.corridors is not None
        assert f.rooms is not None
        assert f.connections is not None

    def test_get_floor_by_name(self):
        f = self.osm_bridge.get_floor('AMK_L4')
        assert f.id == 164
        assert f.walls is None
        assert f.corridors is not None
        assert f.rooms is not None
        assert f.connections is not None

    def test_search_by_scope_for_floor(self):
        f = self.osm_bridge.get_floor('AMK_L4')
        r = f.room('AMK_B_L4_RoomB401')
        assert r.id == 22

        c = f.corridor('AMK_B_L4_C6')
        assert c.id == 19

    def test_get_building_by_id(self):
        b = self.osm_bridge.get_building(149)
        assert b.geometry is not None
        assert b.id == 149
        assert b.stairs is None
        assert b.elevators is not None
        assert b.floors is not None

    def test_get_building_by_name(self):
        b = self.osm_bridge.get_building('AMK')
        assert b.geometry is not None
        assert b.id == 149
        assert b.stairs is None
        assert b.elevators is not None
        assert b.floors is not None

    def test_search_by_scope_for_building(self):
        b = self.osm_bridge.get_building('AMK')
        f = b.floor('AMK_L4')
        assert f.id == 164

        e = b.elevator('AMK_B_E1')
        assert e.id == 5

        self.assertRaises(Exception, b.stair, 'AMK_B_S1')


if __name__ == '__main__':
    unittest.main()
