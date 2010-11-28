import math
from bisect import bisect, bisect_left, insort
import numpy as np

from softsailor.utils import *
from softsailor.classes import *

from sol_xmlutil import *

def poly_intersect(poly, line):
    if line[0][0] > line[2][0]:
        max_line_lat = line[0][0]
        min_line_lat = line[2][0]
    else:
        max_line_lat = line[2][0]
        min_line_lat = line[0][0]
    if line[0][1] > line[2][1]:
        max_line_lon = line[0][1]
        min_line_lon = line[2][1]
    else:
        max_line_lon = line[2][1]
        min_line_lon = line[0][1]
    for poly_part in poly:
        # First check boxes. If they don't intersect, the lines can't either
        if (poly_part[0][0] > max_line_lat \
                    and poly_part[2][0] > max_line_lat) \
                or (poly_part[0][0] < min_line_lat \
                    and poly_part[2][0] < min_line_lat) \
                or (poly_part[0][1] > max_line_lon \
                    and poly_part[2][1] > max_line_lon) \
                or (poly_part[0][1] < min_line_lon \
                    and poly_part[2][1] < min_line_lon):
            continue

        # Now check for actual intersection
        bearing1 = line[2].get_bearing_from(poly_part[0])
        bearing2 = line[2].get_bearing_from(poly_part[2]) 
        phi1 = normalize_angle_pipi(line[1][0] - bearing1[0])
        phi2 = normalize_angle_pipi(line[1][0] - bearing2[0])
        # When the angles have a different sign, the points lie
        # each on different sides of the course line.
        # Further investigation required
        if (phi1 > 0 and phi2 <= 0) or (phi1 <= 0 and phi2 > 0):
            # Now check if the two points of the course segment lie on different 
            # sides of the poly segment. 
            bearing2 = line[0].get_bearing_from(poly_part[0])
            phi1 = normalize_angle_pipi(poly_part[1][0] - bearing1[0])
            phi2 = normalize_angle_pipi(poly_part[1][0] - bearing2[0])
            if (phi1 > 0 and phi2 <= 0) or (phi1 <= 0 and phi2 > 0):
                return True
    return False

class MapPoint(Position):
    def __init__(self, *args, **kwargs):
        super(MapPoint, self).__init__(*args, **kwargs)
        self.links = []

class Map:
    def load(self, mapurl):
        dom = fetch_sol_document_from_url(mapurl)
        root = dom.childNodes[0]

        cellmap = get_element(root, 'cellmap')
        self.minlat = deg_to_rad(float(cellmap.getAttribute('minlat')))
        self.maxlat = deg_to_rad(float(cellmap.getAttribute('maxlat')))
        self.minlon = deg_to_rad(float(cellmap.getAttribute('minlon')))
        self.maxlon = deg_to_rad(float(cellmap.getAttribute('maxlon')))
        self.cellsize = deg_to_rad(float(cellmap.getAttribute('cellsize')))

        lat_cells = int(round((self.maxlat - self.minlat) / self.cellsize))
        lon_cells = int(round((self.maxlon - self.minlon) / self.cellsize))
        self.cells = [[[] for i in range(lon_cells)] for j in range(lat_cells)]
        cells = get_elements(cellmap, 'cell')
        for cell in cells:
            cell_minlat = deg_to_rad(float(cell.getAttribute('minlat')))
            cell_minlon = deg_to_rad(float(cell.getAttribute('minlon')))
            lat_i = int(round((cell_minlat - self.minlat) / self.cellsize))
            lon_i = int(round((cell_minlon - self.minlon) / self.cellsize))
            polys = get_elements(cell, 'poly')
            for poly in polys:
                pl = []
                points = get_elements(poly, 'point')
                pos2 = None
                for point in points:
                    lat = float(point.getAttribute('lat'))
                    lon = float(point.getAttribute('lon'))
                    pos1 = Position(deg_to_rad(lat), deg_to_rad(lon))
                    if not pos2 is None and not pos2 == pos1:
                        # Avoid adding grid lines
                        looks_like_grid = False
                        if pos1[0] == pos2[0]: 
                            # This line is horizontal
                            rounded = round(pos1[0] / self.cellsize)
                            rounded *= self.cellsize
                            if np.allclose(pos1[0], rounded):
                                looks_like_grid = True
                        if pos1[1] == pos2[1]: 
                            # This line is vertical
                            rounded = round(pos1[1] / self.cellsize)
                            rounded *= self.cellsize
                            if np.allclose(pos1[1], rounded):
                                looks_like_grid = True
                        if not looks_like_grid:
                            pl.append((pos1, pos2 - pos1, pos2))
                    pos2 = pos1
                if len(pl) > 0:
                    self.cells[lat_i][lon_i].append(pl)

        dom.unlink()
        self.__connect()


    def hit(self, line):
        i1 = int(math.floor((line[0][0] - self.minlat) / self.cellsize))
        j1 = int(math.floor((line[0][1] - self.minlon) / self.cellsize))
        i2 = int(math.floor((line[2][0] - self.minlat) / self.cellsize))
        j2 = int(math.floor((line[2][1] - self.minlon) / self.cellsize))
        min_i = min(i1, i2)
        max_i = max(i1, i2)
        min_j = min(j1, j2)
        max_j = max(j1, j2)
        for i in range(min_i, max_i + 1):
            for j in range(min_j, max_j + 1):   
                for pl in self.cells[i][j]:
                    if poly_intersect(pl, line):
                        return True
        return False

    def outer(self, line):
        return tuple()

    def __find_point(self, point):
        i = bisect_left(self.points, point)
        if i != len(self.points) and self.points[i] == point:
            return self.points[i]
        else:
            return None
    
    def __connect(self):
        self.points = []
        for cell_row in self.cells:
            for cell in cell_row:
                for polys in cell:
                    for poly_part in polys:
                        p1 = self.__find_point(poly_part[0])
                        p2 = self.__find_point(poly_part[2])
                        if p1 is None:
                            p1 = MapPoint(poly_part[0])
                            insort(self.points, p1)
                        if p2 is None:
                            p2 = MapPoint(poly_part[2])
                            insort(self.points, p2)
                        p1.links.append(p2)
                        p2.links.append(p1)


