import overpass
import logging
import sys
from structs.osm.node import Node
from structs.osm.way import Way
from structs.osm.relation import Relation, Member

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

        endpoint = "http://" + server_ip + ":" + str(server_port) + "/api/interpreter"
        self.api = overpass.API(endpoint=endpoint)
        
        self.global_origin = kwargs.get("global_origin", self._global_origin)
        self.local_origin = kwargs.get("local_origin", self._local_origin)
        self.map_location = kwargs.get("map_location", self._map_location)

        if kwargs.get("debug", self._debug):
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        
        logging.info("Connecting to overpass server at {}:{}....".format(server_ip, server_port))

        if self.test_overpass_connection():
            logging.info("Successfully connected to Overpass server")
        else:
            logging.info("Couldn't connect to Overpass server")

    '''
    Tests if connection to overpass server was successfully established
    '''
    def test_overpass_connection(self):
        try:
            data = self.api.get('node(1234);')  # just test query for testing overpass connection
        except:
            return False
        return True

    '''
    Constructs output response based on data retrieved from overpass
    '''
    def _construct_output_response(self, data):
        node_list = []
        way_list = []
        relation_list = []
        for element in data.get('elements'):
            element_type = element.get('type')
            if element_type == 'node':
                node_list.append(Node(element))
            elif element_type == 'way':
                way_list.append(Way(element))
            elif element_type == 'relation':
                relation_list.append(Relation(element))
        return node_list,way_list,relation_list


    '''
    Makes request to overpass server and returns response as python data structures
    '''
    def get(self, query_string):
        if len(query_string) > 0:
            data = self.api.get(query_string) 
        else:
            data = self.api.get('out;')
        return self._construct_output_response(data)


    '''
    Queries OSM data elements - node, way and relation based on their id
    For OSM relations, its members can be directly retrieved by passing its role and type
    '''
    def get_osm_element_by_id(self, ids=[], data_type='', role='', role_type=''):
        logging.debug('Received new query request - ids:{},data_type:{}role:{},role_type:{}'.format(ids,data_type,role,role_type))
        if data_type == 'relation' and role and role_type:
            query_string = data_type + "(id:" + ','.join([str(id) for id in ids]) +  ");" + role_type + "(r._:'" + role + "');"
        else:
            query_string = data_type + "(id:" + ','.join([str(id) for id in ids]) +  ");"
        return  self.get(query_string)

    