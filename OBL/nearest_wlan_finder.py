import logging
import sys
from OBL.structs.wm.point import Point

class NearestWLANFinder(object):

    """Finds the nearest wlan access point to a give position (x, y) of robot"""

    # default values
    _debug = False
    _isLatlong = False

    def __init__(self, osm_bridge, *args, **kwargs):
        self.osm_bridge = osm_bridge

        self.logger = logging.getLogger("NearestWLANFinder")
        # if kwargs.get("debug", self._debug):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def get_nearest_wlan(self, **kwargs):
        """gets the Point object with wlan tag nearest to robot's pose.

        :key word arguments:
        :x: float
        :y: float
        :area_name: string or int
        :local_area_name: string or int
        :floor_name: string or int

        :returns: Point object

        one of the following three must be provided to get a non None return
        - x and y and floor_name
        - area_name
        - local_area_name

        """
        area_name = kwargs.get("area_name")
        local_area_name = kwargs.get("local_area_name")
        floor_name = kwargs.get("floor_name")
        pointX = kwargs.get("x")
        pointY = kwargs.get("y")

        if area_name is None and local_area_name is None and \
                (pointX is None or pointY is None or floor_name is None):
            return None

        if area_name is not None:
            return self._get_wlan_point_from_area(area_name)
        elif local_area_name is not None:
            return self._get_wlan_point_from_local_area(local_area_name)
        else:
            return self._get_wlan_point_from_pose(pointX, pointY, floor_name)

    def _get_wlan_point_from_pose(self, x, y, floor_name):
        """Get the nearest wlan point from point(x, y)

        :x: float
        :y: float
        :floor_name: string or int
        :returns: Point

        """
        floor_object = self.osm_bridge.get_floor(floor_name)
        wlan_points = floor_object.wlans
        nearest_wlan_point = None
        least_distance = 10**10 # just a random big number
        for point in wlan_points:
            distance = self._calculate_cartesian_distance(point.x, point.y, x, y)
            if distance < least_distance:
                least_distance = distance
                nearest_wlan_point = point
        return nearest_wlan_point

    def _get_wlan_point_from_area(self, area_name):
        """Get topology node of area and get nearest wlan point from that node

        :area_name: string or int
        :returns: Point

        """
        area_obj = self.osm_bridge.get_area(area_name)
        __, __, relations = area_obj.osm_adapter.get_parent(
            id=area_obj.id,
            data_type='relation',
            parent_child_role=area_obj.type)
        floor_id = relations[0].id
        topology = area_obj.topology
        return self._get_wlan_point_from_pose(topology.x, topology.y, floor_id)

    def _get_wlan_point_from_local_area(self, local_area_name):
        """Get topology node of area containing given local_area and get nearest
        wlan point from that.

        :local_area_name: string or int
        :returns: Point

        """
        local_area_obj = self.osm_bridge.get_local_area(local_area_name)
        __, __, relations = local_area_obj.osm_adapter.get_parent(
            id=local_area_obj.id,
            data_type='relation',
            parent_child_role=local_area_obj.type)
        area_id = relations[0].id
        return self._get_wlan_point_from_area(area_id)

    def _calculate_cartesian_distance(self, x1, y1, x2, y2):
        """returns the cartesian distance between 2 points

        :x1: int/float
        :y1: int/float
        :x2: int/float
        :y2: int/float
        :returns: float

        """
        return ((x2 - x1)**2 + (y2 - y1)**2)**0.5
