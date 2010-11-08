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
        return 3 * math.sqrt(relative_wind[1]) * abs(math.sin(relative_wind[0] * 1.2))

    def get_optimal_angles(self, wind_speed):
        return (0.25 * math.pi, 0.75 * math.pi)
