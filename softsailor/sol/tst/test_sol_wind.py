import unittest
import testing_helper
from datetime import datetime, timedelta

from softsailor.utils import *

from softsailor.sol.sol_wind import *
from softsailor.sol.sol_weather import *
from softsailor.sol.sol_settings import *

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
        pass

class TestWind(unittest.TestCase):
    def setUp(self):
        self.weather = FakeWeather()
        self.wind = SolWind(self.weather)

    def tearDown(self):
        self.wind = None
        self.weather = None

    def testGetIndices(self):
        indices = self.wind.get_indices(0.4, 0.12, 36000)
        self.assertEqual(1, indices[0])
        self.assertEqual(2, indices[1])
        self.assertEqual(1, indices[2])

    def testUpdateSlices(self):
        self.wind.update_slices(0.4, 0.12, 10800)
        self.assertEqual(0.25, self.wind.grid_slice[0, 0, 0, 0])
        self.assertEqual(0.50, self.wind.grid_slice[0, 1, 0, 0])
        self.assertEqual(0.1, self.wind.grid_slice[1, 0, 0, 0])
        self.assertEqual(0.0, self.wind.grid_slice[2, 0, 0, 0])

        self.assertEqual(3, self.wind.u_slice[0, 0, 0])
        self.assertEqual(4, self.wind.u_slice[1, 1, 0])

        self.assertEqual(5, self.wind.u_slice[0, 1, 1])
        self.assertEqual(6, self.wind.u_slice[1, 0, 1])
        self.assertEqual(7, self.wind.u_slice[1, 1, 1])

        self.assertEqual(3, self.wind.v_slice[0, 0, 0])
        self.assertEqual(-3, self.wind.v_slice[1, 0, 0])

    def testGetFracs(self):
        fracs = self.wind.get_fracs(0.4, 0.12, 32400) 
        self.assertAlmostEqual(0.6, fracs[0], 8)
        self.assertAlmostEqual(0.2, fracs[1], 8)
        self.assertAlmostEqual(0.5, fracs[2], 8)

    def testEvaluateCubic(self):
        self.wind.update_slices(0.375, 0.15, 10800)
        self.wind.base_funcs = base_funcs_cubic
        self.wind.u_slice = np.array([[[1, 0],[0, 0]],[[0, 0],[0, 0]]])
        self.wind.du_slice = np.array([[[[0, 0],[0, 0]],[[0, 0],[0, 0]]],
                                       [[[0, 0],[0, 0]],[[0, 0],[0, 0]]],
                                       [[[0, 0],[0, 0]],[[0, 0],[0, 0]]]])
        self.assertAlmostEqual(0.125, self.wind.evaluate(0.5, 0.5, 0.5)[0], 8)
        self.assertAlmostEqual(1.0, self.wind.evaluate(0, 0, 0)[0], 8)
        self.wind.u_slice = np.array([[[0, 0],[0, 0]],[[0, 0],[0, 0]]])
        self.wind.du_slice = np.array([[[[1, 0],[0, 0]],[[0, 0],[0, 0]]],
                                       [[[0, 0],[0, 0]],[[0, 0],[0, 0]]],
                                       [[[0, 0],[0, 0]],[[0, 0],[0, 0]]]])
        self.assertAlmostEqual(0.03125, self.wind.evaluate(0.5, 0.5, 0.5)[0], 8)

    def testEvaluateLinear(self):
        self.wind.update_slices(0.375, 0.15, 10800)
        self.wind.u_slice = np.array([[[1, 0],[0, 0]],[[0, 0],[0, 0]]])
        self.wind.du_slice = np.array([[[[0, 0],[0, 0]],[[0, 0],[0, 0]]],
                                       [[[0, 0],[0, 0]],[[0, 0],[0, 0]]],
                                       [[[0, 0],[0, 0]],[[0, 0],[0, 0]]]])
        self.assertAlmostEqual(0.125, self.wind.evaluate(0.5, 0.5, 0.5)[0], 8)
        self.assertAlmostEqual(1.0, self.wind.evaluate(0, 0, 0)[0], 8)
        self.wind.u_slice = np.array([[[0, 0],[0, 0]],[[0, 0],[0, 0]]])
        self.wind.du_slice = np.array([[[[1, 0],[0, 0]],[[0, 0],[0, 0]]],
                                       [[[0, 0],[0, 0]],[[0, 0],[0, 0]]],
                                       [[[0, 0],[0, 0]],[[0, 0],[0, 0]]]])
        self.assertAlmostEqual(0.0, self.wind.evaluate(0.5, 0.5, 0.5)[0], 8)

    def testGet(self):
        t = datetime.utcnow() + timedelta(hours = 8)
        wind = self.wind.get((0.375, 0.1), t)
        self.assertAlmostEqual(3.1415, wind[0], 2)
        self.assertAlmostEqual(5.25, wind[1], 2)


if __name__ == '__main__':
    unittest.main()
