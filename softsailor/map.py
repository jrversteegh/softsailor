"""
Map module

Contains an interface for a map provider 
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

class Map(object):
    def hit(self, line):
        """Returns whether the segment crosses a land boundary"""
        return False

    def outer(self, line):
        """Returns tuple of outermost points of land hit"""    
        return tuple()
