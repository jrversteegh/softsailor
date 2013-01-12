"""
Grib wind module

Contains implementation wind provider for grib data
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from datetime import datetime, timedelta
import math
import os.path
import numpy as np
import pygrib as pg

from softsailor.utils import *
from softsailor.wind import *


class GribWind(InterpolledWind):
    _filename = ''
    _filedate = 0
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self._filename = args[0]
        else:
            try:
                self._filename = kwargs['filename']
            except KeyError:
                pass
        super(GribWind, self).__init__(*args, **kwargs)

    def update(self):
        self.update_from_file()

    def update_from_file(self, filename=''):
        if filename:
            self._filename = filename
            self._filedate = 0
        if self._filename:
            if not os.path.isfile(self._filename):
                raise Exception('Grib file doesn''t exist: %s' % self._filename)
            fdate = os.path.getmtime(self._filename)
            if fdate != self._filedate:
                self._load_from(self._filename)
                self._filedate = fdate

    def _load_from(self, filename):
        grb = pg.open(filename)
        # Dictionary with data with time as key and a dictionary with properties
        # as values
        data = {}
        for msg in grb:
            fcst = timedelta(hours=msg.unitOfTimeRange * msg.P1)
            t = msg.analDate + fcst
            try:
                d = data[t]
            except KeyError:
                d = {'fcst': fcst}
                data[t] = d
            # Handle u and v messages, mind that u and v in grib are 
            # inverted, because the grib definition is u -> y direction(east)
            # v -> x direction(north)
            if msg.paramId in [131, 165]:  # U component (surface or 10m)
                self._add_data(d, 'v', msg, fcst)
            elif msg.paramId in [132, 166]: # V component (surface or 10m)
                self._add_data(d, 'u', msg, fcst)
            else:
                pass
        self._arrays_from_data(data)

    def _data_shape(self, data):
        las, los, ts = (0, 0, 0)
        for k, v in data.iteritems():
            ts += 1
            s = v['grid'][0].shape
            if s[0] > las:
                las = s[0]
            if s[1] > los:
                los = s[1]
        return (las, los, ts)


    def _add_data(self, dct, key, msg, fcst):
        try:
            vals = dct[key]
            # The values already exist. Only get new once in
            # case the forecast offset is less i.e. the data is newer
            if fcst > dct['fcst']:
                return
        except KeyError:
            pass # Expected
        dct['grid'] = np.array(msg.latlons()) * (math.pi / 180.)
        if msg.units == 'm s**-1':
            unitf = 1.
        elif msg.units == 'knots':
            unitf = 1852. / 3600.
        elif msg.units == 'km h**-1':
            unitf = 1000. / 3600.
        else:
            raise Exception('Unexpected unit for wind speed: %s' % msg.units)
        dct[key] = np.array(msg.values) * unitf
       
    def _arrays_from_data(self, data):
        # Clear any calculation state
        self.clear()
        # Setup grid shape and init value arrays
        shape = self._data_shape(data)
        self.grid = np.zeros((3,) + shape)
        self.init_value_arrays()

        times = sorted(data.keys())
        if len(times) == 0:
            return
        self.start = times[0]
        secs = np.zeros(len(times))
        # Loop over the data
        for i, t in enumerate(times):
            secs[i] = (t - self.start).total_seconds()
            d = data[t]
            self.u[:,:,i] = d['u']
            self.v[:,:,i] = d['v']
            self.grid[:2,:,:,i] = d['grid']

        # Set time coordinates of the mesh
        self.grid[2,:,:] = secs

        # Update calculation coefficients
        self.update_coefficients()
            




        





