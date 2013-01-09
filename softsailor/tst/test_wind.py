
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

class TestBasefuncs(unittest.TestCase):
    def testLinear(self):
        s = 0
        for i, j, k in cube_corners:
            f = basefuncs_linear(0.5, 0.5, 0.5, i, j, k) 
            for v in f:
                s += v
        self.assertAlmostEqual(1., s, places=8) 


    def testCubic(self):
        s = 0
        for c in cube_corners:
            f = basefuncs_cubic(0.5, 0.5, 0.5, c[0], c[1], c[2]) 
            for i, v in enumerate(f):
                s += v
        self.assertAlmostEqual(1., s, places=8) 
        s = 0
        for c in cube_corners:
            f = basefuncs_cubic(0.5, 0.5, 0.5, c[0], c[1], c[2]) 
            for i, v in enumerate(f):
                if i > 0:
                    if c[i - 1]:
                        s -= v
                    else:
                        s += v
                else:
                    s += v
        self.assertAlmostEqual(1.75, s, places=8) 

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
    d_acc = 0.01
    s_acc = 0.02
    def setUp(self):
        self.wind = InterpolledWind(basefuncs=basefuncs_cubic)
        self.doSetup()

    def testGetIndices(self):
        indices = self.wind.get_indices(0.4, 0.12, 36000)
        self.assertEqual(1, indices[0])
        self.assertEqual(2, indices[1])
        self.assertEqual(1, indices[2])

    def testGetFracs(self):
        fracs = self.wind.get_fracs(0.4, 0.12, 32400) 
        self.assertAlmostEqual(0.6, fracs[0], 8)
        self.assertAlmostEqual(0.2, fracs[1], 8)
        self.assertAlmostEqual(0.5, fracs[2], 8)

    def testUpdateSlices(self):
        self.wind.update_slices(0.4, 0.12, 10800)
        self.assertEqual(0.25, self.wind.grid_slice[0, 0, 0, 0])
        self.assertEqual(0.50, self.wind.grid_slice[0, 1, 0, 0])
        self.assertEqual(0.1, self.wind.grid_slice[1, 0, 0, 0])
        self.assertEqual(0.0, self.wind.grid_slice[2, 0, 0, 0])


    def testEvaluateCubic(self):
        self.wind.update_slices(0.375, 0.15, 10800)
        self.wind.basefuncs = basefuncs_cubic
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
        self.wind.basefuncs = basefuncs_linear
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

class TestSplinedWind(unittest.TestCase, WindSetup):
    d_acc = 0.05
    s_acc = 0.3
    def setUp(self):
        self.wind = SplinedWind()
        self.doSetup()


if __name__ == '__main__':
    unittest.main()
