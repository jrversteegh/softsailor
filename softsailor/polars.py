"""
Polars module

Contains classes for dealing with boat polars
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"


import math
import numpy as np
from scipy import interpolate

from classes import Object
from utils import *

class Polars(Object):
    def __init__(self, *args, **kwargs):
        super(Polars, self).__init__(*args, **kwargs)
        self._mesh = None
        self._data = None
        try:
            self._filename = kwargs['filename']
            self.load_from_file()
        except KeyError:
            self._filename = 'noname.txt'
        try:
            wss = kwargs['wss']
            was = kwargs['was']
            vs = kwargs['vs']
            self._mesh = np.meshgrid(wss, was)
            self._data = np.array(vs)
            self._update_splines()
        except KeyError:
            pass

        try:
            self._mesh = kwargs['mesh']
            self._data = kwargs['data']
            self._update_splines()
        except KeyError:
            pass


    def _update_splines(self):
        size = min(len(self.angles), len(self.speeds))
        smoothing = size - 0.5 * math.sqrt(2 * size)
        self._cfs = interpolate.bisplrep(self._mesh[0], self._mesh[1],
                                         self._data, s=smoothing)


    def save_to_file(self, filename=None):
        if not filename:
            filename = self._filename
        with open(filename, "w") as f:
            f.write('# Wind speeds\n')
            for speed in self.speeds:
                f.write(' %.2f' % ms_to_kn(speed))
            f.write("\n")
            f.write('# Wind angles\n')
            for angle in self.angles:
                f.write(' %.2f' % rad_to_deg(angle))
            f.write("\n")
            f.write('# Boat speeds\n')
            for r in self.data:
                for c in r:
                    f.write(' %.2f' % ms_to_kn(c))
                f.write("\n")


    def load_from_file(self, filename=None):
        if not filename:
            filename = self._filename
        self._filename = filename
        f = open(filename, "r")
        f.close()
        self._update_splines()


    @property
    def mesh(self):
        return self._mesh

    @property
    def data(self):
        return self._data

    @property
    def angles(self):
        return self._mesh[1][:,0]

    @property
    def speeds(self):
        return self._mesh[0][0,:]

    def get(self, angles, windspeed=None):
        if windspeed is None:
            angles, windspeed = angles
        angles = np.fabs(angles)
        return interpolate.bisplev(windspeed, angles, self._cfs)
