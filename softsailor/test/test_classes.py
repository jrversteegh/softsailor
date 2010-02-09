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
        self.assertTrue(self.vector.equals(CartesianVector(3, 4)))

    def testAddition(self):
        vector = self.vector + CartesianVector(1, -1)
        self.assertTrue(vector.equals(CartesianVector(4,3)))

        self.vector += CartesianVector(1, -1)
        self.assertTrue(self.vector.equals(CartesianVector(4,3)))
        self.assertTrue(self.vector.equals((math.atan(3.0/4.0), 5)))

    def testSubtraction(self):
        vector = self.vector - CartesianVector(1, -1)
        self.assertTrue(vector.equals(CartesianVector(2,5)))

        self.vector -= CartesianVector(1, -1)
        self.assertTrue(self.vector.equals(CartesianVector(2,5)))

    def testMultiplication(self):
        vector = self.vector * 2
        self.assertTrue(vector.equals(CartesianVector(6,8)))

        self.vector *= 2
        self.assertTrue(self.vector.equals(CartesianVector(6,8)))

class TestPolarVector(unittest.TestCase, BaseTestVector):
    def setUp(self):
        self.vector = PolarVector(math.atan(4.0/3.0), 5)

class TestCartesianVector(unittest.TestCase, BaseTestVector):
    def setUp(self):
        self.vector = CartesianVector(3, 4)


if __name__ == '__main__':
    unittest.main()

