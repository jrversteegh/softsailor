"""
Classes module

Contains utility classes
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

import math
import numpy as np
from datetime import datetime, timedelta

import kmlbase
import kmldom

from geofun import Line, Position

from softsailor.utils import *

class Object(object):
    def __init__(self, *args, **kwargs):
        super(Object, self).__init__()

class Logable(Object):
    '''Base class for data loggers'''
    def __init__(self, *args, **kwargs):
        super(Logable, self).__init__(*args, **kwargs)
        self._log_data = []
        self.fmtrs = []

    def log(self, log_str, *record_fields):
        self.add(datetime.utcnow(), log_str, *record_fields)

    def add(self, date_time, log_str, *record_fields):
        self._log_data.append((date_time, log_str, record_fields))
        while len(self.fmtrs) < len(record_fields):
            self.fmtrs.append(str)

    def save_log(self, filename):
        f = open(filename, "w")
        for record in self._log_data:
            f.write(record[0].strftime(time_format) + ", " + record[1])
            for i, field in enumerate(record[2]):
                f.write(", " + self.fmtrs[i](field))
            f.write("\n")
        f.close()

    def print_log(self, lines=0):
        for record in self._log_data[-lines:]:
            fields = []
            for i, field in enumerate(record[2]):
                fields.append(self.fmtrs[i](field))
            print record[0].strftime(time_format), record[1], fields

    @property
    def records(self):
        return self._log_data

    @property
    def data(self):
        for rec in self._log_data:
            yield rec[2]


class Path(list):
    def __init__(self, *args, **kwargs):
        # Don't pass anything to list constructor
        super(Path, self).__init__()
        if len(args) > 0:
            try:
                it = iter(args[0])
            except TypeError:
                it = args
            for i in it:
                self.add(i)

    def add(self, item):
        self.append(item)

    @property
    def length(self):
        l = 0
        for segment in self.segments:
            l += segment.v.r
        return l

    @property
    def segments(self):
        prev_p = None
        for p in self:
            if prev_p is not None:
                yield Line(prev_p, p)
            prev_p = p

    def similar(self, other):
        if other is None:
            return False
        if len(self) != len(other):
            return False
        for p1, p2 in zip(self, other):
            l = Line(p1, p2)
            # When points are more that 10m apart, consider them different
            if l.v.r > 20:
                return False
        return True

    def __eq__(self, other):
        if other is None:
            return False
        if len(self) != len(other):
            return False
        for p1, p2 in zip(self, other):
            if p1 != p2:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.length > other.length

    def __lt__(self, other):
        return self.length < other.length
    
    def __ge__(self, other):
        return self.length >= other.length

    def __le__(self, other):
        return self.length <= other.length

    def __str__(self):
        result =  ""
        for p in self:
            deg_p = rad_to_deg(p)
            result += "%f, %f %5.0f" % (deg_p[0], deg_p[1], p.range)
            if hasattr(p, 'comment'):
                result += " " + p.comment
            result += "\n"
        return result

    def get_type_name(self):
        return self.__class__.__name__

    def save_to_kml(self, filename):
        filedir, file = os.path.split(filename)
        filebase, fileext = os.path.splitext(file)

        kml, doc = create_kml_document(self.get_type_name() + ': ' + filebase)

        factory = kmldom.KmlFactory_GetFactory()
        
        points = factory.CreateFolder()
        points.set_name('Points')
        for i, p in enumerate(self):
            point = create_point_placemark('Point ' + str(i), \
                    rad_to_deg(p[0]), rad_to_deg(p[1]))
            try:
                point.set_description(p.comment)
            except AttributeError:
                pass
            point.set_styleurl('#default')
            points.add_feature(point)

        lines = factory.CreateFolder()
        lines.set_name('Track')
        for i, ln in enumerate(self.segments):
            vec = ln.v
            p1 = list(ln.p1)
            p2 = list(ln.p2)
            ln = (rad_to_deg(p1), rad_to_deg(p2))
            line = create_line_placemark('Segment ' + str(i), ln)
            description = 'Vector: ' + vec_to_str(vec) 
            line.set_description(description)
            lines.add_feature(line)

        description = 'UTC: ' + str(datetime.utcnow())
        description += ' Length: ' + str(int(self.length / 1852)) + ' nm'
        doc.set_description(description)
        doc.add_feature(points)
        doc.add_feature(lines)
        
        save_kml_document(kml, filename)
