import unittest
import testing_helper

from softsailor.chart import Chart
from softsailor.course import Course
from softsailor.boat import SailBoat
from softsailor.router import *

from geofun import Position

class TestRouter(unittest.TestCase):
    def testConstruction(self):
        boat = SailBoat()
        course = Course()
        chart = Chart()
        router = Router(boat=boat, course=course, chart=chart)
        self.assertEqual(1, len(router.legs))

    def testValidRoute(self):
        p1 = Position(0.9, 0.9)
        p2 = Position(1.0, 1.0)
        p3 = Position(1.0, 1.1)
        pt1 = Position(0.99, 1.0)
        pt2 = Position(1.01, 1.0)
        r1 = Route((p1, pt1, p3))
        r2 = Route((p1, pt2, p3))
        c = Course((p1, p2, p3))
        boat = SailBoat()
        chart = Chart()
        router = Router(boat=boat, course=c, chart=chart)
        self.assertFalse(router.valid_route(r1))
        self.assertTrue(router.valid_route(r2))
        c.marks[0].to_port = True
        self.assertTrue(router.valid_route(r1))
        self.assertFalse(router.valid_route(r2))


if __name__ == '__main__':
    unittest.main()
