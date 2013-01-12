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


class SolWind(InterpolledWind):
    def __init__(self, *args, **kwargs):
        self.weather = args[0]
        self._last_verification = datetime(1970, 1, 1, 0, 0)
        super(SolWind, self).__init__(*args, **kwargs)

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
        self.start = weather.start_datetime
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

        self.init_value_arrays()

        for i, frame in enumerate(weather.frames):
            a = np.array(frame)
            u = a[:,:,0]
            v = a[:,:,1]
            self.u[:,:,i] = u
            self.v[:,:,i] = v
        
        self.update_coefficients()

