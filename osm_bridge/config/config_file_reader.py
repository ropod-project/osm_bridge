import yaml
from osm_bridge.config.params import ConfigParams
'''An interface for reading configuration files
'''

class ConfigFileReader(object):
    '''
    Keyword arguments:
    @param config_file absolute path of a config file

    '''
    @staticmethod
    def load(config_file):
        config_params = ConfigParams()
        config_data = ConfigFileReader.__read_yaml_file(config_file)

        if 'overpass_server_ip' in config_data.keys():
            config_params.overpass_server_ip = config_data['overpass_server_ip']
        else:
            print('Config error: "overpass server ip address" not specified')

        if 'overpass_server_port' in config_data.keys():
            config_params.overpass_server_port = config_data['overpass_server_port']
        else:
            print('Config error: "overpass server port" not specified')

        if 'global_origin_lat' in config_data.keys():
            config_params.global_origin_lat = config_data['global_origin_lat']
        else:
            print('Config error: "global origin lat" not specified')

        if 'global_origin_lon' in config_data.keys():
            config_params.global_origin_lon = config_data['global_origin_lon']
        else:
            print('Config error: "global origin lon" not specified')

        if 'local_origin_x' in config_data.keys():
            config_params.local_origin_x = config_data['local_origin_x']
        else:
            print('Config error: "local origin x" not specified')

        if 'local_origin_y' in config_data.keys():
            config_params.local_origin_y = config_data['local_origin_y']
        else:
            print('Config error: "local origin y" not specified')

        if 'map_location' in config_data.keys():
            config_params.map_location = config_data['map_location']
        else:
            print('Config error: "map location" not specified')

        return config_params

    @staticmethod
    def __read_yaml_file(config_file_name):
        file_handle = open(config_file_name, 'r')
        data = yaml.load(file_handle)
        file_handle.close()
        return data
