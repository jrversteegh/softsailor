import os
import unittest
import test_utils

from softsailor.utils import *
from softsailor.sol.sol_course import *
from softsailor.sol.sol_map import *

from geofun import Position, Vector

def gen_waypoints():
    result = []
    # Rotterdam start
    result.append(Position(deg_to_rad(52.00), deg_to_rad( 4.10)))
    # Somewhere on the english coast a little north of newcastle
    result.append(Position(deg_to_rad(55.64), deg_to_rad(-1.55)))
    # Skagen
    result.append(Position(deg_to_rad(57.74), deg_to_rad(10.60)))
    # South of laeso island
    result.append(Position(deg_to_rad(57.20), deg_to_rad(11.15)))
    # Goteborg finish
    result.append(Position(deg_to_rad(57.61), deg_to_rad(11.70)))
    return result

def gen_waypoints_pb3_2011():
    """Race along the shores of estonia"""
    # Good race for collision detection
    result = []
    result.append(Position(*deg_to_rad(58.3700, 24.5000)))
    result.append(Position(*deg_to_rad(58.9036, 23.3503)))
    result.append(Position(*deg_to_rad(58.9500, 23.5000)))
    result.append(Position(*deg_to_rad(59.2200, 23.5200)))
    result.append(Position(*deg_to_rad(59.4870, 24.7080)))
    result.append(Position(*deg_to_rad(59.4690, 24.8190)))
    return result

class TestCourse(unittest.TestCase):
    def setUp(self):
        chart = Map()
        dirname = os.path.dirname(os.path.abspath(__file__))
        chart.load(dirname + '/Gbr_Gtb.xml')
        waypoints = gen_waypoints()
        self.crs = SolCourse(waypoints, 1000, chart)

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
    chart = Map()
    chart.load_tiles('race.sailport.se', 'h', deg_to_rad(57, 60, 22, 25))
    def setUp(self):
        waypoints = gen_waypoints_pb3_2011()
        self.crs = SolCourse(waypoints, 1000, self.chart)

    def testOrientation(self):
        self.assertFalse(self.crs.marks[0].to_port)
        self.assertTrue(self.crs.marks[1].to_port)
        self.assertFalse(self.crs.marks[2].to_port)
        self.assertFalse(self.crs.marks[3].to_port)

    def testOnLand(self):
        self.assertTrue(self.crs.marks[0].on_land)
        self.assertFalse(self.crs.marks[1].on_land)
        self.assertTrue(self.crs.marks[2].on_land)
        self.assertTrue(self.crs.marks[3].on_land)

if __name__ == '__main__':
    unittest.main()
