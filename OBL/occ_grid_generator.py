import logging
import sys
import os
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
    _dimension = 10000 #10000
    _scale = 1

    def __init__(self, osm_bridge, *args, **kwargs):
        """TODO: to be defined1. 
        
        args
        :osm_bridge: OSMBridge object
        :debug: boolean
        """
        
        if not isinstance(osm_bridge, OSMBridge):
            raise Exception("Please pass OSM bridge object")
        self.osm_bridge = osm_bridge

        self.osm_adapter = OSMAdapter(server_ip=self.osm_bridge._server_ip, server_port=self.osm_bridge._server_port)

        self._building = None
        self._elevators = None
        self._coordinate_system = 'cartesian'

        self.logger = logging.getLogger("OccGridGenerator")
        if kwargs.get("debug", self._debug):            
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        self.logger.debug("inside init of occ grid generator")
        self._dirname = kwargs.get("dirname", self._dirname)
        self._file_name = kwargs.get("filename", self._file_name)
        self._dimension = kwargs.get("dimension", self._dimension)
        self._scale = kwargs.get("scale", self._scale)

    def generate_map(self, floor=None):
        """generates occupancy grid maps for a given floor

        :floor: string
        :returns: None

        """
        if floor == None :
            raise "Floor name is required"

        """ create directory for maps """
        if not os.path.exists(self._dirname):
            self.logger.debug("maps folder not found")
            try:
                os.makedirs(self._dirname)
            except OSError as exc: # Guard against race condition
                print(str(exc))


        grid_map = Image.new('L', (self._dimension*self._scale,self._dimension*self._scale),255) #128

        drawObject = ImageDraw.Draw(grid_map)
        ways = list(self._get_walls(floor))
#        ways = []
        ways.extend(self._get_elevator_walls())
        ways.extend(self._get_doors(floor))
        for way in ways:
            way_cartesian = [self.osm_bridge.convert_to_cartesian(n.lat, n.lon) for n in way]
            drawObject.polygon(way_cartesian,0,0)
        grid_map.save(self._dirname + "/" + self._file_name + "_floor_" + str(floor) + ".pgm")
        self._save_yaml_file(floor)

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

    def _save_yaml_file(self, floor):
        """save yaml file with map specifications

        :floor: int
        :returns: None

        """
        grid_map_origin = [0,0]
        grid_map_origin[1] = ((self._dimension*self.osm_bridge.resolution*self._scale) - self.osm_bridge.local_origin[0]) - (- self.osm_bridge.local_origin[1])
        grid_map_origin[0] = self.osm_bridge.local_origin[1] - self.osm_bridge.local_origin[0]
        data = dict(
            image = self._file_name + '_floor_' + str(floor) + '.pgm',
            resolution = self.osm_bridge.resolution*self._scale,
            origin = [grid_map_origin[0], grid_map_origin[1], 0.0],
            negate = 0,
            latitude = self.osm_bridge.global_origin[0],
            longitude = self.osm_bridge.global_origin[1],
            occupied_thresh = 0.99,
            free_thresh =  0.01
        )

        with open(self._dirname + "/" + self._file_name + '_floor_' + str(floor) + '.yaml', 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=True)
"""


"""
