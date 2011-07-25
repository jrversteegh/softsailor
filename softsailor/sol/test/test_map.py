import unittest
import test_utils

from softsailor.classes import *

from softsailor.sol.sol_map import *
from softsailor.sol.sol_settings import Settings

class TestFuncs(unittest.TestCase):
    def testIntersection(self):
        p1 = Position(0.99, 0.99)
        p2 = Position(0.99, 1.0)
        p3 = Position(1.0, 1.0)
        p4 = Position(1.0, 0.99) 
        line1 = line(p1, p2)
        line2 = line(p2, p3)
        line3 = line(p3, p4)
        line4 = line(p4, p1)
        line5 = line(p1, p3)
        line6 = line(p2, p4)
        line7 = line(p4, p2)
        p = intersection(line1, line2)
        b = p2 - p
        self.assertTrue(b[1] < 200)
        pa = intersection(line5, line6)
        pb = intersection(line6, line5)
        pc = intersection(line5, line7)
        bb = pb - pa
        bc = pc - pa
        print pa
        print pb, bb
        print pc, bc
        self.assertTrue(bb[1] < 200)
        self.assertTrue(bc[1] < 200)
        

class TestMap(unittest.TestCase):
    def setUp(self):
        self.map = Map()

    def testLoad(self):
        settings = Settings()
        self.map.load(settings.map)
        for point in self.map.points:
            has_one_or_two_links = (len(point.links) == 1) \
                    or (len(point.links) == 2)
            self.assertTrue(has_one_or_two_links, \
                            "Expected each point to have one or two links")

    def testHit(self):
        self.map.load('http://race.sailport.se/site_media/maps/xmlmaps/Canary_Brazil.xml')

        # Attempt to hit Sao Antao (Cabo Verde) from all sides
        pos_to = Position(0.297869, -0.43921)
        bearing = PolarVector(0, 30000)
        pos_from = pos_to - bearing
        segment = (pos_from, bearing, pos_to)
        hit = self.map.hit(segment)
        self.assertTrue(hit)

        bearing = PolarVector(1.57, 25000)
        pos_from = pos_to - bearing
        segment = (pos_from, bearing, pos_to)
        hit = self.map.hit(segment)
        self.assertTrue(hit)

        bearing = PolarVector(3.14, 25000)
        pos_from = pos_to - bearing
        segment = (pos_from, bearing, pos_to)
        hit = self.map.hit(segment)
        self.assertTrue(hit)

        bearing = PolarVector(4.71, 30000)
        pos_from = pos_to - bearing
        segment = (pos_from, bearing, pos_to)
        hit = self.map.hit(segment)
        self.assertTrue(hit)

        # This point is not on the island
        pos1 = Position((0.3019, -0.4363))
        pos2 = pos1 - bearing
        segment = (pos1, bearing, pos2 )
        hit = self.map.hit(segment)
        self.assertFalse(hit)

    def testOuter(self):
        self.map.load('http://race.sailport.se/site_media/maps/xmlmaps/Canary_Brazil.xml')
        # Attempt to pass Sao Antao (Cabo Verde) from north to south
        pos_from = Position(0.297869, -0.43921) + PolarVector(0, 30000)
        pos_to = Position(0.297869, -0.43921) + PolarVector(math.pi, 30000)
        segment = (pos_from, pos_to - pos_from, pos_to)
        # First verify that we're hitting
        hit = self.map.hit(segment)
        self.assertTrue(hit, 'Expected island hit')

        outer_points = self.map.outer(segment)
        self.assertEquals(2, len(outer_points))
        self.assertTrue(not outer_points[0] is None \
                        and not outer_points[1] is None, \
                        'Island, so expected two ways to pass (both sides)')

        # ..now from south to north
        pos_from = Position(0.297869, -0.43921) + PolarVector(math.pi, 30000)
        pos_to = Position(0.297869, -0.43921) + PolarVector(0, 30000)
        segment = (pos_from, pos_to - pos_from, pos_to)
        # First verify that we're hitting
        hit = self.map.hit(segment)
        self.assertTrue(hit, 'Expected island hit')

        outer_points = self.map.outer(segment)
        self.assertEquals(2, len(outer_points))
        self.assertTrue(not outer_points[0] is None \
                        and not outer_points[1] is None, \
                        'Island, so expected two ways to pass (both sides)')


class TestMapPoint(unittest.TestCase):
    def setUp(self):
        self.point = MapPoint(0.5, 0.5)

    def testOtherLink(self):
        p1 = MapPoint(0.55, 0.5)
        p2 = MapPoint(0.5, 0.55)
        self.point.links.append(p1)
        self.point.links.append(p2)
        p = self.point.other_link(p1)
        self.assertTrue(p is p2, "Expected p2 to be the other link point")

if __name__ == '__main__':
    unittest.main()
