import os
import unittest

import testing_helper
from courses import *

from softsailor.utils import *
from softsailor.sol.sol_course import *
from softsailor.sol.sol_chart import *

from geofun import Position, Vector


class TestCourse(unittest.TestCase):
    def setUp(self):
        chart = Chart()
        dirname = os.path.dirname(os.path.abspath(__file__))
        chart.load(dirname + '/Gbr_Gtb.xml')
        waypoints = gen_waypoints()
        self.crs = Course(waypoints, 1000, chart)

    def testOrientation(self):
        self.assertFalse(self.crs.marks[0].to_port)
        self.assertFalse(self.crs.marks[1].to_port)
        self.assertTrue(self.crs.marks[2].to_port)

    def testOnLand(self):
        self.assertFalse(self.crs.marks[0].on_land)
        self.assertTrue(self.crs.marks[1].on_land)
        self.assertFalse(self.crs.marks[2].on_land)

    def testSaveToKml(self):
        dirname = os.path.dirname(os.path.abspath(__file__))
        self.crs.save_to_kml(dirname + '/course.kml')

class TestCourse2(unittest.TestCase):
    chart = Chart()
    if not testing_helper.offline:
        chart.load_tiles('node1.sailonline.org', 'h', deg_to_rad(57, 60, 22, 28))
    def setUp(self):
        waypoints = gen_waypoints_pb3_2011()
        self.crs = Course(waypoints, 1000, self.chart)

    @unittest.skipIf(testing_helper.offline, "Can't load maptiles offline")
    def testOrientation(self):
        self.assertFalse(self.crs.marks[0].to_port)
        self.assertTrue(self.crs.marks[1].to_port)
        self.assertFalse(self.crs.marks[2].to_port)
        self.assertFalse(self.crs.marks[3].to_port)

    @unittest.skipIf(testing_helper.offline, "Can't load maptiles offline")
    def testOnLand(self):
        self.assertTrue(self.crs.marks[0].on_land)
        self.assertFalse(self.crs.marks[1].on_land)
        self.assertTrue(self.crs.marks[2].on_land)
        self.assertTrue(self.crs.marks[3].on_land)

if __name__ == '__main__':
    unittest.main()
