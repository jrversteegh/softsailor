import unittest

from test_utils import *
from softsailor.sailor import *
from softsailor.boat import *
from softsailor.controller import *
from softsailor.updater import *
from softsailor.route import *
from softsailor.navigator import *
from softsailor.chart import *

class TestSailor(unittest.TestCase):
    def setUp(self):
        self.boat = SailBoat()
        self.boat.position = (1.0, 1.0)
        self.controller = BoatController(self.boat)
        self.updater = BoatUpdater(self.boat)
        self.chart = Chart()
        self.route = Route(((1.0, 1.0), (0.9, 1.0)))
        self.navigator = Navigator(route=self.route, boat=self.boat)
        self.sailor = Sailor(boat=self.boat, controller=self.controller, \
                updater=self.updater, navigator=self.navigator, chart=self.chart)

    def testHasSail(self):
        self.assertTrue(hasattr(self.sailor, 'sail'))
        self.assertTrue(hasattr(self.sailor.sail, '__call__'))

    def testAdjustHeadingForWind(self):
        h = 3
        c, h = self.sailor.adjust_heading_for_wind(h)

    def testHandleTackingAndGybing(self):
        h = 3
        b = (3, 3)
        c, h = self.sailor.handle_tacking_and_gybing(h, b)

    def testPreventBeaching(self):
        h = 3
        c, h = self.sailor.prevent_beaching(h)

    def testGetHeading(self):
        h = self.sailor.get_heading()


if __name__ == '__main__':
    unittest.main()

	
