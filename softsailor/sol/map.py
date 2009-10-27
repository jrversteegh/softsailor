from bisect import bisect

from xmlutil import *

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
        dom.unlink()

    def hit(self, segment):
        pass
