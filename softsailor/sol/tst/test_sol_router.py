import os
import unittest
import logging
import testing_helper

from softsailor.utils import *
from softsailor.sol.sol_chart import *
from softsailor.sol.sol_course import *
from softsailor.sol.sol_functions import *
from softsailor.router import *

from courses import *

setup_log('test_sol_router', logging.DEBUG)
_log = logging.getLogger('softsailor.sol.tst.test_sol_router')

class TestRouter(unittest.TestCase):
    @unittest.skipIf(testing_helper.offline or True, "Can't get map tiles offline")
    def testPB3(self):
        _log.info('******** PB3 test ********')
        chart = SolChart()
        chart.load_tiles('race.sailport.se', 'h', deg_to_rad(57, 60, 22, 28))
        chart.save_to_kml('estonia_chart.kml')
        course = SolCourse(gen_waypoints_pb3_2011(), 200, chart)
        course.save_to_kml('estonia_course.kml')
        router = Router(chart=chart, boat=None, course=course)
        router.construct_legs()
        router.course.save_to_kml('estonia_router.kml')
        for i, leg in enumerate(router.legs):
            for j, rt in enumerate(leg):
                rt.save_to_kml('router_leg_%d_%d.kml' % (i, j))
                if j > 4:
                    break

    @unittest.skip('This test is currently failing')
    @unittest.skipIf(testing_helper.offline, "Can't get map tiles offline")
    def testBrittany(self):
        _log.info('******** Brittany test ********')
        sts = get_settings('Breizh_Lightning_2012.xml')
        chrt = get_chart()
        crs = get_course()
        rtr = Router(chart=chrt, boat=None, course=crs)
        rtr.construct_legs()



if __name__ == '__main__':
    unittest.main()
