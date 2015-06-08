import unittest
import testing_helper
from datetime import datetime, timedelta

from softsailor.utils import *

from softsailor.vr.vr_wind import *
from softsailor.vr.vr_weather import *
from softsailor.vr.vr_settings import *

class FakeWeather:
    lat_min = 0
    lat_max = 0.75
    lat_n = 4
    lon_min = -0.1
    lon_max = 0.3
    lon_n = 5

    def __init__(self):
        self.frames = []
        self.datetimes = []
        self.reltimes = []

        self.lat_range = self.lat_max - self.lat_min
        self.lat_step = self.lat_range / (self.lat_n - 1)
        self.lon_range = self.lon_max - self.lon_min
        self.lon_step = self.lon_range / (self.lon_n - 1)

        now = datetime.utcnow()
        self.start_datetime = now - timedelta(hours = 1)
        self.datetimes.append(now - timedelta(hours = 1))
        self.datetimes.append(now + timedelta(hours = 5))
        self.datetimes.append(now + timedelta(hours = 11))
        self.datetimes.append(now + timedelta(hours = 17))
        self.reltimes.append(0)
        self.reltimes.append(21600)
        self.reltimes.append(43200)
        self.reltimes.append(64800)
        self.frames.append( \
                [[(2,1), (3,2), (4, 3), (5, 4), (5, 4)], \
                 [(3,1), (3,2), (3, 3), (3, 4), (5, 4)], \
                 [(4,-1), (4,-2), (4, -3), (4, -4), (5, 4)], \
                 [(4,-1), (4,-2), (4, -3), (4, -4), (5, 4)]])
        self.frames.append( \
                [[(3,1), (4,2), (5, 3), (6, 4), (5, 4)], \
                 [(4,1), (4,2), (4, 3), (5, 4), (5, 4)], \
                 [(5,-1), (5,-2), (6, -3), (7, -4), (5, 4)], \
                 [(5,-1), (5,-2), (5, -3), (5, -4), (5, 4)]])
        self.frames.append( \
                [[(4,1), (5,2), (6, 3), (7, 4), (5, 4)], \
                 [(5,1), (5,2), (5, 3), (5, 4), (5, 4)], \
                 [(6,-1), (6,-2), (6, -3), (6, -4), (5, 4)], \
                 [(6,-1), (6,-2), (6, -3), (6, -4), (5, 4)]])
        self.frames.append( \
                [[(4,1), (5,2), (6, 3), (7, 4), (5, 4)], \
                 [(5,1), (5,2), (5, 3), (5, 4), (5, 4)], \
                 [(6,-1), (6,-2), (6, -3), (6, -4), (5, 4)], \
                 [(6,-1), (6,-2), (6, -3), (6, -4), (5, 4)]])

        self.reltime_range = self.reltimes[-1]
        self.reltime_n = len(self.reltimes)

    def update_when_required(self):
        return True

class TestWind(unittest.TestCase):
    def setUp(self):
        self.weather = FakeWeather()
        self.wind = Wind(self.weather)

    def tearDown(self):
        self.wind = None
        self.weather = None


    def testGet(self):
        t = datetime.utcnow() + timedelta(hours = 8)
        #wind = self.wind.get((0.375, 0.1), t)
        #self.assertAlmostEqual(3.1415, wind[0], 2)
        #self.assertAlmostEqual(5.25, wind[1], 2)


if __name__ == '__main__':
    unittest.main()
