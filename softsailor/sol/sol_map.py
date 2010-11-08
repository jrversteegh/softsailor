import math
from bisect import bisect

from softsailor.utils import *
from softsailor.classes import *

from sol_xmlutil import *

def poly_intersect(poly, segment):
    for poly_segment in poly:
        # I know there is a good optimization in here somewhere
        # I just can't figure it out now...
        bearing1 = segment[2].get_bearing_from(poly_segment[0])
        bearing2 = segment[2].get_bearing_from(poly_segment[2]) 
        phi1 = normalize_angle_pipi(segment[1][0] - bearing1[0])
        phi2 = normalize_angle_pipi(segment[1][0] - bearing2[0])
        # When the angles have a different sign, the points lie
        # each on different sides of the course line.
        # Further investigation required
        if (phi1 > 0 and phi2 <= 0) or (phi1 <= 0 and phi2 > 0):
            # Now check if the two points of the course segment lie on different 
            # sides of the poly segment. 
            bearing2 = segment[0].get_bearing_from(poly_segment[0])
            phi1 = normalize_angle_pipi(poly_segment[1][0] - bearing1[0])
            phi2 = normalize_angle_pipi(poly_segment[1][0] - bearing2[0])
            if (phi1 > 0 and phi2 <= 0) or (phi1 <= 0 and phi2 > 0):
                return True
    return False

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
                    if pos2 != None:
                      pl.append((pos1, pos2 - pos1, pos2))
                    pos2 = pos1
                self.cells[lat_i][lon_i].append(pl)

        dom.unlink()


    def hit(self, segment):
        lat_i = int(math.floor((segment[2][0] - self.minlat) / self.cellsize))
        lon_i = int(math.floor((segment[2][1] - self.minlon) / self.cellsize))
        for pl in self.cells[lat_i][lon_i]:
            if poly_intersect(pl, segment):
                return True
        return False

