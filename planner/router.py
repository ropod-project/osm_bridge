from planner.node import Node
from planner.visited_node import VisitedNode
from planner.connection import Connection
from heapq import heappop, heappush, heapify
from math import sin, radians, cos, atan2, sqrt


class Router(object):

    def __init__(self, from_, to, connections):
        self.from_ = VisitedNode(from_)
        self.to = to
        self.connections = connections
        self.path_distance = 0

    def route(self):
        self.from_.g = 0
        self.from_.h = self.path_estimate(self.from_.node, self.to)
        self.visited = []
        self.heap = [(self.from_.f, self.from_)]
        self.nodes = []

        while self.heap:
            selected = heappop(self.heap)[1]
            self.visited.append(selected)
            print("Exploring %(node_id)s (%(distance).03f m to go, %(visited)s nodes seen, %(roads)s roads left)" % {
                'node_id': repr(selected.node.id),
                'distance': selected.h,
                'roads': len(self.heap),
                'visited': len(self.visited),
            })
            self.explore(selected)
            if selected.node == self.to:
                print("Path successfully planned ", selected.g, " m")
                self.path_distance = selected.g
                break
        else:
            print("Couldn't plan the path")
            return False

        while selected:
            self.nodes.insert(0, selected)
            selected = selected.parent

        return True

    def get_connections(self, node):
        way_list = []
        for connection in self.connections:
            if node in connection.nodes:
                way_list.append(connection)
        return way_list

    def explore(self, selected):
        for way in self.get_connections(selected.node):
            self.walk(way, selected, True)
            self.walk(way, selected, False)

    def walk(self, way, from_, forward=True):
        nodes = way.nodes
        index = nodes.index(from_)

        if forward:
            # walk_nodes = way.nodes[index + 1:index + 100]
            walk_nodes = way.nodes[index+1:index+2]
        else:            
            if index == 0:
                # We're at the beginning of the path.
                return
            walk_nodes = way.nodes[index-1:index ]
        # print("Found %d steps on %d" % (len(walk_nodes), way.id))

        g = 0
        for idx, step in enumerate(walk_nodes):
            if not self.is_way_section_accessible(way, from_, step):
                # Remaining nodes are not accessible, so there's no point in
                # walking them. Also these nodes cannot be marked as visited,
                # as they might be accessible through a different path.
                break

            if step in self.visited:
                # We've already been here, and most likely also visited the
                # remainder of the street. So we can safely skip the
                # remainder of the way.
                break
            g = from_.g + self.path_cost(way, from_, step)
            for index, (_, other) in enumerate(self.heap):
                if step != other:
                    continue
                if other.g <= g:
                    # We've already found a shorter route to this node; the
                    # remainder of the way can be skipped as well.
                    return
                self.heap[index] = self.heap[-1]
                self.heap.pop()
                heapify(self.heap)
                break
            node = VisitedNode(step, parent=from_, g=g, h=self.path_estimate(step, self.to))
            heappush(self.heap, (node.f, node))
            # print("    √ %s" % node)
            from_ = node

    def is_way_section_accessible(self, way, from_, to):
        if way.oneway and way.nodes.index(from_) > way.nodes.index(to):
            # print("ｘ %(way)s is one-way" % {'way': way.id})
            return False
        return True

    def path_cost(self, way, from_, to):
        d = self.distance(from_, to)
        # s = way.maxspeed or self.maxspeeds[way.highway]
        return d

    def path_estimate(self, from_, to):
        return self.distance(from_, to)

    def cal_distance(self, p1, p2):
        R = 6371000  # radius of the earth
        dlat = radians(p2[0]) - radians(p1[0])
        dlon = radians(p2[1]) - radians(p1[1])
        a = (sin(dlat / 2)) ** 2 + cos(radians(p1[0])) * cos(radians(p2[0])) * (sin(dlon / 2)) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def distance(self, from_, to):
        return self.cal_distance((from_.lat, from_.lon), (to.lat, to.lon))
