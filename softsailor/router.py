"""
Router module

Contains an object that determines which way to head in order to follow a route
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

import math
from classes import *
from boat import *
from route import *

class Router(object):
    __active_index = 0
    """Object that determines which way to head to follow a route"""
    def __init__(self, *args, **kwargs):
        super(Router, self).__init__()
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
                br = sg[1].get_bearing_from(self.boat.position)
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
            return PolarVector(0.0, 0.0)
        segment, waypoint = self.get_active_segment()
        bearing = waypoint.get_bearing_from(self.boat.position)
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
            return wp.get_bearing_from(self.route[self.__active_index - 1]), wp
        else:
            return PolarVector(0, 0), Waypoint(0, 0)

    def get_cross_track(self):
        sg = self.get_active_segment()
        tr = sg[0]
        br = self.get_bearing()
        return br[1] * math.sin(tr[0] - br[0])

