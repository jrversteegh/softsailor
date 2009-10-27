import unittest

from softsailor.sol.functions import *
from softsailor.sol.settings import *
from softsailor.sol.performance import *
from softsailor.boat import *

class TestBoatWind(unittest.TestCase):
    def testBoatSpeedVersusPerformance(self):
        boat = SailBoat()
        get_boat(boat)
        settings = Settings()
        performance = Performance(settings.polar_data)

        speed = performance.get(boat.relative_wind)
        self.assertAlmostEqual(boat.speed, speed, 1)
    
