import math

from classes import PolarData

class Performance(object):
    def __init__(self, *args, **kwargs):
        #super(Performance, self).__init__(*args, **kwargs)
        if len(args) > 0:
            self.polar_data = args[0]
        else:
            self.polar_data = kwargs['polar_data']

    def get(self, relative_wind):
        return 0.0

    def optimal_angles(self, wind_speed):
        return (0.0, math.pi)
