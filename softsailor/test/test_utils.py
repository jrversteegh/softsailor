import unittest

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
