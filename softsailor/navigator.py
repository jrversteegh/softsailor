"""
Navigator module

Contains an object that determines which way to head in order to follow a route
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

import math
from utils import *
from classes import *
from geofun import Vector
from boat import *
from route import *

class Navigator(object):
    __active_index = 0
    """Object that determines which way to head to follow a route"""
    def __init__(self, *args, **kwargs):
        super(Navigator, self).__init__()
        if len(args) > 0:
            self.route = args[0]
            self.boat = args[1]
        else:
            self.route = kwargs['route']
            self.boat = kwargs['boat']
        self.initialize()

    def initialize(self):
        """Select the waypoint to sail to initially"""
        segments = self.route.segments
        while True:
            self.__next()
            try:
                sg = segments.next()
                tr = sg[0]
                br = sg[1] - self.boat.position
                # We're looking for a waypoint that has a bearing
                # along the track
                cs = math.cos(tr[0] - br[0]) 
                if cs > 0.7:
                    break
            except StopIteration:
                break

    def __next(self):
        self.__active_index += 1

    @property
    def active_index(self):
        return self.__active_index

    @property
    def active_waypoint(self):
        if self.__active_index < len(self.route):
            return self.route[self.__active_index]
        else:
            return Waypoint(0.0, 0.0)

    @property
    def is_complete(self):
        return self.__active_index >= len(self.route)

    def get_bearing(self):
        if self.is_complete:
            return Vector(0.0, 0.0)
        segment, waypoint = self.get_active_segment()
        bearing = waypoint - self.boat.position
        # If if waypoint has been reached or has been 'overshot'...
        if waypoint.is_reached(self.boat.position) \
                or math.cos(segment[0] - bearing[0]) < 0.0:
            # ... go to the next waypoint
            self.__next()
            return self.get_bearing()
        return bearing

    def get_active_segment(self):
        if self.active_index > 0 \
                and self.active_index < len(self.route):
            wp = self.route[self.__active_index]
            return wp - self.route[self.__active_index - 1], wp
        else:
            return Vector(0, 0), Waypoint(0, 0)

    def get_cross_track(self):
        """Returns distance to track. Not accurate for larget distances"""
        sg = self.get_active_segment()
        tr = sg[0]
        br = self.get_bearing()
        return br[1] * math.sin(tr[0] - br[0])

    def to_track(self):
        """Return vector to track"""
        sg = self.get_active_segment()
        tr = sg[0]
        tr.r = 1
        br = self.get_bearing()
        cs = -br.r * math.cos(tr.a - br.a)
        # Position projected on track line
        pr = sg[1] + tr * cs
        return pr - self.boat.position

    def get_optimal_angles(self, wind_speed):
        opt_angles = self.boat.performance.get_optimal_angles(wind_speed)
        br = self.get_bearing()
        # Allow a little space when close to a waypoint, to avoid stupid 
        # gybes or tacks when the waypoint is just outside the optimal angle range
        if br.r < 2000:
            # Maximum of 0.1 rad at the waypoint
            allowance = (2000 - br.r) * 0.00005
            # A little less allowance upwind
            opt_angles[0] -= allowance * 0.6
            # ..than downwind
            opt_angles[1] += allowance
            if opt_angles[0] < 0:
                opt_angles[0] = 0
            if opt_angles[1] > pi:
                opt_angles[1] = pi

        # TODO add optimal angle adjustment from route here
            
        return opt_angles
        


