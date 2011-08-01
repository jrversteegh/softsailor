import os
import unittest
import testing_helper

from softsailor.utils import *
from softsailor.sol.sol_map import *
from softsailor.sol.sol_course import *
from softsailor.router import *

from courses import *

class TestRouter(unittest.TestCase):
    def testPB3(self):
        chart = Map()
        chart.load_tiles('race.sailport.se', 'h', deg_to_rad(57, 60, 22, 25))
        course = SolCourse(gen_waypoints_pb3_2011(), 200, chart)
        router = Router(chart=chart, boat=None, course=course)
        router.course.save_to_kml('course_route.kml')


if __name__ == '__main__':
    unittest.main()
