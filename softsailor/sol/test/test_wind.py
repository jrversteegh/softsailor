import unittest
import test_utils

from softsailor.sol.wind import *
from softsailor.utils import *

from datetime import datetime, timedelta


class FakeWeather:
    lat_min = 0
    lat_max = 0.75
    lat_n = 4
    lon_min = -0.1
    lon_max = 0.2
    lon_n = 4
    frames = []
    frame_times = []

    def __init__(self):
        now = datetime.utcnow()
        self.frame_times.append(now - timedelta(hours = 1))
        self.frame_times.append(now + timedelta(hours = 5))
        self.frame_times.append(now + timedelta(hours = 11))
        self.frame_times.append(now + timedelta(hours = 17))
        self.frames.append( \
                [[(2,1), (3,2), (4, 3), (5, 4)], \
                 [(3,1), (3,2), (3, 3), (3, 4)], \
                 [(4,-1), (4,-2), (4, -3), (4, -4)], \
                 [(4,-1), (4,-2), (4, -3), (4, -4)]])
        self.frames.append( \
                [[(3,1), (4,2), (5, 3), (6, 4)], \
                 [(4,1), (4,2), (4, 3), (4, 4)], \
                 [(5,-1), (5,-2), (5, -3), (5, -4)], \
                 [(5,-1), (5,-2), (5, -3), (5, -4)]])
        self.frames.append( \
                [[(4,1), (5,2), (6, 3), (7, 4)], \
                 [(5,1), (5,2), (5, 3), (5, 4)], \
                 [(6,-1), (6,-2), (6, -3), (6, -4)], \
                 [(6,-1), (6,-2), (6, -3), (6, -4)]])
        self.frames.append( \
                [[(4,1), (5,2), (6, 3), (7, 4)], \
                 [(5,1), (5,2), (5, 3), (5, 4)], \
                 [(6,-1), (6,-2), (6, -3), (6, -4)], \
                 [(6,-1), (6,-2), (6, -3), (6, -4)]])

class TestWind(unittest.TestCase):
    def setUp(self):
        self.wind = Wind(FakeWeather())

    def testGetWind(self):
        t = datetime.utcnow() + timedelta(hours = 8)
        wind = self.wind.get_bilinear((0.375, 0.1), t)
        self.assertAlmostEqual(3.1415927, wind[0], 5)
        self.assertAlmostEqual(5, wind[1], 5)
        t = datetime.utcnow() + timedelta(hours = 11)
        wind = self.wind.get_splined((0.5, 0.1), t)
        expected_wind = rectangular_to_polar((-6, 3))
        self.assertAlmostEqual(expected_wind[0], wind[0], 5)
        self.assertAlmostEqual(expected_wind[1], wind[1], 5)
        t = datetime.utcnow() - timedelta(hours = 1)
        wind = self.wind.get_splined((0, -0.1), t)
        expected_wind = rectangular_to_polar((-2, -1))
        self.assertAlmostEqual(expected_wind[0], wind[0], 5)
        self.assertAlmostEqual(expected_wind[1], wind[1], 5)

    def testBilinearVersusSplined(self):
        t = datetime.utcnow() + timedelta(hours = 7)
        bilinear_wind = self.wind.get_bilinear((0.366, 0.05), t)
        splined_wind = self.wind.get_splined((0.366, 0.05), t)
        self.assertAlmostEqual(bilinear_wind[0], splined_wind[0], 1)
        self.assertAlmostEqual(bilinear_wind[1], splined_wind[1], 1)
        

if __name__ == '__main__':
    unittest.main()
