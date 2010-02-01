import unittest
import test_utils

from softsailor.sol.wind import *
from softsailor.utils import *
from softsailor.sol.weather import *
from softsailor.sol.settings import *

from datetime import datetime, timedelta

class TestWindOnline(unittest.TestCase):
    def setUp(self):
        settings = Settings()
        self.weather = Weather()
        self.weather.load(settings)
        self.wind = Wind(self.weather)

    def tearDown(self):
        self.wind = None
        self.weather = None

    def testBoatWind(self):
        pass

if __name__ == '__main__':
    unittest.main()
