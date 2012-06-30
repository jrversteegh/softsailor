"""
Sol chart module

Contains sol chart implementation
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

import math
from bisect import bisect, bisect_left, insort
import numpy as np
from time import sleep
from logging import getLogger
_log = getLogger('softsailor.sol.sol_chart')

from softsailor.utils import *
from softsailor.chart import Path, Chart
from softsailor.route import Route
from sol_xmlutil import *

from geofun import Position, Line, floats_equal


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

def trace_poly(point, first=True):
    if first:
        p = point.link1
    else:
        p = point.link2
    last_p = point
    while p is not None and p is not point:
        yield p
        new_p = p.other_link(last_p)
        last_p = p
        p = new_p

class ChartPointException(Exception):
    pass

class ChartPoint(Position):
    link1 = None
    link2 = None
    section = -1
    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            super(ChartPoint, self).__init__(args[0], args[1])
        elif len(args) > 0:
            super(ChartPoint, self).__init__(args[0][0], args[0][1])
        else:
            super(ChartPoint, self).__init__()

    def other_link(self, point):
        if point is self.link1:
            return self.link2
        elif point is self.link2:
            return self.link1
        else:
            raise ChartPointException('Parameter "point" should be one of the two links')

    def set_link(self, point):
        if self.link1 is None:
            self.link1 = point
        elif self.link2 is None:
            if point is self.link1:
                self.link1 = None
            else:
                self.link2 = point
        else:
            if point is self.link1:
                try:
                    self.link1 = self.link3
                    del self.link3
                except AttributeError:
                    self.link1 = None
            elif point is self.link2:
                self.link2 = None
            else:
                try:
                    if point is self.link3:
                        del self.link3
                    else:
                        raise ChartPointException(
                            'Point already fully linked: %s -> 1: %s 2: %s 3: %s new: %s' % \
                              (str(self), 
                               str(self.link1), str(self.link2), str(self.link3), 
                               str(point)))
                except AttributeError:
                    self.link3 = self.link1
                    self.link1 = point

    def is_degenerate(self):
        return self.link1 == self.link2


def side_of(v1, v2, right=False):
    if v2 is None:
        return True
    if v1 is None:
        return True
    da = angle_diff(v1.a, v2.a)
    if right:
        return da > 0
    else:
        return da < 0

def angle_bigger(a1, a2, right=True):
    # No angle_diff here as this functions compares absolute angles
    da = a1 - a2
    if right:
        return da > 0
    else:
        return da < 0


# Sizes of cells in tile maps
tile_cell_size = {'c': deg_to_rad(45), 
                  'h': deg_to_rad(1), 
                  'i': deg_to_rad(2), 
                  'l': deg_to_rad(10)}
tile_cell_count = {'c': 360 / 45, 
                   'h': 360, 
                   'i': 360 / 2, 
                   'l': 360 / 10}

class SolChart(Chart):
    @property
    def lat_range(self):
        return self.maxlat - self.minlat

    @property
    def lon_range(self):
        return normalize_angle_2pi(self.maxlon - self.minlon)

    def cell_offset(self, lat, lon):
        return int(round((lat - self.minlat) / self.cellsize)), \
               int(round(normalize_angle_2pi(lon - self.minlon) / self.cellsize))

    def setup_cells(self):
        lat_cells = int(round(self.lat_range / self.cellsize))
        lon_cells = int(round(self.lon_range / self.cellsize))
        _log.info('Chart range: %f %f %f %f' % ( 
                  rad_to_deg(self.minlat), 
                  rad_to_deg(self.maxlat), 
                  rad_to_deg(self.minlon), 
                  rad_to_deg(self.maxlon)))
        _log.info('Cells: %d %d' % (lat_cells, lon_cells))
        self.cells = [[[] for i in range(lon_cells)] for j in range(lat_cells)]

    def load_cell(self, cell_elem, cell):
        polys = get_elements(cell_elem, 'poly')
        for poly in polys:
            pl = []
            points = get_elements(poly, 'point')
            if points:
                # Start with the last point
                point = points[-1]
                lat = float(point.getAttribute('lat'))
                lon = float(point.getAttribute('lon'))
                pos1 = Position(deg_to_rad(lat), deg_to_rad(lon))
            for point in points:
                lat = float(point.getAttribute('lat'))
                lon = float(point.getAttribute('lon'))
                pos2 = Position(deg_to_rad(lat), deg_to_rad(lon))
                # There are duplicates in the list (why is a bit unclear to me)
                if not (pos2 == pos1):
                    # Avoid adding grid lines
                    looks_like_grid = False
                    if pos1.lat == pos2.lat: 
                        # This line is horizontal
                        rounded = round(pos1.lat / self.cellsize)
                        rounded *= self.cellsize
                        if floats_equal(pos1.lat, rounded):
                            looks_like_grid = True
                    if pos1.lon == pos2.lon: 
                        # This line is vertical
                        rounded = round(pos1.lon / self.cellsize)
                        rounded *= self.cellsize
                        if floats_equal(pos1.lon, rounded):
                            looks_like_grid = True
                    if not looks_like_grid:
                        pl.append(Line(pos1, pos2))
                pos1 = pos2
            if len(pl) > 0:
                cell.append(pl)


    def load(self, mapurl):
        self.tiles = None
        dom = fetch_sol_document_from_url(mapurl, cached=True)
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
            lat_i, lon_i = self.cell_offset(cell_minlat, cell_minlon)
            try:
                self.load_cell(cell, self.cells[lat_i][lon_i])
            except Exception as e:
                raise Exception('Error in ' + mapurl + '. ' + str(e))

        dom.unlink()
        self.__connect()
        self.__setup_sections()

    def load_tile_dom(self, host, lati, loni):
        loni %= tile_cell_count[self.tiles]
        uri = '/site_media/maps/tiles/%s/%d_%d.xml.z' % (self.tiles, loni, lati)
        url = 'http://' + host + uri
        return fetch_sol_document_from_url(url, cached=True), url

    def get_chart_size(self, load_area):
        # Initialize to world...
        self.minlat = -half_pi
        self.maxlat =  half_pi 
        self.minlon = -2 * pi 
        self.maxlon =  2 * pi 
        if load_area is not None:
            # ... and shrink to sailing arena
            while self.minlat <= load_area[0]:
                self.minlat += self.cellsize
            while self.maxlat >= load_area[1]:
                self.maxlat -= self.cellsize
            while self.minlon <= normalize_angle_pipi(load_area[2]):
                self.minlon += self.cellsize
            while self.maxlon >= normalize_angle_pipi(load_area[3]):
                self.maxlon -= self.cellsize
        # .. and add a border of 1, because we shrunk to inside the arena
        self.minlat -= self.cellsize
        self.maxlat += self.cellsize
        self.minlon -= self.cellsize
        self.maxlon += self.cellsize

    def load_tiles(self, host, tiles, load_area=None):
        self.tiles = tiles

        self.cellsize = tile_cell_size[tiles]

        self.get_chart_size(load_area)

        _log.info('Race area: %s' % str(rad_to_deg(load_area)))

        min_i = int(round((half_pi + self.minlat) / self.cellsize))
        min_j = int(round((pi + self.minlon) / self.cellsize))

        self.setup_cells()

        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                lati = min_i + i 
                loni = min_j + j
                dom, mapurl = self.load_tile_dom(host, lati, loni)
                root = get_first_element(dom)

                cell_elem = get_element(root, 'cell')
                try:
                    self.load_cell(cell_elem, cell)
                except Exception as e:
                    raise Exception('Error in ' + mapurl + '. ' + str(e))

                dom.unlink()

        self.__connect()
        self.__setup_sections()

    def __intersects(self, line):
        result = []
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
                try:
                    for pl in self.cells[i][j]:
                        intersects = poly_intersect(pl, line) 
                        for intersect in intersects:
                            result.append(intersect)
                except IndexError:
                    raise Exception('Line %s outside of map: %f, %f - %f, %f' \
                                    % (str(line), 
                                       self.minlat, 
                                       self.minlon,
                                       self.maxlat,
                                       self.maxlon))
        return result

    def __hit(self, line):
        result = (None, None)
        # Maximum hit distance is the length of the line
        dist = line.v.r
        intersects = self.__intersects(line)
        # Determine the closest hit
        for poly_part, intersect in intersects:
            intersect_vec = intersect - line.p1
            if intersect_vec.r < dist:
                result = poly_part, intersect
                dist = intersect_vec.r
        return result

    def hit(self, line):
        segment, point = self.__hit(line)
        if segment is not None:
            return True
        else:
            return False

    def intersect(self, line):
        return self.__hit(line)

    def intersections(self, line):
        result = []
        intersects = self.__intersects(line)
        for line, point in intersects:
            result.append(point)
        return result

    def route_around(self, line, distance_hint=1E8):
        poly_part, intersect = self.__hit(line)
        if poly_part is None:
            # We didn't hit anything :)
            return [[Position(line.p1), Position(line.p2)]]

        _log.debug('routing line %s - %s around %s' % ( 
            str(line.p1), str(line.p2), str(intersect)))

        # We're hitting so set up left and right around as
        # the line sections from current position to hit point
        result = [[Position(line.p1)], [Position(line.p1)]]
        
        # Find the points of the map line that is being intersected
        # (This should not really be necessary.. as the poly_part
        # could already contain this information, but doesn't at
        # the moment. The poly_part points are not ChartPoints)
        p1 = self.__find_point(poly_part.p1)
        p2 = self.__find_point(poly_part.p2)
        b1 = p1 - line.p1
        b2 = p2 - line.p1
        right = side_of(b2, b1, True)

        def trace_poly(p_last, p, right):
            points = result[right]
            a = line.v.a  # Angle of line from last point to current point
            b = a
            a_max = a
            p_max = None
            p_start = p
            p_next = None

            while True:
                # Poly ended (edge of map?) or looped back to start
                if p is None or ((p_next is not None) and (p == p_start)):
                    if p_max == p_last:
                        result[right] = None
                    break

                try:
                    # Cumulative angles
                    ar = p - line.p1
                    a += angle_diff(ar.a, a)
                    br = line.p2 - p  # Target bearing
                    b += angle_diff(br.a, b)

                    # Distance to target exceeds distance hint, invalidate this
                    # solution
                    if br.r > distance_hint:
                        result[right] = None
                        break

                    # We've gone more than halfway around the target: stop for
                    # now
                    if abs(b - line.v.a) > pi:
                        break

                    # Check if we've found a new 'outer' point
                    if angle_bigger(a, a_max, right):
                        a_max = a
                        p_max = p
                finally:
                    p_next = p.other_link(p_last)
                    p_last = p
                    p = p_next

            assert p_max is not None, '%f %f %f %s' % (line.v.a, a, a_max, str(right))
            v = p_max - line.p1
            p = p_max + veer_vector(v, right)
            points.append(Position(p))
            points.append(Position(line.p2))

        # Trace both directions
        trace_poly(p1, p2, right)
        trace_poly(p2, p1, not right)

        try:
            result.remove(None)
            result.remove(None)
            raise Exception('Expected at least one route around')
        except ValueError:
            pass

        return result
                

    def __find_point(self, point):
        i = bisect_left(self.points, point)
        try:
            if self.points[i] == point:
                return self.points[i]
            else:
                return None
        except IndexError:
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
                            p1 = ChartPoint(poly_part.p1)
                            insort(self.points, p1)
                        if p2 is None:
                            p2 = ChartPoint(poly_part.p2)
                            insort(self.points, p2)
                        p1.set_link(p2)
                        p2.set_link(p1)
        for point in self.points:
            if point.is_degenerate():
                _log.info('Removed degenerate point: %s' % str(point))
        _log.info('Connected map with %d points' % len(self.points))

    def __setup_sections(self):
        self.sections = []
        for point in self.points:
            if point.section < 0:
                point.section = len(self.sections)
                for connected_point in trace_poly(point, True):
                    connected_point.section = len(self.sections)
                for connected_point in trace_poly(point, False):
                    if connected_point.section >= 0:
                        break
                    # If we ended up here, this is an open polygon: 
                    # reassign "point" so "point" becomes a tail
                    # of the open polygon
                    point = connected_point
                    point.section = len(self.sections)
                self.sections.append(point)
        _log.info('Found %d sections in map' % len(self.sections))


    def save_to_kml(self, filename):
        filedir, file = os.path.split(filename)
        filebase, fileext = os.path.splitext(file)

        kml, doc = create_kml_document('Chart: ' + filebase)

        factory = kmldom.KmlFactory_GetFactory()
        
        lines = factory.CreateFolder()
        lines.set_name('Chart')
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                for poly in cell:
                    for i, ln in enumerate(poly):
                        vec = ln.v
                        p1 = list(ln.p1)
                        p2 = list(ln.p2)
                        ln = (rad_to_deg(p1), rad_to_deg(p2))
                        line = create_line_placemark('Segment ' + str(i), ln)
                        description = pos_to_str(p1) + ' - ' + pos_to_str(p2)
                        line.set_description(description)
                        lines.add_feature(line)

        description = pos_to_str((self.minlat, self.minlon)) + ' - ' \
                    + pos_to_str((self.maxlat, self.maxlon))
        doc.set_description(description)
        doc.add_feature(lines)
        
        save_kml_document(kml, filename)


