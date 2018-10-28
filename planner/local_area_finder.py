from osm_bridge import OSMBridge
import logging
import sys
import utm
from structs.wm.point import Point
from structs.wm.room import Room
from structs.wm.corridor import Corridor
from structs.wm.area import Area
from structs.wm.floor import Floor

class LocalAreaFinder(object):

    """Finds the nearest local area to a give position (x, y) of robot"""

    # default values
    _debug = False
    resolution = 0.02
    local_origin = [-25, -25]
    _isLatlong = False

    def __init__(self, osm_bridge, *args, **kwargs):
        self.osm_bridge = osm_bridge

        self.logger = logging.getLogger("LocalAreaFinder")
        if kwargs.get("debug", self._debug):            
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        self.logger.debug("inside init of LocalAreaFinder")
    
        self.global_origin = self.osm_bridge.get_global_origin()
        self.global_origin_cartesian = utm.from_latlon(self.global_origin[0], self.global_origin[1])

    def get_local_area(self, pointX, pointY, *args, **kwargs):
        """gets the LocalArea of the point corresponding to x and y

        :x: int/float
        :y: int/float
        :area_name: string
        :floor_name: string
        :isLatlong: boolean (default False)
        :returns: TODO

        Either area_name or floor_name is required to get non None return

        """
        self.logger.debug(kwargs.get("area_name"))
        if kwargs.get("floor_name") == None and kwargs.get("area_name") == None :
#            raise Exception ("Either area_name or floor_name is required")
            return None

        area_name = kwargs.get("area_name")
        floor_name = kwargs.get("floor_name")

        if kwargs.get("isLatlong", self._isLatlong):            
            x, y = self.convert_to_cartesian(pointX, pointY)
            self.logger.debug(x)
            self.logger.debug(y)
        else :
            x, y = pointX, pointY

        if area_name == None :
            area_object = self._get_area_object(x, y, floor_name)
        else :
            area_object = self.osm_bridge.get_area(area_name)

        self.logger.debug("Area ID: "+str(area_object.id))
        local_areas = area_object.local_areas
        for local_area in local_areas :
            self.logger.debug(local_area.ref)
            geometry = local_area.geometry
            self.logger.debug(geometry)
            self.logger.debug(geometry.points)
            if self._is_inside_polygon(x, y, geometry.points) :
                return local_area.ref
        return self._get_nearest_local_area(x, y, local_areas)

    def _get_nearest_local_area(self, x, y, local_areas):
        """returns the local area that is nearest to the point (x, y)

        :x: int/float
        :y: int/float
        :local_areas: list of LocalArea objects
        :returns: TODO

        """
        min_dist = 0
        min_dist_local_area = None
        for local_area in local_areas :
            topology = local_area.topology
            if topology.coordinate_system == "spherical" :
                cart_x, cart_y = self.convert_to_cartesian(topology.lat, topology.lon)
            else :
                cart_x, cart_y = topology.x, topology.y
            dist = self._calculate_cartesian_distance(x, y, cart_x, cart_y)
            if min_dist_local_area == None or dist < min_dist :
                min_dist = dist
                min_dist_local_area = local_area
        return min_dist_local_area.ref

    def _is_inside_polygon(self, x, y, points):
        """checks if point (x,y) is inside the polygon created by points

        :x: int/float
        :y: int/float
        :points: list of Point objects
        :returns: bool

        """
        xPoints = []
        yPoints = []

        for point in points[:-1] :      # first and last point in points is same
            if point.coordinate_system == "spherical" :
                cart_x, cart_y = self.convert_to_cartesian(point.lat, point.lon)
            else :
                cart_x, cart_y = point.x, point.y
            xPoints.append(cart_x)
            yPoints.append(cart_y)
        return self._ray_tracing_algorithm(xPoints, yPoints, x, y)

    def _ray_tracing_algorithm(self, vertx, verty, testx, testy) :
        """Checks if the point (textx, testy) is inside polygon defined by list vertx and verty
        Taken from : https://stackoverflow.com/a/2922778/10460994
        Implements ray tracing algorithm.

        :vertx: list of floats
        :verty: list of floats
        :testx: float
        :testy: float
        :returns: bool

        """
        j = -1
        counter = 0
        for i in range(len(vertx)) :
            numerator = testy - verty[i]
            denominator = (verty[j] - verty[i])
            temp = (vertx[j] - vertx[i]) * (numerator / denominator) + vertx[i]
            if (verty[i] > testy) != (verty[j] > testy) and (testx < temp) :
                counter += 1
            j = i
        return (counter % 2 == 1)

    def convert_to_cartesian(self, lat, lon):
        """convert a point (x, y) from spherical coordinates to cartesian coordinates

        :lat: int/float
        :lon: int/float
        :returns: tuple (float, float)

        """
        temp = utm.from_latlon(lat, lon)
        x = temp[0] - self.global_origin_cartesian[0] - self.local_origin[0]
        y = -(temp[1] - self.global_origin_cartesian[1]) - self.local_origin[1]
        return (x/self.resolution, y/self.resolution)

    def _calculate_cartesian_distance(self, x1, y1, x2, y2):
        """returns the cartesian distance between 2 points

        :x1: int/float
        :y1: int/float
        :x2: int/float
        :y2: int/float
        :returns: float

        """
        return ((x2-x1)**2 + (y2-y1)**2)**0.5

    def _get_area_object(self, x, y, floor_name):
        """get the Area object in which the point (x, y) is located

        :x: int/float
        :y: int/float
        :floor_name: String
        :returns: Area object

        """
        self.logger.debug(floor_name)
        floor_object = self.osm_bridge.get_floor(floor_name)
        self.logger.debug("Floor ID: "+str(floor_object.id))
        areas = floor_object.corridors
        areas.extend(floor_object.rooms)
        distances = []
        for area in areas :
            self.logger.debug(area.ref)
            topology = area.topology
            if topology.coordinate_system == "spherical" :
                cart_x, cart_y = self.convert_to_cartesian(topology.lat, topology.lon)
            else :
                cart_x, cart_y = topology.x, topology.y
            dist = self._calculate_cartesian_distance(x, y, cart_x, cart_y)
            distances.append(dist)
        self.logger.debug(distances)
        for i in range(5) :
            ind = distances.index(min(distances))
            probable_area = areas.pop(ind)
            distances.pop(ind)
            self.logger.debug(probable_area.ref)
            geometry = probable_area.geometry
            self.logger.debug(geometry)
            self.logger.debug(geometry.points)
            if self._is_inside_polygon(x, y, geometry.points) :
                return probable_area
#        return self.osm_bridge.get_area("AMK_B_L-1_C29")
        return None
