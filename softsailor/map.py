"""
Map module

Contains an interface for a map provider 
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from geofun import Line, Position

class Map(object):
    def hit(self, line):
        """Returns whether the segment crosses a land boundary"""
        return False

    def outer_points_first(self, line):
        """Returns the two lines arount the first land hit"""    
        return ((line.p1, line.p2), (line.p1, line.p2))

    def outer_points(self, line):
        """Returns a list of lines around land"""
        outers = self.outer_points_first(line)
        try:
            outers.remove(None)
        except ValueError:
            pass
        modified = True
        while  modified:
            modified = False
            for outer in outers:
                for i in xrange(1, len(outer)):
                    p1 = outer[i - 1]
                    p2 = outer[i]
                    l = Line(p1, p2)
                    sub_outers = self.outer_points_first(l)
                    try:
                        sub_outers.remove(None)
                    except ValueError:
                        pass
                    outer_copy = None
                    for sub_outer in sub_outers:
                        sub_outer = sub_outer[1:-1]
                        if sub_outer:
                            modified = True
                            if outer_copy:
                                outer_copy[i:i] = sub_outer
                                outers.append(outer_copy)
                            else:
                                outer_copy = outer[:]
                                outer[i:i] = sub_outer

        return outers

