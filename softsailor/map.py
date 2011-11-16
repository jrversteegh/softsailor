"""
Map module

Contains an interface for a map provider 
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from heapq import *
import functools

from datetime import datetime
from geofun import Line, Position
from route import Route
from utils import *
import kmlbase
import kmldom

class Path(list):
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

    def __eq__(self, other):
        return self.length == other.length

    def __ne__(self, other):
        return self.length != other.length

    def __gt__(self, other):
        return self.length > other.length

    def __lt__(self, other):
        return self.length < other.length
    
    def __ge__(self, other):
        return self.length >= other.length

    def __le__(self, other):
        return self.length <= other.length

    def save_to_kml(self, filename):
        filedir, file = os.path.split(filename)
        filebase, fileext = os.path.splitext(file)

        kml, doc = create_kml_document('Path: ' + filebase)

        factory = kmldom.KmlFactory_GetFactory()
        
        points = factory.CreateFolder()
        points.set_name('Points')
        for i, p in enumerate(self):
            point = create_point_placemark('Point ' + str(i), \
                    rad_to_deg(p[0]), rad_to_deg(p[1]))
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

class Map(object):
    def hit(self, line):
        """Returns whether the segment crosses a land boundary"""
        return False

    def intersect(self, line):
        """Returns segment and intersection point or None, None when not hitting"""
        return [None, None]

    def route_around(self, line):
        """Returns convex paths around land hit"""    
        return [Path([line.p1, line.p2])]

    def find_paths(self, line, max_paths=32):
        """Returns a heap of lines around land given the input line"""

        def clean_path(path):
            """Try and remove points and still not hit land"""
            prev_len = len(path)
            for i in xrange(len(path) - 2, 0, -1):
                l = Line(path[i - 1], path[i + 1])
                if not self.hit(l):
                    path.pop(i)

            return len(path) != prev_len
        
        result = []
        paths = []
        heappush(paths, Path([line.p1, line.p2]))

        it_count = -1
        while len(result) < max_paths and len(paths) > 0:
            path = heappop(paths)
            it_count += 1
            path.save_to_kml('path_%.4d.kml' % it_count)

            path_clear = True
            for i, segment in enumerate(path.segments):
                if not self.hit(segment):
                    continue
                path_clear = False
                detours = self.route_around(segment)
                new_path = None
                # There can be 2 detours
                right = 0
                for detour in detours:
                    detour_path = Path(detour)
                    detour_path.save_to_kml('path_%.4ds%d.kml' % (it_count, right))
                    right += 1
                
                    if new_path is not None:
                        path = new_path
                    # create a copy of the original in case there are indeed two detours    
                    new_path = Path(path)
                    # Fit the detour into the existing path
                    path[i:i+2] = detour
                    # And push it back onto the path heap
                    heappush(paths, path)
                break
            # When a path was walked without hitting anything, we got a winner. 
            # Add it to the result
            if path_clear:
                heappush(result, path)

        for path in result:
            while clean_path(path):
                pass
        result.sort()
        return result

