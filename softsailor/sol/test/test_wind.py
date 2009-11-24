import unittest
import test_utils

from softsailor.sol.wind import *
from softsailor.utils import *
from softsailor.sol.weather import *
from softsailor.sol.settings import *

from datetime import datetime, timedelta


class FakeWeather:
    lat_min = 0
    lat_max = 0.75
    lat_n = 4
    lon_min = -0.1
    lon_max = 0.3
    lon_n = 5

    def __init__(self):
        self.frames = []
        self.frame_times = []
        now = datetime.utcnow()
        self.frame_times.append(now - timedelta(hours = 1))
        self.frame_times.append(now + timedelta(hours = 5))
        self.frame_times.append(now + timedelta(hours = 11))
        self.frame_times.append(now + timedelta(hours = 17))
        self.frames.append( \
                [[(2,1), (3,2), (4, 3), (5, 4), (5, 4)], \
                 [(3,1), (3,2), (3, 3), (3, 4), (5, 4)], \
                 [(4,-1), (4,-2), (4, -3), (4, -4), (5, 4)], \
                 [(4,-1), (4,-2), (4, -3), (4, -4), (5, 4)]])
        self.frames.append( \
                [[(3,1), (4,2), (5, 3), (6, 4), (5, 4)], \
                 [(4,1), (4,2), (4, 3), (4, 4), (5, 4)], \
                 [(5,-1), (5,-2), (5, -3), (5, -4), (5, 4)], \
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

    def verify_up_to_date(self):
        pass

class TestWind(unittest.TestCase):
    def setUp(self):
        self.weather = FakeWeather()
        self.wind = Wind(self.weather)

    def tearDown(self):
        self.wind = None
        self.weather = None

    def testGetWind(self):
        t = datetime.utcnow() + timedelta(hours = 8)
        wind = self.wind.get_bilinear((0.375, 0.1), t)
        self.assertAlmostEqual(3.1415927, wind[0], 5)
        self.assertAlmostEqual(5, wind[1], 5)

    def testGetSplined(self):
        t = datetime.utcnow() + timedelta(hours = 11)
        wind = self.wind.get_splined((0.5, 0.1), t)
        expected_wind = rectangular_to_polar((-6, 3))
        self.assertAlmostEqual(expected_wind[0], wind[0], 4)
        self.assertAlmostEqual(expected_wind[1], wind[1], 4)

    def testGetSplinedEdge(self):
        t = datetime.utcnow() - timedelta(hours = 1)
        wind = self.wind.get_splined((0, -0.1), t)
        expected_wind = rectangular_to_polar((-2, -1))
        self.assertAlmostEqual(expected_wind[0], wind[0], 5)
        self.assertAlmostEqual(expected_wind[1], wind[1], 5)

    def testBilinearVersusSplined(self):
        t = datetime.utcnow() + timedelta(hours = 7)
        bilinear_wind = self.wind.get_bilinear((0.366, 0.05), t)
        splined_wind = self.wind.get_splined((0.366, 0.05), t)
        self.assertAlmostEqual(bilinear_wind[0], splined_wind[0], 2)
        self.assertAlmostEqual(bilinear_wind[1], splined_wind[1], 1)
        

    def testBilinearVersusSplinedReal(self):
        settings = Settings()
        weather = Weather()
        weather.load(settings)
        wind = Wind(weather)
        lat_step = (weather.lat_max - weather.lat_min) / (weather.lat_n - 1)
        lon_step = (weather.lon_max - weather.lon_min) / (weather.lon_n - 1)
        print "lats, lons: ", lat_step, lon_step
        print "latmi, lonmi: ", weather.lat_min, weather.lon_min
        print "latma, lonma: ", weather.lat_max, weather.lon_max
        lat = weather.lat_min + 8 * lat_step 
        lon = weather.lon_min + 15 * lon_step 
        print "lat, lon: ", lat, lon
        t = wind.start_time + 2 * \
                        (weather.frame_times[1] - weather.frame_times[0])
        print "t: ", t
        bilinear_wind = wind.get_bilinear((lat, lon), t)
        splined_wind = wind.get_splined((lat, lon), t)
        self.assertAlmostEqual(bilinear_wind[0], splined_wind[0], 3)
        self.assertAlmostEqual(bilinear_wind[1], splined_wind[1], 3)

if __name__ == '__main__':
    unittest.main()
