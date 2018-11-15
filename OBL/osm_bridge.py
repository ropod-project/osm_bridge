import overpass
import logging
import sys
import utm
from OBL.structs.osm.node import Node
from OBL.structs.osm.way import Way
from OBL.structs.osm.relation import Relation
from OBL.osm_adapter import OSMAdapter
from OBL.structs.wm.wm_entity import WMEntity
from OBL.structs.wm.feature import Feature
from OBL.structs.wm.door import Door
from OBL.structs.wm.wall import Wall
from OBL.structs.wm.side import Side
from OBL.structs.wm.local_area import LocalArea
from OBL.structs.wm.connection import Connection
from OBL.structs.wm.room import Room
from OBL.structs.wm.corridor import Corridor
from OBL.structs.wm.elevator import Elevator
from OBL.structs.wm.stairs import Stairs
from OBL.structs.wm.floor import Floor
from OBL.structs.wm.building import Building
from OBL.structs.wm.point import Point
from OBL.structs.wm.area import Area


class OSMBridge(object):

    """Summary
    Provides abstraction to world model (https://git.ropod.org/ropod/wm/openstreetmap-indoor-modelling) using OSM adapter
    
    Attributes:
        logger (logging): logger
    """
    
    # default values
    _server_ip = "127.0.0.1"
    _server_port = 8000
    _global_origin = [50.1363485, 8.6474024]
    _coordinate_system = "spherical"
    _debug = False

    def __init__(self, *args, **kwargs):
        """Summary
        
        Args:
            server_ip(str, optional): ip address of overpass server
            server_port(int, optional): overpass server port
        """
        self._server_ip = kwargs.get("server_ip", self._server_ip)
        self._server_port = kwargs.get("server_port", self._server_port)

        WMEntity.osm_adapter = OSMAdapter(server_ip=self._server_ip, server_port=self._server_port)
        
        self._global_origin = kwargs.get("global_origin", self._global_origin)
        self._coordinate_system = kwargs.get("coordinate_system", self._coordinate_system)
        Point.coordinate_system = self._coordinate_system
        self._global_origin_cartesian = utm.from_latlon(self._global_origin[0], self._global_origin[1])

        self.logger = logging.getLogger("OSMBridge")
        if kwargs.get("debug", self._debug):            
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        Point._convert_to_cartesian = self.convert_to_cartesian

    def convert_to_cartesian(self, lat, lon):
        """convert a point (x, y) from spherical coordinates to cartesian coordinates (in meters)
            based on the global_origin provided to OSMBridge

        :lat: int/float
        :lon: int/float
        :returns: tuple (float, float)

        """
        temp = utm.from_latlon(lat, lon)
        x = temp[0] - self._global_origin_cartesian[0]
        y = temp[1] - self._global_origin_cartesian[1]
        return (x, y)

    def set_coordinate_system(self, name, *args, **kwargs):
        """Set the global or local origin for the OSMBridge
        
        Args:
            name (str): spherical/cartesian
        """
        Point.coordinate_system = name
        self._coordinate_system = name
        self._global_origin = kwargs.get("global_origin", self._global_origin)
        self._local_origin = kwargs.get("local_origin", self._local_origin)

    @property
    def global_origin(self) :
        return self._global_origin

    def get_feature(self, ref):
        """Summary
        
        Args:
            ref (str, int): feature ref
        
        Returns:
            Feature: feature wm entity
        """
        return  Feature(ref)

    def get_side(self, ref):
        """Summary
        
        Args:
            ref (str, int): side ref
        
        Returns:
            Side: side wm entity
        """
        return  Side(ref)

    def get_door(self, ref):
        """Summary
        
        Args:
            ref (str, int): door ref
        
        Returns:
            Door: door wm entity
        """
        return  Door(ref)

    def get_wall(self, ref):
        """Summary
        
        Args:
            ref (str, int): wall ref
        
        Returns:
            Wall: wall wm entity
        """
        return  Wall(ref)

    def get_local_area(self, ref):
        """Summary
        
        Args:
            ref (str, int): local area ref
        
        Returns:
            LocalArea: local area wm entity
        """
        return  LocalArea(ref)

    def get_connection(self, ref):
        """Summary
        
        Args:
            ref (str, int): connection ref
        
        Returns:
            Connection: connection wm entity
        """
        return  Connection(ref)

    def get_room(self, ref):
        """Summary
        
        Args:
            ref (str, int): room ref
        
        Returns:
            Room: room wm entity
        """
        return  Room(ref)

    def get_corridor(self, ref):
        """Summary
        
        Args:
            ref (str, int): corridor ref
        
        Returns:
            Corridor: corridor wm entity
        """
        return  Corridor(ref)

    def get_area(self, ref):
        """Summary
        
        Args:
            ref (str, int): area ref
        
        Returns:
            Area: area wm entity
        """
        return  Area(ref)

    def get_elevator(self, ref):
        """Summary
        
        Args:
            ref (str, int): elevator ref
        
        Returns:
            Elevator: elevator wm entity
        """
        return  Elevator(ref)

    def get_stairs(self, ref):
        """Summary
        
        Args:
            ref (str, int): stairs ref
        
        Returns:
            Stairs: stair wm entity
        """
        return  Stair(ref)

    def get_floor(self, ref):
        """Summary
        
        Args:
            ref (str, int): floor ref
        
        Returns:
            Floor: floor wm entity
        """
        return  Floor(ref)

    def get_building(self, ref):
        """Summary
        
        Args:
            ref (str, int): building ref
        
        Returns:
            Building: building wm entity
        """
        return  Building(ref)
    
