import overpass
import logging
import sys
from osm_bridge.structs.osm_node import Node
from osm_bridge.structs.osm_way import Way
from osm_bridge.structs.osm_relation import Relation, Member

class OSMBridge(object):

    def __init__(self, config_params):
        # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        self.api_url = "http://" + config_params.overpass_server_ip + ":" + str(config_params.overpass_server_port) + "/api/interpreter"
        self.api = overpass.API(endpoint=self.api_url)
        self.global_origin = [config_params.global_origin_lat, config_params.global_origin_lon]
        self.local_origin = [config_params.local_origin_x, config_params.local_origin_y]
        self.map_location = config_params.map_location
        logging.info("Connecting to overpass server at {}:{}....".format(config_params.overpass_server_ip, config_params.overpass_server_port))

        if self.test_overpass_connection():
            logging.info("Successfully connected to Overpass server")
        else:
            logging.info("Couldn't connect to Overpass server")


    def test_overpass_connection(self):
        try:
            data = self.api.get('node(1234);')  # just test query for testing overpass connection
        except:
            return False
        return True

    def query(self, ids=[], query_type='', data_type='', role='', role_type=''):
        logging.debug('Received new query request - ids:{},query_type:{},data_type:{},role:{},role_type:{}'.format(ids,query_type,data_type,role,role_type))
        query_string = self.construct_overpass_query(query_type, data_type, ids, role, role_type)
        return  self.make_overpass_request(query_string)

    '''
    Constructs queries to send to overpass server

    Query types:
      - 'info' - returns geometry and semantic info of all element ids
      - 'geometry' - returns geometry corresponding to given topological node
      - 'topological_node' - returns geometry corresponding to given topological node
      - 'graph' - returns graphs containing given topological node
    '''
    def construct_overpass_query(self, query_type, data_type, ids, role, role_type):
        valid_query_type = {'info','geometry','graph','topological_node'}
        valid_data_type = {'node','way','relation'}

        if query_type not in valid_query_type or data_type not in valid_data_type or len(ids) == 0:
            logging.error("Invalid OSM request")
            return None

        query_string = ""

        if query_type == 'info':
            if data_type == 'relation' and role and role_type:
                query_string = data_type + "(id:" + ','.join([str(id) for id in ids]) +  ");" + role_type + "(r._:'" + role + "');"
            else:
                query_string = data_type + "(id:" + ','.join([str(id) for id in ids]) +  ");"
        elif query_type == 'geometry':
            if data_type == 'node':
                query_string = data_type + "(id:" + ','.join([str(id) for id in ids]) +  ");rel(bn:'topology');way(r._:'geometry');"
            else:
                logging.error("Invalid OSM request")
        elif query_type == 'topological_node':
            if data_type == 'way':
                query_string = data_type + "(id:" + ','.join([str(id) for id in ids]) +  ");rel(bw:'geometry');node(r._:'topology');"
            else:
                logging.error("Invalid OSM request")
        elif query_type == 'graph':
            if data_type == 'node':
                query_string = data_type + "(id:" + ','.join([str(id) for id in ids]) +  ");way(bn);"
            else:
                logging.error("Invalid OSM request")
      
        logging.debug("Constructed overpass query string:{}".format(query_string))
        return query_string

    '''
    Constructs output response based on data retrieved from overpass
    '''
    def construct_output_response(self, data):
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
    def make_overpass_request(self, query_string):
        if len(query_string) > 0:
            data = self.api.get(query_string) 
        else:
            data = self.api.get('out;')
        return self.construct_output_response(data)
