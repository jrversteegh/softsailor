"""
Route module

Contains objects for dealing with route information
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

import os
import datetime
from utils import *
from geofun import Position, Line, floats_equal
import kmlbase
import kmldom

from softsailor.classes import Path

class Waypoint(Position):
    range = 42.0  # Default range for waypoint: 42m
    comment = ''
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            lat, lon = args[0]
        else:
            lat, lon = args[:2]
        super(Waypoint, self).__init__(lat, lon)
        if len(args) > 0:
            # Copy constructor
            try:
                self.range = args[0].range
                self.comment = args[0].comment
            except AttributeError:
                pass
        if len(args) > 2:
            self.range = float(args[2])
        if len(args) > 3:
            self.comment = str(args[3])

    def is_reached(self, position):
        """Return whether the waypoint has been reached by object
           with 'position'
        """
        v = self - position
        return (v[1] < self.range)

class Route(Path):
    """Object that contains a list of waypoints"""
    def __init__(self, *args, **kwargs):
        super(Route, self).__init__(*args, **kwargs)

    def __setitem__(self, index, value):
        while len(self) < index:
            self.append(Waypoint(0, 0))
        if index < len(self):
            super(Route, self).__setitem__(index, Waypoint(value))
        else:
            self.append(Waypoint(value))


    def __iadd__(self, value):
        # Ignore the first point
        for point in value[1:]:
            self.append(Waypoint(point))
        return self

    def __add__(self, value):
        result = Route(self)
        result += value
        return result
                      
    @property
    def waypoints(self):
        return self
    @waypoints.setter
    def waypoints(self, value):
        del self[:]
        for wp in value:
            self.add(wp)

    @vec_func
    def add(self, lat, lon):
        self.append(Waypoint(lat, lon))

    @vec_func
    def insert(self, index, lat, lon):
        self.insert(index, Waypoint(lat, lon))

    def load_from_file(self, filename):
        f = open(filename, "r")
        del self[:]
        for line in f:
            # Split off comments
            line, sep, comment = line.partition("#")
            line = line.strip()
            if line != "": 
                vals = line.split()
                la, lo = deg_to_rad(vals[:2])
                if len(vals) > 2:
                    ra = float(vals[2])
                else:
                    ra = Waypoint.range
                wp = Waypoint(la, lo, ra)
                wp.comment = comment.strip()
                self.append(wp)
        f.close()

    def save_to_file(self, filename):
        f = open(filename, "w")
        for wp in self:
            lat, lon = rad_to_deg(wp.lat, wp.lon)
            line = '%f %f %f # %s\n' % (lat, lon, wp.range, wp.comment)
            f.write(line)
        f.close()


