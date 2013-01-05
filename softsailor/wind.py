"""
Wind module

Contains an wind data provider interface
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from math import pi
from datetime import datetime, timedelta

import numpy as np
from scipy.ndimage.interpolation import spline_filter, map_coordinates

from classes import Object
from utils import *


class Wind(Object):
    '''Basic prototype for wind object'''
    def get(self, position, time = None):
        """Get wind direction at position an time"""
        # Default is a 5m/s southerly wind
        return pi, 5.0

class GriddedWind(Wind):
    '''Base class for 3D grid based wind objects'''
    lon_2pi = False  # Indicates whether longitude grid is [0, 2pi> instead
                     # of [-pi, pi>

    def __init__(self, *args, **kwargs):
        super(GriddedWind, self).__init__(*args, **kwargs)
        # Start datetime of data. Times are relative from this datetime
        try:
            self.start = kwargs['start']
        except KeyError:
            self.start = datetime(1970, 1, 1, 0, 0)
        # Initialize with a worldwide forever grid
        self.grid = np.mgrid[-pi:pi:3j, -pi:pi:3j, 0.0:1E10:11j]
        self.init_value_arrays()

    def get(self, position, time):
        self.update()
        t = (time - self.start).total_seconds()
        lat = position[0]
        if self.lon_2pi:
            lon = normalize_angle_2pi(position[1])
        else:
            lon = position[1]
        uv = self.get_uv(lat, lon, t)
        d, s = rectangular_to_polar(uv)
        # Wind direction points opposite to wind speed vector, so add pi
        return normalize_angle_2pi(d + math.pi), s

    def get_uv(self, lat, lon, t):
        # Implement in descendant classes
        return 5.0, 0

    def update(self):
        '''Check and update data'''
        # Implement in descendant classes that rely on e.g. live or localized data
        # and setup grid mesh and u an v arrays
        pass

    def init_value_arrays(self):
        '''Initialize u, v arrays'''
        # Assumes the grid has been setup
        self.u = np.zeros_like(self.grid[0])
        self.v = np.zeros_like(self.grid[0])

    def update_coefficients(self):
        '''
        Routine to update fixed calculation coefficients after values have
        been set or updated
        '''
        # Implement in descendant classes
        pass


def basefuncs_linear(laf, lof, tif, i, j, k):
    return ((1 - (laf + (1 - 2 * laf) * i)) * \
            (1 - (lof + (1 - 2 * lof) * j)) * \
            (1 - (tif + (1 - 2 * tif) * k)), 
            0, 0, 0)

def basefuncs_cubic(laf, lof, tif, i, j, k):
    laf = laf + (1 - 2 * laf) * i
    lof = lof + (1 - 2 * lof) * j
    tif = tif + (1 - 2 * tif) * k
    lab = 1 - 3 * laf**2 + 2 * laf**3
    lob = 1 - 3 * lof**2 + 2 * lof**3
    tib = 1 - 3 * tif**2 + 2 * tif**3
    la = laf * (1 - laf)**2 * (1 - lof) * (1 - tif)
    lo = lof * (1 - lof)**2 * (1 - laf) * (1 - tif)
    ti = tif * (1 - tif)**2 * (1 - laf) * (1 - lof)
    return lab * lob * tib, la, lo, ti

cube_corners = (
    (0, 0, 0),
    (0, 0, 1),
    (0, 1, 0),
    (0, 1, 1),
    (1, 0, 0),
    (1, 0, 1),
    (1, 1, 0),
    (1, 1, 1),)

class InterpolledWind(GriddedWind):
    grid_slice = None
    u_slice = None
    v_slice = None
    du_slice = None
    dv_slice = None

    def __init__(self, *args, **kwargs):
        try:
            # Interpolating function for grid cube
            self.basefuncs = kwargs['basefuncs']
        except KeyError:
            self.basefuncs = basefuncs_linear
        super(InterpolledWind, self).__init__(*args, **kwargs)

    def get_uv(self, lat, lon, t):
        fracs = self.get_fracs(lat, lon, t)
        return self.evaluate(*fracs)

    def calc_gradients(self):
        self.du[:,:,:,:] = np.gradient(self.u)
        self.dv[:,:,:,:] = np.gradient(self.v)

    def get_indices(self, lat, lon, tim):
        lat_i = np.searchsorted(self.grid[0,:,0,0], lat, side='righ') - 1
        lon_i = np.searchsorted(self.grid[1,0,:,0], lon, side='right') - 1
        tim_i = np.searchsorted(self.grid[2,0,0,:], tim, side='right') - 1
        return (lat_i, lon_i, tim_i)

    def update_slices(self, lat, lon, tim):
        la, lo, ti = self.get_indices(lat, lon, tim)
        lap, lop, tip = la + 2, lo + 2, ti + 2 
        self.grid_slice = self.grid[:, la:lap, lo:lop, ti:tip]
        self.u_slice = self.u[la:lap, lo:lop, ti:tip]
        self.du_slice = self.du[:, la:lap, lo:lop, ti:tip]
        self.v_slice = self.v[la:lap, lo:lop, ti:tip]
        self.dv_slice = self.dv[:, la:lap, lo:lop, ti:tip]

    def get_fracs(self, lat, lon, tim):
        if self.grid_slice == None:
            self.update_slices(lat, lon, tim)
            
        steps = self.grid_slice[:, 1, 1, 1] - self.grid_slice[:, 0, 0, 0]
        fracs = ((lat, lon, tim) - self.grid_slice[:,0,0,0]) / steps
        for frac in fracs:
            if frac < 0 or frac > 1:
                self.update_slices(lat, lon, tim)
                return self.get_fracs(lat, lon, tim)
        return fracs 

    def evaluate(self, laf, lof, tif):
        u = 0
        v = 0
        for i, j, k in cube_corners:
            base = self.basefuncs(laf, lof, tif, i, j, k)
            u += self.u_slice[i, j, k] * base[0] + \
                    self.du_slice[0, i, j, k] * base[1] + \
                    self.du_slice[1, i, j, k] * base[2] + \
                    self.du_slice[2, i, j, k] * base[3]
            v += self.v_slice[i, j, k] * base[0] + \
                    self.dv_slice[0, i, j, k] * base[1] + \
                    self.dv_slice[1, i, j, k] * base[2] + \
                    self.dv_slice[2, i, j, k] * base[3]
        return u, v

    def init_value_arrays(self):
        '''Initialize u, du, v, dv arrays'''
        # Assumes the grid has been setup
        GriddedWind.init_value_arrays(self)
        self.du = np.zeros_like(self.grid)
        self.dv = np.zeros_like(self.grid)

    def update_coefficients(self):
        self.calc_gradients()


class SplinedWind(GriddedWind):
    def update_coefficients(self):
        self.calc_splinecoeffs()

    def calc_splinecoeffs(self):
        self.u_coeffs = spline_filter(self.u)
        self.v_coeffs = spline_filter(self.v)
        self.p0 = self.grid[:,0,0,0]
        self.inv_dp = 1. / (self.grid[:,1,1,1] - self.p0)

    def get_uv(self, lat, lon, t):
        # map_coordinates wants columns, so we have transpose and make the
        # coords array two dimensional
        coords = (((lat, lon, t) - self.p0) * self.inv_dp)[:,np.newaxis]
        u = map_coordinates(self.u_coeffs, coords, prefilter=False, mode='nearest')
        v = map_coordinates(self.v_coeffs, coords, prefilter=False, mode='nearest')
        return u, v
