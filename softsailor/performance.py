import math

from classes import PolarData

class Performance:
    def __init__(self, polar_data):
        self.polar_data = polar_data

    def get(self, relative_wind):
        return 0

    def optimal_angles(self, wind_speed):
        return (0, math.pi)
