from math import cos
from classes import *
from boat import *
from route import *

class Router(object):
    __active_index = 0
    """Object that determines which way to steer to follow a route"""
    def __init__(self, *args, **kwargs):
        super(Router, self).__init__()
        if len(args) > 0:
            self.route = args[0]
            self.boat = args[1]
        else:
            self.route = kwargs['route']
            self.boat = kwargs['boat']
        self.__initiate()

    def __initiate(self):
        # Select the waypoint to sail to initially
        segments = self.route.segments
        while True:
            self.__next()
            try:
                sg = segments.next()
                tr = sg[0]
                br = sg[1].get_bearing_from(self.boat.position)
                # We're looking for a waypoint that has a bearing
                # along the track
                if cos(tr[0] - br[0]) > 0.7:
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
        result = self.active_waypoint.get_bearing_from(self.boat.position)
        if result.r < self.active_waypoint.range:
            self.__next()
            return self.get_bearing()
        return result

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

