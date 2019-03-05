import overpass
import logging
import sys
from OBL.structs.osm.node import Node
from OBL.structs.osm.way import Way
from OBL.structs.osm.relation import Relation


class OSMAdapter(object):

    # default values
    _server_ip = "127.0.0.1"
    _server_port = 8000
    _debug = False

    def __init__(self, *args, **kwargs):
        server_ip = kwargs.get("server_ip", self._server_ip)
        server_port = kwargs.get("server_port", self._server_port)

        endpoint = "http://" + server_ip + ":" + \
            str(server_port) + "/api/interpreter"
        self.api = overpass.API(endpoint=endpoint,)

        self.logger = logging.getLogger("OSMAdapter")
        if kwargs.get("debug", self._debug):
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        self.logger.info("Connecting to overpass server at {}:{}....".format(
            server_ip, server_port))

        if not self.check_connection_status():
            raise Exception("Unable to connect to Overpass server")

    def check_connection_status(self):
        self.connection_status = self.test_overpass_connection()
        if self.connection_status:
            self.logger.info("Successfully connected to Overpass server")
        else:
            self.logger.info("Couldn't connect to Overpass server")
        return self.connection_status

    def test_overpass_connection(self):
        '''
        Tests if connection to overpass server was successfully established
        '''
        try:
            # just test query for testing overpass connection
            self.api.get('node(1234);', responseformat="json")
        except:
            return False
        return True

    def _construct_output_response(self, data):
        '''
        Constructs output response based on data retrieved from overpass
        '''
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
        return node_list, way_list, relation_list

    def get(self, query_string):
        '''
        Makes request to overpass server and returns response as python data structures
        '''
        if len(query_string) > 0:
            data = self.api.get(query_string, responseformat="json")
        else:
            data = self.api.get('out;', responseformat="json")
        return self._construct_output_response(data)

    def get_osm_element_by_id(self, ids=[], data_type='', role='', role_type=''):
        '''
        Queries OSM data elements - node, way and relation based on their id
        For OSM relations, its members can be directly retrieved by passing its role and type
        '''
        self.logger.debug(
            'Received new query request - ids:{},data_type:{},role:{},role_type:{}'.format(ids, data_type, role, role_type))
        if len(ids) == 0:
            raise Exception("Empty list of Ids passed.")
        if data_type == 'relation' and role and role_type:
            if len(ids) > 1:
                return self._get_ordered_osm_element_by_id(ids, data_type, role, role_type)
            else:
                query_string = data_type + \
                    "(id:" + ','.join([str(id) for id in ids]) + \
                    ");" + role_type + "(r._:'" + role + "');"
        else:
            query_string = data_type + \
                "(id:" + ','.join([str(id) for id in ids]) + ");"
#        print(query_string)
        data = self.get(query_string)
        if len(ids) > 1:
            return self._reorder_elements(ids, data)
        else:
            return data

    def search_by_tag(self, data_type='', *args, **kwargs):
        '''
        Searches OSM elements based on tag within a scope (if provided)
        '''
        scope_id = kwargs.get("scope_id", '')        # id of scope relation
        scope_role = kwargs.get("scope_role", '')    # role of scope relation
        scope_role_type = kwargs.get(
            "scope_role_type", '')    # role of scope relation
        # dictionary object with multiple keys value tag search
        key_val_dict = kwargs.get("key_val_dict")
        key = kwargs.get("key")  # key for a single tag search
        value = kwargs.get("value")  # value for a single tag search

        if key_val_dict is None and (key is None and value is None):
            raise Exception("Either key and value or key_val_dict is required")

        # this restricts search scope to this relation
        if scope_id and scope_role and scope_role_type:
            scope_string = 'relation(' + str(scope_id) + ');' + \
                scope_role_type + "(r._:'" + scope_role + "');"
        else:
            scope_string = ''

        if key_val_dict is None:
            self.logger.debug(
                'Received new search by tag request - data_type:{},key:{},value:{}'.format(data_type, key, value))
            query_string = scope_string + data_type + \
                "[" + key + "='" + str(value) + "'];"
        else:
            self.logger.debug(
                'Received new search by tag request - data_type:{},key_val_dict:{}'.format(data_type, key_val_dict))
            query_string = scope_string + data_type
            for key in key_val_dict.keys():
                query_string += "[" + key + "='" + \
                    str(key_val_dict[key]) + "']"
            query_string += ";"
        return self.get(query_string)

    # 'node('+str(node.id)+');rel(bn:"topology");way(r._:"geometry");'
    def get_parent(self, id, data_type, parent_child_role, role_type='', role=''):
        '''
        Get parent relation of OSM element
        Members can be directly retrieved by passing its role and type
        '''
        if data_type == 'node':
            role_code = 'bn'
        elif data_type == 'way':
            role_code = 'bw'
        elif data_type == 'relation':
            role_code == 'br'

        query_string = data_type + \
            '(' + str(id) + ');rel(' + role_code + ':"' + parent_child_role + '");'

        if role and role_type:
            query_string = query_string + role_type + "(r._:'" + role + "');"
        return self.get(query_string)

    def _reorder_elements(self, ids, data):
        """Reorders elements in data according to the ids list

        :ids: list of int
        :data: tuple of size 3, each element is a list of objects
        :returns: tuple of size 3, each element is a list of objects

        """
        reordered_data = [[], [], []]
        for i in range(3):
            if len(data[i]) != 0:
                for element_id in ids:
                    for element in data[i]:
                        if element.id == element_id:
                            reordered_data[i].append(element)
                            break
        return tuple(reordered_data)

    def _get_ordered_osm_element_by_id(self, ids, data_type, role, role_type):
        """get the elements in order of their ids by making individual queries

        :data_type: string
        :ids: list of int
        :role: string
        :role_type: string
        :returns: tuple of 3 lists, each list can contain objects

        """
        data = [[], [], []]
        for id_number in ids:
            query_string = data_type + \
                "(id:" + str(id_number) + ");" + \
                role_type + "(r._:'" + role + "');"
            response = self.get(query_string)
            for i in range(3):
                data[i].extend(response[i])
        return tuple(data)
