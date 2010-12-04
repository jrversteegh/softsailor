import unittest
import math

import test_helper
from softsailor.classes import *

class BaseTestVector:
    def testHasPolarCoords(self):
        self.assertTrue(hasattr(self.vector, 'ar'))

    def testHasCartesianCoords(self):
        self.assertTrue(hasattr(self.vector, 'xy'))

    def testHasA(self):
        self.assertTrue(hasattr(self.vector, 'a'))

    def testHasR(self):
        self.assertTrue(hasattr(self.vector, 'r'))

    def testHasX(self):
        self.assertTrue(hasattr(self.vector, 'x'))

    def testHasY(self):
        self.assertTrue(hasattr(self.vector, 'y'))

    def testSetX(self):
        self.vector.x = 4
        self.assertAlmostEqual(4, self.vector.x)
        self.assertAlmostEqual(math.sqrt(32), self.vector.r)

    def testEquality(self):
        self.assertEquals(self.vector, CartesianVector(3, 4))

    def testAddition(self):
        vector = self.vector + CartesianVector(1, -1)
        self.assertEquals(vector, CartesianVector(4, 3))

        self.vector += CartesianVector(1, -1)
        self.assertTrue(self.vector == (CartesianVector(4, 3)))
        self.assertTrue(self.vector == ((math.atan(3.0/4.0), 5)))

    def testSubtraction(self):
        vector = self.vector - CartesianVector(1, -1)
        self.assertTrue(vector == CartesianVector(2,5))

        self.vector -= CartesianVector(1, -1)
        self.assertTrue(self.vector == CartesianVector(2, 5))

    def testMultiplication(self):
        vector = self.vector * 2
        self.assertTrue(vector == CartesianVector(6,8))

        self.vector *= 2
        self.assertTrue(self.vector == CartesianVector(6,8))

class TestPolarVector(unittest.TestCase, BaseTestVector):
    def setUp(self):
        self.vector = PolarVector(math.atan(4.0/3.0), 5)

class TestCartesianVector(unittest.TestCase, BaseTestVector):
    def setUp(self):
        self.vector = CartesianVector(3, 4)

class TestPosition(unittest.TestCase):
    def setUp(self):
        self.position_1 = Position((1.0, 1.0))
        self.position_2 = Position(0.9, 1.0)
        self.position_3 = Position(1.0, 0.9)
        self.position_4 = Position(0.9, 0.9)

    def testHasGetBearingFrom(self):
        self.assertTrue(hasattr(self.position_1, 'get_bearing_from'))
        self.assertTrue(hasattr(self.position_1.get_bearing_from, '__call__'))

    def testHasGetBearingTo(self):
        self.assertTrue(hasattr(self.position_1, 'get_bearing_to'))
        self.assertTrue(hasattr(self.position_1.get_bearing_to, '__call__'))

    def testGetBearingFrom(self):
        br = self.position_3.get_bearing_from(self.position_1)
        self.assertAlmostEqual(math.pi * 3/2, br[0])

    def testGetBearingTo(self):
        br = self.position_1.get_bearing_to(self.position_2)
        self.assertAlmostEqual(math.pi, br[0])

    def testAddition(self):
        bearing = self.position_4 - self.position_1
        new_pos = self.position_1 + bearing
        bearing = new_pos.get_bearing_from(self.position_4)
        self.assertTrue(bearing[1] < 100, "Check addition")

    def testSubtraction(self):
        bearing = self.position_4 - self.position_1
        new_pos = self.position_4 - bearing
        bearing = new_pos.get_bearing_from(self.position_1)
        self.assertTrue(bearing[1] < 100, "Check addition")

    def testNonLinearity(self):
        bearing = self.position_4 - self.position_1
        new_pos = Position(self.position_1)
        for i in range(10):
            new_pos += bearing * 0.1
        bearing = new_pos.get_bearing_from(self.position_4)
        self.assertTrue(bearing[1] < 320, "Check non linearity")


if __name__ == '__main__':
    unittest.main()

