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
        bs = ms_to_knots(boat.speed)
        cs = ms_to_knots(speed)
        msg = 'Boat speed: ' + str(bs) + \
              'Calc speed: ' + str(cs)
        
        # Test boat performance accuracy. Should be within 0.2 knots
        self.failIf(abs(bs - cs) > 0.2, msg)
    
