import os
import unittest
import testing_helper

from softsailor.utils import *
from softsailor.sol.sol_map import *
from softsailor.sol.sol_course import *
from softsailor.router import *

from courses import *

class TestRouter(unittest.TestCase):
    @unittest.skipIf(testing_helper.offline, "Can't get map tiles offline")
    def testPB3(self):
        chart = SolMap()
        chart.load_tiles('race.sailport.se', 'h', deg_to_rad(57, 60, 22, 28))
        chart.save_to_kml('estonia_chart.kml')
        course = SolCourse(gen_waypoints_pb3_2011(), 200, chart)
        course.save_to_kml('estonia_course.kml')
        router = Router(chart=chart, boat=None, course=course)
        router.course.save_to_kml('router_course.kml')
        for i, leg in enumerate(router.legs):
            for j, rt in enumerate(leg):
                rt.save_to_kml('router_leg_%d_%d.kml' % (i, j))
                if j > 4:
                    break


if __name__ == '__main__':
    unittest.main()
