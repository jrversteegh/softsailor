import unittest
import testing_helper

from softsailor.boat import *
from softsailor.utils import *

from softsailor.sol.sol_functions import *
from softsailor.sol.sol_weather import *
from softsailor.sol.sol_settings import *
from softsailor.sol.sol_wind import *

class TestBoatWind(unittest.TestCase):
    def testBoatWindVersusWeather(self):
        settings = Settings()
        weather = Weather()
        weather.load(settings)
        wind = SolWind(weather)

        boat = SailBoat()
        fetch_boat(boat)

        time = datetime.utcnow() # - timedelta(minutes = 30)

        boatwind = wind.get(boat.position, time)

        bw = rad_to_deg(boat.condition.wind[0]), ms_to_kn(boat.condition.wind[1])
        cw = rad_to_deg(boatwind[0]), ms_to_kn(boatwind[1])

        msg = 'Boat wind: ' + str(bw[0]) +  ', ' + str(bw[1]) + \
            '  Calc wind: ' + str(cw[0]) +  ', ' + str(cw[1])

        # Expect error of less than two degrees
        self.failIf(abs(bw[0] - cw[0]) > 2, msg)

        # Expect error of less than a quarter of a knot
        self.failIf(abs(bw[1] - cw[1]) > 0.25, msg)
    

if __name__ == '__main__':
    unittest.main()
