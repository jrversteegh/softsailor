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
import time

from softsailor.utils import *
from softsailor.map import Map
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

class MapPoint(Position):
    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            super(MapPoint, self).__init__(args[0], args[1])
        elif len(args) > 0:
            super(MapPoint, self).__init__(args[0][0], args[0][1])
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

class SolMap(Map):

    def setup_cells(self):
        lat_cells = int(round((self.maxlat - self.minlat) / self.cellsize))
        lon_cells = int(round((self.maxlon - self.minlon) / self.cellsize))
        self.cells = [[[] for i in range(lon_cells)] for j in range(lat_cells)]

    def load_cell(self, cell_elem, cell):
        polys = get_elements(cell_elem, 'poly')
        for poly in polys:
            pl = []
            points = get_elements(poly, 'point')
            if points:
                point = points[-1]
                lat = float(point.getAttribute('lat'))
                lon = float(point.getAttribute('lon'))
                pos2 = Position(deg_to_rad(lat), deg_to_rad(lon))
            for point in points:
                lat = float(point.getAttribute('lat'))
                lon = float(point.getAttribute('lon'))
                pos1 = Position(deg_to_rad(lat), deg_to_rad(lon))
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
        self.minlat = -half_pi
        self.maxlat =  half_pi 
        self.minlon = -pi 
        self.maxlon =  pi 

        self.cellsize = tile_cell_size[tiles]

        if loadarea is not None:
            while self.minlat <= loadarea[0]:
                self.minlat += self.cellsize
            while self.maxlat >= loadarea[1]:
                self.maxlat -= self.cellsize
            while self.minlon <= loadarea[2]:
                self.minlon += self.cellsize
            while self.maxlon >= loadarea[3]:
                self.maxlon -= self.cellsize
            self.minlat -= self.cellsize
            self.maxlat += self.cellsize
            self.minlon -= self.cellsize
            self.maxlon += self.cellsize

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
                for pl in self.cells[i][j]:
                    intersects = poly_intersect(pl, line) 
                    for intersect in intersects:
                        result.append(intersect)
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

    def _outer_points_first(self, line):
        poly_part, intersect = self.__hit(line)
        p_outer = [[line.p1], None]
        if poly_part is not None:
            p_outer[True] = [line.p1]
            # Line intersects with land
            p_outer[False].append(intersect)
            p_outer[True].append(intersect)
            #print pos_to_str(line.p1), pos_to_str(line.p2), pos_to_str(intersect)

            # Find the points of the map line that is being intersected
            # (This should not really be necessary.. as the poly_part
            #  could already contain this information, but doesn't at
            #  the moment. The poly_part points are not MapPoints)
            p1 = self.__find_point(poly_part.p1)
            p2 = self.__find_point(poly_part.p2)
            b1 = p1 - line.p1
            b2 = p2 - line.p1
            right = side_of(b2, b1, True)

            def trace_poly(p_last, p_cur, right):
                #print "============================================"
                #print "Trace right", right
                p_start = p_last
                ps = p_outer[right]
                b = line.v.a 
                a = b
                g = a
                ans = [line.v.a]
                def last_a():
                    if ans:
                        return ans[-1]
                    else:
                        return line.v.a
                def new_a():
                    return (p_cur - ps[-1]).a
                def new_b():
                    return (line.p2 - p_cur).a
                def new_g():
                    return (p_cur - p_last).a
                # While there is a next point and we haven't gone completely round
                while (p_cur is not None) and (p_cur is not p_start):
                    # Cumulative angle
                    a += angle_diff(new_a(), a)
                    b += angle_diff(new_b(), b)
                    g += angle_diff(new_g(), g)
                    # Remove points that lie within the convex hull upto
                    # the current point
                    #print 'Cur', pos_to_str(p_cur), 'A: ', ang_to_str(a)
                    #time.sleep(1)
                    while ans and \
                            angle_bigger(a, last_a(), right) and \
                            angle_bigger(a, b, right):
                        #print "Removed. New len %d" % len(ps)
                        la = ans.pop()
                        lp = ps.pop()
                        a = la + angle_diff(new_a(), la)
                    # if this point 'hides' the last point, then replace the last
                    # point with this one. This is a bit of a hack to get past 
                    # inlets, which can make the convex hull upto the current 
                    # point intersect with the land, causing the calculation 
                    # of a to be off by 2 pi. 
                    # TODO I think this could be done better by properly
                    # calculating a instead, but that looks non-trivial
                    if ans and math.fabs(a - g) > pi and ps[-1] == p_last:
                        a = ans.pop()
                        p = ps.pop()
                        #print 'Popped %s %s %s' % (pos_to_str(p), ang_to_str(a), ang_to_str(g))
                        a += angle_diff(new_a(), a)
                        ps.append(p_cur)
                        #print 'Pushed %s %s' % (pos_to_str(p_cur), ang_to_str(a))
                        ans.append(a)
                    # Only add this point when going 'outside' of straight line
                    # to p2, otherwise we apparently have a clear look at p2
                    # and can go straight toward it. At least the way it looks
                    # now
                    elif angle_bigger(a, b, right):
                        ps.append(p_cur)
                        ans.append(a)
                        #else:
                        #print "Not adding a: %s b: %s" % (ang_to_str(a), ang_to_str(b))

                    p_next = p_cur.other_link(p_last)
                    p_last = p_cur
                    p_cur = p_next

                # Poly ended (edge of map?) and last point was part of the
                # expected curve. This is a dead end...
                if p_cur is None and p_last == ps[-1] \
                        or len(p_outer[right]) == 1:  
                        # or when only the start point is still present
                        # that might mean we arrived the wrong way around a bay
                        # i.e. when the border is completely concave and hence
                        # hence the convex hull empty
                    p_outer[right] = None
                else:
                    ps.append(line.p2)

            # Trace both directions
            trace_poly(p1, p2, right)
            trace_poly(p2, p1, not right)
            p_outer[False] = push_out(p_outer[False], chart=self)
            p_outer[True] = push_out(p_outer[True], chart=self)

            def check_not_intersecting_self(p_list):
                if p_list:
                    p_l = p_list[0]
                    for p in p_list[1:]:
                        l = Line(p_l, p)

                        t_l = p1
                        t = p2
                        while t and not (t == p1):
                            r = Line(t_l, t)
                            if r.intersects(l):
                                return False
                            t_o = t_l
                            t_l = t
                            t = t.other_link(t_o)

                        t_l = p2
                        t = p1
                        while t and not (t == p2):
                            r = Line(t_l, t)
                            if r.intersects(l):
                                return False
                            t_o = t_l
                            t_l = t
                            t = t.other_link(t_o)

                        p_l = p
                return True

            rt = None
            if not check_not_intersecting_self(p_outer[False]):
                rt = Route(p_outer[False])
                s = 'Problem left'
            if not check_not_intersecting_self(p_outer[True]):
                rt = Route(p_outer[True])
                s = 'Problem right'
            if rt:
                rt.save_to_kml('failed.kml')
                rt.save_to_file('failed.txt')
                raise Exception(s)
                        
        else:
            p_outer[False].append(line.p2)

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

    def save_to_kml(self, filename):
        filedir, file = os.path.split(filename)
        filebase, fileext = os.path.splitext(file)

        kml, doc = create_kml_document('Map: ' + filebase)

        factory = kmldom.KmlFactory_GetFactory()
        
        lines = factory.CreateFolder()
        lines.set_name('Map')
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
                        line.set_description(description.encode("utf-8"))
                        lines.add_feature(line)

        description = pos_to_str((self.minlat, self.minlon)) + ' - ' \
                    + pos_to_str((self.maxlat, self.maxlon))
        doc.set_description(description.encode("utf-8"))
        doc.add_feature(lines)
        
        save_kml_document(kml, filename)


