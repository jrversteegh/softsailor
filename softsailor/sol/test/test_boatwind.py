import unittest

from softsailor.sol.functions import *
from softsailor.sol.weather import *
from softsailor.sol.settings import *
from softsailor.sol.wind import *
from softsailor.boat import *
from softsailor.utils import *

class TestBoatWind(unittest.TestCase):
    def testBoatWindVersusWeather(self):
        settings = Settings()
        weather = Weather()
        weather.load(settings)
        wind = Wind(weather)

        boat = SailBoat()
        get_boat(boat)

        time = datetime.utcnow() # - timedelta(minutes = 30)

        boatwind = wind.get(boat.position, time)

        bw = rad_to_deg(boat.wind[0]), ms_to_knots(boat.wind[1])
        cw = rad_to_deg(boatwind[0]), ms_to_knots(boatwind[1])

        msg = 'Boat wind: ' + str(bw[0]) +  ', ' + str(bw[1]) + \
            '  Calc wind: ' + str(cw[0]) +  ', ' + str(cw[1])

        # Expect error of less than a degree
        self.failIf(abs(bw[0] - cw[0]) > 1, msg)

        # Expect error of less than two tenths of a knot
        self.failIf(abs(bw[1] - cw[1]) > 0.2, msg)
    

if __name__ == '__main__':
    unittest.main()
