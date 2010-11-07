import unittest
from softsailor.route import *
from softsailor.boat import *
from softsailor.router import *

class TestRouter(unittest.TestCase):
    def setUp(self):
        self.route = Route(((1.0, 1.0), (0.9, 1.0)))
        self.boat = SailBoat()
        self.router = Router(self.route, self.boat)

    def testHasBearing(self):
        self.assertTrue(hasattr(self.router, 'bearing'))

    def testHasActiveWaypoint(self):
        wp = self.router.active_waypoint

    def testHasActiveIndex(self):
        i = self.router.active_index

    def testHasIsComplete(self):
        b = self.router.is_complete
