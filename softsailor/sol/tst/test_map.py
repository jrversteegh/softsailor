import os
import unittest
import testing_helper


from softsailor.utils import *
from softsailor.route import Route
from softsailor.map import Path
from softsailor.sol.sol_map import *
from softsailor.sol.sol_settings import Settings

from geofun import Position, Vector

dirname = os.path.dirname(os.path.abspath(__file__))

try:
    value = os.environ['SOL_BROKEN_MAP']
    mapbroken = True
except KeyError:
    mapbroken = False

class TestFuncs(unittest.TestCase):
    def testIntersection(self):
        p1 = Position(0.99, 0.99)
        p2 = Position(0.99, 1.0)
        p3 = Position(1.0, 1.0)
        p4 = Position(1.0, 0.99) 
        # Square
        line1 = Line(p1, p2)
        line2 = Line(p2, p3)
        line3 = Line(p3, p4)
        line4 = Line(p4, p1)
        line5 = Line(p1, p3)
        # Cross
        line6 = Line(p2, p4)
        line7 = Line(p4, p2)

        pa = line5.intersection(line6)
        pb = line6.intersection(line5)
        pc = line5.intersection(line7)
        bb = pb - pa
        bc = pc - pa
        #print pos_to_str(pa)
        #print pos_to_str(pb), vec_to_str(bb)
        #print pos_to_str(pc), vec_to_str(bc)
        self.assertTrue(bb[1] < 200)
        self.assertTrue(bc[1] < 200)
        

class TestMap(unittest.TestCase):
    def setUp(self):
        self.map = SolMap()

    @unittest.skipIf(mapbroken, "Don't test because of broken map")
    @unittest.skipIf(testing_helper.offline, "Requires sailonline connection")
    def testLoad(self):
        settings = Settings()
        if settings.map != '':
            self.map.load(settings.map)
        else:
            self.assertTrue(settings.area[0] > -half_pi)
            self.map.load_tiles(settings.host, settings.tilemap, settings.area)
        for point in self.map.points:
            has_one_or_two_links = (len(point.links) == 1) \
                    or (len(point.links) == 2)
            self.assertTrue(has_one_or_two_links, \
                            "Expected each point to have one or two links: %s" % \
                            pos_to_str(point))

    def testHit(self):
        self.map.load(dirname + '/Canary_Brazil.xml')

        # Attempt to hit Sao Antao (Cabo Verde) from all sides
        pos_to = Position(0.297869, -0.43921)
        bearing = Vector(0, 30000)
        pos_from = pos_to - bearing
        segment = Line(pos_from, pos_to)
        hit = self.map.hit(segment)
        self.assertTrue(hit)

        bearing = Vector(1.57, 25000)
        pos_from = pos_to - bearing
        segment = Line(pos_from, pos_to)
        hit = self.map.hit(segment)
        self.assertTrue(hit)

        bearing = Vector(3.14, 25000)
        pos_from = pos_to - bearing
        segment = Line(pos_from, pos_to)
        hit = self.map.hit(segment)
        self.assertTrue(hit)

        bearing = Vector(4.71, 30000)
        pos_from = pos_to - bearing
        segment = Line(pos_from, pos_to)
        hit = self.map.hit(segment)
        self.assertTrue(hit)

        # This point is not on the island
        pos1 = Position(0.3019, -0.4363)
        pos2 = pos1 - bearing
        segment = Line(pos1, pos2)
        hit = self.map.hit(segment)
        self.assertFalse(hit)

    def testOuterPoints(self):
        self.map.load(dirname + '/Canary_Brazil.xml')
        # Attempt to pass Sao Antao (Cabo Verde) from north to south
        pos_from = Position(0.297869, -0.43921) + Vector(0, 30000)
        pos_to = Position(0.297869, -0.43921) + Vector(math.pi, 30000)
        segment = Line(pos_from, pos_to)
        # First verify that we're hitting
        hit = self.map.hit(segment)
        self.assertTrue(hit, 'Expected island hit')

        outer_points = self.map.route_around(segment)
        self.assertEquals(2, len(outer_points))
        self.assertTrue(not outer_points[0] is None \
                        and not outer_points[1] is None, \
                        'Island, so expected two ways to pass (both sides)')

        # ..now from south to north and the start a little offset to the east
        # so we'll also hit Sao Vicente
        pos_from = Position(0.297869, -0.43921) + Vector(math.pi - 0.2, 35000)
        pos_to = Position(0.297869, -0.43921) + Vector(0, 30000)
        segment = Line(pos_from, pos_to)
        # First verify that we're hitting
        hit = self.map.hit(segment)
        self.assertTrue(hit, 'Expected island hit')

        outer_points = self.map.route_around(segment)
        self.assertEquals(2, len(outer_points))
        route = Route(outer_points[0])
        route.save_to_kml(dirname + '/outer_points_first_0.kml')
        route = Route(outer_points[1])
        route.save_to_kml(dirname + '/outer_points_first_1.kml')

        outer_points = self.map.find_paths(segment)
        for i, points in enumerate(outer_points):
            path = Path(points)
            path.save_to_kml('result_%d.kml' % i)
        # Expected 3 lines around both islands
        self.assertTrue(len(outer_points) >= 3)

    def testSaveToKml(self):
        self.map.load(dirname + '/Gbr_Gtb.xml')
        self.map.save_to_kml(dirname + '/gbr_gtb.kml')
        self.map.load(dirname + '/Canary_Brazil.xml')
        self.map.save_to_kml(dirname + '/canary_brazil.kml')

    def testRouteAround(self):
        p1 = Position(*deg_to_rad(39.3082, 26.4316))
        p2 = Position(*deg_to_rad(39.3365, 26.4245))
        
        self.map.load(dirname + '/Turkey.xml') 
        l = Line(p1, p2)
        self.map.route_around(l)



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
