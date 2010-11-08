import unittest
from softsailor.route import *
from softsailor.boat import *
from softsailor.router import *

class TestRouter(unittest.TestCase):
    def setUp(self):
        self.route = Route(((1.1, 1.25), (1.0, 1.0), (0.9, 1.0)))
        self.boat = SailBoat(position=(1.02, 0.98))
        self.router = Router(self.route, self.boat)

    def testHasGetBearing(self):
        self.assertTrue(hasattr(self.router, 'get_bearing'))
        self.assertTrue(hasattr(self.router.get_bearing, '__call__'))

    def testHasActiveWaypoint(self):
        wp = self.router.active_waypoint

    def testHasActiveIndex(self):
        i = self.router.active_index

    def testHasIsComplete(self):
        b = self.router.is_complete

    def testGetBearing(self):
        br = self.router.get_bearing()
        self.assertAlmostEqual(3.046, br[0], 3)
        self.assertEqual(767559, round(br[1]))

    def testCrossTrack(self):
        cte = self.router.get_cross_track()
        self.assertEqual(73028, round(cte))

    def testActiveIndex(self):
        self.assertEquals(2, self.router.active_index)
