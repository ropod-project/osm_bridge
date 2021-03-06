import logging
import sys
from OBL.osm_bridge import OSMBridge
from OBL.local_area_finder import LocalAreaFinder
from math import sqrt


class SemanticFeatures(object):

    def __init__(self):
        self.wall_sides = []
        self.door_sides = []
        self.corners = []
        self.features = []
        self.pillars = []


class SemanticFeaturesFinder(object):

    """Summary
    Provides method to find semantic features visible from any given top level area

    Attributes:
    """

    # default values
    _debug = False

    def __init__(self, osm_bridge, *args, **kwargs):
        """
        Args:
            osm_bridge (OSMBridge): bridge between world model and OSM
        """
        if not isinstance(osm_bridge, OSMBridge):
            raise Exception("Please pass OSM bridge instance")
        self.osm_bridge = osm_bridge
        self.local_area_finder = LocalAreaFinder(self.osm_bridge, debug=False)

        self.logger = logging.getLogger("SemanticFeaturesFinder")
        if kwargs.get("debug", self._debug):
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def get_features(self, area_ref):
        """Summary
        Args:
            area_ref (int/string): uuid or semantic name of the building
        """
        semantic_features = SemanticFeatures()
        area = self.osm_bridge.get_area(area_ref)
        area_geometry = area.geometry

        walls = area.walls
        doors = area.doors

        semantic_features.wall_sides = self._get_sides(walls, area_geometry)
        semantic_features.door_sides = self._get_sides(doors, area_geometry)
        semantic_features.features = area.features
        semantic_features.pillars = area.pillars
        return semantic_features

    def _get_sides(self, parents, area_geometry):
        sides = []
        for parent in parents:
            parent_sides = parent.sides
            if len(parent_sides) == 1:
                sides.append([parent_sides[0]])
            else:
                sides.append(self._get_visible_sides(
                    parent_sides, area_geometry))
        return [item for sublist in sides for item in sublist]

    def _get_visible_sides(self, parent_sides, area_geometry):
        sides = []
        for parent_side in parent_sides:
            if self._check_if_side_is_visible(parent_side, area_geometry):
                sides.append(parent_side)
        return sides

    def _check_if_side_is_visible(self, side, area_geometry):
        corners = side.corners
        is_corner1_inside = self.local_area_finder.is_inside_polygon(
            corners[0].x, corners[0].y, area_geometry.points)
        is_corner2_inside = self.local_area_finder.is_inside_polygon(
            corners[1].x, corners[1].y, area_geometry.points)

        if is_corner1_inside and is_corner2_inside:
            # if both corners are inside the area then side is definitely
            # visible from given area from some angle
            return True
        elif (is_corner1_inside and ~is_corner2_inside) or (~is_corner1_inside and is_corner2_inside):
            # if 1 side corner is inside the geometry
            side_line = self._line(corners[0], corners[1])
            area_lines = self._get_area_lines(area_geometry)
            # check if side intersects with area geometry
            for area_line in area_lines:
                res = self._check_intersection(side_line, area_line)
                # if yes decide based on how much of side length lies inside
                # the area geometry
                if res:
                    dist1 = sqrt((corners[0].x - res[0])
                                 ** 2 + (corners[0].y - res[1])**2)
                    dist2 = sqrt((res[0] - corners[1].x) **
                                 2 + (res[1] - corners[1].y)**2)
                    if (is_corner1_inside and dist1 > dist2) or (is_corner2_inside and dist2 > dist1):
                        return True
            return False
        elif (~is_corner1_inside and ~is_corner2_inside):
            # if both side corners are outside the area geometry then it should
            # intersect 2 area geometry lines to reach the
            side_line = self._line(corners[0], corners[1])
            area_lines = self._get_area_lines(area_geometry)
            intersection_count = 0
            for area_line in area_lines:
                res = self._check_intersection(side_line, area_line)
                intersection_count = intersection_count + 1 if res else intersection_count
            if intersection_count >= 2:
                return True
        return False

    # Source: https://stackoverflow.com/questions/20677795/
    def _line(self, p1, p2):
        A = (p1.y - p2.y)
        B = (p2.x - p1.x)
        C = (p1.x * p2.y - p2.x * p1.y)
        return A, B, -C, p1, p2

    def _check_intersection(self, L1, L2):
        max_x = max([L1[3].x, L1[4].x, L2[3].x, L2[4].x])
        min_x = min([L1[3].x, L1[4].x, L2[3].x, L2[4].x])
        min_y = min([L1[3].y, L1[4].y, L2[3].y, L2[4].y])
        max_y = max([L1[3].y, L1[4].y, L2[3].y, L2[4].y])

        D = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            if (x > min_x and x < max_x) and (y > min_y and y < max_y):
                return x, y
            else:
                return False
        else:
            return False

    def _get_area_lines(self, area_geometry):
        total_points = len(area_geometry.points)
        lines = []
        for i, pt in enumerate(area_geometry.points):
            if i == 0:
                pass
            else:
                lines.append(self._line(area_geometry.points[i - 1], pt))
        return lines
