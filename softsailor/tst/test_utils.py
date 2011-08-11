import unittest
import testing_helper
import math

from softsailor.utils import *

class TestUtils(unittest.TestCase):
    def testDegToRad(self):
        self.assertEqual(math.pi, deg_to_rad(180))
        degs =[90, -90]
        rads = deg_to_rad(degs)
        self.assertAlmostEqual(math.pi / 2, rads[0])
        self.assertAlmostEqual(-math.pi / 2, rads[1])
        rads = deg_to_rad(degs[0], degs[1])
        self.assertAlmostEqual(math.pi / 2, rads[0])
        self.assertAlmostEqual(-math.pi / 2, rads[1])

    def testBearingToHeading(self):
        bearing = (math.pi / 4, 1)
        speed = 5
        current = (0, 1)
        heading = bearing_to_heading(bearing, speed, current)
        self.assertAlmostEqual(math.atan(4.0/3.0), heading)
        bearing = (math.atan(4.0/2.0), 1)
        current = (math.pi, 1)
        heading = bearing_to_heading(bearing, speed, current)
        self.assertAlmostEqual(math.atan(4.0/3.0), heading)

if __name__ == '__main__':
    unittest.main()
