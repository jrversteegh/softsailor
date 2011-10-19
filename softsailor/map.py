"""
Map module

Contains an interface for a map provider 
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

import heapq

from geofun import Line, Position
from route import Route

class Map(object):
    def hit(self, line):
        """Returns whether the segment crosses a land boundary"""
        return False

    def intersect(self, line):
        """Returns segment and intersection point or None, None when not hitting"""
        return [None, None]

    def outer_points(self, line):
        """Returns the first pair of convex parts around land hit"""    
        return [[line.p1, line.p2], None]

    def find_paths(self, line, max_paths=32):
        """Returns a heap of lines around land given the input line"""
        def scan_sub_outers():
            """
            Scan outers for hitting land and splitting the outer
            around it in both directions when it does
            """
            modified = False
            for j in range(len(outers)):
                outer = outers[j]
                if outer is None:
                    raise Exception('Expected at least one path around land')
                for i in xrange(1, len(outer)):
                    p1 = outer[i - 1]
                    p2 = outer[i]
                    l = Line(p1, p2)
                    sub_outers = self._outer_points_first(l)
                    try:
                        sub_outers.remove(None)
                    except ValueError:
                        pass
                    outer_copy = None
                    # Sort on number of points, sorting on actual track length
                    # would be slightly better?
                    try:
                        sub_outers.sort(key=lambda l: len(l))
                    except TypeError:
                        # sort will raise if there is a None in the list still
                        raise Exception(
                            'Expected at least one path around land in sub search')
                    for sub_outer in sub_outers:
                        sub_outer = sub_outer[1:-1]
                        if sub_outer:
                            if outer_copy:
                                outer_copy[i:i] = sub_outer
                                outers.append(outer_copy)
                            else:
                                outer_copy = outer[:]
                                outer[i:i] = sub_outer
                            modified = True
            return modified

        def clean_paths():
            """Try and remove points and still not hit land"""
            modified = False
            for outer in outers:
                for i in xrange(len(outer) - 2, 0, -1):
                    l = Line(outer[i - 1], outer[i + 1])
                    if not self.hit(l):
                        outer.pop(i)

                        modified = True
            return modified


        
        clear_paths = []
        paths = [line]
        outers = self._outer_points_first(line)
        #print "Outers 1:", len(outers)
        try:
            outers.remove(None)
        except ValueError:
            pass
        scans = 0
        while scans < 32 and scan_sub_outers():
            while clean_outers():
                pass
            scans += 1

        return outers

