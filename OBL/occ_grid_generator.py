import logging
import sys
import os
import utm
import yaml
from PIL import Image, ImageDraw, ImageFilter

from OBL.osm_bridge import OSMBridge
from OBL.osm_adapter import OSMAdapter

class OccGridGenerator(object):

    """Generates occupancy grids for a map based on the OSM map
    """

    _debug = False
    _dirname = "../maps"
    _file_name = "map"
    _server_ip = "127.0.0.1"
    _osm_bridge = None
    _server_port = 8000
    _dimension = 10000 #10000
    _resolution = 0.02
    _global_origin = [50.1363485, 8.6474024]
    _local_offset = [0, 0]
    _scale = 1

    def __init__(self, *args, **kwargs):
        """ 
        kwargs
        :osm_bridge: OSMBridge object
        :server_ip(str, optional): ip address of overpass server
        :server_port(int, optional): overpass server port
        :dirname: String
        :filename: String
        :local_offset: [float, float]
        :scale: float
        :dimension: int
        :resolution: float
        :debug: boolean
        """
        self._server_ip = kwargs.get("server_ip", self._server_ip)
        self._server_port = kwargs.get("server_port", self._server_port)
        self._osm_bridge = kwargs.get("osm_bridge", self._osm_bridge)
        self._global_origin = kwargs.get("global_origin", self._global_origin)
        
        if self._osm_bridge == None and (self._server_ip == None or self._server_port == None or self._global_origin == None) :
            raise Exception("Either OSMBridge object or (server_ip and server_port and global_origin) is required")

        if (not self._osm_bridge == None) and (not isinstance(self._osm_bridge, OSMBridge)):
            raise Exception("Object provided with keyword \"osm_bridge\" is not a OSMBridge object")

        if not self._osm_bridge == None :
            self._server_ip = self._osm_bridge._server_ip
            self._server_port = self._osm_bridge._server_port
            self._global_origin = self._osm_bridge.global_origin

        self.osm_adapter = OSMAdapter(server_ip=self._server_ip, server_port=self._server_port)

        self.logger = logging.getLogger("OccGridGenerator")
        if kwargs.get("debug", self._debug):            
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        self._local_offset = kwargs.get("local_offset", self._local_offset)
        self._resolution = kwargs.get("resolution", self._resolution)
        self._dirname = kwargs.get("dirname", self._dirname)
        self._file_name = kwargs.get("filename", self._file_name)
        self._dimension = kwargs.get("dimension", self._dimension)
        self._scale = kwargs.get("scale", self._scale)
        self._global_origin_cartesian = utm.from_latlon(self._global_origin[0], self._global_origin[1])

    @property
    def resolution(self):
        return self._resolution

    def generate_map(self, floor=None, **kwargs):
        """generates occupancy grid maps for a given floor

        :floor: int
        :returns: None

        """
        if floor == None :
            raise Exception("Floor number is required")

        """ create directory for maps """
        if not os.path.exists(self._dirname):
            self.logger.debug("maps folder not found")
            try:
                os.makedirs(self._dirname)
            except OSError as exc: # Guard against race condition
                print(str(exc))

        print("Trying to create map file...")
        grid_map = Image.new('L', (self._dimension*self._scale,self._dimension*self._scale),255) #128

        drawObject = ImageDraw.Draw(grid_map)
        ways = []
        ways.extend(self._get_walls(floor))
        ways.extend(self._get_elevator_walls())
        ways.extend(self._get_doors(floor))
        max_x , max_y = 0, 0
        for way in ways:
            way_cartesian= [self._convert_to_cartesian(n.lat, n.lon) for n in way]
            local_max_x = max(way_cartesian, key=lambda x: x[0])[0]
            local_max_y = max(way_cartesian, key=lambda y: y[1])[1]
            max_x = local_max_x if local_max_x > max_x else max_x
            max_y = local_max_y if local_max_y > max_y else max_y
            drawObject.polygon(way_cartesian,0,0)
        self.logger.debug("size x " + str(max_x))
        self.logger.debug("size y " + str(max_y))
        max_x += 100
        max_y += 100
        cropped_image = grid_map.crop((0,0, int(max_x), int(max_y)))
        cropped_image.save(self._dirname + "/" + self._file_name + "_floor_" + str(floor) + ".pgm")
        self._save_yaml_file(floor, max_x, max_y)
        print("Map files saved at " + os.path.abspath(self._dirname))

    def _get_walls(self, floor):
        """returns all the nodes for all ways with wall tag

        :floor: int
        :returns: ((n, n,..), (n, n, ..), ...) where n represents Node object

        """
        __,ways,__ = self.osm_adapter.search_by_tag(data_type='way', key_val_dict={'level':floor,'indoor':'wall'})
        walls = []
        for way in ways :
            nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=way.nodes,data_type='node')
            walls.append(tuple(nodes))
        self.logger.debug(str(len(walls)) + " walls found")
        return tuple(walls)

    def _get_elevator_walls(self):
        """returns all the nodes for all ways with wall tag with no level tag (elevator walls)

        :returns: ((n, n,..), (n, n, ..), ...) where n represents Node object

        """
        __,ways,__ = self.osm_adapter.get('way[!"level"][indoor=wall];')
        walls = []
        for way in ways :
            nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=way.nodes,data_type='node')
            walls.append(tuple(nodes))
        self.logger.debug(str(len(walls)) + " elevator walls found")
        return tuple(walls)

    def _get_doors(self, floor):
        """returns all the nodes for all ways with door tag and always_closed tag

        :floor: int
        :returns: ((n, n,..), (n, n, ..), ...) where n represents Node object

        """
        __,ways,__ = self.osm_adapter.search_by_tag(data_type='way', \
                key_val_dict={'level':floor,'indoor':'door', 'always_closed':'yes'})
        walls = []
        for way in ways :
            nodes,__,__ = self.osm_adapter.get_osm_element_by_id(ids=way.nodes,data_type='node')
            walls.append(tuple(nodes))
        self.logger.debug(str(len(walls)) + " doors found")
        return tuple(walls)

    def _save_yaml_file(self, floor, max_x, max_y):
        """save yaml file with map specifications

        :floor: int
        :max_x: int
        :max_y: int
        :returns: None

        """
        map_origin_y = - (max_y * self._resolution - ( - self._local_offset[1]))

        data = dict(
            image = self._file_name + '_floor_' + str(floor) + '.pgm',
            resolution = self._resolution*self._scale,
            origin = [self._local_offset[0]*self._scale, map_origin_y*self._scale, 0.0],
            negate = 0,
            latitude = self._global_origin[0],
            longitude = self._global_origin[1],
            occupied_thresh = 0.9,
            free_thresh =  0.1
        )

        with open(self._dirname + "/" + self._file_name + '_floor_' + str(floor) + '.yaml', 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=True)


    def _convert_to_cartesian(self, lat, lon):
        """convert a point (x, y) from spherical coordinates to cartesian coordinates (in meters)
            based on the global_origin and the local_offset provided to OccGridGenerator

        :lat: int/float
        :lon: int/float
        :returns: tuple (float, float)

        """
        temp = utm.from_latlon(lat, lon)
        x = temp[0] - self._global_origin_cartesian[0] + self._local_offset[0]
        y = -(temp[1] - self._global_origin_cartesian[1]) + self._local_offset[1]
        return (x / self._resolution, y / self._resolution)

#     commented because current map does not have all the details
#     def generate_map_all_floor(self, building=None):
#         """generate map of all the floor in the given building
# 
#         :building: String
#         :returns: None
# 
#         """
#         if building == None :
#             raise Exception("Building ref is required")
#         building_object = self.osm_bridge.get_building(building)
#         floors = building_object.floors
#         for floor in floors :
#             self.logger.debug(floor.ref)
#             floor_number = int(floor.ref.split("_")[1][1:])
#             self.generate_map(floor=floor_number)

