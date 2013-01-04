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
from softsailor.wind import *


class SolWind(GriddedWind):
    def __init__(self, weather, base_funcs = base_funcs_linear):
        self.weather = weather
        self._last_verification = datetime.utcnow()
        self.update_grid()
        self.base_funcs = base_funcs

    def get(self, position, time):
        self.update_weather()
        reltime = (time - self.weather.start_datetime).total_seconds()
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

    def update(self):
        self.update_weather()


    def update_weather(self):
        now = datetime.utcnow() 
        if now - self._last_verification > timedelta(minutes = 2):
            if self.weather.update_when_required():
                self.update_grid()
            self._last_verification = now


    def update_grid(self):
        self.grid_slice = None
        weather = self.weather
        self.lon_2pi = weather.lon_max >= pi
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

        self.init_values_arrays()

        for i, frame in enumerate(weather.frames):
            a = np.array(frame)
            u = a[:,:,0]
            v = a[:,:,1]
            self.u[:,:,i] = u
            self.v[:,:,i] = v
        
        self.calc_gradients()

