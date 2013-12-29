import unittest
import testing_helper

from softsailor.boat import *

from softsailor.sol.sol_functions import *
from softsailor.sol.sol_settings import *
from softsailor.sol.sol_performance import *


class TestBoatWind(unittest.TestCase):
    @unittest.skipIf(testing_helper.offline, "Can't compare boat performance offline")
    def testBoatSpeedVersusPerformance(self):
        boat = SailBoat()
        fetch_boat(boat)
        settings = Settings()
        performance = Performance(polars=settings.polars)
        settings.polars.save_to_file('polars.txt')

        speed1 = performance.get_speed(boat.relative_wind)
        speed2 = settings.polars.get(boat.relative_wind)
        bs = ms_to_kn(boat.motion.speed)
        cs1 = ms_to_kn(speed1) * boat.efficiency
        cs2 = ms_to_kn(speed2) * boat.efficiency
        msg = 'Boat speed: ' + str(bs) + \
              '  Calc speed1: ' + str(cs1) + \
              '  Calc speed2: ' + str(cs2)
        
        # Test boat performance accuracy. Should be within a tenth of a knot.
        self.failIf(abs(bs - cs1) > 0.1, msg)
        self.failIf(abs(bs - cs2) > 0.1, msg)
    
if __name__ == '__main__':
    unittest.main()
