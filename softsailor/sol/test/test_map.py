import unittest

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
        # Attempt to hit Sao Antao (Cabo Verde)
        segment = ((3.66, 100000), (0.2985, -0.4398))
        hit = self.map.hit(segment)
        self.assertTrue(hit)
        segment = ((3.66, 100000), (0.3019, -0.4363))
        hit = self.map.hit(segment)
        self.assertFalse(hit)

