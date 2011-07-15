"""
Wind module

Contains an wind data provider interface
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

import math

class Wind(object):
    def get(self, position, time = None):
        """Get wind direction at position an time"""
        # Default is a 1m/s southerly wind
        return math.pi, 1.0
