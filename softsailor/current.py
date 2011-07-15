"""
Current module

Contains an interface for a current data provider
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

class Current(object):
    def get(self, position, time):
        return 0.0, 0.0
