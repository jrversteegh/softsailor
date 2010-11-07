import unittest
import math

import test_helper
from softsailor.classes import *
from softsailor.route import *

class TestWaypoint(unittest.TestCase):
    def setUp(self):
        self.waypoint = Waypoint(1, 1)
    
    def testBearing(self):
        self.assertAlmostEqual(math.pi, self.waypoint.bearing(1.1, 1)[0])

class TestRoute(unittest.TestCase):
    def setUp(self):
        self.route = Route()
        self.route.add(1, 2)
        self.route.add(0.9, 2)

    def testIsSubsriptable(self):
        wp = self.route[0]
        lat, lon = wp
        self.assertAlmostEqual(1, lat)
        self.assertAlmostEqual(2, lon)

    def testHasWaypoints(self):
        try:
            it = iter(self.route.waypoints)
        except TypeError:
            self.fail('Waypoints iterable check')

    def testHasSegments(self):
        try:
            it = iter(self.route.segments)
        except TypeError:
            self.fail('Segments iterable check')
        sg = self.route.segments.next()
        self.assertAlmostEqual(math.pi, sg[0].a)
        self.assertAlmostEqual(dxy_dpos(1.05, 0)[0] * 0.1, sg[0].r)

    def testLength(self):
        self.assertAlmostEqual(dxy_dpos(1.05, 0)[0] * 0.1, self.route.length)

    def testLen(self):
        self.assertEquals(2, len(self.route))

