import unittest

from softsailor.boat import Boat, SailBoat

class TestBoat(unittest.TestCase):
    """ Test a boat for required properties and functionality """
    def setUp(self):
        self.boat = Boat()

    def testHasHeading(self):
        self.assertTrue(hasattr(self.boat, 'heading'))

    def testHasCourse(self):
        self.assertTrue(hasattr(self.boat, 'course'))

    def testHasSpeed(self):
        self.assertTrue(hasattr(self.boat, 'speed'))

    def testHasPosition(self):
        self.assertTrue(hasattr(self.boat, 'position'))
        try:
            it = iter(self.boat.position)
        except TypeError:
            self.fail('Position iterable check')

    def testSteeringSetsHeading(self):
        self.boat.steer(88)
        self.assertEqual(88, self.boat.heading)

class TestSailBoat(TestBoat):
    """ Test properties and functionality of a sailing boat """
    def setUp(self):
        self.boat = SailBoat()

    def testHasMainSail(self):
        self.assertTrue(hasattr(self.boat, 'main_sail'))

    def testHasHeadSail(self):
        self.assertTrue(hasattr(self.boat, 'head_sail'))

    def testHasSpinnaker(self):
        self.assertTrue(hasattr(self.boat, 'spinnaker'))

    def testHasWind(self):
        self.assertTrue(hasattr(self.boat, 'wind'))
        try:
            it = iter(self.boat.wind)
        except TypeError:
            self.fail('Wind iterable check')

    def testWindAngle(self):
        self.assertEqual(0, self.boat.wind_angle)

if __name__ == '__main__':
    unittest.main()

