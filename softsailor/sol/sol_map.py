"""
Sol map module

Contains sol map implementation
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

import math
from bisect import bisect, bisect_left, insort
import numpy as np

from softsailor.utils import *
from sol_xmlutil import *

from geofun import Position, Line


def poly_intersect(poly, line):
    result = []
    for poly_part in poly:
        # First check boxes. If they don't intersect, the lines can't either
        if not line.intersects(poly_part):
            continue

        # Now check for actual intersection
        intersect_point = line.intersection(poly_part)
        result.append((poly_part, intersect_point))
    return result

class MapPoint(Position):
    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            super(MapPoint, self).__init__(args[0], args[1])
        elif len(args) > 0:
            super(MapPoint, self).__init__(args[0])
        else:
            super(MapPoint, self).__init__()

        self.links = []

    def other_link(self, point):
        for link_point in self.links:
            if not link_point is point:
                return link_point
        return None

    @property
    def link1(self):
        if len(self.links) > 0:
            return self.links[0]
        else:
            return None

    @property
    def link2(self):
        if len(self.links) > 1:
            return self.links[1]
        else:
            return None


def side_of(b1, b2, right=False):
    if b2 is None:
        return True
    if b1 is None:
        return True
    left = angle_diff(b1.a, b2.a) < 0
    if right:
        return not left
    else:
        return left

# Sizes of cells in tile maps
tile_cell_size = {'c': deg_to_rad(45), 
                  'h': deg_to_rad(1), 
                  'i': deg_to_rad(2), 
                  'l': deg_to_rad(10)}

class Map:

    def setup_cells(self):
        lat_cells = int(round((self.maxlat - self.minlat) / self.cellsize))
        lon_cells = int(round((self.maxlon - self.minlon) / self.cellsize))
        self.cells = [[[] for i in range(lon_cells)] for j in range(lat_cells)]

    def load_cell(self, cell_elem, cell):
        polys = get_elements(cell_elem, 'poly')
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
                        pl.append(Line(pos1, pos2))
                pos2 = pos1
            if len(pl) > 0:
                cell.append(pl)


    def load(self, mapurl):
        self.tiles = None
        dom = fetch_sol_document_from_url(mapurl)
        root = dom.childNodes[0]

        cellmap = get_element(root, 'cellmap')
        self.minlat = deg_to_rad(float(cellmap.getAttribute('minlat')))
        self.maxlat = deg_to_rad(float(cellmap.getAttribute('maxlat')))
        self.minlon = deg_to_rad(float(cellmap.getAttribute('minlon')))
        self.maxlon = deg_to_rad(float(cellmap.getAttribute('maxlon')))
        self.cellsize = deg_to_rad(float(cellmap.getAttribute('cellsize')))

        self.setup_cells()

        cells = get_elements(cellmap, 'cell')
        for cell in cells:
            cell_minlat = deg_to_rad(float(cell.getAttribute('minlat')))
            cell_minlon = deg_to_rad(float(cell.getAttribute('minlon')))
            lat_i = int(round((cell_minlat - self.minlat) / self.cellsize))
            lon_i = int(round((cell_minlon - self.minlon) / self.cellsize))
            self.load_cell(cell, self.cells[lat_i][lon_i])

        dom.unlink()
        self.__connect()

    def load_tile_dom(self, host, lati, loni):
        uri = '/site_media/maps/tiles/%s/%d_%d.xml.z' % (self.tiles, loni, lati)
        url = 'http://' + host + uri
        return fetch_sol_document_from_url(url)

    def load_tiles(self, host, tiles, loadarea=None):
        self.tiles = tiles
        self.minlat = loadarea[0]
        self.maxlat = loadarea[1]
        self.minlon = loadarea[2]
        self.maxlon = loadarea[3]

        self.cellsize = tile_cell_size[tiles]

        min_i = int(round((half_pi + self.minlat) / self.cellsize))
        min_j = int(round((pi + self.minlon) / self.cellsize))

        self.setup_cells()

        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                lati = min_i + i
                loni = min_j + j
                dom = self.load_tile_dom(host, lati, loni)
                root = dom.childNodes[0]

                cell_elem = get_element(root, 'cell')
                self.load_cell(cell_elem, cell)

                dom.unlink()

        self.__connect()


    def __hit(self, line):
        result = None
        # Maximum hit distance is the length of the line
        dist = line.v.r
        i1 = int(math.floor((line.p1.lat - self.minlat) / self.cellsize))
        j1 = int(math.floor((line.p1.lon - self.minlon) / self.cellsize))
        i2 = int(math.floor((line.p2.lat - self.minlat) / self.cellsize))
        j2 = int(math.floor((line.p2.lon - self.minlon) / self.cellsize))
        min_i = min(i1, i2)
        max_i = max(i1, i2)
        min_j = min(j1, j2)
        max_j = max(j1, j2)
        for i in range(min_i, max_i + 1):
            for j in range(min_j, max_j + 1):   
                for pl in self.cells[i][j]:
                    intersects = poly_intersect(pl, line) 
                    if intersects:
                        # Determine the closest hit
                        for poly_part, intersect_point in intersects:
                            intersect_bearing = intersect_point - line.p1
                            if intersect_bearing.r < dist:
                                result = poly_part
                                dist = intersect_bearing.r
        return result

    def hit(self, line):
        poly_part = self.__hit(line)
        if poly_part is not None:
            return True
        else:
            return False

    def outer(self, line):
        poly_part = self.__hit(line)
        p_outer = [None, None]
        if poly_part is not None:
            # Line intersects with land
            p = [self.__find_point(poly_part.p1), \
                 self.__find_point(poly_part.p2)]
            p_from = Position(line.p1)
            b = [p[0] - p_from, p[1] - p_from]
            b_outer = [None, None]
            if side_of(b[1], b[0], False):
                direction = 1
            else:
                direction = 0

            def trace_poly(forward, right):
                #print "Trace forward: %d direct %d" % (forward, right)
                p_cur = p[forward]
                # Remember last point in order to maintain direction
                p_last = p[1 - forward]
                # While there is a next point and we haven't gone completely round
                while p_cur and not p_cur is p[1 - forward]:
                    b_cur = p_cur - p_from
                    #print p_last, p_cur, b_cur
                    # Only when point is closer then line length, otherwise
                    # the point will never be reached
                    if b_cur[1] < line[1][1]:
                        if side_of(b_cur, b_outer[right], right):
                            b_outer[right] = b_cur
                            p_outer[right] = p_cur
                            #print 'Outer: ', p_outer[right], b_outer[right]
                    else:
                        pass
                        #print "Out of reach"

                    p_next = p_cur.other_link(p_last)
                    p_last = p_cur
                    p_cur = p_next

                # Poly ended (edge of map?). That's not a way around
                if not p_cur and p_last is p_outer[right]:
                    p_outer[right] = None

            trace_poly(0, direction)
            trace_poly(1, 1 - direction)

        return p_outer

                

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
                        p1 = self.__find_point(poly_part.p1)
                        p2 = self.__find_point(poly_part.p2)
                        if p1 is None:
                            p1 = MapPoint(poly_part.p1)
                            insort(self.points, p1)
                        if p2 is None:
                            p2 = MapPoint(poly_part.p2)
                            insort(self.points, p2)
                        p1.links.append(p2)
                        p2.links.append(p1)


