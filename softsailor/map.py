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

from geofun import Line, Position
from route import Route

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

        while len(result) < max_paths and len(paths) > 0:
            path = heappop(paths)
            path_clear = True
            for i, segment in enumerate(path.segments):
                if not self.hit(segment):
                    continue
                path_clear = False
                detours = self.route_around(segment)
                new_path = None
                for detour in detours:
                    if new_path is not None:
                        path = new_path
                    new_path = Path(path)
                    path[i:i+2] = detour
                    heappush(paths, path)
                break
            if path_clear:
                heappush(result, path)

        for path in result:
            while clean_path(path):
                pass
        result.sort()
        return result

