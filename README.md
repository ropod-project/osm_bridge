# OSM bridge

## Installation

Get the requirements:
```
pip3 install -r requirements.txt
```

To add the osm_bridge to you `PYTHONPATH` simply run:
```
sudo pip3 install -e .
```

To run all unit tests:
```
python3 -m unittest discover -s 'tests' -p '*_test.py'
```