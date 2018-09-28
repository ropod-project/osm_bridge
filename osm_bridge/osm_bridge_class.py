import overpass

class OSMBridge(object):

    def __init__(self, config_params):
        self.api_url = "http://" + config_params.overpass_server_ip + ":" + str(config_params.overpass_server_port) + "/api/interpreter"
        self.api = overpass.API(endpoint=self.api_url)
        self.global_origin = [config_params.global_origin_lat, config_params.global_origin_lon]
        self.local_origin = [config_params.local_origin_x, config_params.local_origin_y]
        self.map_location = config_params.map_location
        print("Connecting to overpass server at {}:{}....".format(config_params.overpass_server_ip, config_params.overpass_server_port))

        if self.test_overpass_connection():
            print("Successfully connected to Overpass server")
        else:
            print("Couldn't connect to Overpass server")


    def test_overpass_connection(self):
        try:
            data = self.api.get('node(1234);')
        except:
            return False
        return True