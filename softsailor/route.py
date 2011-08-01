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
from geofun import Position, Line
import kmlbase
import kmldom

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

class Route(object):
    """Object that contains a list of waypoints"""
    def __init__(self, *args, **kwargs):
        super(Route, self).__init__()
        self.__waypoints = []
        if len(args) == 1:
            for wp in args[0]:
                self.__waypoints.append(Waypoint(wp))

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

    def __str__(self):
        result =  ""
        for wp in self:
            deg_wp = rad_to_deg(wp)
            result += "%f, %f %5.0f" % (deg_wp[0], deg_wp[1], wp.range)
            if hasattr(wp, 'comment'):
                result += " " + wp.comment
            result += "\n"
        return result

    def __iadd__(self, value):
        for point in value:
            self.__waypoints.append(Waypoint(point))

    def __add__(self, value):
        result = Route(self)
        result += value
        return result
                      
    @property
    def waypoints(self):
        return self.__waypoints
    @waypoints.setter
    def waypoints(self, value):
        self.__waypoints = []
        for wp in value:
            self.add(wp)

    @property
    def segments(self):
        wp = iter(self.__waypoints)
        wp_from = wp.next()
        while True:
            wp_to = wp.next()
            yield wp_to - wp_from, wp_to
            wp_from = wp_to

    @property
    def lines(self):
        wp = iter(self.__waypoints)
        wp_from = wp.next()
        while True:
            wp_to = wp.next()
            yield Line(wp_from, wp_to)
            wp_from = wp_to

    @property
    def length(self):
        l = 0
        for segment in self.segments:
            l += segment[0].r
        return l

    @vec_func
    def add(self, lat, lon):
        self.__waypoints.append(Waypoint(lat, lon))

    @vec_func
    def insert(self, index, lat, lon):
        self.__waypoints.insert(index, Waypoint(lat, lon))

    def load_from_file(self, filename):
        f = open(filename, "r")
        self.__waypoints = []
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
                self.__waypoints.append(wp)
        f.close()

    def save_to_kml(self, filename):
        filedir, file = os.path.split(filename)
        filebase, fileext = os.path.splitext(file)

        kml, doc = create_kml_document('Route: ' + filebase)

        factory = kmldom.KmlFactory_GetFactory()
        
        waypoints = factory.CreateFolder()
        waypoints.set_name('Waypoints')
        for i, wp in enumerate(self.waypoints):
            waypoint = create_point_placemark('Waypoint ' + str(i), \
                    rad_to_deg(wp[0]), rad_to_deg(wp[1]))
            waypoint.set_description(wp.comment)
            waypoint.set_styleurl('#default')
            waypoints.add_feature(waypoint)

        lines = factory.CreateFolder()
        lines.set_name('Track')
        for i, ln in enumerate(self.lines):
            vec = ln.v
            p1 = list(ln.p1)
            p2 = list(ln.p2)
            ln = (rad_to_deg(p1), rad_to_deg(p2))
            line = create_line_placemark('Track ' + str(i), ln)
            description = u'Bearing: ' + u"%.2f\u00B0" % rad_to_deg(vec.a) \
                    + u'  Length: ' + u"%.2f nm" % (vec.r / 1852)
            line.set_description(description.encode("utf-8"))
            lines.add_feature(line)

        description = 'UTC: ' + str(datetime.datetime.utcnow())
        description += ' Length: ' + str(int(self.length / 1852)) + ' nm'
        doc.set_description(description)
        doc.add_feature(waypoints)
        doc.add_feature(lines)
        
        save_kml_document(kml, filename)

