from math import cos
from classes import *
from boat import *
from route import *

class Router(object):
    __active_index = 0
    """Object that determines which way to steer to follow a route"""
    def __init__(self, *args, **kwargs):
        super(Router, self).__init__()
        if len(args) > 1:
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
                br = sg[1].bearing(self.boat.position)
                # We're looking for a waypoint that has a bearing
                # along the track
                if cos(tr[0] - br[0]) > 0.7:
                    break
            except StopIteration:
                break

    def __next(self):
        self.__active_index += 1

    def bearing(self):
        if self.is_complete:
            return PolarVector(0.0, 0.0)
        result = self.active_waypoint.bearing(self.boat.position)
        if result.r < self.active_waypoint.range:
            self.__next()
            return self.bearing()
        return result

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


