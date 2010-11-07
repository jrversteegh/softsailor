from utils import *
from classes import *

class Waypoint(Position):
    range = 100  # Default range for waypoint: 100m
    def __init__(self, *args, **kwargs):
        super(Waypoint, self).__init__(*args, **kwargs)
        if len(args) > 2:
            self.range = args[2]
        elif len(args) > 1:
            try:
                it = iter(args[0])
                self.range = args[1]
            except TypeError:
                pass

class Route(object):
    """Object that contains a list of waypoints"""
    def __init__(self, *args, **kwargs):
        super(Route, self).__init__()
        self.__waypoints = []
        if len(args) > 0:
            for wp in args[0]:
                self.add(wp)

    def __iter__(self):
        return iter(self.__waypoints)
    def __getitem__(self, index):
        return self.__waypoints[index]
    def __setitem__(self, index, value):
        while len(self.__waypoints) < index:
            self.__waypoints.append(Waypoint(0, 0))
        if index < len(self.__waypoints):
            self.__waypoints[index] = Waypoint(value)
        else:
            self.__waypoints.append(Waypoint(value))
    def __len__(self):
        return len(self.__waypoints)
                      
    @property
    def waypoints(self):
        return self.__waypoints
    @waypoints.setter
    def waypoints(self, value):
        self.__waypoints = []
        for wp in value:
            self.__waypoints.append(Waypoint(wp))

    @property
    def segments(self):
        wp = iter(self.__waypoints)
        wp_from = wp.next()
        while True:
            wp_to = wp.next()
            yield wp_to.bearing(wp_from), wp_to
            wp_from = wp_to

    @property
    def length(self):
        l = 0
        for segment in self.segments:
            l += segment[0].r
        return l

    @vec_meth
    def add(self, waypoint):
        self.__waypoints.append(Waypoint(waypoint))

    def load_from_file(self, filename):
        f = open(filename, "r")
        fdata = f.read()
        flines = fdata.splitlines()
        self.__waypoints = []
        for line in flines:
            if line != "": 
                vals = line.split(" ")
                la, lo = deg_to_rad(vals[:2])
                if len(vals) > 2:
                    ra = vals[2]
                else:
                    ra = Waypoint.range
                self.__waypoints.append(Waypoint(la, lo, ra))
        f.close()

