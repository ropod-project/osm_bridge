# OBL (OSM Bridge Library)

## Architecture

![architecture](docs/architecture.png)


## Installation

To install OBL clone & run the following command:
```
sudo pip3 install -e .
```

## Tests
To run all the tests:
```
python3 -m unittest discover -s 'tests' -p '*_test.py'
```

## Usage

### OSM Adapter

Methods
```
- OSMAdapter(server_ip=, server_port=): constructor
  - server_ip : overpass server ip
  - server_port : overpass server port

- test_overpass_connection() - to check if overpass connection was successful

- get_osm_element_by_id(ids, data_type, role, role_type) : to find OSM element by id/s
  - ids : array containing OSM ids
  - data_type : node/way/relation
  - role : to query specific member of relation (optional)
  - role_type : data type of relation member with specified role (optional)

- search_by_tag(data_type, key, value, scope_id=, scope_role=, scope_role_type=): search OSM element by tag 
  - data_type : node/way/relation
  - key : key to identify tag
  - value : value of tag
  - scope_id : reduces the search scope to specified relation members (optional)
  - scope_role : relation member role where search should be performed (optional)
  - scope_role_type : data type of relation member with specified role (optional)

- get(raw_overpass_query) : can be used to make raw overpass queries
```

### OSM bridge
* Provides abstraction to world model (https://git.ropod.org/ropod/wm/openstreetmap-indoor-modelling) using OSM adapter

Methods
```
- OSMBridge(server_ip=, server_port=, global_origin=, local_origin=, cooridnate_system=): constructor
  - server_ip : overpass server ip
  - server_port : overpass server port
  - global_origin : global origin in lat,lng ([lat,lng])
  - local_origin : local origin in x,y ([x,y])
  - coordinate_system : spherical / cartesian

- set_cooridnate_system(name, global_origin=, local_origin=) : setter for coordinate system related settings

- get_feature(ref) : returns Feature given semantic ref or OSM uuid

- get_side(ref) : returns Side given semantic ref or OSM uuid

- get_door(ref) : returns Door given semantic ref or OSM uuid

- get_wall(ref) : returns Wall given semantic ref or OSM uuid

- get_local_area(ref) : returns LocalArea given semantic ref or OSM uuid

- get_connection(ref) : returns Connection given semantic ref or OSM uuid

- get_room(ref) : returns Room given semantic ref or OSM uuid

- get_corridor(ref) : returns Corridor given semantic ref or OSM uuid

- get_elevator(ref) : returns Elevator given semantic ref or OSM uuid

- get_stairs(ref) : returns Stairs given semantic ref or OSM uuid

- get_floor(ref) : returns Floor given semantic ref or OSM uuid

- get_building(ref) : returns Building given semantic ref or OSM uuid
```


### Path planner
Methods
```
- set_building(building ref) - to set building 
- set_cooridnate_system('spherical'/'cartesian') - to set cooridnate system
- get_path_plan(start floor ref,destination floor ref, start area ref, destination area ref)
  Available keyword arguments:
    - start_local_area: start local area ref
    - destination_local_area: destination local area ref
    - destination_task: task to be performed at destination
    - robot_position: robot starting position
    (2 of these 4 keyword arguments are required - 1 each for start and destination)
- get_estimated_path_distance(start floor ref, destination floor ref, start area ref, destination area ref) - returns estimated path distance in m
```

### OccGridGenerator
Methods
```
- generate_map(floor ref, building ref) - generates occupancy grid map
```

## World model structs
[wm](OBL/structs/wm/README.md)


