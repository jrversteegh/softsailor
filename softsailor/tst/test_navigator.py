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

    def testHasActiveSegment(self):
        l = self.navigator.active_segment
        self.assertEquals(3, len(l))

    def testHasActiveLeg(self):
        l = self.navigator.active_leg
        self.assertEquals(2, len(l))

    def testHasIsComplete(self):
        b = self.navigator.is_complete
        self.assertFalse(b)

    def testGetBearing(self):
        self.assertFalse(self.navigator.is_complete)
        br = self.navigator.get_bearing()
        self.assertFalse(self.navigator.is_complete)
        self.assertAlmostEqual(3.046, br.a, 3)
        self.assertEqual(768884, round(br.r))

    def testCrossTrack(self):
        self.assertEquals(3, len(self.route))
        self.assertFalse(self.navigator.is_complete)
        cte = self.navigator.get_cross_track()
        self.assertEquals(3, len(self.route))
        self.assertEquals(2, self.navigator.active_index)
        self.assertFalse(self.navigator.is_complete)
        self.assertEqual(73100, round(cte))

    def testActiveIndex(self):
        self.assertEquals(2, self.navigator.active_index)

    def testToTrack(self):
        self.assertFalse(self.navigator.is_complete)
        tt = self.navigator.to_track()
        self.assertFalse(self.navigator.is_complete)
        self.assertAlmostEqual(66924, tt.r, -1)
        self.assertAlmostEqual(math.pi / 2, tt.a, 4)

if __name__ == '__main__':
    unittest.main()
