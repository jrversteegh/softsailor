"""
Polars module

Contains classes for dealing with boat polars
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"


import numpy as np

from classes import Object

class Polars(Object):
    _filename = ''
    def __init__(self, *args, **kwargs):
        super(Polars, self).__init__(*args, **kwargs)
        try:
            self._filename = kwargs['filename']
        except KeyError:
            pass
        try:
            self._mesh = kwargs['mesh']
            self._data = kwargs['data']
        except KeyError:
            pass

    def save_to_file(self, filename):
        angles, windspeeds = self._data.shape
        f = open(filename, "w")
        for i in range(angles):
            angle = self._mesh[0, i, 0]
            f.write('%.2f' % rad_to_deg(angle) + ':')
            for j in range(windspeeds):
                windspeed = self._mesh[1, 0, j]
                boatspeed = self._data[i, j]
                f.write(' %.2f:%.2f' % (ms_to_kn(wind_speed),
                                        ms_to_kn(boat_speed)))
            f.write("\n")
        f.close()

    def load_from_file(self, filename):
        f = open(filename, "r")
        f.close()
