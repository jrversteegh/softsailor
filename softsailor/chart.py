"""
Chart module

Contains an interface for a chart provider 
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
import kmlbase
import kmldom

from softsailor.route import Route
from softsailor.utils import *
from softsailor.classes import Path

class Chart(object):
    def hit(self, line):
        """Returns whether the segment crosses a land boundary"""
        return False

    def intersect(self, line):
        """Returns segment and intersection point or None, None when not hitting"""
        return [None, None]

    def route_around(self, line, distance_hint=1E8):
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
        path = Path((line.p1, line.p2))
        path.clear_upto = 0
        heappush(paths, path)

        c = 0
        last_path = None
        while len(result) < max_paths and len(paths) > 0:
            best = 1E8
            c += 1
            path = heappop(paths)
            #path.save_to_kml('path_%.4d.kml' % c)
            # Don't consider paths that are longer than twice the best result
            if path.length > 2 * best:
                continue

            if path == last_path:
                print "Path duplicate"
                continue
            last_path = path

            # We'll have to stop at some point, when we have a valid result at
            # least
            if len(result) > 0 and c > 512:
                break

            path_clear = True
            for i, segment in enumerate(path.segments):
                if i < path.clear_upto:
                    continue
                if not self.hit(segment):
                    path.clear_upto = i
                    continue
                path_clear = False
                detours = self.route_around(segment, best)
                for detour in detours:
                    new_path = Path(path)
                    new_path.clear_upto = path.clear_upto
                    # Fit the detour into the existing path
                    new_path[i:i+2] = detour
                    # And push it back onto the path heap
                    heappush(paths, new_path)
                break
            # When a path was walked without hitting anything, we got a winner. 
            # Add it to the result
            if path_clear:
                while clean_path(path):
                    pass
                try:
                    # Avoid duplicates
                    result.index(path)
                except ValueError:
                    if path.length < best:
                        best = path.length 
                    result.append(path)

        result.sort()
        return result

