import unittest

from softsailor.sol.functions import *
from softsailor.sol.weather import *
from softsailor.sol.settings import *
from softsailor.sol.wind import *
from softsailor.boat import *

class TestBoatWind(unittest.TestCase):
    def testBoatWindVersusWeather(self):
        settings = Settings()
        weather = Weather()
        weather.load(settings)
        wind = Wind(weather)

        boat = SailBoat()
        get_boat(boat)

        boatwind = wind.get(boat.position, datetime.utcnow())

        self.assertAlmostEqual(boatwind[0], boat.wind[0], 1)
        self.assertAlmostEqual(boatwind[1], boat.wind[1], 1)
    
    def testBilinearVersusSplined(self):
        settings = Settings()
        weather = Weather()
        weather.load(settings)
        wind = Wind(weather)

        boat = SailBoat()
        get_boat(boat)

        bilinear_wind = wind.get_bilinear(boat.position, datetime.utcnow())
        splined_wind = wind.get_splined(boat.position, datetime.utcnow())

        self.assertAlmostEqual(bilinear_wind[0], splined_wind[0], 1)
        self.assertAlmostEqual(bilinear_wind[1], splined_wind[1], 1)
