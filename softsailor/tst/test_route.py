import unittest
import math
import tempfile

import testing_helper
from softsailor.classes import *
from softsailor.route import *

class TestWaypoint(unittest.TestCase):
    def setUp(self):
        self.waypoint = Waypoint(1, 1)
        self.waypoint.range = 18
        self.waypoint.comment = "Test"
    
    def testBearing(self):
        self.assertAlmostEqual(math.pi, (self.waypoint - Position(1.1, 1))[0])

    def testCopyConstruct(self):
        wp = Waypoint(self.waypoint)
        self.assertEqual(self.waypoint.lat, wp.lat)
        self.assertEqual(self.waypoint.lon, wp.lon)
        self.assertEqual(self.waypoint.range, wp.range)
        self.assertEqual(self.waypoint.comment, wp.comment)

class TestRoute(unittest.TestCase):
    def setUp(self):
        self.route = Route()
        self.route.add(1, 2)
        self.route.add(0.9, 2)
        self.route[0].comment = "Test"

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
        self.assertAlmostEqual(math.pi, sg.v.a)

    def testLength(self):
        #TODO
        pass

    def testSaveToKml(self):
        self.route.save_to_kml(tempfile.gettempdir() + '/test.kml')

    def testLen(self):
        self.assertEquals(2, len(self.route))

    def testCopyConstruct(self):
        route = Route(self.route)
        self.assertEqual(len(self.route), len(route))
        self.assertEqual(self.route[0], route[0])

if __name__ == '__main__':
    unittest.main()
