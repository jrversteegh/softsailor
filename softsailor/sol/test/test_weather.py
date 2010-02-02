import unittest

from softsailor.sol.weather import Weather
from softsailor.sol.settings import Settings

class TestWeather(unittest.TestCase):
    def testLoad(self):
        settings = Settings()
        weather = Weather()
        weather.load(settings)
        self.assertEqual(len(weather.reltimes), len(weather.frames))
        self.assertTrue(weather.lat_n > 0)
        self.assertEqual(weather.lat_n, len(weather.frames[0]))
        self.assertTrue(weather.lon_n > 0)
        self.assertEqual(weather.lon_n, len(weather.frames[0][0]))
