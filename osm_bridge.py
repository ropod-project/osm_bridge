import overpass
import logging
import sys
from structs.osm.node import Node
from structs.osm.way import Way
from structs.osm.relation import Relation
from osm_adapter import OSMAdapter
from structs.wm.feature import Feature
from structs.wm.wm_entity import WMEntity

class OSMBridge(object):

    # default values
    _server_ip = "127.0.0.1"
    _server_port = 8000
    _global_origin = [50.1363485, 8.6474024]
    _local_origin = [0,0]
    _map_location = "~"
    _debug = False

    def __init__(self, *args, **kwargs):
        server_ip = kwargs.get("server_ip", self._server_ip)
        server_port = kwargs.get("server_port", self._server_port)

        WMEntity.osm_adapter = OSMAdapter(server_ip=server_ip, server_port=server_port)
        
        self.global_origin = kwargs.get("global_origin", self._global_origin)
        self.local_origin = kwargs.get("local_origin", self._local_origin)
        self.map_location = kwargs.get("map_location", self._map_location)

        self.logger = logging.getLogger("OSMBridge")
        if kwargs.get("debug", self._debug):            
            self.logger.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def get_feature(self, id):
        return  Feature(id)
    