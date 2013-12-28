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
        settings.polars.save_to_file('polar_data.txt')

        speed = performance.get_speed(boat.relative_wind)
        bs = ms_to_kn(boat.motion.speed)
        cs = ms_to_kn(speed) * boat.efficiency
        msg = 'Boat speed: ' + str(bs) + \
              '  Calc speed: ' + str(cs)
        
        # Test boat performance accuracy. Should be within a tenth of a knot.
        self.failIf(abs(bs - cs) > 0.1, msg)
    
if __name__ == '__main__':
    unittest.main()
