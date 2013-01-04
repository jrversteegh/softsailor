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
from classes import Object

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

class Wind(Object):
    '''Basic prototype for wind object'''
    def get(self, position, time = None):
        """Get wind direction at position an time"""
        # Default is a 5m/s southerly wind
        return pi, 5.0

class GriddedWind(Wind):
    '''Base class for 3D grid based wind objects'''
    basefuncs = basefuncs_linear
    grid_slice = None
    u_slice = None
    v_slice = None
    du_slice = None
    dv_slice = None
    lon_2pi = False  # Indicates whether longitude grid is [0, 2pi> instead
                     # of [-pi, pi>

    def __init__(self, *args, **kwargs):
        super(GriddedWind, Self).__init__(*args, **kwargs)
        try:
            # Interpolating function for grid cube
            self.basefuncs = kwargs['basefuncs']
        except KeyError:
            pass
        # min,max,step,stride for lat,lon,t
        self.ranges[[0.0 for i in range(4)] for j in range(3)]
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
        fracs = self.get_fracs(lat, lon, t)
        uv = self.evaluate(*fracs)
        d, s = rectangular_to_polar(uv)
        # Wind direction points opposite to wind speed vector, so add pi
        return normalize_angle_2pi(d + math.pi), s

    def update(self):
        '''Check and update data'''
        # Implement in descendant classes that rely on e.g. live or localized data

    def get_indices(self, lat, lon, tim):
        lat_i = np.searchsorted(self.grid[0,:,0,0], lat)
        lon_i = np.searchsorted(self.grid[1,0,:,0], lon)
        tim_i = np.searchsorted(self.grid[2,0,0,:], tim)
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
            
        lat_step = self.grid_slice[0, 1, 0, 0] - self.grid_slice[0, 0, 0, 0]
        lon_step = self.grid_slice[1, 0, 1, 0] - self.grid_slice[1, 0, 0, 0]
        tim_step = self.grid_slice[2, 0, 0, 1] - self.grid_slice[2, 0, 0, 0]
        lat_frac = (lat - self.grid_slice[0,0,0,0]) / lat_step
        lon_frac = (lon - self.grid_slice[1,0,0,0]) / lon_step
        tim_frac = (tim - self.grid_slice[2,0,0,0]) / tim_step

        if lat_frac < 0 or lat_frac > 1 or \
                lon_frac < 0 or lon_frac > 1 or \
                tim_frac < 0 or tim_frac > 1:
            self.update_slices(lat, lon, tim)
            return self.get_fracs(lat, lon, tim)
        else:
            return lat_frac, lon_frac, tim_frac

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
        self.u = np.zeros_like(grid[0])
        self.du = np.zeros_like(grid)

        self.v = np.zeros_like(grid[0])
        self.dv = np.zeros_like(grid)

    def calc_gradients(self):
        self.du[:,:,:,:] = np.gradient(self.u)
        self.dv[:,:,:,:] = np.gradient(self.v)


