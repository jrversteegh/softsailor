#!/usr/bin/env python

import unittest

from softsailor.boat import Boat, SailBoat, Situation, Motion, Sails

class TestSituation(unittest.TestCase):
    def setUp(self):
        self.situation = Situation()

    def testHasHeading(self):
        self.assertTrue(hasattr(self.situation, 'heading'))

    def testHasPosition(self):
        self.assertTrue(hasattr(self.situation, 'position'))
        try:
            it = iter(self.situation.position)
        except TypeError:
            self.fail('Position iterable check')
    

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

    def testWindAngle(self):
        self.assertEqual(0, self.boat.wind_angle)

if __name__ == '__main__':
    unittest.main()

