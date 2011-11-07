#!/usr/bin/env python

import unittest
import testing_helper

from softsailor.boat import Boat, SailBoat, Situation, Motion, Sails

class TestBoat(unittest.TestCase):
    """ Test a boat for required properties and functionality """
    def setUp(self):
        self.boat = Boat()

    def testHasSituation(self):
        self.assertTrue(hasattr(self.boat, 'situation'))

    def testHasCondition(self):
        self.assertTrue(hasattr(self.boat, 'condition'))

    def testHasMotion(self):
        self.assertTrue(hasattr(self.boat, 'motion'))

    def testHasHeading(self):
        self.assertTrue(hasattr(self.boat, 'heading'))

    def testHasSpeed(self):
        self.assertTrue(hasattr(self.boat, 'speed'))

    def testHasDrift(self):
        self.assertTrue(hasattr(self.boat, 'drift'))


class TestSails(unittest.TestCase):
    def setUp(self):
        self.sails = Sails()

    def testHasMainSail(self):
        self.assertTrue(hasattr(self.sails, 'main_sail'))

    def testHasHeadSail(self):
        self.assertTrue(hasattr(self.sails, 'head_sail'))

    def testHasSpinnaker(self):
        self.assertTrue(hasattr(self.sails, 'spinnaker'))


class TestSailBoat(TestBoat):
    """ Test properties and functionality of a sailing boat """
    def setUp(self):
        self.boat = SailBoat()

    def testHasSails(self):
        self.assertTrue(hasattr(self.boat, 'sails'))

    def testHasWindAngle(self):
        self.assertTrue(hasattr(self.boat, 'wind_angle'))

    def testHasRelativeWind(self):
        self.assertTrue(hasattr(self.boat, 'relative_wind'))
        try:
            it = iter(self.boat.relative_wind)
        except TypeError:
            self.fail('Relative wind iterable check')

    def testHasApparentWind(self):
        self.assertTrue(hasattr(self.boat, 'apparent_wind'))
        try:
            it = iter(self.boat.apparent_wind)
        except TypeError:
            self.fail('Apparent wind iterable check')

    def testHasVelocityOverGround(self):
        self.assertTrue(hasattr(self.boat, 'velocity_over_ground'))
        try:
            it = iter(self.boat.velocity_over_ground)
        except TypeError:
            self.fail('Velocity over ground iterable check')

if __name__ == '__main__':
    unittest.main()

