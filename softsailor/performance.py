"""
Performance module

Contains a provider interface for boat performance
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

import math


class Performance(object):
    def __init__(self, *args, **kwargs):
        super(Performance, self).__init__()
        if len(args) > 0:
            self.polars = args[0]
        else:
            try:
                self.polars = kwargs['polars']
            except KeyError:
                pass

    def get(self, relative_wind):
        return 0, 3 * math.sqrt(relative_wind[1]) \
                * abs(math.sin(relative_wind[0] * 1.2)) 

    def get_speed(self, relative_wind):
        return self.get(relative_wind)[1]

    def get_drift(self, relative_wind):
        return self.get(relative_wind[0])

    def get_optimal_angles(self, wind_speed):
        return (0.25 * math.pi, 0.75 * math.pi)
