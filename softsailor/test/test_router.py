import unittest
import testing_helper

from softsailor.map import Map
from softsailor.course import Course
from softsailor.boat import SailBoat
from softsailor.router import *

class TestRouter(unittest.TestCase):
    def testConstruction(self):
        boat = SailBoat()
        course = Course()
        chart = Map()
        router = Router(boat=boat, course=course, chart=chart)
        self.assertEqual(1, len(router.legs))


if __name__ == '__main__':
    unittest.main()
