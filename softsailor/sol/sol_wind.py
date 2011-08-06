"""
Sol wind module

Contains wind implementation for sol
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from datetime import datetime, timedelta
import math
import numpy as np

from softsailor.utils import *

def base_funcs_linear(laf, lof, tif, i, j, k):
    return ((1 - (laf + (1 - 2 * laf) * i)) * \
            (1 - (lof + (1 - 2 * lof) * j)) * \
            (1 - (tif + (1 - 2 * tif) * k)), 
            0, 0, 0)

def base_funcs_cubic(laf, lof, tif, i, j, k):
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

_corners = (
    (0, 0, 0),
    (0, 0, 1),
    (0, 1, 0),
    (0, 1, 1),
    (1, 0, 0),
    (1, 0, 1),
    (1, 1, 0),
    (1, 1, 1),)

class SolWind(object):
    def __init__(self, weather, base_funcs = base_funcs_linear):
        self.weather = weather
        self._last_verification = datetime.utcnow()
        self.update_grid()
        self.base_funcs = base_funcs

    def get(self, position, time):
        self.update_weather()
        reltime = timedelta_to_seconds(time - self.weather.start_datetime)
        lat = position[0]
        if self.weather.lon_max >= math.pi:
            lon = normalize_angle_2pi(position[1])
        else:
            lon = position[1]
        fracs = self.get_fracs(lat, lon, reltime)
        uv = self.evaluate(*fracs)
        d, s = rectangular_to_polar(uv)
        # Wind direction points opposite to wind speed vector, so add pi
        return normalize_angle_2pi(d + math.pi), s

    def evaluate(self, laf, lof, tif):
        u = 0
        v = 0
        for i, j, k in _corners:
            base = self.base_funcs(laf, lof, tif, i, j, k)
            u += self.u_slice[i, j, k] * base[0] + \
                    self.du_slice[0, i, j, k] * base[1] + \
                    self.du_slice[1, i, j, k] * base[2] + \
                    self.du_slice[2, i, j, k] * base[3]
            v += self.v_slice[i, j, k] * base[0] + \
                    self.dv_slice[0, i, j, k] * base[1] + \
                    self.dv_slice[1, i, j, k] * base[2] + \
                    self.dv_slice[2, i, j, k] * base[3]
        return u, v

    def update_weather(self):
        now = datetime.utcnow() 
        if now - self._last_verification > timedelta(minutes = 2):
            if self.weather.update_when_required():
                self.update_grid()
            self._last_verification = now

    def get_indices(self, lat, lon, reltime):
        lat_i = int((lat - self.weather.lat_min) / self.weather.lat_step)
        lon_i = int((lon - self.weather.lon_min) / self.weather.lon_step)
        for i in range(self.weather.reltime_n):
            if reltime >= self.weather.reltimes[i]:
                time_i = i
        return (lat_i, lon_i, time_i)

    def update_slices(self, lat, lon, reltime):
        la, lo, ti = self.get_indices(lat, lon, reltime)
        lap, lop, tip = la + 2, lo + 2, ti + 2 
        self.grid_slice = self.grid[:, la:lap, lo:lop, ti:tip]
        self.u_slice = self.u[la:lap, lo:lop, ti:tip]
        self.du_slice = self.du[:, la:lap, lo:lop, ti:tip]
        self.v_slice = self.v[la:lap, lo:lop, ti:tip]
        self.dv_slice = self.dv[:, la:lap, lo:lop, ti:tip]

    def get_fracs(self, lat, lon, reltime):
        if self.grid_slice == None:
            self.update_slices(lat, lon, reltime)
            
        lat_frac = (lat - self.grid_slice[0,0,0,0]) / self.weather.lat_step
        lon_frac = (lon - self.grid_slice[1,0,0,0]) / self.weather.lon_step
        time_frac = (reltime - self.grid_slice[2,0,0,0]) / \
               (self.grid_slice[2,0,0,1] - self.grid_slice[2,0,0,0])

        if lat_frac < 0 or lat_frac > 1 or \
                lon_frac < 0 or lon_frac > 1 or \
                time_frac < 0 or time_frac > 1:
            self.update_slices(lat, lon, reltime)
            return self.get_fracs(lat, lon, reltime)
        else:
            return lat_frac, lon_frac, time_frac

    def update_grid(self):
        self.grid_slice = None
        weather = self.weather
        self.grid = np.mgrid[weather.lat_min: weather.lat_max: weather.lat_n * 1j,
                             weather.lon_min: weather.lon_max: weather.lon_n * 1j,
                             0: weather.reltime_n]
        grid = self.grid
        # Fix up relative time values
        for i,lat in enumerate(grid[2,:,0,0]):
            for j, lon in enumerate(grid[2,i,:,0]):
                for k, tim in enumerate(grid[2,i,j,:]):
                    assert(k == tim)
                    grid[2,i,j,k] = weather.reltimes[k]

        self.u = np.zeros_like(grid[0])
        self.du = np.zeros_like(grid)

        self.v = np.zeros_like(grid[1])
        self.dv = np.zeros_like(grid)

        for i, frame in enumerate(weather.frames):
            a = np.array(frame)
            u = a[:,:,0]
            v = a[:,:,1]
            self.u[:,:,i] = u
            self.v[:,:,i] = v
        
        self.du[:,:,:,:] = np.gradient(self.u)
        self.dv[:,:,:,:] = np.gradient(self.v)

