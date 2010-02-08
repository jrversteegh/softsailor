import unittest
import test_utils

from softsailor.classes import *
from softsailor.sol.map import Map
from softsailor.sol.settings import Settings

class TestMap(unittest.TestCase):
    def setUp(self):
        self.map = Map()

    def testLoad(self):
        settings = Settings()
        self.map.load(settings.map)

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

if __name__ == '__main__':
    unittest.main()
