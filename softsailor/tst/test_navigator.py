import unittest
import testing_helper
from softsailor.route import *
from softsailor.boat import *
from softsailor.navigator import *

class TestNavigator(unittest.TestCase):
    def setUp(self):
        self.route = Route(((1.1, 1.25), (1.0, 1.0), (0.9, 1.0)))
        self.boat = SailBoat(position=(1.02, 0.98))
        self.navigator = Navigator(self.route, self.boat)

    def testHasGetBearing(self):
        self.assertTrue(hasattr(self.navigator, 'get_bearing'))
        self.assertTrue(hasattr(self.navigator.get_bearing, '__call__'))

    def testHasActiveWaypoint(self):
        wp = self.navigator.active_waypoint

    def testHasActiveIndex(self):
        i = self.navigator.active_index

    def testHasIsComplete(self):
        b = self.navigator.is_complete

    def testGetBearing(self):
        br = self.navigator.get_bearing()
        self.assertAlmostEqual(3.046, br[0], 3)
        self.assertEqual(768884, round(br[1]))

    def testCrossTrack(self):
        cte = self.navigator.get_cross_track()
        self.assertEqual(73100, round(cte))

    def testActiveIndex(self):
        self.assertEquals(2, self.navigator.active_index)
