
import unittest
import math
from datetime import datetime, timedelta
import testing_helper

import numpy as np

from wind import *
from utils import * 

grid = np.mgrid[0:0.75:4j,-0.1:0.3:5j,0:64800:4j]

def u_fun(lat, lon, t):
    return 10 * (1 - lat + lon + lat * lon) - 0.0001 * t

def v_fun(lat, lon, t):
    return 10 * (1 - lon - lat * lon) + 0.0001 * t

u = 10 * (1 - grid[0] + grid[1] + grid[0] * grid[1]) - 0.0001 * grid[2]
v = 10 * (1 - grid[1] - grid[0] * grid[1]) + 0.0001 * grid[2]

class WindSetup(object):
    def doSetup(self):
        self.wind.start = datetime.utcnow()
        # Assign grid and data
        self.wind.grid = grid
        self.wind.init_value_arrays()
        self.wind.u = u
        self.wind.v = v
        # Make sure we're ready to calculate
        self.wind.update_coefficients()

    def testGet(self):
        lat = 0.69 
        lon = 0.05
        dt = timedelta(hours=4.5)
        ts = dt.total_seconds()
        t = self.wind.start + dt
        d, s = self.wind.get((lat, lon), t)
        d_ex, s_ex = rectangular_to_polar(
            (u_fun(lat, lon, ts), v_fun(lat, lon, ts)))
        d_ex = normalize_angle_2pi(d_ex + math.pi)
        self.assertAlmostEqual(d_ex, d, delta=self.d_acc)
        self.assertAlmostEqual(s_ex, s, delta=self.s_acc)


class TestInterpolledWind(unittest.TestCase, WindSetup):
    d_acc = 0.1
    s_acc = 0.2
    def setUp(self):
        self.wind = InterpolledWind(basefuncs=basefuncs_cubic)
        self.doSetup()

    def testGetIndices(self):
        indices = self.wind.get_indices(0.4, 0.12, 36000)
        self.assertEqual(1, indices[0])
        self.assertEqual(2, indices[1])
        self.assertEqual(1, indices[2])


class TestSplinedWind(unittest.TestCase, WindSetup):
    d_acc = 0.05
    s_acc = 0.3
    def setUp(self):
        self.wind = SplinedWind()
        self.doSetup()


if __name__ == '__main__':
    unittest.main()
