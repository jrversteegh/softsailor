import unittest
import testing_helper

from softsailor.polars import *

import numpy as np

from math import pi
wind_angles = [0, 0.25 * pi, 0.5 * pi, 0.75 * pi, pi]
wind_speeds = [0, 5, 10, 15, 20]
boat_speeds = [[0,0,0,0,0],[0,4,5,3,2],[0,5,6,6,5],[0,5,6,6,4],[0,5,6,7,5]]

class TestPolars(unittest.TestCase):
    def setUp(self):
        self.polars = Polars(wind_angles=wind_angles, wind_speeds=wind_speeds,
                             boat_speeds=np.array(boat_speeds).transpose())

    def test_get(self):
        vals = self.polars.get((0, 1), 12)
        self.assertAlmostEqual(0, vals[0], 3)
        self.assertAlmostEqual(5.539, vals[1], 3)
        vals = self.polars.get(1.7, 12)
        self.assertAlmostEqual(6.098, vals, 3)
        vals = self.polars.get((1.7, 12))
        self.assertAlmostEqual(6.098, vals, 3)


if __name__ == "__main__":
    unittest.main()
