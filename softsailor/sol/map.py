from bisect import bisect

from xmlutil import *
from utils import *

class Map:
    def load(self, mapurl):
        dom = fetch_sol_document_from_url(mapurl)
        root = dom.childNodes[0]
        cellmap = get_element(root, 'cellmap')
        minlat = int(cellmap.getAttribute('minlat'))
        maxlat = int(cellmap.getAttribute('maxlat'))
        minlon = int(cellmap.getAttribute('minlon'))
        maxlon = int(cellmap.getAttribute('maxlon'))
        cellsize = int(cellmap.getAttribute('cellsize'))
        lat_cells = (maxlat - minlat) / cellsize
        lon_cells = (maxlon - minlon) / cellsize
        self.cells = [[[] for i in range(lon_cells)] for j in range(lat_cells)]
        cells = get_elements(cellmap, 'cell')
        for cell in cells:
            cell_minlat = int(cell.getAttribute('minlat'))
            cell_minlon = int(cell.getAttribute('minlon'))
            lat_i = (cell_minlat - minlat) / cellsize
            lon_i = (cell_minlon - minlon) / cellsize
            polys = get_elements(cell, 'poly')
            for poly in polys:
                pl = []
                points = get_elements(poly, 'point')
                for point in points:
                    lat = float(point.getAttribute('lat'))
                    lon = float(point.getAttribute('lon'))
                    pl.append((deg_to_rad(lat), deg_to_rad(lon)))
                self.cells[lat_i][lon_i].append(pl)

        dom.unlink()

    def hit(self, segment):
        pass
