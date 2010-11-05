import unittest

from softsailor.boat import *

from softsailor.sol.sol_functions import *
from softsailor.sol.sol_settings import *
from softsailor.sol.sol_performance import *


class TestBoatWind(unittest.TestCase):
    def testBoatSpeedVersusPerformance(self):
        boat = SailBoat()
        get_boat(boat)
        settings = Settings()
        performance = Performance(polar_data=settings.polar_data)

        speed = performance.get(boat.relative_wind)
        bs = ms_to_knots(boat.motion.speed)
        cs = ms_to_knots(speed)
        msg = 'Boat speed: ' + str(bs) + \
              '  Calc speed: ' + str(cs)
        
        # Test boat performance accuracy. Should be within quarter knot.
        self.failIf(abs(bs - cs) > 0.25, msg)
    
