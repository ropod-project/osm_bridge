from osm_bridge.structs.osm_node import Node
from osm_bridge.structs.osm_way import Way
from osm_bridge.structs.osm_relation import Relation, Member
import unittest

class TestStructs(unittest.TestCase):

    def setUp(self):
        pass

    def test_node(self):
        data = {
            "type": "node",
            "id": 4865,
            "lat": 50.1362318,
            "lon": 8.6475163,
            "tags": 
              {
                  "highway": "elevator"
              }
        }
        n = Node(data)
        print(n)
        self.assertEqual(n.id, 4865)
        self.assertEqual(n.lat, 50.1362318)
        self.assertEqual(n.lon, 8.6475163)
        self.assertEqual(n.highway, "elevator")

    def test_way(self):
        data =  {
            "type": "way",
            "id": 499,
            "nodes": [
                2518,
                2519,
                2520,
                2521,
                2518
            ],
            "tags": 
              {
                "indoor": "wall",
                "level": "-1"
              }
        }
        w = Way(data)
        print(w)
        self.assertEqual(w.id, 499)
        self.assertEqual(w.indoor, "wall")
        self.assertEqual(w.highway, None)
        self.assertEqual(w.oneway, None)

    def test_relation(self):
        data = {
            "type": "relation",
            "id": 149,
            "members": [
                {
                    "type": "way",
                    "ref": 1352,
                    "role": "geometry"
                },
                {
                    "type": "relation",
                    "ref": 164,
                    "role": "level"
                },
                {
                    "type": "relation",
                    "ref": 148,
                    "role": "level"
                },
                {
                    "type": "relation",
                    "ref": 5,
                    "role": "elevator"
                }
            ],
            "tags": {
                "ref": "AMK",
                "type": "building"
            }
        }
        r = Relation(data)
        print(r)
        self.assertEqual(r.id, 149)
        self.assertEqual(len(r.members), 4)
        self.assertEqual(r.ref, "AMK")
        self.assertEqual(r.something, None)


if __name__ == '__main__':
    unittest.main()
